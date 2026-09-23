# InterviewIQ — Simulador Inteligente de Entrevistas por Competencias
## AD5018 Inteligencia Artificial para Negocios · UTEC 2026-2

**Equipo:** Valeria Briceño · Lucía Rodríguez · Aaron Van Oord

---

## ¿Qué es InterviewIQ?

InterviewIQ es un simulador conversacional de entrevistas por competencias diseñado para estudiantes universitarios peruanos de últimos ciclos que buscan prácticas preprofesionales o su primer empleo. Permite practicar entrevistas conductuales de manera recurrente y recibir retroalimentación estructurada sobre la calidad de las respuestas, sin depender de la disponibilidad de un entrevistador humano.

El sistema adapta la dificultad de las preguntas al nivel de preparación detectado de cada estudiante y evalúa si las respuestas incluyen los componentes de la metodología STAR (Situación, Tarea, Acción, Resultado).

---

## Problema que resuelve

Los estudiantes universitarios peruanos de últimos ciclos tienen dificultad para preparar y mejorar sus respuestas en entrevistas laborales por competencias porque cuentan con oportunidades limitadas de práctica recurrente con retroalimentación estructurada. Una encuesta propia a 50 estudiantes confirma la escala del problema: **60% se siente poco o nada preparado**, **80% reporta dificultad para estructurar respuestas conductuales** y **40% rara vez recibe retroalimentación estructurada** al practicar.

---

## Arquitectura del sistema

El sistema integra dos etapas de clasificación y un componente generativo RAG:

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
[Feedback estructurado mostrado al estudiante]
```

### Componentes

| Componente | Descripción | Tecnología |
|---|---|---|
| **Clasificador de nivel** | Logistic Regression sobre cuestionario diagnóstico (5 variables). Asigna nivel {básico / intermedio / avanzado} | scikit-learn |
| **Clasificador STAR (A2)** | Clasificación multilabel (S/T/A/R = 0 o 1) por etiqueta. Se comparan TF-IDF + LR (baseline) y TF-IDF + Linear SVM (alternativo) | scikit-learn |
| **Pipeline RAG (G2)** | Chunking del corpus → embeddings → índice vectorial → retrieval top-k → LLM genera feedback | OpenAI, FAISS/ChromaDB |
| **Interfaz** | Aplicación web conversacional: cuestionario → selección de rol → práctica → feedback | Streamlit |

---

## Datasets

El sistema requiere tres recursos de datos:

| Recurso | Descripción | Estado |
|---|---|---|
| **R1 — Cuestionario diagnóstico** | Respuestas de estudiantes al cuestionario de 5 ítems para entrenar el clasificador de nivel | 🟡 Pendiente de recolección (Semana 13) |
| **R2 — InterviewIQ-STAR** | ~200 pares (pregunta conductual · respuesta · etiquetas S/T/A/R = 0/1). Construido por el equipo con respuestas sintéticas y reales | 🟡 Pendiente de construcción (Semanas 7–8) |
| **R3 — Corpus RAG** | ~20–50 documentos sobre metodología STAR y competencias por rol. Fuentes: USC Career Center, UC Santa Cruz Career Success, Wilkie & Rosendale (2024), Marcus et al. (2023), ESCO | 🟡 Fuentes verificadas; corpus a cerrar (Semana 7) |

### Esquema de R2 — InterviewIQ-STAR

```
id, pregunta, respuesta, situacion, tarea, accion, resultado, fuente, anotador
```

- `situacion`, `tarea`, `accion`, `resultado` ∈ {0, 1}
- `fuente` ∈ {sintetica, real}
- Etiquetado con doble anotador + kappa de Cohen para control de calidad

---

## Métricas de evaluación

| Componente | Métrica | Criterio mínimo |
|---|---|---|
| Clasificador de nivel (Etapa 1) | Accuracy en test | ≥ 0.65 |
| Clasificador STAR A2 (Etapa 2) | Macro F1 en test | ≥ 0.65 |
| Pipeline RAG G2 | Retrieval precision@k | ≥ 0.80 |

---

## Impacto esperado (OKRs)

| KR | Baseline | Meta |
|---|---|---|
| Estudiantes poco/nada preparados para entrevistas | 60% | ≤ 40% tras uso del MVP |
| Estudiantes con dificultad para estructurar respuestas STAR | 80% | ≤ 55% tras sesiones de práctica |
| Estudiantes que rara vez reciben feedback estructurado | 40% | ≥ 90% reciben feedback en al menos 1 sesión |

Medición: cuestionario pre/post con ≥ 15 usuarios en Semana 13.

---

## Estructura del repositorio

```
InterviewIQ/
│
├── plantillas/
│   ├── plantilla_1_problem_statement.md
│   ├── plantilla_2_data_readiness.md
│   └── plantilla_3_ai_product_canvas.md
│
├── data/
│   ├── raw/
│   │   ├── interviewiq_star_v1.csv       # Dataset STAR (R2) — a construir
│   │   ├── corpus_rag/                   # Documentos del corpus RAG (R3)
│   │   └── schema.md                     # Esquema y protocolo del dataset
│   └── processed/                        # Datos limpios con split 70/10/20
│
├── notebooks/
│   ├── 01_clasificador_nivel.ipynb       # Logistic Regression sobre cuestionario
│   ├── 02_baseline_tfidf_lr.ipynb        # Baseline STAR: TF-IDF + LR
│   ├── 03_modelo_alternativo_svm.ipynb   # Alternativo STAR: TF-IDF + SVM
│   └── 04_rag_pipeline.ipynb             # Pipeline RAG completo
│
├── src/
│   └── app/                              # Interfaz Streamlit
│
├── docs/
│   ├── cuestionario_diagnostico_v1.md
│   ├── protocolo_etiquetado_star.md
│   ├── system_prompt_v2.md
│   └── consentimiento_informado.md
│
├── evaluation/
│   ├── clasificador_nivel.md
│   ├── comparacion_modelos_a2.md
│   ├── consultas_prueba_rag.md
│   └── metricas_g2.md
│
├── cronograma.md
├── resumen_ejecutivo.md
└── README.md
```

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Clasificadores | Python 3.10 · scikit-learn |
| Embeddings | OpenAI text-embedding-3-small |
| Índice vectorial | FAISS o ChromaDB (local) |
| LLM | GPT-4o-mini (API OpenAI) |
| Interfaz | Streamlit |
| Despliegue | Streamlit Community Cloud |

---

## Hoja de ruta

| Semana | Hito |
|---|---|
| 6 | PC1 — Entrega de plantillas + README + presentación |
| 7–8 | Construcción y etiquetado del dataset InterviewIQ-STAR |
| 9 | Entrenamiento del clasificador de nivel + baseline STAR A2 |
| 10 | Modelo alternativo A2 + inicio del pipeline RAG |
| 11 | Pipeline RAG G2 funcional |
| **12** | **MVP integrado y desplegado (URL pública)** |
| 13 | Evaluación con ≥ 15 usuarios reales |
| 14 | PC2 — Sustentación |

---

## Consideraciones éticas y legales

- Las respuestas reales de usuarios se recolectan con consentimiento informado y se anonimiza la información personal antes de almacenarla, en cumplimiento de la **Ley N.° 29733** (Ley de Protección de Datos Personales, Perú).
- Las respuestas sintéticas generadas con LLM para el dataset son revisadas manualmente antes de ser etiquetadas.
- El system prompt del componente G2 prohíbe explícitamente: inventar experiencias del usuario, afirmar probabilidades de contratación, y contradecir la salida del modelo A2.
- Las fuentes del corpus RAG están verificadas y se documentan sus licencias de uso.

---
