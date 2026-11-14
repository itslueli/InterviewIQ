# Coherencia del feedback con el modelo — 20 casos
## mvp/evidencia/coherencia_feedback.md

**Proyecto:** InterviewIQ · AD5018 · UTEC 2026-2
**Métrica (Plantilla 4, A3):** feedback coherente con el output de A2, meta ≥ 90% en 20 casos
**Modo evaluado:** feedback por reglas, el que muestra la app cuando no hay API key configurada. Se usaron los modelos de `models/` con los umbrales vigentes (S 0.30 · T 0.30 · A 0.75 · R 0.50) y las mismas funciones de `app.py` (`predecir`, `gen_feedback`, `es_hip`).

---

## Resultado

| Métrica | Resultado | Meta | Cumple |
|---|---|---|---|
| **Coherencia feedback ↔ modelo** (el feedback no contradice lo que detectó A2) | **20/20 (100%)** | ≥ 90% | ✅ |
| Feedback correcto frente a la etiqueta real (respuestas del dataset) | 12/15 (80%) | — | — |
| Feedback correcto en casos límite | 2/5 (40%) | — | — |
| **Feedback correcto en total** | **14/20 (70%)** | — | — |

**Cómo leerlo:**
- **Coherencia (100%).** Sin API key, el feedback se arma directamente con lo que detecta el modelo: lo presente va en "Lo que hiciste bien" y lo ausente en "Lo que falta". Por eso nunca lo contradice. Es coherente por diseño.
- **Corrección (70%).** Que el feedback sea coherente no garantiza que sea correcto. Cuando el modelo se equivoca, el feedback repite el error. Los 6 errores vienen del clasificador, no del feedback.

---

## Registro de los 20 casos

Componentes: S = Situación · T = Tarea · A = Acción · R = Resultado. Las probabilidades del componente que falla van entre paréntesis.

| # | Origen | Esperado | Detectado por el modelo | Qué dice el feedback | ¿Coherente con el modelo? | ¿Correcto? |
|---|---|---|---|---|---|---|
| 1 | Dataset id 61 | S-T-A-R | S-T-A-R | "Respuesta STAR completa" | ✅ | ✅ |
| 2 | Dataset id 3 | S-T-A-R | S-T-A (R 0.43) | Falta Resultado | ✅ | ❌ Falso negativo en R |
| 3 | Dataset id 62 | S-T-A-R | S-T-A-R | "Respuesta STAR completa" | ✅ | ✅ |
| 4 | Dataset id 181 | S-T-A-R | S-T-A-R | "Respuesta STAR completa" | ✅ | ✅ |
| 5 | Dataset id 22 | S-T-A | S-T-A | Falta Resultado | ✅ | ✅ |
| 6 | Dataset id 26 | S-T-A | S-T-A-R (R 0.91) | "Respuesta STAR completa" | ✅ | ❌ Falso positivo en R |
| 7 | Dataset id 23 | S-T-A | S-T-A | Falta Resultado | ✅ | ✅ |
| 8 | Dataset id 87 | S-A | S-A | Faltan Tarea y Resultado | ✅ | ✅ |
| 9 | Dataset id 85 | S-A | S-A | Faltan Tarea y Resultado | ✅ | ✅ |
| 10 | Dataset id 71 | S-T | S-T | Faltan Acción y Resultado | ✅ | ✅ |
| 11 | Dataset id 68 | S-T | S-T | Faltan Acción y Resultado | ✅ | ✅ |
| 12 | Dataset id 34 | A | Ninguno (A 0.41) | Reorganizar con la plantilla STAR completa | ✅ | ❌ Falso negativo en A |
| 13 | Dataset id 38 | A | A | Faltan Situación, Tarea y Resultado | ✅ | ✅ |
| 14 | Dataset id 112 | Ninguno | Ninguno | Reorganizar con la plantilla STAR completa | ✅ | ✅ |
| 15 | Dataset id 91 | S-A-R | S-A-R | Falta Tarea | ✅ | ✅ |
| 16 | Límite · muy corta | Ninguno | Ninguno | Reorganizar con la plantilla STAR completa | ✅ | ✅ |
| 17 | Límite · todo en "nosotros" | S-T-R, sin A | S-T-A-R (A 0.87) | "Respuesta STAR completa" | ✅ | ❌ Falso positivo en A |
| 18 | Límite · sin resultado | S-T-A | S-T-A-R (R 0.57) | "Respuesta STAR completa" | ✅ | ❌ Falso positivo en R |
| 19 | Límite · hipotética | Ninguno | S-T-A + aviso de respuesta hipotética | Falta Resultado; la app además muestra el aviso "cuenta un caso real" | ✅ | ❌ Falso positivo, mitigado por el aviso |
| 20 | Límite · resultado corto | S-T-A-R | S-T-A-R (R 0.61) | "Respuesta STAR completa" | ✅ | ✅ |

---

## Hallazgos

1. **El feedback por reglas nunca contradice al modelo**, así que la meta de coherencia se cumple. La calidad del feedback depende por completo de que el clasificador acierte.
2. **El error más frecuente es el falso positivo** (4 de 6 errores: casos 6, 17, 18 y 19). Coincide con la lectura de costos de la Plantilla 4: es el error más caro, porque el estudiante recibe "Respuesta STAR completa" sin que lo esté.
3. **Las respuestas que cuentan todo en "nosotros" pasan como completas** (caso 17). El feedback de "Respuesta STAR completa" no le recuerda al estudiante que hable en primera persona.
4. **El aviso de respuesta hipotética funciona** (caso 19). Es la única mitigación activa contra un falso positivo.

## Limitaciones

- Las respuestas de los casos límite 17, 18 y 20 son reconstrucciones de los casos C2, C3 y C5 de `pruebas_usuario.md`, porque el texto original no quedó registrado. Por eso sus probabilidades no coinciden con las de ese archivo.
- Las 15 respuestas del dataset pueden haber estado en el entrenamiento de los `.pkl` de `models/`, así que su 80% de acierto puede ser optimista.
- No se evaluó el feedback con Gemini. El modelo que usa la app por defecto (`gemini-2.5-flash`) ya no está disponible para claves nuevas, y el equipo decidió dejar el MVP sin API key.
