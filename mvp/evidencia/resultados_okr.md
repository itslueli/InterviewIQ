# Resultados OKR — InterviewIQ
## mvp/evidencia/resultados_okr.md

**Proyecto:** InterviewIQ  
**Curso:** AD5018 — Inteligencia Artificial para Negocios · UTEC 2026-2  
**Equipo:** Valeria Briceño · Lucía Rodríguez · Aaron Van Oord  
**MVP URL:** *(pegar URL de Streamlit aquí)*  
**Fecha de medición:** Noviembre 2026

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

> Completar con los datos reales de las pruebas de usuario. Ver protocolo completo en `mvp/evidencia/pruebas_usuario.md`.

| KR | Baseline | Meta | Resultado real | Cumple |
|----|----------|------|---------------|--------|
| KR1 | 60% | ≤ 40% | ___% | ☐ |
| KR2 | 80% | ≤ 55% | ___% | ☐ |
| KR3 | 40% | ≥ 90% | ___% | ☐ |

**Muestra:** ___ usuarios externos al equipo (meta: ≥ 5)  
**Período de prueba:** Noviembre 2026  
**Instrumento:** Cuestionario pre/post aplicado a cada usuario (mismas preguntas del baseline original)

---

## Métricas técnicas del MVP (ya disponibles)

| Métrica | Meta PC1 | Resultado | Cumple |
|---------|----------|-----------|--------|
| F1 Macro promedio — clasificador STAR (A2) | ≥ 0.65 | **0.830** | ✅ |
| F1 componente S — Situación | ≥ 0.65 | **0.865** | ✅ |
| F1 componente T — Tarea | ≥ 0.65 | **0.822** | ✅ |
| F1 componente A — Acción | ≥ 0.65 | **0.804** | ✅ |
| F1 componente R — Resultado | ≥ 0.65 | **0.829** | ✅ |
| MVP con URL pública | Sí | *(pendiente deploy)* | 🔄 |
| Feedback coherente con output A2 (Patrón 1) | Siempre | ✅ G2 siempre recibe output de A2 | ✅ |

---

## Análisis

*(Completar después de las pruebas de usuario)*

**¿Qué funcionó?**  
_

**¿Qué no alcanzó la meta?**  
_

**¿Qué cambiaría el equipo si tuviera más tiempo?**  
_

---

## Evidencia

| Evidencia | Ubicación |
|-----------|-----------|
| Registro de pruebas de usuario (5 usuarios) | `mvp/evidencia/pruebas_usuario.md` |
| Métricas del clasificador STAR | `plantillas/plantilla_4_scorecard_risk.md` |
| Notebook de entrenamiento (output) | Adjunto en sustentación |
| URL del MVP | *(pegar aquí)* |
