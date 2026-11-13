# Plantilla 4 — Scorecard de Resultados y Análisis de Riesgos

**Proyecto:** InterviewIQ  
**Curso:** AD5018 — Inteligencia Artificial para Negocios · UTEC 2026-2  
**Equipo:** Lucía Rodríguez · Valeria Briceño · Jennifer Patiño · Aaron Van Oord  
**Semana de evaluación:** 14 (PC2)

---

## Parte A — Métricas de impacto (Fase P2)

### A1. OKRs comprometidos en PC1 vs resultados reales

| KR | Descripción | Meta PC1 | Resultado real | Cumple |
|----|-------------|----------|---------------|--------|
| KR1 | Reducir tasa de respuestas sin estructura STAR de estudiantes que usan InterviewIQ | 60% → ≤40% | Pendiente validación con usuarios reales | 🔄 En medición |
| KR2 | Reducir respuestas que omiten el componente "Resultado" (R) | 80% → ≤55% | Pendiente validación con usuarios reales | 🔄 En medición |
| KR3 | Aumentar respuestas con los 4 componentes STAR presentes | 40% → ≥90% de usuarios que completan el flujo | Pendiente validación con usuarios reales | 🔄 En medición |

> Los KRs se medirán con las pruebas de usuario documentadas en `mvp/evidencia/pruebas_usuario.md`. El modelo ya está entrenado y desplegado; los datos de impacto real se registran en la semana de sustentación.

---

### A2. Métricas del Componente Analítico (A2 — Clasificador STAR)

**Modelo seleccionado:** TF-IDF bigramas + Linear SVM (CalibratedClassifierCV)  
**Dataset:** `interviewiq_star_v1.csv` — 200 pares etiquetados (sintético)  
**Split:** 70% entrenamiento / 10% validación / 20% prueba  
**Vectorizador:** TF-IDF, bigramas, max_features=5000, sublinear_tf=True

#### Resultados en set de prueba (con umbrales ajustados)

| Componente | F1 Macro | Falsos Positivos | Falsos Negativos | Umbral | Criterio ≥0.65 |
|------------|----------|-----------------|-----------------|--------|----------------|
| S — Situación | **0.865** | 4 (25.0%) | 1 | 0.30 | ✅ CUMPLE |
| T — Tarea | **0.822** | 7 (33.3%) | 0 | 0.30 | ✅ CUMPLE |
| A — Acción | **0.804** | 1 (9.1%) | 6 | 0.75 | ✅ CUMPLE |
| R — Resultado | **0.829** | 2 (7.7%) | 4 | 0.70 | ✅ CUMPLE |
| **PROMEDIO** | **0.830** | — | — | — | ✅ CUMPLE |

#### Comparación baseline vs modelo final

| Componente | LR Baseline F1 | SVM Final F1 | Ganador |
|------------|---------------|-------------|---------|
| S — Situación | 0.840 | **0.896** | SVM ✓ |
| T — Tarea | 0.874 | **0.900** | SVM ✓ |
| A — Acción | 0.881 | 0.881 | LR ~ |
| R — Resultado | 0.774 | **0.868** | SVM ✓ |
| **Promedio** | 0.842 | **0.886** | **SVM** |

> El modelo supera su baseline en 3 de 4 componentes. F1 promedio final: **0.830** (con umbrales ajustados para minimizar Falsos Positivos).

#### Lectura en costos de negocio

El error más costoso en InterviewIQ es el **Falso Positivo**: decirle al estudiante que un componente STAR está presente cuando no lo está genera feedback incorrecto y daña la confianza en la herramienta.

| Componente | Tasa FP (umbral ajustado) | Riesgo | Acción tomada |
|------------|--------------------------|--------|---------------|
| S — Situación | 25.0% | 🔴 Alto | Umbral 0.30 |
| T — Tarea | 33.3% | 🔴 Alto | Umbral 0.30 |
| A — Acción | 9.1% | 🟢 Bajo | Umbral 0.75 |
| R — Resultado | 7.7% | 🟢 Bajo | Umbral 0.70 |

> Los umbrales fueron ajustados en el set de validación usando scoring combinado: maximizar F1 y penalizar tasa FP (puntuación = F1 − 0.5 × tasa_FP).

---

### A3. Métrica del Componente Generativo (G2 — Feedback por reglas)

**Nivel declarado en PC1:** G2 (RAG)  
**Implementación en MVP:** Feedback basado en reglas estructuradas (G1). El RAG completo quedó fuera del alcance del MVP por restricciones de tiempo y dependencia de API key del usuario.

| Métrica | Meta PC1 | Resultado | Cumple |
|---------|----------|-----------|--------|
| Feedback coherente con output A2 | Patrón 1 siempre activo | ✅ G2 siempre recibe output de A2 | ✅ |
| Latencia de respuesta | < 5 seg | ~1-2 seg (modo reglas) | ✅ |

> **Decisión documentada:** El MVP usa feedback basado en reglas por defecto para garantizar disponibilidad sin depender de API key ni servicios externos. La Etapa 1 de clasificación de nivel de preparación también quedó fuera del MVP actual.

---

## Parte B — Riesgos, ética y regulación (Fase T)

### B1. Matriz de riesgos

#### Riesgos del Componente Analítico (modelo)

| # | Riesgo | Probabilidad | Impacto | Nivel | Mitigación concreta |
|---|--------|-------------|---------|-------|---------------------|
| R1 | El modelo clasifica incorrectamente una respuesta real como STAR completa (Falso Positivo) | Alta | Alto | 🔴 Crítico | Ajuste de umbrales por componente en validación. Umbral acción=0.75, resultado=0.70 para ser conservador. Se muestra la probabilidad numérica al usuario para que evalúe. |
| R2 | Dataset sintético no representa la variedad real de respuestas (sesgo de distribución) | Media | Alto | 🟡 Moderado | 200 ejemplos sintéticos son el punto de partida. Se planifica re-entrenamiento con datos reales post-lanzamiento. Las pruebas de usuario (≥5 personas) validarán el comportamiento con texto real. |
| R3 | Degradación del modelo en respuestas muy cortas (<15 palabras) | Alta | Medio | 🟡 Moderado | La app advierte al usuario si la respuesta tiene menos de 20 palabras. El modelo muestra confianza baja para respuestas cortas. |

#### Riesgos de la Capa de Lenguaje (G2)

| # | Riesgo | Probabilidad | Impacto | Nivel | Mitigación concreta |
|---|--------|-------------|---------|-------|---------------------|
| R4 | El feedback basado en reglas no conecta con el contexto específico del usuario | Media | Medio | 🟡 Moderado | El sistema de reglas está diseñado por componente STAR: cada combinación de presentes/ausentes produce un mensaje diferente. Se testea con 5+ respuestas reales antes de la sustentación. |
| R5 | El modelo genera feedback que el estudiante interpreta como garantía de éxito en entrevista real | Baja | Alto | 🟡 Moderado | La interfaz incluye disclaimer visible: "InterviewIQ es una herramienta de práctica, no una evaluación oficial." |

#### Riesgo de acción no deseada (aplica si se agrega agente)

| # | Riesgo | Probabilidad | Impacto | Nivel | Mitigación concreta |
|---|--------|-------------|---------|-------|---------------------|
| R6 | Si se implementa agente n8n: el agente registra datos de usuarios sin consentimiento explícito | Baja | Crítico | 🔴 Crítico | Se solicitará consentimiento explícito antes del registro. Los datos se anonimizarán. Aplica Ley N.° 29733. |

---

### B2. Ética y regulación

#### Regulación aplicable

**Ley N.° 29733 — Ley de Protección de Datos Personales del Perú**

InterviewIQ procesa respuestas de texto libre que pueden contener información personal del usuario (experiencias laborales, situaciones académicas). Se aplica la ley porque:

1. Las respuestas del usuario son datos personales según el Art. 2 de la Ley.
2. El procesamiento de estas respuestas requiere consentimiento informado (Art. 13).

**Cómo InterviewIQ cumple la Ley N.° 29733:**

| Obligación legal | Implementación en InterviewIQ |
|-----------------|-------------------------------|
| Consentimiento informado (Art. 13) | La app muestra aviso visible antes del análisis: "Tus respuestas se procesan para darte feedback. No se almacenan." |
| Finalidad específica (Art. 8) | Los datos se usan exclusivamente para clasificación STAR. No se envían a terceros. |
| No almacenamiento sin consentimiento | El MVP no persiste respuestas del usuario. Streamlit no guarda texto entre sesiones. |
| Seguridad (Art. 16) | La comunicación es HTTPS (Streamlit Community Cloud). No hay base de datos con datos personales. |

#### Declaración de transparencia del MVP

El MVP informa visiblemente al usuario que está interactuando con IA mediante:
- Encabezado: "InterviewIQ — Análisis con IA"
- Disclaimer en la sección de feedback: "Este análisis es generado automáticamente por un modelo de IA entrenado con datos sintéticos."

---

### B3. Respuesta a "¿qué pasa si la IA se equivoca?"

| Escenario | Qué puede pasar | Cómo lo manejamos |
|-----------|----------------|-------------------|
| El modelo dice que falta Situación, pero sí estaba presente (FN) | El estudiante recibe feedback innecesario sobre cómo añadir contexto | El feedback de FN es constructivo y no dañino: en el peor caso el estudiante aprende algo extra. |
| El modelo dice que la Acción está presente, pero no lo estaba (FP) | El estudiante no recibe el consejo correcto sobre qué mejorar | Se minimiza con umbral 0.75 para Acción. Las probabilidades se muestran para que el usuario las evalúe. |
| El MVP no está disponible el día de la sustentación | El evaluador no puede acceder | El deploy está en Streamlit Community Cloud (SLA 99.9%). Se tiene screenshot de demostración como respaldo. |

---

### B4. Archivos generados por el modelo

| Archivo | Descripción | Ubicación en repo |
|---------|-------------|------------------|
| `clasificador_star_situacion.pkl` | Modelo SVM para componente S | `models/` |
| `clasificador_star_tarea.pkl` | Modelo SVM para componente T | `models/` |
| `clasificador_star_accion.pkl` | Modelo SVM para componente A | `models/` |
| `clasificador_star_resultado.pkl` | Modelo SVM para componente R | `models/` |
| `config_clasificador.json` | Umbrales óptimos y metadata del modelo | `models/` |
| `interviewiq_star_v1.csv` | Dataset de entrenamiento (200 filas) | `data/raw/` |
