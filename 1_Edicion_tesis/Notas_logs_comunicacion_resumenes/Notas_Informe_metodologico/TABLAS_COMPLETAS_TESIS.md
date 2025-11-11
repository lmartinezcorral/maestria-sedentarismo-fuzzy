# TABLAS COMPLETAS PARA TESIS
## Sistema de Inferencia Difusa para Evaluación de Sedentarismo

**Fecha:** 18 de octubre de 2025  
**Umbral óptimo:** τ = 0.30  
**Total de semanas válidas:** 1,337

---

## TABLA 1: Métricas de Clasificación (Fuzzy vs. Clusters) por Usuario

| Usuario | Semanas (N) | % Datos obs.* | Accuracy | Precision | Recall | F1 | MCC | τ usado | TP | FP | TN | FN |
|---------|------------:|---------------:|---------:|----------:|-------:|----:|-----:|--------:|----:|----:|----:|----:|
| **u1 – ale** | 149 | 100.0 | 0.993 | 0.993 | 1.000 | **0.997** | 0.000 | 0.30 | 148 | 1 | 0 | 0 |
| **u2 – brenda** | 7 | 100.0 | 0.429 | 0.750 | 0.500 | **0.600** | -0.354 | 0.30 | 3 | 1 | 0 | 3 |
| **u3 – christina** | 141 | 100.0 | 0.277 | 0.123 | 0.875 | **0.215** | 0.060 | 0.30 | 14 | 100 | 25 | 2 |
| **u4 – edson** | 14 | 100.0 | 0.714 | 0.714 | 1.000 | **0.833** | 0.000 | 0.30 | 10 | 4 | 0 | 0 |
| **u5 – esmeralda** | 14 | 100.0 | 0.714 | 0.692 | 1.000 | **0.818** | 0.372 | 0.30 | 9 | 4 | 1 | 0 |
| **u6 – fidel** | 278 | 100.0 | 0.817 | 0.827 | 0.982 | **0.898** | 0.104 | 0.30 | 224 | 47 | 3 | 4 |
| **u7 – kevin** | 114 | 100.0 | 0.947 | 0.947 | 1.000 | **0.973** | 0.000 | 0.30 | 108 | 6 | 0 | 0 |
| **u8 – legarda** | 191 | 100.0 | 0.440 | 0.315 | 0.868 | **0.462** | 0.151 | 0.30 | 46 | 100 | 38 | 7 |
| **u9 – lmartinez** | 298 | 100.0 | 0.856 | 0.869 | 0.976 | **0.919** | 0.305 | 0.30 | 245 | 37 | 10 | 6 |
| **u10 – vane** | 131 | 100.0 | 0.809 | 0.809 | 1.000 | **0.895** | 0.000 | 0.30 | 106 | 25 | 0 | 0 |

### Métricas Globales (10 usuarios, 1,337 semanas)

- **Accuracy:** 0.740
- **Precision:** 0.737
- **Recall:** 0.976 ⭐
- **F1-Score:** 0.840 ⭐
- **MCC:** 0.294
- **Umbral:** τ = 0.30

### Matriz de Confusión Global

|  | Predicho: Bajo (0) | Predicho: Alto (1) | **Total** |
|---|---:|---:|---:|
| **Real: Bajo (0)** | TN = 77 | FP = 325 | 402 |
| **Real: Alto (1)** | FN = 22 | TP = 913 | 935 |
| **Total** | 99 | 1,238 | 1,337 |

**Notas:**
- \* `% Datos observados` se calcula como (1 − %imputación total) en la semana promedio del usuario.
- **Alta sensibilidad (Recall = 97.6%):** Apto para screening poblacional; minimiza falsos negativos.
- **Trade-off aceptado:** FP = 325 (26.2% de predicciones positivas); política conservadora preferida en contexto de salud pública.

---

## TABLA 2: Distribución de Clusters por Usuario

| Usuario | Cluster Alto Sed (%) | Cluster Bajo Sed (%) | Diferencia absoluta (%) | Perfil Dominante |
|---------|---------------------:|---------------------:|------------------------:|------------------|
| **u1 – ale** | 99.3 | 0.7 | 98.7 | **Alto Sedentarismo** |
| **u2 – brenda** | 85.7 | 14.3 | 71.4 | **Alto Sedentarismo** |
| **u3 – christina** | 11.3 | 88.7 | 77.3 | **Bajo Sedentarismo** |
| **u4 – edson** | 71.4 | 28.6 | 42.9 | Alto Sedentarismo |
| **u5 – esmeralda** | 64.3 | 35.7 | 28.6 | Alto Sedentarismo |
| **u6 – fidel** | 82.0 | 18.0 | 64.0 | **Alto Sedentarismo** |
| **u7 – kevin** | 94.7 | 5.3 | 89.5 | **Alto Sedentarismo** |
| **u8 – legarda** | 27.7 | 72.3 | 44.5 | **Bajo Sedentarismo** |
| **u9 – lmartinez** | 84.2 | 15.8 | 68.5 | **Alto Sedentarismo** |
| **u10 – vane** | 80.9 | 19.1 | 61.8 | **Alto Sedentarismo** |

### Distribución Global

- **Cluster 1 (Alto Sedentarismo):** 935 semanas (69.9%)
- **Cluster 0 (Bajo Sedentarismo):** 402 semanas (30.1%)

**Notas:**
- **Usuarios con perfil dominante de Alto Sedentarismo (>80%):** u1, u2, u6, u7, u9, u10 (6/10 usuarios).
- **Usuarios con perfil dominante de Bajo Sedentarismo (>70%):** u3, u8 (2/10 usuarios).
- **Usuarios con perfil balanceado (30-70%):** u4, u5 (2/10 usuarios).

---

## TABLA 3: Estadísticos Semanales por Usuario

### Parte A: Actividad y Superávit Calórico

| Usuario | Actividad_rel_p50<br>(media ± std) | Actividad_rel_IQR<br>(media ± std) | Superávit_cal_p50<br>(media ± std) | Superávit_cal_IQR<br>(media ± std) |
|---------|-----------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|
| **u1 – ale** | 0.083 ± 0.029 | 0.041 ± 0.027 | 22.8 ± 5.2 | 9.3 ± 5.8 |
| **u2 – brenda** | 0.161 ± 0.028 | 0.072 ± 0.043 | 33.1 ± 5.0 | 16.3 ± 7.0 |
| **u3 – christina** | 0.145 ± 0.049 | 0.096 ± 0.038 | 46.0 ± 11.0 | 25.7 ± 14.4 |
| **u4 – edson** | 0.163 ± 0.057 | 0.089 ± 0.039 | 21.4 ± 6.9 | 7.9 ± 3.2 |
| **u5 – esmeralda** | 0.163 ± 0.057 | 0.089 ± 0.039 | 32.0 ± 10.4 | 11.9 ± 4.8 |
| **u6 – fidel** | 0.175 ± 0.037 | 0.070 ± 0.067 | 23.8 ± 6.1 | 12.0 ± 6.4 |
| **u7 – kevin** | 0.118 ± 0.038 | 0.054 ± 0.052 | 20.2 ± 4.9 | 8.8 ± 6.0 |
| **u8 – legarda** | 0.166 ± 0.027 | 0.049 ± 0.023 | 47.3 ± 14.0 | 27.5 ± 12.7 |
| **u9 – lmartinez** | 0.111 ± 0.028 | 0.049 ± 0.028 | 35.0 ± 7.7 | 14.9 ± 15.0 |
| **u10 – vane** | 0.091 ± 0.033 | 0.054 ± 0.037 | 25.2 ± 9.8 | 16.0 ± 11.6 |

**Notas sobre Actividad_relativa_p50:**
- **Valores >0.15:** Usuarios muy activos (u2, u3, u4, u5, u6, u8).
- **Valores 0.10-0.15:** Usuarios moderadamente activos (u7, u9).
- **Valores <0.10:** Usuarios con baja actividad relativa (u1, u10).

**Notas sobre Superávit_calórico_basal_p50:**
- **Valores >40% TMB:** Alto gasto energético (u3, u8).
- **Valores 25-40% TMB:** Gasto moderado (u2, u5, u9, u10).
- **Valores <25% TMB:** Bajo gasto energético (u1, u4, u6, u7).

---

### Parte B: HRV, Delta Cardiaco y Score Fuzzy

| Usuario | HRV_SDNN_p50<br>(ms, media ± std) | HRV_SDNN_IQR<br>(media ± std) | Delta_card_p50<br>(lpm, media ± std) | Delta_card_IQR<br>(media ± std) | Score_fuzzy<br>(media ± std) |
|---------|----------------------------------:|------------------------------:|-------------------------------------:|--------------------------------:|-----------------------------:|
| **u1 – ale** | 55.0 ± 6.3 | 11.4 ± 4.9 | 37.0 ± 4.0 | 8.6 ± 4.6 | **0.644 ± 0.211** |
| **u2 – brenda** | 40.7 ± 6.8 | 7.7 ± 3.0 | 40.7 ± 4.8 | 9.1 ± 6.2 | **0.334 ± 0.334** |
| **u3 – christina** | 34.7 ± 8.4 | 12.9 ± 7.8 | 57.4 ± 8.0 | 11.5 ± 4.7 | **0.465 ± 0.250** |
| **u4 – edson** | 38.7 ± 6.8 | 11.2 ± 7.1 | 49.3 ± 4.2 | 12.8 ± 6.0 | **0.719 ± 0.196** |
| **u5 – esmeralda** | 38.7 ± 6.8 | 11.2 ± 7.1 | 49.3 ± 4.2 | 12.8 ± 6.0 | **0.683 ± 0.271** |
| **u6 – fidel** | 33.9 ± 4.7 | 8.7 ± 4.5 | 46.3 ± 6.2 | 9.5 ± 4.5 | **0.638 ± 0.221** |
| **u7 – kevin** | 46.2 ± 7.9 | 13.1 ± 6.1 | 38.5 ± 4.9 | 8.4 ± 4.0 | **0.735 ± 0.243** |
| **u8 – legarda** | 62.8 ± 7.1 | 14.3 ± 6.8 | 35.1 ± 5.1 | 10.3 ± 5.3 | **0.385 ± 0.214** |
| **u9 – lmartinez** | 55.6 ± 10.2 | 15.2 ± 7.5 | 45.3 ± 4.8 | 8.4 ± 4.4 | **0.552 ± 0.180** |
| **u10 – vane** | 52.7 ± 6.7 | 11.8 ± 5.8 | 41.6 ± 5.3 | 10.1 ± 4.8 | **0.612 ± 0.184** |

**Notas sobre HRV_SDNN_p50:**
- **HRV alta (>55 ms):** Buen tono vagal (u1, u8, u9).
- **HRV media (45-55 ms):** Tono vagal moderado (u7, u10).
- **HRV baja (<40 ms):** Tono vagal bajo, posible estrés/desacondicionamiento (u2, u3, u4, u5, u6).

**Notas sobre Delta_cardiaco_p50:**
- **Δ alto (>50 lpm):** Respuesta cardíaca vigorosa al esfuerzo (u3).
- **Δ medio (40-50 lpm):** Respuesta apropiada (u2, u4, u5, u6, u9, u10).
- **Δ bajo (<40 lpm):** Respuesta moderada (u1, u7, u8).

**Notas sobre Score_fuzzy:**
- **Score alto (>0.65):** Sistema fuzzy clasifica como Alto Sedentarismo (u1, u4, u5, u6, u7).
- **Score medio (0.40-0.65):** Zona intermedia (u3, u9, u10).
- **Score bajo (<0.40):** Sistema fuzzy clasifica como Bajo Sedentarismo (u2, u8).

---

## RESUMEN EJECUTIVO DE TABLAS

### Principales Hallazgos

1. **Alta concordancia en usuarios con patrones estables:**
   - **u1 (ale):** F1=0.997, 99.3% de semanas en Alto Sedentarismo → Excelente concordancia.
   - **u7 (kevin):** F1=0.973, 94.7% de semanas en Alto Sedentarismo → Muy buena concordancia.
   - **u6 (fidel), u9 (lmartinez), u10 (vane):** F1>0.89 → Buena concordancia.

2. **Baja concordancia en usuarios con alta variabilidad:**
   - **u3 (christina):** F1=0.215, 88.7% de semanas en Bajo Sedentarismo pero alta variabilidad intra-semanal (IQR alto) → Fuzzy sobreclasifica como Alto.
   - **u8 (legarda):** F1=0.462, 72.3% de semanas en Bajo Sedentarismo pero HRV muy alta (62.8 ms) y actividad moderada-alta → Desacuerdo sistemático.

3. **Usuarios con muestra pequeña:**
   - **u2 (brenda), u4 (edson), u5 (esmeralda):** N<20 semanas → Estadística poco robusta.

4. **Heterogeneidad fisiológica confirmada:**
   - **Actividad_relativa:** Rango 0.083–0.175 (variabilidad 110%).
   - **HRV_SDNN:** Rango 33.9–62.8 ms (variabilidad 85%).
   - **Superávit_calórico:** Rango 20.2–47.3% TMB (variabilidad 134%).

### Recomendaciones para Tesis

1. **Destacar la alta sensibilidad del sistema (Recall=97.6%):** Minimiza falsos negativos, ideal para screening.
2. **Explicar el trade-off FP/FN:** En salud pública, preferible alertar de más (con confirmación) que pasar por alto casos de riesgo.
3. **Discutir heterogeneidad inter-sujeto:** Proponer personalización de τ por usuario o reglas moduladas por IQR.
4. **Usar u1 y u7 como casos de éxito:** Concordancia >94%, perfiles estables.
5. **Usar u3 y u8 como casos de revisión:** Baja concordancia, requieren análisis cualitativo adicional.

---

## ARCHIVOS DISPONIBLES

- ✅ `tabla1_metricas_por_usuario.csv` — Métricas de clasificación por usuario
- ✅ `tabla2_distribucion_clusters.csv` — Distribución de clusters por usuario
- ✅ `tabla3_estadisticos_semanales.csv` — Estadísticos semanales por usuario
- ✅ `TABLAS_COMPLETAS_TESIS.md` — Este documento (formato Markdown)

---

**Fecha de generación:** 18 de octubre de 2025  
**Autor:** Luis Ángel Martínez  
**Proyecto:** Sistema de Inferencia Difusa para Evaluación de Sedentarismo  
**Tesis de Maestría en Ciencias, Semestre 3**



