"""
MVP del Presidio DLP Challenge: anonimiza un .txt con Microsoft Presidio.

Uso:
    python main.py texto_original.txt texto_anonimizado.txt

Instalación (una vez, con internet; la ejecución final es offline):
    pip install presidio-analyzer presidio-anonymizer spacy
    python -m spacy download es_core_news_lg

Flujo:
    1. Leer el texto (UTF-8, sin tocar saltos de línea).
    2. ANALYZER: detectar entidades (NER de spaCy + reconocedores propios).
    3. Resolver solapamientos (una zona del texto solo recibe una etiqueta).
    4. ANONYMIZER: sustituir cada entidad por su etiqueta canónica.
    5. Escribir el resultado (UTF-8).
"""

import re
import sys

from presidio_analyzer import (
    AnalyzerEngine,
    EntityRecognizer,
    Pattern,
    PatternRecognizer,
    RecognizerRegistry,
    RecognizerResult,
)
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.predefined_recognizers import (
    EmailRecognizer,
    IbanRecognizer,
    SpacyRecognizer,
)
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

LANG = "es"

# Entidad de Presidio -> etiqueta exacta que exige el benchmark.
# Las claves que no vienen de Presidio (PHONE, DNI_NIE, SECRET) son
# nombres que damos nosotros a nuestros reconocedores propios.
ETIQUETAS = {
    "PERSON": "<PERSON>",
    "EMAIL_ADDRESS": "<EMAIL>",
    "PHONE": "<PHONE>",
    "DNI_NIE": "<DNI_NIE>",
    "IBAN_CODE": "<IBAN>",
    "SECRET": "<SECRET>",
}


# ---------------------------------------------------------------------------
# RECONOCEDORES PROPIOS
# ---------------------------------------------------------------------------

class DniNieRecognizer(PatternRecognizer):
    """DNI (8 dígitos + letra) y NIE (X/Y/Z + 7 dígitos + letra).

    La regex solo propone candidatos; validate_result comprueba la letra de
    control. Así un "12345678A" inventado que no cuadra NO se anonimiza
    (típico caso trampa de un benchmark).
    """

    LETRAS = "TRWAGMYFPDXBNJZSQVHLCKE"

    def __init__(self):
        patron = Pattern(
            "dni_nie",
            r"\b(?:\d{8}|[XYZxyz]\d{7})[- ]?[A-Za-z]\b",
            0.5,
        )
        super().__init__(
            supported_entity="DNI_NIE",
            patterns=[patron],
            supported_language=LANG,
        )

    def validate_result(self, pattern_text: str):
        # True -> se acepta con score máximo; False -> se descarta.
        t = re.sub(r"[- ]", "", pattern_text).upper()
        numero, letra = t[:-1], t[-1]
        # En el NIE la letra inicial se cambia por un dígito: X=0, Y=1, Z=2
        numero = numero.translate(str.maketrans("XYZ", "012"))
        return self.LETRAS[int(numero) % 23] == letra


class PhoneEsRecognizer(PatternRecognizer):
    """Teléfonos españoles: móviles/fijos de 9 dígitos, con o sin +34."""

    def __init__(self):
        patron = Pattern(
            "tel_es",
            r"(?<![\w+])(?:(?:\+|00)34[ .-]?)?[6-9]\d{2}[ .-]?\d{3}[ .-]?\d{3}(?!\w)",
            0.6,
        )
        super().__init__(
            supported_entity="PHONE",
            patterns=[patron],
            supported_language=LANG,
        )


class SecretRecognizer(EntityRecognizer):
    """Contraseñas, tokens y credenciales.

    Dos señales:
      a) CONTEXTO: palabra clave ("password", "clave"...) seguida de ":", "=" o
         "es" -> el secreto es el VALOR, no la palabra clave.
      b) FORMATO: prefijos típicos de tokens (sk-..., ghp_..., AKIA...).
    Es una clase propia (no PatternRecognizer) para poder devolver solo el
    valor y no la palabra clave que lo precede.
    """

    CLAVE = re.compile(
        r"(?i)\b(?:password|passwd|pwd|contraseña|contrasena|clave|token|"
        r"api[_ -]?key|secret|secreto)\b"
        r"(?:\s*[:=]\s*|\s+es\s+)[\"']?(?P<valor>[^\s\"',;]+)"
    )
    FORMATO = re.compile(r"\b(?:sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b")

    def __init__(self):
        super().__init__(supported_entities=["SECRET"], supported_language=LANG)

    def load(self):  # método obligatorio de la clase base; no necesitamos cargar nada
        pass

    def analyze(self, text, entities, nlp_artifacts=None):
        resultados = []
        for m in self.CLAVE.finditer(text):
            resultados.append(RecognizerResult("SECRET", m.start("valor"), m.end("valor"), 0.9))
        for m in self.FORMATO.finditer(text):
            resultados.append(RecognizerResult("SECRET", m.start(), m.end(), 0.95))
        return resultados


# ---------------------------------------------------------------------------
# CONSTRUCCIÓN DEL MOTOR
# ---------------------------------------------------------------------------

def construir_analyzer() -> AnalyzerEngine:
    # Motor NLP: modelo spaCy en español, cargado desde local (offline).
    nlp_engine = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": LANG, "model_name": "es_core_news_lg"}],
    }).create_engine()

    # Registro explícito: solo los reconocedores que queremos, sin sorpresas.
    registry = RecognizerRegistry(supported_languages=[LANG])
    registry.add_recognizer(SpacyRecognizer(supported_language=LANG))  # NER -> PERSON
    registry.add_recognizer(EmailRecognizer(supported_language=LANG))
    registry.add_recognizer(IbanRecognizer(supported_language=LANG))   # valida checksum
    registry.add_recognizer(DniNieRecognizer())
    registry.add_recognizer(PhoneEsRecognizer())
    registry.add_recognizer(SecretRecognizer())

    return AnalyzerEngine(
        registry=registry, nlp_engine=nlp_engine, supported_languages=[LANG]
    )


def resolver_solapamientos(resultados):
    """Si dos detecciones se pisan, gana la de mayor score (y luego la más larga).

    Ejemplo: dígitos de un IBAN que parecen un teléfono. Sin esto, el texto
    saldría con etiquetas mezcladas.
    """
    elegidos = []
    for r in sorted(resultados, key=lambda r: (-r.score, -(r.end - r.start))):
        if all(r.end <= e.start or r.start >= e.end for e in elegidos):
            elegidos.append(r)
    return elegidos


def anonimizar(texto: str, analyzer: AnalyzerEngine) -> str:
    # 1) Detectar
    detectados = analyzer.analyze(
        text=texto,
        language=LANG,
        entities=list(ETIQUETAS.keys()),  # ignora todo lo que no esté en la política
        score_threshold=0.5,              # AJUSTAR con tus pruebas (sube = menos FP)
    )
    detectados = resolver_solapamientos(detectados)

    # 2) Sustituir por la etiqueta canónica
    operadores = {
        entidad: OperatorConfig("replace", {"new_value": etiqueta})
        for entidad, etiqueta in ETIQUETAS.items()
    }
    return AnonymizerEngine().anonymize(
        text=texto, analyzer_results=detectados, operators=operadores
    ).text


# ---------------------------------------------------------------------------
# PUNTO DE ENTRADA
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print("Uso: python main.py entrada.txt salida.txt", file=sys.stderr)
        sys.exit(2)
    ruta_in, ruta_out = sys.argv[1], sys.argv[2]

    try:
        # newline="" conserva tal cual los saltos de línea (\n o \r\n).
        with open(ruta_in, encoding="utf-8", newline="") as f:
            texto = f.read()

        resultado = anonimizar(texto, construir_analyzer())

        with open(ruta_out, "w", encoding="utf-8", newline="") as f:
            f.write(resultado)
        print(f"OK: {ruta_in} -> {ruta_out}")
    except Exception as e:  # cualquier fallo: mensaje por stderr y código != 0
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()