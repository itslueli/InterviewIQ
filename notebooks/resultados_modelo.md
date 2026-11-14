### Baseline vs modelo final (validación cruzada 5x5, umbral 0.5)

| componente | F1 LR (media) | ± LR | F1 SVM (media) | ± SVM | ganador |
|---|---|---|---|---|---|
| situacion | 0.929 | 0.044 | 0.934 | 0.042 | SVM |
| tarea | 0.848 | 0.047 | 0.848 | 0.055 | Empate |
| accion | 0.815 | 0.062 | 0.829 | 0.058 | SVM |
| resultado | 0.779 | 0.041 | 0.793 | 0.045 | SVM |
| PROMEDIO | 0.843 |  | 0.851 |  | SVM |

### Baseline vs modelo final (un split de prueba, umbral 0.5)

| componente | F1 LR | F1 SVM | ganador |
|---|---|---|---|
| situacion | 0.971 | 0.971 | Empate |
| tarea | 0.893 | 0.893 | Empate |
| accion | 0.796 | 0.804 | SVM |
| resultado | 0.824 | 0.768 | LR |
| PROMEDIO | 0.871 | 0.859 | LR |

### Modelo final con umbrales de la app (prueba)

| componente | umbral | F1 macro | FP | FN | tasa FP | cumple ≥ 0.65 |
|---|---|---|---|---|---|---|
| situacion | 0.30 | 0.903 | 3 | 0 | 0.250 | ✅ |
| tarea | 0.30 | 0.829 | 6 | 0 | 0.375 | ✅ |
| accion | 0.75 | 0.733 | 4 | 6 | 0.286 | ✅ |
| resultado | 0.50 | 0.768 | 6 | 3 | 0.240 | ✅ |
| PROMEDIO |  | 0.808 |  |  |  | ✅ |

### Lectura en costos

| componente | umbral | FP | FN | tasa FP | riesgo por FP |
|---|---|---|---|---|---|
| situacion | 0.30 | 3 | 0 | 0.250 | 🔴 Alto |
| tarea | 0.30 | 6 | 0 | 0.375 | 🔴 Alto |
| accion | 0.75 | 4 | 6 | 0.286 | 🔴 Alto |
| resultado | 0.50 | 6 | 3 | 0.240 | 🟡 Medio |
