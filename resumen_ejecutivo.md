# Resumen Ejecutivo — InterviewIQ
## Inteligencia Artificial para Negocios | UTEC 2026-2

**Equipo:** Valeria Briceño · Lucía Rodríguez · Aaron Van Oord
**Fecha:** 2026-09-19 · PC1 Semana 6

---

## Problema

Los estudiantes universitarios peruanos de últimos ciclos tienen dificultad para preparar y mejorar sus respuestas en entrevistas laborales por competencias porque cuentan con oportunidades limitadas de práctica recurrente con retroalimentación estructurada, lo que genera bajos niveles de preparación percibida y dificultades para estructurar respuestas conductuales.

El contexto nacional agrava el problema: 14.3% de desempleo juvenil (INEI, 2024), 7 de cada 10 jóvenes en situación de inadecuación ocupacional (MTPE, 2024) y 60.8% de empresas que no encuentra trabajadores con las habilidades requeridas (INEI ENE, 2020). Una encuesta propia a 50 estudiantes universitarios de últimos ciclos confirma la escala del problema en el usuario objetivo: **60% se siente poco o nada preparado**, **80% reporta dificultad para estructurar respuestas conductuales** y **40% rara vez recibe retroalimentación estructurada** al practicar.

---

## Usuario

Estudiantes universitarios peruanos de últimos ciclos que buscan prácticas preprofesionales o su primer empleo y necesitan prepararse para entrevistas laborales por competencias, sin acceso a coaching profesional.

---

## Propuesta

**InterviewIQ** es un simulador conversacional de entrevistas por competencias. El estudiante selecciona un rol objetivo, responde preguntas conductuales en texto libre y recibe de forma inmediata: (1) un análisis de qué componentes STAR comunicó y cuáles faltan, y (2) retroalimentación personalizada con recomendaciones concretas para mejorar su respuesta.

---

## Datos

El componente analítico se entrenará con **`InterviewIQ-STAR`**: dataset propio de ~200 pares (pregunta conductual, respuesta candidato, etiquetas S/T/A/R) construido por el equipo. Las respuestas se generarán sintéticamente con LLM y se etiquetarán manualmente con un protocolo explícito; la consistencia se medirá con kappa de Cohen. El componente generativo usará un corpus RAG de ~20–50 documentos curados sobre metodología STAR, entrevistas conductuales y competencias por rol (fuentes: USC Career Center, UC Santa Cruz Career Success, ESCO, literatura académica verificada).

---

## Componente Analítico (A2)

Clasificación multilabel que detecta la presencia o ausencia independiente de Situación, Tarea, Acción y Resultado en cada respuesta. Se compararán **TF-IDF + Logistic Regression** (baseline) y **TF-IDF + Linear SVM** (modelo alternativo) con Macro F1 como métrica principal. El umbral de decisión se ajustará en validación por etiqueta, priorizando reducir falsos positivos (el error más costoso: indicar que un componente STAR está presente cuando no lo está). Criterio mínimo de aceptación: **Macro F1 ≥ 0.65** sobre el conjunto de test.

---

## Componente Generativo (G2 — RAG)

Pipeline RAG que formula preguntas conductuales contextualizadas al rol y genera feedback personalizado combinando la salida del clasificador A2 con conocimiento recuperado del corpus. Flujo: chunking (300–500 tokens) → embeddings → índice vectorial (FAISS/ChromaDB) → retrieval top-k → LLM (GPT-4o-mini) con system prompt restrictivo. El prompt prohíbe inventar experiencias, afirmar probabilidades de contratación o sustituir la salida del modelo A2. Criterio mínimo: **retrieval precision@k ≥ 0.80** sobre consultas de prueba.

---

## Producto

Interfaz web conversacional (Streamlit) desplegada en URL pública antes de la Semana 12. El flujo es: selección de rol → pregunta conductual → respuesta del usuario → análisis STAR + feedback → siguiente pregunta. Sin audio, video, autenticación ni base de datos persistente en el MVP. La práctica con entrevistas simuladas reduce ansiedad y aumenta preparación (Wilkie & Rosendale, 2024; Marcus et al., 2023).

---

## Impacto esperado

| OKR | Valor actual | Meta con MVP |
|---|---|---|
| Estudiantes poco/nada preparados para entrevistas | 60% | ≤ 40% tras uso del MVP |
| Estudiantes con dificultad para estructurar respuestas STAR | 80% | ≤ 55% tras sesiones de práctica |
| Estudiantes que nunca reciben feedback estructurado | 40% | ≥ 90% reciben feedback en al menos 1 sesión |

Los OKRs se medirán con cuestionario pre/post aplicado a ≥ 15 usuarios en la Semana 13.

---

## Validación

Prueba con ≥ 15 usuarios externos al equipo (estudiantes universitarios de últimos ciclos). Métricas: cuestionario pre/post (KR1, KR2, KR3), Macro F1 del modelo A2 sobre test etiquetado y retrieval precision@k del pipeline G2. Estado actual del stack: 🟡 viable — dataset pendiente de construcción (bloqueante para PC2), fuentes RAG iniciales verificadas y accesibles.

---
