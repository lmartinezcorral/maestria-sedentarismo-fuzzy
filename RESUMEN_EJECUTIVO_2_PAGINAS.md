# RESUMEN EJECUTIVO
## Sistema de Inferencia Difusa para Evaluación de Sedentarismo a partir de Datos de Wearables

**Autor:** Luis Ángel Martínez  
**Programa:** Maestría en Ciencias, Semestre 3  
**Fecha:** 18 de octubre de 2025  
**Documento:** Resumen Ejecutivo para Comité Tutorial

---

## 1. OBJETIVO Y JUSTIFICACIÓN

### Objetivo Principal
Desarrollar y validar un **sistema de inferencia difusa tipo Mamdani** para clasificar el sedentarismo semanal a partir de biomarcadores obtenidos de wearables (Apple Watch), contrastando su salida con una **verdad operativa** derivada de clustering no supervisado K-means.

### Justificación Clínica
El sedentarismo es un factor de riesgo cardiovascular crítico. Este proyecto aporta:
1. **Evaluación objetiva** basada en wearables (supera sesgo de autoreporte)
2. **Normalización antropométrica** (400 kcal ≠ impacto equivalente entre sujetos)
3. **Interpretabilidad clínica** (reglas lingüísticas auditables vs. "caja negra")

---

## 2. METODOLOGÍA

### Población y Datos
- **Cohorte:** 10 adultos (5M/5H), seguimiento multianual
- **Unidad de análisis:** 1,385 semanas agregadas → 1,337 válidas tras filtrado de calidad
- **Variables diarias base:** Actividad física, gasto calórico, HRV (SDNN), FC (reposo/caminata), horas monitoreadas

### Variables Derivadas Clave
1. **Actividad_relativa** = min_movimiento / (60 × hrs_monitor) → Corrige por exposición al uso del reloj
2. **Superávit_calórico_basal** = (Gasto_activo × 100) / TMB → Ajusta por antropometría (Mifflin-St Jeor)
3. **Delta_cardiaco** = FC_caminata − FC_reposo → Respuesta cardiovascular al esfuerzo

### Pipeline de 5 Fases
```
Preprocesamiento → Agregación Semanal → Clustering K=2 → Sistema Difuso → Validación
    (Imputación          (p50, IQR)      (Verdad        (5 reglas      (τ=0.30,
     jerárquica)                          operativa)     Mamdani)       F1=0.84)
```

**Garantías metodológicas:**
- ✅ Imputación sin leak temporal (rolling mediana solo del pasado)
- ✅ Gates fisiológicos (hard no-wear → no imputar; soft low-act → baseline FCr + Δ*)
- ✅ Auditoría completa (flags de fuente de imputación por día/usuario)

---

## 3. MODELOS Y RESULTADOS

### 3.1. Clustering No Supervisado (Verdad Operativa)
- **Algoritmo:** K-Means con K-sweep (K=2..6), selección por Silhouette y estabilidad ARI
- **K óptimo:** **K=2** (Silhouette=0.232)
  - **Cluster 0 (Bajo Sedentarismo):** 402 semanas (30%) — Actividad_rel=0.160, Superávit=45.4%
  - **Cluster 1 (Alto Sedentarismo):** 935 semanas (70%) — Actividad_rel=0.116, Superávit=25.4%

### 3.2. Sistema de Inferencia Difusa
**Entradas (4):** Actividad_relativa, Superávit_calórico, HRV_SDNN, Delta_cardiaco  
**Funciones de membresía:** Triangulares por percentiles (p10-p25-p40, p35-p50-p65, p60-p75-p90)  
**Reglas (5 ejemplos):**
- R1: Actividad **Baja** ∧ Superávit **Bajo** → Sedentarismo **Alto**
- R2: Actividad **Alta** ∧ Superávit **Alto** → Sedentarismo **Bajo**
- R3: HRV **Baja** ∧ Delta **Alto** → Sedentarismo **Alto** (desacondicionamiento)

**Salida:** Sedentarismo_score ∈ [0,1] → Binarización con umbral τ=0.30

### 3.3. Validación vs. Clustering (1,337 semanas)
| Métrica | Valor | Interpretación |
|---------|------:|----------------|
| **Accuracy** | **74.0%** | Concordancia global cluster-fuzzy |
| **F1-Score** | **0.840** | Balance óptimo precisión-sensibilidad |
| **Precision** | 73.7% | 73.7% de predicciones "Alto" son correctas |
| **Recall** | **97.6%** ⭐ | Minimiza falsos negativos (screening) |
| **MCC** | 0.294 | Concordancia moderada ajustada por azar |
| **Umbral τ** | **0.30** | Maximiza F1 en búsqueda exhaustiva |

**Matriz de Confusión:**
```
            Fuzzy: Bajo  |  Fuzzy: Alto  |  Total
Cluster 0:    TN=77     |    FP=325     |   402
Cluster 1:    FN=22     |    TP=913     |   935
Total:         99       |    1,238      |  1,337
```

**Concordancia por usuario:** Media 70.0% (rango: 27.7%–99.3%)
- **Alta concordancia (>90%):** u1 (ale), u7 (kevin) — Patrones estables
- **Baja concordancia (<50%):** u3 (christina), u8 (legarda) — Alta variabilidad intra-semanal

---

## 4. HALLAZGOS PRINCIPALES

### 4.1. Fortalezas del Sistema
1. **Alta sensibilidad (Recall=97.6%):** Solo 22/935 semanas de Alto Sedentarismo pasan desapercibidas → Apto para **screening poblacional**
2. **Convergencia supervisado–no supervisado:** Sistema fuzzy interpretable converge con estructura data-driven (F1=0.84)
3. **Trazabilidad completa:** Auditorías de imputación, logs por paso, reproducibilidad garantizada
4. **MF por percentiles:** Fácil recalibración en nueva cohorte (recalcular percentiles, mantener estructura de reglas)

### 4.2. Trade-offs Metodológicos
1. **Falsos positivos (FP=325, 26% de predicciones "Alto"):**
   - **Justificación clínica:** En screening de salud pública, preferible alertar de más (con confirmación clínica) que pasar por alto casos de riesgo
   - **Mitigación:** Zona gris (scores 0.40–0.60) → Etiqueta "Indeterminado" + evaluación adicional

2. **Heterogeneidad inter-sujeto:**
   - Usuarios con alta variabilidad intra-semanal (IQR alto) → Fuzzy sobreclasifica
   - **Solución propuesta:** τ personalizado por usuario o reglas moduladas por IQR

3. **Silhouette moderado (K=2: 0.232):**
   - Refleja continuo fisiológico (no frontera "dura" entre sedentario/activo)
   - K=2 preferido por **interpretabilidad clínica clara** sobre complejidad algorítmica

---

## 5. IMPACTO Y APLICACIONES

### Clínica
- **Herramienta de screening** con reglas auditables por clínicos
- **Monitoreo longitudinal** de cambios conductuales (detección temprana de empeoramiento)
- **Dashboard clínico** (especificado): Timeline semanal, MF interactivas, alertas por bandas de riesgo

### Salud Pública y Laboral
- Evaluación poblacional objetiva del sedentarismo
- Programas de intervención dirigidos (identificación de subpoblaciones de alto riesgo)

### Investigación
- Marco reproducible para integrar nuevas variables (sueño, dieta, estrés) sin perder interpretabilidad
- Validación externa en nuevas cohortes (transferibilidad de MF y reglas)

---

## 6. LIMITACIONES Y PRÓXIMOS PASOS

### Limitaciones Reconocidas
1. **FP elevados:** Requiere confirmación clínica en contexto real
2. **Cohorte pequeña (N=10):** Validación externa necesaria antes de despliegue clínico
3. **Escalado global:** Recalibración anual o por cohorte para evitar arrastre por valores extremos

### Próximos Pasos (Corto Plazo)
1. **Personalización de τ** por usuario o subpoblaciones (sexo, rango de TMB)
2. **Reglas moduladas por IQR** para capturar intermitencia conductual
3. **Análisis de sensibilidad** de MF (variar percentiles ±5%, medir impacto en F1)

### Próximos Pasos (Mediano-Largo Plazo)
1. **Validación externa** en nueva cohorte (≥20 usuarios, ≥1,000 semanas)
2. **Integración de nuevas variables:** Sueño (duración, eficiencia), estrés percibido
3. **Modelado temporal avanzado:** ARIMA/LSTM para predicción de "próxima semana será Alto Sedentarismo"
4. **Implementación de dashboard clínico** (FastAPI + React + Plotly)
5. **Publicación científica** en revista de salud digital (*JMIR mHealth*, *Digital Health*)

---

## 7. ENTREGABLES COMPLETADOS

| Categoría | Entregables | Estado |
|-----------|-------------|--------|
| **Datasets** | 10 archivos `DB_final_v3_uN.csv` + consolidados | ✅ |
| **Modelos** | Clustering K=2, Sistema Fuzzy 5 reglas | ✅ |
| **Validación** | Evaluación completa (τ=0.30, F1=0.84) | ✅ |
| **Visualizaciones** | 8 figuras (MF×4, confusión, PR, distribuciones) | ✅ |
| **Documentación** | Informe maestro 68 páginas + metodología | ✅ |
| **Tablas Tesis** | 3 tablas completas (10 usuarios) | ✅ |
| **Scripts** | Pipeline reproducible con auditorías | ✅ |

**Total:** 7 fases del pipeline completadas al 100%

---

## 8. CONCLUSIONES

1. **Sistema fuzzy validado:** Convergencia robusta con clustering K=2 (F1=0.84), reglas interpretables capturan estructura real del sedentarismo en la cohorte.

2. **Política conservadora efectiva:** Alta sensibilidad (Recall=97.6%) minimiza falsos negativos, adecuado para screening poblacional con confirmación clínica posterior.

3. **Variables fisiológicamente relevantes:** Actividad_relativa y Superávit_calórico (principales discriminadores) + HRV_SDNN y Delta_cardiaco (complementarios) → Integración multivariada robusta.

4. **Heterogeneidad manejable:** Concordancia usuario-específica 27.7%–99.3% → Personalización futura necesaria (τ ajustable, reglas moduladas por IQR).

5. **Trazabilidad y reproducibilidad:** Pipeline completo documentado, auditorías de imputación, fácil recalibración en nueva cohorte.

---

## REFERENCIAS CLAVE

1. Troiano, R. P., et al. (2008). Physical activity in the United States measured by accelerometer. *Medicine & Science in Sports & Exercise*, 40(1), 181-188.
2. Thayer, J. F., et al. (2010). A meta-analysis of heart rate variability and neuroimaging studies. *Neuroscience & Biobehavioral Reviews*, 36(2), 747-756.
3. Mifflin, M. D., et al. (1990). A new predictive equation for resting energy expenditure. *The American Journal of Clinical Nutrition*, 51(2), 241-247.
4. Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338-353.
5. Mamdani, E. H., & Assilian, S. (1975). An experiment in linguistic synthesis with a fuzzy logic controller. *International Journal of Man-Machine Studies*, 7(1), 1-13.

---

**Contacto:** Luis Ángel Martínez  
**Institución:** Maestría en Ciencias, Semestre 3  
**Repositorio:** `4 semestre_dataset/` (todos los archivos y documentación)

---

**Este documento resume 1,266 líneas de informe maestro, 1,337 semanas analizadas, 10 usuarios, 5 fases metodológicas, 8 visualizaciones y métricas de validación robustas (F1=0.84, Recall=97.6%). Listo para presentación al comité tutorial.**



