# InterviewIQ - Simulador Inteligente de Entrevistas para Universitarios
**Curso:** AD5018 - Inteligencia Artificial para Negocios UTEC 2026-2  
**Fase actual:** PC1 (Semanas 1-6)

---

## 1. Problema
Los estudiantes universitarios peruanos enfrentan una brecha significativa entre sus competencias académicas y las exigencias del mercado laboral. La falta de práctica real con entrevistas por competencias (formato STAR) genera una alta tasa de rechazo en procesos de selección.

**Evidencia verificada:**
* **14.3%** de desempleo juvenil en Perú (INEI, 2024).
* **7 de cada 10** jóvenes peruanos experimentan inadecuación ocupacional (MTPE, 2024).
* Brecha de competencias del **40%** entre egresados y requisitos empresariales (BID, 2019).
* **60.8%** de empresas peruanas declara no encontrar trabajadores con las habilidades requeridas (INEI ENE, 2020).
* La práctica con *mock interviews* reduce la ansiedad y aumenta la preparación (Wilkie & Rosendale, 2024).

---

## 2. Usuario Objetivo
* **Primario:** Estudiantes universitarios peruanos (18-28 años) en etapa de búsqueda de primer empleo o prácticas, sin acceso a coaching profesional.
* **Secundario:** Egresados recientes con hasta 2 años de experiencia.

---

## 3. Propuesta
InterviewIQ es un simulador conversacional de entrevistas por competencias que:
1. Genera preguntas conductuales según el sector o rol objetivo.
2. Recibe respuestas del usuario en texto libre.
3. Clasifica automáticamente la calidad de la respuesta según el framework STAR (**Componente Analítico A2/A1**).
4. Genera retroalimentación personalizada mediante **RAG + LLM** (**Componente Generativo G2**).
5. Acumula el historial de sesiones para mostrar el progreso.

---

## 4. Arquitectura de IA
* **Generador de preguntas:** LLM con prompts por rol/sector.
* **Componente Analítico:** Clasificador STAR ML entrenado por el equipo (Output: Alto / Medio / Bajo).
* **Componente Generativo:** RAG + LLM apoyado en guías STAR y ejemplos por sector.

---

## 5. Componente Analítico
* **Tarea:** Clasificación de calidad de respuestas conductuales.
* **Clases objetivo:**
  * **ALTO:** Respuesta completa (Situación + Tarea + Acción + Resultado cuantificable).
  * **MEDIO:** Respuesta parcial (2-3 elementos STAR presentes).
  * **BAJO:** Respuesta vaga sin estructura STAR.
* **Dataset:** Dataset propio construido por el equipo (~200 pares etiquetados).
* **Métricas objetivo:**
  * $F1\text{ macro} \ge 0.65$ sobre conjunto de validación.
  * $\text{Accuracy} \ge 0.70$.

---

## 6. Componente Generativo (G2)
* **Tipo:** RAG (Retrieval-Augmented Generation) + LLM (GPT-4o-mini o similar).
* **Base de conocimiento:** Guías de entrevistas por competencias (STAR), ejemplos por sector y errores comunes.

---

## 7. Estructura del Repositorio
```text
proyecto-entrevistas-ia/
├── README.md                     <-- Portada principal
├── resumen_ejecutivo.md          <-- Síntesis de 1 página
├── presentacion_pc1.pdf          <-- Presentación evaluable
├── cronograma.md                 <-- Gantt semanas 1-13
└── plantillas/
    ├── plantilla_1_problem_statement.md
    ├── plantilla_2_data_readiness.md
    └── plantilla_3_ai_product_canvas.md
└── plantilla_3_ai_product_canvas.md
```
