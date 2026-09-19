# Plantilla 3 — AI Product Canvas
## Framework PROMPT | Fase O — Oportunidad de IA
### AD5018 Inteligencia Artificial para Negocios | UTEC

---

**Equipo:**
- Integrante 1: Valeria Briceño
- Integrante 2: Lucía Rodríguez
- Integrante 3: Aaron Van Oord
**Fecha de entrega:** 19/09/2026
**Versión del canvas:** v1.0

---



## SECCIÓN 1 — Identidad del producto

### 1.1 Nombre del producto / MVP
```
Nombre: InterviewIQ — Simulador Inteligente de Entrevistas para Universitarios
```

### 1.2 Problema que resuelve
> *Copia exactamente la declaración del Problem Statement Canvas. No parafrasear.*

```
"Los estudiantes universitarios peruanos de últimos ciclos que buscan prácticas
preprofesionales o su primer empleo tienen dificultad para preparar y mejorar sus
respuestas en entrevistas laborales por competencias porque cuentan con oportunidades
limitadas de práctica recurrente con retroalimentación estructurada, lo que genera
bajos niveles de preparación percibida y dificultades para estructurar respuestas
conductuales."
```

### 1.3 Usuario principal
> *¿Quién usa el producto directamente? Sé específico — no "las empresas" sino el rol exacto.*

```
Estudiantes universitarios peruanos de últimos ciclos que se encuentran buscando
prácticas preprofesionales o su primer empleo y necesitan prepararse para entrevistas
laborales por competencias.
```

### 1.4 Los dos componentes
> *Copia lo declarado en la Plantilla 1, Sección 3. Si aquí cambia algo, la Plantilla 1 se actualiza también.*

| Componente | Qué hace en este producto | Nivel |
|---|---|---|
| **Analítico** *(modelo entrenado)* | Clasifica cada respuesta textual para identificar presencia o ausencia de Situación, Tarea, Acción y Resultado (STAR). Se compararán TF-IDF + Logistic Regression y TF-IDF + Linear SVM, ajustando el umbral según el costo de los errores. | A2 |
| **Generativo** *(capa de lenguaje)* | Formula preguntas conductuales contextualizadas al rol y genera feedback personalizado usando la respuesta del estudiante, la salida del clasificador STAR y conocimiento recuperado de fuentes seleccionadas. | G2 |

**Patrón de conexión:** **1 modelo→lenguaje**

**El eje donde va la ambición del equipo:** **analítico y generativo — nivel intermedio A2 + G2**

---

## SECCIÓN 2 — Tech & Cost Overview *(visión de temperatura)*

>---

### 2.1 Categorías de IA que podrían aplicar al problema

> *Marca todas las que el equipo considera relevantes para el problema definido. No es un compromiso — es una exploración.*

| Categoría | ¿Podría aplicar? | Razonamiento en 1 línea |
|---|---|---|
| **Modelos de lenguaje (LLM)** — texto, conversación, generación | SÍ | Se requiere generar preguntas y feedback personalizado en lenguaje natural. |
| **Visión computacional** — imágenes, video, detección visual | NO | El MVP trabaja únicamente con texto. |
| **ML supervisado tabular** — predicción con datos históricos | SÍ | Se entrenará un clasificador supervisado sobre representaciones TF-IDF de respuestas textuales etiquetadas con S/T/A/R. |
| **ML no supervisado** — segmentación, clustering | NO | El objetivo ya tiene etiquetas definidas y no requiere descubrir grupos. |
| **Automatización de flujos con IA** — orquestación de agentes | NO | El MVP usa un flujo A2→G2 definido y no requiere un agente autónomo. |
| **Clasificación de audio / voz** | NO | Audio y voz están fuera del alcance del MVP. |

---

### 2.2 Estimación de costo rough del MVP

> *Nivel de precisión esperado: orden de magnitud, no presupuesto formal.*
> *Escala de referencia: 🟢 Gratuito o casi / 🟡 Freemium con límites / 🔴 Pago con costo significativo*

| Componente | Categoría de herramienta | Nivel de costo estimado | Comentario |
|---|---|---|---|
| Motor de IA principal | Python/scikit-learn en Google Colab + GPT para capa generativa | 🟡 | El entrenamiento A2 puede realizarse con herramientas gratuitas; el principal costo variable sería el uso del modelo GPT/API durante pruebas. |
| Interfaz o frontend | Streamlit / entorno de desarrollo asistido con Antigravity | 🟢 | Se priorizarán alternativas gratuitas para el MVP. |
| Almacenamiento de datos | CSV + almacenamiento local/GitHub y vector store open source | 🟢 | El volumen del MVP es pequeño y no requiere infraestructura de pago dedicada. |
| Orquestación / automatización | Código Python | 🟢 | No se utilizará un agente ni una plataforma de automatización de pago. |
| Otros *(APIs, integraciones)* | Embeddings/LLM y eventual hosting | 🟡 | Puede existir un costo bajo según el modelo y el volumen de pruebas. |

**Costo total estimado del MVP (rango aproximado):**
```
Mínimo: S/. 0 / mes      Máximo: S/. 50 / mes
Supuestos clave de esta estimación:
- Uso de Google Colab en su modalidad gratuita para desarrollo y entrenamiento.
- Uso de Python y scikit-learn, que son herramientas open source.
- Uso de alternativas gratuitas para vector store y despliegue cuando sea posible.
- El principal costo variable proviene de GPT/API y depende del modelo y número de pruebas.
- El rango es una estimación de orden de magnitud para el MVP académico, no un
  presupuesto de operación a escala.
```

---

### 2.3 Complejidad de implementación percibida

> *Evaluación honesta del equipo sobre qué tan difícil sería construir con estas categorías.*

| Dimensión | Nivel | Comentario |
|---|---|---|
| Curva de aprendizaje de las herramientas | Media | El equipo debe integrar ML supervisado, RAG, LLM e interfaz, pero las herramientas elegidas tienen documentación disponible. |
| Disponibilidad de tutoriales y documentación | Alta | Python, scikit-learn, Colab, Streamlit y las herramientas de RAG cuentan con documentación y ejemplos. |
| Dependencia de conocimiento técnico externo | Baja | El MVP puede desarrollarse con el equipo y documentación disponible, sin depender de una empresa externa. |
| Viabilidad de construir el MVP en 7 semanas | Alta | El alcance se limita a texto, A2 + G2 y una interfaz web sencilla; se excluyen audio, video, autenticación e integraciones complejas. |

---

> **\* Análisis financiero detallado:** Esta sección será complementada con la **Plantilla 5 — Financial & Tech Feasibility**, que desarrollaremos más adelante en el curso. Incluirá costeo por tokens, comparación de APIs, ROI estimado del MVP y análisis de viabilidad financiera del producto a escala.

---

## SECCIÓN 3 — Experiencia del usuario

### 3.1 Input del usuario
> *¿Qué hace o ingresa el usuario para activar la IA?*

- [x] Escribe texto en un chat o formulario
- [ ] Sube un archivo (imagen, PDF, CSV, audio)
- [x] Hace clic en un botón o selecciona una opción
- [ ] Habla o graba un audio
- [ ] El sistema se activa automáticamente (sin acción del usuario)
- [ ] Otro: _______________

**Descripción detallada del input:**
```
El estudiante selecciona el rol o área laboral para la cual desea practicar.
InterviewIQ presenta una pregunta conductual y el estudiante escribe su respuesta
en texto libre. Esa respuesta activa el análisis STAR y la generación de feedback.
```

### 3.2 Output de la IA
> *¿Qué recibe el usuario como resultado de la interacción con la IA?*

- [x] Texto / respuesta en lenguaje natural
- [x] Número o predicción
- [x] Clasificación o categoría
- [ ] Alerta o notificación
- [x] Recomendación con opciones
- [ ] Imagen generada
- [ ] Acción ejecutada automáticamente (email enviado, registro guardado, etc.)
- [ ] Otro: _______________

**Descripción detallada del output:**
```
El usuario recibe el análisis de presencia o ausencia de S, T, A y R y un feedback
en lenguaje natural que explica fortalezas, aspectos faltantes y recomendaciones
concretas para mejorar la respuesta. Luego puede continuar con otra pregunta.
```

---

## SECCIÓN 4 — Flujo del producto

### 4.1 Diagrama de flujo
> *Dibuja o describe el flujo completo paso a paso. Usa flechas (→) para conectar los pasos.*

```
Paso 1: Usuario → selecciona rol/área y comienza la simulación
Paso 2: → InterviewIQ genera/presenta una pregunta conductual contextualizada
Paso 3: → Usuario escribe su respuesta en texto libre
Paso 4: → Modelo A2 clasifica S/T/A/R → RAG recupera contexto → GPT genera feedback
Paso 5: → Usuario recibe: análisis STAR + fortalezas + aspectos a mejorar + recomendación
```

**Versión visual (opcional pero recomendada):**
> *Pega aquí una imagen del diagrama o el link a la herramienta donde lo dibujaste (Miro, Lucidchart, draw.io, etc.)*

```
Link o imagen: PENDIENTE — se elaborará el diagrama visual a partir del flujo anterior.
```

### 4.2 Humano en el circuito
> *¿En qué punto del flujo interviene un humano para validar o corregir antes de que la IA actúe?*

- [x] No hay intervención humana — la IA actúa de forma autónoma
- [ ] El humano revisa el output antes de que llegue al usuario final
- [ ] El humano puede aprobar o rechazar la recomendación de la IA
- [ ] El humano interviene solo cuando la IA no tiene respuesta
- [ ] Otro: _______________

**Justificación de la decisión:**
```
InterviewIQ es una herramienta de práctica y no toma decisiones de contratación.
El feedback llega directamente al estudiante para permitir práctica recurrente.
El equipo sí realizará validación humana durante desarrollo y evaluación del MVP,
pero no habrá una persona revisando cada respuesta en tiempo real.
```

### 4.3 Plan de contingencia
> *¿Qué pasa si la IA falla, no tiene respuesta o la API no está disponible?*

```
Si el modelo A2 no puede procesar la respuesta, el sistema informará que no pudo
realizar el análisis STAR y permitirá volver a intentar. Si la capa generativa o
la API no está disponible, se mostrará el análisis A2 disponible y un mensaje de
indisponibilidad temporal del feedback generativo, sin inventar una respuesta.
```

---

## SECCIÓN 5 — Decisión estratégica Build / Buy / Integrate

Marca con una X:

- [ ] **Buy** — usar herramienta existente sin modificar
- [ ] **Integrate** — conectar API de IA a flujo o interfaz propia
- [ ] **Build** — entrenar modelo propio con datos del equipo
- [x] **Combinación** — especificar: **Build + Integrate**

**Justificación (obligatoria):**
> *¿Por qué esta estrategia y no las otras dos? Argumenta en función del problema y el tiempo disponible.*

```
El componente A2 se construirá y entrenará con datos del equipo porque el proyecto
necesita detectar específicamente los cuatro componentes STAR. Para el componente
generativo se integrará un LLM existente con RAG, ya que entrenar un modelo de
lenguaje desde cero no es viable en el tiempo del curso. Esta combinación permite
desarrollar propiedad analítica propia sin asumir el costo y complejidad de construir
toda la capa generativa.
```

---

## SECCIÓN 6 — Diseño de cada componente

### 6.1 Componente generativo — System Prompt

> *Escribe el system prompt completo que usará el MVP. Debe seguir la estructura mínima obligatoria.*

```
ROL:
Eres InterviewIQ, un simulador de entrevistas laborales por competencias dirigido
a estudiantes universitarios que buscan prácticas preprofesionales o su primer empleo.

CONTEXTO:
El usuario está practicando una entrevista conductual para un rol seleccionado.
Recibes la pregunta realizada, la respuesta original del estudiante, la salida del
clasificador analítico indicando presencia o ausencia de Situación, Tarea, Acción
y Resultado (STAR), y fragmentos recuperados de la base de conocimiento RAG.

Tu objetivo es ayudar al estudiante a reconocer qué comunicó correctamente y qué
puede mejorar para estructurar una respuesta más clara y concreta.

RESTRICCIONES:
- No inventes experiencias, logros, resultados ni datos que el estudiante no haya mencionado.
- No afirmes que una persona será contratada, rechazada o que tiene una probabilidad
  determinada de conseguir el puesto.
- No sustituyas la salida del modelo A2 con una clasificación STAR inventada.
- Usa los fragmentos recuperados cuando des recomendaciones metodológicas.
- Si el contexto recuperado no es suficiente, indícalo en lugar de inventar información.
- No solicites datos personales que no sean necesarios para la práctica.
- No evalúes características protegidas ni realices inferencias sobre personalidad.
- El feedback debe centrarse en la estructura y claridad de la respuesta.

FORMATO DE RESPUESTA:
1. Análisis STAR:
   - Situación: presente/ausente
   - Tarea: presente/ausente
   - Acción: presente/ausente
   - Resultado: presente/ausente
2. Lo que hiciste bien: máximo 2 puntos.
3. Qué puedes mejorar: máximo 3 puntos concretos.
4. Siguiente paso: una recomendación práctica para reformular o completar la respuesta.

TONO:
Claro, cercano, respetuoso, constructivo y directo. Evita lenguaje excesivamente técnico.

IDIOMA:
Español, salvo que el usuario solicite practicar la entrevista en otro idioma.
```

**Plan de gestión de alucinaciones:**
```
¿Qué pasa si la IA inventa información?
El prompt prohíbe inventar experiencias o resultados y obliga a basar las recomendaciones
metodológicas en el contexto recuperado. Durante las pruebas se revisará una muestra
de respuestas para detectar afirmaciones no sustentadas.

¿Hay validación humana en decisiones críticas?
InterviewIQ no toma decisiones críticas de contratación. Durante el desarrollo,
el equipo revisará manualmente casos de prueba y errores del feedback.

¿El usuario puede reportar respuestas incorrectas?
Para el MVP se incluirá, si el tiempo lo permite, una opción simple para indicar
que el feedback no fue útil/correcto. Como mínimo, esta información se recogerá
en el formulario de validación de usuarios de la Semana 13.
```

**Solo si el nivel es G2 (RAG):**

| Campo | Detalle |
|---|---|
| Documentos que alimentan el RAG | Guías institucionales sobre metodología STAR y entrevistas conductuales; USC Career Center, UC Santa Cruz Career Success; fuentes académicas sobre mock interviews; ESCO para ocupaciones/competencias. |
| En qué fragmentos se parten | Configuración inicial de 300–500 tokens, respetando secciones y límites semánticos cuando sea posible. |
| Quién los actualiza y cada cuánto | Valeria Briceño; revisión antes del MVP y antes de PC2, además de cambios relevantes en las fuentes. |
| Cómo se comprobará que recupera el documento correcto | Con consultas de prueba y verificación de que el fragmento/fuente esperado aparezca dentro de los resultados top-k. |

**Solo si el nivel es G3 o G4 (agente):**

| Herramienta | Qué hace | ¿Lee o escribe? | Qué pasa si falla |
|---|---|---|---|
| 1. N/A | El proyecto es G2 | N/A | N/A |
| 2. N/A | N/A | N/A | N/A |
| 3. N/A | N/A | N/A | N/A |

| Control del agente | Definición del equipo |
|---|---|
| Máximo de pasos por tarea | N/A |
| Cómo sabe que la tarea terminó | N/A |
| Qué acciones exigen aprobación humana antes de ejecutarse | N/A |

---

### 6.2 Componente analítico — Model Design Canvas

> *Este es el gemelo del system prompt: aquí se decide qué va a aprender el modelo y cuándo lo consideramos suficientemente bueno. **Se completa antes de entrenar, no después.***

| Campo | Detalle |
|---|---|
| **Qué predice** *(variable objetivo, en una frase)* | Presencia o ausencia independiente de Situación, Tarea, Acción y Resultado en una respuesta conductual. |
| **Tipo de tarea** | Clasificación multilabel. |
| **Con qué lo predice** *(variables de entrada)* | Principalmente el texto de la respuesta representado con TF-IDF; se evaluará si incluir la pregunta mejora el desempeño sin introducir leakage. |
| **Variables excluidas y por qué** *(fuga de datos)* | Etiquetas S/T/A/R porque son el target; identidad del anotador y origen como features porque no existirán como señales necesarias en producción; feedback posterior porque se genera después de la predicción. |
| **Herramienta de entrenamiento** | Python + scikit-learn en Google Colab. |
| **Cómo se separan los datos** | Diseño previsto: 70% entrenamiento, 10% validación y 20% prueba. Se evitará que respuestas duplicadas o variantes casi idénticas queden en conjuntos distintos. |
| **Baseline a superar** | TF-IDF + Logistic Regression. **Cifra pendiente:** se obtendrá en Semana 9 al entrenar con el dataset etiquetado. |
| **Métrica principal** *(una sola)* | Macro F1. |
| **Por qué esa métrica y no otra** | Porque existen cuatro etiquetas y puede haber desbalance entre presencia/ausencia; Macro F1 permite evaluar el rendimiento sin dejar que las clases más frecuentes dominen el resultado. |
| **Criterio mínimo de aceptación** | Macro F1 ≥ 0.65 y que el modelo seleccionado iguale o supere el baseline. El valor será revisado con resultados reales antes de PC2. |
| **Umbral de decisión previsto** | Se parte del umbral estándar del modelo y se ajustará en validación por etiqueta según el costo observado de falsos positivos y falsos negativos. El valor final no se fija antes de tener datos. |

**Costo del error — el razonamiento de negocio:**

| Tipo de error | Qué significa en este negocio | Cuánto cuesta aproximadamente |
|---|---|---|
| **Falsa alarma** *(marqué algo que no era)* | InterviewIQ indica que un componente STAR está presente aunque la respuesta realmente no lo desarrolla. El estudiante podría creer que no necesita mejorarlo. | **Costo alto cualitativo:** puede generar feedback incorrectamente positivo y ocultar una debilidad real. |
| **Caso perdido** *(no marqué algo que sí era)* | InterviewIQ indica que falta un componente STAR que el estudiante sí expresó. El feedback podría pedir una mejora innecesaria. | **Costo medio cualitativo:** genera frustración o corrección innecesaria, pero el estudiante todavía recibe una recomendación de mejora. |

> *¿Cuál de los dos errores es más caro y qué implica eso para el umbral?*
```
Se considera más costoso el falso positivo, porque puede hacer creer al estudiante
que una parte débil de su respuesta ya está correctamente desarrollada. Por ello,
durante la validación se priorizará evitar marcar S/T/A/R como presente sin evidencia
suficiente. El umbral final se ajustará con los datos de validación y no se fijará
arbitrariamente antes del entrenamiento.
```

**Solo si el equipo solicitó y obtuvo la excepción al componente analítico:**

| Campo | Detalle |
|---|---|
| Fecha de aprobación de la excepción | N/A — no se solicita excepción |
| Casos del conjunto de prueba etiquetado | N/A *(mínimo 30)* |
| Quién definió la respuesta correcta de cada caso | N/A |
| Qué se mide y cuál es el mínimo aceptable | N/A |

---

### 6.3 La conexión entre ambos componentes

**Patrón elegido** *(viene de la Plantilla 1, Sección 3.3)*:

- [x] Patrón 1 — Modelo → lenguaje
- [ ] Patrón 2 — Lenguaje → modelo
- [ ] Patrón 3 — Modelo como herramienta del agente

**Dibuja o describe el punto exacto de conexión:**
```
¿Qué produce el primer componente?
El modelo A2 produce cuatro predicciones: presencia/ausencia de Situación, Tarea,
Acción y Resultado para la respuesta del estudiante.

¿Cómo llega ese dato al segundo?
La aplicación pasa las predicciones S/T/A/R, la respuesta original y la pregunta
al pipeline generativo. El sistema usa esta información para formular la consulta
al RAG y construir el contexto que recibe el LLM.

¿Qué hace el segundo con él?
G2 recupera conocimiento relevante y el LLM combina ese contexto con la salida
A2 para explicar fortalezas, componentes faltantes y acciones concretas de mejora.
```

---

## SECCIÓN 7 — Alcance del MVP

### Lo que SÍ incluye el MVP
> *Lista las funcionalidades que estarán listas para la sustentación de la Semana 14.*

```
1. Selección de un rol o área objetivo y simulación textual de preguntas conductuales.
2. Clasificación A2 de presencia/ausencia de Situación, Tarea, Acción y Resultado.
3. RAG G2 con fuentes seleccionadas sobre STAR, entrevistas y competencias.
4. Feedback personalizado en lenguaje natural y acceso al MVP mediante una URL pública.
```

### Lo que NO incluye el MVP *(pero podría incluir una versión futura)*
> *Declarar esto explícitamente demuestra madurez en la gestión del proyecto.*

```
1. Audio, video, reconocimiento facial, emociones o análisis de voz.
2. Decisiones de contratación/rechazo, integraciones con plataformas de empleo o empresas.
3. Aplicación móvil, autenticación completa y base de datos persistente de usuarios.
```

### Plan de despliegue del MVP
> *El MVP debe estar accesible por URL pública antes de la sustentación (requisito de admisibilidad de la PC2). Decide desde ahora dónde vivirá el producto — no en la Semana 13.*

| Pregunta | Respuesta |
|---|---|
| ¿Dónde se desplegará el MVP? *(plataforma o servicio)* | Streamlit Community Cloud como opción prevista; se verificará técnicamente durante el desarrollo. |
| ¿Qué tipo de acceso tendrá el evaluador? *(link abierto, link con clave, formulario)* | Link público abierto al MVP. |
| ¿Requiere que el evaluador instale algo? *(la respuesta debe ser NO)* | NO |
| ¿Tiene costo el despliegue? ¿Cuál y quién lo asume? | Se priorizará el plan gratuito. Si el uso de API genera costo, será asumido por el equipo dentro del rango estimado del MVP. |
| Semana comprometida para el primer despliegue público | **Semana 12** |

### Criterio de éxito del MVP
> *¿Cómo sabrá el equipo que el MVP está listo para ser sustentado?*

```
"El MVP está listo cuando un usuario externo al equipo puede abrirlo desde su propio
dispositivo, seleccionar un rol, responder una pregunta conductual sin instrucciones
adicionales y obtener un análisis STAR y feedback personalizado generado por el flujo
A2 + G2."
```

---

## SECCIÓN 8 — OKRs y KPIs del producto


---

### Estructura obligatoria: O + KR + KPI

```
OBJETIVO (O)          → La mejora de negocio que persigue el producto (1 frase aspiracional)
    Key Result 1 (KR) → Métrica de negocio con valor actual y meta específica
    Key Result 2 (KR) → Métrica de negocio con valor actual y meta específica
    KPI técnico       → Métrica del modelo que indica que la IA funciona correctamente
```

**Ejemplo de referencia (NO copiar — solo para entender la estructura):**
```
O:   Reducir la carga operativa del equipo de atención al cliente
KR1: Tasa de resolución autónoma por IA > 75% (valor actual: 0% — todo es manual)
KR2: Tiempo promedio de respuesta < 2 min (valor actual: 45 min)
KPI: Tasa de alucinación del modelo < 5%
```

---

### OKR + KPI del proyecto

**Objetivo (O):**
> *Una frase que describe la mejora de negocio que el producto persigue. Debe ser ambiciosa pero alcanzable en el semestre.*

```
O: Mejorar la preparación de estudiantes universitarios para entrevistas laborales
por competencias mediante práctica recurrente y retroalimentación estructurada.
```

---

**Key Result 1 (KR1):**

| Campo | Detalle |
|---|---|
| Métrica | Porcentaje de estudiantes que se sienten poco o nada preparados para afrontar entrevistas laborales por competencias. |
| Valor actual | **60%**, según la encuesta inicial realizada a 50 estudiantes universitarios de últimos ciclos. |
| Meta con el MVP | Reducir a **40% o menos** entre los participantes de la validación después de utilizar InterviewIQ. |
| Método de medición | Cuestionario pre/post aplicado a usuarios del MVP utilizando la misma escala/pregunta comparable a la medición inicial. |
| Período de medición | **Semana 13 (2–8 de noviembre de 2026).** |

---

**Key Result 2 (KR2):**

| Campo | Detalle |
|---|---|
| Métrica | Porcentaje de estudiantes que reporta al menos alguna dificultad para estructurar ejemplos concretos al responder preguntas conductuales. |
| Valor actual | **80%**, según la encuesta inicial realizada a 50 estudiantes universitarios de últimos ciclos. |
| Meta con el MVP | Reducir a **55% o menos** entre los participantes de la validación después de las sesiones de práctica. |
| Método de medición | Cuestionario pre/post y contraste con las respuestas generadas durante la práctica para observar cambios en la estructura STAR. |
| Período de medición | **Semana 13 (2–8 de noviembre de 2026).** |

---

**Key Result 3 (KR3) — opcional pero recomendado:**

| Campo | Detalle |
|---|---|
| Métrica | Porcentaje de estudiantes que rara vez o nunca recibe retroalimentación estructurada al practicar entrevistas. |
| Valor actual | **40%**, según la encuesta inicial realizada a 50 estudiantes. |
| Meta con el MVP | Lograr que **90% o más** de los participantes de la validación complete al menos una práctica en InterviewIQ y reciba feedback estructurado. |
| Método de medición | Registro de sesiones del MVP + encuesta posterior confirmando recepción y utilidad del feedback. |
| Período de medición | **Semana 13 (2–8 de noviembre de 2026).** |

---

**KPI técnico del modelo:**

| Campo | Detalle |
|---|---|
| Métrica técnica | **A2:** Macro F1 de clasificación S/T/A/R. **G2:** tasa de recuperación correcta en top-k sobre un conjunto de consultas de prueba. |
| Criterio mínimo aceptable | **A2:** Macro F1 ≥ 0.65 y desempeño igual o superior al baseline. **G2:** al menos 80% de consultas de prueba recuperan un fragmento relevante dentro del top-k definido. |
| Método de medición | **A2:** evaluación sobre test etiquetado separado del entrenamiento. **G2:** conjunto de consultas con fuente/fragmento esperado y revisión de los resultados recuperados. |

---

### Verificación de coherencia interna

| Pregunta | Respuesta |
|---|---|
| ¿El Objetivo refleja directamente el problema de la Sección 1.2? | SÍ |
| ¿Los KRs son medibles con números concretos (no "mejorar" o "aumentar")? | SÍ |
| ¿Hay un KPI técnico por cada componente declarado en la Sección 1.4? | SÍ |
| ¿El equipo puede obtener el valor actual de los KRs antes de la Semana 6? | SÍ — provienen de la encuesta inicial real de 50 estudiantes. |


---

## SECCIÓN 9 — Autoevaluación del equipo

| Pregunta de control | Respuesta |
|---|---|
| ¿El problema en la Sección 1.2 es copia exacta del Problem Statement Canvas? | SÍ |
| ¿El flujo de la Sección 4 muestra dónde se pasa de un componente al otro? | SÍ |
| ¿El Model Design Canvas tiene baseline declarado con su cifra? | **NO — el baseline está definido, pero su cifra real se obtiene en Semana 9 al entrenarlo.** |
| ¿Se revisó variable por variable que no haya fuga de datos? | SÍ a nivel de diseño; la verificación final se repetirá sobre el dataset construido. |
| ¿El umbral de decisión se justifica con el costo del error, no por defecto? | SÍ — el valor numérico final se ajustará con validación. |
| ¿El stack tecnológico fue verificado (cuentas creadas, accesos confirmados)? | **PENDIENTE de verificación completa durante Semana 7.** |
| ¿El alcance del MVP es realista para construir y desplegar entre las Semanas 7 y 11? | SÍ |
| ¿El plan de despliegue de la Sección 7 identifica una plataforma concreta y verificada? | **PARCIAL — Streamlit Community Cloud está definido, falta realizar prueba de despliegue.** |
| ¿El system prompt fue probado al menos una vez antes de entregar? | **NO — redactado, prueba pendiente.** |
| ¿El equipo verificó que la herramienta de entrenamiento acepta sus datos? | **NO — dataset pendiente de construcción.** |
| ¿El Objetivo del OKR refleja el problema definido en Fase P? | SÍ |
| ¿Los KRs tienen valores actuales concretos (no estimados)? | SÍ — encuesta real de 50 estudiantes. |
| ¿Todos los integrantes entienden cada sección de este canvas? | PENDIENTE de validación interna del equipo. |

