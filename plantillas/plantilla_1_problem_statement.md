# Plantilla 1 — Problem Statement Canvas
## Problema de Negocio
### AD5018 Inteligencia Artificial para Negocios | UTEC

---

**Equipo:**
- Integrante 1: Valeria Briceño
- Integrante 2: Lucia Rodriguez
- Integrante 3: Aaron Van Oord

---

## SECCIÓN 1 — Definición del problema

### 1.1 Usuario afectado
Estudiantes universitarios peruanos de últimos ciclos que se encuentran buscando prácticas preprofesionales o su primer empleo y necesitan prepararse para entrevistas laborales por competencias.

### 1.2 Problema específico
Los estudiantes tienen oportunidades limitadas para practicar entrevistas laborales de manera recurrente y recibir retroalimentación estructurada sobre la calidad de sus respuestas. Esto dificulta que identifiquen qué aspectos de sus respuestas comunican adecuadamente sus experiencias y cuáles necesitan mejorar.

### 1.3 Causa raíz
La práctica individual de entrevistas no proporciona retroalimentación externa sobre la estructura y claridad de las respuestas, mientras que practicar repetidamente con una persona que pueda simular una entrevista y brindar feedback depende de la disponibilidad de terceros. Esto limita la posibilidad de practicar, identificar deficiencias y corregirlas de manera recurrente antes de una entrevista real.

### 1.4 Consecuencia medible
En una muestra objetivo de 50 estudiantes universitarios de últimos ciclos, se validó que aproximadamente **60%** se siente poco o nada preparado para afrontar entrevistas laborales por competencias, **40%** rara vez o nunca recibe retroalimentación estructurada al practicar entrevistas y **80%** reporta al menos alguna dificultad para estructurar ejemplos concretos al responder preguntas conductuales.

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

El sistema utilizará **dos etapas de clasificación** que trabajan en secuencia:

**Etapa 1 — Diagnóstico de nivel de preparación:**
Un clasificador procesará las respuestas del estudiante a un cuestionario diagnóstico inicial (experiencia previa, conocimiento de STAR, nivel de confianza autodeclarada, dificultad para estructurar respuestas y frecuencia de feedback recibido) para asignarle un nivel de preparación. Este nivel adapta la dificultad y el tipo de preguntas conductuales que se generarán en la sesión de práctica.

**Etapa 2 — Detección de componentes STAR:**
El modelo principal identificará la presencia o ausencia de los componentes **Situación, Tarea, Acción y Resultado (STAR)** en las respuestas textuales del usuario a las preguntas conductuales.

**Tipo de tarea:**
- [x] **Clasificación**
- [ ] **Regresión**
- [ ] **Agrupamiento**

**Nivel de profundidad elegido:**
- [ ] **A1**
- [x] **A2** — compara modelos y ajusta el umbral según el costo del error
- [ ] **A3**

**Compromiso A2:** se entrenará un baseline y al menos un modelo alternativo para la detección STAR. Se compararán con métricas adecuadas y se justificará el umbral considerando el costo de falsos positivos y falsos negativos.

### 3.2 Componente generativo — qué va a hacer la capa de lenguaje

**¿Qué comunica, decide o ejecuta?**

La capa generativa cumple dos funciones según la etapa del flujo:

1. **Generación de preguntas conductuales adaptadas** al puesto objetivo y al nivel de preparación detectado en la etapa diagnóstica.
2. **Generación de retroalimentación personalizada** sobre cada respuesta del usuario, utilizando el resultado del clasificador STAR (Etapa 2) y conocimiento recuperado de fuentes seleccionadas sobre entrevistas y metodología STAR.

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

El flujo completo del sistema es el siguiente:

```
[Cuestionario diagnóstico]
        ↓
[Clasificador de nivel de preparación — Logistic Regression]
Output: nivel ∈ {básico, intermedio, avanzado}
        ↓
[Generación de preguntas adaptadas al rol y nivel — LLM]
        ↓
[Respuesta del usuario en texto libre]
        ↓
[Clasificador STAR — A2 (TF-IDF + LR o SVM)]
Output: S ∈ {0,1}, T ∈ {0,1}, A ∈ {0,1}, R ∈ {0,1}
        ↓
[RAG: recuperación de contexto relevante del corpus]
        ↓
[LLM genera feedback personalizado — G2]
```

El clasificador de nivel (Etapa 1) envía el nivel asignado al generador de preguntas. El clasificador STAR (Etapa 2) envía a G2 las predicciones de presencia/ausencia de S, T, A y R junto con la respuesta original. G2 combina ese resultado con los fragmentos recuperados del corpus para elaborar retroalimentación específica.

### 3.4 Dónde va la ambición del equipo

- [ ] Vamos a fondo en el **componente generativo** (G3 o G4) y mantenemos el analítico en A1
- [ ] Vamos a fondo en el **componente analítico** (A3) y mantenemos el generativo en G1
- [x] **Nos quedamos en un punto intermedio en ambos (A2 + G2)**

**¿Por qué esa elección?**

El equipo adopta A2 + G2 porque el problema requiere tanto una evaluación confiable de respuestas abiertas como retroalimentación contextualizada. Dentro del componente analítico se incorpora un diagnóstico inicial del nivel de preparación del estudiante, lo que permite adaptar las preguntas a su perfil antes de iniciar la práctica STAR. En la detección STAR se compararán modelos para seleccionar el que mejor identifique los componentes y se justificará el umbral de clasificación. El RAG permitirá generar feedback apoyado en fuentes seleccionadas. Este alcance equilibra profundidad técnica y viabilidad dentro del tiempo disponible.

### 3.5 Justificación general
El diagnóstico inicial de nivel de preparación personaliza la experiencia desde el primer momento, evitando preguntas demasiado fáciles para usuarios avanzados o demasiado exigentes para usuarios básicos. El clasificador STAR permite evaluar de manera consistente la estructura de las respuestas conductuales. La capa generativa convierte ese resultado técnico en retroalimentación comprensible y contextualizada. El uso de RAG permite fundamentar el feedback en fuentes seleccionadas sobre metodología STAR, en lugar de depender únicamente del conocimiento general del LLM. La combinación A2 + G2 permite diagnosticar, adaptar, evaluar y orientar la mejora de cada respuesta manteniendo un alcance viable para el MVP.

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
| ¿El flujo completo entre las dos etapas de clasificación y G2 está descrito? | **SÍ** |
| ¿Todos los integrantes pueden explicar este canvas sin leerlo? | **SÍ** |
