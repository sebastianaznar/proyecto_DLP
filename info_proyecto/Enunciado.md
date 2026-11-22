# Trabajo de asignatura: Presidio DLP Challenge — Anonimización avanzada e integración de una solución DLP

## Objetivo del trabajo

El objetivo de esta actividad es que los estudiantes **diseñen, desarrollen, evalúen e integren una solución de protección de información sensible utilizando Microsoft Presidio**.

En el *Secret Hunter Challenge* el reto consistía en identificar si un fragmento de texto contenía secretos. En esta segunda actividad, el problema avanza un paso: **recibir un texto completo, identificar los datos sensibles que contiene y devolver ese mismo texto correctamente anonimizado**, preservando el contenido que no debe modificarse.

Además, cada equipo deberá **integrar el motor de anonimización en una solución DLP funcional** (*Data Loss Prevention*) que responda a un caso de uso realista de su elección.

La actividad mantiene el enfoque de resolución de problemas, desarrollo de herramientas propias, experimentación, demostración y competición. La complejidad técnica deberá estar justificada por la utilidad y el funcionamiento de la solución, no por la acumulación de tecnologías.

---

## Vinculación con ISO/IEC 27001:2022 — Control A.8.12 (Data Leakage Prevention)

Esta actividad se plantea como un **caso práctico de aplicación del control A.8.12 del Anexo A de ISO/IEC 27001:2022: prevención de fuga de datos (Data Leakage Prevention, DLP)**. Su finalidad es contribuir a prevenir la divulgación o extracción no autorizada de información sensible de los sistemas, redes y dispositivos que la tratan.

La orientación de **ISO/IEC 27002:2022, apartado 8.12**, destaca tres capacidades complementarias: **identificar la información que debe protegerse, detectar los canales por los que podría divulgarse y actuar preventivamente sobre esa exposición**. La actividad lleva estas capacidades a un prototipo demostrable; **no pretende acreditar por sí sola la implantación completa del control ni la conformidad de una organización con ISO/IEC 27001**.

### Relación entre los bloques de la actividad y los controles

| Trabajo realizado | Referencia ISO/IEC 27001:2022 | Evidencia que debe aportar el equipo |
|---|---|---|
| Identificar qué datos son sensibles y cuáles deben conservarse | **A.5.12 — Clasificación de la información** | Criterios de sensibilidad y justificación de la política aplicada |
| Detectar y anonimizar el texto del benchmark | **A.8.11 — Enmascaramiento de datos**, como técnica de protección; contribuye a **A.8.12** | Archivo anonimizado y resultados de detección y sustitución (Precision, Recall y F1) |
| Integrar Presidio en un flujo realista de salida o intercambio de información | **A.8.12 — Prevención de fuga de datos** | Canal de exposición, punto de inspección, tratamiento preventivo y demostración funcional |
| Tratar información personal identificable | **A.5.34 — Privacidad y protección de información personal identificable (PII)** | Alcance de datos personales tratados y medidas de protección adoptadas |

### Requisito de vinculación para la integración DLP (20 %)

Cada equipo deberá **explicar y demostrar**, dentro de su caso de uso elegido:

1. **Qué información protege** y por qué resulta sensible en ese contexto.
2. **Por qué canal o proceso podría producirse la fuga**: envío de correo, subida de documentos, intercambio con servicios de IA, exportación de logs, compartición de archivos u otro escenario justificado.
3. **En qué momento interviene Presidio** para inspeccionar el contenido **antes de la exposición** o entrega a un destinatario no autorizado.
4. **Qué medida preventiva aplica** su solución: generar una copia anonimizada, bloquear el envío, solicitar revisión o aplicar una política equivalente, según el riesgo y la finalidad del caso de uso.
5. **Cómo comprueba que funciona** mediante una prueba con información sintética en la que se observe el texto o documento original y el resultado de la intervención.

La elección del canal, la arquitectura y las funcionalidades avanzadas es libre. **No se exige OCR, procesamiento de imágenes, correo electrónico, ni una interfaz gráfica**, pero sí un flujo de protección operativo, no únicamente un anonimizador aislado presentado como si fuera una solución DLP completa.

La memoria incluirá una breve **justificación de la correspondencia con A.8.12**, y la demostración mostrará la medida preventiva elegida. Esta vinculación se valorará **dentro de los criterios ya existentes de la integración del 20 %**, sin crear un apartado de nota adicional.

**Referencias:**

- [ISO/IEC 27001:2022 — Sistemas de gestión de seguridad de la información (ISO)](https://www.iso.org/es/norma/27001)
- [ISO/IEC 27002:2022 — Controles de seguridad de la información (ISO)](https://www.iso.org/es/contents/data/standard/07/56/75652.html)
- [ISACA — Guía al control 8.12 de ISO/IEC 27002:2022](https://www.isaca.org/resources/news-and-trends/newsletters/atisaca/2023/volume-12/a-guide-to-the-updated-iso-iec-27002-2022-standard-part-2)

---

## Duración, organización y alcance

- **Duración:** dos semanas.
- **Organización:** por parejas.
- **Tecnología base obligatoria:** Microsoft Presidio, utilizado desde Python.
- **Benchmark común:** anonimización de **un archivo de texto completo** (`.txt`, UTF-8).
- **Integración DLP:** caso de uso y funcionalidades a elección del equipo; pueden incluir documentos, imágenes, OCR u otras capacidades.
- **Resultado esperado:** prototipo funcional, reproducible y técnicamente justificado; no se exige una solución lista para producción.

No es necesario entrenar un modelo desde cero, desplegar infraestructura cloud ni desarrollar una interfaz gráfica. Tampoco se exige que todos los equipos implementen las mismas funcionalidades avanzadas.

Se valorará la aportación técnica propia, la calidad de las decisiones, el trabajo experimental y la capacidad de integración.

---

# Planteamiento del problema

Una organización necesita reducir la exposición de datos personales y otra información confidencial antes de compartir documentos, enviar mensajes, registrar incidencias o utilizar servicios externos.

Un sistema de anonimización útil debe resolver **dos problemas a la vez**:

1. **Proteger** la información sensible que no debe divulgarse.
2. **Conservar** el contenido legítimo, sin eliminar datos innecesariamente ni destruir el sentido del texto.

Por ejemplo, para el texto original:

> La clienta Ana García tiene el correo ana@example.com. Su expediente es EXP-2026-458.

La salida esperada sería:

> La clienta `<PERSON>` tiene el correo `<EMAIL>`. Su expediente es EXP-2026-458.

En este ejemplo, el nombre y el correo son sensibles, mientras que el identificador de expediente se considera no sensible **según la política definida para la actividad**.

La dificultad del challenge no consiste simplemente en sustituir cadenas que parezcan números o nombres. Habrá información que se parece a un dato sensible pero no lo es, nombres ambiguos, textos con varios datos sensibles y casos en los que una detección incorrecta modifica contenido que debería conservarse.

---

# Parte I. Motor de anonimización para el benchmark — 30 %

## 1. Uso obligatorio de Microsoft Presidio

El motor deberá utilizar **Presidio Analyzer** para el reconocimiento de entidades y **Presidio Anonymizer** —o una integración equivalente basada en sus resultados— para generar el texto protegido.

Se deberá configurar o extender Presidio para el idioma y los tipos de información definidos en la actividad. Las decisiones técnicas deben documentarse y poder reproducirse.

### Requisito de reconocimiento avanzado

**No se admitirán soluciones cuya lógica principal de detección consista únicamente en expresiones regulares, palabras clave o listas de coincidencias.**

La solución deberá integrar **al menos un mecanismo de reconocimiento lingüístico o contextual basado en NLP/NER**, junto con una **aportación propia y comprobable** al motor de detección, tratamiento de entidades o anonimización.

Son opciones válidas, entre otras:

- NER con spaCy, Stanza o Transformers, integrado con Presidio.
- Reconocedores personalizados que incorporen análisis contextual u otra lógica avanzada.
- Combinación de modelos NLP con reconocedores estructurados de Presidio.
- Ajuste y combinación justificados de reconocedores, umbrales, contextos y operadores de anonimización.

**Las regex sí pueden utilizarse como apoyo**, especialmente para formatos estructurados, pero **un detector basado solo en regex no cumple el requisito técnico**. Tampoco es suficiente instalar Presidio y ejecutarlo sin ninguna configuración, adaptación o mejora propia.

No se premiará automáticamente un modelo por ser más complejo: deberá funcionar, estar integrado y aportar una mejora razonada.

## 2. Categorías de información sensible

El benchmark utilizará un catálogo **cerrado y publicado antes del desarrollo**. Como categorías iniciales del reto se establecen:

| Etiqueta obligatoria | Información que protege |
|---|---|
| `<PERSON>` | Nombres de personas físicas cuando el contexto indica que identifican a alguien |
| `<EMAIL>` | Direcciones de correo electrónico personales o asociadas a personas |
| `<PHONE>` | Números de teléfono personales |
| `<DNI_NIE>` | Identificadores personales españoles de tipo DNI/NIE |
| `<IBAN>` | Números de cuenta bancaria en formato IBAN |
| `<SECRET>` | Contraseñas, tokens y credenciales de acceso |

El profesor facilitará ejemplos de la política de etiquetado, incluyendo **excepciones y casos ambiguos**. Una cadena solo deberá anonimizarse cuando la política del reto lo exija. No toda cifra, nombre de producto, referencia documental o cadena aleatoria es un dato sensible.

En el benchmark las sustituciones serán **deterministas y canónicas**, con las etiquetas exactas de la tabla. No se aceptarán como equivalentes máscaras arbitrarias, asteriscos, pseudónimos inventados ni otras etiquetas, aunque puedan ser adecuados en una solución DLP real. Esta restricción se aplica al **benchmark automatizado**, no a las funciones adicionales de la integración.

## 3. Formato obligatorio de entrada y salida

Para el benchmark **no se utilizarán JSON, JSONL ni ficheros de predicciones**.

El profesor entregará un archivo de texto completo, que podrá contener párrafos, listados, correos, fragmentos de incidencias, mensajes y documentación simulada. El programa deberá generar otro archivo de texto con el mismo contenido, salvo por las sustituciones necesarias para anonimizarlo.

La ejecución obligatoria será:

```bash
python main.py texto_original.txt texto_anonimizado.txt
```

La aplicación deberá:

1. Leer el archivo de entrada indicado en el primer argumento, codificado en **UTF-8**.
2. Analizar y anonimizar automáticamente el contenido mediante su integración con Presidio.
3. Escribir el resultado en el archivo indicado en el segundo argumento, también en **UTF-8**.
4. Utilizar **exclusivamente** las etiquetas de sustitución acordadas para el benchmark.
5. Mantener el orden de las frases, la estructura, los signos, los saltos de párrafo y el contenido no sensible.
6. Procesar el archivo completo sin interacción humana, ventanas, preguntas ni configuración manual durante la ejecución.
7. Finalizar con código de salida `0` cuando termine correctamente; ante un error, finalizar con código distinto de `0` y explicar el problema por `stderr`.
8. Permitir repetir la ejecución con diferentes rutas de entrada y salida.

La salida estándar (`stdout`) podrá incluir información diagnóstica, pero **no sustituirá al archivo de salida**.

En el benchmark no se permitirá corregir manualmente el resultado ni conocer las anotaciones del oráculo.

## 4. Ejecución completamente offline

Durante la evaluación:

- No se permitirán conexiones a Internet, servicios cloud, consultas a APIs externas ni llamadas a LLM remotos.
- Todos los modelos, pesos, vocabularios, paquetes y demás recursos necesarios deberán estar disponibles localmente antes de comenzar.
- La aplicación deberá poder ejecutarse con el entorno y las dependencias documentados en el `README`.
- Todos los equipos serán evaluados en una máquina de referencia y bajo condiciones equivalentes, anunciadas antes de la entrega.

La falta de una interfaz gráfica o web no será penalizada en el benchmark. El requisito es que **el comando anterior funcione de forma autónoma**.

Si la entrega no permite ejecutar el benchmark, se registrará la incidencia y se seguirá el procedimiento de subsanación comunicado antes del comienzo del reto. No se modificará la lógica de detección ni se optimizará el código de ningún equipo por parte del profesor.

---

# Benchmark automático con texto oráculo

## 5. Texto de desarrollo y texto privado

Durante el desarrollo, los equipos podrán utilizar ejemplos facilitados en clase y las herramientas de prueba de **Presidio Research** para experimentar con reconocedores y analizar sus errores.

El reto final consistirá en **un texto privado completo**, preparado por el profesor, con una combinación de:

- Datos sensibles de las categorías publicadas.
- Fragmentos con varios datos sensibles.
- Elementos no sensibles con apariencia similar a datos personales.
- Referencias internas, valores técnicos y documentación ficticia que deben conservarse.
- Variaciones razonables de formato y contexto, coherentes con los ejemplos de desarrollo.

El texto de evaluación será diferente de los ejemplos utilizados en el desarrollo. Se utilizarán datos ficticios o sintéticos, no datos personales reales.

## 6. El oráculo del profesor

El profesor conservará **el texto original, la versión anonimizada correcta y la anotación de los fragmentos sensibles y no sensibles**. Las anotaciones permitirán identificar qué partes deben sustituirse y cuáles deben permanecer intactas.

Los estudiantes solo recibirán el archivo original. No tendrán acceso a la versión anonimizada correcta ni a las anotaciones privadas.

El objetivo es evaluar el **resultado anonimizado**, no exigir a los equipos que entreguen listas de entidades, posiciones, probabilidades ni ficheros intermedios.

## 7. Métrica y nota del benchmark

El **100 % de la puntuación del benchmark** se determinará mediante una única métrica: **F1-score de anonimización**, calculada al comparar el texto anonimizado entregado por el equipo con el oráculo del profesor.

El evaluador utilizará el texto original y las anotaciones privadas del oráculo para identificar cada sustitución efectuada. Una detección solo se considerará correcta cuando anonimice **el fragmento sensible completo y con la etiqueta canónica exigida**.

- **TP (verdadero positivo):** fragmento sensible correctamente anonimizado con su etiqueta.
- **FN (falso negativo):** fragmento sensible no anonimizado, anonimizado de forma incompleta o con una etiqueta incorrecta.
- **FP (falso positivo):** sustitución de un fragmento que no debía anonimizarse, sustitución sobre una zona incorrecta o uso de una etiqueta errónea.
- Una etiqueta errónea sobre un fragmento sensible implica **un FN por la entidad esperada y un FP por la sustitución incorrecta**.

A partir de estos valores se calcularán:

\[
Precision=\frac{TP}{TP+FP}
\]

\[
Recall=\frac{TP}{TP+FN}
\]

\[
F1=2\cdot\frac{Precision\cdot Recall}{Precision+Recall}
\]

Si una métrica tiene denominador cero, se aplicará el criterio publicado por el evaluador de referencia; una solución sin detecciones correctas obtendrá F1 igual a cero.

**La preservación del contenido no sensible no tendrá un porcentaje de nota independiente.** Las modificaciones indebidas se penalizarán **como falsos positivos dentro de la F1**. El objetivo sigue siendo devolver el texto original modificando únicamente los datos sensibles.

La nota se calculará exclusivamente como:

\[
\boxed{\text{Nota}_{benchmark}=F1\times10}
\]

El benchmark representa el **30 % de la calificación global de la actividad**.

Para dar crédito parcial, el evaluador alineará el original, el oráculo y la salida, sin exigir coincidencia exacta de todo el archivo. Se publicará antes del challenge un evaluador de muestra con casos de prueba y el procedimiento de alineamiento y cómputo de TP, FP y FN. Así se evitarán interpretaciones diferentes entre equipos.

Todos los equipos trabajarán con el mismo texto privado. El tiempo de ejecución se utilizará **solo como criterio de desempate** cuando obtengan la misma F1, sin alterar la nota.

---

# Parte II. Integración en una solución DLP — 20 %

## 8. Un caso de uso elegido por cada equipo

Además del motor textual obligatorio, cada equipo deberá **integrar Presidio en una solución DLP funcional** que resuelva una necesidad realista de protección de información. La integración deberá describir el canal de posible fuga, el punto de inspección y una medida preventiva ejecutable, conforme a la vinculación con el **control A.8.12 de ISO/IEC 27001:2022**.

Existe libertad para seleccionar el escenario y desarrollar las funcionalidades que se consideren más útiles. Por ejemplo:

- **OCR y anonimización de imágenes:** capturas de pantalla, formularios, fotografías y documentos escaneados.
- **Procesamiento de PDF y documentos:** identificación y anonimización preservando, en la medida de lo posible, el formato.
- **Protección de prompts de IA generativa:** filtrado y anonimización antes de enviarlos a un servicio externo (la demostración podrá ser simulada/local si no existe conexión).
- **DLP para correo electrónico:** revisión de mensajes y adjuntos antes de su envío.
- **Sanitización de logs:** eliminación de información sensible antes de remitir registros a plataformas de observabilidad.
- **Procesamiento masivo:** tratamiento de carpetas, lotes de documentos o repositorios.
- **Integración mediante API, aplicación web o herramienta de escritorio.**
- **Políticas DLP configurables:** decisiones según contexto, tipo de dato, destinatario o canal.
- **Reconocimiento avanzado:** modelos especializados, varios idiomas, análisis contextual o reconocedores propios.

**Estas posibilidades son orientativas. No es obligatorio implementar OCR, imágenes, PDF, una web ni un servicio API.** Se valorará la calidad de la implementación elegida, no el número de funciones anunciadas.

El prototipo debe ser **real, ejecutable y demostrable**, no una maqueta visual ni una propuesta exclusivamente teórica. Debe incorporar Presidio de forma efectiva y añadir trabajo de integración propio.

La solución adicional puede utilizar anonimización diferente de las etiquetas canónicas (redacción, enmascaramiento, pseudonimización, etc.), según su caso de uso. Esto no altera el contrato del benchmark, que debe seguir funcionando con el mismo `main.py` y formato de salida.

## 9. Rúbrica de integración

| Criterio | Peso dentro de la actividad |
|---|---:|
| Funcionalidad real y utilidad del caso de uso | **8 %** |
| Arquitectura e integración técnica de los componentes | **5 %** |
| Automatización y facilidad de utilización | **4 %** |
| Robustez, gestión de errores y reproducibilidad | **3 %** |
| **Total integración** | **20 %** |

Se reconocerán especialmente la autonomía, el trabajo de ingeniería, la calidad de las integraciones, la demostración de una medida preventiva de fuga de información y la justificación de su alcance. Una funcionalidad no implementada o que no pueda demostrarse no recibirá puntuación como capacidad desarrollada.

---

# Recursos de referencia y pruebas

## 10. Microsoft Presidio y Presidio Research

Los estudiantes deberán conocer y utilizar, al menos, los siguientes recursos:

- **Documentación general de Presidio:** https://microsoft.github.io/presidio/
- **Presidio Analyzer y reconocedores personalizados:** https://microsoft.github.io/presidio/analyzer/
- **Presidio Anonymizer:** https://microsoft.github.io/presidio/anonymizer/
- **Instalación:** https://microsoft.github.io/presidio/installation/
- **Presidio Research (pruebas y evaluación):** https://presidio-research.dataprivacystack.org/
- **Código de Presidio Research:** https://github.com/data-privacy-stack/presidio-research

**Presidio Research** ofrece herramientas para generar ejemplos sintéticos, probar reconocedores, medir Precision/Recall/F1 e investigar falsos positivos y falsos negativos. Sus notebooks de evaluación y configuración del detector son especialmente útiles para establecer una línea base y comprobar mejoras.

Estos recursos **no sustituyen al benchmark final del profesor**: permiten ensayar la detección durante el desarrollo. La anonimización del texto completo se comprobará finalmente con el oráculo específico de la actividad.

La instalación y descarga de modelos podrán realizarse durante el desarrollo; la ejecución final deberá ser offline.

---

# Desarrollo y metodología de trabajo

## 11. Dos semanas de trabajo

### Semana 1: línea base, reconocimiento y experimentación

1. Instalar Presidio y preparar la ejecución local.
2. Familiarizarse con sus módulos Analyzer y Anonymizer.
3. Ejecutar una versión inicial de anonimización textual y medir sus limitaciones.
4. Configurar el reconocimiento lingüístico/contextual avanzado requerido.
5. Incorporar y justificar mejoras propias de detección o anonimización.
6. Probar casos positivos, negativos y ambiguos con ayuda de Presidio Research u otros conjuntos sintéticos.
7. Seleccionar el caso de uso de integración DLP y comenzar su arquitectura.

### Semana 2: integración, mejora y entrega

1. Completar la interfaz de ejecución `python main.py entrada.txt salida.txt`.
2. Validar que procesa un archivo completo y anonimiza los fragmentos sensibles sin sustituir contenido ajeno a la política.
3. Probar la ejecución offline en un entorno reproducible.
4. Completar el prototipo de integración DLP.
5. Comparar al menos dos iteraciones de mejora con resultados reales.
6. Elaborar la memoria técnica y preparar la presentación y demostración.

Cada pareja organizará libremente el trabajo. **Ambos integrantes deberán conocer y poder defender la solución completa**, independientemente del reparto de tareas.

---

# Entregables

## 12. Tres entregables independientes

Cada equipo deberá entregar:

**1. Memoria técnica — PDF.** Extensión orientativa máxima: **10 páginas**, excluidas portada, referencias y anexos.

**2. Código y proyecto — ZIP.** Debe incluir:

- Código fuente completo y punto de entrada `main.py`.
- `requirements.txt` o instrucciones equivalentes de instalación de dependencias.
- Configuraciones, modelos y demás recursos necesarios para la ejecución offline; se indicarán las licencias y procedencia de modelos de terceros.
- `README.md` con instalación, preparación del entorno, ejecución exacta del benchmark y ejecución del prototipo de integración.
- Archivos de ejemplo no sensibles para comprobar el funcionamiento.

**3. Presentación y defensa — PPTX.** Se utilizará en una exposición pública de **15 minutos como máximo, incluida una demostración funcional**.

Ejemplo de denominación:

```text
Apellido1_Apellido2_Memoria.pdf
Apellido1_Apellido2_Codigo.zip
Apellido1_Apellido2_Presentacion.pptx
```

Aunque el desarrollo sea por parejas, **cada integrante deberá entregar individualmente los tres archivos en Canvas**, siguiendo el procedimiento de la asignatura.

---

# Estructura y evaluación de la memoria técnica — 15 %

## 13. Contenido mínimo

La memoria será breve y técnica; deberá explicar **decisiones, arquitectura, experimentación, resultados y conclusiones**, no limitarse a narrar cronológicamente el proceso.

Contendrá:

1. **Introducción y objetivos:** problema de protección de información y objetivos concretos.
2. **Análisis del problema y tipos de datos:** alcance, categorías, ambigüedades y falsos positivos relevantes.
3. **Estrategia técnica:** reconocedores, NLP/NER, configuración de Presidio, políticas y operadores de anonimización; justificación de las elecciones.
4. **Diseño y arquitectura:** diagrama del flujo de procesamiento y arquitectura de la integración DLP; identificar el canal de fuga, el punto de inspección, la respuesta preventiva y su relación con A.8.12 de ISO/IEC 27001:2022.
5. **Implementación:** componentes propios, bibliotecas y decisiones de ingeniería relevantes.
6. **Metodología experimental:** datos de desarrollo, línea base, versiones y principales mejoras.
7. **Resultados:** pruebas reales de anonimización, con Precision, Recall y F1 o ejemplos verificables.
8. **Análisis de errores:** falsos negativos, sustituciones indebidas y dificultades de anonimización.
9. **Limitaciones y posibles mejoras:** dificultades no resueltas y su impacto.
10. **Conclusiones:** decisiones más eficaces, aprendizajes y trabajo futuro.
11. **Organización del trabajo:** reparto de tareas entre los dos integrantes.
12. **Uso de Inteligencia Artificial:** declaración expresa de herramientas empleadas, finalidad, instrucciones relevantes y método de verificación; declarar también si no se utilizaron.
13. **Referencias:** documentación, modelos, código, datasets y otras fuentes utilizadas.

## 14. Rúbrica de memoria

Se utilizarán los mismos **ocho criterios académicos** aplicados en Secret Hunter Challenge:

1. Claridad y estructura.
2. Análisis del problema.
3. Justificación de la estrategia.
4. Calidad técnica.
5. Metodología experimental.
6. Análisis crítico de resultados.
7. Reproducibilidad.
8. Conclusiones.

Los ocho criterios tendrán el mismo peso dentro de la nota de memoria. La **memoria representa el 15 % de la actividad**.

No se premiará un modelo por ser ML ni por incluir más componentes sin justificar. Sí se valorarán la complejidad que aporte utilidad demostrable, el trabajo de ingeniería y la claridad de las decisiones. La puntuación del benchmark no sustituirá la evaluación académica de la memoria ni se duplicará como nota técnica.

---

# Presentación y demostración — 15 %

## 15. Defensa del proyecto

Cada equipo dispondrá de **15 minutos como máximo**, incluyendo una demostración del funcionamiento real.

La defensa deberá explicar:

- Problema y caso de uso DLP seleccionado, con referencia al control A.8.12 de ISO/IEC 27001:2022.
- Arquitectura general y componentes de Presidio utilizados.
- Reconocimiento avanzado y personalizaciones desarrolladas.
- Ejecución del anonimizador textual con el contrato exigido.
- Demostración de la integración DLP, mostrando el canal de exposición y la medida preventiva aplicada.
- Evolución experimental, resultados, errores y limitaciones.
- Principales decisiones técnicas y posibles mejoras.

El profesor valorará **claridad, capacidad de síntesis, dominio técnico, defensa de las decisiones, análisis de resultados y calidad de la demostración**.

La presentación visual no sustituye una demo funcional. Ambos integrantes deberán ser capaces de responder preguntas sobre cualquier parte de la solución.

---

# Coevaluación entre estudiantes — 20 %

## 16. Evaluación entre iguales

Cada estudiante evaluará las **presentaciones y demostraciones de sus compañeros**, no sus memorias escritas.

Se facilitará una rúbrica común basada en los seis criterios anteriores. Las valoraciones deberán estar justificadas y ser coherentes con lo observado. No se admitirán puntuaciones basadas en afinidad personal, intercambios de notas o decisiones arbitrarias.

Las valoraciones serán anónimas para los equipos evaluados y se remitirán individualmente al profesor por el canal indicado en Canvas.

La coevaluación tendrá un peso del **20 % de la nota final**. El profesor podrá revisar evaluaciones manifiestamente injustificadas o contrarias a la rúbrica conforme a las instrucciones académicas comunicadas para la actividad.

---

# Sistema de calificación y competición

## 17. Distribución final de pesos

| Bloque | Peso |
|---|---:|
| **Benchmark automático de anonimización textual** | **30 %** |
| **Integración avanzada en una solución DLP** | **20 %** |
| Evaluación del profesor: memoria técnica | 15 % |
| Evaluación del profesor: presentación y demo | 15 % |
| Coevaluación de estudiantes: presentación y demo | 20 % |
| **TOTAL** | **100 %** |

Las calificaciones de cada apartado se expresarán sobre 10. La nota ordinaria será:

\[
N=0{,}30B+0{,}20I+0{,}15M+0{,}15P+0{,}20C
\]

Donde:

- **B:** benchmark textual.
- **I:** integración DLP.
- **M:** memoria técnica.
- **P:** presentación y demo evaluadas por el profesor.
- **C:** coevaluación entre estudiantes.

## 18. Clasificación competitiva y bonus

La clasificación del **Presidio DLP Challenge** se establecerá por la **nota del benchmark textual**, calculada sobre el mismo texto privado y con el mismo evaluador para todos. La integración DLP no alterará la posición en el ranking, aunque contribuya a la nota final de la actividad.

- **Primer equipo clasificado:** **+1 punto** sobre la nota final.
- **Segundo equipo clasificado:** **+0,5 puntos**.
- **Resto de equipos:** sin bonus competitivo.

El tiempo de ejecución se utilizará únicamente como desempate de la puntuación de benchmark. Ambos integrantes de una pareja recibirán el mismo bonus.

El bonus se aplicará después de calcular la nota ordinaria:

\[
\text{Nota final}=\min(10,\ N+\text{bonus})
\]

La calificación final **nunca podrá superar 10 puntos**.

---

# Condiciones generales

## 19. Autoría, uso de IA y reproducibilidad

Se permite el uso de herramientas de Inteligencia Artificial como apoyo para programar, investigar, depurar y documentar, siempre que se **declare expresamente** y se verifiquen críticamente sus resultados.

La autoría y las decisiones técnicas deberán poder defenderse en la presentación. La lógica adicional y las integraciones que se presenten como propias deberán estar implementadas por el equipo. No se considerará suficiente entregar un simple envoltorio de Presidio sin aportación técnica relevante.

El uso de un modelo preentrenado no exime de explicar sus capacidades, límites, instalación local e integración.

Los textos de prueba, ejemplos y demostraciones deben utilizar **información ficticia o sintética**, sin publicar ni procesar datos personales reales sin autorización.

## 20. Criterios de éxito

Una buena solución no será necesariamente la que anonimice más caracteres ni la que incluya más funcionalidades.

Se espera que el equipo sea capaz de:

1. **Anonimizar correctamente** la información que debe protegerse.
2. **Conservar** el contenido que no requiere protección.
3. **Superar una línea base de Presidio** mediante decisiones justificadas.
4. **Ejecutar el benchmark con un único comando Python**, sin intervención manual.
5. **Integrar** el motor en un prototipo DLP funcional y útil que demuestre una medida preventiva relacionada con el control A.8.12 de ISO/IEC 27001:2022.
6. **Explicar y defender** las decisiones, limitaciones y resultados observados.

El objetivo es desarrollar **una solución de seguridad aplicable y evaluable**, combinando precisión, ingeniería, experimentación y protección efectiva de la información.
