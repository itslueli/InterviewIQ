# Plantilla 3 — AI Product Canvas
## Fase O — Diseño del Producto de IA
### AD5018 Inteligencia Artificial para Negocios | UTEC

---

**Equipo:**
- Integrante 1: Valeria Briceño
- Integrante 2: Lucía Rodríguez
- Integrante 3: Jennifer Patiño
- Integrante 4: Aaron Van Oord

**Proyecto:** InterviewIQ — Simulador Inteligente de Entrevistas para Universitarios

> **Nota de versión final (PC2 — Semana 14):** Esta plantilla corresponde al diseño original (PC1). El MVP implementado realizó dos ajustes: (1) la **Etapa 1** (clasificador de nivel de preparación con Logistic Regression) quedó fuera del alcance del MVP — no se entrenó ni se desplegó; (2) el componente generativo bajó de **G2 (RAG con GPT-4o-mini + ChromaDB)** a **G1 (Gemini 2.5 Flash vía API REST)** con fallback automático a reglas estructuradas. El flujo del MVP no incluye cuestionario diagnóstico ni generación de preguntas adaptadas: el usuario selecciona una pregunta del banco o escribe la propia, escribe su respuesta, y recibe análisis STAR + feedback de Gemini.

---

## SECCIÓN 1 — Descripción del producto

### 1.1 Nombre del producto
**InterviewIQ** — Simulador conversacional de entrevistas por competencias con retroalimentación estructurada.

### 1.2 Usuario objetivo
Estudiantes universitarios peruanos de últimos ciclos que buscan prácticas preprofesionales o su primer empleo y necesitan prepararse para entrevistas laborales por competencias, sin acceso a coaching profesional.

### 1.3 Propuesta de valor
InterviewIQ permite que cualquier estudiante pueda practicar entrevistas conductuales de manera recurrente y recibir retroalimentación estructurada sobre la calidad de sus respuestas STAR, adaptada a su nivel de preparación y al rol que busca.

### 1.4 Descripción funcional del producto

> **MVP implementado (PC2):** El flujo se simplificó respecto al diseño original. Etapa 1 (diagnóstico de nivel) quedó fuera del alcance. El componente generativo pasó de G2 (RAG) a G1 (Gemini 2.5 Flash vía API REST).

El MVP ofrece el siguiente flujo de práctica:

1. **Selección de pregunta:** El usuario elige una pregunta conductual del banco predefinido o escribe la suya propia (texto libre).

2. **Respuesta y análisis STAR:** El usuario escribe su respuesta en texto libre. El clasificador STAR (componente A2 — TF-IDF bigramas + LinearSVC + CalibratedClassifierCV) detecta la presencia o ausencia de cada componente (Situación, Tarea, Acción, Resultado) con umbrales calibrados por etiqueta.

3. **Retroalimentación personalizada:** Gemini 2.5 Flash recibe la respuesta original más las predicciones S/T/A/R y genera feedback específico. Si la API key no está disponible, el sistema usa reglas estructuradas como fallback automático.

**Flujo del MVP implementado:**

```
[Selección de pregunta del banco o texto libre]
        ↓
[Respuesta del usuario en texto libre]
        ↓
[Clasificador STAR — A2 (TF-IDF bigramas + LinearSVC + CalibratedClassifierCV)]
Output: S ∈ {0,1}, T ∈ {0,1}, A ∈ {0,1}, R ∈ {0,1} con umbrales por etiqueta
        ↓
[G1 — Gemini 2.5 Flash vía API REST]
Input: respuesta + predicciones STAR
Output: feedback personalizado
(fallback: reglas estructuradas si no hay GEMINI_API_KEY)
        ↓
[Feedback mostrado al estudiante]
```

**Flujo original diseñado (PC1 — no implementado en MVP):**

```
[Cuestionario diagnóstico] → [Clasificador de nivel — Etapa 1] → [Preguntas adaptadas — LLM]
→ [Respuesta] → [Clasificador STAR A2] → [RAG corpus] → [LLM feedback — G2]
```

---

## SECCIÓN 2 — Model Design Canvas

### 2.1 Componente analítico — Etapa 1: Clasificador de nivel de preparación *(diseño original — no implementado en MVP)*

> **Estado en MVP:** Quedó fuera del alcance. No se entrenó ni desplegó. Documentado como deuda técnica en `plantillas/plantilla_4_scorecard_risk.md`.

| Elemento | Detalle |
|---|---|
| **Tarea** | Clasificación multiclase |
| **Input** | Respuestas del cuestionario diagnóstico (5 variables numéricas/ordinales) |
| **Output** | `nivel` ∈ {básico, intermedio, avanzado} |
| **Algoritmo** | Logistic Regression (sklearn) |
| **Dataset de entrenamiento** | Recurso 1 — datos del cuestionario diagnóstico recolectados de estudiantes |
| **Tamaño esperado** | ≥ 50 respuestas (misma encuesta que validó el problema) |
| **Split** | 70% entrenamiento / 10% validación / 20% test |
| **Métrica principal** | Accuracy |
| **Criterio mínimo de aceptación** | Accuracy ≥ 0.65 en validación |
| **Costo del error** | Bajo: error de clasificación de nivel ajusta la dificultad de preguntas; no afecta directamente la evaluación de respuestas |
| **Estado final** | ❌ No implementado — deuda técnica |

### 2.2 Componente analítico — Clasificador STAR (A2 — implementado ✅)

| Elemento | Detalle |
|---|---|
| **Tarea** | Clasificación multilabel (4 etiquetas independientes: S, T, A, R) |
| **Input** | Respuesta del usuario en texto libre (variable `answer`) |
| **Output** | Vector binario (S, T, A, R) ∈ {0,1}⁴ |
| **Algoritmo baseline** | TF-IDF + Logistic Regression (OneVsRest) |
| **Algoritmo implementado** | TF-IDF bigramas + LinearSVC + CalibratedClassifierCV (mejor resultado) |
| **Dataset de entrenamiento** | Recurso 2 — InterviewIQ-STAR (200 pares etiquetados) |
| **Split** | 70% entrenamiento / 10% validación / 20% test |
| **Métrica principal** | Macro F1 (promedia las 4 etiquetas con igual peso) |
| **Resultado obtenido** | **F1 promedio = 0.808** ✅ (supera criterio mínimo) |
| **Criterio mínimo de aceptación** | Macro F1 ≥ 0.65 sobre el conjunto de test |
| **Umbrales calibrados por etiqueta** | situacion=0.30, tarea=0.30, accion=0.75, resultado=0.50 |
| **Costo del error** | **Falso positivo más costoso:** indicar que un componente STAR está presente cuando no lo está significa decirle al estudiante que su respuesta es buena cuando no lo es. Los umbrales se ajustaron por etiqueta priorizando reducir falsos positivos. |
| **¿Se pasa al componente generativo?** | Sí — las predicciones (S, T, A, R) se pasan directamente al prompt de G1 |

### 2.3 Componente generativo — G1 (implementado ✅) / G2 diseño original

> **MVP:** Se implementó G1 (Gemini 2.5 Flash vía API REST). G2 (RAG con GPT-4o-mini) quedó como deuda técnica.

**G1 — Implementado en MVP:**

| Elemento | Detalle |
|---|---|
| **Tipo de tarea** | Generación de texto (feedback personalizado sobre la respuesta STAR) |
| **Modelo LLM** | Gemini 2.5 Flash (Google AI) |
| **Integración** | API REST con `requests`; clave en Streamlit secrets (`GEMINI_API_KEY`) |
| **Input** | Respuesta original del usuario + predicciones S/T/A/R del clasificador A2 |
| **Output** | Feedback personalizado: fortalezas, componentes ausentes y recomendaciones |
| **Fallback** | Reglas estructuradas automáticas si no hay `GEMINI_API_KEY` |
| **Restricciones del system prompt** | El LLM no puede: (1) inventar experiencias del usuario, (2) afirmar probabilidades de contratación, (3) contradecir la salida de A2, (4) marcar como presentes componentes que A2 marcó ausentes |
| **¿Depende del componente analítico?** | Sí (Patrón 1: Modelo → Lenguaje) — G1 siempre recibe las predicciones de A2 antes de generar feedback |

**G2 — Diseño original (no implementado — deuda técnica):**

| Elemento | Detalle |
|---|---|
| **Modelo LLM** | GPT-4o-mini (API OpenAI) |
| **Corpus RAG** | ~20–50 documentos sobre metodología STAR y competencias por rol (Recurso 3) |
| **Embeddings** | text-embedding-3-small (OpenAI) |
| **Índice vectorial** | FAISS o ChromaDB |
| **Retrieval** | Top-k (k=3–5) por similitud coseno |
| **Estado** | ❌ No implementado — deuda técnica documentada en plantilla_4 |

### 2.4 Patrón de conexión entre componentes

- [x] **Patrón 1 — Modelo → Lenguaje:** La salida del clasificador STAR (A2) alimenta la generación de feedback. G1 no opera de manera independiente — siempre recibe las predicciones S/T/A/R antes de generar el feedback.
- [ ] **Patrón 2 — Lenguaje → Modelo**
- [ ] **Patrón 3 — Modelo como herramienta del agente**

---

## SECCIÓN 3 — Inputs y outputs del sistema

### 3.1 Inputs del sistema

| Input | Descripción | Formato | Momento en el flujo | Estado MVP |
|---|---|---|---|---|
| Pregunta conductual | Pregunta seleccionada del banco o escrita por el usuario | Texto libre o selección | Inicio de la sesión | ✅ Implementado |
| Respuesta conductual | Respuesta del estudiante a la pregunta | Texto libre | Sesión de práctica | ✅ Implementado |
| Rol objetivo | Puesto al que aplica el estudiante | Selección de lista | Inicio *(diseño original)* | ⚠️ Banco fijo en MVP |
| Cuestionario diagnóstico | 5 ítems sobre experiencia, confianza, conocimiento STAR | Variables ordinales | Inicio *(diseño original)* | ❌ No implementado |

### 3.2 Outputs del sistema

| Output | Descripción | Generado por | Estado MVP |
|---|---|---|---|
| Predicciones STAR | S/T/A/R ∈ {0,1} con probabilidad por componente | Clasificador STAR A2 (TF-IDF + SVM) | ✅ Implementado |
| Feedback personalizado | Análisis con fortalezas, componentes ausentes y recomendaciones | Gemini 2.5 Flash (G1) o reglas fallback | ✅ Implementado |
| Nivel de preparación | `básico` / `intermedio` / `avanzado` | Clasificador Etapa 1 *(diseño original)* | ❌ No implementado |
| Preguntas adaptadas | Preguntas ajustadas al rol y nivel | LLM G2 *(diseño original)* | ❌ No implementado |

---

## SECCIÓN 4 — OKRs y métricas de impacto

### Objetivo general
Incrementar la preparación percibida y la capacidad de estructurar respuestas conductuales de los estudiantes universitarios peruanos que buscan prácticas o primer empleo.

### Key Results

| KR | Indicador | Baseline (n=50) | Meta | Resultado MVP (n=8) | Estado |
|---|---|---|---|---|---|
| **KR1** | % que se sienten poco o nada preparados | **60%** | ≤ 40% | **62.5% → 25%** (pre/post) | ✅ Cumplido |
| **KR2** | % con dificultad para estructurar respuestas STAR | **80%** | ≤ 55% | **37.5% → 25%** (pre/post) | ✅ Cumplido |
| **KR3** | % que nunca reciben feedback estructurado | **40%** | ≥ 90% reciben ≥ 1 sesión | **87.5%** (7/8 recibieron feedback) | ✅ Cumplido |

> Medición aplicada con cuestionario pre/post a 8 usuarios externos al equipo (n=8). Los 3 KRs fueron cumplidos.

### Métricas técnicas

| Componente | Métrica | Criterio mínimo | Resultado |
|---|---|---|---|
| Clasificador STAR A2 | Macro F1 en test | ≥ 0.65 | **0.808** ✅ |
| G1 Gemini 2.5 Flash | Coherencia de feedback con predicciones A2 | Fallback funcional | ✅ Implementado con fallback |
| Clasificador Etapa 1 | Accuracy en test | ≥ 0.65 | ❌ No implementado |
| Pipeline RAG G2 | Retrieval precision@k | ≥ 0.80 | ❌ No implementado |

---

## SECCIÓN 5 — Arquitectura del MVP

### 5.1 Stack tecnológico

| Capa | Tecnología diseño original (PC1) | Tecnología MVP implementado (PC2) |
|---|---|---|
| Interfaz | Streamlit | Streamlit ✅ |
| Clasificador de nivel | scikit-learn (Logistic Regression) | ❌ No implementado |
| Clasificador STAR | scikit-learn (TF-IDF + LR y LinearSVC) | scikit-learn (TF-IDF bigramas + LinearSVC + CalibratedClassifierCV) ✅ |
| Embeddings | OpenAI text-embedding-3-small | ❌ No aplica (G2 no implementado) |
| Índice vectorial | FAISS o ChromaDB | ❌ No aplica (G2 no implementado) |
| LLM | GPT-4o-mini (API OpenAI) | Gemini 2.5 Flash (API REST con `requests`) ✅ |
| Despliegue | Streamlit Community Cloud | Streamlit Community Cloud ✅ |

### 5.2 Alcance del MVP

**Implementado ✅:**
- Banco de preguntas conductuales predefinidas + opción de texto libre
- Análisis STAR de la respuesta (clasificador A2)
- Feedback personalizado (Gemini 2.5 Flash con fallback a reglas estructuradas)
- Interfaz web accesible desde cualquier dispositivo
- Despliegue público en https://interviewiq-utec.streamlit.app/

**Quedó fuera del MVP ❌ (deuda técnica):**
- Cuestionario diagnóstico + clasificación de nivel (Etapa 1)
- Generación de preguntas adaptadas al rol y nivel
- Pipeline RAG (corpus, embeddings, índice vectorial) — G2
- Autenticación de usuarios
- Base de datos persistente de sesiones

### 5.3 Diagrama de componentes (MVP implementado)

```
┌──────────────────────────────────────────────────────┐
│                  Interfaz Streamlit                  │
│  [Banco de preguntas / texto libre] → [Respuesta]   │
└────────────────────────┬─────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Clasificador STAR  │
              │       (A2)          │
              │  TF-IDF bigramas +  │
              │  LinearSVC + Calib. │
              │  F1 promedio=0.808  │
              │  Output: S,T,A,R   │
              └──────────┬──────────┘
                         │  predicciones + respuesta original
              ┌──────────▼──────────┐
              │  G1 — Gemini 2.5   │
              │  Flash (API REST)  │
              │  Fallback: reglas  │
              │  Output: feedback  │
              └──────────┬──────────┘
                         │
              ┌──────────▼──────────┐
              │  Feedback al        │
              │  estudiante         │
              └─────────────────────┘
```

---

## SECCIÓN 6 — Riesgos y consideraciones éticas

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Dataset STAR insuficiente (< 150 pares) | Media | Alto | Generación sintética con LLM + validación manual; protocolo de etiquetado con doble anotador y kappa de Cohen |
| Clasificador STAR con Macro F1 < 0.65 | Media | Alto | Ajuste de umbrales por etiqueta; comparación de modelos A2; aumentar dataset si es necesario |
| LLM genera feedback incorrecto o engañoso | Baja | Alto | System prompt restrictivo; el LLM no puede contradecir la salida de A2 |
| Sesgo en las respuestas sintéticas del dataset | Media | Medio | Mezcla de respuestas sintéticas y reales; doble etiquetado para control de calidad |
| Privacidad de respuestas reales de usuarios | Baja | Alto | Consentimiento informado; datos anonimizados; cumplimiento Ley N.° 29733 (Perú) |

---

## SECCIÓN 7 — Autoevaluación del equipo

| Pregunta de control | Respuesta |
|---|---|
| ¿El flujo del MVP implementado está descrito (pregunta → respuesta → STAR → G1 → feedback)? | **SÍ** |
| ¿El componente analítico A2 (clasificador STAR) está documentado con inputs, outputs, algoritmo y resultado F1? | **SÍ — F1=0.808** |
| ¿El componente generativo G1 (Gemini) depende de la salida de A2 y tiene fallback documentado? | **SÍ** |
| ¿El patrón de conexión (Modelo → Lenguaje) está justificado? | **SÍ** |
| ¿Los OKRs tienen baseline, meta y resultado real (n=8)? | **SÍ — 3/3 KRs cumplidos** |
| ¿El alcance del MVP está delimitado con lo implementado y lo que quedó fuera? | **SÍ** |
| ¿Los riesgos críticos tienen mitigaciones concretas? | **SÍ** |
| ¿El stack refleja lo que se desplegó (Gemini, no GPT-4o-mini; sin FAISS/ChromaDB)? | **SÍ** |
| ¿El equipo puede explicar el producto completo sin leer este canvas? | **SÍ** |
