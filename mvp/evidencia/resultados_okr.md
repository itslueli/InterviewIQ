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

> Escala de preparación: 1 = Nada preparado/a · 5 = Muy preparado/a  
> Escala de dificultad STAR: 1 = Nada difícil · 5 = Muy difícil  
> KR1 y KR2: valores 1-2 = "poco/nada preparado" o "con dificultad"

| KR | Baseline | Meta | Pre-MVP | Post-MVP | Resultado | Cumple |
|----|----------|------|---------|----------|-----------|--------|
| KR1 | 60% | ≤ 40% | **71%** (5/7 con valor ≤ 2) | **29%** (2/7 con valor ≤ 2) | 71% → 29% | ✅ |
| KR2 | 80% | ≤ 55% | **57%** (4/7 con valor ≥ 4) | **29%** (2/7 con valor ≥ 4) | 57% → 29% | ✅ |
| KR3 | 40% | ≥ 90% | — | **100%** (7/7 recibieron feedback) | 100% | ✅ |

**Muestra:** 7 usuarios externos al equipo  
**Período de prueba:** 13 de noviembre de 2026  
**Instrumento:** Cuestionario pre/post (preguntas 1-3 pre, preguntas 5-6 post)

---

## Métricas técnicas del MVP

| Métrica | Meta PC1 | Resultado | Cumple |
|---------|----------|-----------|--------|
| F1 Macro promedio — clasificador STAR (A2) | ≥ 0.65 | **0.830** | ✅ |
| F1 componente S — Situación | ≥ 0.65 | **0.865** | ✅ |
| F1 componente T — Tarea | ≥ 0.65 | **0.822** | ✅ |
| F1 componente A — Acción | ≥ 0.65 | **0.804** | ✅ |
| F1 componente R — Resultado | ≥ 0.65 | **0.829** | ✅ |
| MVP con URL pública | Sí | https://interviewiq-utec.streamlit.app/ | ✅ |
| Feedback coherente con output A2 (Patrón 1) | Siempre | G1 siempre recibe output de A2 | ✅ |

---

## Análisis

**¿Qué funcionó?**  
El flujo completo fue completado de forma autónoma por 6 de 7 usuarios sin necesitar explicación. El feedback de Gemini fue calificado como "Muy útil" por todos los usuarios que respondieron esa pregunta. El 100% indicó que usaría la herramienta para prepararse para una entrevista real.

**¿Qué no alcanzó la meta?**  
Todos los KRs fueron cumplidos. Un usuario indicó que necesitó ayuda para usar la app.

**¿Qué cambiaría el equipo si tuviera más tiempo?**  
Según comentarios de usuarios: añadir más variedad de colores en la interfaz y ampliar el banco de preguntas por rol.

---

## Evidencia

| Evidencia | Ubicación |
|-----------|-----------|
| Registro de pruebas de usuario (7 usuarios) | `mvp/evidencia/pruebas_usuario.md` |
| Métricas del clasificador STAR | `plantillas/plantilla_4_scorecard_risk.md` |
| Notebook de entrenamiento | `notebooks/02_modelo_svm.ipynb` |
| URL del MVP | https://interviewiq-utec.streamlit.app/ |
