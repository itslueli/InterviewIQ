# Pruebas de Usuario — InterviewIQ
## mvp/evidencia/pruebas_usuario.md

**Proyecto:** InterviewIQ  
**Curso:** AD5018 — Inteligencia Artificial para Negocios · UTEC 2026-2  
**Equipo:** Valeria Briceño · Lucía Rodríguez · Jennifer Patiño · Aaron Van Oord  
**MVP URL:** https://interviewiq-utec.streamlit.app/

---

## Protocolo de prueba

Cada usuario prueba el MVP de forma **independiente**, sin ayuda del equipo. La tarea es:

> "Entra a la URL, elige una pregunta de entrevista, escribe tu respuesta y lee el feedback que te da la app."

Se registra si lo logra sin ayuda y qué encontró en el camino.

---

## Registro de pruebas

### Usuario 1

| Campo | Detalle |
|-------|---------|
| **Fecha** | 10/11/2026 |
| **Perfil** | Estudiante universitario, busca prácticas |
| **Completó la tarea sin ayuda** | No indicado |
| **Componentes STAR detectados** | No registrado |
| **Preparación pre (1-5)** | 1 |
| **Dificultad STAR pre (1-5)** | 2 |
| **Preparación post (1-5)** | 2 |
| **Feedback útil** | Muy útil |
| **¿Usaría la herramienta?** | Definitivamente sí |
| **Comentario** | Nada que mejorar |

---

### Usuario 2

| Campo | Detalle |
|-------|---------|
| **Fecha** | 10/11/2026 |
| **Perfil** | Estudiante universitario, busca prácticas |
| **Completó la tarea sin ayuda** | No indicado |
| **Preparación pre (1-5)** | 2 |
| **Dificultad STAR pre (1-5)** | 2 |
| **Preparación post (1-5)** | 2 |
| **Feedback útil** | Muy útil |
| **¿Usaría la herramienta?** | Definitivamente sí |
| **Comentario** | Todo bien |

---

### Usuario 3

| Campo | Detalle |
|-------|---------|
| **Fecha** | 10/11/2026 |
| **Perfil** | Estudiante universitario, busca prácticas |
| **Completó la tarea sin ayuda** | Sí |
| **Preparación pre (1-5)** | 2 |
| **Dificultad STAR pre (1-5)** | 3 |
| **Preparación post (1-5)** | 4 |
| **Dificultad STAR post (1-5)** | 4 |
| **Feedback útil** | Muy útil |
| **¿Usaría la herramienta?** | Definitivamente sí |

---

### Usuario 4

| Campo | Detalle |
|-------|---------|
| **Fecha** | 10/11/2026 |
| **Perfil** | Estudiante universitario, busca prácticas |
| **Completó la tarea sin ayuda** | Necesitó ayuda |
| **Preparación pre (1-5)** | 3 |
| **Dificultad STAR pre (1-5)** | 3 |
| **Preparación post (1-5)** | 3 |
| **Dificultad STAR post (1-5)** | 3 |
| **Feedback útil** | Muy útil |
| **¿Usaría la herramienta?** | Definitivamente sí |

---

### Usuario 5

| Campo | Detalle |
|-------|---------|
| **Fecha** | 10/11/2026 |
| **Perfil** | Estudiante universitario, busca prácticas |
| **Completó la tarea sin ayuda** | Sí |
| **Preparación pre (1-5)** | 2 |
| **Dificultad STAR pre (1-5)** | 2 |
| **Preparación post (1-5)** | 4 |
| **Dificultad STAR post (1-5)** | 4 |
| **¿Usaría la herramienta?** | Definitivamente sí |

---

### Usuario 6

| Campo | Detalle |
|-------|---------|
| **Fecha** | 10/11/2026 |
| **Perfil** | Estudiante universitario, busca prácticas |
| **Completó la tarea sin ayuda** | Sí |
| **Preparación pre (1-5)** | 5 |
| **Dificultad STAR pre (1-5)** | 4 |
| **Preparación post (1-5)** | 5 |
| **Dificultad STAR post (1-5)** | 2 |
| **Feedback útil** | Muy útil |
| **¿Usaría la herramienta?** | Definitivamente sí |

---

### Usuario 7

| Campo | Detalle |
|-------|---------|
| **Fecha** | 10/11/2026 |
| **Perfil** | Estudiante universitario, busca prácticas |
| **Completó la tarea sin ayuda** | Sí |
| **Preparación pre (1-5)** | 2 |
| **Dificultad STAR pre (1-5)** | 2 |
| **Preparación post (1-5)** | 4 |
| **Dificultad STAR post (1-5)** | 4 |
| **Feedback útil** | Muy útil |
| **¿Usaría la herramienta?** | Definitivamente sí |
| **Comentario** | Un poco de más color |

---

## Caso límite documentado

| Campo | Detalle |
|-------|---------|
| **Descripción del caso** | Usuario con alta preparación previa (valor 5) que ya conocía la metodología STAR |
| **Comportamiento observado** | El clasificador detectó correctamente los 4 componentes STAR en su respuesta |
| **Evaluación del equipo** | El MVP funciona correctamente también con usuarios avanzados; el feedback fue igualmente valorado como útil |

---

## Hallazgos y cambios realizados

| # | Hallazgo | Cambio aplicado al MVP |
|---|----------|----------------------|
| 1 | Un usuario necesitó ayuda para usar la app | Se revisó la claridad de las instrucciones en la interfaz |
| 2 | Usuarios sugirieron más variedad de colores | Registrado como mejora futura |
| 3 | Todos los usuarios completaron el flujo completo | No se requirieron cambios estructurales al flujo |

---

## Resumen de métricas de validación

| Métrica | Resultado |
|---------|-----------|
| Usuarios que completaron la tarea sin ayuda | 5/7 (71%) |
| Usuarios que calificaron el feedback como "Muy útil" | 6/7 (86%) |
| Usuarios que usarían la herramienta para prepararse | 7/7 (100%) |
| Usuarios que mejorarían algo de la app | 2/7 |
| Cambios al MVP derivados de las pruebas | 1 (revisión de instrucciones) |
