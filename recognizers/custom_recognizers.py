
from presidio_analyzer import (
    AnalyzerEngine,
    Pattern,
    PatternRecognizer
)
from presidio_analyzer.nlp_engine import NlpEngineProvider


def build_analyzer():

    # 1. Configurar el motor NLP de spaCy en español
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {
                "lang_code": "es",
                "model_name": "es_core_news_md"
            }
        ]
    }

    provider = NlpEngineProvider(
        nlp_configuration=configuration
    )

    nlp_engine = provider.create_engine()

    # 2. Inicializar Presidio Analyzer
    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        supported_languages=["es"]
    )

    # ------------------------------------------------
    # 3. RECONOCEDOR DNI Y NIE
    # ------------------------------------------------

    dni_patterns = [
        Pattern(
            name="dni_espanol",
            regex=r"\b\d{8}[A-HJ-NP-TV-Z]\b",
            score=0.85
        ),
        Pattern(
            name="nie_espanol",
            regex=r"\b[XYZ]\d{7}[A-HJ-NP-TV-Z]\b",
            score=0.90
        )
    ]

    dni_recognizer = PatternRecognizer(
        supported_entity="DNI_NIE",
        patterns=dni_patterns,
        context=[
            "DNI",
            "NIE",
            "documento",
            "identidad",
            "identificación"
        ],
        supported_language="es"
    )

    analyzer.registry.add_recognizer(dni_recognizer)

    # ------------------------------------------------
    # 4. RECONOCEDOR IBAN
    # ------------------------------------------------

    iban_recognizer = PatternRecognizer(
        supported_entity="IBAN",
        patterns=[
            Pattern(
                name="iban_es",
                regex=r"\bES\d{2}(?:\s?\d{4}){5}\b",
                score=0.90
            ),
            Pattern(
                name="iban_internacional",
                regex=r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]){11,30}\b",
                score=0.80
            )
        ],
        context=[
            "IBAN",
            "cuenta bancaria",
            "transferencia",
            "cuenta"
        ],
        supported_language="es"
    )

    analyzer.registry.add_recognizer(iban_recognizer)

    # ------------------------------------------------
    # 5. RECONOCEDOR DE CONTRASEÑAS Y SECRETOS
    # ------------------------------------------------

    secret_recognizer = PatternRecognizer(
        supported_entity="SECRET",
        patterns=[
            Pattern(
                name="password",
                regex=r"""(?i)\b(?:password|passwd|contraseña|contrasena|clave|token|secret|api[_-]?key)\s*[:=]\s*['"]?[A-Za-z0-9_\-./+=]{6,}['"]?""",
                score=0.95
            ),
            Pattern(
                name="bearer_token",
                regex=r"(?i)\bBearer\s+[A-Za-z0-9\-._~+/]+=*",
                score=0.95
            )
        ],
        context=[
            "password",
            "contraseña",
            "token",
            "secret",
            "clave",
            "api key"
        ],
        supported_language="es"
    )

    analyzer.registry.add_recognizer(secret_recognizer)

    # ------------------------------------------------
    # 6. RECONOCEDOR DE TELÉFONOS ESPAÑOLES
    # ------------------------------------------------

    phone_recognizer = PatternRecognizer(
        supported_entity="PHONE_NUMBER",
        patterns=[
            Pattern(
                name="telefono_espanol",
                regex=r"(?<!\d)(?:\+34[\s.-]?)?[6789]\d{2}(?:[\s.-]?\d{2}){3}(?!\d)",
                score=0.80
            )
        ],
        context=[
            "teléfono",
            "telefono",
            "móvil",
            "movil",
            "contacto"
        ],
        supported_language="es"
    )

    analyzer.registry.add_recognizer(phone_recognizer)

    return analyzer
