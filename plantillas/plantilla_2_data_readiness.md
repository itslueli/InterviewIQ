# Plantilla 2 — Data Readiness Checklist
## Recursos de Datos
### AD5018 Inteligencia Artificial para Negocios | UTEC

---

**Equipo:**
- Integrante 1: Valeria Briceño
- Integrante 2: Lucía Rodríguez
- Integrante 3: Aaron Van Oord


**Proyecto:** InterviewIQ — Simulador Inteligente de Entrevistas para Universitarios
**Tipo de IA del proyecto:** A2 (diagnóstico de nivel + clasificación multilabel STAR) + G2 (RAG)

---

> **Estado de esta versión:** el diseño de datos está definido. El proyecto requiere **tres recursos de datos diferenciados**: (1) datos del cuestionario diagnóstico para la clasificación del nivel de preparación del estudiante, (2) dataset de respuestas etiquetadas S/T/A/R para el clasificador STAR, y (3) corpus de documentos para el componente RAG. Los recursos (1) y (2) están pendientes de construcción; el recurso (3) tiene fuentes iniciales verificadas y accesibles.

---

## SECCIÓN 1 — Inventario de datos

### Visión general: los tres recursos del sistema

```
RECURSO 1 — Datos del cuestionario diagnóstico
  → Alimenta el clasificador de nivel de preparación (Logistic Regression)
  → Permite adaptar la dificultad y tipo de preguntas al perfil del usuario

RECURSO 2 — Dataset InterviewIQ-STAR
  → Alimenta el clasificador STAR multilabel (componente A2 principal)
  → ~200 pares (pregunta conductual, respuesta candidato, etiquetas S/T/A/R)

RECURSO 3 — Corpus RAG
  → Base de conocimiento del componente generativo (G2)
  → ~20–50 documentos sobre metodología STAR y competencias por rol
```

---

### Parte A — Recurso 1: datos del cuestionario diagnóstico

**Descripción:** Respuestas al cuestionario corto aplicado al estudiante al inicio de la sesión. Se usan como features para un clasificador de Logistic Regression que asigna un nivel de preparación (básico / intermedio / avanzado).

**Variables capturadas:**

| Variable | Descripción | Tipo |
|---|---|---|
| `experiencia_entrevistas` | ¿Cuántas entrevistas por competencias ha tenido? | Ordinal (0 / 1–2 / 3 o más) |
| `conocimiento_star` | ¿Conoce la metodología STAR? | Binario (Sí / No) |
| `confianza_autodeclarada` | ¿Qué tan confiado/a se siente para responder preguntas conductuales? | Escala 1–5 |
| `dificultad_estructurar` | ¿Le cuesta estructurar ejemplos concretos en sus respuestas? | Binario (Sí / No) |
| `feedback_previo` | ¿Ha recibido retroalimentación estructurada antes al practicar? | Binario (Rara vez o nunca / Sí) |

**Variable objetivo:**
```
nivel_preparacion ∈ {básico, intermedio, avanzado}
```

**Estado actual:** 🟡 — cuestionario diseñado, recolección pendiente. Se aplicará en sesiones piloto (Semana 7) y a ≥ 15 usuarios externos (Semana 13).

---

### Parte B — Recurso 2: dataset analítico `InterviewIQ-STAR`

| # | Dataset | Fuente | Formato | N° de registros aprox. | ¿Tiene etiquetas? |
|---|---|---|---|---|---|
| 1 | `InterviewIQ-STAR` | Dataset propio del equipo; construcción pendiente | CSV | ~200 pares | Pendiente de etiquetado |
| 2 | Preguntas conductuales de referencia | Fuentes públicas seleccionadas sobre entrevistas conductuales | CSV / texto | Pendiente | NO (no aplica como target) |

**Esquema del dataset:**

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer | Identificador único del par |
| `question` | String | Pregunta conductual realizada |
| `answer` | String | Respuesta del candidato en texto libre |
| `situation` | Binario (0/1) | ¿La respuesta incluye Situación? |
| `task` | Binario (0/1) | ¿La respuesta incluye Tarea? |
| `action` | Binario (0/1) | ¿La respuesta incluye Acción? |
| `result` | Binario (0/1) | ¿La respuesta incluye Resultado? |
| `source` | String | Origen de la respuesta (sintética / real-anon) |
| `annotator` | String | Código del anotador (A1, A2, A3) |

**Variable objetivo:**

```
El problema se modela como clasificación multilabel. Para cada respuesta
textual se predicen cuatro etiquetas binarias:

- situation: 1 si se identifica Situación; 0 si no.
- task:      1 si se identifica Tarea; 0 si no.
- action:    1 si se identifica Acción; 0 si no.
- result:    1 si se identifica Resultado; 0 si no.

Una misma respuesta puede contener cualquier combinación de estas cuatro
etiquetas. Por ejemplo: S=1, T=1, A=1, R=0.
```

**Tipo de problema confirmado:**
- [x] Clasificación — decide entre categorías (SÍ/NO) *(multilabel: cuatro etiquetas binarias S/T/A/R)*
- [ ] Regresión — estima un número
- [ ] Agrupamiento — encuentra grupos sin categorías previas

**Recuento de casos por categoría** *(el total de filas no basta)*:

| Categoría que se quiere distinguir | N° de casos disponibles |
|---|---|
| Situation (S) | Pendiente — dataset aún no construido |
| Task (T) | Pendiente — dataset aún no construido |
| Action (A) | Pendiente — dataset aún no construido |
| Result (R) | Pendiente — dataset aún no construido |

Actualmente **no existe un conteo verificable** porque el dataset todavía no ha sido construido y etiquetado. El equipo verificará que las respuestas incluyan combinaciones completas (S=1,T=1,A=1,R=1), parciales y deficientes para asegurar que cada etiqueta tenga representación suficiente antes de hacer el split de entrenamiento, validación y prueba.

**Revisión de fuga de datos** *(obligatoria)*:

| Variable sospechosa | ¿Existe antes del hecho a predecir? | Decisión |
|---|---|---|
| `answer` | SÍ | Se mantiene (feature principal) |
| `question` | SÍ | Se mantiene / evaluar su inclusión; disponible al momento de predicción |
| `situation`, `task`, `action`, `result` | NO | Se eliminan como features (son los targets; nunca entran como features) |
| `annotator` | NO (no es información del usuario) | Se elimina (excluir del modelo) |
| `source` | Puede existir como metadato | Se elimina (evita que el modelo aprenda patrones artificiales de procedencia) |
| Feedback generado después de clasificar | NO | Se elimina completamente |

El split se diseñará agrupando por pregunta o plantilla de origen para evitar que ejemplos casi idénticos queden simultáneamente en train y test.

**Responsable de esta revisión:** Aaron Van Oord, con revisión del equipo.

---

### Parte C — Recurso 3: corpus RAG (componente generativo G2)

| # | Tipo de información | Dónde está actualmente | Formato | ¿Está disponible? |
|---|---|---|---|---|
| 1 | Metodología STAR y recomendaciones para entrevistas conductuales | USC Career Center — *Interview Preparation* | Página web / HTML | SÍ |
| 2 | Definición y ejemplos de Situation, Task, Action, Result | UC Santa Cruz Career Success — *Interview Prep* | Página web / HTML | SÍ |
| 3 | Evidencia sobre utilidad de entrevistas simuladas en estudiantes universitarios | Wilkie & Rosendale (2024), *Journal of University Teaching and Learning Practice* | Artículo / PDF | SÍ |
| 4 | Evidencia sobre preparación, confianza y ansiedad después de entrevistas simuladas | Marcus et al. (2023), *Journal of Nursing Education* / PubMed PMID 37561904 | Abstract / artículo académico | PARCIAL |
| 5 | Ocupaciones y competencias para contextualizar preguntas según rol objetivo | ESCO — Comisión Europea | Portal web / CSV / ODS / RDF / API | SÍ |

**Estrategia de contexto elegida:**
- [ ] **G1** Prompt simple *(base de conocimiento pequeña y estable)*
- [x] **G2** RAG *(base de conocimiento grande o cambiante)*
- [ ] **G3/G4** Agente con herramientas
- [ ] Memoria de sesión

El sistema recuperará fragmentos relevantes de las fuentes seleccionadas y los combinará con la respuesta original del estudiante y con la salida del clasificador STAR (A2). El feedback no depende únicamente del conocimiento general del LLM sino de contenido curado sobre metodología STAR, entrevistas conductuales y competencias por rol.

**Si el nivel es G2 (RAG):**

| Pregunta | Respuesta del equipo |
|---|---|
| ¿En qué fragmentos se parten los documentos? | Fragmentos de aproximadamente **300–500 tokens**, respetando en lo posible títulos, subtítulos y límites semánticos. El tamaño definitivo se ajustará mediante pruebas de recuperación. |
| ¿Quién los actualiza y cada cuánto? | **Responsable principal: Valeria Briceño.** Revisará las fuentes antes de la construcción del MVP y nuevamente antes de la evaluación final de PC2. Los cambios se registrarán en `README_data.md`. |
| ¿Cómo se comprobará que recupera el documento correcto? | Se construirá un conjunto pequeño de consultas de prueba con una fuente o fragmento esperado. Se evaluará si el contenido relevante aparece dentro de los primeros resultados recuperados (top-k). La métrica de evaluación será retrieval precision@k. |

---

### Parte D — Cómo se conectan los tres recursos

```
¿Qué dato exactamente viaja entre recursos y componentes?

RECURSO 1 (cuestionario diagnóstico)
  → Clasificador de nivel (LR)
  → nivel ∈ {básico, intermedio, avanzado}
  → adapta preguntas conductuales generadas por G2

RECURSO 2 (InterviewIQ-STAR) — entrenamiento
  → Clasificador STAR (A2)

En inferencia:
respuesta del usuario
  → Clasificador STAR (A2)
  → S/T/A/R presente o ausente
  → junto con respuesta original y nivel del usuario

RECURSO 3 (corpus RAG)
  → Retrieval de fragmentos relevantes
  → LLM genera feedback personalizado (G2)

Patrón: Modelo → Lenguaje.
Los clasificadores (A2 Etapa 1 y A2 Etapa 2) siempre alimentan a G2.
G2 nunca opera de forma independiente.
```

---

## SECCIÓN 2 — Evaluación de calidad con semáforo

> 🟢 **Verde** = listo, sin acciones pendientes
> 🟡 **Amarillo** = necesita trabajo, hay un plan concreto
> 🔴 **Rojo** = bloqueante, requiere replantear antes de continuar

### Dataset / Fuente 1: Datos del cuestionario diagnóstico

| Dimensión | Semáforo | Evidencia que respalda la evaluación | Plan de acción (si es 🟡 o 🔴) |
|---|---|---|---|
| **Disponibilidad** | 🟡 | El cuestionario está diseñado pero no aplicado aún. | Aplicar en sesión piloto (Lucía, Semana 7); recolectar de ≥ 15 usuarios en Semana 13. |
| **Relevancia** | 🟢 | Las variables capturadas son predictores directos del nivel de preparación real. | — |
| **Volumen** | 🟡 | El tamaño de muestra depende de la evaluación con usuarios. | Complementar con datos del equipo y compañeros si la muestra piloto es pequeña. |
| **Legalidad** | 🟡 | Las respuestas del cuestionario son datos personales bajo Ley N.° 29733. | Incluir aviso de privacidad y consentimiento antes de aplicar. |

### Dataset / Fuente 2: Dataset analítico `InterviewIQ-STAR`

| Dimensión | Semáforo | Evidencia que respalda la evaluación | Plan de acción (si es 🟡 o 🔴) |
|---|---|---|---|
| **Disponibilidad** | 🟡 | El dataset será construido por el equipo, pero todavía no existe la versión final. | Construir primeros ~50 pares sintéticos (Aaron, Semana 7); completar ~200 pares (Semana 8). |
| **Volumen** | 🟡 | El número final de respuestas está pendiente de construcción. | Plan B: reducir a 150 pares documentando la limitación. |
| **Calidad** | 🟡 | Se necesita definir y aplicar el protocolo de etiquetado STAR. | Crear reglas claras para S/T/A/R = 0/1 (Lucía, Semana 7); doble etiquetado + kappa de Cohen (Semana 8). |
| **Relevancia** | 🟢 | Las respuestas conductuales etiquetadas con STAR corresponden directamente al input real del sistema. | — |
| **Legalidad** | 🟡 | Si se recolectan respuestas reales, aplica Ley N.° 29733. | Preparar consentimiento informado antes de recolectar (Lucía, Semana 7). |
| **Etiquetas** | 🟡 | Se conoce el target S/T/A/R, pero el dataset no está etiquetado aún. | Protocolo STAR + doble etiquetado (ver Calidad). |
| **Balance** | 🟡 | No verificable hasta tener el dataset. Debe incluir respuestas completas, parciales y deficientes. | Contar positivos/negativos por etiqueta y corregir subrepresentación (Aaron, Semana 8). |
| **Fuga de datos** | 🟡 | Variables sospechosas identificadas; comprobación final pendiente sobre dataset real. | Split por pregunta/plantilla, no solo por fila (Aaron, Semana 9). |
| **Vigencia** | 🟡 | Debe verificarse que las respuestas construidas representen respuestas plausibles de estudiantes, no solo ejemplos STAR perfectos. | Incluir respuestas completas, parciales y deficientes (Lucía + Aaron, Semana 8). |

### Dataset / Fuente 3: Corpus RAG

| Dimensión | Semáforo | Evidencia | Plan de acción |
|---|---|---|---|
| **Disponibilidad** | 🟢 | Fuentes públicas accesibles verificadas. | — |
| **Volumen** | 🟡 | Fuentes iniciales identificadas; corpus definitivo pendiente de cierre. | Seleccionar y guardar fuentes finales (Valeria, Semana 7). |
| **Calidad** | 🟢 | Fuentes institucionales (universidades) y académicas (DOI/PMID verificados). | — |
| **Relevancia** | 🟢 | Las fuentes cubren STAR, entrevistas conductuales y competencias por rol. | — |
| **Legalidad** | 🟡 | Condiciones de uso de cada fuente pendientes de documentación formal. | Registrar URL, autor, fecha de acceso y condiciones de uso (Valeria, Semana 7). |
| **Cobertura** *(generativo)* | 🟡 | No se ha probado recuperación con consultas reales aún. | Crear consultas de prueba y verificar top-k (Valeria + Aaron, Semana 10). |
| **Actualidad** *(generativo)* | 🟡 | Primera revisión formal del corpus definitivo aún no ejecutada. | Ejecutar primera revisión formal (Valeria, Semana 7). |

---

## SECCIÓN 3 — Plan de resolución de bloqueantes

```
No aplica — no se identifican actualmente bloqueadores rojos (🔴).
Los puntos amarillos requieren trabajo antes de PC2 (ver plan abajo).
```

### Plan complementario para pendientes 🟡

| Recurso | Dimensión / problema | Acción concreta | Responsable | Fecha límite | Plan B |
|---|---|---|---|---|---|
| R1 | Cuestionario no aplicado | Aplicar sesión piloto; ajustar variables según respuestas | Lucía | Semana 7 | Complementar con compañeros del equipo |
| R2 | Dataset no construido | Definir esquema CSV final y construir primeros ~50 pares sintéticos | Aaron | Semana 7 | Reducir a 150 pares documentando la limitación |
| R2 | Protocolo STAR pendiente | Crear guía de etiquetado con ejemplos para cada componente | Lucía | Semana 7 | Ronda piloto y corrección antes del etiquetado completo |
| R2 | Consistencia de etiquetas | Doble etiquetado de ~30 pares; medir y documentar kappa de Cohen | Lucía + equipo | Semana 8 | Reentrenar anotadores con ejemplos frontera y repetir |
| R2 | Balance por etiqueta desconocido | Contar positivos/negativos para S, T, A y R; corregir subrepresentación | Aaron | Semana 8 | Generar ejemplos adicionales para etiquetas con menor representación |
| R2 | Leakage pendiente de validar | Revisar columnas; hacer split agrupado por pregunta/plantilla | Aaron | Semana 9 | Agrupar por origen antes de dividir |
| R2 | Consentimiento pendiente | Preparar formulario para respuestas reales | Lucía | Semana 7 | — |
| R3 | Corpus definitivo pendiente | Seleccionar, guardar y documentar fuentes finales del MVP | Valeria | Semana 7 | Reducir a fuentes institucionales/académicas de mayor relevancia |
| R3 | Condiciones de uso | Registrar URL, autor, fecha y licencia de cada fuente | Valeria | Semana 7 | No indexar fuentes cuya reutilización no pueda justificarse |
| R3 | Retrieval no probado | Crear consultas de prueba y verificar recuperación top-k | Valeria + Aaron | Semana 10 | Ajustar chunking, embeddings o corpus según errores encontrados |

---

## SECCIÓN 4 — Privacidad y legalidad de los datos

| Pregunta | Respuesta | Detalle |
|---|---|---|
| ¿Los datos contienen información personal de usuarios? | SÍ (condicional) | Si se recolectan respuestas reales de estudiantes para R1 o R2. |
| ¿Se cuenta con consentimiento explícito para usar esos datos? | SÍ (pendiente de implementar) | Se preparará formulario antes de recolectar cualquier respuesta real. |
| ¿Los datos serán anonimizados antes de usarlos en el proyecto? | SÍ | Eliminar nombres, correos u otros identificadores antes de usar los textos. |
| ¿Aplica la Ley N° 29733 de Protección de Datos Personales del Perú? | SÍ | Aplica si se procesan datos personales de participantes peruanos. |
| ¿Hay alguna restricción contractual o de confidencialidad? | NO | No identificadas actualmente. No solicitar información confidencial de empleadores. |

Las respuestas reales de usuarios no se publicarán en el repositorio. La carpeta `data/raw/` estará en `.gitignore` si contiene respuestas reales.

---

## SECCIÓN 5 — Autoevaluación del equipo

| Pregunta de control | Respuesta |
|---|---|
| ¿Se identificaron los tres recursos de datos del sistema (cuestionario, dataset STAR, corpus RAG)? | **SÍ** |
| ¿Cada semáforo tiene evidencia concreta que lo respalda? | **SÍ** |
| ¿Todos los 🔴 tienen un plan de acción con fecha y responsable? | **SÍ (no hay 🔴; cada punto 🟡 tiene acción, responsable y fecha)** |
| ¿El equipo verificó el acceso real a los datos antes de completar este checklist? | **SÍ (fuentes RAG verificadas; datasets propios pendientes de construcción)** |
| ¿La estrategia de contexto es coherente con los datos disponibles? | **SÍ (coherente con G2 — RAG)** |
| ¿Hay casos suficientes de cada categoría, no solo filas en total? | **Pendiente de verificar cuando se construya el dataset** |
| ¿Se revisó variable por variable que no haya fuga de datos? | **Diseño realizado; validación final pendiente sobre el dataset real** |
| ¿Se definió qué información viaja entre los tres recursos y entre A2 y G2? | **SÍ** |
| ¿Se definió tratamiento de privacidad para respuestas reales? | **SÍ** |

> **Si alguna respuesta es NO → el checklist no está listo para entregar.**

### Conclusión de readiness

**Estado general: 🟡 Amarillo — viable, pero todavía no listo para entrenamiento.**

El recurso R3 (corpus RAG) está en el mejor estado: fuentes verificadas y accesibles. El recurso R1 (cuestionario diagnóstico) tiene diseño definido pero recolección pendiente. El recurso R2 (dataset `InterviewIQ-STAR`) es el principal bloqueante para PC2: tiene diseño definido pero construcción y etiquetado pendientes.

---

## Fuentes iniciales verificadas para el corpus RAG

1. University of Southern California Career Center. *Interview Preparation* — metodología STAR y entrevistas conductuales.
2. UC Santa Cruz Career Success. *Interview Prep* — explicación de Situation, Task, Action y Result.
3. Wilkie, L. & Rosendale, J. (2024). *Efficacy and Benefits of Virtual Mock Interviews: Analysing Student Perceptions of Digital Employment Preparations*. Journal of University Teaching and Learning Practice, 21(1). DOI: 10.53761/rvtxt659.
4. Marcus, J. A. et al. (2023). *Evaluating the Effectiveness of a Virtual Mock Interview for Health Professions Students*. Journal of Nursing Education, 62(8), 479–482. PMID: 37561904.
5. European Commission. *ESCO — European Skills, Competences, Qualifications and Occupations*.

> **Nota:** Wilkie & Rosendale y Marcus et al. respaldan principalmente la pertinencia de las entrevistas simuladas como intervención. Para el contenido operativo del RAG sobre cómo estructurar respuestas STAR se priorizan las guías universitarias y, para contextualización por rol, ESCO.

---
