# Plantilla 2 — Data Readiness Checklist
## Framework PROMPT | Fase R — Recursos de Datos
### AD5018 Inteligencia Artificial para Negocios | UTEC

---

**Equipo:**
- Integrante 1: Valeria Briceño
- Integrante 2: Lucía Rodríguez
- Integrante 3: Aaron Van Oord


**Proyecto:** InterviewIQ — Simulador Inteligente de Entrevistas para Universitarios
**Fecha de entrega:** 19/09/2026
**Tipo de IA del proyecto:** A2 (clasificación multilabel STAR) + G2 (RAG)

---

> **Estado de esta versión:** el diseño de datos está definido, pero el dataset analítico A2 todavía está pendiente de construcción y validación. Por ello, las dimensiones relacionadas con volumen, balance, etiquetas y leakage se marcan en amarillo hasta contar con evidencia real.

---

## SECCIÓN 1 — Inventario de datos

### Parte A — Componente generativo: inventario de conocimiento

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
- [ ] **G3/G4** Agente con herramientas *(completa además el inventario de herramientas)*
- [ ] Memoria de sesión *(se combina con cualquiera de las anteriores)*

El sistema recuperará fragmentos relevantes de las fuentes seleccionadas y los combinará con la respuesta original del estudiante y con la salida del clasificador A2. El objetivo es que el feedback no dependa únicamente del conocimiento general del LLM, sino que pueda apoyarse en contenido seleccionado sobre metodología STAR, entrevistas conductuales y competencias asociadas a roles.

**Si el nivel es G2 (RAG):**

| Pregunta | Respuesta del equipo |
|---|---|
| ¿En qué fragmentos se parten los documentos? | Configuración inicial propuesta: fragmentos de aproximadamente **300–500 tokens**, respetando en lo posible títulos, subtítulos y límites semánticos. El tamaño definitivo se ajustará mediante pruebas de recuperación. |
| ¿Quién los actualiza y cada cuánto? | **Responsable principal: Valeria Briceño.** Revisará las fuentes antes de la construcción del MVP y nuevamente antes de la evaluación final de PC2. Si una fuente cambia, deja de estar disponible o se incorpora una fuente mejor, se actualizará el corpus y se registrará el cambio en `README_data.md`. |
| ¿Cómo se comprobará que recupera el documento correcto? | Se construirá un conjunto pequeño de consultas de prueba con una fuente o fragmento esperado. Se revisará si el contenido relevante aparece dentro de los primeros resultados recuperados (top-k). La evaluación final incluirá una métrica de recuperación, además de revisión manual de que el feedback esté sustentado por el contexto recuperado. |

**Si el nivel es G3 o G4 — inventario de herramientas del agente:**

| # | Herramienta | Sistema al que toca | ¿Lee o escribe? | Costo por llamada |
|---|---|---|---|---|
| 1 | N/A — el MVP no requiere herramientas externas de agente | N/A | N/A | N/A |

---

### Parte B — Componente analítico: inventario de datos históricos

| # | Dataset | Fuente | Formato | N° de registros aprox. | ¿Tiene etiquetas? |
|---|---|---|---|---|---|
| 1 | `InterviewIQ-STAR` | Dataset propio del equipo; construcción pendiente | CSV | **Pendiente de definir** | Pendiente |
| 2 | Preguntas conductuales de referencia | Fuentes públicas seleccionadas sobre entrevistas conductuales | CSV / texto | Pendiente | NO (no aplica como target) |

**Variable objetivo (target):**

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
- [x] Clasificación — decide entre categorías (SÍ/NO, A/B/C) *(multilabel: cuatro etiquetas binarias S/T/A/R)*
- [ ] Regresión — estima un número
- [ ] Agrupamiento — encuentra grupos sin categorías previas

**Recuento de casos por categoría** *(el total de filas no basta)*:

| Categoría que se quiere distinguir | N° de casos disponibles |
|---|---|
| Situation (S) | Pendiente — dataset aún no construido |
| Task (T) | Pendiente — dataset aún no construido |
| Action (A) | Pendiente — dataset aún no construido |
| Result (R) | Pendiente — dataset aún no construido |

Actualmente **no existe un conteo verificable**, porque el dataset todavía no ha sido construido y etiquetado. Por tanto, no se reportarán cantidades inventadas. Antes del entrenamiento se calcularán los positivos y negativos reales para S, T, A y R y se comprobará si existe suficiente representación para cada etiqueta. El equipo buscará que ninguna etiqueta quede representada por muy pocos ejemplos y revisará el balance antes de realizar el split de entrenamiento, validación y prueba.

**Revisión de fuga de datos** *(obligatoria)*:

| Variable sospechosa | ¿Existe antes del hecho a predecir? | Decisión |
|---|---|---|
| `answer` | SÍ | Se mantiene (feature principal) |
| `question` | SÍ | Se mantiene / evaluar su inclusión; disponible al momento de predicción |
| `situation`, `task`, `action`, `result` | NO | Se elimina como feature (son los targets; nunca entran como features) |
| `annotator` | NO (no es información del usuario) | Se elimina (excluir del modelo) |
| `source` | Puede existir como metadato | Se elimina (evita que el modelo aprenda patrones artificiales de procedencia) |
| Feedback generado después de clasificar | NO | Se elimina completamente |

Además, si se generan varias respuestas a partir de una misma pregunta o plantilla, se evitará que ejemplos casi idénticos queden simultáneamente en train y test. El split se diseñará para reducir esta forma de leakage.

**Responsable de esta revisión:** Aaron Van Oordt, con revisión del equipo.

---

### Parte C — Cómo se conectan los datos de ambos componentes

```
¿Qué dato exactamente viaja de un componente al otro?

Patrón: Modelo → Lenguaje.

pregunta conductual + respuesta del estudiante
  → A2 clasificador STAR
  → S/T/A/R presente o ausente
  → G2 retrieval de fuentes relevantes
  → LLM
  → feedback personalizado

El componente A2 envía a G2:
1. La respuesta textual original del estudiante.
2. La pregunta conductual realizada.
3. La predicción de presencia/ausencia para S, T, A y R.
4. Cuando corresponda, scores o probabilidades/confianza del modelo.

G2 usa esa información para decidir qué aspecto de la respuesta necesita
mayor explicación y recuperar contenido relevante del corpus RAG.
```

---

## SECCIÓN 2 — Evaluación de calidad con semáforo

> *Instrucciones para el semáforo:*
> 🟢 **Verde** = listo, sin acciones pendientes
> 🟡 **Amarillo** = necesita trabajo, hay un plan concreto
> 🔴 **Rojo** = bloqueante, requiere replantear antes de continuar

### Dataset / Fuente principal: Dataset analítico `InterviewIQ-STAR`

| Dimensión | Semáforo | Evidencia que respalda la evaluación | Plan de acción (si es 🟡 o 🔴) |
|---|---|---|---|
| **Disponibilidad** — ¿Los datos existen y son accesibles? | 🟡 | El dataset será construido por el equipo, pero todavía no existe la versión final. | Definir tamaño final, fuentes de respuestas y esquema del CSV; construir la primera versión (Aaron, Semana 7). |
| **Volumen** — ¿Hay casos suficientes según la tabla de mínimos? | 🟡 | El número final de respuestas todavía está pendiente de definición y construcción. | Igual que Disponibilidad. Plan B: reducir alcance del dataset manteniendo suficiente cobertura por etiqueta y documentar la limitación. |
| **Calidad** — ¿Los datos están completos y son consistentes? | 🟡 | Se necesita definir y aplicar el protocolo de etiquetado STAR. | Crear reglas claras y ejemplos para S/T/A/R = 1 o 0 (Lucía, Semana 7); doble etiquetado de una muestra y medir acuerdo entre anotadores (Lucía + equipo, Semana 8). |
| **Relevancia** — ¿Los datos representan el problema definido en Fase P? | 🟢 | Las respuestas a entrevistas conductuales corresponden directamente al input real que analizará InterviewIQ. | — |
| **Legalidad** — ¿Hay autorización para usar estos datos? | 🟡 | Las respuestas sintéticas/manuales no plantean el mismo riesgo que datos personales; si se recolectan respuestas reales se requerirá consentimiento y tratamiento conforme a la Ley N.° 29733. | Preparar consentimiento informado antes de recolectar respuestas reales (ver Sección 4). |
| **Etiquetas** *(analítico)* — ¿Sabemos el resultado real de cada caso pasado? | 🟡 | Se conoce el target S/T/A/R, pero el dataset todavía no está etiquetado. | Protocolo STAR + doble etiquetado (ver Calidad). Plan B: ronda piloto y corrección de reglas ambiguas antes del etiquetado completo. |
| **Balance** *(analítico)* — ¿Hay casos suficientes de cada categoría? | 🟡 | No puede comprobarse hasta tener el dataset y contar positivos/negativos por etiqueta. | Contar positivos/negativos para S, T, A y R y corregir subrepresentación antes del entrenamiento (Aaron, Semana 8). Plan B: generar/recolectar ejemplos adicionales para las etiquetas con menor representación. |
| **Fuga de datos** *(analítico)* — ¿Se revisó variable por variable? | 🟡 | Las variables sospechosas ya fueron identificadas, pero la comprobación final se hará sobre el dataset construido. | Revisar columnas y hacer un split que evite duplicados o ejemplos casi idénticos entre train/test (Aaron, Semana 9). Plan B: agrupar por pregunta/plantilla/origen antes de dividir. |
| **Vigencia** *(analítico)* — ¿Los datos describen la realidad actual del negocio? | 🟡 | Debe verificarse que las respuestas construidas representen respuestas plausibles de estudiantes universitarios y no solamente ejemplos STAR perfectos. | Revisar que el dataset incluya respuestas completas, parciales y deficientes (Lucía + Aaron, Semana 8). Plan B: incorporar ejemplos adicionales que cubran combinaciones STAR faltantes. |
| **Cobertura** *(generativo)* — ¿Los documentos cubren lo que se va a preguntar? | N/A | Corresponde al corpus G2 (ver fuente secundaria). | — |
| **Actualidad** *(generativo)* — ¿Hay alguien encargado de mantenerlos al día? | N/A | Corresponde al corpus G2 (ver fuente secundaria). | — |
| **Permisos** *(solo agentes)* — ¿Cada herramienta tiene su alcance acotado? | N/A | El MVP G2 no requiere un agente con herramientas externas. | — |

---

### Dataset / Fuente secundaria *(si aplica)*: Corpus RAG

| Dimensión | Semáforo | Evidencia | Plan de acción |
|---|---|---|---|
| **Disponibilidad** | 🟢 | Se localizaron fuentes públicas y accesibles de universidades, literatura académica y ESCO. | — |
| **Volumen** | 🟡 | Ya existen fuentes iniciales suficientes para comenzar, pero falta cerrar el corpus definitivo y comprobar si cubre todos los roles/sectores del MVP. | Seleccionar, guardar y documentar las fuentes finales del MVP (Valeria, Semana 7). Plan B: reducir el corpus a fuentes institucionales/académicas de mayor relevancia. |
| **Calidad** | 🟢 | Las fuentes iniciales incluyen centros de carrera universitarios, publicaciones académicas y una clasificación oficial de la Comisión Europea. | — |
| **Relevancia** | 🟢 | Las fuentes cubren STAR, entrevistas conductuales, preparación para entrevistas y competencias/ocupaciones. | — |
| **Legalidad** | 🟡 | Antes de indexar el corpus definitivo se documentará la procedencia y condiciones de uso de cada fuente. | Registrar URL, autor/institución, fecha de acceso y condiciones de uso/licencia (Valeria, Semana 7). Plan B: no indexar una fuente cuya reutilización no pueda justificarse; reemplazarla por otra. |
| **Vigencia** | 🟢 | Las fuentes se encuentran disponibles actualmente; ESCO mantiene una versión actualizada y las fuentes universitarias están accesibles. | — |
| **Cobertura** *(generativo)* | 🟡 | Falta probar sistemáticamente si las consultas del MVP recuperan contenido útil para todos los casos definidos. | Crear consultas de prueba y verificar recuperación top-k (Valeria + Aaron, Semana 10). Plan B: ajustar chunking, embeddings o corpus según los errores encontrados. |
| **Actualidad** *(generativo)* | 🟡 | Se definió responsable y proceso de revisión, pero todavía no se ejecutó la primera revisión formal del corpus final. | Ejecutar la primera revisión formal (Valeria; ver Sección 1, Parte A). |

---

## SECCIÓN 3 — Plan de resolución de bloqueantes

> *Por cada semáforo 🔴 en cualquier dimensión, el equipo debe completar este plan. Si no hay ningún 🔴, escribir "No aplica".*

### Bloqueante 1
```
No aplica — no se identifican actualmente bloqueadores rojos.
Los puntos amarillos requieren trabajo antes de PC2 (ver plan abajo).
```

### Bloqueante 2 *(si aplica)*
```
No aplica
```

### Plan complementario para pendientes 🟡

| Dimensión / problema | Acción concreta | Responsable | Fecha límite | Plan B |
|---|---|---|---|---|
| Dataset A2 aún no construido | Definir tamaño final, fuentes de respuestas y esquema del CSV; construir la primera versión | Aaron | Semana 7 | Reducir alcance del dataset manteniendo suficiente cobertura por etiqueta y documentar la limitación |
| Protocolo STAR pendiente | Crear reglas claras y ejemplos para decidir cuándo S/T/A/R = 1 o 0 | Lucía | Semana 7 | Hacer una ronda piloto y corregir reglas ambiguas antes del etiquetado completo |
| Consistencia de etiquetas | Hacer doble etiquetado de una muestra y medir acuerdo entre anotadores; resolver desacuerdos | Lucía + equipo | Semana 8 | Reentrenar a los anotadores con ejemplos frontera y repetir la muestra |
| Balance por etiqueta desconocido | Contar positivos/negativos para S, T, A y R y corregir subrepresentación antes del entrenamiento | Aaron | Semana 8 | Generar/recolectar ejemplos adicionales dirigidos a las etiquetas con menor representación |
| Leakage pendiente de validar | Revisar columnas y realizar un split que evite duplicados o ejemplos casi idénticos entre train/test | Aaron | Semana 9 | Agrupar por pregunta/plantilla/origen antes de dividir los datos |
| Corpus RAG definitivo pendiente | Seleccionar, guardar y documentar las fuentes finales del MVP | Valeria | Semana 7 | Reducir el corpus a fuentes institucionales/académicas de mayor relevancia |
| Condiciones de uso del corpus | Registrar URL, autor/institución, fecha de acceso y condiciones de uso/licencia disponibles | Valeria | Semana 7 | No indexar una fuente cuya reutilización no pueda justificarse; reemplazarla por otra fuente |
| Cobertura de retrieval no probada | Crear consultas de prueba y verificar recuperación top-k | Valeria + Aaron | Semana 10 | Ajustar chunking, embeddings o corpus según los errores encontrados |
| Representatividad de respuestas | Revisar que el dataset incluya respuestas completas, parciales y deficientes, no solo ejemplos ideales | Lucía + Aaron | Semana 8 | Incorporar ejemplos adicionales diseñados para cubrir combinaciones STAR faltantes |

---

## SECCIÓN 4 — Privacidad y legalidad de los datos

> *Responde cada pregunta con SÍ, NO o N/A.*

| Pregunta | Respuesta | Detalle |
|---|---|---|
| ¿Los datos contienen información personal de usuarios? | SÍ | Sí, si se recolectan respuestas reales de estudiantes. Evitar solicitar datos personales innecesarios y advertir al participante que no incluya nombres, empresas u otra información identificable cuando no sea necesaria. |
| ¿Se cuenta con consentimiento explícito para usar esos datos? | SÍ | Se solicitará para respuestas reales usadas en validación o dataset. Preparar consentimiento informado antes de recolectar respuestas. |
| ¿Los datos serán anonimizados antes de usarlos en el proyecto? | SÍ | Sustituir/eliminar nombres, correos, teléfonos, empresas u otros identificadores antes de usar los textos. |
| ¿Aplica la Ley N° 29733 de Protección de Datos Personales del Perú? | SÍ | Aplica si se procesan datos personales de participantes. Documentar el tratamiento de datos y limitar su uso al propósito académico declarado. |
| ¿Hay alguna restricción contractual o de confidencialidad? | NO | No identificadas actualmente para el dataset propio. No solicitar información confidencial de empleadores o procesos reales; verificar condiciones de las fuentes externas antes de incorporarlas al corpus. |

Las respuestas reales no se publicarán en el repositorio. Si el equipo las almacena localmente para evaluación, la carpeta correspondiente deberá mantenerse fuera del repositorio público.

---

## SECCIÓN 5 — Autoevaluación del equipo

| Pregunta de control | Respuesta |
|---|---|
| ¿Cada semáforo tiene evidencia concreta que lo respalda? | SÍ |
| ¿Todos los 🔴 tienen un plan de acción con fecha y responsable? | SÍ (no hay 🔴; cada punto 🟡 pendiente tiene acción, responsable y fecha) |
| ¿El equipo verificó el acceso real a los datos antes de completar este checklist? | SÍ (se verificó acceso real a las fuentes RAG iniciales) |
| ¿La estrategia de contexto es coherente con los datos disponibles? | SÍ (coherente con G2) |
| ¿Hay casos suficientes de **cada** categoría, no solo filas en total? | **Pendiente de verificar cuando se construya el dataset** |
| ¿Se revisó variable por variable que no haya fuga de datos? | Diseño realizado; **validación final pendiente sobre el dataset real** |
| ¿Están inventariadas las herramientas del agente, si el producto tiene una? | N/A (no se requieren herramientas externas de agente) |
| ¿Se definió qué información viaja entre A2 y G2? | SÍ |
| ¿Se definió tratamiento de privacidad para respuestas reales? | SÍ |

> **Si alguna respuesta es NO → el checklist no está listo para entregar.**

### Conclusión de readiness

**Estado general: 🟡 Amarillo — viable, pero todavía no listo para entrenamiento.**

La principal dependencia es construir y etiquetar el dataset `InterviewIQ-STAR`. El componente G2 tiene fuentes iniciales reales y accesibles, mientras que el componente A2 cuenta con un target y una estrategia definidos, pero todavía necesita evidencia concreta de volumen, balance, calidad de etiquetas y ausencia de leakage.

Esto no invalida el proyecto para PC1: documenta de forma explícita qué recursos existen actualmente y qué acciones deben completarse antes del entrenamiento en PC2.

---

## Fuentes iniciales verificadas para el corpus / sustento

1. University of Southern California Career Center. *Interview Preparation* — metodología STAR y entrevistas conductuales.
2. UC Santa Cruz Career Success. *Interview Prep* — explicación de Situation, Task, Action y Result.
3. Wilkie, L. & Rosendale, J. (2024). *Efficacy and Benefits of Virtual Mock Interviews: Analysing Student Perceptions of Digital Employment Preparations*. Journal of University Teaching and Learning Practice, 21(1). DOI: 10.53761/rvtxt659.
4. Marcus, J. A. et al. (2023). *Evaluating the Effectiveness of a Virtual Mock Interview for Health Professions Students*. Journal of Nursing Education, 62(8), 479–482. PMID: 37561904.
5. European Commission. *ESCO — European Skills, Competences, Qualifications and Occupations*. Fuente complementaria para ocupaciones y competencias asociadas a roles.

> **Nota:** Wilkie & Rosendale y Marcus et al. respaldan principalmente la pertinencia de las entrevistas simuladas como intervención. Para el contenido operativo del RAG sobre cómo estructurar respuestas STAR se priorizan las guías universitarias y, para contextualización por rol, ESCO.

---

*Framework PROMPT v2.0 — AD5018 UTEC | Plantilla 2 de 4*
