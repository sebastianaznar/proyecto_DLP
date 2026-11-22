
import argparse
import sys
from pathlib import Path

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from recognizers.custom_recognizers import build_analyzer


# Etiquetas oficiales exigidas por el profesor
CANONICAL_LABELS = {
    "PERSON": "<PERSON>",
    "EMAIL_ADDRESS": "<EMAIL>",
    "PHONE_NUMBER": "<PHONE>",
    "DNI_NIE": "<DNI_NIE>",
    "IBAN": "<IBAN>",
    "SECRET": "<SECRET>"
}


def anonymize_text(text, analyzer=None):

    # Crear el motor de detección
    if analyzer is None:
        analyzer = build_analyzer()

    # Crear el motor de anonimización
    anonymizer = AnonymizerEngine()

    # Detectar las entidades sensibles
    results = analyzer.analyze(
        text=text,
        language="es",
        entities=list(CANONICAL_LABELS.keys())
    )

    # Configurar las sustituciones
    operators = {
        entity: OperatorConfig(
            "replace",
            {"new_value": label}
        )
        for entity, label in CANONICAL_LABELS.items()
    }

    # Anonimizar el texto
    result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )

    return result.text


def main():

    parser = argparse.ArgumentParser(
        description="Motor de anonimización DLP con Presidio"
    )

    parser.add_argument(
        "input_file",
        help="Archivo TXT original"
    )

    parser.add_argument(
        "output_file",
        help="Archivo TXT anonimizado"
    )

    args = parser.parse_args()

    try:

        input_path = Path(args.input_file)
        output_path = Path(args.output_file)

        if not input_path.is_file():
            raise FileNotFoundError(
                f"No existe el archivo: {input_path}"
            )

        # Leer archivo original
        original_text = input_path.read_text(
            encoding="utf-8"
        )

        # Anonimizar
        anonymized_text = anonymize_text(original_text)

        # Crear directorio de salida si no existe
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Guardar resultado
        output_path.write_text(
            anonymized_text,
            encoding="utf-8"
        )

        print("Anonimización completada correctamente.")
        print(f"Archivo generado: {output_path}")

        return 0

    except Exception as error:

        print(
            f"ERROR: {error}",
            file=sys.stderr
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
