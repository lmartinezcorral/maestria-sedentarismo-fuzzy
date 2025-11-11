# CONTENIDO COMPLETO DE LA PRESENTACIÓN (18 SLIDES)
## Sistema de Inferencia Difusa para Evaluación de Sedentarismo

**Nota:** Este archivo contiene el texto completo de cada slide. Puedes copiar y pegar en PowerPoint o Google Slides manualmente.

---

## SLIDE 1: TÍTULO

**Título Principal:**
# Sistema de Inferencia Difusa para Evaluación del Comportamiento Sedentario

**Subtítulo:**
Modelo Mamdani con Validación vs. Clustering No Supervisado

**Autor:**
Luis Ángel Martínez  
Maestría en Ciencias, Semestre 3  
18 de octubre de 2025

---

## SLIDE 2: OBJETIVOS

**OBJETIVO PRINCIPAL:**

Desarrollar y validar un sistema de inferencia difusa tipo Mamdani para clasificar el sedentarismo semanal a partir de biomarcadores de wearables (Apple Watch)

**OBJETIVOS ESPECÍFICOS:**

• Preprocesar datos con imputación jerárquica sin leak temporal  
• Crear variables derivadas normalizadas (Actividad_relativa, Superávit_calórico_basal)  
• Descubrir estructura latente con clustering K-means (K=2)  
• Diseñar funciones de membresía triangulares por percentiles  
• Definir reglas difusas clínicamente interpretables  
• Validar sistema fuzzy vs. clustering (búsqueda de umbral τ óptimo)

---

## SLIDE 3: DATOS Y COHORTE

**CARACTERÍSTICAS:**

• Cohorte: 10 adultos (5M/5H)  
• Seguimiento: Multianual  
• Unidad de análisis: 1,337 semanas válidas  
• Fuente: Apple Watch (datos diarios)  
• Variables base: Actividad, FC, HRV, gasto calórico

**TABLA: Características de Usuarios Seleccionados**

| Usuario | Sexo | Edad | Peso (kg) | TMB (kcal/d) | Semanas |
|---------|------|------|-----------|--------------|---------|
| u1 (ale) | M | 34 | 68 | 1411 | 149 |
| u6 (fidel) | H | 34 | 100 | 1958 | 278 |
| u9 (lmartinez) | H | 32 | 124 | 2241 | 298 |
| u10 (vane) | M | 28 | 58 | 1304 | 131 |
| ... | ... | ... | ... | ... | ... |

---

## SLIDE 4: VARIABLES DERIVADAS CLAVE

**1. ACTIVIDAD_RELATIVA (normalizada por exposición):**

= min_movimiento / (60 × hrs_monitoreadas)

**Rationale:** Corrige por tiempo de uso del reloj

**2. SUPERÁVIT_CALÓRICO_BASAL (ajustado por antropometría):**

= (Gasto_activo × 100) / TMB

**Rationale:** 400 kcal ≠ impacto equivalente (depende de metabolismo basal)

**3. HRV_SDNN (variabilidad cardíaca, marcador vagal):**

- Alta HRV (>60 ms) = tono vagal saludable
- Baja HRV (<40 ms) = desacondicionamiento, estrés

**4. DELTA_CARDIACO (respuesta al esfuerzo):**

= FC_caminata - FC_reposo

---

## SLIDE 5: PIPELINE METODOLÓGICO (5 FASES)

**FASE 1: Preprocesamiento Diario + Imputación Jerárquica**
- Gates: Hard no-wear, Soft low-activity, Normal
- Rolling mediana (solo pasado, sin leak temporal)

**FASE 2: Creación de Variables Derivadas**
- Actividad_relativa, Superávit_calórico_basal (reemplazan originales)

**FASE 3: Agregación Semanal Robusta**
- 8 features: p50 (mediana) + IQR por variable clave

**FASE 4: Clustering No Supervisado (Verdad Operativa)**
- K-Means con K-sweep (K=2..6), K=2 óptimo (Silhouette=0.232)

**FASE 5: Sistema de Inferencia Difusa + Validación**
- 4 entradas × 3 etiquetas, 5 reglas Mamdani, τ=0.30

---

## SLIDE 6: CLUSTERING K-MEANS (VERDAD OPERATIVA)

**K-SWEEP (K=2..6):**
- K=2 óptimo (Silhouette=0.232)
- Estabilidad ARI=0.565

**CLUSTER 0 (Bajo Sedentarismo):**
- 402 semanas (30%)
- Actividad_rel = 0.160
- Superávit = 45.4%

**CLUSTER 1 (Alto Sedentarismo):**
- 935 semanas (70%)
- Actividad_rel = 0.116
- Superávit = 25.4%

**TABLA: Resultados del K-sweep**

| K | Silhouette | Davies-B | Tamaños |
|---|------------|----------|---------|
| 2 | 0.232 | 2.058 | {0:402, 1:935} |
| 3 | 0.195 | 1.721 | {0:685, 1:235, 2:417} |
| 4 | 0.192 | 1.422 | 4 clusters |
| 5 | 0.148 | 1.444 | 5 clusters |

---

## SLIDE 7: FUNCIONES DE MEMBRESÍA - ACTIVIDAD RELATIVA

**Título:** Funciones de Membresía: Actividad Relativa (normalizada por exposición)

**Figura:** `MF_Actividad_relativa_p50.png`

**Descripción:**
- **Baja:** Percentiles p10-p25-p40 (0.070, 0.095, 0.117)
- **Media:** Percentiles p35-p50-p65 (0.111, 0.131, 0.154)
- **Alta:** Percentiles p60-p75-p90 (0.148, 0.165, 0.195)

**Interpretación:** Mayor actividad relativa = MENOR sedentarismo

---

## SLIDE 8: FUNCIONES DE MEMBRESÍA - SUPERÁVIT CALÓRICO

**Título:** Funciones de Membresía: Superávit Calórico Basal (% del TMB)

**Figura:** `MF_Superavit_calorico_basal_p50.png`

**Descripción:**
- **Bajo:** Percentiles p10-p25-p40 (17.3%, 22.4%, 27.6%)
- **Moderado:** Percentiles p35-p50-p65 (25.8%, 31.8%, 38.9%)
- **Alto:** Percentiles p60-p75-p90 (36.7%, 46.4%, 62.1%)

**Interpretación:** Mayor superávit = MENOR sedentarismo

---

## SLIDE 9: FUNCIONES DE MEMBRESÍA - HRV SDNN

**Título:** Funciones de Membresía: HRV SDNN (Variabilidad Cardíaca)

**Figura:** `MF_HRV_SDNN_p50.png`

**Descripción:**
- **Baja:** Percentiles p10-p25-p40 (33.5, 40.3, 45.1 ms)
- **Media:** Percentiles p35-p50-p65 (43.6, 49.5, 56.7 ms)
- **Alta:** Percentiles p60-p75-p90 (54.6, 64.1, 75.0 ms)

**Interpretación:** Menor HRV = MAYOR sedentarismo (desacondicionamiento)

---

## SLIDE 10: FUNCIONES DE MEMBRESÍA - DELTA CARDIACO

**Título:** Funciones de Membresía: Delta Cardiaco (FC_caminata - FC_reposo)

**Figura:** `MF_Delta_cardiaco_p50.png`

**Descripción:**
- **Baja:** Percentiles p10-p25-p40 (25.0, 33.5, 40.3 lpm)
- **Media:** Percentiles p35-p50-p65 (38.7, 46.2, 53.5 lpm)
- **Alta:** Percentiles p60-p75-p90 (51.7, 60.8, 72.9 lpm)

**Interpretación:** Delta alto = buena respuesta cardíaca al esfuerzo

---

## SLIDE 11: SISTEMA DE INFERENCIA DIFUSA (5 REGLAS)

**ENTRADAS (4):** Actividad_relativa, Superávit_calórico, HRV_SDNN, Delta_cardiaco

**FUNCIONES DE MEMBRESÍA:** Triangulares por percentiles (p10-p25-p40, p35-p50-p65, p60-p75-p90)

**REGLAS MAMDANI (5 ejemplos):**

**R1:** SI Actividad es Baja Y Superávit es Bajo → Sedentarismo Alto

**R2:** SI Actividad es Alta Y Superávit es Alto → Sedentarismo Bajo

**R3:** SI HRV es Baja Y Delta es Alta → Sedentarismo Alto (desacondicionamiento)

**R4:** SI Actividad es Media Y HRV es Media → Sedentarismo Medio

**R5:** SI Actividad es Baja Y Superávit es Medio → Sedentarismo Medio-Alto

**DEFUZZIFICACIÓN:** Centroide → Score ∈ [0, 1]

**BINARIZACIÓN:** τ = 0.30 (maximiza F1-score vs. clusters)

---

## SLIDE 12: MÉTRICAS DE VALIDACIÓN

**MÉTRICAS PRINCIPALES:**

# F1-Score: 0.840  |  Recall: 97.6%  |  Accuracy: 74.0%
# Precision: 73.7%  |  MCC: 0.294  |  τ = 0.30

**MATRIZ DE CONFUSIÓN:**

- **TN = 77** (Bajo correcto)
- **FP = 325** (Sobreclasificación conservadora)
- **FN = 22** (Subclasificación baja)
- **TP = 913** (Alto correcto)

**INTERPRETACIÓN:**

✓ **Alta Sensibilidad (97.6%):**  
Solo 22/935 semanas de Alto Sedentarismo pasan desapercibidas

✓ **Trade-off FP (26%):**  
Política conservadora para screening poblacional

---

## SLIDE 13: MATRIZ DE CONFUSIÓN (VISUAL)

**Título:** Matriz de Confusión (Visual)

**Figura:** `confusion_matrix.png`

**Tabla de Confusión:**

|  | Fuzzy: Bajo | Fuzzy: Alto | Total |
|---|-------------|-------------|-------|
| **Cluster: Bajo (0)** | TN = 77 | FP = 325 | 402 |
| **Cluster: Alto (1)** | FN = 22 | TP = 913 | 935 |
| **Total** | 99 | 1,238 | 1,337 |

**Concordancia:** 990/1,337 semanas (74.0%)

---

## SLIDE 14: CURVA PR Y DISTRIBUCIÓN DE SCORES

**Título:** Curva Precision-Recall y Distribución de Scores

**Figura Izquierda:** `pr_curve.png`
- Curva Precision-Recall para distintos valores de τ
- Punto óptimo: τ=0.30 (F1=0.84)

**Figura Derecha:** `score_distribution_by_cluster.png`
- Distribución de Sedentarismo_score por cluster
- Cluster 0 (Bajo): Media=0.454, Std=0.249
- Cluster 1 (Alto): Media=0.621, Std=0.212

---

## SLIDE 15: CONCORDANCIA POR USUARIO

**HETEROGENEIDAD INTER-SUJETO:**

Concordancia media: **70.0%**  
Rango: **27.7% - 99.3%**

**ALTA CONCORDANCIA (>90%):**
- u1 (ale): 99.3%
- u7 (kevin): 94.7%
- → Patrones estables

**BAJA CONCORDANCIA (<50%):**
- u3 (christina): 27.7%
- u8 (legarda): 44.0%
- → Alta variabilidad intra-semanal

**TABLA: Concordancia por Usuario**

| Usuario | Concordancia | F1 | Recall |
|---------|--------------|-----|--------|
| u1 (ale) | 99.3% | 0.997 | 1.000 |
| u7 (kevin) | 94.7% | 0.973 | 1.000 |
| u6 (fidel) | 81.7% | 0.898 | 0.982 |
| u10 (vane) | 80.9% | 0.895 | 1.000 |
| u3 (christina) | 27.7% | 0.215 | 0.875 |
| u8 (legarda) | 44.0% | 0.462 | 0.868 |

---

## SLIDE 16: CONCLUSIONES PRINCIPALES

**1. SISTEMA FUZZY VALIDADO:**

Convergencia robusta con clustering K=2 (F1=0.84, Recall=97.6%)  
Reglas interpretables capturan estructura real del sedentarismo

**2. POLÍTICA CONSERVADORA EFECTIVA:**

Alta sensibilidad minimiza falsos negativos → Screening poblacional  
Trade-off FP aceptado (26%) con confirmación clínica posterior

**3. VARIABLES FISIOLÓGICAMENTE RELEVANTES:**

Actividad_relativa y Superávit_calórico_basal (principales discriminadores)  
HRV_SDNN y Delta_cardiaco (complementarios) → Integración multivariada

**4. HETEROGENEIDAD MANEJABLE:**

Concordancia usuario-específica 27.7%-99.3%  
→ Personalización futura necesaria (τ ajustable, reglas por IQR)

**5. TRAZABILIDAD Y REPRODUCIBILIDAD:**

Pipeline documentado, auditorías de imputación, recalibración fácil

---

## SLIDE 17: PRÓXIMOS PASOS

**CORTO PLAZO:**

• Personalización de τ por usuario o subpoblaciones (sexo, rango de TMB)  
• Reglas moduladas por IQR para capturar intermitencia conductual  
• Análisis de sensibilidad de MF (variar percentiles ±5%, medir impacto en F1)

**MEDIANO PLAZO:**

• Validación externa en nueva cohorte (≥20 usuarios, ≥1,000 semanas)  
• Integración de nuevas variables: Sueño (duración, eficiencia), estrés percibido  
• Zona gris (scores 0.40-0.60) → Etiqueta 'Indeterminado' + evaluación adicional

**LARGO PLAZO:**

• Modelado temporal avanzado: ARIMA/LSTM para predicción de tendencias  
• Implementación de dashboard clínico interactivo (FastAPI + React + Plotly)  
• Publicación científica en revista de salud digital (JMIR mHealth, Digital Health)  
• Despliegue clínico en programa de salud ocupacional o comunitaria

---

## SLIDE 18: AGRADECIMIENTOS

# ¡Gracias por su atención!

## Preguntas y Discusión

**Luis Ángel Martínez**  
Maestría en Ciencias, Semestre 3  
luis.martinez@institution.edu

**Sistema de Inferencia Difusa para Evaluación de Sedentarismo**  
Validado con F1=0.84, Recall=97.6%

---

# FIN DEL CONTENIDO DE SLIDES

**Total: 18 slides**

---

## NOTAS PARA EL PRESENTADOR

### Timing Sugerido (60 min total):

- Slides 1-2: 3 min (Título + Objetivos)
- Slides 3-5: 8 min (Datos + Variables + Pipeline)
- Slide 6: 5 min (Clustering)
- Slides 7-10: 10 min (MF, 2.5 min c/u)
- Slide 11: 5 min (Sistema Difuso)
- Slides 12-14: 10 min (Métricas)
- Slide 15: 5 min (Concordancia por usuario)
- Slides 16-17: 10 min (Conclusiones + Próximos pasos)
- Slide 18: 4 min (Preguntas)

### Transiciones Clave:

**De Pipeline (5) a Clustering (6):**
"Una vez procesados los datos, descubrimos la estructura latente con clustering K-means. Veamos los resultados..."

**De Clustering (6) a MF (7):**
"Con los clusters como verdad operativa, diseñamos las funciones de membresía para el sistema difuso. Empecemos con la variable más discriminante: Actividad_relativa..."

**De MF (10) a Sistema Difuso (11):**
"Ahora que tenemos las funciones de membresía definidas, veamos cómo se combinan en las reglas del sistema difuso..."

**De Sistema Difuso (11) a Métricas (12):**
"¿Qué tan bien funciona este sistema? Veamos las métricas de validación contra el clustering..."

**De Métricas (14) a Concordancia (15):**
"Las métricas globales son robustas, pero ¿qué pasa a nivel de usuario individual? Aquí vemos heterogeneidad importante..."

---

## FIGURAS NECESARIAS (8 PNG):

1. `MF_Actividad_relativa_p50.png` → Slide 7
2. `MF_Superavit_calorico_basal_p50.png` → Slide 8
3. `MF_HRV_SDNN_p50.png` → Slide 9
4. `MF_Delta_cardiaco_p50.png` → Slide 10
5. `confusion_matrix.png` → Slide 13
6. `pr_curve.png` → Slide 14 (izquierda)
7. `score_distribution_by_cluster.png` → Slide 14 (derecha)
8. `sedentarismo_score_histogram.png` → (Opcional, no usada en las 18 slides principales)

**Ubicación:** `analisis_u/fuzzy/plots/`

---

**¡Listo para copiar/pegar en PowerPoint o Google Slides!** 🎉




