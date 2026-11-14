# Resumen Ejecutivo — InterviewIQ
## AD5018 Inteligencia Artificial para Negocios | UTEC 2026-2

**Equipo:** Lucía Rodríguez · Valeria Briceño · Jennifer Patiño · Aaron Van Oord  
**MVP activo:** https://interviewiq-utec.streamlit.app/  
**Semana de evaluación:** 14 (PC2) — Noviembre 2026

---

## Problema

Los estudiantes universitarios peruanos de últimos ciclos tienen dificultad para preparar y mejorar sus respuestas en entrevistas laborales por competencias porque cuentan con oportunidades limitadas de práctica recurrente con retroalimentación estructurada, lo que genera bajos niveles de preparación percibida y dificultades para estructurar respuestas conductuales.

El contexto nacional agrava el problema: **14.3% de desempleo juvenil** (INEI, 2024), 7 de cada 10 jóvenes en situación de inadecuación ocupacional (MTPE, 2024) y 60.8% de empresas que no encuentra trabajadores con las habilidades requeridas (INEI ENE, 2020).

Una encuesta propia a 50 estudiantes universitarios de últimos ciclos confirma la escala del problema:

| Indicador | Resultado |
|-----------|-----------|
| Se sienten poco o nada preparados para entrevistas | **60%** |
| Reportan dificultad para estructurar respuestas conductuales | **80%** |
| Rara vez reciben retroalimentación estructurada al practicar | **40%** |

La solución existente —prepararse con un coach o practicar con compañeros— es costosa, poco recurrente y no escalable. InterviewIQ propone automatizar el ciclo de práctica y retroalimentación.

---

## Usuario objetivo

**Segmento principal:** Estudiantes universitarios peruanos de 8.° a 10.° ciclo que buscan prácticas preprofesionales o su primer empleo formal, sin acceso a coaching profesional de entrevistas.

**Pain points específicos:**
- No saben qué componentes STAR falta en su respuesta
- No reciben feedback inmediato al practicar solos
- El feedback de compañeros es inconsistente y subjetivo

---

## Propuesta de valor

**InterviewIQ** es un simulador de entrevistas por competencias que usa IA para detectar automáticamente la estructura STAR en las respuestas del usuario y generar feedback personalizado para mejorarlas.

**Flujo del MVP:**

```
1. Selecciona una pregunta conductual del banco
2. Escribe tu respuesta en texto libre
3. El clasificador STAR detecta S / T / A / R presentes o ausentes
4. Gemini 2.5 Flash genera feedback contextualizado
5. El estudiante corrige y vuelve a intentarlo
```

**Qué NO hace el MVP (scope delimitado):**
- No clasifica el nivel de preparación del usuario (Etapa 1 fuera de scope)
- No guarda historial entre sesiones
- No genera preguntas adaptativas según el nivel

---

## Datasets

| Recurso | Descripción | Tamaño | Estado |
|---------|-------------|--------|--------|
| **R1 — Cuestionario diagnóstico** | Encuesta pre/post sobre preparación para entrevistas (instrumento de medición de OKRs) | 50 estudiantes (baseline) | ✅ Construido |
| **R2 — InterviewIQ-STAR** | Pares (pregunta conductual, respuesta, etiquetas S/T/A/R = 0/1) | 200 filas | ✅ Construido — `data/raw/interviewiq_star_v1.csv` |

**Esquema R2:**
```
id, pregunta, respuesta, situacion, tarea, accion, resultado, fuente
```
Split: 70% entrenamiento / 10% validación / 20% prueba.

---

## Componente Analítico (A2) — Clasificador STAR

**Tarea:** Clasificación multilabel independiente por componente STAR (4 clasificadores binarios).  
**Comparación:** TF-IDF + Logistic Regression (baseline) vs TF-IDF + Linear SVM (modelo final).  
**Criterio de selección:** F1 Macro ≥ 0.65 por componente, minimizando Falsos Positivos.

**Modelo seleccionado: TF-IDF bigramas + Linear SVM (CalibratedClassifierCV)**

| Componente | LR Baseline F1 | SVM Final F1 | Umbral ajustado | Criterio ≥ 0.65 |
|------------|---------------|-------------|----------------|----------------|
| S — Situación | 0.840 | **0.865** | 0.30 | ✅ CUMPLE |
| T — Tarea | 0.874 | **0.822** | 0.30 | ✅ CUMPLE |
| A — Acción | 0.881 | **0.804** | 0.75 | ✅ CUMPLE |
| R — Resultado | 0.774 | **0.829** | 0.50* | ✅ CUMPLE |
| **Promedio** | 0.842 | **0.830** | — | ✅ CUMPLE |

> \* El F1 de R se calculó con umbral 0.70; el umbral vigente es 0.50 (ajustado tras pruebas internas). Recalcular en el notebook.

> Los umbrales fueron ajustados en validación usando: `score = F1 − 0.5 × tasa_FP`. El error más costoso en este dominio es el Falso Positivo (decirle al usuario que un componente está presente cuando no lo está).

---

## Componente Generativo (G1) — Feedback con IA

**Implementación:** Gemini 2.5 Flash vía API REST (`requests`). El componente G1 siempre recibe el output del clasificador A2 antes de generar feedback (Patrón 1 activo).

**Input al modelo:** pregunta conductual + respuesta del usuario + componentes detectados (S/T/A/R presentes/ausentes con probabilidad)  
**Output:** párrafo de feedback contextualizado con orientación específica por componente ausente

**Fallback:** Reglas estructuradas por combinación de componentes (activo cuando no hay API key). Garantiza disponibilidad del MVP sin depender de servicios externos.

| Modo | Latencia aprox. | Disponibilidad |
|------|----------------|---------------|
| Gemini 2.5 Flash | Pocos segundos (no medido formalmente) | Requiere `GEMINI_API_KEY` en Streamlit secrets |
| Fallback (reglas) | < 0.5 seg | Siempre disponible |

**Nota de scope:** El pipeline RAG completo (GPT-4o-mini + ChromaDB + corpus de entrevistas) quedó fuera del MVP por restricciones de tiempo. Documentado en la Plantilla 3 (nota de versión final) y como deuda técnica en la Plantilla 4 (sección B5).

---

## Producto (MVP)

Interfaz web Streamlit desplegada en Streamlit Community Cloud. Diseño de dos páginas:

- **Landing:** presentación del producto, propuesta de valor, botón de inicio
- **Análisis:** selección de pregunta → respuesta → análisis STAR con gauge de score (0–4) → feedback estructurado

Sin autenticación ni base de datos persistente. Las respuestas del usuario no se almacenan.

**URL del MVP:** https://interviewiq-utec.streamlit.app/  
**Repositorio:** https://github.com/itslueli/InterviewIQ

---

## Impacto esperado y medición

| KR | Baseline (n=50) | Meta con MVP | Resultado real (n=8) | Cumple |
|----|----------------|-------------|----------------------|--------|
| KR1 — Estudiantes poco/nada preparados | 60% | ≤ 40% | 62.5% → **25%** (−37.5 pp) | ✅ (indicativo) |
| KR2 — Dificultad para estructurar respuestas STAR | 80% | ≤ 55% | 33% → **17%** (n=6) | ✅ (indicativo) |
| KR3 — Reciben feedback estructurado en ≥ 1 sesión | 40% | ≥ 90% | 50% → **87.5%** (indirecto) | ⚠️ Cerca de la meta |

> Muestra pequeña y por conveniencia: los resultados son indicativos, no estadísticamente concluyentes. KR3 se midió de forma indirecta porque el formulario no incluyó la pregunta "¿Recibiste feedback?".

**Instrumento de medición:** Cuestionario pre/post (Google Forms, anónimo) aplicado a 8 usuarios externos al equipo.  
**Protocolo completo:** `mvp/evidencia/pruebas_usuario.md`  
**Resultados:** `mvp/evidencia/resultados_okr.md`

---

## Estado del stack PC2

| Componente | Estado |
|------------|--------|
| Dataset R2 (200 filas etiquetadas) | ✅ Construido |
| Modelos entrenados y guardados (`models/`) | ✅ Listo |
| App Streamlit (app.py) | ✅ Funcional |
| Deploy en Streamlit Community Cloud | ✅ Activo — https://interviewiq-utec.streamlit.app/ |
| Pruebas con ≥ 5 usuarios reales | ✅ Completado — 8 usuarios externos + 5 casos límite internos |
| Resultados OKR finales | ✅ Medidos — KR1 y KR2 cumplidos; KR3 cerca de la meta (indirecto) |
