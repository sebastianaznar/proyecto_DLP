"""Filtro DLP previo al envío de prompts a un servicio de IA externo.

Inspecciona cada prompt con el motor de anonimización (Presidio) y aplica una política:
  - BLOQUEAR   si contiene datos de alto riesgo (credenciales, IBAN, DNI/NIE).
  - ANONIMIZAR si solo contiene otros datos personales (nombre, correo, teléfono).
  - PASAR      si no se detecta nada.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

from main import anonymize_text, CANONICAL_LABELS
from recognizers.custom_recognizers import build_analyzer

ALTO_RIESGO = {"SECRET", "IBAN", "DNI_NIE"}
LOG = Path("auditoria_dlp.log")

EJEMPLOS = [
    "Resume este correo de la clienta Ana García (ana.garcia@example.com), teléfono 612 34 56 78.",
    "Revisa este fallo: la contraseña: Hunter2024 no funciona en el servidor.",
    "Prepara una transferencia a ES91 2100 0418 4502 0005 1332 por la factura FAC-2026-0099.",
    "Explícame cómo funciona un índice hash en una base de datos.",
    "El cliente Luis Pérez con DNI 12345678Z pide un duplicado de su contrato.",
]


def decidir(tipos):
    if tipos & ALTO_RIESGO:
        return "BLOQUEAR"
    return "ANONIMIZAR" if tipos else "PASAR"


def enviar_a_ia_externa(texto):
    # Servicio externo simulado: aquí iría la llamada real a la API de la IA.
    print(f"  Enviado a la IA externa: {texto}")


def registrar(decision, tipos):
    # Auditoría: solo se guardan los tipos detectados, nunca los valores sensibles.
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} | {decision} | {sorted(tipos)}\n")


def procesar(prompt, analyzer):
    resultados = analyzer.analyze(
        text=prompt, language="es", entities=list(CANONICAL_LABELS)
    )
    tipos = {r.entity_type for r in resultados}
    decision = decidir(tipos)

    print(f"\nPrompt original: {prompt}")
    print(f"  Datos detectados: {sorted(tipos) or 'ninguno'}")
    print(f"  Decisión: {decision}")

    if decision == "BLOQUEAR":
        print("  Envío bloqueado: el prompt contiene datos de alto riesgo.")
    elif decision == "ANONIMIZAR":
        enviar_a_ia_externa(anonymize_text(prompt, analyzer))
    else:
        enviar_a_ia_externa(prompt)

    registrar(decision, tipos)
    return decision


def modo_interactivo(analyzer):
    print("Modo interactivo. Escribe un prompt y pulsa Enter. Para terminar: salir")
    while True:
        try:
            prompt = input("\nPrompt> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if prompt.lower() in {"salir", "exit", "q"}:
            break
        if prompt:
            procesar(prompt, analyzer)


def main():
    parser = argparse.ArgumentParser(
        description="Filtro DLP para prompts dirigidos a una IA externa"
    )
    parser.add_argument("archivo", nargs="?", help="archivo de texto con un prompt a filtrar")
    parser.add_argument("-i", "--interactivo", action="store_true",
                        help="escribir prompts por terminal")
    args = parser.parse_args()

    try:
        analyzer = build_analyzer()
        if args.interactivo:
            modo_interactivo(analyzer)
        elif args.archivo:
            procesar(Path(args.archivo).read_text(encoding="utf-8"), analyzer)
        else:
            for prompt in EJEMPLOS:
                procesar(prompt, analyzer)
        return 0
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())