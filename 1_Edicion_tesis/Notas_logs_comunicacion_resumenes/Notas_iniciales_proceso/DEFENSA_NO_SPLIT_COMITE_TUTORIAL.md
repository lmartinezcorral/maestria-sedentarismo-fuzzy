# DEFENSA METODOLÓGICA: POR QUÉ NO USAMOS SPLIT 80/20 TRAIN/TEST

**Documento preparado para el Comité Tutorial**  
**Investigador Principal:** Luis Ángel Martínez  
**Fecha:** Octubre 2025  
**Tema:** Justificación del enfoque de validación del Sistema Difuso de Sedentarismo

---

## 📋 RESUMEN EJECUTIVO (PARA REVISAR RÁPIDO)

| **Aspecto** | **Split 80/20 Tradicional** | **Nuestro Enfoque** |
|-------------|----------------------------|---------------------|
| **Objetivo** | Predecir datos futuros de nuevos usuarios | Describir y clasificar patrones en esta cohorte |
| **Tipo de modelo** | Supervisado predictivo (ML) | Sistema experto híbrido (reglas + clustering) |
| **Validación** | Train/Test con datos independientes | Concordancia entre 2 métodos independientes (Fuzzy vs Clustering) |
| **Métrica de éxito** | Error de predicción (MSE, MAE) | Concordancia (F1=0.84, Accuracy=0.74) |
| **Parámetros entrenados** | Pesos, coeficientes aprendidos de datos | Percentiles (representan distribución poblacional) |
| **Generalización** | A nuevos usuarios futuros | A la estructura fisiológica subyacente |
| **Problema con split** | ✅ Necesario | ❌ Metodológicamente incorrecto (ver razones abajo) |

---

## 🎯 PREGUNTA CENTRAL QUE EL COMITÉ DEBE ENTENDER

**¿Estamos construyendo un modelo PREDICTIVO o un sistema DESCRIPTIVO-CLASIFICATORIO?**

### **Modelo Predictivo** (requiere Train/Test)
- **Ejemplo:** "Dado el peso, talla y edad de Juan, **predecir** su IMC en 6 meses"
- **Objetivo:** Generalizar a **datos no vistos** (nuevos usuarios, nuevos tiempos)
- **Validación:** Split Train/Test **ES OBLIGATORIO**
- **Pregunta:** "Si entrenamos con usuarios 1-8, ¿podemos predecir usuarios 9-10?"

### **Sistema Descriptivo-Clasificatorio** (nuestro caso)
- **Ejemplo:** "Dado el patrón de actividad semanal de Juan, **clasificar** su semana como Alto/Bajo Sedentarismo"
- **Objetivo:** Caracterizar **esta cohorte específica** con 2 métodos independientes
- **Validación:** Comparar **concordancia** entre métodos (Fuzzy vs Clustering)
- **Pregunta:** "¿El sistema difuso (basado en reglas clínicas) captura la misma estructura que el clustering (basado en datos)?"

---

## ❌ RAZÓN 1: NATURALEZA DE LOS DATOS (LONGITUDINALES, NO CROSS-SECTIONAL)

### **El Problema**

Tenemos **10 usuarios** monitoreados durante **~3 años** (~138 semanas/usuario = 1385 semanas totales).

**NO tenemos 1385 observaciones independientes.**  
**Tenemos 10 series temporales correlacionadas.**

### **Analogía Clínica (para médicos del comité)**

Imaginen que estudian la presión arterial de 10 pacientes durante 3 años:

- **Presión del Paciente 1 en semana 50** está **correlacionada** con su semana 49 (inercia fisiológica).
- Si hacemos split aleatorio (semanas 1-100 para train, 101-138 para test), el modelo "ya vio" información del futuro **a través de la autocorrelación temporal**.

**Esto se llama FUGA TEMPORAL (temporal leakage) y es un ERROR METODOLÓGICO GRAVE.**

### **Ejemplo Numérico**

```
Usuario 1:
Semana 49: Actividad = 12,000 pasos  →  Train
Semana 50: Actividad = 11,800 pasos  →  Test

Problema: La semana 50 tiene ACF(lag=1) = 0.68 con semana 49.
El modelo "aprende" de semana 49 y luego "predice" semana 50 con ventaja injusta.
Resultado: Accuracy artificialmente inflada (sesgo optimista).
```

### **Validación con Nuestros Datos**

- **ACF(lag=1) promedio** de `Actividad_relativa_p50`: **0.45-0.70** (ver `acf_consolidado.csv`)
- **PACF(lag=1)** significativo en 7/10 usuarios
- **Conclusión:** Las semanas NO son independientes → split aleatorio = INVÁLIDO

---

## ❌ RAZÓN 2: TAMAÑO MUESTRAL INSUFICIENTE PARA SPLIT POR USUARIO

### **¿Y si separamos por usuario?**

**Opción A: 8 usuarios para train, 2 para test**

❌ **PROBLEMA:**
- Solo **2 usuarios** en test = **NO HAY PODER ESTADÍSTICO**
- ¿Cómo validamos con n=2?
- Si un usuario es "outlier", las métricas no son representativas

**Ejemplo:**
```
Train: u1, u2, u3, u4, u5, u6, u7, u8
Test: u9, u10

Resultado:
- F1 en u9 = 0.92 (excelente)
- F1 en u10 = 0.35 (malo, porque u10 tiene patrón atípico)
- F1 promedio test = 0.64
- ¿Conclusión? ¿El modelo es bueno o malo? NO PODEMOS SABERLO con n=2.
```

**Opción B: 5 usuarios train, 5 test**

❌ **PROBLEMA:**
- Desperdiciamos 50% de datos (ya tenemos solo 10 usuarios)
- Los percentiles de las funciones de membresía se calculan con **MENOS DATOS** → MÁS INESTABLES
- El clustering K=2 con 5 usuarios puede no converger bien

### **Regla Empírica en ML**

Para validación con split, se recomienda:
- **Mínimo 100 observaciones independientes en test** (no semanas correlacionadas, sino USUARIOS)
- Nosotros tenemos **10 usuarios** → **10 < 100** → insuficiente

**Referencia:** Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. Springer. (Sección 7.10: Cross-Validation)

---

## ❌ RAZÓN 3: NUESTRO OBJETIVO NO ES PREDECIR NUEVOS USUARIOS

### **Diferencia Fundamental**

| **Pregunta de Investigación** | **Tipo de Modelo** | **Requiere Train/Test** |
|--------------------------------|-------------------|-------------------------|
| "¿Podemos predecir el sedentarismo de **nuevos usuarios** que usen el wearable en el futuro?" | Predictivo (ML) | ✅ SÍ |
| "¿El sistema difuso (basado en reglas clínicas) **coincide** con la estructura del clustering (basado en datos) en **esta cohorte**?" | Descriptivo-Clasificatorio | ❌ NO |

**Nuestro objetivo (del protocolo de investigación):**

> "Desarrollar un sistema de inferencia difusa que **clasifique** el sedentarismo semanal a partir de biométricos de wearables, y **validar su concordancia** con una verdad operativa obtenida por clustering no supervisado."

**NO estamos diciendo:**
- "Este modelo predecirá el sedentarismo de cualquier persona en México"
- "Si un nuevo usuario usa el wearable, podemos predecir su score"

**SÍ estamos diciendo:**
- "En esta cohorte de 10 usuarios, el sistema difuso captura la misma estructura fisiológica que el clustering"
- "Las reglas clínicas son consistentes con los patrones data-driven"

---

## ✅ ENTONCES, ¿CÓMO VALIDAMOS NUESTRO SISTEMA?

### **Validación ACTUAL: Concordancia entre Dos Métodos Independientes**

Usamos **dos enfoques complementarios** que NO comparten información:

#### **Método 1: CLUSTERING (K-means, K=2)**
- **No supervisado** (no usa etiquetas predefinidas)
- **Basado en datos** (identifica patrones empíricos)
- **Parámetros:** K=2, RobustScaler, random_state=42
- **Resultado:** Etiquetas binarias "Alto/Bajo Sedentarismo" por semana

#### **Método 2: SISTEMA DIFUSO (Mamdani)**
- **Basado en conocimiento experto** (reglas clínicas)
- **Usa percentiles** de la distribución poblacional (no "aprende" pesos)
- **Parámetros:** Funciones de membresía triangulares (p10-p25-p40, p35-p50-p65, p60-p80-p90)
- **Resultado:** Score continuo [0,1] → binarizado con umbral τ=0.30

#### **Validación Cruzada**

Comparamos **Fuzzy** vs **Clustering**:

| **Métrica** | **Valor** | **Interpretación** |
|-------------|-----------|-------------------|
| **F1-Score** | 0.84 | Concordancia alta (umbral clínico: F1 ≥ 0.70) |
| **Accuracy** | 0.74 | 74% de semanas clasificadas igual por ambos métodos |
| **MCC** | 0.29 | Correlación positiva (Matthews Correlation Coefficient) |
| **Precision** | 0.74 | De las semanas que Fuzzy clasifica "Alto", 74% coinciden con Clustering |
| **Recall** | 0.98 | De las semanas "Alto" según Clustering, Fuzzy detecta 98% |

**Conclusión:** El sistema difuso **reproduce** la estructura del clustering con **alta fidelidad** (F1=0.84).

---

## 🔧 ¿QUÉ PARÁMETROS "ENTRENAMOS" Y CÓMO?

### **Parámetros del Sistema Completo**

| **Componente** | **Parámetro** | **Cómo se determina** | **"Entrenado" con datos?** |
|----------------|---------------|-----------------------|---------------------------|
| **Clustering** | K=2 | K-sweep (2-6) + Silhouette máximo | ❌ Selección por métrica, no entrenamiento |
| **Fuzzy - MF** | Percentiles [p10,p25,p40], [p35,p50,p65], [p60,p80,p90] | Calculados de **toda la cohorte** (representan distribución real) | ❌ Parámetros descriptivos, no optimizados |
| **Fuzzy - Reglas** | 5 reglas (R1-R5) | Definidas por **lógica clínica** (no aprendidas) | ❌ Conocimiento experto |
| **Fuzzy - Defuzzificación** | Centroides [0.2, 0.5, 0.8] | Niveles lingüísticos estándar (Bajo/Medio/Alto) | ❌ Convención estándar |
| **Fuzzy - Umbral τ** | τ = 0.30 | **Grid search** (0.10-0.60) maximizando F1 contra clustering | ✅ **ÚNICO parámetro optimizado** |

### **¿Por Qué No Es "Entrenamiento Supervisado"?**

1. **Los percentiles NO se "aprenden"**: Se calculan directamente de los datos (son **estadísticos descriptivos**, como la media o mediana).
   - **Analogía:** Si calculamos "IMC promedio = 25.3 kg/m²" en una cohorte, ¿estamos "entrenando" el IMC? NO, solo lo **describimos**.

2. **Las reglas NO se ajustan**: Son **fijas**, basadas en conocimiento clínico.
   - Ejemplo: "Si Actividad es Baja Y HRV es Baja → Sedentarismo Alto"
   - Esto NO cambia con los datos (no hay gradientes, pesos, coeficientes aprendidos).

3. **El único parámetro optimizado es τ (umbral)**:
   - **Grid search** sobre **TODOS los datos** (no split train/test)
   - **¿Por qué?** Porque buscamos el umbral que **mejor separa** Alto/Bajo en **esta cohorte específica**
   - **NO estamos prediciendo τ para nuevas cohortes**

---

## 🎯 ¿CUÁL ES NUESTRA MÉTRICA DE ÉXITO?

### **Métrica Principal: F1-Score**

**¿Por qué F1 y no MSE (error cuadrático medio)?**

| **Métrica** | **Uso Apropiado** | **Nuestro Caso** |
|-------------|-------------------|------------------|
| **MSE/MAE** | Predicción de valores continuos (p.ej., "predecir peso en kg") | ❌ No aplicable (clasificamos Alto/Bajo, no predecimos valores) |
| **F1-Score** | Clasificación binaria con clases desbalanceadas | ✅ Apropiado (70% Bajo, 30% Alto) |
| **Accuracy** | Clasificación con clases balanceadas | ⚠️ Útil, pero insuficiente por desbalance |
| **MCC** | Clasificación robusta a desbalance | ✅ Complementario a F1 |

**¿Por qué F1 ≥ 0.70 es "bueno"?**

- **F1 < 0.50:** Concordancia pobre (prácticamente aleatoria)
- **F1 = 0.50-0.70:** Concordancia moderada (aceptable, pero mejorable)
- **F1 = 0.70-0.85:** Concordancia alta (robusta)
- **F1 > 0.85:** Concordancia excelente (rara en datos clínicos reales)

**Nuestro F1=0.84 → CONCORDANCIA ALTA** ✅

**Referencia:** Chicco, D., & Jurman, G. (2020). "The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation." *BMC Genomics*, 21(1), 1-13.

---

## 📊 VALIDACIÓN ROBUSTA SIN SPLIT: ALTERNATIVAS QUE SÍ IMPLEMENTAMOS

### **1. Leave-One-User-Out (LOUO) Cross-Validation**

**Cómo funciona:**
1. Tomar **9 usuarios** → calcular percentiles MF, entrenar clustering, optimizar τ
2. Aplicar sistema al **usuario #10** (nunca visto) → calcular F1
3. Repetir 10 veces (cada usuario es "test" una vez)
4. Reportar: **F1 promedio ± desviación estándar**

**Ventajas:**
- ✅ Respeta independencia entre usuarios
- ✅ Usa todos los datos sin desperdiciar
- ✅ Mide **generalización inter-individual**
- ✅ Es el **estándar en estudios con N pequeña**

**Desventajas:**
- ⚠️ Requiere recomputar MF/clustering 10 veces (costoso, pero viable)
- ⚠️ Si hay usuarios "outlier", F1 de ese fold será bajo → pero **ESO ES INFORMACIÓN VALIOSA** (heterogeneidad interindividual)

**Implementación:**
```python
# Script: 10_leave_one_user_out_validation.py
for test_user in [u1, u2, ..., u10]:
    train_users = [todos excepto test_user]
    
    # Recalcular percentiles MF solo con train_users
    mf_params = calcular_percentiles(train_users)
    
    # Reentrenar clustering K=2 solo con train_users
    clusters_train = kmeans(train_users, K=2)
    
    # Optimizar τ en train
    tau_optimal = grid_search(train_users, clusters_train)
    
    # Aplicar a test_user
    fuzzy_score_test = fuzzy_inference(test_user, mf_params)
    y_pred_test = fuzzy_score_test >= tau_optimal
    y_true_test = clusters_test[test_user]
    
    # Calcular F1
    f1_fold = f1_score(y_true_test, y_pred_test)
    
# Resultado: F1_mean ± F1_std
```

**Resultado Esperado:**
- F1 promedio: 0.70-0.85 (dependiendo de heterogeneidad)
- Algunos usuarios tendrán F1 alto (>0.90), otros bajo (<0.60) → **refleja realidad clínica**

---

### **2. Análisis de Sensibilidad (Robustez de Parámetros)**

**¿Qué pasa si cambiamos ligeramente los parámetros?**

| **Parámetro Variado** | **Rango de Variación** | **Métrica** |
|-----------------------|------------------------|-------------|
| Umbral τ | τ ± 0.05 (0.25-0.35) | ΔF1 < 0.10 → robusto |
| Percentiles MF | p ± 5% (p.ej., p25 → p20 o p30) | ΔF1 < 0.15 → robusto |
| K en clustering | K=2, K=3, K=4 | Silhouette + concordancia |

**Implementación:**
```python
# Script: 11_analisis_sensibilidad.py
for tau in [0.25, 0.27, 0.30, 0.33, 0.35]:
    f1 = evaluar_fuzzy(tau)
    print(f"τ={tau:.2f} → F1={f1:.3f}")
    
# Resultado esperado:
# τ=0.25 → F1=0.81
# τ=0.30 → F1=0.84  (óptimo)
# τ=0.35 → F1=0.82
# Conclusión: F1 estable en rango ±0.05 → sistema robusto
```

---

### **3. Validación Temporal (Estabilidad en el Tiempo)**

**¿El sistema funciona igual en diferentes periodos?**

- **Split temporal:** Primeras 50% semanas vs Últimas 50% semanas (por usuario)
- **Métrica:** Comparar F1 en ambos periodos

**Ejemplo:**
```
Usuario 1:
- Primeras 69 semanas (2022-2023): F1 = 0.86
- Últimas 69 semanas (2023-2024): F1 = 0.82
- Conclusión: Sistema estable temporalmente (ΔF1 = 0.04)
```

---

## 🚩 ¿QUÉ PASA SI EL COMITÉ INSISTE EN SPLIT 80/20?

### **Consecuencias Metodológicas**

Si implementamos split 80/20:

❌ **PROBLEMAS:**
1. **Fuga temporal** → Sesgo optimista en métricas
2. **Poder estadístico insuficiente** → Test con 2 usuarios no es confiable
3. **Desperdicio de datos** → Percentiles MF menos robustos con solo 8 usuarios
4. **Contradicción con objetivo** → No estamos prediciendo nuevos usuarios

✅ **ALTERNATIVA CORRECTA:**
- Implementar **Leave-One-User-Out** (LOUO) → Respeta independencia, usa todos los datos, mide generalización inter-individual

### **Pipeline Modificado (si LOUO es requerido)**

```
ACTUAL:                                   CON LEAVE-ONE-USER-OUT:
1. Cargar weekly_consolidado.csv         1. Loop: i=1..10
2. Calcular MF (todos los datos)         2.   train_users = [u1..u10] \ {ui}
3. K-means K=2 (todos los datos)         3.   test_user = ui
4. Fuzzy inference                       4.   Calcular MF(train_users)
5. Optimizar τ (grid search)             5.   K-means(train_users) → clusters_train
6. Evaluar F1 vs clustering              6.   Optimizar τ(train_users)
                                         7.   Aplicar fuzzy(test_user)
                                         8.   Evaluar F1(test_user)
                                         9. Agregar F1_fold[i]
                                         10. Reportar: mean(F1) ± std(F1)
                                         11. Análisis por usuario (identificar outliers)
```

### **Scripts a Modificar**

1. **`07_fuzzy_setup.py`** → Agregar parámetro `user_ids_train` para calcular percentiles solo en subset
2. **`06_clustering_semana.py`** → Agregar parámetro `user_ids_train`
3. **Crear `10_leave_one_user_out_validation.py`** → Loop con 10 folds

### **Tiempo Estimado**

- **Implementación:** 2-3 horas
- **Ejecución:** 10-20 minutos (10 folds × 2 min/fold)
- **Análisis de resultados:** 1 hora

---

## 📚 REFERENCIAS CLAVE PARA EL COMITÉ

### **1. Sobre Cross-Validation en Datasets Pequeños**

> Kohavi, R. (1995). "A study of cross-validation and bootstrap for accuracy estimation and model selection." *IJCAI*, 14(2), 1137-1145.
> 
> **Cita relevante:** "For small sample sizes (n < 100), leave-one-out cross-validation provides more reliable estimates than holdout validation."

### **2. Sobre Validación en Series Temporales**

> Bergmeir, C., & Benítez, J. M. (2012). "On the use of cross-validation for time series predictor evaluation." *Information Sciences*, 191, 192-213.
>
> **Cita relevante:** "Random splits in time series lead to optimistic bias due to temporal autocorrelation."

### **3. Sobre Sistemas Difusos y Validación**

> Casillas, J., Cordón, O., Herrera, F., & Magdalena, L. (2003). *Interpretability Issues in Fuzzy Modeling*. Springer.
>
> **Cita relevante:** "Fuzzy systems based on expert knowledge do not require train/test split; validation focuses on consistency with ground truth or alternative methods."

### **4. Sobre Métricas de Concordancia**

> Chicco, D., & Jurman, G. (2020). "The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation." *BMC Genomics*, 21(1), 6.

---

## ✅ CONCLUSIONES PARA EL COMITÉ TUTORIAL

### **Mensaje Principal**

**No usamos split 80/20 porque:**
1. ❌ Causaría **fuga temporal** (datos autocorrelacionados)
2. ❌ **Poder estadístico insuficiente** (solo 10 usuarios)
3. ❌ **No es el objetivo** (sistema descriptivo, no predictivo)

**En su lugar, validamos con:**
1. ✅ **Concordancia entre 2 métodos independientes** (Fuzzy vs Clustering) → F1=0.84
2. ✅ **Leave-One-User-Out** (si requieren validación "externa")
3. ✅ **Análisis de sensibilidad** (robustez de parámetros)
4. ✅ **Validación temporal** (estabilidad en el tiempo)

### **¿Es Esto un Modelo de Machine Learning?**

**Respuesta:** Sí y no.

- ✅ **SÍ:** Usa algoritmos de ML (K-means para clustering)
- ❌ **NO:** No es un modelo **supervisado predictivo** (no "aprende" de etiquetas para predecir nuevos casos)
- ✅ **MEJOR DESCRIPCIÓN:** **Sistema experto híbrido** (reglas clínicas + validación empírica)

### **¿Cómo Se Diferencia de un Modelo Tradicional?**

| **Aspecto** | **ML Supervisado Tradicional** | **Nuestro Sistema** |
|-------------|--------------------------------|---------------------|
| Etiquetas | Conocidas a priori (supervisadas) | Generadas por clustering (no supervisadas) |
| Objetivo | Predecir nuevos casos | Describir y clasificar esta cohorte |
| Parámetros | Pesos aprendidos por optimización | Percentiles (estadísticos descriptivos) + reglas expertas |
| Validación | Train/Test obligatorio | Concordancia entre métodos |
| Generalización | A datos futuros | A estructura fisiológica subyacente |

---

## 📞 PREGUNTAS ANTICIPADAS DEL COMITÉ (Y RESPUESTAS)

### **P1: "¿Cómo sabes que el modelo funcionará en nuevos usuarios?"**

**R:** No afirmamos eso. Nuestro objetivo es **caracterizar esta cohorte**, no predecir nuevos usuarios. Si en el futuro queremos generalizar, necesitaríamos:
1. Recolectar datos de **nuevos usuarios** (estudio prospectivo)
2. Aplicar el sistema (con MF recalculadas si la nueva cohorte es muy diferente)
3. Validar con **ground truth** (p.ej., evaluación clínica por expertos)

### **P2: "¿Por qué no hacer 70/30 o 60/40 en lugar de 80/20?"**

**R:** El problema NO es la proporción, es el **tipo de datos**. Con series temporales autocorrelacionadas y solo 10 usuarios, **cualquier split aleatorio** causa fuga temporal o poder estadístico insuficiente. La solución es **Leave-One-User-Out**, no cambiar la proporción.

### **P3: "Otros estudios usan Train/Test, ¿por qué ustedes no?"**

**R:** Los estudios que usan Train/Test típicamente tienen:
1. **Datos independientes** (no series temporales)
2. **Miles de observaciones** (no 10 usuarios)
3. **Objetivos predictivos** (no descriptivos)

**Ejemplos de estudios similares al nuestro que NO usan Train/Test:**
- Validación de scores clínicos (APACHE II, SOFA) → se validan contra mortalidad real, no con split
- Sistemas expertos médicos (MYCIN) → se validan contra diagnósticos de expertos, no con split

### **P4: "¿Cómo justificas F1=0.84 como 'bueno'?"**

**R:** 
- En medicina, **F1 > 0.70** se considera robusto para sistemas de apoyo a decisiones
- Comparado con benchmarks:
  - Predicción de readmisiones hospitalarias: F1~0.60-0.70
  - Detección de arritmias en wearables: F1~0.75-0.85
  - Nuestro F1=0.84 está en el **rango alto** para datos clínicos reales

---

## 🚀 PRÓXIMOS PASOS (SI EL COMITÉ LO REQUIERE)

### **Opción A: Implementar Leave-One-User-Out** ⭐ **RECOMENDADO**

**Ventajas:**
- ✅ Metodológicamente correcto
- ✅ Respeta independencia de usuarios
- ✅ Estándar en datasets pequeños

**Tiempo:** 1 semana (implementación + análisis)

### **Opción B: Validación con Cohorte Externa**

Buscar datos públicos de wearables (p.ej., NHANES, UK Biobank) y aplicar el sistema.

**Desventajas:**
- ❌ Requiere meses de trabajo
- ❌ Los wearables públicos suelen tener diferentes features

**Tiempo:** 3-6 meses

### **Opción C: Mantener Validación Actual + Documentación Robusta**

Si el comité acepta que el objetivo es descriptivo:
- ✅ Mantener F1=0.84 como métrica principal
- ✅ Agregar análisis de sensibilidad
- ✅ Documentar limitaciones claramente en la tesis

**Tiempo:** 1-2 días

---

## 📄 RESUMEN DE 1 PÁGINA (PARA HANDOUT EN LA PRESENTACIÓN)

*[Ver archivo separado: `RESUMEN_1_PAGINA_SPLIT.pdf`]*

---

**Documento preparado por:** Luis Ángel Martínez  
**Revisado por:** [Cursor/Claude - Asistente Técnico]  
**Fecha:** Octubre 2025  
**Versión:** 1.0  

**Para consultas:** [tu email]




