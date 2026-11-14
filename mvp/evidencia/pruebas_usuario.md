# Pruebas de Usuario — InterviewIQ
## mvp/evidencia/pruebas_usuario.md

**Proyecto:** InterviewIQ  
**Curso:** AD5018 — Inteligencia Artificial para Negocios · UTEC 2026-2  
**Equipo:** Valeria Briceño · Lucía Rodríguez · Jennifer Patiño · Aaron Van Oord  
**MVP URL:** https://interviewiq-utec.streamlit.app/  
**Fecha de las pruebas:** 13 de noviembre de 2026 (16:29 – 18:03)

---

## Protocolo de prueba

Cada usuario prueba el MVP de forma **independiente**, sin ayuda del equipo. La tarea es:

> "Entra a la URL, elige una pregunta de entrevista, escribe tu respuesta y lee el feedback que te da la app."

- **Participantes:** 8 estudiantes universitarios externos al equipo, contactados por WhatsApp. El perfil es el usuario objetivo de la Plantilla 1: estudiantes que se preparan para entrevistas de prácticas o de primer empleo.
- **Instrumento:** Google Form anónimo en 3 secciones: (1) antes de usar la app, (2) uso de la app con el link, (3) después de usar la app. El equipo solo envió el link del formulario y no explicó cómo usar la app.
- **Privacidad:** no se recolectaron nombres, correos ni DNI (Ley N.° 29733). Por eso no se registró la pregunta elegida ni la respuesta escrita por cada usuario.
- **Nota de método:** las 2 primeras respuestas (U01 y U02) se recogieron con una versión inicial del formulario, que aún no tenía las preguntas 4 (uso sin ayuda) ni 6 (dificultad STAR después).

---

## Registro de pruebas

Escalas de 1 a 5. Preparación: 1 = nada preparado/a, 5 = muy preparado/a. Facilidad STAR: 1 = muy difícil, 5 = muy fácil. Frecuencia de feedback: 1 = nunca, 5 = siempre.

| Usuario | Hora | Preparación antes → después | Facilidad STAR antes → después | Recibe feedback (antes) | ¿Sin ayuda? | Utilidad del feedback | Entender el análisis (1–5) | ¿La usaría? | Observación del usuario |
|---|---|---|---|---|---|---|---|---|---|
| U01 | 16:29 | 1 → 2 | 2 → — | 4 | — | Muy útil | 3 | Sí | "nada" |
| U02 | 16:31 | 2 → 2 | 2 → — | 2 | — | Muy útil | 3 | Sí | "todo bien" |
| U03 | 16:51 | 2 → 4 | 3 → 4 | 2 | Sí | Muy útil | 4 | Sí | — |
| U04 | 17:35 | 3 → 3 | 3 → 3 | 3 | **Necesité ayuda** | Muy útil | 3 | Sí | — |
| U05 | 17:53 | 2 → 4 | 2 → 4 | 1 | Sí | (en blanco) | 3 | Sí | — |
| U06 | 18:01 | 5 → 5 | 4 → **2** | 4 | Sí | Muy útil | 4 | Sí | — |
| U07 | 18:02 | 2 → 4 | 2 → 4 | 1 | Sí | Muy útil | 4 | Sí | "un poco de más color" |
| U08 | 18:03 | 4 → 5 | 4 → 5 | 4 | Sí | Muy útil | 5 | Sí | — |

---

## Caso límite documentado

Escenarios diseñados por el equipo para encontrar dónde falla el modelo. **Son pruebas internas, no usuarios.** Entre paréntesis está la probabilidad del modelo frente al umbral vigente: S 0.30 · T 0.30 · A 0.75 · R 0.50.

| Caso | Respuesta ingresada | Esperado | Output del MVP | Evaluación del equipo |
|---|---|---|---|---|
| C1 · Muy corta | "Trabajé en equipo y salió bien." | Ninguno | Ninguno (S 0.21 · T 0.20 · A 0.36 · R 0.15) + aviso de respuesta corta | ✅ Correcto: no inventa componentes. |
| C2 · Todo en "nosotros" | Campaña de Marketing contada solo con "nosotros hicimos…", cierra con "nos fue bien y el profesor nos felicitó" | S, T y un R vago; sin Acción personal | S-T-R · A ausente (0.63 < 0.75) | ✅ Correcto: el umbral alto de Acción no premia respuestas sin acción individual. |
| C3 · Sin resultado | Reporte de 3 horas → aprendió Power Query y automatizó, sin decir qué pasó | S-T-A, falta R | S-T-A (R 0.49) | ✅ Correcto, aunque R queda muy cerca del umbral. |
| C4 · Hipotética | "Si tuviera un conflicto en mi equipo, yo hablaría con cada persona…" | Ninguno (no es un caso real) | S-T-A (A 0.84) + **aviso de respuesta hipotética** | ❌ Falso positivo del modelo, **mitigado**: la app ahora detecta frases en condicional y avisa al usuario (ver hallazgo 1). |
| C5 · Resultado numérico claro | Igual que C3 + "el reporte pasó a tomar 15 minutos y el gerente lo adoptó" | S-T-A-R | S-T-A (R 0.45) | ❌ Falso negativo: aun con el umbral en 0.50, el modelo no reconoce resultados cortos. Queda como limitación. |

---

## Hallazgos y cambios realizados

| # | Hallazgo | Fuente | Cambio aplicado al MVP |
|---|----------|--------|----------------------|
| 1 | Las respuestas hipotéticas ("yo haría…") se marcan como STAR casi completas | Caso límite C4 | ✅ **Sí.** Se agregó la detección de frases en condicional: la app avisa que hay que contar un caso real, y el feedback de IA también recibe esa alerta. |
| 2 | Los resultados cortos con datos no superan el umbral de R | Caso límite C5 | ❌ No. El umbral de R se bajó a 0.50, pero el caso sigue fallando (0.45). Requiere más ejemplos de "Resultado" en el dataset (solo 38% tiene R = 1). |
| 3 | "Entender el análisis STAR" es el indicador más bajo (3.6/5); la mitad de los usuarios marcó 3 | Usuarios (pregunta 8) | ⏳ Propuesto: reemplazar los valores técnicos de las tarjetas (`p=0.20 · u=0.3`) por una explicación simple. |
| 4 | 1 de 6 usuarios necesitó ayuda (U04) | Usuarios (pregunta 4) | ❌ No. El formulario no preguntó en qué se trabó; se agregará esa pregunta en la próxima ronda. |
| 5 | U06 reportó que estructurar STAR le resulta **más difícil** después de usar la app (4 → 2) | Usuarios (preguntas 2 y 6) | ❌ No. Sin comentario del usuario no se conoce la causa. Una hipótesis es que el análisis le mostró componentes que creía tener. Se documenta como resultado negativo. |
| 6 | Comentario: "un poco de más color" | Usuarios (pregunta 10) | ❌ No. El rediseño visual se hizo el mismo día, antes de las pruebas. |

---

## Resumen de métricas de validación

| Métrica | Resultado |
|---------|-----------|
| Usuarios externos que probaron el MVP | **8** (meta ≥ 5) |
| Usuarios que completaron la tarea sin ayuda | **5/6** (83%) |
| Usuarios que reportaron feedback útil | **7/7** "Muy útil" (1 en blanco) |
| Preparación promedio antes → después (1–5) | **2.6 → 3.6** |
| Usuarios que la usarían para una entrevista real | **8/8** |
| Casos límite probados | 5 (3 correctos · 1 mitigado · 1 limitación documentada) |
| Cambios al MVP derivados de las pruebas | **1 aplicado** (aviso de respuestas hipotéticas) · 1 propuesto |

> **Limitaciones:** n = 8 y muestra por conveniencia (contactos del equipo), con posible sesgo de complacencia. Las preguntas 7 y 9 solo tenían 2 opciones. Se mide la percepción inmediata, no el desempeño en una entrevista real.
