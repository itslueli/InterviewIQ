# Cronograma del Proyecto — InterviewIQ
## AD5018 Inteligencia Artificial para Negocios | UTEC 2026-2

**Equipo:** Valeria Briceño · Lucía Rodríguez · Aaron Van Oord

---

## Resumen de hitos

| Hito | Fecha | Estado |
|---|---|---|
| PC1 — Entrega plantillas + README + presentación | Semana 6 (fin de septiembre 2026) | 🔄 En curso |
| Cuestionario diagnóstico diseñado y aplicado (piloto) | Semana 7 | ⏳ Pendiente |
| Primera versión del dataset `InterviewIQ-STAR` | Semana 7 | ⏳ Pendiente |
| Protocolo STAR + acuerdo entre anotadores | Semana 8 | ⏳ Pendiente |
| Clasificador de nivel entrenado (Logistic Regression) | Semana 9 | ⏳ Pendiente |
| Baseline A2 (clasificador STAR) entrenado y evaluado | Semana 9 | ⏳ Pendiente |
| Pipeline RAG G2 funcional | Semana 10–11 | ⏳ Pendiente |
| MVP integrado y desplegado (URL pública) | **Semana 12** | ⏳ Pendiente |
| Evaluación con usuarios reales (cuestionario pre/post) | Semana 13 | ⏳ Pendiente |
| PC2 — Sustentación | Semana 14 | ⏳ Pendiente |

---

## PC1 — Fases P + R + O (Semanas 1–6)

| Semana | Tarea | Responsable | Entregable | Estado |
|---|---|---|---|---|
| 1–2 | Definición del problema · investigación de evidencia · encuesta a 50 estudiantes | Equipo | Datos de la encuesta · evidencia verificada | ✅ |
| 2–3 | Plantilla 1 — Problem Statement Canvas (incluye flujo de dos etapas de clasificación) | Equipo | `plantilla_1_problem_statement.md` | ✅ |
| 3–4 | Inventario de fuentes RAG · verificar disponibilidad y licencias | Valeria | Lista de fuentes con URL y condiciones de uso | ✅ |
| 3–4 | Diseño del cuestionario diagnóstico · 5 variables e ítems | Lucía | Cuestionario v1 (5 ítems) | ✅ |
| 3–4 | Diseño del dataset A2 · esquema CSV · protocolo STAR preliminar | Aaron + Lucía | Esquema del dataset definido | ✅ |
| 4 | Plantilla 2 — Data Readiness Checklist (3 recursos: cuestionario diagnóstico + InterviewIQ-STAR + corpus RAG) | Equipo | `plantilla_2_data_readiness.md` | ✅ |
| 4–5 | Plantilla 3 — AI Product Canvas · flujo completo (2 clasificadores + G2) · Model Design Canvas · OKRs | Equipo | `plantilla_3_ai_product_canvas.md` | ✅ |
| 5 | README.md · cronograma.md | Equipo | `README.md` · `cronograma.md` | ✅ |
| 5–6 | Resumen ejecutivo | Equipo | `resumen_ejecutivo.md` | ✅ |
| 6 | Presentación PC1 | Equipo | `presentacion_pc1.pdf` | ⏳ |
| **Semana 6** | **Entrega y sustentación PC1** | **Equipo** | **Carpeta completa del repositorio** | ⏳ |

---

## PC2 — Fases M + P2 + T (Semanas 7–14)

### Semana 7 — Diseño del cuestionario + inicio del dataset

| Tarea | Responsable | Entregable |
|---|---|---|
| Finalizar cuestionario diagnóstico: 5 ítems, escala y opciones de respuesta para las variables (experiencia_entrevistas, conocimiento_star, confianza_autodeclarada, dificultad_estructurar, feedback_previo) | Lucía | `docs/cuestionario_diagnostico_v1.md` |
| Definir tamaño final y esquema CSV del dataset `InterviewIQ-STAR` (columnas: id, pregunta, respuesta, situacion, tarea, accion, resultado, fuente, anotador) | Aaron | `data/raw/schema.md` |
| Crear reglas claras y ejemplos para etiquetar S/T/A/R = 0 o 1 (qué cuenta y qué no cuenta como cada componente) | Lucía | `docs/protocolo_etiquetado_star.md` |
| Seleccionar y guardar fuentes finales del corpus RAG; registrar URL y condiciones de uso | Valeria | `data/raw/corpus_rag/` + `README_data.md` |
| Generar primeras respuestas sintéticas con LLM para el dataset (variedad: respuestas completas, parciales y deficientes) | Aaron | Primeros ~50 pares en CSV |
| Preparar consentimiento informado si se recolectan respuestas reales (Ley N.° 29733) | Lucía | `docs/consentimiento_informado.md` |

### Semana 8 — Etiquetado, balance y calidad

| Tarea | Responsable | Entregable |
|---|---|---|
| Doble etiquetado de una muestra (~30 pares) y medición de kappa de Cohen para cada etiqueta S/T/A/R | Lucía + equipo | Reporte de acuerdo entre anotadores |
| Resolver desacuerdos y actualizar protocolo STAR | Lucía | Protocolo STAR v2 |
| Completar ~200 pares etiquetados (respuestas completas, parciales y deficientes, con variedad de combinaciones de etiquetas) | Aaron + Lucía | `data/raw/interviewiq_star_v1.csv` |
| Contar positivos/negativos por etiqueta (S, T, A, R) y verificar balance; diseñar estrategia de balanceo si hay desbalance severo | Aaron | Reporte de balance |

### Semana 9 — Entrenamiento de clasificadores

| Tarea | Responsable | Entregable |
|---|---|---|
| Limpieza y procesamiento del dataset · split 70/10/20 · verificar ausencia de leakage entre particiones | Aaron | `data/processed/` |
| **Entrenar clasificador de nivel de preparación** (Logistic Regression sobre las 5 variables del cuestionario diagnóstico) | Aaron + Lucía | `notebooks/01_clasificador_nivel.ipynb` |
| **Documentar accuracy y umbral del clasificador de nivel; registrar matriz de confusión** | Aaron | `evaluation/clasificador_nivel.md` |
| Entrenar baseline STAR: TF-IDF + Logistic Regression (OneVsRest, 4 etiquetas) · registrar Macro F1 por etiqueta y global | Aaron | `notebooks/02_baseline_tfidf_lr.ipynb` |
| Documentar resultados del baseline STAR | Aaron | `evaluation/comparacion_modelos_a2.md` (v1) |

### Semana 10 — Modelo alternativo A2 + inicio pipeline RAG

| Tarea | Responsable | Entregable |
|---|---|---|
| Entrenar y comparar modelo alternativo STAR (TF-IDF + Linear SVM, OneVsRest) con el baseline · ajustar umbral por etiqueta en validación priorizando reducir falsos positivos | Aaron | `notebooks/03_modelo_alternativo_svm.ipynb` |
| Seleccionar modelo final A2 y documentar decisión con justificación del umbral considerando el costo diferencial de errores | Aaron | `evaluation/comparacion_modelos_a2.md` (v2) |
| Iniciar pipeline RAG: chunking del corpus (300–500 tokens, sin cortar oraciones) + generación de embeddings (text-embedding-3-small) | Valeria | `notebooks/04_rag_pipeline.ipynb` (v1) |
| Crear consultas de prueba para evaluar retrieval top-k (≥ 20 consultas con ground truth de documentos relevantes) | Valeria + Aaron | `evaluation/consultas_prueba_rag.md` |

### Semana 11 — Pipeline RAG G2 funcional

| Tarea | Responsable | Entregable |
|---|---|---|
| Construir índice vectorial (FAISS o ChromaDB) con el corpus final | Valeria | Índice vectorial local |
| Conectar retrieval + LLM (GPT-4o-mini) + system prompt · prueba end-to-end del flujo completo (cuestionario diagnóstico → clasificador de nivel → A2 → G2) | Valeria + Aaron | `notebooks/04_rag_pipeline.ipynb` (v2) |
| Evaluar retrieval: precision@k sobre las consultas de prueba · documentar resultado | Valeria | Métrica en `evaluation/metricas_g2.md` |
| Revisar y ajustar system prompt: restricciones (no inventar experiencias, no afirmar probabilidades de contratación, no contradecir A2) | Lucía | `docs/system_prompt_v2.md` |

### Semana 12 — Integración MVP y despliegue

| Tarea | Responsable | Entregable |
|---|---|---|
| Desarrollar interfaz Streamlit: cuestionario diagnóstico + selección de rol + sesión de práctica + panel de feedback con componentes STAR | Lucía | `src/app/` |
| **Integrar clasificador de nivel + clasificador STAR A2 + pipeline G2 + interfaz Streamlit en flujo completo funcional** | Equipo | MVP local funcionando |
| Desplegar en Streamlit Community Cloud · obtener URL pública | Aaron | **URL pública del MVP** |
| Prueba interna del MVP completo (equipo) · documentar bugs y ajustes | Equipo | Lista de bugs / ajustes |

### Semana 13 — Evaluación con usuarios y análisis de riesgos

| Tarea | Responsable | Entregable |
|---|---|---|
| Aplicar cuestionario pre-uso a ≥ 15 usuarios externos al equipo (incluyendo cuestionario diagnóstico del sistema) | Lucía | Datos baseline por usuario |
| Sesión de práctica con el MVP (≥ 15 usuarios externos al equipo, estudiantes universitarios de últimos ciclos) | Equipo | Sesiones registradas |
| Aplicar cuestionario post-uso · medir KR1 (preparación percibida), KR2 (dificultad STAR) y KR3 (feedback recibido) | Lucía | Datos post-uso |
| Análisis de métricas técnicas finales: clasificador de nivel (accuracy), A2 (Macro F1 sobre test), G2 (retrieval precision@k) | Aaron | `evaluation/` actualizado |
| Análisis de riesgos del proyecto (Fase T del framework PROMPT) | Equipo | Sección de riesgos en PC2 |

### Semana 14 — Sustentación PC2

| Tarea | Responsable | Entregable |
|---|---|---|
| Preparar presentación PC2 con resultados reales de métricas técnicas y validación con usuarios | Equipo | `presentacion_pc2.pdf` |
| **Sustentación PC2** | **Equipo** | **MVP + métricas + análisis de riesgos** |

---

## Roles por integrante (PC2)

| Integrante | Rol principal |
|---|---|
| **Aaron Van Oord** | Dataset `InterviewIQ-STAR` · entrenamiento de clasificadores (nivel + STAR A2) · pipeline técnico · despliegue |
| **Lucía Rodríguez** | Cuestionario diagnóstico · protocolo de etiquetado · system prompt · interfaz Streamlit · evaluación con usuarios |
| **Valeria Briceño** | Corpus RAG · embeddings · retrieval · fuentes y licencias · pipeline G2 |
| **Todos** | Integración final · presentaciones · sustentaciones |

---

## Dependencias críticas

```
Cuestionario diagnóstico diseñado (S7)
   └──► Recolección de datos de nivel (S13)
           └──► Clasificador de nivel entrenado (S9)
                   └──► Generación de preguntas adaptadas integrada en MVP (S12)

Dataset InterviewIQ-STAR construido y etiquetado (S8)
   └──► Entrenamiento baseline STAR A2 (S9)
           └──► Modelo alternativo y selección final A2 (S10)
                   └──► Integración con pipeline G2 (S11–S12)
                           └──► Evaluación con usuarios (S13)

Corpus RAG seleccionado (S7)
   └──► Chunking + embeddings (S10)
           └──► Índice vectorial + retrieval funcional (S11)
                   └──► Integración con A2 y clasificador de nivel (S12)
```

---
