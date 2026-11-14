# Plantilla 4 — Scorecard de Resultados y Análisis de Riesgos

**Proyecto:** InterviewIQ  
**Curso:** AD5018 — Inteligencia Artificial para Negocios · UTEC 2026-2  
**Equipo:** Lucía Rodríguez · Valeria Briceño · Jennifer Patiño · Aaron Van Oord  
**Fecha:** Noviembre 2026  
**Semana de evaluación:** 14 (PC2)

---

## Parte A — Métricas de impacto (Fase P2)

### A1. OKRs comprometidos en PC1 vs resultados reales

**Objetivo:** Reducir la falta de preparación estructurada de estudiantes universitarios peruanos para entrevistas laborales por competencias, mediante práctica con retroalimentación automática basada en la metodología STAR.

| KR | Descripción | Meta PC1 | Pre (inicio) | Post (tras MVP) | Delta | Cumple |
|----|-------------|----------|-------------|----------------|-------|--------|
| KR1 | Reducir % de estudiantes que se sienten poco o nada preparados para entrevistas (baseline: 60%) | ≤ 40% | 62.5% (5/8) | **25.0%** (2/8) | −37.5 pp | ✅ (indicativo) |
| KR2 | Reducir % con dificultad para estructurar respuestas conductuales (baseline: 80%) | ≤ 55% | 33.3% (2/6) | **16.7%** (1/6) | −16.7 pp | ✅ (indicativo) |
| KR3 | Aumentar % que reciben feedback estructurado en al menos 1 sesión (baseline: 40%) | ≥ 90% | 50.0% (4/8) | **87.5%** (7/8, indirecto) | +37.5 pp | ⚠️ Cerca de la meta, sin pregunta directa |

**Muestra:** 8 usuarios externos al equipo · **Fecha:** 13 de noviembre de 2026 · **Instrumento:** cuestionario pre/post vía Google Forms (escala 1–5)  
**Cálculo:** KR1 = % con 1–2 en preparación (1 = nada preparado/a). KR2 = % con 1–2 en facilidad STAR (1 = muy difícil); n = 6 porque las 2 primeras respuestas usaron una versión del formulario sin la pregunta post. KR3: el formulario no incluyó "¿Recibiste feedback?"; se usa como indicador indirecto el % que calificó el feedback recibido. Detalle en `mvp/evidencia/resultados_okr.md`.

---

### A2. Métricas del Componente Analítico (A2 — Clasificador STAR)

**Tarea:** Clasificación multilabel independiente — 4 clasificadores binarios, uno por componente STAR.  
**Modelo seleccionado:** TF-IDF bigramas + Linear SVM (CalibratedClassifierCV)  
**Dataset:** `interviewiq_star_v1.csv` — 200 pares etiquetados (100% sintéticos, generados y etiquetados por el equipo)  
**Split:** 70% entrenamiento / 10% validación / 20% prueba  
**Vectorizador:** TF-IDF, bigramas, max_features=5000, sublinear_tf=True

#### Resultados en set de prueba (con umbrales ajustados)

| Componente | F1 Macro | Falsos Positivos | Falsos Negativos | Umbral | Criterio ≥0.65 |
|------------|----------|-----------------|-----------------|--------|----------------|
| S — Situación | **0.865** | 4 (25.0%) | 1 | 0.30 | ✅ CUMPLE |
| T — Tarea | **0.822** | 7 (33.3%) | 0 | 0.30 | ✅ CUMPLE |
| A — Acción | **0.804** | 1 (9.1%) | 6 | 0.75 | ✅ CUMPLE |
| R — Resultado | **0.829** | 2 (7.7%) | 4 | 0.50 | ✅ CUMPLE |
| **PROMEDIO** | **0.808** | — | — | — | ✅ CUMPLE |

> ⚠️ Los F1 de esta tabla se calcularon con el umbral de Resultado ajustado a 0.50 (vigente en la app).

#### Comparación baseline vs modelo final

| Componente | LR Baseline F1 | SVM Final F1 | Ganador |
|------------|---------------|-------------|---------|
| S — Situación | 0.840 | **0.896** | SVM ✓ |
| T — Tarea | 0.874 | **0.900** | SVM ✓ |
| A — Acción | 0.881 | 0.881 | Empate |
| R — Resultado | 0.774 | **0.868** | SVM ✓ |
| **Promedio** | 0.842 | **0.851** | **SVM** |

> El modelo SVM supera al baseline en 3 de 4 componentes (sin ajuste de umbral: F1 promedio 0.851 vs 0.842). Con umbrales ajustados para minimizar FP, el F1 promedio final es **0.808**, superando el criterio de 0.65 en todos los componentes.

#### Lectura en costos de negocio

El error más costoso en InterviewIQ es el **Falso Positivo**: decirle al estudiante que un componente STAR está presente cuando no lo está genera feedback incorrecto y daña la confianza en la herramienta. El Falso Negativo es menos dañino: en el peor caso el estudiante recibe consejos constructivos que no eran necesarios.

| Componente | Tasa FP (umbral ajustado) | Riesgo de negocio | Umbral elegido | Justificación |
|------------|--------------------------|------------------|----------------|---------------|
| S — Situación | 25.0% | 🔴 Alto (sigue siendo alto) | 0.30 | Umbral más bajo ya penaliza FP; bajar más destruiría recall |
| T — Tarea | 33.3% | 🔴 Alto (sigue siendo alto) | 0.30 | Ídem S; componente difícil de separar de S en texto corto |
| A — Acción | 9.1% | 🟢 Bajo | 0.75 | Umbral alto reduce FP sin sacrificar demasiado recall |
| R — Resultado | 7.7% | 🟢 Bajo | 0.50 | Umbral ajustado a 0.50 para reducir FN sin aumentar FP; componente más distintivo léxicamente |

**Fórmula de ajuste de umbral:**
```
score(umbral) = F1(umbral) − 0.5 × tasa_FP(umbral)
```
Se evaluó cada umbral de 0.05 a 0.95 en el set de validación y se eligió el que maximiza este score combinado.

---

### A3. Métrica del Componente Generativo (G1 — Feedback con IA)

**Nivel declarado en PC1:** G2 (RAG con GPT-4o-mini + ChromaDB)  
**Implementación en MVP:** G1 — Gemini 2.5 Flash vía API REST. El RAG completo quedó fuera del alcance del MVP por restricciones de tiempo. Se incluye fallback a reglas estructuradas para garantizar disponibilidad.

| Métrica | Meta PC1 | Resultado | Cumple |
|---------|----------|-----------|--------|
| Feedback coherente con output A2 (Patrón 1 activo) | ≥ 90% en 20 casos | Por diseño, el feedback por reglas no puede contradecir al modelo. Medición en 20 casos: **100%** | ✅ |
| Latencia de respuesta | < 5 seg | Observada en la demo; no se midió formalmente | ⚠️ No medido |
| Disponibilidad sin API key | Fallback disponible | ✅ Reglas estructuradas activas cuando no hay GEMINI_API_KEY | ✅ |

> **Decisión documentada:** El MVP usa Gemini 2.5 Flash como componente generativo principal, con fallback automático a reglas estructuradas. El RAG completo y la Etapa 1 (clasificador de nivel de preparación) quedaron fuera del MVP actual y están documentados en la Plantilla 3 (nota de versión final) y como deuda técnica en la sección B5 de esta plantilla.

---

## Parte B — Riesgos, ética y regulación (Fase T)

### B1. Matriz de riesgos

#### Riesgos del Componente Analítico (modelo A2)

| # | Riesgo | Probabilidad | Impacto | Nivel | Mitigación concreta |
|---|--------|-------------|---------|-------|---------------------|
| R1 | El modelo clasifica incorrectamente un componente STAR como presente cuando no lo está (Falso Positivo) | Alta (S: 25%, T: 33%) | Alto | 🔴 Crítico | Ajuste de umbrales por componente en validación. Se muestra la probabilidad numérica al usuario para que evalúe. Umbral conservador en A (0.75); R en 0.50 tras pruebas internas (caso límite C5). La app además avisa cuando la respuesta es hipotética ("yo haría…"), que fue el falso positivo más grave encontrado. |
| R2 | Dataset sintético no representa la variedad real de respuestas (sesgo de distribución) | Media | Alto | 🟡 Moderado | 200 ejemplos son el punto de partida. Las pruebas de usuario (≥5 personas reales) validan el comportamiento con texto real. Se planifica re-entrenamiento post-lanzamiento con datos reales. |
| R3 | Degradación del modelo en respuestas muy cortas (< 15 palabras) | Alta | Medio | 🟡 Moderado | La app advierte al usuario si la respuesta es muy corta. El modelo muestra confianza baja en estos casos. |
| R4 | Respuestas en otro idioma o con mucho argot degradan la clasificación | Media | Bajo | 🟢 Bajo | El modelo fue entrenado solo en español. La interfaz indica que la respuesta debe ser en español. |

#### Riesgos de la Capa Generativa (G1)

| # | Riesgo | Probabilidad | Impacto | Nivel | Mitigación concreta |
|---|--------|-------------|---------|-------|---------------------|
| R5 | La API de Gemini no responde o devuelve error | Media | Medio | 🟡 Moderado | Fallback automático a reglas estructuradas. El usuario siempre recibe feedback, aunque sea más genérico. |
| R6 | Gemini genera feedback que contradice el output del clasificador A2 | Baja | Alto | 🟡 Moderado | El prompt enviado a Gemini incluye explícitamente los componentes detectados por A2. El feedback se genera condicionado a ese output. |
| R7 | El estudiante interpreta el feedback de IA como garantía de éxito en una entrevista real | Baja | Alto | 🟡 Moderado | La interfaz incluye disclaimer visible: *"InterviewIQ es una herramienta de práctica, no una evaluación oficial."* |

#### Riesgo de acción no deseada

| # | Riesgo | Probabilidad | Impacto | Nivel | Mitigación concreta |
|---|--------|-------------|---------|-------|---------------------|
| R8 | Si se implementa agente autónomo (n8n): el agente registra datos de usuarios sin consentimiento explícito | Baja | Crítico | 🔴 Crítico | Fuera del MVP actual. Si se implementa en versión futura, se solicitará consentimiento explícito antes del registro. Los datos se anonimizarán. Aplica Ley N.° 29733. |

---

### B2. Ética y regulación

#### Regulación aplicable

**Ley N.° 29733 — Ley de Protección de Datos Personales del Perú**

InterviewIQ procesa respuestas de texto libre que pueden contener información personal del usuario (experiencias laborales, situaciones académicas, datos sobre terceros mencionados en las respuestas). Se aplica la ley porque:

1. Las respuestas del usuario son datos personales según el Art. 2 de la Ley.
2. El procesamiento de estas respuestas (clasificación + envío a Gemini API) requiere consentimiento informado (Art. 13).
3. La finalidad del procesamiento debe ser específica y declarada (Art. 8).

**Cómo InterviewIQ cumple la Ley N.° 29733:**

| Obligación legal | Implementación en InterviewIQ |
|-----------------|-------------------------------|
| Consentimiento informado (Art. 13) | La app muestra un aviso visible antes del análisis: *"Privacidad (Ley N.° 29733): tu respuesta se usa solo en esta sesión; evita datos personales."* En las pruebas con usuarios, el formulario fue anónimo y no recolectó nombres, correos ni DNI. |
| Finalidad específica (Art. 8) | Los datos se usan exclusivamente para clasificación STAR y generación de feedback. No se usan para entrenamiento ni se envían a terceros más allá de Gemini API (propósito declarado). |
| No almacenamiento sin consentimiento | El MVP no persiste respuestas del usuario. Streamlit no guarda texto entre sesiones. No hay base de datos. |
| Seguridad (Art. 16) | La comunicación es HTTPS (Streamlit Community Cloud). Las llamadas a Gemini API también son HTTPS. No hay base de datos con datos personales. |

#### Declaración de transparencia del MVP

El MVP informa visiblemente al usuario que está interactuando con IA mediante:
- Landing: *"…y recibe análisis con IA en segundos."*
- Aviso visible en la pantalla de análisis: *"Herramienta de práctica — puede equivocarse y no predice resultados en entrevistas reales."*
- El feedback indica si fue generado por Google Gemini o por reglas.
- El score STAR muestra la probabilidad numérica de cada componente, no solo la clasificación binaria.

---

### B3. Respuesta a "¿qué pasa si la IA se equivoca?"

| Escenario | Qué puede pasar | Cómo lo manejamos |
|-----------|----------------|-------------------|
| El modelo dice que falta Situación, pero sí estaba presente (FN) | El estudiante recibe feedback innecesario sobre cómo añadir contexto | El feedback de FN es constructivo y no dañino. En el peor caso el estudiante aprende algo extra sobre estructura STAR. |
| El modelo dice que la Acción está presente, pero no lo estaba (FP) | El estudiante no recibe el consejo correcto sobre qué mejorar | Se minimiza con umbral 0.75 para Acción. Las probabilidades se muestran para que el usuario las evalúe. |
| Gemini genera feedback incorrecto o incoherente | El estudiante recibe orientación errónea | El prompt incluye los componentes detectados por A2 como restricción. Si la respuesta de Gemini falla, el fallback a reglas garantiza feedback consistente. |
| El MVP no está disponible el día de la sustentación | El evaluador no puede acceder | Deploy en Streamlit Community Cloud (plan gratuito, sin SLA garantizado). Se abre la app antes de la sustentación para "despertarla" y se tiene un video/capturas de la demo como respaldo. |

---

### B4. Archivos generados por el modelo

| Archivo | Descripción | Ubicación en repo |
|---------|-------------|------------------|
| `clasificador_star_situacion.pkl` | Modelo SVM + TF-IDF vectorizer para componente S | `models/` |
| `clasificador_star_tarea.pkl` | Modelo SVM + TF-IDF vectorizer para componente T | `models/` |
| `clasificador_star_accion.pkl` | Modelo SVM + TF-IDF vectorizer para componente A | `models/` |
| `clasificador_star_resultado.pkl` | Modelo SVM + TF-IDF vectorizer para componente R | `models/` |
| `config_clasificador.json` | Umbrales óptimos por componente y metadata del modelo | `models/` |
| `interviewiq_star_v1.csv` | Dataset de entrenamiento (200 filas etiquetadas) | `data/raw/` |

---

### B5. Deuda técnica documentada

| ID | Componente | Descripción | Prioridad para próxima versión |
|----|------------|-------------|-------------------------------|
| DT-01 | Etapa 1 (clasificador de nivel) | Clasificar al usuario como principiante/intermedio/avanzado para adaptar preguntas | Alta |
| DT-02 | RAG (G2) | Recuperación de ejemplos reales de respuestas STAR para enriquecer el feedback de Gemini | Media |
| DT-03 | Re-entrenamiento con datos reales | Ampliar el dataset R2 con respuestas reales de las pruebas de usuario | Alta |
| DT-04 | Historial de sesiones | Permitir al usuario ver su progreso entre sesiones | Media |
| DT-05 | Evaluación automática del feedback | Medir calidad del feedback de Gemini vs reglas (BLEU, aceptación por usuario) | Baja |
| DT-06 | Soporte multiidioma | Entrenar o adaptar el modelo para respuestas en inglés | Baja |
