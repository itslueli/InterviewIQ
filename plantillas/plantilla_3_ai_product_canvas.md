# Plantilla 3 — AI Product Canvas
## Fase O — Diseño del Producto de IA
### AD5018 Inteligencia Artificial para Negocios | UTEC

---

**Equipo:**
- Integrante 1: Valeria Briceño
- Integrante 2: Lucía Rodríguez
- Integrante 3: Aaron Van Oord

**Proyecto:** InterviewIQ — Simulador Inteligente de Entrevistas para Universitarios

---

## SECCIÓN 1 — Descripción del producto

### 1.1 Nombre del producto
**InterviewIQ** — Simulador conversacional de entrevistas por competencias con retroalimentación estructurada.

### 1.2 Usuario objetivo
Estudiantes universitarios peruanos de últimos ciclos que buscan prácticas preprofesionales o su primer empleo y necesitan prepararse para entrevistas laborales por competencias, sin acceso a coaching profesional.

### 1.3 Propuesta de valor
InterviewIQ permite que cualquier estudiante pueda practicar entrevistas conductuales de manera recurrente y recibir retroalimentación estructurada sobre la calidad de sus respuestas STAR, adaptada a su nivel de preparación y al rol que busca.

### 1.4 Descripción funcional del producto

El sistema ofrece un flujo de práctica completo en cuatro etapas:

1. **Diagnóstico inicial:** El estudiante completa un cuestionario breve (5 ítems) sobre su experiencia con entrevistas, conocimiento de la metodología STAR, nivel de confianza y frecuencia de feedback previo. Un clasificador de nivel de preparación (Logistic Regression) asigna al usuario un nivel: `básico`, `intermedio` o `avanzado`.

2. **Generación de preguntas adaptadas:** El LLM genera preguntas conductuales ajustadas al rol objetivo del estudiante y a su nivel de preparación detectado en la etapa anterior.

3. **Respuesta y análisis STAR:** El estudiante responde en texto libre. El clasificador STAR (componente A2) detecta la presencia o ausencia de cada componente (Situación, Tarea, Acción, Resultado) en la respuesta.

4. **Retroalimentación personalizada:** El pipeline RAG recupera contexto relevante del corpus y el LLM genera feedback específico usando la salida del clasificador A2 y el contexto recuperado.

**Flujo completo del sistema:**

```
[Selección de rol objetivo]
        ↓
[Cuestionario diagnóstico — 5 ítems]
        ↓
[Clasificador de nivel — Logistic Regression]
Output: nivel ∈ {básico, intermedio, avanzado}
        ↓
[Generación de preguntas conductuales adaptadas al rol y nivel — LLM]
        ↓
[Respuesta del usuario en texto libre]
        ↓
[Clasificador STAR — A2 (TF-IDF + LR baseline vs TF-IDF + SVM)]
Output: S ∈ {0,1}, T ∈ {0,1}, A ∈ {0,1}, R ∈ {0,1}
        ↓
[RAG — recuperación de contexto del corpus (FAISS/ChromaDB)]
        ↓
[LLM — genera feedback personalizado con salida A2 + contexto recuperado]
        ↓
[Feedback mostrado al estudiante]
```

---

## SECCIÓN 2 — Model Design Canvas

### 2.1 Componente analítico — Etapa 1: Clasificador de nivel de preparación

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
| **¿Se usará para entrenar G2?** | No directamente — el nivel detectado se pasa como parámetro al prompt de generación de preguntas |

### 2.2 Componente analítico — Etapa 2: Clasificador STAR (A2 principal)

| Elemento | Detalle |
|---|---|
| **Tarea** | Clasificación multilabel (4 etiquetas independientes: S, T, A, R) |
| **Input** | Respuesta del usuario en texto libre (variable `answer`) |
| **Output** | Vector binario (S, T, A, R) ∈ {0,1}⁴ |
| **Algoritmo baseline** | TF-IDF + Logistic Regression (OneVsRest) |
| **Algoritmo alternativo** | TF-IDF + Linear SVM (OneVsRest) |
| **Dataset de entrenamiento** | Recurso 2 — InterviewIQ-STAR (~200 pares etiquetados) |
| **Split** | 70% entrenamiento / 10% validación / 20% test |
| **Métrica principal** | Macro F1 (promedia las 4 etiquetas con igual peso) |
| **Criterio mínimo de aceptación** | Macro F1 ≥ 0.65 sobre el conjunto de test |
| **Costo del error** | **Falso positivo más costoso:** indicar que un componente STAR está presente cuando no lo está significa decirle al estudiante que su respuesta es buena cuando no lo es. El umbral se ajustará por etiqueta en validación priorizando reducir falsos positivos. |
| **¿Se usará para entrenar G2?** | Sí — las predicciones (S, T, A, R) se pasan directamente al prompt de G2 |

### 2.3 Componente generativo — G2 (RAG)

| Elemento | Detalle |
|---|---|
| **Tipo de tarea** | Generación de texto (preguntas conductuales y feedback personalizado) |
| **Input de la generación de preguntas** | Nivel detectado (Etapa 1) + rol objetivo del estudiante |
| **Input del feedback** | Respuesta original del usuario + predicciones S/T/A/R (Etapa 2) + contexto recuperado del corpus |
| **Modelo LLM** | GPT-4o-mini (API OpenAI) |
| **Corpus RAG** | ~20–50 documentos sobre metodología STAR y competencias por rol (Recurso 3) |
| **Chunking** | 300–500 tokens por chunk, sin cortar oraciones |
| **Embeddings** | text-embedding-3-small (OpenAI) |
| **Índice vectorial** | FAISS o ChromaDB (local) |
| **Retrieval** | Top-k (k=3–5) por similitud coseno |
| **Métrica RAG** | Retrieval precision@k sobre conjunto de consultas de prueba |
| **Criterio mínimo de aceptación RAG** | Precision@k ≥ 0.80 |
| **Restricciones del system prompt** | El LLM no puede: (1) inventar experiencias del usuario, (2) afirmar probabilidades de contratación, (3) contradecir la salida del modelo A2, (4) recomendar componentes STAR como presentes si A2 los marcó como ausentes |
| **¿Depende del componente analítico?** | Sí (Patrón 1: Modelo → Lenguaje) — G2 siempre recibe las predicciones de A2 antes de generar feedback |

### 2.4 Patrón de conexión entre componentes

- [x] **Patrón 1 — Modelo → Lenguaje:** La salida del clasificador de nivel alimenta la generación de preguntas; la salida del clasificador STAR alimenta la generación de feedback. G2 no opera de manera independiente.
- [ ] **Patrón 2 — Lenguaje → Modelo**
- [ ] **Patrón 3 — Modelo como herramienta del agente**

---

## SECCIÓN 3 — Inputs y outputs del sistema

### 3.1 Inputs del sistema

| Input | Descripción | Formato | Momento en el flujo |
|---|---|---|---|
| Rol objetivo | Puesto al que aplica el estudiante | Texto libre o selección de lista | Antes del cuestionario |
| Cuestionario diagnóstico | 5 ítems sobre experiencia, confianza, conocimiento STAR y feedback previo | Variables ordinales/numéricas | Inicio de la sesión |
| Respuesta conductual | Respuesta del estudiante a la pregunta generada | Texto libre | Sesión de práctica |

### 3.2 Outputs del sistema

| Output | Descripción | Generado por |
|---|---|---|
| Nivel de preparación | `básico` / `intermedio` / `avanzado` | Clasificador de nivel (Etapa 1) |
| Preguntas conductuales adaptadas | Preguntas ajustadas al rol y nivel | LLM (G2) |
| Predicciones STAR | S/T/A/R ∈ {0,1} por componente | Clasificador STAR (Etapa 2) |
| Feedback personalizado | Análisis con fortalezas, componentes ausentes y recomendaciones de mejora | LLM con RAG (G2) |

---

## SECCIÓN 4 — OKRs y métricas de impacto

### Objetivo general
Incrementar la preparación percibida y la capacidad de estructurar respuestas conductuales de los estudiantes universitarios peruanos que buscan prácticas o primer empleo.

### Key Results

| KR | Indicador | Baseline (encuesta propia, n=50) | Meta con MVP | Medición |
|---|---|---|---|---|
| **KR1** | % de estudiantes que se sienten poco o nada preparados para entrevistas por competencias | **60%** | ≤ 40% tras uso del MVP | Cuestionario pre/post (n ≥ 15 usuarios) |
| **KR2** | % de estudiantes con dificultad para estructurar respuestas conductuales (STAR) | **80%** | ≤ 55% tras sesiones de práctica | Cuestionario pre/post (n ≥ 15 usuarios) |
| **KR3** | % de estudiantes que rara vez o nunca reciben retroalimentación estructurada | **40%** | ≥ 90% reciben feedback en al menos 1 sesión | Registro de uso del MVP |

### Métricas técnicas

| Componente | Métrica | Criterio mínimo |
|---|---|---|
| Clasificador de nivel (Etapa 1) | Accuracy en test | ≥ 0.65 |
| Clasificador STAR A2 (Etapa 2) | Macro F1 en test | ≥ 0.65 |
| Pipeline RAG G2 | Retrieval precision@k | ≥ 0.80 |

---

## SECCIÓN 5 — Arquitectura del MVP

### 5.1 Stack tecnológico

| Capa | Tecnología |
|---|---|
| Interfaz | Streamlit |
| Clasificador de nivel | scikit-learn (Logistic Regression) |
| Clasificador STAR | scikit-learn (TF-IDF + LR y TF-IDF + LinearSVC) |
| Embeddings | OpenAI text-embedding-3-small |
| Índice vectorial | FAISS o ChromaDB (local) |
| LLM | GPT-4o-mini (API OpenAI) |
| Despliegue | Streamlit Community Cloud (URL pública) |

### 5.2 Alcance del MVP

**Incluido:**
- Cuestionario diagnóstico (5 ítems) + clasificación de nivel
- Selección de rol objetivo (lista predefinida)
- Generación de preguntas conductuales adaptadas al rol y nivel
- Análisis STAR de la respuesta
- Feedback personalizado (RAG + LLM)
- Interfaz web accesible desde cualquier dispositivo

**Excluido del MVP:**
- Autenticación de usuarios
- Base de datos persistente de sesiones
- Audio o video
- Análisis de CV o carta de presentación
- Soporte multilingüe

### 5.3 Diagrama de componentes

```
┌────────────────────────────────────────────────────────┐
│                   Interfaz Streamlit                   │
│  [Cuestionario] → [Selección rol] → [Práctica] → [FB] │
└────────────┬───────────────────────────────┬───────────┘
             │                               │
    ┌────────▼────────┐             ┌────────▼────────┐
    │ Clasificador    │             │ Clasificador    │
    │ de Nivel        │             │ STAR (A2)       │
    │ (Logistic Reg.) │             │ TF-IDF + LR/SVM │
    │ Output: nivel   │             │ Output: S,T,A,R │
    └────────┬────────┘             └────────┬────────┘
             │                               │
    ┌────────▼────────────────────────────────▼────────┐
    │              Pipeline RAG + LLM (G2)             │
    │  Corpus → Chunks → Embeddings → FAISS → top-k   │
    │  LLM (GPT-4o-mini) → preguntas y feedback       │
    └──────────────────────────────────────────────────┘
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
| ¿El flujo completo del sistema (cuestionario → nivel → preguntas → respuesta → STAR → RAG → feedback) está descrito? | **SÍ** |
| ¿Los dos componentes analíticos (clasificador de nivel + clasificador STAR) están diferenciados con inputs, outputs y métricas propias? | **SÍ** |
| ¿El componente generativo G2 usa RAG y depende de la salida de A2? | **SÍ** |
| ¿El patrón de conexión (Modelo → Lenguaje) está justificado? | **SÍ** |
| ¿Las métricas técnicas y los OKRs de impacto están definidos con criterios mínimos de aceptación? | **SÍ** |
| ¿El alcance del MVP está delimitado con lo que incluye y lo que excluye? | **SÍ** |
| ¿Los riesgos críticos tienen mitigaciones concretas? | **SÍ** |
| ¿El baseline del KR3 (40%) es el valor real de la encuesta? | **SÍ — 40%, no 10%** |
| ¿El equipo puede explicar el producto completo sin leer este canvas? | **SÍ** |
