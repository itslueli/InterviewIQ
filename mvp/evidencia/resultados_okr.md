# Resultados OKR — InterviewIQ
## mvp/evidencia/resultados_okr.md

**Proyecto:** InterviewIQ  
**Curso:** AD5018 — Inteligencia Artificial para Negocios · UTEC 2026-2  
**Equipo:** Valeria Briceño · Lucía Rodríguez · Jennifer Patiño · Aaron Van Oord  
**MVP URL:** https://interviewiq-utec.streamlit.app/  

---

## OKR comprometido en PC1

**Objetivo:** Reducir la falta de preparación estructurada de estudiantes universitarios peruanos para entrevistas laborales por competencias, mediante práctica con retroalimentación automática basada en la metodología STAR.

| KR | Descripción | Baseline (encuesta propia, n=50) | Meta PC1 |
|----|-------------|----------------------------------|----------|
| KR1 | Reducir % de estudiantes que se sienten poco o nada preparados | 60% | ≤ 40% |
| KR2 | Reducir % con dificultad para estructurar respuestas conductuales | 80% | ≤ 55% |
| KR3 | Aumentar % que reciben feedback estructurado en al menos 1 sesión | 40% | ≥ 90% |

---

## Resultados reales (pruebas con usuarios externos)

Detalle por usuario y protocolo en `mvp/evidencia/pruebas_usuario.md`.

| KR | Baseline PC1 | Meta | Antes de usar la app | Después de usar la app | Cumple |
|----|----------|------|---------------|--------|--------|
| KR1 | 60% | ≤ 40% | 62.5% (5/8) | **25.0% (2/8)** | ✅ (indicativo) |
| KR2 | 80% | ≤ 55% | 33.3% (2/6) | **16.7% (1/6)** | ✅ (indicativo) |
| KR3 | 40% | ≥ 90% | 50.0% (4/8) | **87.5% (7/8)**, medido de forma indirecta | ⚠️ Cerca de la meta, sin pregunta directa |

**Muestra:** 8 estudiantes universitarios externos al equipo (meta: ≥ 5)  
**Período de prueba:** 09 de noviembre, hasta 13 noviembre de 2026
**Instrumento:** Google Form anónimo con preguntas antes y después del uso de la app (escala 1–5)

**Cómo se calculó cada KR**
- **KR1:** % que marca 1 o 2 en "¿Qué tan preparado/a te sientes para una entrevista laboral por competencias?" (1 = nada preparado/a), antes (pregunta 1) y después (pregunta 5).
- **KR2:** % que marca 1 o 2 en "¿Qué tan difícil te resulta estructurar tus respuestas en formato STAR?" (1 = muy difícil), antes (pregunta 2) y después (pregunta 6). Se usan los 6 usuarios que respondieron ambas, porque las 2 primeras respuestas se recogieron con una versión del formulario que no tenía la pregunta 6. Con los 8 usuarios, el "antes" es 50%.
- **KR3:** antes = % que recibe feedback estructurado "a veces" o más (3 a 5 en la pregunta 3). Después: el formulario no incluyó la pregunta directa "¿Recibiste feedback?". Como indicador indirecto, 7 de 8 usuarios calificaron el feedback que recibieron (todos "Muy útil") y 1 dejó la pregunta en blanco.

---

## Indicadores complementarios de uso

| Indicador | Resultado |
|-----------|-----------|
| Preparación promedio (1–5), antes → después | 2.6 → 3.6 |
| Usuarios que mejoraron / se mantuvieron / empeoraron en preparación | 5 / 3 / 0 |
| Facilidad STAR promedio (1–5), antes → después (n = 6) | 3.0 → 3.7 |
| Completaron la tarea sin ayuda | 83% (5/6) |
| Facilidad para entender el análisis STAR (1–5) | 3.6 |
| ¿La usarían para una entrevista real? | 8/8 "Definitivamente sí" |

---

## Métricas técnicas del MVP

| Métrica | Meta PC1 | Resultado | Cumple |
|---------|----------|-----------|--------|
| F1 Macro promedio — clasificador STAR (A2) | ≥ 0.65 | **0.808** | ✅ |
| F1 componente S — Situación | ≥ 0.65 | **0.865** | ✅ |
| F1 componente T — Tarea | ≥ 0.65 | **0.822** | ✅ |
| F1 componente A — Acción | ≥ 0.65 | **0.804** | ✅ |
| F1 componente R — Resultado | ≥ 0.65 | **0.829** | ✅ |
| MVP con URL pública | Sí | https://interviewiq-utec.streamlit.app/ | ✅ |
| Feedback coherente con el output de A2 (patrón 1: modelo → lenguaje) | ≥ 90% en 20 casos | **100%** (20/20 casos — feedback por reglas) | ✅ |

> ⚠️ Los F1 de esta tabla se calcularon con el umbral de Resultado ajustado a 0.50 (vigente en la app).

> La capa de lenguaje es **G1** (LLM con contexto fijo, Google Gemini). El equipo bajó formalmente de G2 (RAG) a G1; ver Plantilla 3.

---

## Análisis

**¿Qué funcionó?**  
- El MVP cumple el ciclo completo con usuarios reales: 8 estudiantes externos lo usaron desde su propio dispositivo y 5 de los 6 consultados lo usaron sin ayuda.
- KR1 y KR2 superan la meta: después de una sesión, el % de estudiantes que se sienten poco o nada preparados bajó de 62.5% a 25%, y ningún usuario reportó sentirse menos preparado.
- El clasificador STAR supera la meta técnica en los 4 componentes, y el feedback fue valorado como "Muy útil" por todos los que respondieron.

**¿Qué no alcanzó la meta?**  
- **KR3 no se midió de forma directa** porque el formulario no incluyó la pregunta "¿Recibiste feedback?". La evidencia indirecta (87.5%) está cerca, pero no basta para decir que se cumple la meta de ≥ 90%.
- La **comprensión del análisis STAR** es el punto más débil (3.6/5): las tarjetas muestran valores técnicos (probabilidad y umbral) que un estudiante no sabe interpretar.
- Un usuario (U06) reportó que estructurar STAR le resulta más difícil después de usar la app (de 4 a 2).

**Limitaciones de la medición**  
- n = 8, muestra por conveniencia (contactos del equipo), con posible sesgo de complacencia: 8/8 respondieron "Definitivamente sí" en una pregunta de solo 2 opciones. El resultado es **indicativo, no estadísticamente concluyente**.
- La muestra tenía menos dificultad inicial que la encuesta de PC1 en KR2 (50% vs. 80%). Parte del cumplimiento se explica por la muestra, no solo por la app.
- Es una medición inmediata y autorreportada: no muestra si el estudiante rinde mejor en una entrevista real.

**¿Qué cambiaría el equipo si tuviera más tiempo?**  
- Repetir la prueba con 15 o más usuarios no conocidos, con la pregunta directa de KR3, escalas de 1 a 5 en todas las preguntas, y una pregunta sobre en qué necesitaron ayuda.
- Reemplazar los valores técnicos de las tarjetas STAR por explicaciones simples.
- Ampliar el dataset con más ejemplos de "Resultado" (solo 38% de las respuestas tienen R = 1) para corregir los falsos negativos con resultados cortos.
- Recuperar la Etapa 1 (cuestionario diagnóstico y nivel) y el RAG (G2), que quedaron fuera del MVP.

---

## Evidencia

| Evidencia | Ubicación |
|-----------|-----------|
| Registro de pruebas de usuario (8 usuarios + 5 casos límite) | `mvp/evidencia/pruebas_usuario.md` |
| Métricas del clasificador STAR | `plantillas/plantilla_4_scorecard_risk.md` |
| Notebook de entrenamiento | `notebooks/` |
| URL del MVP | https://interviewiq-utec.streamlit.app/ |
