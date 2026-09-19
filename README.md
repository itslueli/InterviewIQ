# 🎯 InterviewIQ — Simulador Inteligente de Entrevistas para Universitarios

> **Curso:** AD5018 – Inteligencia Artificial para Negocios · UTEC · 2026-2
**Fase actual:** PC1 (Semanas 1–6)

---

## 1. Problema

Los estudiantes universitarios peruanos de últimos ciclos que buscan prácticas preprofesionales o su primer empleo tienen dificultad para preparar y mejorar sus respuestas en entrevistas laborales por competencias porque cuentan con oportunidades limitadas de práctica recurrente con retroalimentación estructurada, lo que genera bajos niveles de preparación percibida y dificultades para estructurar respuestas conductuales.

**Evidencia verificada — contexto nacional:**
- 14.3% de desempleo juvenil en Perú (INEI, 2024)
- 7 de cada 10 jóvenes peruanos experimenta inadecuación ocupacional (MTPE, 2024)
- Brecha de competencias del 40% entre egresados y requisitos empresariales (BID, 2019)
- 60.8% de empresas peruanas no encuentra trabajadores con las habilidades requeridas (INEI ENE, 2020)
- La práctica con mock interviews reduce ansiedad y aumenta preparación (Wilkie & Rosendale, 2024)

**Evidencia directa — muestra objetivo (50 estudiantes universitarios de últimos ciclos):**
- ~60% se siente poco o nada preparado para entrevistas por competencias
- ~40% rara vez o nunca recibe retroalimentación estructurada al practicar
- ~80% reporta dificultad para estructurar ejemplos concretos al responder preguntas conductuales

---

## 2. Usuario Objetivo

**Primario:** Estudiantes universitarios peruanos de últimos ciclos (18–28 años) que buscan prácticas preprofesionales o su primer empleo y necesitan prepararse para entrevistas laborales por competencias.

**Secundario:** Egresados recientes con hasta 2 años de experiencia que buscan cambiar de sector.

---

## 3. Propuesta

**InterviewIQ** es un simulador conversacional de entrevistas por competencias que:

1. Genera preguntas conductuales contextualizadas según sector/rol objetivo
2. Recibe las respuestas del usuario en texto libre
3. Detecta la presencia o ausencia de los componentes STAR (Situación, Tarea, Acción, Resultado) en cada respuesta — **Componente Analítico A2**
4. Genera retroalimentación personalizada fundamentada en fuentes seleccionadas sobre entrevistas y metodología STAR, usando el resultado del clasificador — **Componente Generativo G2 (RAG)**
5. Acumula historial de sesiones para mostrar progreso por competencia

---

## 4. Arquitectura de IA

```
Usuario
   │
   ▼
[Generador de preguntas — LLM con prompts por rol/sector]
   │
   ▼
[Respuesta del usuario — texto libre]
   │
   ├──► [A2: Clasificador STAR — ML entrenado por el equipo]
   │         └── Output: presencia/ausencia de S, T, A, R por componente
   │
   └──► [G2: RAG + LLM — Retroalimentación]
             ├── Base de conocimiento: guías STAR, ejemplos por sector
             ├── Pipeline: chunking → embeddings → retrieval → contexto → LLM
             └── Output: feedback específico + sugerencia de mejora
```

**Patrón de conexión — Modelo → Lenguaje (Patrón 1):**
El clasificador A2 detecta los componentes STAR presentes/ausentes y envía ese resultado junto con la respuesta original a la capa generativa G2. El RAG combina esa información con conocimiento recuperado para producir retroalimentación específica.

---

## 5. Componente Analítico (A2)

**Tarea:** Identificar la presencia o ausencia de los componentes STAR (Situación, Tarea, Acción, Resultado) en las respuestas textuales del usuario a preguntas conductuales.

**Tipo de tarea:** Clasificación

**Nivel:** A2 — se entrenará un baseline y al menos un modelo alternativo. Se compararán con métricas adecuadas y se justificará el umbral considerando el costo de falsos positivos y falsos negativos.

**Modelos a comparar:**

| Modelo | Tipo | Rol |
|---|---|---|
| TF-IDF + Logistic Regression | Baseline clásico | Modelo de referencia |
| TF-IDF + Linear SVM | Clasificador lineal | Modelo alternativo |

**Dataset — propio construido por el equipo:**

| Campo | Detalle |
|---|---|
| Tipo | Dataset supervisado propio |
| Tamaño | ~200 pares (pregunta conductual, respuesta candidato, label STAR) |
| Generación | Respuestas sintéticas con LLM + etiquetado manual; o recolección de compañeros |
| Etiquetado | 3 miembros del equipo; consistencia medida con kappa de Cohen |
| Idioma | Español |
| Dominio | ✅ Correcto — directamente entrevistas por competencias |
| Split | 70% train / 10% val / 20% test |
| Privacidad | Consentimiento informado si se usan respuestas reales (Ley N.° 29733, Perú) |

**Métricas objetivo A2:**
- F1 macro ≥ 0.65 sobre conjunto de validación
- Accuracy ≥ 0.70
- Justificación del umbral según costo del error (FP vs FN)

---

## 6. Componente Generativo (G2 — RAG)

**Tarea:** Generar preguntas conductuales contextualizadas al puesto objetivo y retroalimentación personalizada sobre cada respuesta, usando el resultado del clasificador A2 y conocimiento recuperado de fuentes seleccionadas.

**Pipeline RAG:**

```
Documentos fuente (guías STAR, ejemplos por sector, tips de entrevista)
   └── Chunking (~300–500 tokens)
         └── Embeddings (sentence-transformers o text-embedding-ada-002)
               └── Índice vectorial (FAISS o ChromaDB)
                     └── Retrieval (top-k chunks relevantes)
                           └── Contexto → LLM (GPT-4o-mini)
                                 └── Retroalimentación personalizada
```

**Base de conocimiento a indexar:**
- Guías de entrevistas por competencias (STAR)
- Ejemplos de respuestas por sector (tecnología, finanzas, consultoría)
- Errores comunes en entrevistas conductuales
- TBD: material adicional según sector/rol

**LLM propuesto:** GPT-4o-mini (API OpenAI) — PENDIENTE DE VALIDAR costo / alternativa open source

**Métricas objetivo G2:**
- Retrieval precision@3 ≥ 0.70
- Faithfulness (feedback anclado en fuentes recuperadas) ≥ 0.80

---

## 7. Datos

### A2 — Clasificador STAR
| Campo | Detalle |
|---|---|
| Fuente | Dataset propio (equipo) |
| Tamaño | ~200 pares etiquetados |
| Generación | LLM sintético + etiquetado manual, o recolección de compañeros |
| Split | 70 / 10 / 20 (train / val / test) |
| Idioma | Español |

### G2 — Base RAG
| Campo | Detalle |
|---|---|
| Tipo | Documentos curados (no requiere etiquetado) |
| Fuentes candidatas | Guías RRHH, artículos de coaching, ejemplos STAR públicos |
| Tamaño estimado | ~20–50 documentos (~50K–200K tokens) |
| Idioma | Español |

---

## 8. Arquitectura del Sistema

```
┌─────────────────────────────────────────────────┐
│                  FRONTEND                        │
│  Interfaz conversacional (Streamlit)             │
│  - Panel de sesión de entrevista                 │
│  - Historial de respuestas + feedback            │
│  - Dashboard de progreso por competencia         │
└───────────────┬─────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────┐
│                  BACKEND                         │
│  ┌──────────────┐    ┌──────────────────────┐   │
│  │ A2 Classifier│───►│   G2 RAG Pipeline    │   │
│  │ (STAR detect)│    │ (embeddings + LLM)   │   │
│  └──────────────┘    └──────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │      Question Generator (LLM prompt)     │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 9. Métricas

### Métricas técnicas
| Componente | Métrica | Objetivo |
|---|---|---|
| A2 Clasificador | F1 macro (detección STAR) | ≥ 0.65 |
| A2 Clasificador | Accuracy | ≥ 0.70 |
| G2 RAG | Retrieval precision@3 | ≥ 0.70 |
| G2 RAG | Faithfulness vs. fuentes | ≥ 0.80 |
| Sistema | Latencia de respuesta | < 5 seg |

### OKRs — PENDIENTE DE FORMALIZAR
> ⚠️ Los Key Results definidos en PC1 no pueden modificarse para PC2. Pendiente validación con el equipo.

| Objetivo | Key Result candidato |
|---|---|
| Mejorar preparación del usuario | ≥ 70% de usuarios mejoran detección STAR entre sesión 1 y sesión 3 |
| Validar utilidad percibida | NPS ≥ 40 en prueba con ≥ 15 usuarios |
| Demostrar funcionamiento técnico | A2 F1 macro ≥ 0.65 en conjunto de test |

---

## 10. Alcance MVP

**Incluye (PC2 — Semanas 7–13):**
- [ ] Generación de preguntas por rol/sector (LLM con prompt engineering)
- [ ] Clasificador A2 entrenado y evaluado (baseline + modelo alternativo comparados)
- [ ] Pipeline RAG funcional con ≥ 20 documentos indexados
- [ ] Retroalimentación generada por G2 para cada respuesta
- [ ] Interfaz conversacional (Streamlit)
- [ ] Historial de sesión (en memoria / archivo local)
- [ ] Evaluación con ≥ 15 usuarios reales

**Excluye del MVP:**
- Autenticación / cuentas de usuario
- Base de datos persistente
- Evaluación de audio o video
- Integración con plataformas de empleo externas
- App móvil

---

## 11. Stack

| Capa | Tecnología | Estado |
|---|---|---|
| Lenguaje | Python 3.11+ | Confirmado |
| ML baseline | scikit-learn — TF-IDF + Logistic Regression | Confirmado |
| ML alternativo | scikit-learn — TF-IDF + Linear SVM | Confirmado |
| Vector DB | FAISS / ChromaDB | PENDIENTE DE VALIDAR |
| LLM API | OpenAI GPT-4o-mini | PENDIENTE DE VALIDAR |
| Frontend MVP | Streamlit | PENDIENTE DE VALIDAR |
| Control de versiones | GitHub | Confirmado |
| Dependencias | pip + requirements.txt | Confirmado |
| Entorno entrenamiento | Google Colab / Jupyter | Confirmado |

---

## 12. Estructura del Repositorio

```
proyecto-entrevistas-ia/
│
├── README.md
├── resumen_ejecutivo.md
├── presentacion_pc1.pdf
├── cronograma.md
│
├── plantillas/
│   ├── plantilla_1_problem_statement.md   ✅ Completada
│   ├── plantilla_2_data_readiness.md      ⏳ Pendiente
│   └── plantilla_3_ai_product_canvas.md   ⏳ Pendiente
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README_data.md
│
├── notebooks/
├── 01_exploracion_datos.ipynb
├── 02_baseline_tfidf_lr.ipynb
├── 03_modelo_alternativo_svm.ipynb
└── 04_rag_pipeline.ipynb
│
├── src/
│   ├── classifier/
│   ├── rag/
│   └── app/
│
├── models/
│   ├── baseline_tfidf_lr.pkl
│   └── svm_star.pkl
│
├── evaluation/
│   ├── comparacion_modelos_a2.md
│   └── metricas_g2.md
│
└── docs/
    └── system_prompt_v1.md
```

---

## 13. Cronograma

| Semana | Fase | Entregable |
|---|---|---|
| 1–2 | Problem Statement + investigación | Evidencia verificada, Plantilla 1 |
| 3–4 | Diseño A2 + G2 | Plantillas 2–3, arquitectura, system prompt |
| 5–6 | Cierre PC1 | OKRs, cronograma, README, resumen ejecutivo, presentación |
| **PC1 → Semana 6** | **Evaluación** | **Plantillas 1–3 + README + presentación** |
| 7–9 | Construcción dataset | ~200 pares etiquetados (kappa de Cohen) |
| 9–10 | Entrenamiento A2 | Baseline + modelo alternativo, F1 registrado |
| 11 | Pipeline G2 | RAG funcional, ≥ 20 docs indexados |
| 12 | Integración MVP | A2 + G2 + interfaz Streamlit |
| 13 | Evaluación con usuarios | ≥ 15 usuarios, métricas, riesgos |
| **PC2 → Semana 14** | **Evaluación** | **MVP + métricas + análisis de riesgos** |

---

## 14. Integrantes

| Nombre | Email |
|---|---|---|
| Valeria Briceño | valeria.briceno@utec.edu.pe |
| Lucía Rodríguez | lucia.rodriguez@utec.edu.pe |
| Aaron Van Oord | aaron.vanoordt@utec.edu.pe |

---

## 15. Estado Actual

**Actualizado:** 2026-09-19

| Ítem | Estado |
|---|---|
| Plantilla 1 — Problem Statement | ✅ Completada |
| Plantilla 2 — Data Readiness | ⏳ Pendiente |
| Plantilla 3 — AI Product Canvas | ⏳ Pendiente |
| Dataset A2 — decisión | ⏳ Pendiente |
| Arquitectura A2 | ✅ Definida — baseline TF-IDF + Linear SVM |
| Arquitectura G2 — RAG | ✅ Hipótesis definida |
| OKRs formales | ⏳ Pendiente |
| Cronograma detallado | ⏳ Pendiente |
| Resumen ejecutivo | ⏳ Pendiente |
| Presentación PC1 | ⏳ Pendiente |
| Código / notebooks | ⏳ Pendiente (inicia PC2) |

---

## 16. Fuentes Principales

> **REGLA FUNDAMENTAL:** Solo se citan fuentes verificadas. No se inventan estadísticas ni papers.

### Evidencia del problema
- INEI (2024). *Situación del mercado laboral en Lima Metropolitana.* Instituto Nacional de Estadística e Informática del Perú.
- MTPE (2024). *Boletín de estadísticas ocupacionales.* Ministerio de Trabajo y Promoción del Empleo del Perú.
- BID (2019). *El futuro ya está aquí: habilidades transversales en América Latina y el Caribe.* Banco Interamericano de Desarrollo.
- INEI (2020). *Encuesta Nacional de Empresas (ENE) 2020.* Instituto Nacional de Estadística e Informática del Perú.

### Evidencia de intervención
- Wilkie, L. & Rosendale, J.A. (2024). *Mock interview effectiveness on student anxiety and preparedness.* *(URL a verificar antes de PC1)*

### Marco metodológico
- Guía del Proyecto AD5018 – PROMPT v2.0. UTEC, 2026.
- Sílabo AD5018 – Inteligencia Artificial para Negocios. UTEC, 2026-2.

### Marco legal
- Ley N.° 29733 – Ley de Protección de Datos Personales. Perú, 2011.

---

*Última actualización: 2026-09-19 · Semana 2 / FASE 0–1 · Se actualiza al cierre de cada fase.*
