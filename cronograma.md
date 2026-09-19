# Cronograma del Proyecto — InterviewIQ
## Inteligencia Artificial para Negocios | UTEC 2026-2

**Equipo:** Valeria Briceño · Lucía Rodríguez · Aaron Van Oord
**Fecha de actualización:** 2026-09-19

---

## Resumen de hitos

| Hito | Fecha | Estado |
|---|---|---|
| PC1 — Entrega plantillas + README + presentación | Semana 6 (fin de septiembre 2026) | 🔄 En curso |
| Primera versión del dataset `InterviewIQ-STAR` | Semana 7 | ⏳ Pendiente |
| Protocolo STAR + acuerdo entre anotadores | Semana 8 | ⏳ Pendiente |
| Baseline A2 entrenado y evaluado | Semana 9 | ⏳ Pendiente |
| Pipeline RAG G2 funcional | Semana 10–11 | ⏳ Pendiente |
| MVP integrado y desplegado (URL pública) | **Semana 12** | ⏳ Pendiente |
| Evaluación con usuarios reales | Semana 13 | ⏳ Pendiente |
| PC2 — Sustentación | Semana 14 | ⏳ Pendiente |

---

## PC1 — Fases P + R + O (Semanas 1–6)

| Semana | Tarea | Responsable | Entregable | Estado |
|---|---|---|---|---|
| 1–2 | Definición del problema · investigación de evidencia · encuesta a 50 estudiantes | Equipo | Datos de la encuesta · evidencia verificada | ✅ |
| 2–3 | Plantilla 1 — Problem Statement Canvas | Equipo | `plantilla_1_problem_statement.md` | ✅ |
| 3–4 | Inventario de fuentes RAG · verificar disponibilidad y licencias | Valeria | Lista de fuentes con URL y condiciones de uso | ✅ |
| 3–4 | Diseño del dataset A2 · esquema CSV · protocolo STAR preliminar | Aaron + Lucía | Esquema del dataset definido | ✅ |
| 4 | Plantilla 2 — Data Readiness Checklist | Equipo | `plantilla_2_data_readiness.md` | ✅ |
| 4–5 | Plantilla 3 — AI Product Canvas · System Prompt · Model Design Canvas · OKRs | Equipo | `plantilla_3_ai_product_canvas.md` | ✅ |
| 5 | README.md · cronograma.md | Equipo | `README.md` · `cronograma.md` | ✅ |
| 5–6 | Resumen ejecutivo | Equipo | `resumen_ejecutivo.md` | 🔄 |
| 6 | Presentación PC1 | Equipo | `presentacion_pc1.pdf` | ⏳ |
| **Semana 6** | **Entrega y sustentación PC1** | **Equipo** | **Carpeta completa del repositorio** | ⏳ |

---

## PC2 — Fases M + P2 + T (Semanas 7–14)

### Semana 7 — Construcción del dataset (inicio)

| Tarea | Responsable | Entregable |
|---|---|---|
| Definir tamaño final y esquema CSV del dataset `InterviewIQ-STAR` | Aaron | `data/raw/schema.md` |
| Crear reglas claras y ejemplos para etiquetar S/T/A/R = 1 o 0 | Lucía | `docs/protocolo_etiquetado_star.md` |
| Seleccionar y guardar fuentes finales del corpus RAG; registrar URL y condiciones de uso | Valeria | `data/raw/corpus_rag/` + `README_data.md` |
| Generar primeras respuestas sintéticas con LLM para el dataset | Aaron | Primeros ~50 pares en CSV |

### Semana 8 — Etiquetado, balance y calidad

| Tarea | Responsable | Entregable |
|---|---|---|
| Doble etiquetado de una muestra (~30 pares) y medición de kappa de Cohen | Lucía + equipo | Reporte de acuerdo entre anotadores |
| Resolver desacuerdos y actualizar protocolo STAR | Lucía | Protocolo STAR v2 |
| Completar ~200 pares etiquetados (respuestas completas, parciales y deficientes) | Aaron + Lucía | `data/raw/interviewiq_star_v1.csv` |
| Contar positivos/negativos por etiqueta (S, T, A, R) y verificar balance | Aaron | Reporte de balance |
| Preparar consentimiento informado si se recolectan respuestas reales | Lucía | `docs/consentimiento_informado.md` |

### Semana 9 — Entrenamiento baseline A2

| Tarea | Responsable | Entregable |
|---|---|---|
| Limpieza y procesamiento del dataset · split 70/10/20 · verificar ausencia de leakage | Aaron | `data/processed/` |
| Entrenar baseline: TF-IDF + Logistic Regression · registrar Macro F1 | Aaron | `notebooks/02_baseline_tfidf_lr.ipynb` |
| Documentar resultados del baseline | Aaron | `evaluation/comparacion_modelos_a2.md` (v1) |
| Exploración inicial: TF-IDF + Linear SVM (modelo alternativo) | Aaron | Primeros resultados en notebook |

### Semana 10 — Modelo alternativo A2 + inicio pipeline RAG

| Tarea | Responsable | Entregable |
|---|---|---|
| Entrenar y comparar modelo alternativo (SVM o BETO) con el baseline · ajustar umbral por etiqueta | Aaron | `notebooks/03_modelo_alternativo.ipynb` |
| Seleccionar modelo final A2 y documentar decisión con justificación del umbral | Aaron | `evaluation/comparacion_modelos_a2.md` (v2) |
| Iniciar pipeline RAG: chunking del corpus (300–500 tokens) + generación de embeddings | Valeria | `notebooks/04_rag_pipeline.ipynb` (v1) |
| Crear consultas de prueba para evaluar retrieval top-k | Valeria + Aaron | `evaluation/consultas_prueba_rag.md` |

### Semana 11 — Pipeline RAG G2 funcional

| Tarea | Responsable | Entregable |
|---|---|---|
| Construir índice vectorial (FAISS o ChromaDB) con el corpus final | Valeria | Índice vectorial local |
| Conectar retrieval + LLM + system prompt · prueba end-to-end del flujo A2→G2 | Valeria + Aaron | `notebooks/04_rag_pipeline.ipynb` (v2) |
| Evaluar retrieval: precision@k sobre consultas de prueba | Valeria | Métrica en `evaluation/metricas_g2.md` |
| Revisar y ajustar system prompt según pruebas iniciales | Lucía | `docs/system_prompt_v2.md` |

### Semana 12 — Integración MVP y despliegue

| Tarea | Responsable | Entregable |
|---|---|---|
| Desarrollar interfaz Streamlit: selección de rol + sesión de práctica + panel de feedback | Lucía | `src/app/` |
| Integrar A2 + G2 + interfaz en flujo completo funcional | Equipo | MVP local funcionando |
| Desplegar en Streamlit Community Cloud · obtener URL pública | Aaron | **URL pública del MVP** |
| Prueba interna del MVP completo (equipo) | Equipo | Lista de bugs / ajustes |

### Semana 13 — Evaluación con usuarios y análisis de riesgos

| Tarea | Responsable | Entregable |
|---|---|---|
| Aplicar cuestionario pre-uso a ≥ 15 usuarios | Lucía | Datos baseline por usuario |
| Sesión de práctica con el MVP (≥ 15 usuarios externos al equipo) | Equipo | Sesiones registradas |
| Aplicar cuestionario post-uso · medir KR1, KR2 y KR3 | Lucía | Datos post-uso |
| Análisis de métricas técnicas finales A2 (Macro F1 sobre test) y G2 (retrieval) | Aaron | `evaluation/` actualizado |
| Análisis de riesgos del proyecto (Fase T del framework PROMPT) | Equipo | Sección de riesgos en PC2 |

### Semana 14 — Sustentación PC2

| Tarea | Responsable | Entregable |
|---|---|---|
| Preparar presentación PC2 con resultados reales de métricas y validación | Equipo | `presentacion_pc2.pdf` |
| **Sustentación PC2** | **Equipo** | **MVP + métricas + análisis de riesgos** |

---

## Roles por integrante (PC2)

| Integrante | Rol principal |
|---|---|
| **Aaron Van Oord** | Dataset · entrenamiento A2 · pipeline técnico · despliegue |
| **Lucía Rodríguez** | Protocolo de etiquetado · system prompt · interfaz · evaluación con usuarios |
| **Valeria Briceño** | Corpus RAG · embeddings · retrieval · fuentes y licencias |
| **Todos** | Integración final · presentaciones · sustentaciones |

---

## Dependencias críticas

```
Dataset A2 construido y etiquetado (S8)
   └──► Entrenamiento baseline A2 (S9)
           └──► Modelo alternativo y selección final (S10)
                   └──► Integración con G2 (S11–S12)
                           └──► Evaluación con usuarios (S13)

Corpus RAG seleccionado (S7)
   └──► Chunking + embeddings (S10)
           └──► Índice vectorial + retrieval funcional (S11)
                   └──► Integración con A2 (S12)
```

---

*Framework PROMPT v2.0 — AD5018 UTEC | Se actualiza al cierre de cada semana.*
