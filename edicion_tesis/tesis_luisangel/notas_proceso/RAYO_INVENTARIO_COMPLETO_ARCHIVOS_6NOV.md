# ⚡ INVENTARIO COMPLETO DE ARCHIVOS - AUDITORÍA TÉCNICA
## Todos los Logs, CSV, PNG y MD Relevantes del Proyecto

**Fecha:** Jueves, 06 de noviembre de 2025, 12:00 hrs  
**Auditor:** Rayo Veloz ⚡ (Agente Técnico Original)  
**Solicitud de:** Luis Ángel Martínez  
**Objetivo:** Documentar TODOS los archivos técnicos para Ades y equipo

---

## 🎯 CONTEXTO DE LA AUDITORÍA

**Luis Ángel solicitó:**
> "Si existen otros logs o archivos relevantes como .csv .png o .md que se me hayan pasado informar, añádelos a la lista de auditoría para que Ades los conozca."

**Acción realizada:**
1. ✅ Ejecutado script LOUO (con bug detectado - reportado abajo)
2. ✅ Búsqueda exhaustiva de todos los archivos técnicos
3. ✅ Clasificación por tipo y relevancia
4. ✅ Documentación de rutas completas

---

## 📊 ESTADÍSTICAS GENERALES

| Tipo | Cantidad | Ubicación Principal |
|------|----------|---------------------|
| **Logs (.txt)** | 10 | `4 semestre_dataset/analisis_u/` |
| **CSV** | 155+ | `4 semestre_dataset/analisis_u/` |
| **PNG** | 180+ | `4 semestre_dataset/analisis_u/` |
| **MD** | 12 | `4 semestre_dataset/documentos_tesis/` |
| **Scripts Python** | 30+ | `4 semestre_dataset/` |

---

## 📁 SECCIÓN 1: LOGS DE EJECUCIÓN (.txt)

### **LOGS CRÍTICOS (Pipeline Principal):**

#### **1. Control de Insumos**
```
4 semestre_dataset/control_insumos_log.txt
```
- **Fecha:** 2025-10-16 14:09:34
- **Contenido:** 
  - Cohorte 10 usuarios (datos demográficos completos)
  - TMB calculados
  - % Imputación FC_walk por usuario (10%-35%)
  - Días monitoreados totales: 9,185 días

#### **2. Agregación Semanal**
```
4 semestre_dataset/04_agregacion_semanal_log.txt
```
- **Fecha:** 2025-10-16 17:03:05
- **Contenido:**
  - 1,385 semanas generadas
  - Cobertura promedio: 6.6/7 días por semana
  - Criterios de validez aplicados

#### **3. Variabilidad Dual (Panel A/B)**
```
4 semestre_dataset/analisis_u/variabilidad/03_variabilidad_dual_log.txt
```
- **Fecha:** 2025-10-16 15:59:36
- **Contenido:**
  - Coeficientes de variación (CV) por usuario
  - Comparación operativa vs observada
  - Hallazgo: CV similar entre ambos paneles

#### **4. Missingness y ACF**
```
4 semestre_dataset/analisis_u/missingness_y_acf/05_missingness_y_acf_log.txt
```
- **Fecha:** 2025-10-16 19:45 hrs (aprox)
- **Contenido:**
  - Patrones de datos faltantes por usuario
  - Análisis de autocorrelación (ACF/PACF)
  - Lag significativos detectados

#### **5. Precluster QC (Control de Calidad)**
```
4 semestre_dataset/analisis_u/semanal/precluster/06_precluster_qc_log.txt
```
- **Fecha:** 2025-10-16 17:30 hrs (aprox)
- **Contenido:**
  - VIF (Variance Inflation Factor)
  - Matriz de correlación 4 variables
  - PCA y t-SNE preprocesamiento

#### **6. Clustering K-Means**
```
4 semestre_dataset/analisis_u/clustering/06_clustering_log.txt
```
- **Fecha:** 2025-10-16 18:32:31
- **Contenido:** ⭐ **CRÍTICO**
  - K óptimo = 2
  - Silhouette Score = 0.232
  - Cluster 0: 402 semanas (30.1%)
  - Cluster 1: 935 semanas (69.9%)
  - 1,337 semanas válidas finales

#### **7. Sistema Difuso (Fuzzy Inference)**
```
4 semestre_dataset/analisis_u/fuzzy/08_fuzzy_inference_log.txt
```
- **Fecha:** 2025-10-17 17:25 hrs (aprox)
- **Contenido:** ⭐ **CRÍTICO**
  - Configuración 5 reglas Mamdani
  - Score promedio: 0.571 ± 0.235
  - 1,385 semanas procesadas

#### **8. Evaluación Fuzzy vs Clustering**
```
4 semestre_dataset/analisis_u/fuzzy/09_eval_fuzzy_vs_cluster.txt
```
- **Fecha:** 2025-10-17 18:42:59
- **Contenido:** ⭐⭐⭐ **MUY CRÍTICO - MÉTRICAS OFICIALES**
  - Umbral óptimo τ = 0.30
  - Accuracy: 0.740
  - Precision: 0.737
  - Recall: 0.976
  - F1-Score: 0.840
  - MCC: 0.294
  - Matriz confusión: TN=77, FP=325, FN=22, TP=913

#### **9. LOUO Validation (RECIÉN GENERADO)**
```
4 semestre_dataset/analisis_u/loou_results/loou_global_report.txt
```
- **Fecha:** 2025-11-06 11:58:59
- **Contenido:** ⚠️ **BUG DETECTADO**
  - F1-Score: 0.000 (TODOS los folds)
  - Accuracy promedio: 0.280
  - **PROBLEMA:** Script no está clasificando correctamente
  - **ACCIÓN:** Requiere debugging (ver Sección 5 abajo)

#### **10. Reporte Markov (Predicción)**
```
4 semestre_dataset/analisis_u/prediccion/reporte_markov.txt
```
- **Fecha:** Desconocida
- **Contenido:**
  - Matriz de transición de estados
  - Predicción de comportamiento futuro

---

## 📁 SECCIÓN 2: CSV DE DATOS Y RESULTADOS

### **A. DATASETS PRINCIPALES (Consolidados):**

#### **Dataset Semanal Consolidado** ⭐⭐⭐
```
4 semestre_dataset/analisis_u/semanal/weekly_consolidado.csv
```
- **Filas:** 1,385 semanas
- **Columnas:** ~60 variables
- **Contenido:** Medianas (p50), IQR (p25-p75), percentiles p10/p90 de todas las variables

#### **Cluster Inputs (4 Variables Derivadas)**
```
4 semestre_dataset/analisis_u/semanal/cluster_inputs_weekly.csv
```
- **Filas:** 1,385 semanas
- **Columnas:** 8 features (4 variables × p50/IQR)
- **Variables:** Actividad_relativa, Superavit_calorico_basal, HRV_SDNN, Delta_cardiaco

#### **Datasets Semanales por Usuario (10 archivos)**
```
4 semestre_dataset/analisis_u/semanal/
├── weekly_u1.csv (159 semanas)
├── weekly_u2.csv (8 semanas)
├── weekly_u3.csv (141 semanas)
├── weekly_u4.csv (15 semanas)
├── weekly_u5.csv (15 semanas)
├── weekly_u6.csv (303 semanas)
├── weekly_u7.csv (117 semanas)
├── weekly_u8.csv (192 semanas)
├── weekly_u9.csv (302 semanas)
└── weekly_u10.csv (133 semanas)
```

---

### **B. RESULTADOS DE CLUSTERING:**

```
4 semestre_dataset/analisis_u/clustering/
├── cluster_assignments.csv         (1,337 semanas con cluster asignado)
├── cluster_centroids.csv            (Centroides K=2)
├── cluster_profiles.csv             (Perfiles estadísticos por cluster)
└── model_selection_metrics.csv     (Silhouette, Inertia, K-sweep)
```

---

### **C. RESULTADOS DEL SISTEMA DIFUSO:**

```
4 semestre_dataset/analisis_u/fuzzy/
├── fuzzy_output.csv                (1,385 semanas con scores difusos 0-1)
└── discordancias_top20.csv         (20 casos discordantes para revisión clínica)
```

---

### **D. VARIABILIDAD (Panel A/B):**

```
4 semestre_dataset/analisis_u/variabilidad/
├── variabilidad_dual_consolidado.csv (Resumen todos los usuarios)
├── variabilidad_dual_u1.csv ... variabilidad_dual_u10.csv (30 archivos)
├── variabilidad_operativa_u1.csv ... u10 (10 archivos)
├── variabilidad_observada_u1.csv ... u10 (10 archivos)
└── std_u1.csv ... std_u10.csv (10 archivos - desviaciones estándar)
```

---

### **E. MISSINGNESS Y AUTOCORRELACIÓN:**

```
4 semestre_dataset/analisis_u/missingness_y_acf/
├── missingness_consolidado.csv     (Patrón de faltantes agregado)
├── acf_consolidado.csv              (ACF/PACF agregado)
├── missingness_resumen_u1.csv ... u10 (10 archivos)
└── acf_stats_u1.csv ... u10.csv     (10 archivos)
```

---

### **F. IMPUTACIÓN FC_WALK (V3):**

```
4 semestre_dataset/analisis_u/
├── FC_walk_imputacion_V3_u1.csv
├── FC_walk_imputacion_V3_u2.csv
... (10 archivos, uno por usuario)
└── FC_walk_imputacion_V3_u10.csv
```

---

### **G. PRECLUSTER (PCA, t-SNE, VIF):**

```
4 semestre_dataset/analisis_u/semanal/precluster/
├── scaled_matrix.csv                (Matriz normalizada)
├── features_correlacion.csv         (Matriz correlación 4V)
├── features_vif.csv                 (VIF multicolinealidad)
├── pca_2d.csv                       (Proyección PCA 2D)
├── k_sweep_metrics.csv              (K=2-10 evaluación)
├── PCA_LOADINGS_4V.csv              (Cargas principales)
├── PCA_LOADINGS_3D.csv
└── DATASET_SEMANAL_CON_PCA_TSNE.csv (Con proyecciones)
```

---

### **H. ANÁLISIS SF-36 (Validación Convergente):**

```
4 semestre_dataset/analisis_u/
├── TABLA_COMPARATIVA_SF36_FUZZY_N9.csv  (Tabla consolidada N=9)
├── correlaciones_sf36_fuzzy_N9.csv      (Correlaciones actualizadas)
├── TABLA_USUARIOS_SF36_FUZZY.csv        (Datos por usuario)
└── correlaciones_sf36_fuzzy.csv         (Primera versión N=8)
```

---

### **I. PREDICCIÓN MARKOV:**

```
4 semestre_dataset/analisis_u/prediccion/
├── matriz_transicion_global.csv         (Transiciones de estados)
├── matriz_transicion_global_probs.csv   (Probabilidades)
├── matriz_transicion_por_usuario.csv    (Markov por usuario)
├── predicciones_backtest.csv            (Validación histórica)
├── prediccion_proxima_semana_por_usuario.csv
└── semaforo_semanal.csv                 (Clasificación verde/amarillo/rojo)
```

---

### **J. SENSIBILIDAD DE PARÁMETROS:**

```
4 semestre_dataset/analisis_u/sensibilidad/
└── sensibilidad_tau.csv                 (Grid search τ=0.10-0.70)
```

---

### **K. ANÁLISIS DESCRIPTIVOS VISUALES:**

```
4 semestre_dataset/analisis_u/descriptivos_visuales/
└── tabla_descriptivos_actualizados.csv  (Estadísticos por usuario y variable)
```

---

### **L. CORRELACIONES Y VARIABILIDAD (Legacy):**

```
4 semestre_dataset/analisis_u/
├── comparativo_correlacion_flat.csv
├── comparativo_variabilidad.csv
└── DB_final_v3_u1..u10_* (60 archivos variabilidad/correlación legacy)
```

---

### **M. VALIDACIÓN LOUO (RECIÉN GENERADO):**

```
4 semestre_dataset/analisis_u/loou_results/
├── loou_global_report.txt               ⚠️ BUG - F1=0.000 (ver Sección 5)
└── loou_summary.csv                     ⚠️ BUG - Todos los scores 0
```

---

## 📁 SECCIÓN 3: PLOTS Y FIGURAS (.png)

### **A. FUZZY SYSTEM (Sistema Difuso):**

```
4 semestre_dataset/analisis_u/fuzzy/plots/
├── confusion_matrix.png                 ⭐ Matriz confusión τ=0.30
├── pr_curve.png                         ⭐ Curva Precision-Recall
└── score_distribution_by_cluster.png   ⭐ Distribución scores por cluster
```

```
4 semestre_dataset/analisis_u/fuzzy/
├── DIAGRAMA_FLUJO_FIS.png               (Flujo sistema inferencia)
├── MEMBRESIAS_3_CASOS.png               (3 casos ejemplo)
├── PIPELINE_COMPLETO_3_CASOS.png        (Pipeline visual)
├── SCORES_COMPARATIVOS_3_CASOS.png      (Comparación scores)
├── VISUALIZACION_3_CASOS_FUZZY.png      (Interpretación clínica)
└── TABLA_INTERPRETACION_CLINICA.png     (Tabla visual)
```

```
4 semestre_dataset/analisis_u/fuzzy/plots/
├── MF_Actividad_relativa_p50.png        (Función de membresía)
├── MF_Superavit_calorico_basal_p50.png
├── MF_HRV_SDNN_p50.png
└── MF_Delta_cardiaco_p50.png
```

---

### **B. CLUSTERING:**

```
(No se generaron plots PNG en directorio clustering/, solo CSV)
```

---

### **C. PRECLUSTER (PCA, t-SNE, K-sweep):**

```
4 semestre_dataset/analisis_u/semanal/precluster/
├── PCA_4_VARIABLES_CORRECTAS.png        ⭐ PCA 2D con clusters
├── TSNE_4_VARIABLES_CORRECTAS.png       ⭐ t-SNE 2D
├── COMPARATIVA_PCA_TSNE_4V.png          ⭐ Comparación lado a lado
├── PCA_LOADINGS_HEATMAP_4V.png          (Cargas principales)
├── SCREE_PLOT_4V.png                    (Varianza explicada)
├── PCA_POR_USUARIO_4V.png               (Proyección por usuario)
├── PCA_3D_4_VISTAS.png                  (4 ángulos 3D)
└── PCA_PROYECCIONES_2D_DE_3D.png        (2D desde 3D)
```

---

### **D. MISSINGNESS Y ACF (80 archivos - 10 usuarios × 4 variables × 2 tipos):**

#### **ACF Plots (40 archivos):**
```
4 semestre_dataset/analisis_u/missingness_y_acf/acf_plots/
├── acf_Actividad_relativa_p50_u1.png ... u10.png (10 archivos)
├── acf_Actividad_relativa_iqr_u1.png ... u10.png (10 archivos)
├── acf_Superavit_calorico_basal_p50_u1.png ... u10.png (10 archivos)
├── acf_Superavit_calorico_basal_iqr_u1.png ... u10.png (10 archivos)
├── acf_HRV_SDNN_p50_u1.png ... u10.png (10 archivos)
├── acf_HRV_SDNN_iqr_u1.png ... u10.png (10 archivos)
├── acf_Delta_cardiaco_p50_u1.png ... u10.png (10 archivos)
└── acf_Delta_cardiaco_iqr_u1.png ... u10.png (10 archivos)
```

#### **PACF Plots (40 archivos):**
```
4 semestre_dataset/analisis_u/missingness_y_acf/pacf_plots/
└── [Misma estructura que acf_plots/]
```

---

### **E. DESCRIPTIVOS VISUALES:**

```
4 semestre_dataset/analisis_u/descriptivos_visuales/
├── violin_plots_por_usuario.png         ⭐ Distribuciones por usuario
├── grouped_bar_medianas_por_usuario.png ⭐ Barras agrupadas
├── heatmap_patron_semanal.png           (Patrón temporal)
├── scatter_matrix_relaciones.png        (Matriz de dispersión)
├── boxplots_comparativos.png            ⭐ Boxplots 4 variables
└── histogramas_con_kde.png              (Histogramas + densidad)
```

---

### **F. ANÁLISIS SF-36:**

```
4 semestre_dataset/analisis_u/
├── HEATMAP_SF36_FUZZY.png               ⭐ Correlaciones fuzzy vs SF-36
├── SCATTER_SF36_FUZZY_TOP4.png          (Top 4 dimensiones)
├── TABLA_VISUAL_SF36_FUZZY.png          (Tabla visual)
├── HEATMAP_SF36_FUZZY_N9.png            (Actualizado N=9)
├── SCATTER_SF36_FUZZY_N9_TOP6.png       (Top 6 dimensiones N=9)
├── SCATTER_SF36_FUZZY_N9_COMPLETO.png   (Todas las dimensiones)
├── TABLA_COMPARATIVA_SF36_FUZZY_N9_VISUAL.png
└── BARPLOT_COMPARATIVO_FUZZY_SF36_N9.png
```

---

### **G. VISUALIZACIONES GENERALES:**

```
4 semestre_dataset/analisis_u/
├── boxplots_por_usuario.png             ⭐ Distribución 4 variables por usuario
├── histogramas_variables_clave.png      (4 histogramas)
└── qqplots_normalidad.png               (Q-Q plots Shapiro-Wilk)
```

---

### **H. LOUO PLOTS (RECIÉN GENERADO):**

```
4 semestre_dataset/analisis_u/loou_results/plots/
└── f1_by_user.png                       ⚠️ BUG - Todos F1=0.000
```

---

## 📁 SECCIÓN 4: DOCUMENTOS MARKDOWN (.md)

### **DOCUMENTOS TÉCNICOS PRINCIPALES:**

#### **1. Roadmap del Proyecto** ⭐⭐⭐
```
4 semestre_dataset/documentos_tesis/ROADMAP_PROYECTO_COMPLETO.md
```
- **Líneas:** 775
- **Contenido:** Historia completa 2023-2025, fases, pipeline, decisiones

#### **2. Informe Maestro Sistema Difuso** ⭐⭐⭐
```
4 semestre_dataset/documentos_tesis/INFORME_MAESTRO_SISTEMA_DIFUSO_SEDENTARISMO.md
```
- **Líneas:** 1,267
- **Contenido:** Sistema fuzzy completo, reglas, parámetros, validación

#### **3. Síntesis MCC y Métricas** ⭐⭐
```
4 semestre_dataset/documentos_tesis/SINTESIS_PARA_GEMINI_MCC.md
```
- **Líneas:** ~200
- **Contenido:** Matriz confusión, métricas, interpretación MCC

#### **4. Perfiles de Clusters** ⭐⭐
```
4 semestre_dataset/documentos_tesis/perfil_clusters_completo.md
```
- **Líneas:** ~300
- **Contenido:** Características de Cluster 0 vs Cluster 1, estadísticos Mann-Whitney

#### **5. Análisis de Robustez** ⭐
```
4 semestre_dataset/documentos_tesis/analisis_robustez.md
```
- **Líneas:** ~250
- **Contenido:** Modelo 4V vs 2V, análisis ablación

#### **6. Resumen Ejecutivo Pipeline**
```
4 semestre_dataset/documentos_tesis/RESUMEN_EJECUTIVO_PIPELINE.md
```
- **Líneas:** ~400
- **Contenido:** Pipeline completo en formato ejecutivo

#### **7. Resumen Trabajo Técnico Completo**
```
4 semestre_dataset/documentos_tesis/RESUMEN_TRABAJO_TECNICO_COMPLETO.md
```
- **Líneas:** 795
- **Contenido:** Timeline completo, todos los scripts, datasets, hallazgos

#### **8. Inventario Recursos Poseidón**
```
4 semestre_dataset/documentos_tesis/INVENTARIO_RECURSOS_POSEIDON.md
```
- **Líneas:** ~600
- **Contenido:** Lista completa de 178 figuras + 64 tablas para artículo IEEE

#### **9. Resumen Entrega Octubre 2025**
```
4 semestre_dataset/documentos_tesis/RESUMEN_ENTREGA_OCTUBRE_2025.md
```
- **Líneas:** ~300
- **Contenido:** Estado del proyecto a final de octubre

#### **10-12. README y Modificaciones**
```
4 semestre_dataset/documentos_tesis/
├── README_DOCUMENTOS_TESIS.md
├── README_INFORME_LATEX.md
├── RESUMEN_MODIFICACIONES_FIGURAS.md
└── PLAN_COMPILACION_PDF.md
```

---

## 📁 SECCIÓN 5: PROBLEMA CRÍTICO DETECTADO - SCRIPT LOUO

### 🚨 **BUG EN VALIDACIÓN LOOU:**

**Script ejecutado:**
```
4 semestre_dataset/10_leave_one_user_out_validation.py
```

**Resultado:** ❌ **FALLA COMPLETA**
```
F1-Score: 0.000 ± 0.000 (en TODOS los 10 folds)
Precision: 0.000 (en TODOS)
Recall: 0.000 (en TODOS)
```

**Diagnóstico preliminar:**
- ✅ Script ejecuta sin errores Python
- ✅ Lee datos correctamente (1,385 semanas)
- ✅ Split train/test correcto (ej: u1 = 1,226 train / 159 test)
- ❌ Sistema fuzzy NO clasifica positivos (TP=0 en todos los folds)
- ❌ F1_train también es 0.000 (problema en optimización de τ)

**Causa probable:**
1. Funciones de membresía mal parametrizadas en LOUO (percentiles calculados incorrectamente)
2. Sistema difuso no genera scores >0 (problema en fuzzify o inference)
3. Normalización incorrecta entre train/test

**Acción requerida:**
- 🔴 **CRÍTICO:** Script necesita debugging antes de usar resultados
- 🔴 **NO USAR** los plots/CSV generados por este script
- 🔴 **MANTENER** métricas de `09_eval_fuzzy_vs_cluster.txt` (esas SÍ son correctas)

**Siguiente paso:**
- Luis debe decidir si debuggear script LOUO ahora
- O usar métricas globales (0.740/0.737/0.976/0.840) como oficiales
- Tabla 6.2 de la tesis (con métricas por usuario) podría ser SIMULADA o de otra fuente

---

## 📊 SECCIÓN 6: RESUMEN DE ARCHIVOS POR CATEGORÍA

### **LOGS (10 archivos):**
1. ✅ control_insumos_log.txt
2. ✅ 04_agregacion_semanal_log.txt
3. ✅ 03_variabilidad_dual_log.txt
4. ✅ 05_missingness_y_acf_log.txt
5. ✅ 06_precluster_qc_log.txt
6. ✅ 06_clustering_log.txt ⭐⭐⭐
7. ✅ 08_fuzzy_inference_log.txt ⭐⭐
8. ✅ 09_eval_fuzzy_vs_cluster.txt ⭐⭐⭐
9. ✅ reporte_markov.txt
10. ⚠️ loou_global_report.txt (BUG DETECTADO)

### **CSV (155 archivos):**
- 🟢 **10 datasets semanales** por usuario
- 🟢 **1 consolidado** principal (1,385 semanas)
- 🟢 **4 CSV clustering** (assignments, centroids, profiles, metrics)
- 🟢 **2 CSV fuzzy** (output, discordancias)
- 🟢 **40 CSV variabilidad** (dual, operativa, observada, std)
- 🟢 **20 CSV missingness/ACF**
- 🟢 **10 CSV imputación** FC_walk
- 🟢 **7 CSV precluster** (PCA, VIF, correlación)
- 🟢 **8 CSV SF-36**
- 🟢 **7 CSV predicción** Markov
- 🟢 **1 CSV sensibilidad** τ
- 🟢 **~45 CSV legacy** (correlaciones, variabilidad antiguas)

### **PNG (180+ archivos):**
- 🟢 **6 plots fuzzy** principales
- 🟢 **4 plots fuzzy** membresías
- 🟢 **8 plots precluster** (PCA, t-SNE)
- 🟢 **80 plots ACF/PACF** (4 vars × 2 tipos × 10 usuarios)
- 🟢 **6 plots descriptivos** visuales
- 🟢 **8 plots SF-36**
- 🟢 **3 plots generales** (boxplots, histogramas, Q-Q)
- 🟢 **1 plot LOOU** (con bug)

### **MD (12 archivos):**
- ✅ ROADMAP_PROYECTO_COMPLETO.md ⭐⭐⭐
- ✅ INFORME_MAESTRO_SISTEMA_DIFUSO_SEDENTARISMO.md ⭐⭐⭐
- ✅ SINTESIS_PARA_GEMINI_MCC.md ⭐⭐
- ✅ perfil_clusters_completo.md ⭐⭐
- ✅ analisis_robustez.md ⭐
- ✅ RESUMEN_TRABAJO_TECNICO_COMPLETO.md
- ✅ RESUMEN_EJECUTIVO_PIPELINE.md
- ✅ INVENTARIO_RECURSOS_POSEIDON.md
- ✅ RESUMEN_ENTREGA_OCTUBRE_2025.md
- ✅ README_DOCUMENTOS_TESIS.md
- ✅ README_INFORME_LATEX.md
- ✅ RESUMEN_MODIFICACIONES_FIGURAS.md

---

## 🎯 SECCIÓN 7: ARCHIVOS CRÍTICOS PARA ADES

### **LECTURA OBLIGATORIA (Top 5):**

1. ⭐⭐⭐ **09_eval_fuzzy_vs_cluster.txt** (Métricas oficiales: 0.740/0.737/0.976/0.840/0.294)
2. ⭐⭐⭐ **06_clustering_log.txt** (Silhouette=0.232, K=2, 1,337 semanas)
3. ⭐⭐⭐ **control_insumos_log.txt** (Cohorte 10 usuarios, 9,185 días)
4. ⭐⭐ **ROADMAP_PROYECTO_COMPLETO.md** (Historia 2023-2025)
5. ⭐⭐ **INFORME_MAESTRO_SISTEMA_DIFUSO_SEDENTARISMO.md** (Sistema completo)

### **PLOTS CRÍTICOS PARA VALIDAR TESIS:**

1. ⭐⭐⭐ **confusion_matrix.png** (Matriz oficial)
2. ⭐⭐ **pr_curve.png** (Curva Precision-Recall)
3. ⭐⭐ **PCA_4_VARIABLES_CORRECTAS.png** (Separación bimodal)
4. ⭐ **boxplots_por_usuario.png** (Heterogeneidad inter-sujeto)

### **CSV CRÍTICOS PARA VERIFICAR NÚMEROS:**

1. ⭐⭐⭐ **cluster_assignments.csv** (Verdad operativa 1,337 semanas)
2. ⭐⭐⭐ **fuzzy_output.csv** (Scores difusos 1,385 semanas)
3. ⭐⭐ **cluster_profiles.csv** (Perfiles estadísticos Cluster 0/1)
4. ⭐⭐ **features_vif.csv** (Multicolinealidad)

---

## 📢 MENSAJE PARA ADES

**Ades,**

**INVENTARIO COMPLETO DE ARCHIVOS TÉCNICOS:**
- 📊 **10 logs** de ejecución (2023-10 a 2025-11-06)
- 📊 **155+ CSV** con datos y resultados
- 📊 **180+ PNG** con visualizaciones
- 📊 **12 MD** con documentación técnica

**ARCHIVOS CRÍTICOS PARA TU REVISIÓN:**
- Los 8 primeros logs (NO el #10 de LOOU - tiene bug)
- Los 4 CSV principales (cluster_assignments, fuzzy_output, cluster_profiles, weekly_consolidado)
- Los 4 plots principales (confusion_matrix, pr_curve, PCA, boxplots)
- Los 5 MD top (ROADMAP, INFORME_MAESTRO, SINTESIS_MCC, perfil_clusters, analisis_robustez)

**ADVERTENCIA CRÍTICA:**
- ⚠️ Script LOOU (10_leave_one_user_out_validation.py) tiene BUG
- ⚠️ NO usar outputs de loou_results/ hasta debugging
- ⚠️ Tabla 6.2 de tesis (métricas por usuario LOOU) podría ser simulada o de fuente diferente
- ✅ Métricas OFICIALES están en `09_eval_fuzzy_vs_cluster.txt` (17-Oct-2025)

---

## 🚨 ALERTAS PARA LUIS ÁNGEL

**Luis,**

**PROBLEMA DETECTADO:**
1. ✅ Script LOOU ejecutado exitosamente (7 segundos)
2. ❌ Resultados INVÁLIDOS (F1=0.000 en todos los folds)
3. ⚠️ Tabla 6.2 de tu tesis muestra métricas diferentes (F1 rango 0.215-0.997)
4. ❓ ¿De dónde salieron las métricas de Tabla 6.2?

**OPCIONES:**

**A. Debuggear script LOOU ahora** (1-2 horas)
- Identificar por qué sistema fuzzy no clasifica positivos
- Corregir lógica de normalización train/test
- Re-ejecutar y verificar métricas

**B. Usar métricas globales (sin LOUO)** (5 minutos)
- Mantener F1=0.840 como métrica principal
- Eliminar Tabla 6.2 (métricas por usuario)
- Simplificar narrativa Cap. 6

**C. Verificar fuente de Tabla 6.2** (30 minutos)
- ¿Hay otro log o CSV con métricas LOOU?
- ¿Script diferente que generó esos datos?
- ¿Fueron calculados manualmente?

**¿Qué opción prefieres?** 🎯

---

**Timestamp:** Jueves, 06 de noviembre de 2025, 12:02:45  
**Auditor:** ⚡ Rayo Veloz  
**Estado:** ✅ Inventario completo | ⚠️ Bug LOOU detectado | ⏳ Esperando decisión

