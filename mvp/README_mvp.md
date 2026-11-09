# InterviewIQ — MVP

## URL de acceso

> **aca va el link**

Accesible desde cualquier dispositivo con internet. No requiere instalación ni cuenta.

---

## ¿Qué hace el MVP?

InterviewIQ analiza tus respuestas de entrevista por competencias y te dice qué componentes STAR (Situación, Tarea, Acción, Resultado) están presentes o ausentes, con feedback personalizado para mejorar.

---

## Instrucciones para el evaluador

1. Abre la URL en tu navegador
2. Elige una pregunta de entrevista del menú desplegable
3. Escribe tu respuesta en el cuadro de texto (mínimo 20 palabras)
4. Presiona **"Analizar mi respuesta"**
5. Revisa el análisis STAR y el feedback

No se necesita cuenta, API key ni configuración adicional. El feedback funciona sin clave de OpenAI

---

## Stack técnico

| Componente | Tecnología |
|------------|------------|
| Interfaz | Streamlit |
| Clasificador STAR (A2) | TF-IDF bigramas + Linear SVM (scikit-learn) |
| Feedback (G2) | Reglas estructuradas + GPT-4o-mini opcional |
| Deploy | Streamlit Community Cloud |
| Modelos | 4 archivos `.pkl` + `config_clasificador.json` |

---

## Métricas del modelo

- **Modelo:** TF-IDF + Linear SVM
- **F1 Macro promedio:** 0.830 (set de prueba, umbrales ajustados)
- **Dataset:** 200 pares etiquetados — `data/raw/interviewiq_star_v1.csv`

---

## Limitaciones conocidas

- El modelo fue entrenado con datos sintéticos; puede fallar con respuestas muy coloquiales o muy cortas (< 20 palabras)
- El feedback con IA requiere que el usuario ingrese su propia API key de OpenAI en la sección de configuración
- El MVP no guarda historial de respuestas entre sesiones

---

## Repositorio

[github.com/itslueli/InterviewIQ](https://github.com/itslueli/InterviewIQ)
