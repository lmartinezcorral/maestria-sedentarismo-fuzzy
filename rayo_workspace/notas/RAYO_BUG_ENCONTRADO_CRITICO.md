# 🔥 BUG CRÍTICO ENCONTRADO EN LOUO - RAYO VELOZ

**Timestamp:** 2025-11-06 13:27:00  
**Archivo:** `10_leave_one_user_out_validation.py`  
**Líneas afectadas:** 385-404

---

## 🐛 DESCRIPCIÓN DEL BUG

### **PROBLEMA:**

En el loop LOUO, el script identifica `cluster_alto_id` después del mapeo (línea 387):

```python
cluster_means = df_train.groupby('cluster_label')['Actividad_relativa_p50'].mean()
cluster_alto_id = cluster_means.idxmin()  # Resultado: 0 o 1 (YA MAPEADO)
```

Luego pasa este valor a `clustering_predict` (línea 403):

```python
y_cluster_test = clustering_predict(df_test, scaler_cluster, kmeans_model, cluster_alto_id)
```

Pero `clustering_predict` (línea 205) espera recibir el **ID del cluster ORIGINAL del k-means** (antes del mapeo):

```python
def clustering_predict(df_test, scaler, kmeans, cluster_alto_original):
    labels = kmeans.predict(X_scaled)  # Esto devuelve 0 o 1 ORIGINAL
    labels_mapped = np.where(labels == cluster_alto_original, 1, 0)  # Compara con ORIGINAL
    return labels_mapped
```

### **CONSECUENCIA:**

Si `cluster_alto_id = 0` (ya mapeado), pero el cluster original alto en kmeans era `1`, entonces:

- `kmeans.predict(X_test)` devuelve `[1, 1, 0, 1, ...]` (IDs originales)
- `labels_mapped = np.where(labels == 0, 1, 0)` busca cluster `0`
- ❌ **Pero el cluster alto ORIGINAL es `1`, no `0`**
- ❌ **Resultado:** Labels invertidos o todos asignados a clase incorrecta

Esto explica por qué:
- ✅ F1_train = 0.000 (todos clasificados mal o sin varianza)
- ❌ Scores fuzzy generados correctamente, pero umbral τ=0.30 es inútil
- ❌ F1_test = 0.000 (clustering de test también incorrecto)

---

## ✅ SOLUCIÓN

### **FIX 1: Retornar cluster_alto_original de clustering_train**

Modificar `clustering_train` para retornar el **ID original** del cluster alto:

```python
def clustering_train(df_train):
    # ... (código existente) ...
    
    # Determinar cuál cluster es "Alto"
    cluster_means = df_train_copy.groupby('cluster_temp')['Actividad_relativa_p50'].mean()
    cluster_alto_original = cluster_means.idxmin()  # ID ORIGINAL (del kmeans)
    
    # Mapear
    labels_mapped = np.where(labels == cluster_alto_original, 1, 0)
    
    # RETORNAR cluster_alto_original para usarlo en predict
    return labels_mapped, scaler, kmeans, cluster_alto_original  # <-- CAMBIO
```

### **FIX 2: Usar cluster_alto_original en loop LOUO**

```python
# En main(), línea 380-388
log("  [2] Entrenando clustering K=2 en train...")
y_cluster_train, scaler_cluster, kmeans_model, cluster_alto_original = clustering_train(df_train)
df_train['cluster_label'] = y_cluster_train

# ... (resto del código) ...

# Línea 402
log("  [5] Aplicando clustering a test...")
y_cluster_test = clustering_predict(df_test, scaler_cluster, kmeans_model, cluster_alto_original)
```

---

## 🧪 HIPÓTESIS DE VALIDACIÓN

### **Predicción:**

Con este fix:
- ✅ F1_train debería ser >0.70 (similar a script 09 que funciona)
- ✅ F1_test (LOUO) debería ser >0.40-0.60 (con variabilidad entre usuarios)
- ✅ CV% debería ser ~10-20% (razonable para N=10)

### **Si persiste F1_test bajo (<0.40):**

Entonces el problema es otro (percentiles, normalización, etc.) y procedemos con Plan B4 - Ajustes A2+A3.

---

## ⚡ ACCIÓN INMEDIATA

1. Implementar fix en `rayo_workspace/scripts/10_louo_rayo_v2_FIXED.py`
2. Ejecutar y obtener métricas
3. Si F1 >0.50 → **ÉXITO**
4. Si F1 <0.50 → Proceder con ajustes A2+A3

---

**Rayo Veloz ⚡ - Bug crítico identificado**  
**Tiempo invertido:** 15 minutos  
**Confianza en fix:** 85%

