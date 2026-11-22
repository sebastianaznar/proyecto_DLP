
# Presidio DLP Challenge

## 1. Descripción del proyecto

Desarrollo de un motor de anonimización avanzada de información sensible utilizando Microsoft Presidio y técnicas de procesamiento del lenguaje natural (NLP).

El objetivo es identificar información confidencial dentro de documentos de texto y sustituirla automáticamente por etiquetas normalizadas, conservando el contenido que no necesita protección.

El sistema procesa archivos TXT completos codificados en UTF-8.

## 2. Objetivos

- Detectar información personal y confidencial.
- Anonimizar automáticamente los datos sensibles.
- Conservar el contenido no sensible.
- Incorporar reconocimiento lingüístico mediante NLP/NER.
- Desarrollar reconocedores personalizados.
- Reducir falsos positivos y falsos negativos.
- Permitir la ejecución completamente offline.

## 3. Tecnologías utilizadas

- **Python:** lenguaje principal.
- **Microsoft Presidio Analyzer:** detección de información sensible.
- **Microsoft Presidio Anonymizer:** sustitución de entidades detectadas.
- **spaCy:** procesamiento del lenguaje natural y reconocimiento de entidades.
- **Regular Expressions:** apoyo para reconocer formatos estructurados.

## 4. Estructura del proyecto

```text
PRESIDIO_DLP/
│
├── main.py
├── requirements.txt
├── README.md
│
├── recognizers/
│   ├── __init__.py
│   └── custom_recognizers.py
│
└── ejemplos/
    └── texto_original.txt
```

## 5. Instalación



### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Descargar modelo NLP de español

```bash
python -m spacy download es_core_news_md
```

El modelo debe estar descargado localmente antes de ejecutar el programa sin conexión a Internet.

## 6. Categorías de información sensible

El motor contempla las siguientes categorías:

| Entidad | Etiqueta de anonimización |
|---|---|
| PERSON | `<PERSON>` |
| EMAIL_ADDRESS | `<EMAIL>` |
| PHONE_NUMBER | `<PHONE>` |
| DNI_NIE | `<DNI_NIE>` |
| IBAN | `<IBAN>` |
| SECRET | `<SECRET>` |

Las etiquetas son deterministas y siguen el formato establecido en el enunciado del Presidio DLP Challenge.

## 7. Funcionamiento del motor

El sistema sigue el siguiente flujo de procesamiento:

1. Recibe la ruta del archivo TXT original.
2. Lee el contenido utilizando codificación UTF-8.
3. Procesa el texto mediante spaCy.
4. Presidio Analyzer identifica las posibles entidades sensibles.
5. Se aplican los reconocedores personalizados.
6. Presidio Anonymizer sustituye las entidades detectadas.
7. Se genera un nuevo archivo TXT con el contenido anonimizado.

## 8. Ejecución

El programa utiliza dos argumentos:

- Archivo de entrada.
- Archivo de salida.

Comando obligatorio:

```bash
python main.py texto_original.txt texto_anonimizado.txt
```

Ejemplo utilizando los archivos del proyecto:

```bash
python main.py ejemplos/texto_original.txt ejemplos/texto_anonimizado.txt
```

El programa funciona de forma autónoma, sin interacción humana durante el procesamiento.

## 9. Reconocedores personalizados

El proyecto incorpora reconocedores adicionales para ampliar las capacidades de Presidio.

Se contemplan los siguientes casos:

- DNI y NIE españoles.
- IBAN.
- Contraseñas y credenciales.
- Tokens de autenticación.
- Teléfonos españoles.

Además, se utiliza spaCy como motor NLP para apoyar el reconocimiento de nombres de personas.

Los reconocedores se podrán ampliar y ajustar durante la experimentación para mejorar la precisión de las detecciones.

## 10. Evaluación y experimentación

La evaluación del motor se realizará mediante las métricas:

- **Precision:** proporción de detecciones realizadas que son correctas.
- **Recall:** proporción de entidades sensibles existentes que han sido detectadas.
- **F1-score:** equilibrio entre Precision y Recall.

Se realizarán pruebas con información sintética que incluyan:

- Casos positivos: información sensible que debe anonimizarse.
- Casos negativos: información que debe conservarse.
- Casos ambiguos: información cuyo contexto puede generar errores de detección.

También se compararán distintas configuraciones del motor para comprobar las mejoras introducidas.

## 11. Ejecución offline

El proyecto está diseñado para ejecutarse localmente.

Una vez instaladas las dependencias y descargados los modelos necesarios, el procesamiento no requiere:

- Conexión a Internet.
- Servicios cloud.
- APIs externas.
- Modelos alojados remotamente.
- Consultas a servicios de inteligencia artificial externos.

## 12. Limitaciones conocidas

- La detección de nombres depende del modelo NLP y del contexto.
- Los reconocedores estructurados pueden generar falsos positivos.
- La detección de IBAN requiere validaciones adicionales, como el checksum.
- La identificación de secretos depende de los patrones y contextos configurados.
- Es necesario realizar pruebas experimentales para ajustar los umbrales de detección.

## 13. Trabajo futuro

- Mejorar los reconocedores personalizados.
- Incorporar validaciones adicionales para DNI, NIE e IBAN.
- Reducir falsos positivos y falsos negativos.
- Ampliar los contextos de reconocimiento.
- Comparar diferentes configuraciones NLP.
- Implementar pruebas automatizadas.
- Evaluar el rendimiento mediante Precision, Recall y F1-score.
- Validar la ejecución offline en un entorno limpio.

## 14. Uso de Inteligencia Artificial

Las herramientas de inteligencia artificial utilizadas como apoyo al desarrollo se documentarán en la memoria técnica, indicando su finalidad y los procedimientos empleados para verificar los resultados.

