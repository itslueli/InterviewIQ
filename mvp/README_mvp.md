# InterviewIQ — Guía del MVP para el Evaluador

**Proyecto:** InterviewIQ  
**Curso:** AD5018 — Inteligencia Artificial para Negocios · UTEC 2026-2  
**Equipo:** Lucía Rodríguez · Valeria Briceño · Jennifer Patiño · Aaron Van Oord

---

## URL de acceso

> **https://interviewiq-utec.streamlit.app/**

Accesible desde cualquier dispositivo con internet. No requiere instalación, cuenta ni configuración adicional.

---

## ¿Qué hace el MVP?

InterviewIQ analiza respuestas de entrevistas por competencias y detecta automáticamente qué componentes STAR (Situación, Tarea, Acción, Resultado) están presentes o ausentes, con un score de 0 a 4 y feedback personalizado para mejorar la respuesta.

**Flujo completo:**

```
Landing page → Elegir pregunta → Escribir respuesta → Analizar → Ver resultados STAR + feedback
```

---

## Instrucciones para el evaluador

### Paso 1 — Acceder al MVP

Abre **https://interviewiq-utec.streamlit.app/** en cualquier navegador. Verás la landing page con la descripción del producto.

### Paso 2 — Iniciar el análisis

Haz clic en **"Comenzar práctica →"** para ir a la página de análisis.

### Paso 3 — Seleccionar una pregunta

En el panel **"1 · Pregunta de entrevista"**, elige una pregunta del banco desplegable. También puedes escribir tu propia pregunta seleccionando la opción *"✏️ Escribe tu propia pregunta..."*.

**Ejemplos de preguntas disponibles:**
- *"Cuéntame sobre una vez que tuviste que resolver un problema difícil en equipo"*
- *"¿Puedes darme un ejemplo de cuando tuviste que cumplir un plazo muy ajustado?"*
- *"Describe una situación en la que tuviste que adaptarte a un cambio inesperado"*

### Paso 4 — Escribir la respuesta

En el panel **"2 · Tu respuesta"**, escribe una respuesta en texto libre. Se recomienda mínimo 20 palabras para que el modelo pueda analizar correctamente la estructura.

**Respuesta de ejemplo — 3 o 4/4 (resultado depende de la frase final):**

> *"En mi último semestre, mi equipo tenía que entregar un proyecto de análisis de datos en una semana pero nos dimos cuenta que el dataset tenía errores graves. Mi responsabilidad era liderar la limpieza de datos. Reorganicé el trabajo en turnos, asigné tareas específicas a cada miembro y establecimos checkpoints diarios. Logramos entregar a tiempo y el proyecto obtuvo la mejor nota del ciclo."*

Esta respuesta puede dar 3/4 o 4/4 según la confianza del modelo: "la mejor nota del ciclo" es un resultado vago sin dato numérico concreto y queda cerca del umbral de detección (u=0.50). El modelo puede detectarlo como presente o ausente.

**Respuesta de ejemplo — 4/4 (todos los componentes presentes):**

> *"En mi último semestre, mi equipo tenía que entregar un proyecto de análisis de datos en una semana pero nos dimos cuenta que el dataset tenía errores graves. Mi responsabilidad era liderar la limpieza de datos. Reorganicé el trabajo en turnos, asigné tareas específicas a cada miembro y establecimos checkpoints diarios. Logramos entregar a tiempo, corregimos el 100% de los errores del dataset y el proyecto obtuvo 20/20, la nota más alta de la sección."*

Esta versión agrega un resultado con dato concreto (100% de errores corregidos, 20/20) y debería dar 4/4.

### Paso 5 — Analizar

Presiona el botón **"Analizar respuesta →"** (se activa cuando hay pregunta y respuesta escritas).

### Paso 6 — Revisar resultados

La página mostrará:

| Panel | Contenido |
|-------|-----------|
| **Score STAR** | Gauge de 0 a 4 con los 4 componentes detectados |
| **Análisis por componente** | S / T / A / R con ✅ presente o ❌ ausente y probabilidad |
| **Feedback** | Retroalimentación contextualizada generada por Gemini 2.5 Flash |

---

## Casos de prueba recomendados

Para evaluar el comportamiento del modelo en distintos escenarios:

| Caso | Descripción | Score esperado |
|------|-------------|---------------|
| Respuesta completa STAR | Incluye los 4 componentes explícitamente | 4/4 |
| Sin Resultado | Describe la situación, tarea y acción, pero no menciona el resultado final | 3/4 (R ausente) |
| Sin Situación ni Tarea | Solo describe qué hizo, sin contexto previo | 2/4 |
| Respuesta muy corta | Menos de 20 palabras, sin estructura | 0–1/4 |
| Respuesta en otro idioma | Inglés u otro idioma | Comportamiento degradado (modelo entrenado en español) |

---

## Stack técnico

| Componente | Tecnología | Detalle |
|------------|------------|---------|
| Clasificador STAR (A2) | TF-IDF bigramas + Linear SVM | scikit-learn · 4 modelos `.pkl` · umbrales ajustados por componente |
| Feedback (G1) | Gemini 2.5 Flash | API REST vía `requests` · fallback a reglas estructuradas |
| Interfaz | Streamlit | Python · dos páginas (landing + análisis) |
| Deploy | Streamlit Community Cloud | HTTPS · sin base de datos persistente |
| Modelos | 4 archivos `.pkl` + `config_clasificador.json` | `models/` en el repositorio |

---

## Métricas del modelo (A2)

| Componente | F1 Macro | Umbral | Criterio ≥ 0.65 |
|------------|----------|--------|----------------|
| S — Situación | **0.865** | 0.30 | ✅ |
| T — Tarea | **0.822** | 0.30 | ✅ |
| A — Acción | **0.804** | 0.75 | ✅ |
| R — Resultado | **0.829** | 0.50 | ✅ |
| **Promedio** | **0.830** | — | ✅ |

---

## Limitaciones conocidas

| Limitación | Descripción | Mitigación |
|------------|-------------|------------|
| Dataset sintético | El modelo fue entrenado con 200 pares, en su mayoría sintéticos | F1 validado en set de prueba; pruebas con usuarios reales en curso |
| Respuestas cortas | Respuestas < 20 palabras pueden tener baja confianza | La app advierte al usuario |
| Idioma | Modelo entrenado en español | Comportamiento no garantizado en otros idiomas |
| Sin historial | No guarda respuestas entre sesiones | Por diseño (privacidad) |

---

## Repositorio

[github.com/itslueli/InterviewIQ](https://github.com/itslueli/InterviewIQ)

Documentación completa del proyecto en:
- `resumen_ejecutivo.md` — visión general del producto
- `plantillas/plantilla_4_scorecard_risk.md` — métricas detalladas y análisis de riesgos
- `mvp/evidencia/pruebas_usuario.md` — protocolo y resultados de pruebas con usuarios
