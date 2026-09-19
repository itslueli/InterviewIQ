# Plantilla 1 — Problem Statement Canvas
## Framework PROMPT | Fase P — Problema de Negocio
### AD5018 Inteligencia Artificial para Negocios | UTEC

---

**Equipo:**
- Integrante 1: Valeria Briceño
- Integrante 2: Lucia Rodriguez
- Integrante 3: Aaron Van Oord


**Fecha de entrega:** 19/09/2026  
**Versión del canvas:** v1

---

## SECCIÓN 1 — Definición del problema

### 1.1 Usuario afectado
Estudiantes universitarios peruanos de últimos ciclos que se encuentran buscando prácticas preprofesionales o su primer empleo y necesitan prepararse para entrevistas laborales por competencias.

### 1.2 Problema específico
Los estudiantes tienen oportunidades limitadas para practicar entrevistas laborales de manera recurrente y recibir retroalimentación estructurada sobre la calidad de sus respuestas. Esto dificulta que identifiquen qué aspectos de sus respuestas comunican adecuadamente sus experiencias y cuáles necesitan mejorar.

### 1.3 Causa raíz
La práctica individual de entrevistas no proporciona retroalimentación externa sobre la estructura y claridad de las respuestas, mientras que practicar repetidamente con una persona que pueda simular una entrevista y brindar feedback depende de la disponibilidad de terceros. Esto limita la posibilidad de practicar, identificar deficiencias y corregirlas de manera recurrente antes de una entrevista real.

### 1.4 Consecuencia medible
En una muestra objetivo de 50 estudiantes universitarios de últimos ciclos, valido que aproximadamente **60%** se siente poco o nada preparado para afrontar entrevistas laborales por competencias, **40%** rara vez o nunca recibe retroalimentación estructurada al practicar entrevistas y **80%** reporta al menos alguna dificultad para estructurar ejemplos concretos al responder preguntas conductuales.


### 1.5 Declaración del problema — formato obligatorio
Los estudiantes universitarios peruanos de últimos ciclos que buscan prácticas preprofesionales o su primer empleo tienen dificultad para preparar y mejorar sus respuestas en entrevistas laborales por competencias porque cuentan con oportunidades limitadas de práctica recurrente con retroalimentación estructurada, lo que genera bajos niveles de preparación percibida y dificultades para estructurar respuestas conductuales.

---

## SECCIÓN 2 — Filtro de validación IA

| Pregunta | SÍ / NO | Justificación |
|---|---|---|
| ¿Una hoja de cálculo o formulario resuelve esto? | **NO** | Las respuestas son texto libre y requieren análisis contextual y retroalimentación personalizada. |
| ¿El problema escala con volumen de datos o usuarios? | **SÍ** | Cada usuario puede generar múltiples respuestas abiertas que deben evaluarse individualmente. |
| ¿Hay un patrón repetitivo difícil de procesar manualmente? | **SÍ** | Cada respuesta debe analizarse para identificar componentes STAR y oportunidades de mejora. |
| ¿El problema requiere generar contenido o razonar en lenguaje natural? | **SÍ** | Se deben formular preguntas y generar retroalimentación sobre respuestas abiertas. |
| ¿Necesitas predecir Y luego explicar o actuar sobre el resultado? | **SÍ** | El modelo identifica componentes STAR y la capa generativa utiliza ese resultado para producir feedback. |

### Conclusión del filtro
La IA es adecuada porque el problema involucra analizar respuestas abiertas de manera repetitiva, identificar patrones en lenguaje natural y generar retroalimentación contextualizada. Una solución basada únicamente en formularios o reglas fijas tendría dificultades para adaptarse a la variedad de respuestas y proporcionar feedback específico a cada usuario.

---

## SECCIÓN 3 — Los dos componentes del producto

### 3.1 Componente analítico — qué va a aprender el modelo

**¿Qué va a predecir, clasificar o agrupar?**

El modelo identificará la presencia o ausencia de los componentes **Situación, Tarea, Acción y Resultado (STAR)** en las respuestas textuales del usuario a preguntas conductuales.

**Tipo de tarea:**
- [x] **Clasificación**
- [ ] **Regresión**
- [ ] **Agrupamiento**

**Nivel de profundidad elegido:**
- [ ] **A1**
- [x] **A2** — compara modelos y ajusta el umbral según el costo del error
- [ ] **A3**

**Compromiso A2:** se entrenará un baseline y al menos un modelo alternativo. Se compararán con métricas adecuadas para la clasificación STAR y se justificará el umbral considerando el costo de falsos positivos y falsos negativos.

### 3.2 Componente generativo — qué va a hacer la capa de lenguaje

**¿Qué comunica, decide o ejecuta?**

Generará preguntas conductuales contextualizadas al puesto objetivo y retroalimentación personalizada sobre cada respuesta, utilizando el resultado del clasificador y conocimiento recuperado de fuentes seleccionadas sobre entrevistas y metodología STAR.

**Nivel de profundidad elegido:**
- [ ] **G1**
- [x] **G2 — RAG**
- [ ] **G3**
- [ ] **G4**

### 3.3 Cómo se conectan — patrón elegido

- [x] **Patrón 1 — Modelo → lenguaje**
- [ ] **Patrón 2 — Lenguaje → modelo**
- [ ] **Patrón 3 — Modelo como herramienta del agente**

**¿Qué dato exactamente viaja de un componente al otro?**

El componente analítico envía a la capa generativa las predicciones sobre presencia o ausencia de cada componente STAR detectado (S, T, A y R), junto con la respuesta original del usuario. La capa generativa combina ese resultado con información recuperada mediante RAG para elaborar retroalimentación específica.

### 3.4 Dónde va la ambición del equipo

- [ ] Vamos a fondo en el **componente generativo** (G3 o G4) y mantenemos el analítico en A1
- [ ] Vamos a fondo en el **componente analítico** (A3) y mantenemos el generativo en G1
- [x] **Nos quedamos en un punto intermedio en ambos (A2 + G2)**

**¿Por qué esa elección?**

El equipo adopta A2 + G2 porque el problema requiere tanto una evaluación confiable de respuestas abiertas como retroalimentación contextualizada. En el componente analítico se compararán modelos para seleccionar el enfoque que identifique mejor los componentes STAR y se justificará el umbral de clasificación. El RAG permitirá generar feedback apoyado en fuentes seleccionadas sobre entrevistas y metodología STAR. Este alcance equilibra profundidad técnica y viabilidad dentro del tiempo disponible.

### 3.5 Justificación general
El componente analítico permite evaluar de manera consistente la estructura de respuestas conductuales mediante la detección de componentes STAR. La capa generativa convierte ese resultado técnico en retroalimentación comprensible y contextualizada para el estudiante. El uso de RAG permite fundamentar el feedback en fuentes seleccionadas sobre entrevistas y metodología STAR, en lugar de depender únicamente del conocimiento general del LLM. La combinación A2 + G2 permite evaluar, explicar y orientar la mejora de cada respuesta manteniendo un alcance viable para el MVP.

### 3.6 Solo si el equipo solicita la excepción
- [ ] Solicitamos excepción al componente analítico

**No aplica.** El proyecto contempla entrenar y comparar modelos analíticos propios.

---

## SECCIÓN 4 — Autoevaluación del equipo

| Pregunta de control | Respuesta |
|---|---|
| ¿El problema está descrito sin mencionar tecnología? | **SÍ** |
| ¿La declaración del problema sigue el formato exacto? | **SÍ** |
| ¿Los dos componentes están definidos, con su nivel y su patrón de conexión? | **SÍ** |
| ¿La elección de niveles se justifica con el problema, no con la preferencia del equipo? | **SÍ** |
| ¿El equipo declaró en cuál de los dos ejes concentra su ambición? | **SÍ — A2 + G2** |
| ¿El componente analítico implica entrenar un modelo, no solo consumir una API? | **SÍ** |
| ¿Todos los integrantes pueden explicar este canvas sin leerlo? | **PENDIENTE DE VALIDACIÓN INTERNA** |

