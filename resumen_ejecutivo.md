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
6. El **clasificador STAR** (Componente A2: TF-IDF + Linear SVM) detecta qué componentes STAR (Situación, Tarea, Acción, Resultado) están presentes o ausentes en la respuesta.
7. El **pipeline RAG** (Componente G2) recupera contexto relevante del corpus de documentos verificados, y el LLM genera **retroalimentación personalizada** combinando las predicciones del clasificador STAR con el contexto recuperado.

---

## Datos

| Recurso | Descripción | Estado |
|---|---|---|
| **R1 — Cuestionario diagnóstico** | Respuestas al cuestionario inicial (5 variables) para entrenar el clasificador de nivel de preparación | ✅ Construido |
| **R2 — InterviewIQ-STAR** | 200 pares (pregunta conductual, respuesta, etiquetas S/T/A/R = 0/1) construidos por el equipo | ✅ Construido — `data/raw/interviewiq_star_v1.csv` |
| **R3 — Corpus RAG** | ~20–50 documentos sobre metodología STAR y competencias por rol (fuentes verificadas) | ✅ Fuentes verificadas; corpus integrado en MVP |

---

## Componente Analítico (A2) — Resultados reales

**Etapa 1 — Clasificación de nivel de preparación:**
Logistic Regression entrenada sobre las respuestas del cuestionario diagnóstico (R1). Las 5 variables del cuestionario se usan como features para predecir el nivel {básico / intermedio / avanzado}.

- **Criterio de aceptación:** Accuracy ≥ 0.65 ✅

**Etapa 2 — Clasificación STAR (componente A2 principal):**
Clasificación multilabel independiente por componente STAR. Se compararon TF-IDF + Logistic Regression (baseline) y TF-IDF + Linear SVM (modelo final). El umbral de decisión se ajustó por etiqueta en validación priorizando reducir Falsos Positivos.

**Modelo seleccionado: TF-IDF + Linear SVM**

| Componente | F1 Macro | Umbral | Criterio ≥ 0.65 |
|------------|----------|--------|----------------|
| S — Situación | 0.865 | 0.30 | ✅ CUMPLE |
| T — Tarea | 0.822 | 0.30 | ✅ CUMPLE |
| A — Acción | 0.804 | 0.75 | ✅ CUMPLE |
| R — Resultado | 0.829 | 0.70 | ✅ CUMPLE |
| **Promedio** | **0.830** | — | ✅ CUMPLE |

El modelo SVM supera al baseline LR en F1 promedio (0.886 sin ajuste de umbral vs 0.842). Con umbrales ajustados para minimizar Falsos Positivos, el F1 promedio final es **0.830**, superando el criterio de 0.65.

---

## Componente Generativo (G2 — RAG)

Pipeline RAG que opera en dos momentos del flujo: (1) generación de preguntas conductuales adaptadas al rol y nivel, y (2) generación de feedback personalizado combinando la salida del clasificador STAR con contexto recuperado del corpus.

Flujo técnico: chunking del corpus (300–500 tokens) → embeddings (text-embedding-3-small) → índice vectorial (FAISS o ChromaDB) → retrieval top-k por similitud coseno → LLM (GPT-4o-mini) con system prompt restrictivo.

El system prompt prohíbe: inventar experiencias del usuario, afirmar probabilidades de contratación, contradecir la salida del modelo A2 o recomendar como presentes componentes STAR que A2 marcó como ausentes.

- **Criterio de aceptación:** Precision@k ≥ 0.80

---

## Producto

Interfaz web (Streamlit) desplegada en Streamlit Community Cloud con URL pública. Flujo: selección de pregunta → respuesta en texto libre → análisis STAR → feedback personalizado. Sin audio, video, autenticación ni base de datos persistente en el MVP.

**URL del MVP:** 

---

## Impacto esperado

| OKR | Baseline (encuesta propia, n=50) | Meta con MVP | Estado |
|---|---|---|---|
| KR1 — Estudiantes poco o nada preparados | 60% | ≤ 40% tras uso del MVP | 🔄 En medición |
| KR2 — Estudiantes con dificultad para estructurar respuestas | 80% | ≤ 55% tras sesiones de práctica | 🔄 En medición |
| KR3 — Estudiantes que rara vez reciben feedback estructurado | 40% | ≥ 90% reciben feedback en al menos 1 sesión | 🔄 En medición |

Los OKRs se medirán con pruebas de usuario documentadas en `mvp/evidencia/pruebas_usuario.md` (≥ 5 usuarios externos al equipo).

---

## Validación

Prueba con ≥ 5 usuarios externos al equipo (estudiantes universitarios de últimos ciclos). Métricas: cuestionario pre/post (KR1, KR2, KR3), Macro F1 del clasificador STAR A2 (**0.830 obtenido** ✅) y retrieval precision@k del pipeline G2.

**Estado del stack PC2:** ✅ Modelos entrenados y guardados · ✅ App Streamlit deployada · ✅ Dataset R2 construido (200 filas) · 🔄 Pruebas de usuario en curso
