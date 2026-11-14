# InterviewIQ — Simulador Inteligente de Entrevistas por Competencias

**AD5018 Inteligencia Artificial para Negocios · UTEC 2026-2**  
**Equipo:** Valeria Briceño · Lucía Rodríguez · Jennifer Patiño · Aaron Van Oord

---

## ¿Qué es InterviewIQ?

InterviewIQ es un simulador de entrevistas por competencias diseñado para estudiantes universitarios peruanos de últimos ciclos que buscan prácticas preprofesionales o su primer empleo. Permite practicar entrevistas conductuales de manera recurrente y recibir retroalimentación estructurada sobre la calidad de sus respuestas, sin depender de la disponibilidad de un entrevistador humano.

El sistema detecta automáticamente qué componentes de la metodología STAR (Situación, Tarea, Acción, Resultado) están presentes o ausentes en cada respuesta, y genera feedback personalizado para mejorarla.

**MVP activo:** https://interviewiq-utec.streamlit.app/

---

## Problema que resuelve

Los estudiantes universitarios peruanos de últimos ciclos tienen dificultad para preparar y mejorar sus respuestas en entrevistas laborales por competencias porque cuentan con oportunidades limitadas de práctica recurrente con retroalimentación estructurada.

Una encuesta propia a 50 estudiantes universitarios confirma la escala del problema:

| Indicador | Resultado |
|-----------|-----------|
| Se sienten poco o nada preparados para entrevistas | **60%** |
| Reportan dificultad para estructurar respuestas conductuales | **80%** |
| Rara vez reciben retroalimentación estructurada al practicar | **40%** |

Contexto nacional: 14.3% de desempleo juvenil (INEI, 2024), 7 de cada 10 jóvenes en situación de inadecuación ocupacional (MTPE, 2024).

---

## Arquitectura del sistema

El MVP integra dos componentes principales: un clasificador STAR (A2) y un generador de feedback con IA (G1).

```
[Selección de pregunta conductual]
         ↓
[Respuesta en texto libre del usuario]
         ↓
[Clasificador STAR — A2 (TF-IDF + Linear SVM)]
  → Detecta S / T / A / R presentes o ausentes
  → Calcula probabilidad por componente
         ↓
[Componente Generativo — G1 (Gemini 2.5 Flash)]
  → Recibe: pregunta + respuesta + componentes detectados
  → Genera feedback contextualizado
  → Fallback a reglas estructuradas si no hay API key
         ↓
[Feedback estructurado mostrado al estudiante]
```

---

## Componentes

| Componente | Descripción | Tecnología |
|------------|-------------|------------|
| Clasificador STAR (A2) | Clasificación multilabel (S/T/A/R = 0 ó 1) por etiqueta. Compara TF-IDF + LR (baseline) vs TF-IDF + Linear SVM (modelo final). Umbrales ajustados por componente. | scikit-learn |
| Componente Generativo (G1) | Gemini 2.5 Flash vía API REST. Recibe la pregunta, respuesta y componentes detectados, genera feedback contextualizado. Fallback a reglas estructuradas. | requests + Gemini API |
| Interfaz | Aplicación web: selección de pregunta → respuesta en texto libre → análisis STAR → feedback | Streamlit |

---

## Dataset

| Recurso | Descripción | Estado |
|---------|-------------|--------|
| **R1 — Cuestionario diagnóstico** | Encuesta a 50 estudiantes sobre preparación para entrevistas (baseline OKRs) | ✅ Construido |
| **R2 — InterviewIQ-STAR** | 200 pares (pregunta conductual, respuesta, etiquetas S/T/A/R = 0/1) construidos por el equipo con respuestas sintéticas y reales | ✅ Construido — `data/raw/interviewiq_star_v1.csv` |

### Esquema de R2 — InterviewIQ-STAR

```
id, pregunta, respuesta, situacion, tarea, accion, resultado, fuente
```

- `situacion`, `tarea`, `accion`, `resultado` ∈ {0, 1}
- `fuente` ∈ {sintético, real}
- Split: 70% entrenamiento / 10% validación / 20% prueba

---

## Métricas del modelo (A2)

**Modelo seleccionado:** TF-IDF bigramas + Linear SVM (CalibratedClassifierCV)  
**Vectorizador:** TF-IDF, bigramas, max_features=5000, sublinear_tf=True

| Componente | F1 Macro | Umbral | Criterio ≥ 0.65 |
|------------|----------|--------|----------------|
| S — Situación | **0.865** | 0.30 | ✅ CUMPLE |
| T — Tarea | **0.822** | 0.30 | ✅ CUMPLE |
| A — Acción | **0.804** | 0.75 | ✅ CUMPLE |
| R — Resultado | **0.829** | 0.50 | ✅ CUMPLE |
| **Promedio** | **0.808** | — | ✅ CUMPLE |

#### Comparación baseline vs modelo final

| Componente | LR Baseline F1 | SVM Final F1 | Ganador |
|------------|---------------|-------------|---------|
| S — Situación | 0.840 | **0.896** | SVM ✓ |
| T — Tarea | 0.874 | **0.900** | SVM ✓ |
| A — Acción | 0.881 | 0.881 | Empate |
| R — Resultado | 0.774 | **0.868** | SVM ✓ |
| **Promedio** | 0.842 | **0.851** | **SVM** |

> Los umbrales fueron ajustados en validación priorizando minimizar Falsos Positivos (el error más costoso en este dominio: decirle al estudiante que un componente está presente cuando no lo está).

---

## Impacto medido (OKRs) — n=8 usuarios externos

| KR | Baseline | Meta | Resultado (pre→post) | Estado |
|----|----------|------|----------------------|--------|
| KR1 — Estudiantes poco/nada preparados para entrevistas | 60% | ≤ 40% | **62.5% → 25%** | ✅ Cumplido |
| KR2 — Estudiantes con dificultad para estructurar respuestas STAR | 80% | ≤ 55% | **37.5% → 25%** | ✅ Cumplido |
| KR3 — Estudiantes que rara vez reciben feedback estructurado | 40% | ≥ 90% reciben ≥ 1 sesión | **87.5%** (7/8 recibieron feedback) | ✅ Cumplido |

Medición: cuestionario pre/post aplicado a 8 usuarios externos al equipo. Los 3 KRs fueron cumplidos.

---

## Estructura del repositorio

```
InterviewIQ/
├── README.md                              # Este archivo
├── resumen_ejecutivo.md                   # Resumen ejecutivo del proyecto
├── app.py                                 # Aplicación Streamlit (MVP)
├── requirements.txt                       # Dependencias Python
│
├── models/                                # Modelos entrenados
│   ├── clasificador_star_situacion.pkl
│   ├── clasificador_star_tarea.pkl
│   ├── clasificador_star_accion.pkl
│   ├── clasificador_star_resultado.pkl
│   └── config_clasificador.json           # Umbrales óptimos por componente
│
├── data/
│   └── raw/
│       └── interviewiq_star_v1.csv        # Dataset R2 — 200 pares etiquetados
│
├── notebooks/                             # Notebooks de entrenamiento
│   ├── 01_baseline_tfidf_lr.ipynb         # Baseline: TF-IDF + Logistic Regression
│   └── 02_modelo_svm.ipynb                # Modelo final: TF-IDF + Linear SVM
│
├── plantillas/                            # Plantillas del curso AD5018
│   ├── plantilla_1_problem_solution.md
│   ├── plantilla_2_mvp_scope.md
│   ├── plantilla_3_technical_decisions.md
│   └── plantilla_4_scorecard_risk.md
│
└── mvp/
    ├── README_mvp.md                      # Instrucciones para el evaluador
    └── evidencia/
        ├── pruebas_usuario.md             # Registro de pruebas con ≥5 usuarios reales
        └── resultados_okr.md             # Resultados KR1, KR2, KR3
```

---

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Clasificador STAR (A2) | Python 3.10 · scikit-learn (TF-IDF + LinearSVC + CalibratedClassifierCV) |
| Componente Generativo (G1) | Gemini 2.5 Flash · API REST vía `requests` |
| Interfaz | Streamlit |
| Deploy | Streamlit Community Cloud |

---

## Cómo usar el MVP

1. Abre **https://interviewiq-utec.streamlit.app/**
2. Elige una pregunta de entrevista conductual del menú
3. Escribe tu respuesta en el cuadro de texto (mínimo 20 palabras)
4. Presiona **"Analizar respuesta →"**
5. Revisa el análisis STAR (componentes presentes/ausentes con probabilidad) y el feedback

No se requiere cuenta, instalación ni configuración adicional.

---

## Decisiones técnicas relevantes

| Decisión | Alternativa descartada | Razón |
|----------|----------------------|-------|
| Linear SVM como clasificador final | Logistic Regression (baseline) | SVM supera baseline en F1 en 3 de 4 componentes |
| Umbrales ajustados por componente | Umbral fijo 0.5 | Minimizar Falsos Positivos es prioritario en este dominio |
| Gemini 2.5 Flash vía API REST | RAG con GPT-4o-mini + ChromaDB | RAG fuera del alcance del MVP por restricciones de tiempo; fallback a reglas garantiza disponibilidad |
| Streamlit | FastAPI + frontend custom | Velocidad de desarrollo para MVP académico |

Ver detalle en `plantillas/plantilla_3_technical_decisions.md`.

---

## Consideraciones éticas y legales

- Las respuestas de usuarios se procesan solo para generar feedback. **No se almacenan** entre sesiones (Streamlit no persiste estado).
- Cumplimiento de **Ley N.° 29733** (Protección de Datos Personales del Perú): aviso visible en la app, finalidad específica, comunicación HTTPS.
- El dataset R2 fue construido con respuestas sintéticas; las respuestas reales recolectadas en pruebas de usuario son anonimizadas.
- La app incluye disclaimer visible: *"InterviewIQ es una herramienta de práctica, no una evaluación oficial."*

---

## Tabla de contribuciones

| Componente | Lucía | Valeria | Jennifer | Aaron |
|------------|-------|---------|----------|-------|
| Dataset R2 (200 pares etiquetados) | | | ✓ | |
| Entrenamiento y evaluación modelo A2 | | | ✓ | |
| App Streamlit (app.py) | ✓ | | | |
| Deploy en Streamlit Community Cloud | ✓ | | | |
| Pruebas con usuarios reales | ✓ | | | ✓ |
| Documentación (plantillas 1-4) | | ✓ | | |
| Resumen ejecutivo | | ✓ | | |
| Presentación PC2 | | | | ✓ |
| Métricas y análisis del modelo | | | ✓ | |
| OKRs y medición de impacto |  |✓ | | |
