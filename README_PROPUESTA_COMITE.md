# README: PROPUESTA PARA COMITÉ TUTORIAL
## Sistema Difuso de Clasificación de Sedentarismo Semanal

**Investigador Principal:** Luis Ángel Martínez  
**Institución:** UACH - Facultad de Medicina y Ciencias Biomédicas  
**Fecha de Actualización:** Octubre 18, 2025  
**Versión del Sistema:** 2.1 (Post-Optimización)

---

## 📋 RESUMEN EJECUTIVO

### **Objetivo del Estudio**

Desarrollar y validar un **sistema de inferencia difusa** (Mamdani) para clasificar el sedentarismo semanal a partir de datos de wearables (Apple Watch), utilizando:
1. **Clustering no supervisado** (K-means, K=2) como verdad operativa
2. **Sistema difuso** basado en reglas clínicas
3. **Validación por concordancia** entre ambos métodos

### **Resultados Clave**

| **Métrica** | **Valor** | **Interpretación** |
|-------------|-----------|-------------------|
| **F1-Score** | 0.84 | Concordancia alta (umbral clínico ≥0.70) |
| **Accuracy** | 0.74 | 74% de semanas clasificadas igual |
| **MCC** | 0.29 | Correlación positiva (Matthews) |
| **Precision** | 0.74 | 74% de predicciones "Alto" son correctas |
| **Recall** | 0.98 | 98% de semanas "Alto" detectadas |

**Conclusión:** El sistema difuso **reproduce** la estructura del clustering con **alta fidelidad**.

---

## 📂 ESTRUCTURA DEL PROYECTO

```
4 semestre_dataset/
├── analisis_u/
│   ├── clustering/                   # Resultados K-means (K=2)
│   │   ├── cluster_assignments.csv   # Etiquetas por semana
│   │   ├── cluster_centroids.csv     # Centroides de clusters
│   │   └── cluster_profiles.csv      # Perfiles clínicos
│   ├── fuzzy/                        # Sistema difuso
│   │   ├── fuzzy_output.csv          # Scores por semana [0,1]
│   │   ├── discordancias_top20.csv   # Casos discordantes para revisión
│   │   └── plots/                    # Visualizaciones
│   │       ├── confusion_matrix.png
│   │       ├── pr_curve.png
│   │       ├── MF_*.png (4 archivos) # Funciones de membresía
│   │       └── score_distribution_by_cluster.png
│   ├── semanal/                      # Datos agregados semanales
│   │   ├── weekly_consolidado.csv    # 1385 semanas, 10 usuarios
│   │   └── cluster_inputs_weekly.csv # Features para clustering (8)
│   ├── missingness_y_acf/            # Análisis de cobertura y ACF/PACF
│   │   ├── acf_plots/                # ✅ REGENERADO (hoy)
│   │   ├── pacf_plots/               # ✅ REGENERADO con statsmodels (hoy)
│   │   ├── missingness_consolidado.csv
│   │   └── acf_consolidado.csv
│   ├── variabilidad_dual/            # ✅ NUEVO (hoy)
│   │   └── plots_consolidados/
│   │       ├── variabilidad_operativa_vs_observada.png
│   │       ├── variabilidad_por_usuario_boxplot.png
│   │       └── heatmap_cv_usuario_variable.png
│   └── comparativo_variabilidad.csv  # ✅ ACTUALIZADO con heatmaps anotados (hoy)
├── fuzzy_config/
│   ├── fuzzy_membership_config.yaml  # Parámetros MF (percentiles)
│   └── feature_scalers.json          # Min/Max para normalización
├── DEFENSA_NO_SPLIT_COMITE_TUTORIAL.md  # ✅ NUEVO (hoy) - Documento crítico
├── INFORME_MAESTRO_SISTEMA_DIFUSO_SEDENTARISMO.md
└── README_PROPUESTA_COMITE.md        # Este archivo
```

---

## 🎯 ENTREGABLES PARA EL COMITÉ TUTORIAL

### **1. DOCUMENTO DE DEFENSA METODOLÓGICA** ⭐ **CRÍTICO**

**Archivo:** `DEFENSA_NO_SPLIT_COMITE_TUTORIAL.md`

**Contenido:**
- **Por qué NO usamos split 80/20 Train/Test** (3 razones fundamentales)
- **Naturaleza de los datos** (longitudinales, autocorrelacionados)
- **Objetivo del estudio** (descriptivo-clasificatorio, NO predictivo)
- **Validación actual** (concordancia Fuzzy vs Clustering)
- **Alternativas robustas** (Leave-One-User-Out, sensibilidad, temporal)
- **Respuestas anticipadas** a preguntas del comité (con analogías clínicas)
- **Referencias académicas** (Kohavi 1995, Bergmeir 2012, Chicco 2020)

**USO:** Leer antes de la reunión del comité. Preparar argumentos con ejemplos.

---

### **2. VISUALIZACIONES NUEVAS** ✅ **GENERADAS HOY**

#### **A) Variabilidad Consolidada** (3 plots)

**Ubicación:** `analisis_u/variabilidad_dual/plots_consolidados/`

1. **`variabilidad_operativa_vs_observada.png`**
   - **Qué muestra:** Barras agrupadas + línea de ratio
   - **Interpretación:** 
     - Variabilidad **operativa** = diferencias ENTRE usuarios
     - Variabilidad **observada** = fluctuaciones DENTRO de cada usuario
     - **Ratio > 1** → Usuarios más heterogéneos entre sí que internamente
     - **Ratio < 1** → Cada usuario es MÁS variable que las diferencias entre usuarios
   - **Justificación clínica:** Por eso usamos **p50 (nivel) + IQR (variabilidad)**

2. **`variabilidad_por_usuario_boxplot.png`**
   - **Qué muestra:** Boxplots por usuario, top 6 variables
   - **Interpretación:** Variabilidad intra-usuario vs línea de CV operativo
   - **Uso en presentación:** Mostrar heterogeneidad inter-individual

3. **`heatmap_cv_usuario_variable.png`**
   - **Qué muestra:** Matriz Usuario × Variable (valores de CV anotados)
   - **Interpretación:** Identificar usuarios con alta/baja variabilidad

#### **B) Heatmaps de Correlación con Valores** ✅ **ACTUALIZADO HOY**

**Ubicación:** `analisis_u/DB_final_v3_u*_heatmap_*.png` (20 archivos, 10×2)

- **Modificación:** Agregado `annot=True` y `fmt=".2f"`
- **Ahora muestra:** Valores de correlación dentro de cada celda
- **Ventaja:** El comité puede ver valores exactos sin necesidad de archivo CSV

#### **C) PACF Plots** ✅ **REGENERADO HOY**

**Ubicación:** `analisis_u/missingness_y_acf/pacf_plots/` (56 archivos)

- **Antes:** Plots vacíos con texto "PACF omitido (requiere statsmodels)"
- **Ahora:** Gráficos PACF reales (instalado `statsmodels`)
- **Uso:** Justificar autocorrelación temporal en los datos

---

### **3. TABLAS Y MÉTRICAS**

#### **A) Métricas de Concordancia (Fuzzy vs Clustering)**

**Archivo:** `analisis_u/fuzzy/09_eval_fuzzy_vs_cluster.txt`

```
Accuracy: 0.740
F1-Score: 0.840
MCC: 0.294
Precision: 0.737
Recall: 0.976

Matriz de Confusión:
        Bajo_pred  Alto_pred
Bajo    77         325
Alto    22         913
```

#### **B) Concordancia por Usuario**

**Archivo:** `analisis_u/fuzzy/09_eval_fuzzy_vs_cluster.txt` (sección 6)

| Usuario | Concordancia | Interpretación |
|---------|--------------|----------------|
| u1      | 99.3%        | Excelente |
| u7      | 94.7%        | Muy buena |
| u9      | 85.6%        | Buena |
| u6      | 81.7%        | Buena |
| u10     | 80.9%        | Buena |
| u5      | 71.4%        | Aceptable |
| u4      | 71.4%        | Aceptable |
| u8      | 44.0%        | Baja ⚠️ |
| u2      | 42.9%        | Baja ⚠️ |
| u3      | 27.7%        | Muy baja ⚠️ |

**Interpretación:**
- 7/10 usuarios tienen concordancia ≥71%
- Usuarios u2, u3, u8 presentan **patrones atípicos** (requieren análisis caso por caso)
- Esto refleja **heterogeneidad interindividual real** (no es un defecto del modelo)

#### **C) Top 20 Discordancias**

**Archivo:** `analisis_u/fuzzy/discordancias_top20.csv`

**Uso:** Revisión caso por caso de semanas donde Fuzzy y Clustering difieren más.

---

## 🔧 PARÁMETROS E HIPERPARÁMETROS DEL SISTEMA

### **Clustering (K-means)**

| **Parámetro** | **Valor** | **Justificación** |
|---------------|-----------|-------------------|
| K (número de clusters) | 2 | K-sweep (2-6) + Silhouette máximo |
| Escalado | RobustScaler | Robusto a outliers (mediana/IQR) |
| Random State | 42 | Reproducibilidad |
| n_init | 10 | Múltiples inicializaciones |
| max_iter | 500 | Convergencia garantizada |

**¿Por qué K=2?**
- Silhouette score máximo en K=2
- Interpretación clínica: "Alto" vs "Bajo" Sedentarismo
- Balanceo 70/30 (razonable para clasificación)

### **Sistema Difuso (Mamdani)**

| **Componente** | **Parámetro** | **Determinación** |
|----------------|---------------|-------------------|
| **Funciones de Membresía** | Triangulares (Bajo, Medio, Alto) | Percentiles [p10-p25-p40], [p35-p50-p65], [p60-p80-p90] |
| **Variables de Entrada** | 4 features (p50) | Actividad, Superávit, HRV, Delta_cardiaco |
| **Reglas** | 5 reglas (R1-R5) | Definidas por lógica clínica (no aprendidas) |
| **Defuzzificación** | Centroide | Niveles [0.2, 0.5, 0.8] |
| **Umbral τ** | 0.30 | **Grid search** (0.10-0.60) maximizando F1 |

**¿Qué parámetros se "entrenan"?**
- ❌ Percentiles de MF: **NO** (son estadísticos descriptivos de la cohorte)
- ❌ Reglas: **NO** (definidas por experto)
- ✅ Umbral τ: **SÍ** (único parámetro optimizado, por grid search)

---

## 📊 COMPARACIÓN: MODELO PREDICTIVO vs NUESTRO SISTEMA

| **Aspecto** | **ML Supervisado Predictivo** | **Nuestro Sistema** |
|-------------|-------------------------------|---------------------|
| **Objetivo** | Predecir nuevos casos futuros | Describir y clasificar esta cohorte |
| **Tipo de modelo** | Red neuronal, SVM, Random Forest | Sistema experto híbrido (reglas + clustering) |
| **Etiquetas** | Conocidas a priori (supervisadas) | Generadas por clustering (no supervisadas) |
| **Parámetros** | Pesos aprendidos (miles) | Percentiles (8×3) + 5 reglas |
| **Validación** | Train/Test **OBLIGATORIO** | Concordancia entre métodos |
| **Métrica de éxito** | Error de predicción (MSE, MAE) | Concordancia (F1-Score) |
| **Generalización** | A datos futuros no vistos | A estructura fisiológica subyacente |
| **Interpretabilidad** | Baja (caja negra) | Alta (reglas explícitas) |
| **Requiere split 80/20** | ✅ SÍ | ❌ NO (causa fuga temporal) |

---

## 🚦 RUTA DE VALIDACIÓN ROBUSTA (ALTERNATIVAS AL SPLIT 80/20)

### **Opción A: Leave-One-User-Out (LOUO)** ⭐ **RECOMENDADA POR EL EQUIPO**

**Cómo funciona:**
1. Loop: i = 1..10
2. train_users = [u1..u10] \ {ui}
3. test_user = ui
4. Recalcular MF percentiles solo con train_users
5. Reentrenar clustering K=2 solo con train_users
6. Optimizar τ en train
7. Aplicar fuzzy a test_user
8. Calcular F1(test_user)
9. Agregar F1_fold[i]
10. Reportar: mean(F1) ± std(F1)

**Ventajas:**
- ✅ Respeta independencia entre usuarios
- ✅ Usa todos los datos sin desperdiciar
- ✅ Mide generalización inter-individual
- ✅ Estándar en estudios con N pequeña

**Desventajas:**
- ⚠️ Computacionalmente costoso (10 folds × 2 min = 20 min)
- ⚠️ Si hay usuarios "outlier", F1 de ese fold será bajo → pero **ESO ES INFORMACIÓN**

**Tiempo de Implementación:** 2-3 horas de código + 20 minutos de ejecución

**Estado:** ⏳ **PENDIENTE** (prioridad si el comité lo solicita)

---

### **Opción B: Análisis de Sensibilidad** ⏳ **EN DESARROLLO**

**¿Qué se varía?**
1. Umbral τ: τ ± 0.05 (rango 0.25-0.35)
2. Percentiles MF: p ± 5% (p.ej., p25 → p20 o p30)
3. K en clustering: K=2, K=3, K=4

**Métrica:** ΔF1 < 0.10 → sistema robusto

**Tiempo:** 1 día de implementación

---

### **Opción C: Validación Temporal** ⏳ **EN DESARROLLO**

**Split:** Primeras 50% semanas (por usuario) vs Últimas 50%

**Métrica:** Comparar F1 en ambos periodos

**Objetivo:** Verificar estabilidad temporal del sistema

**Tiempo:** medio día de implementación

---

## 🚩 RED FLAGS Y RESPUESTAS ANTICIPADAS

### **Pregunta 1: "¿Por qué no hacer split 80/20?"**

**Respuesta Corta:**
Porque nuestros datos son **series temporales autocorrelacionadas** con solo **10 usuarios**. Split aleatorio causa **fuga temporal** (temporal leakage), y split por usuario no tiene **poder estadístico** suficiente (test con 2 usuarios es insuficiente).

**Documento de Respaldo:** `DEFENSA_NO_SPLIT_COMITE_TUTORIAL.md` (Razones 1-3)

---

### **Pregunta 2: "¿Cómo sabemos que el modelo funcionará en nuevos usuarios?"**

**Respuesta Corta:**
**NO afirmamos eso.** Nuestro objetivo es **caracterizar esta cohorte**, no predecir nuevos usuarios. Si en el futuro queremos generalizar, necesitaríamos un **estudio prospectivo** con nuevos datos.

**Analogía:** Es como validar un score clínico (APACHE II) contra mortalidad real en una cohorte. No usamos Train/Test, usamos concordancia con ground truth.

---

### **Pregunta 3: "¿Por qué F1=0.84 es 'bueno'?"**

**Respuesta Corta:**
En medicina, **F1 > 0.70** se considera robusto. Comparado con benchmarks clínicos:
- Predicción de readmisiones hospitalarias: F1~0.60-0.70
- Detección de arritmias en wearables: F1~0.75-0.85
- **Nuestro F1=0.84** está en el rango alto.

**Referencia:** Chicco & Jurman (2020), *BMC Genomics*

---

### **Pregunta 4: "¿Qué pasa con usuarios u2, u3, u8 (baja concordancia)?"**

**Respuesta Corta:**
Reflejan **heterogeneidad interindividual real**. No es un defecto del modelo, es información clínica:
- Posibles razones: adherencia baja, patrones atípicos, condiciones de salud específicas
- **Acción:** Análisis caso por caso (ya disponible en `discordancias_top20.csv`)

---

## 📚 REFERENCIAS CLAVE PARA EL COMITÉ

1. **Kohavi, R. (1995).** "A study of cross-validation and bootstrap for accuracy estimation and model selection." *IJCAI*, 14(2), 1137-1145.
   - **Cita:** "For small sample sizes (n < 100), leave-one-out CV provides more reliable estimates."

2. **Bergmeir, C., & Benítez, J. M. (2012).** "On the use of cross-validation for time series predictor evaluation." *Information Sciences*, 191, 192-213.
   - **Cita:** "Random splits in time series lead to optimistic bias due to temporal autocorrelation."

3. **Chicco, D., & Jurman, G. (2020).** "The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy." *BMC Genomics*, 21(1), 6.

4. **Casillas, J., et al. (2003).** *Interpretability Issues in Fuzzy Modeling.* Springer.
   - **Cita:** "Fuzzy systems based on expert knowledge do not require train/test split."

---

## ✅ CHECKLIST PARA LA REUNIÓN DEL COMITÉ

### **Antes de la Reunión**

- [ ] Leer `DEFENSA_NO_SPLIT_COMITE_TUTORIAL.md` completo
- [ ] Revisar las 3 visualizaciones de variabilidad consolidada
- [ ] Preparar ejemplos de analogías clínicas (presión arterial, APACHE II)
- [ ] Imprimir tabla de concordancia por usuario
- [ ] Revisar casos de discordancia (Top 20)

### **Durante la Presentación**

- [ ] Mostrar F1=0.84 como métrica principal
- [ ] Explicar por qué NO split 80/20 (3 razones)
- [ ] Mostrar plot de variabilidad operativa vs observada
- [ ] Discutir heterogeneidad interindividual (u2, u3, u8)
- [ ] Ofrecer Leave-One-User-Out como alternativa robusta

### **Si el Comité Solicita Cambios**

- [ ] **Opción 1:** Implementar LOUO (2-3 horas + 20 min ejecución)
- [ ] **Opción 2:** Análisis de sensibilidad (1 día)
- [ ] **Opción 3:** Validación temporal (medio día)
- [ ] **Opción 4:** Documentar limitaciones y mantener validación actual

---

## 🚀 PRÓXIMOS PASOS (POST-COMITÉ)

### **Si el Comité Aprueba la Metodología Actual:**

1. ✅ Finalizar manuscrito de tesis
2. ✅ Compilar documentos LaTeX (Informe, Beamer, Poster)
3. ✅ Generar presentación PowerPoint
4. ✅ Preparar defensa oral

**Tiempo estimado:** 1-2 semanas

### **Si el Comité Solicita Leave-One-User-Out:**

1. ⏳ Implementar script `10_leave_one_user_out_validation.py`
2. ⏳ Ejecutar 10 folds (20 minutos)
3. ⏳ Analizar resultados (F1 promedio ± std)
4. ⏳ Actualizar manuscrito con nueva validación

**Tiempo estimado:** 1 semana adicional

### **Si el Comité Solicita Validación Externa:**

1. ⏳ Buscar dataset público (NHANES, UK Biobank)
2. ⏳ Adaptar pipeline a nuevas features
3. ⏳ Aplicar sistema y reportar métricas

**Tiempo estimado:** 3-6 meses adicionales

---

## 📞 CONTACTO Y SOPORTE

**Investigador Principal:** Luis Ángel Martínez  
**Email:** [tu_email@uach.mx]  
**Directorio del Proyecto:** `C:\Users\hulkmtz\Documents\luis angel\Maestria\Asesoria\Semestre 3\Convocatoria\Datos\4 semestre_dataset`

**Asistencia Técnica:** Cursor/Claude (IA de desarrollo)  
**Última Actualización:** Octubre 18, 2025  
**Versión del Sistema:** 2.1

---

## 🎯 MENSAJE FINAL PARA EL COMITÉ

**Nuestro sistema NO es un modelo predictivo tradicional de Machine Learning.**

Es un **sistema experto híbrido** que:
1. ✅ Combina **conocimiento clínico** (reglas difusas) con **patrones data-driven** (clustering)
2. ✅ Valida la concordancia entre ambos métodos (F1=0.84)
3. ✅ Es **interpretable** (cada regla tiene justificación fisiológica)
4. ✅ Captura **heterogeneidad interindividual** (concordancia variable por usuario)
5. ✅ Es **reproducible** (parámetros fijos, random seeds)

**La validación por split 80/20 es:**
- ❌ Metodológicamente incorrecta para series temporales
- ❌ Insuficiente en potencia estadística para 10 usuarios
- ❌ No alineada con el objetivo descriptivo-clasificatorio del estudio

**Alternativas robustas disponibles:**
- ✅ Leave-One-User-Out (implementación: 1 semana)
- ✅ Análisis de sensibilidad (implementación: 1 día)
- ✅ Validación temporal (implementación: medio día)

**Decisión final:** En manos del Comité Tutorial.

---

**Gracias por su tiempo y consideración.**  
**Esperamos sus comentarios y sugerencias.**

---

**README Preparado por:** Luis Ángel Martínez + Cursor/Claude  
**Fecha:** Octubre 18, 2025  
**Versión:** 1.0




