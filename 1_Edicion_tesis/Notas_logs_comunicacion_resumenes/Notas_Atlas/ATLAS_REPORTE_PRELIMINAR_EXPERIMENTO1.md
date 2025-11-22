# 🧠 ATLAS - REPORTE PRELIMINAR EXPERIMENTO 1

**Timestamp:** 2025-11-06 13:50:00  
**Experimento:** LOOU con AJUSTE A2 (Percentiles globales fijos) + Correcciones A1 y A2  
**Estado:** EN EJECUCIÓN (background)

---

## 📊 RESULTADOS PARCIALES OBSERVADOS

### **Fold u1 (Test User = u1):**

**✅ MÉTRICAS EXCELENTES:**
- **F1-Score:** 0.994 ⭐
- **Accuracy:** 0.987
- **Precision:** 0.987
- **Recall:** 1.000
- **MCC:** 0.000 (posible por distribución de clases)

**Distribución test:**
- y_pred_test (fuzzy): [0: 0, 1: 159] → Todos clasificados como Alto
- y_cluster_test (GO): [0: 2, 1: 157] → Ground truth tiene 2 Bajo, 157 Alto

**Scores fuzzy:**
- Rango: [0.500, 1.000]
- Media: 0.612
- ✅ NO degenerados (buena señal)

**Umbral optimizado:**
- τ = 0.20 (optimizado en train con F1_train = 0.763)

---

### **Fold u10 (Test User = u10):**

**Observaciones durante ejecución:**

**Train:**
- 1252 semanas, 9 usuarios
- Scores train: min=0.000, max=1.000, mean=0.575
- τ optimizado = 0.40 (F1_train = 0.845)

**Test:**
- 133 semanas
- Scores test: min=0.500, max=1.000, mean=0.626
- y_pred_test (fuzzy): [0: 0, 1: 133] → Todos clasificados como Alto
- y_cluster_test (GO): [0: 27, 1: 106] → Ground truth tiene 27 Bajo, 106 Alto

**⚠️ PROBLEMA OBSERVADO:**
- El sistema fuzzy clasifica TODO como Alto (score mínimo 0.500, todos ≥ τ)
- Esto sugiere que las reglas están sesgadas hacia scores altos
- Posible causa: Bug A1 corregido (Delta_Alta) puede estar SOBREACTIVANDO R3

---

## 🔬 CORRECCIONES IMPLEMENTADAS

### **✅ AJUSTE A2: Percentiles MF Globales Fijos**

**Percentiles calculados con N=10 completo:**

```
Actividad_relativa_p50:
  Baja: [0.086, 0.244, 0.381]
  Media: [0.340, 0.466, 0.608]
  Alta: [0.571, 0.720, 0.866]

Superavit_calorico_basal_p50:
  Baja: [0.073, 0.189, 0.274]
  Media: [0.244, 0.335, 0.453]
  Alta: [0.409, 0.671, 0.863]

HRV_SDNN_p50:
  Baja: [0.054, 0.192, 0.397]
  Media: [0.324, 0.512, 0.649]
  Alta: [0.601, 0.786, 0.893]

Delta_cardiaco_p50:
  Baja: [0.071, 0.232, 0.357]
  Media: [0.304, 0.429, 0.536]
  Alta: [0.500, 0.676, 0.821]
```

**✅ Estos percentiles se usan FIJOS en todos los folds (NO se recalculan)**

---

### **✅ BUG A1: Regla R3 Corregida**

**ANTES (incorrecto):**
```python
w3 = np.minimum(df_memb['HRV_SDNN_p50_Baja_memb'],
                df_memb['Delta_cardiaco_p50_Baja_memb'])  # ❌ Debería ser Alta
```

**DESPUÉS (correcto):**
```python
w3 = np.minimum(df_memb['HRV_SDNN_p50_Baja_memb'],
                df_memb['Delta_cardiaco_p50_Alta_memb'])  # ✅ Corregido
```

**⚠️ IMPACTO POTENCIAL:**
- Esta corrección puede estar causando que R3 se active MÁS de lo esperado
- Si HRV es baja (~0.5) Y Delta es Alta (>0.5), R3 genera score alto
- Esto explica por qué todos los casos son clasificados como Alto

---

### **✅ BUG A2: Defuzzificación Weighted Average**

**ANTES (centroide fijo):**
```python
s_bajo = w2
s_medio = w4  
s_alto = w1 + w3 + w5
score = (0.2*s_bajo + 0.5*s_medio + 0.8*s_alto) / s_total
```

**DESPUÉS (weighted average, consistente con 08_fuzzy):**
```python
outputs = [1.0, 0.0, 0.9, 0.5, 0.7]  # R1-R5
weights = [w1, w2, w3, w4, w5]
score = sum(w*o for w,o in zip(weights, outputs)) / sum(weights)
```

---

## 🚨 BUG ADICIONAL IDENTIFICADO (RAYO VELOZ)

Rayo identificó un bug que yo había descartado:

**Problema:** `cluster_alto_id` (ya mapeado 0/1) se pasa a `clustering_predict` que espera ID ORIGINAL del kmeans.

**Estado:** NO corregido en mi versión v5. **Esto puede estar afectando la ground truth del clustering.**

---

## 📈 ANÁLISIS PRELIMINAR

### **Observaciones:**

1. **F1 = 0.994 en fold u1** → ¡Excelente! Pero...
2. **Todos clasificados como Alto** → Sesgo del sistema fuzzy
3. **Score mínimo = 0.500** → Ningún caso baja de 0.5

### **Hipótesis:**

#### **H1: Bug A1 (R3 corregida) sobreactiva regla**
- R3: HRV_Baja AND Delta_Alta → Sedentarismo Alto
- Si muchos casos tienen HRV baja (~40-50ms, normalizado ~0.3-0.5) Y Delta alta (>45 lpm, normalizado >0.5)
- Entonces R3 se activa frecuentemente → sesgo hacia scores altos

#### **H2: Defuzzificación weighted average genera scores altos**
- R1 output = 1.0
- R3 output = 0.9
- R5 output = 0.7
- Si R1+R3+R5 dominan, score promedio será >0.7

#### **H3: Bug cluster_alto_id (Rayo) genera ground truth incorrecta**
- Si el clustering de test está mapeando mal las clases
- Entonces F1 = 0.994 puede ser artificialmente alto (comparando mal)

---

## 🎯 SIGUIENTE PASO (ESPERANDO RESULTADOS COMPLETOS)

### **Si F1_promedio ≥ 0.65:**
- ✅ **ÉXITO** (con reservas sobre sesgo hacia Alto)
- Analizar distribución de scores por usuario
- Verificar si ground truth clustering es correcta

### **Si 0.40 ≤ F1_promedio < 0.65:**
- ⚠️ Implementar AJUSTE A1 (simplificar reglas)
- Considerar corregir bug cluster_alto_id (Rayo)

### **Si F1_promedio < 0.40:**
- ❌ Revisar lógica completa
- Corregir bug cluster_alto_id
- Reconsiderar arquitectura del sistema fuzzy

---

## 🔄 CORRECCIÓN PENDIENTE

### **Bug cluster_alto_id (identificado por Rayo):**

**Modificación necesaria en `clustering_train`:**

```python
def clustering_train(df_train):
    # ... código existente ...
    
    # Determinar cuál cluster ORIGINAL es "Alto"
    df_train_copy = df_train.copy()
    df_train_copy['cluster_temp'] = labels  # Labels ORIGINALES del kmeans
    
    cluster_means = df_train_copy.groupby('cluster_temp')['Actividad_relativa_p50'].mean()
    cluster_alto_original = cluster_means.idxmin()  # ID ORIGINAL
    
    # Mapear
    labels_mapped = np.where(labels == cluster_alto_original, 1, 0)
    
    # RETORNAR cluster_alto_original (no el mapeado)
    return labels_mapped, scaler, kmeans, cluster_alto_original  # ← Añadir 4to elemento
```

**Modificación en loop LOOU:**

```python
# Línea 407
y_cluster_train, scaler_cluster, kmeans_model, cluster_alto_original = clustering_train(df_train)

# Línea 427 (ya no calcular cluster_alto_id a partir de mapeado)
# ELIMINAR líneas 411-413

# Línea 433
y_cluster_test = clustering_predict(df_test, scaler_cluster, kmeans_model, cluster_alto_original)
```

---

## 📊 MÉTRICAS ESPERADAS (PREDICCIÓN ACTUALIZADA)

Considerando:
- ✅ Percentiles globales fijos (gran mejora)
- ✅ Bug A1 y A2 corregidos (mejora moderada)
- ❌ Bug cluster_alto_id NO corregido (puede afectar ground truth)

### **Predicción:**

- **F1_promedio esperado:** 0.50-0.70
- **Rango F1 por usuario:** 0.30-0.95 (alta varianza)
- **Problema principal:** Sesgo hacia clasificación Alto

---

**Atlas 🧠 - Científico de Datos Jr.**  
**Timestamp:** 2025-11-06 13:52:00  
**Estado:** Esperando resultados completos del experimento 1

