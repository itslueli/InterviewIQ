# Resumen Ejecutivo — InterviewIQ
## AD5018 Inteligencia Artificial para Negocios | UTEC 2026-2

**Equipo:** Valeria Briceño · Lucía Rodríguez · Aaron Van Oord

---

## Problema

Los estudiantes universitarios peruanos de últimos ciclos tienen dificultad para preparar y mejorar sus respuestas en entrevistas laborales por competencias porque cuentan con oportunidades limitadas de práctica recurrente con retroalimentación estructurada, lo que genera bajos niveles de preparación percibida y dificultades para estructurar respuestas conductuales.

El contexto nacional agrava el problema: 14.3% de desempleo juvenil (INEI, 2024), 7 de cada 10 jóvenes en situación de inadecuación ocupacional (MTPE, 2024) y 60.8% de empresas que no encuentra trabajadores con las habilidades requeridas (INEI ENE, 2020). Una encuesta propia a 50 estudiantes universitarios de últimos ciclos confirma la escala del problema: **60% se siente poco o nada preparado**, **80% reporta dificultad para estructurar respuestas conductuales** y **40% rara vez recibe retroalimentación estructurada** al practicar.

---

## Usuario

Estudiantes universitarios peruanos de últimos ciclos que buscan prácticas preprofesionales o su primer empleo y necesitan prepararse para entrevistas laborales por competencias, sin acceso a coaching profesional.

---

## Propuesta

**InterviewIQ** es un simulador conversacional de entrevistas por competencias que combina dos etapas de clasificación y un componente generativo RAG para personalizar la práctica y proporcionar retroalimentación estructurada. El flujo completo es:

1. El estudiante selecciona el **rol objetivo** al que está postulando.
2. Completa un **cuestionario diagnóstico breve** (5 ítems: experiencia previa en entrevistas, conocimiento de metodología STAR, nivel de confianza autodeclarada, dificultad para estructurar respuestas y frecuencia de feedback recibido).
3. Un **clasificador de nivel de preparación** (Logistic Regression) asigna al usuario un nivel (`básico`, `intermedio` o `avanzado`) según sus respuestas al cuestionario.
4. El sistema genera **preguntas conductuales adaptadas** al rol objetivo y al nivel detectado: preguntas más accesibles para niveles básicos, más exigentes para niveles avanzados.
5. El estudiante responde en texto libre.
6. El **clasificador STAR** (Componente A2: TF-IDF + Logistic Regression baseline vs TF-IDF + Linear SVM alternativo) detecta qué componentes STAR (Situación, Tarea, Acción, Resultado) están presentes o ausentes en la respuesta.
7. El **pipeline RAG** (Componente G2) recupera contexto relevante del corpus de documentos verificados, y el LLM genera **retroalimentación personalizada** combinando las predicciones del clasificador STAR con el contexto recuperado: señala qué componentes están bien desarrollados, cuáles faltan y cómo mejorarlos con ejemplos concretos.

---

## Datos

El sistema requiere tres recursos de datos diferenciados:

| Recurso | Descripción | Estado |
|---|---|---|
| **R1 — Cuestionario diagnóstico** | Respuestas al cuestionario inicial (5 variables) para entrenar el clasificador de nivel de preparación | 🟡 Pendiente de recolección (S13) |
| **R2 — InterviewIQ-STAR** | ~200 pares (pregunta conductual, respuesta, etiquetas S/T/A/R = 0/1) construidos por el equipo | 🟡 Pendiente de construcción (S7–8) |
| **R3 — Corpus RAG** | ~20–50 documentos sobre metodología STAR y competencias por rol (fuentes verificadas) | 🟡 Fuentes identificadas; corpus a cerrar (S7) |

Las fuentes del corpus RAG (USC Career Center, UC Santa Cruz Career Success, Wilkie & Rosendale 2024, Marcus et al. 2023, ESCO) están verificadas y accesibles públicamente o bajo licencias compatibles. El principal bloqueante para PC2 es la construcción del dataset `InterviewIQ-STAR` (R2).

---

## Componente Analítico (A2)

**Etapa 1 — Clasificación de nivel de preparación:**
Logistic Regression entrenada sobre las respuestas del cuestionario diagnóstico (R1). Las 5 variables del cuestionario (experiencia_entrevistas, conocimiento_star, confianza_autodeclarada, dificultad_estructurar, feedback_previo) se usan como features para predecir el nivel {básico / intermedio / avanzado}. El nivel detectado se pasa como parámetro al prompt de generación de preguntas.

- **Métrica:** Accuracy en conjunto de test
- **Criterio de aceptación:** Accuracy ≥ 0.65 en validación

**Etapa 2 — Clasificación STAR (componente A2 principal):**
Clasificación multilabel que detecta la presencia o ausencia independiente de Situación, Tarea, Acción y Resultado en cada respuesta del estudiante. Se compararán **TF-IDF + Logistic Regression** (baseline) y **TF-IDF + Linear SVM** (modelo alternativo), ambos con esquema OneVsRest para las 4 etiquetas, usando Macro F1 como métrica principal. El umbral de decisión se ajustará por etiqueta en validación, priorizando reducir falsos positivos (el error más costoso: indicar que un componente STAR está presente cuando no lo está equivale a decirle al estudiante que su respuesta es buena cuando no lo es).

- **Métrica:** Macro F1 en conjunto de test
- **Criterio de aceptación:** Macro F1 ≥ 0.65

---

## Componente Generativo (G2 — RAG)

Pipeline RAG que opera en dos momentos del flujo: (1) **generación de preguntas conductuales** adaptadas al rol y al nivel detectado en Etapa 1, y (2) **generación de feedback personalizado** combinando la salida del clasificador STAR (Etapa 2) con contexto recuperado del corpus.

Flujo técnico: chunking del corpus (300–500 tokens) → embeddings (text-embedding-3-small) → índice vectorial (FAISS o ChromaDB) → retrieval top-k por similitud coseno → LLM (GPT-4o-mini) con system prompt restrictivo.

El system prompt del LLM prohíbe: inventar experiencias del usuario, afirmar probabilidades de contratación, contradecir la salida del modelo A2 o recomendar como presentes componentes STAR que A2 marcó como ausentes.

- **Métrica:** Retrieval precision@k sobre consultas de prueba
- **Criterio de aceptación:** Precision@k ≥ 0.80

---

## Producto

Interfaz web conversacional (Streamlit) desplegada en Streamlit Community Cloud, con URL pública disponible antes de la Semana 12. Flujo de usuario: selección de rol → cuestionario diagnóstico → pregunta adaptada → respuesta → análisis STAR + feedback → siguiente pregunta. Sin audio, video, autenticación ni base de datos persistente en el MVP.

---

## Impacto esperado

| OKR | Baseline (encuesta propia, n=50) | Meta con MVP |
|---|---|---|
| Estudiantes poco o nada preparados para entrevistas por competencias | 60% | ≤ 40% tras uso del MVP |
| Estudiantes con dificultad para estructurar respuestas conductuales | 80% | ≤ 55% tras sesiones de práctica |
| Estudiantes que rara vez o nunca reciben retroalimentación estructurada | 40% | ≥ 90% reciben feedback en al menos 1 sesión |

Los OKRs se medirán con cuestionario pre/post aplicado a ≥ 15 usuarios en la Semana 13.

---

## Validación

Prueba con ≥ 15 usuarios externos al equipo (estudiantes universitarios de últimos ciclos, no miembros del equipo). Métricas: cuestionario pre/post (KR1, KR2, KR3), Macro F1 del clasificador STAR A2 sobre test etiquetado y retrieval precision@k del pipeline G2 sobre consultas de prueba. Estado actual del stack: 🟡 viable — R2 e R1 pendientes de construcción (bloqueante para PC2), fuentes del corpus RAG (R3) verificadas y accesibles.

---
