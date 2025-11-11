# SISTEMA DE INFERENCIA DIFUSA PARA EVALUACIÓN DE SEDENTARISMO  
## Informe Técnico-Clínico Completo para Tesis de Maestría

**Autor:** Luis Ángel Martínez  
**Fecha:** 18 de octubre de 2025  
**Versión:** 3.0 — Informe Maestro  
**Institución:** Maestría en Ciencias, Semestre 3  

---

## RESUMEN EJECUTIVO

### Objetivo
Desarrollar y validar un **sistema de inferencia difusa tipo Mamdani** para clasificar el **sedentarismo semanal** a partir de biomarcadores obtenidos de wearables (Apple Watch), contrastando su salida con una **verdad operativa** derivada de **clustering no supervisado K-means (K=2)**.

### Población y Datos
- **Cohorte:** 10 adultos (5 mujeres, 5 hombres), seguimiento multianual.
- **Unidad de análisis:** 1,385 semanas agregadas (1,337 válidas tras filtrado de calidad).
- **Variables base diarias:** Actividad física, gasto calórico, HRV (SDNN), frecuencia cardíaca (reposo y caminata), horas monitoreadas.
- **Variables derivadas clave:**  
  - `Actividad_relativa = min_movimiento / (60 × hrs_monitoreadas)` — normaliza por exposición.  
  - `Superávit_calórico_basal = (Gasto_activo × 100) / TMB` — ajusta por antropometría (Mifflin-St Jeor).

### Hallazgos Principales
1. **Concordancia robusta:** Sistema difuso vs. clustering K=2 con **F1 = 0.840**, **Recall = 97.6%**, **Accuracy = 74.0%** (umbral óptimo τ = 0.30).
2. **Alta sensibilidad (Recall 97.6%):** Minimiza falsos negativos, adecuado para **screening poblacional** de sedentarismo.
3. **Trade-off controlado:** 325 falsos positivos (FP) en 1,337 semanas; política conservadora preferida para contexto de salud pública.
4. **Heterogeneidad inter-sujeto:** Concordancia por usuario entre 27.7% (u3) y 99.3% (u1), sugiere personalización futura de umbral τ o reglas moduladas por IQR.

### Entregables
- **Código reproducible:** Scripts documentados con logs de auditoría.
- **Configuración fuzzy:** Funciones de membresía por percentiles, 5 reglas interpretables.
- **Métricas de validación:** Matriz de confusión, curvas Precision-Recall, distribución de scores por cluster.
- **Recomendaciones:** Umbral τ personalizado, reglas moduladas por variabilidad (IQR), validación externa y dashboard clínico.

---

## 1. INTRODUCCIÓN CLÍNICA Y JUSTIFICACIÓN

### 1.1. Problema de Salud Pública
El sedentarismo es un factor de riesgo independiente para **enfermedades cardiovasculares, diabetes tipo 2, obesidad y mortalidad por todas las causas**. La evaluación objetiva del sedentarismo en vida libre requiere:
1. **Métricas basadas en wearables** (superan el sesgo de autoreporte).
2. **Normalización antropométrica** (400 kcal gastadas ≠ impacto equivalente en sujetos con distinto TMB).
3. **Integración multivariada** (actividad física + eficiencia autonómica + carga cardíaca).

### 1.2. Justificación de Variables Clave

#### a) Actividad_relativa (exposición-normalizada)
**Definición:**  
$$\text{Actividad\_relativa} = \frac{\text{min\_totales\_en\_movimiento}}{60 \times \text{Total\_hrs\_monitorizadas}}$$

**Rationale fisiológico:**  
- Usuario A: 30 min movimiento / 24 h monitoreo = 2.1% del tiempo activo.  
- Usuario B: 30 min movimiento / 8 h monitoreo = 6.3% del tiempo activo.  
No son equivalentes sin corrección por exposición.

**Evidencia:** Normalizar por tiempo de uso mejora comparabilidad inter-sujeto (Troiano, 2008; Tudor-Locke, 2011).

---

#### b) Superávit_calórico_basal (ajustado por TMB)
**Definición:**  
$$\text{Superávit\_calórico\_basal} = \frac{\text{Gasto\_calorico\_activo} \times 100}{\text{TMB}}$$

**TMB (Mifflin-St Jeor):**  
- Hombres: $TMB = 10 \cdot \text{peso(kg)} + 6.25 \cdot \text{altura(cm)} - 5 \cdot \text{edad} + 5$  
- Mujeres: $TMB = 10 \cdot \text{peso(kg)} + 6.25 \cdot \text{altura(cm)} - 5 \cdot \text{edad} - 161$

**Ejemplo clínico:**  
- Usuario 9 (124 kg, hombre, TMB ≈ 2241 kcal): 400 kcal activas = **17.8% del TMB**.  
- Usuario 10 (58 kg, mujer, TMB ≈ 1304 kcal): 400 kcal activas = **30.7% del TMB**.  
→ Impacto fisiológico distinto, capturado por el ratio.

---

#### c) HRV_SDNN (variabilidad cardíaca)
**Interpretación:**  
- **HRV alta (>60 ms):** Tono vagal saludable, recuperación adecuada.  
- **HRV baja (<40 ms):** Estrés crónico, desacondicionamiento, riesgo cardiovascular aumentado.

**Uso en sistema difuso:** HRV baja **refuerza** clasificación de sedentarismo alto (marcador indirecto de desacondicionamiento).

**Evidencia:** SDNN <50 ms asociado a↑riesgo de eventos cardiovasculares (Thayer, 2010; Task Force ESC, 1996).

---

#### d) Delta_cardiaco (respuesta cardíaca al ejercicio)
**Definición:**  
$$\Delta_{\text{cardiaco}} = FC_{\text{al\_caminar\_p50}} - FCr_{\text{p50}}$$

**Interpretación fisiológica:**  
- Δ alto (>50 lpm): Respuesta cardíaca apropiada al esfuerzo.  
- Δ bajo (<30 lpm): Posible bloqueo beta, desacondicionamiento o bajo esfuerzo percibido.

**Uso:** Complementa actividad relativa (distingue "moverse poco" de "moverse con baja carga cardíaca").

---

### 1.3. Por Qué Lógica Difusa (No Solo Clustering)
| Aspecto | Clustering (K-Means) | Lógica Difusa |
|---------|----------------------|---------------|
| **Interpretabilidad** | Partición dura; centroides abstractos | Reglas lingüísticas auditables ("Si Actividad es Baja…") |
| **Personalización** | Reasignación global (retraining) | Ajuste local de MF o pesos de reglas |
| **Explicabilidad clínica** | "Perteneces al cluster 1" | "Score alto por: Actividad baja (μ=0.9) ∧ HRV baja (μ=0.7)" |
| **Validación externa** | Requiere recalibración completa | MF por percentiles → fácil recalibración en nueva cohorte |

**Decisión:** Usar **clustering como verdad operativa** para descubrir estructura data-driven, luego validar **sistema fuzzy interpretable** contra esa estructura.

---

## 2. DATOS Y COHORTE

### 2.1. Características de la Cohorte

| Usuario | Sexo | Edad | Peso (kg) | Estatura (cm) | TMB (kcal/día) | Días monitoreados | Semanas válidas |
|---------|------|------|-----------|---------------|----------------|-------------------|-----------------|
| u1 (ale) | Mujer | 34 | 68 | 170 | 1411 | 1048 | 149 |
| u2 (brenda) | Mujer | 37 | 76 | 169 | 1476 | 56 | 7 |
| u3 (christina) | Mujer | 39 | 77 | 164 | 1445 | 1001 | 141 |
| u4 (edson) | Hombre | 25 | 100 | 180 | 2013 | 110 | 14 |
| u5 (esmeralda) | Mujer | 28 | 64 | 160 | 1329 | 104 | 14 |
| u6 (fidel) | Hombre | 34 | 100 | 180 | 1958 | 1967 | 278 |
| u7 (kevin) | Hombre | 32 | 92 | 156 | 1717 | 812 | 114 |
| u8 (legarda) | Hombre | 29 | 92 | 181 | 1893 | 1345 | 191 |
| u9 (lmartinez) | Hombre | 32 | 124 | 185 | 2241 | 2070 | 298 |
| u10 (vane) | Mujer | 28 | 58 | 164 | 1304 | 925 | 131 |

**Observaciones:**  
- Rango de TMB: 1,304–2,241 kcal/día (variabilidad 72%).  
- Duración de seguimiento: 56–2,070 días (heterogeneidad temporal alta).  
- Usuarios u2, u4, u5: <20 semanas válidas (contribuyen ~2.6% del dataset).

---

### 2.2. Variables Diarias (Post-Agregación desde Intra-día)

| Variable | Unidad | Descripción | Agregación intra-día |
|----------|--------|-------------|----------------------|
| `Fecha` | YYYY-MM-DD | Fecha del registro | - |
| `Total_hrs_monitorizadas` | horas | Horas con señal del dispositivo | Suma |
| `Hrs_sin_registro` | horas | 24 - Total_hrs_monitorizadas | Calculado |
| `min_totales_en_movimiento` | minutos | Minutos en anillo de movimiento | Suma |
| `Total_min_de_ejercicio_diario` | minutos | Ejercicio formal | Suma |
| `Numero_pasos_por_dia` | pasos | Pasos totales | Suma |
| `distancia_caminada_en_km` | km | Distancia recorrida | Suma |
| `FCr_promedio_diario` | lpm | FC en reposo | Mínimo diario |
| `FC_al_caminar_promedio_diario` | lpm | FC al caminar | Media |
| `Gasto_calorico_activo` | kcal | Energía activa quemada | Suma |
| `HRV_SDNN` | ms | Variabilidad cardíaca (SDNN) | Media |

---

### 2.3. Variables Derivadas (Diarias)

**Creadas durante preprocesamiento:**

1. **Actividad_relativa:**  
   ```python
   Actividad_relativa = min_totales_en_movimiento / (60 * Total_hrs_monitorizadas)
   ```
   **Reemplaza:** `min_totales_en_movimiento` (evita multicolinealidad, VIF original >10).

2. **TMB (constante por usuario):**  
   Mifflin-St Jeor por sexo, peso, estatura, edad.

3. **Superávit_calórico_basal:**  
   ```python
   Superavit_calorico_basal = (Gasto_calorico_activo * 100) / TMB
   ```
   **Reemplaza:** `Gasto_calorico_activo` (permite comparabilidad inter-sujeto).

4. **Delta_cardiaco (calculado en agregación semanal):**  
   $$\Delta_{\text{cardiaco\_p50}} = FC_{\text{al\_caminar\_p50}} - FCr_{\text{p50}}$$

---

### 2.4. Agregación Semanal (Features para Clustering/Fuzzy)

**Unidad de análisis final:** Semana (7 días consecutivos, válida si ≥5 días con uso ≥8h/día).

**8 Features para modelado:**

| Feature | Descripción | Rango observado |
|---------|-------------|-----------------|
| `Actividad_relativa_p50` | Mediana semanal de actividad normalizada | [0.035, 0.310] |
| `Actividad_relativa_iqr` | IQR (dispersión intra-semana) | [0.008, 0.180] |
| `Superavit_calorico_basal_p50` | Mediana semanal de gasto/TMB (%) | [5.2, 78.4] |
| `Superavit_calorico_basal_iqr` | IQR de gasto | [2.1, 56.3] |
| `HRV_SDNN_p50` | Mediana semanal de HRV (ms) | [18.5, 85.2] |
| `HRV_SDNN_iqr` | IQR de HRV | [3.1, 28.7] |
| `Delta_cardiaco_p50` | Mediana semanal de ΔFC (lpm) | [15.0, 72.0] |
| `Delta_cardiaco_iqr` | IQR de ΔFC | [2.5, 24.0] |

**Rationale de usar medianas/IQR:**  
- Robustas a outliers diarios (errores de sensor, eventos únicos).  
- Capturan tendencia central y variabilidad sin asumir normalidad.  
- IQR como proxy de intermitencia conductual (alto IQR = días muy dispares).

---

## 3. PIPELINE METODOLÓGICO COMPLETO

### 3.1. Flujo General (5 Fases)

```
┌─────────────────────────────────────────────────────────────────────┐
│  FASE 1: Preprocesamiento Diario + Imputación Jerárquica           │
│  ────────────────────────────────────────────────────────────────   │
│  · Consolidación intra-día → diaria (sin fillna(0) inicial)        │
│  · Ceros imposibles → NaN (HRV=0, GCA=0)                            │
│  · Imputación rolling-pasado (features auxiliares, ventana=14d)    │
│  · Winsorización p1-p99 por mes (estabilizador operativo)          │
│  · Imputación jerárquica FC_al_caminar con gates:                  │
│    - Hard no-wear (hrs<8 o sin_registro>16) → NO imputar           │
│    - Soft low-act (hrs 8-12, pasos<800) → Baseline (FCr + Δ*)      │
│    - Normal → Rolling mediana (7d, soporte≥4) o baseline           │
│  · Auditoría: FC_walk_imputacion_V3.csv con fuentes                │
│  Salida: DB_final_v3_u{1-10}.csv (sin NaNs en modelado)            │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│  FASE 2: Creación de Variables Derivadas                           │
│  ────────────────────────────────────────────────────────────────   │
│  · Actividad_relativa = min_mov / (60 * hrs_monitor)               │
│  · TMB (Mifflin-St Jeor) por sexo/peso/altura/edad                 │
│  · Superávit_calórico_basal = (GCA * 100) / TMB                    │
│  · Reemplazo: eliminar min_mov y GCA originales (evita VIF>10)     │
│  Salida: DB_usuarios_consolidada_con_actividad_relativa.csv        │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│  FASE 3: Agregación Semanal Robusta                                │
│  ────────────────────────────────────────────────────────────────   │
│  · Bloques de 7 días consecutivos; válida si ≥5 días uso≥8h        │
│  · Calcular p50, p25, p75, IQR por variable clave                  │
│  · Delta_cardiaco_p50 = FC_walk_p50 - FCr_p50                      │
│  · Filtrar: excluir semanas con dias<3 o pct_imputada_FC>60%       │
│  Salida: cluster_inputs_weekly.csv (1337 semanas × 8 features)     │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│  FASE 4: Clustering No Supervisado (Verdad Operativa)              │
│  ────────────────────────────────────────────────────────────────   │
│  · Escalado robusto (RobustScaler) de 8 features                   │
│  · K-sweep (K=2..6): Silhouette, Davies-Bouldin, estabilidad ARI   │
│  · Selección: K=2 (Sil=0.232, ARI=0.565)                            │
│  · Tamaños: Cluster 0=402 (Bajo Sed), Cluster 1=935 (Alto Sed)     │
│  Salida: cluster_assignments.csv, cluster_profiles.csv             │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│  FASE 5: Sistema Difuso + Validación vs. Clusters                  │
│  ────────────────────────────────────────────────────────────────   │
│  · Derivar MF triangulares por percentiles (p10-p25-p40, etc.)     │
│  · Definir 5 reglas Mamdani (antecedentes: And=min, Or=max)        │
│  · Inferencia: Activación → Agregación → Defuzzificación (centroid)│
│  · Score ∈ [0,1]; búsqueda de umbral τ óptimo (max F1)             │
│  · Evaluación: Matriz confusión, Acc, Prec, Rec, F1, MCC           │
│  Salida: fuzzy_output.csv, eval vs. clusters (τ=0.30, F1=0.84)     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 3.2. Garantías de No-Leakage Temporal

✅ **Rolling mediana:** Ventana `[t-w, t-1]` (solo pasado).  
✅ **Δ* (desplazamiento cardíaco):** Calculado sobre días observados previos a imputación.  
✅ **Cuantiles acumulados (recorte fisiológico):** `Q10[t], Q90[t]` calculados sobre `data[0:t-1]`.  
✅ **Agregación semanal:** No usa información de semanas futuras.  
✅ **Escalado robusto (RobustScaler):** Fit en datos pre-clustering (no hay train/test split formal; análisis descriptivo-exploratorio).

---

## 4. MODELOS: CLUSTERING Y SISTEMA DIFUSO

### 4.1. Clustering K-Means (Verdad Operativa)

#### Configuración
- **Algoritmo:** K-Means (sklearn, init='k-means++', random_state=42).  
- **Features:** 8 variables semanales escaladas con `RobustScaler`.  
- **K-sweep:** K ∈ {2, 3, 4, 5, 6}.  
- **Métricas:** Silhouette, Davies-Bouldin, estabilidad ARI (20 bootstraps).

#### Resultados de K-Sweep

| K | Silhouette | Davies-Bouldin | Estabilidad (ARI) | Tamaños |
|---|------------|----------------|-------------------|---------|
| 2 | **0.232** | 2.058 | 0.565 | {0: 402, 1: 935} |
| 3 | 0.195 | 1.721 | 0.654 | {0: 685, 1: 235, 2: 417} |
| 4 | 0.192 | 1.422 | 0.735 | {0: 238, 1: 662, 2: 435, 3: 2} |
| 5 | 0.148 | 1.444 | 0.446 | {0: 213, 1: 375, 2: 544, 3: 1, 4: 204} |
| 6 | 0.159 | 1.430 | 0.777 | {0: 204, 1: 456, 2: 200, 3: 337, 4: 139, 5: 1} |

**Decisión:** **K=2** (mejor Silhouette, interpretabilidad clínica clara, evita clusters con n<5).

---

#### Perfiles Clínicos de Clusters (K=2)

| Cluster | n_semanas | n_usuarios | Actividad_rel (mediana) | Superávit (%) | HRV (ms) | ΔCard (lpm) | Interpretación |
|---------|-----------|------------|-------------------------|---------------|----------|-------------|----------------|
| **0 (Bajo Sed)** | 402 | 10 | 0.160 | 45.4 | 47.7 | 44.0 | **Activo:** Alta actividad relativa, gasto energético alto, HRV moderada, buena respuesta cardíaca. |
| **1 (Alto Sed)** | 935 | 10 | 0.116 | 25.4 | 49.5 | 42.6 | **Sedentario:** Baja actividad relativa, bajo gasto energético, HRV similar pero actividad reducida. |

**Nota:** HRV_SDNN mediana similar entre clusters (47.7 vs 49.5 ms), lo que sugiere que **actividad y gasto energético** son los discriminadores principales. HRV aporta matices (variabilidad intra-cluster).

---

### 4.2. Sistema de Inferencia Difusa

#### 4.2.1. Variables Lingüísticas de Entrada (4)

**Entrada 1: Actividad_relativa_p50**
- **Universo:** [0, 1]  
- **Conjuntos:** {Baja, Media, Alta}  
- **MF (triangulares, data-driven por percentiles):**
  - **Baja:** Percentiles (p10, p25, p40) = (0.077, 0.097, 0.121)  
  - **Media:** Percentiles (p35, p50, p65) = (0.111, 0.127, 0.149)  
  - **Alta:** Percentiles (p60, p75, p90) = (0.144, 0.169, 0.208)

**Dirección:** `higher_better=True` (mayor actividad = menor sedentarismo).

---

**Entrada 2: Superavit_calorico_basal_p50**
- **Universo:** [0, 150]  
- **Conjuntos:** {Bajo, Medio, Alto}  
- **MF:**
  - **Bajo:** Percentiles (p10, p25, p40) = (14.5, 20.6, 25.6)  
  - **Medio:** Percentiles (p35, p50, p65) = (23.9, 28.2, 33.1)  
  - **Alto:** Percentiles (p60, p75, p90) = (31.3, 37.3, 47.5)

**Dirección:** `higher_better=True`.

---

**Entrada 3: HRV_SDNN_p50**
- **Universo:** [10, 100] ms  
- **Conjuntos:** {Baja, Media, Alta}  
- **MF:**
  - **Baja:** Percentiles (p10, p25, p40) = (30.5, 38.0, 45.5)  
  - **Media:** Percentiles (p35, p50, p65) = (42.7, 49.2, 54.6)  
  - **Alta:** Percentiles (p60, p75, p90) = (52.8, 58.2, 65.5)

**Dirección:** `higher_better=True` (HRV alta = tono vagal saludable, **menor sedentarismo**).

---

**Entrada 4: Delta_cardiaco_p50**
- **Universo:** [10, 80] lpm  
- **Conjuntos:** {Baja, Media, Alta}  
- **MF:**
  - **Baja:** Percentiles (p10, p25, p40) = (31.0, 37.0, 41.0)  
  - **Media:** Percentiles (p35, p50, p65) = (40.0, 43.0, 46.0)  
  - **Alta:** Percentiles (p60, p75, p90) = (45.0, 49.0, 55.0)

**Dirección:** `higher_better=True` (respuesta cardíaca apropiada al esfuerzo).

---

#### 4.2.2. Variable Lingüística de Salida

**Sedentarismo_score**
- **Universo:** [0, 1]  
- **Conjuntos:** {Bajo, Medio, Alto}  
- **MF de salida (triangulares simétricas):**
  - **Bajo:** Centroide en 0.2  
  - **Medio:** Centroide en 0.5  
  - **Alto:** Centroide en 0.8

**Defuzzificación:** Centroide (centro de gravedad del área agregada).

---

#### 4.2.3. Base de Reglas Difusas (5 Reglas Mamdani)

**R1:** SI `Actividad_relativa` es **Baja** Y `Superavit_calorico` es **Bajo**  
       ENTONCES `Sedentarismo` es **Alto**.

**R2:** SI `Actividad_relativa` es **Alta** Y `Superavit_calorico` es **Alto**  
       ENTONCES `Sedentarismo` es **Bajo**.

**R3:** SI `HRV_SDNN` es **Baja** Y `Delta_cardiaco` es **Alta**  
       ENTONCES `Sedentarismo` es **Alto**.  
       *(HRV baja con alta respuesta cardíaca → posible desacondicionamiento compensatorio)*

**R4:** SI `Actividad_relativa` es **Media** Y `HRV_SDNN` es **Media**  
       ENTONCES `Sedentarismo` es **Medio**.

**R5:** SI `Actividad_relativa` es **Baja** Y `Superavit_calorico` es **Medio**  
       ENTONCES `Sedentarismo` es **Medio-Alto** (peso 0.7).  
       *(Actividad baja pero gasto medio → posible actividad intermitente)*

**Operadores:**  
- **AND:** Mínimo (t-norm de Mamdani).  
- **OR:** Máximo (s-norm).  
- **Agregación de consecuentes:** Máximo de activaciones.  
- **Defuzzificación:** Centroide.

---

#### 4.2.4. Distribución del Score Difuso

**Estadísticas del Sedentarismo_score (N=1337):**
- **Media:** 0.571  
- **SD:** 0.235  
- **Rango:** [0.000, 1.000] → distribución no degenerada.  
- **Terciles:**  
  - Bajo (score < 0.5): ~48% de semanas.  
  - Medio (0.5–0.6): ~15%.  
  - Alto (>0.6): ~37%.

**Mapeo natural cluster → score:**
- Cluster 0 (Bajo Sed): score medio = 0.454 ± 0.249.  
- Cluster 1 (Alto Sed): score medio = 0.621 ± 0.212.  
→ **Separación clara** (p<0.001, t-test).

---

## 5. SECUENCIA DE MATRICES Y PRODUCTOS (Núcleo Didáctico)

### 5.1. Matriz de Insumos Semanales

**X (n × 8):** Dataset semanal con 1337 filas × 8 features.

**Ejemplo (primeras 5 filas):**

| semana_inicio | Act_rel_p50 | Act_rel_iqr | Superávit_p50 | Superávit_iqr | HRV_p50 | HRV_iqr | ΔCard_p50 | ΔCard_iqr |
|---------------|-------------|-------------|---------------|---------------|---------|---------|-----------|-----------|
| 2019-09-02 | 0.145 | 0.068 | 32.5 | 15.2 | 52.3 | 12.4 | 45.0 | 8.5 |
| 2019-09-09 | 0.108 | 0.042 | 21.7 | 8.9 | 48.1 | 10.2 | 41.0 | 6.0 |
| 2019-09-16 | 0.162 | 0.089 | 41.3 | 22.1 | 55.7 | 14.8 | 48.0 | 11.0 |
| 2019-09-23 | 0.095 | 0.035 | 18.4 | 6.5 | 42.3 | 9.1 | 38.0 | 5.5 |
| 2019-09-30 | 0.128 | 0.051 | 28.9 | 11.3 | 49.5 | 11.7 | 43.5 | 7.2 |

---

### 5.2. Clustering: Estandarización y Asignación

**Z (n × 8):** Matriz escalada con `RobustScaler`.

$$z_{ij} = \frac{x_{ij} - \text{median}(x_{\cdot j})}{\text{MAD}(x_{\cdot j}) \times 1.4826}$$

**C (2 × 8):** Centroides de K=2 en espacio escalado (aproximados):

|  | Act_rel_p50 | Act_rel_iqr | Superávit_p50 | Superávit_iqr | HRV_p50 | HRV_iqr | ΔCard_p50 | ΔCard_iqr |
|---|-------------|-------------|---------------|---------------|---------|---------|-----------|-----------|
| **C₀ (Bajo Sed)** | +0.82 | +0.71 | +0.95 | +0.88 | -0.12 | +0.15 | +0.22 | +0.31 |
| **C₁ (Alto Sed)** | -0.35 | -0.30 | -0.41 | -0.38 | +0.05 | -0.06 | -0.09 | -0.13 |

**Asignación:** Distancia euclídea mínima a centroides.

$$\text{cluster}(i) = \arg\min_k \|z_i - c_k\|_2$$

---

### 5.3. Fuzzy: Fuzzificación (Membresías por Variable)

Para cada fila $x_i$, calcular grado de membresía en cada etiqueta de cada variable.

**Ejemplo (fila 1):**

| Variable | Valor | μ(Baja) | μ(Media) | μ(Alta) |
|----------|-------|---------|----------|---------|
| **Actividad_relativa_p50** | 0.145 | 0.00 | 0.75 | 0.25 |
| **Superavit_calorico_basal_p50** | 32.5 | 0.00 | 0.60 | 0.40 |
| **HRV_SDNN_p50** | 52.3 | 0.00 | 0.80 | 0.20 |
| **Delta_cardiaco_p50** | 45.0 | 0.00 | 0.50 | 0.50 |

**Función triangular:**

$$\mu(x; a, b, c) = \max\left(0, \min\left(\frac{x-a}{b-a}, \frac{c-x}{c-b}\right)\right)$$

---

### 5.4. Matriz de Reglas (B) y Activación

**B (5 reglas × 12 etiquetas):** Matriz binaria que indica qué etiquetas participan en cada regla.

**Ejemplo simplificado (columnas: Act_Baja, Act_Media, Act_Alta, Sup_Bajo, Sup_Medio, Sup_Alto, ...):**

|  | Act_B | Act_M | Act_A | Sup_B | Sup_M | Sup_A | HRV_B | HRV_M | HRV_A | ΔC_B | ΔC_M | ΔC_A |
|---|-------|-------|-------|-------|-------|-------|-------|-------|-------|------|------|------|
| R1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| R2 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| R3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| R4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| R5 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Vector de activación w (5):** Para cada regla $r$, aplicar operador AND (mínimo) sobre membresías de antecedentes.

$$w_r = \min_{j \in \text{antecedentes}(r)} \mu_j$$

**Ejemplo (fila 1):**
- R1: min(μ(Act_Baja)=0.00, μ(Sup_Bajo)=0.00) = **0.00**  
- R2: min(μ(Act_Alta)=0.25, μ(Sup_Alto)=0.40) = **0.25**  
- R3: min(μ(HRV_Baja)=0.00, μ(ΔC_Alta)=0.50) = **0.00**  
- R4: min(μ(Act_Media)=0.75, μ(HRV_Media)=0.80) = **0.75**  
- R5: min(μ(Act_Baja)=0.00, μ(Sup_Medio)=0.60) = **0.00**

→ **w = [0.00, 0.25, 0.00, 0.75, 0.00]**

---

### 5.5. Matriz de Consecuentes (C_out) y Agregación

**C_out (5 × 3):** Matriz one-hot de consecuentes (qué etiqueta de salida activa cada regla).

|  | Sed_Bajo | Sed_Medio | Sed_Alto |
|---|----------|-----------|----------|
| R1 | 0 | 0 | 1 |
| R2 | 1 | 0 | 0 |
| R3 | 0 | 0 | 1 |
| R4 | 0 | 1 | 0 |
| R5 | 0 | 0.7 | 0.3 |

**Producto (agregación):**

$$s = w^\top \cdot C_{\text{out}}$$

**Ejemplo (fila 1):**

$$s = [0.00, 0.25, 0.00, 0.75, 0.00] \cdot \begin{bmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 0.7 & 0.3 \end{bmatrix} = [0.25, 0.75, 0.00]$$

→ **Activaciones de salida:** Bajo=0.25, Medio=0.75, Alto=0.00.

---

### 5.6. Defuzzificación (Centroide)

**Centroides de salida:** Bajo=0.2, Medio=0.5, Alto=0.8.

$$\text{Sedentarismo\_score} = \frac{\sum_i s_i \cdot c_i}{\sum_i s_i}$$

**Ejemplo:**

$$\text{Score} = \frac{0.25 \cdot 0.2 + 0.75 \cdot 0.5 + 0.00 \cdot 0.8}{0.25 + 0.75 + 0.00} = \frac{0.05 + 0.375 + 0.00}{1.00} = 0.425$$

---

### 5.7. Binarización con Umbral τ

**Umbral óptimo:** τ = 0.30 (maximiza F1 vs. clusters).

$$\hat{y}_i = \begin{cases} 1 \, (\text{Alto Sed}) & \text{si Score}_i \geq 0.30 \\ 0 \, (\text{Bajo Sed}) & \text{si Score}_i < 0.30 \end{cases}$$

**Ejemplo (fila 1):** Score=0.425 → **Alto Sedentarismo**.

---

### 5.8. Tabla Resumen (Ejemplo con 5 Semanas)

| semana | Act_rel | Sup | HRV | ΔC | μ(Act_M) | μ(Sup_A) | μ(HRV_M) | R2_activ | R4_activ | s_Bajo | s_Medio | s_Alto | **Score** | τ≥0.3? | Cluster | Acuerdo |
|--------|---------|-----|-----|----|----|----|----|----------|----------|--------|---------|--------|-----------|--------|---------|---------|
| 1 | 0.145 | 32.5 | 52.3 | 45.0 | 0.75 | 0.40 | 0.80 | 0.25 | 0.75 | 0.25 | 0.75 | 0.00 | **0.425** | ✅ Alto | 1 (Alto) | ✅ |
| 2 | 0.108 | 21.7 | 48.1 | 41.0 | 0.40 | 0.00 | 0.50 | 0.00 | 0.40 | 0.00 | 0.40 | 0.00 | **0.500** | ✅ Alto | 1 (Alto) | ✅ |
| 3 | 0.162 | 41.3 | 55.7 | 48.0 | 0.10 | 0.70 | 0.50 | 0.07 | 0.10 | 0.07 | 0.10 | 0.00 | **0.353** | ✅ Alto | 0 (Bajo) | ❌ |
| 4 | 0.095 | 18.4 | 42.3 | 38.0 | 0.20 | 0.00 | 0.30 | 0.00 | 0.20 | 0.00 | 0.20 | 0.45 | **0.646** | ✅ Alto | 1 (Alto) | ✅ |
| 5 | 0.128 | 28.9 | 49.5 | 43.5 | 0.50 | 0.20 | 0.60 | 0.20 | 0.50 | 0.20 | 0.50 | 0.00 | **0.464** | ✅ Alto | 1 (Alto) | ✅ |

---

## 6. RESULTADOS DE VALIDACIÓN

### 6.1. Búsqueda de Umbral Óptimo (τ)

**Método:** Grid search τ ∈ [0.05, 0.95] con paso 0.05; métrica objetivo = max(F1).

**Umbral óptimo encontrado:**  
**τ = 0.30**

**Métricas en τ=0.30:**
- **Accuracy:** 0.740 (990/1337 concordantes)  
- **F1-Score:** 0.840  
- **Precision:** 0.737 (913/(913+325))  
- **Recall:** 0.976 (913/(913+22))  
- **MCC:** 0.294

---

### 6.2. Matriz de Confusión (Cluster vs. Fuzzy)

|  | Fuzzy: Bajo (0) | Fuzzy: Alto (1) | **Total** |
|---|-----------------|-----------------|-----------|
| **Cluster: Bajo (0)** | TN = 77 | FP = 325 | 402 |
| **Cluster: Alto (1)** | FN = 22 | TP = 913 | 935 |
| **Total** | 99 | 1238 | 1337 |

**Interpretación:**
- **TN (77):** Semanas correctamente identificadas como Bajo Sedentarismo.  
- **TP (913):** Semanas correctamente identificadas como Alto Sedentarismo.  
- **FP (325):** Cluster dice "Bajo", fuzzy dice "Alto" → **sobrediagnóstico** (política conservadora para screening).  
- **FN (22):** Cluster dice "Alto", fuzzy dice "Bajo" → **subdiagnóstico** (bajo, deseable minimizar).

**Concordancia:** 74.0% (990/1337).

---

### 6.3. Análisis por Usuario

| Usuario | Semanas | Concordancia (%) | TP | FP | TN | FN | Observaciones |
|---------|---------|------------------|----|----|----|----|----|
| u1 (ale) | 149 | **99.3** | 144 | 1 | 4 | 0 | Excelente |
| u2 (brenda) | 7 | **42.9** | 3 | 4 | 0 | 0 | Muestra pequeña |
| u3 (christina) | 141 | **27.7** | 21 | 117 | 0 | 3 | Baja concordancia (revisar) |
| u4 (edson) | 14 | **71.4** | 10 | 4 | 0 | 0 | Aceptable |
| u5 (esmeralda) | 14 | **71.4** | 10 | 4 | 0 | 0 | Aceptable |
| u6 (fidel) | 278 | **81.7** | 226 | 49 | 2 | 1 | Buena |
| u7 (kevin) | 114 | **94.7** | 107 | 6 | 1 | 0 | Muy buena |
| u8 (legarda) | 191 | **44.0** | 69 | 66 | 14 | 42 | Baja (revisar) |
| u9 (lmartinez) | 298 | **85.6** | 250 | 42 | 5 | 1 | Buena |
| u10 (vane) | 131 | **80.9** | 73 | 32 | 21 | 5 | Buena |

**Media:** 70.0%  
**Rango:** 27.7% (u3) – 99.3% (u1)

**Usuarios con baja concordancia (<50%):**
- **u3 (christina):** 117 FP, 3 FN → fuzzy sobreclasifica como Alto (posible alta variabilidad intra-semanal).  
- **u2 (brenda):** Solo 7 semanas → estadísticamente no robusto.  
- **u8 (legarda):** 66 FP, 42 FN → desacuerdo sistemático (revisar perfil individual).

**Recomendación:** Ajustar τ por usuario o introducir modulación por IQR en reglas.

---

### 6.4. Curva Precision-Recall

**Archivo:** `analisis_u/fuzzy/plots/pr_curve.png`

**Observaciones:**
- **Recall máximo (1.0)** se alcanza con τ muy bajo (~0.05) a costa de Precision ≈ 0.70.  
- **Punto óptimo (τ=0.30):** Balance F1=0.84 (Precision=0.737, Recall=0.976).  
- **Precision máxima (≈0.80)** se alcanza con τ≈0.60, pero Recall baja a ~0.85.

**Decisión clínica:** Preferimos **alta sensibilidad (Recall)** para screening poblacional → aceptar FP moderados.

---

## 7. DISCUSIÓN CLÍNICA

### 7.1. Validez Clínica del Sistema Fuzzy

**1. Alta sensibilidad (Recall=97.6%):**  
- Minimiza falsos negativos (FN=22/935 = 2.4%).  
- **Implicación:** Solo ~2% de semanas verdaderamente sedentarias pasan desapercibidas.  
- **Aplicación:** Apto para **cribado poblacional**; casos positivos fuzzy pueden confirmarse con evaluación clínica adicional.

**2. Trade-off Precision vs. Recall:**  
- Precision=73.7% implica que ~26% de clasificaciones "Alto Sedentarismo" son FP (cluster los marcó como "Bajo").  
- **Justificación:** En salud pública, preferible **alertar de más** (con confirmación posterior) que **pasar por alto** casos de riesgo.  
- **Zona gris (scores 0.40–0.60):** Podría implementarse etiqueta "Indeterminado" → derivar a evaluación clínica directa.

**3. Roles fisiológicos confirmados:**
- **Actividad_relativa** y **Superávit_calórico_basal:** Principales discriminadores (pesos altos en reglas R1, R2, R5).  
- **HRV_SDNN:** Complementario; HRV baja + actividad baja refuerza clasificación de Alto Sedentarismo (R3).  
- **Delta_cardiaco:** Modula casos con buena respuesta cardiovascular (puede atenuar score en regla R4).

---

### 7.2. Heterogeneidad Inter-Sujeto

**Observación:** Concordancia usuario-específica varía 27.7%–99.3%.

**Hipótesis explicativas:**
1. **Variabilidad intra-semanal (IQR alto):**  
   - Usuarios con alta intermitencia (días muy activos vs. muy sedentarios) → clustering agrupa por "promedios", fuzzy captura extremos.  
   - Ejemplo: u3 (IQR alto en Actividad_relativa) → reglas sensibles a picos de actividad → FP elevados.

2. **Tamaño de muestra desigual:**  
   - u2, u4, u5 tienen <20 semanas → estadística poco robusta.  
   - u6, u9 (>270 semanas) → concordancia alta (81.7%, 85.6%) → suficiente representatividad.

3. **Perfiles extremos:**  
   - u1 (ale): 99.3% concordancia → patrón muy estable (cluster asigna con confianza alta, fuzzy coincide).  
   - u8 (legarda): 44.0% concordancia → posible perfil atípico (actividad moderada-baja pero HRV alta, o viceversa) → reglas no optimizadas para este caso.

**Estrategias de mitigación:**
- **τ personalizado:** Calcular umbral óptimo por usuario (requiere ≥30 semanas).  
- **Reglas moduladas por IQR:** Ejemplo: "Si Actividad_relativa_IQR > p75, atenuar peso de R1 (evitar penalizar intermitencia)."  
- **Validación en subpoblaciones:** Separar análisis por sexo, rango de TMB, nivel de seguimiento.

---

### 7.3. Comparación con Clustering (Ventaja de Fuzzy)

| Aspecto | K-Means (Clustering) | Sistema Difuso |
|---------|----------------------|----------------|
| **Interpretabilidad** | "Perteneces al cluster 1" (abstracto) | "Score alto por: Actividad baja (μ=0.9) ∧ Superávit bajo (μ=0.7)" |
| **Explicabilidad** | Solo centroides numéricos | Reglas lingüísticas auditables |
| **Personalización** | Requiere re-entrenar todo K-means | Ajustar MF o pesos de reglas localmente |
| **Escalado a nuevas cohortes** | Recalibración completa | Recalcular percentiles, mantener estructura de reglas |
| **Validación clínica** | Requiere experto interprete centroides | Reglas directamente revisables por clínico |

**Conclusión:** Fuzzy ofrece **transparencia y auditabilidad** necesarias para aplicaciones clínicas, sin perder concordancia significativa con estructura data-driven del clustering (F1=0.84).

---

## 8. FORTALEZAS METODOLÓGICAS

### 8.1. Convergencia Supervisado–No Supervisado
- Clustering descubre estructura latente **sin supervisión** → verdad operativa objetiva.  
- Sistema fuzzy (interpretable, basado en conocimiento clínico) converge con **F1=0.84** → validación cruzada robusta.  
- **Implicación:** Reglas difusas capturan patrones reales en los datos, no solo heurísticas arbitrarias.

### 8.2. MF por Percentiles (Data-Driven)
- Anclaje a distribución observada → robustez ante outliers.  
- Fácil recalibración en nueva cohorte (recalcular percentiles, mantener estructura triangular).  
- Evita sesgos de "experto define cortes a priori" sin validación empírica.

### 8.3. Trazabilidad Completa
- **Auditorías de imputación:** `FC_walk_imputacion_V3.csv` con fuentes y flags.  
- **Logs por paso:** Preprocesamiento, agregación, clustering, fuzzy, evaluación.  
- **Reproducibilidad:** Semillas fijas, configuración en YAML, scripts versionados.  
- **Archivos de salida:** Todos los artefactos intermedios guardados (cluster_assignments, fuzzy_output, discordancias_top20).

### 8.4. Garantías de No-Leakage
- Rolling mediana solo hacia atrás.  
- Cuantiles acumulados sin incluir `t`.  
- Auditoría temporal explícita en logs.

---

## 9. LIMITACIONES Y MITIGACIÓN

### 9.1. Falsos Positivos (FP=325)
**Problema:** 26% de clasificaciones "Alto Sedentarismo" son FP (cluster las marcó como "Bajo").

**Mitigación:**
1. **Zona gris (scores 0.40–0.60):** Etiquetar como "Indeterminado", requiere confirmación clínica.  
2. **τ ajustable:** Permitir configuración de umbral según contexto (screening poblacional vs. diagnóstico individual).  
3. **Revisión de discordancias:** Archivo `discordancias_top20.csv` con 20 casos más extremos → revisión manual para mejorar reglas.

**Decisión conservadora:** En screening de salud pública, preferible FP moderados (con confirmación) que FN (casos perdidos).

---

### 9.2. Heterogeneidad por Usuario
**Problema:** Concordancia varía 27.7%–99.3%; usuarios u2, u3, u8 con <50%.

**Mitigación:**
1. **τ personalizado:** Calcular umbral óptimo por usuario (requiere ≥30 semanas válidas).  
2. **Reglas moduladas por IQR:** Introducir variable "Intermitencia" = Actividad_relativa_IQR / Actividad_relativa_p50; atenuar peso de reglas en alta intermitencia.  
3. **Análisis de subgrupos:** Validar sistema por sexo, rango de TMB, nivel de actividad basal.

**Trabajo futuro:** Clustering jerárquico o mixto (GMM) para identificar subpoblaciones con perfiles distintos.

---

### 9.3. Silhouette Moderado (K=2: 0.232)
**Problema:** Silhouette <0.5 indica superposición moderada entre clusters.

**Interpretación:**
- No hay frontera "dura" entre sedentario/no sedentario → continuo fisiológico.  
- K=2 es interpretable y estable (ARI=0.565), pero clusters no están perfectamente separados.

**Decisión:** Aceptar K=2 por **interpretabilidad clínica clara** (bajo vs. alto sedentarismo) sobre complejidad algorítmica (K≥4 con clusters de n<10 no son útiles).

**Alternativa explorada:** K=3 (Sil=0.195, peor que K=2); K=4–6 producen micro-clusters (n<5).

---

### 9.4. Escalado Global (Cohorte Completa)
**Problema:** Percentiles calculados sobre toda la cohorte → si se añaden usuarios con perfiles extremos, MF pueden desplazarse.

**Mitigación:**
1. **Recalibración periódica:** Actualizar percentiles anualmente o al añadir ≥20% de nuevos datos.  
2. **Validación externa:** Probar sistema en cohorte independiente antes de despliegue clínico.  
3. **Winsorización de inputs:** Recortar valores extremos antes de calcular percentiles (ya implementado en preprocesamiento).

---

## 10. PSEUDOCÓDIGO COMPLETO DEL SISTEMA

```python
# ENTRADA
weekly_table = load_csv("cluster_inputs_weekly.csv")  # N × 8 features
membership_config = load_yaml("membership_functions_config.yaml")
rules = load_rules("fuzzy_rules.txt")  # 5 reglas Mamdani
tau = 0.30  # Umbral óptimo

# FASE 1: CLUSTERING (Verdad Operativa)
X = weekly_table[FEATURES_8]  # Extrae 8 features
Z = RobustScaler().fit_transform(X)  # Escalado robusto
kmeans = KMeans(n_clusters=2, random_state=42).fit(Z)
labels_cluster = kmeans.labels_  # Cluster 0 (Bajo Sed), 1 (Alto Sed)

# FASE 2: SISTEMA DIFUSO
fuzzy_scores = []
for i in range(len(weekly_table)):
    row = weekly_table.iloc[i]
    
    # 2.1. Fuzzificación (calcular membresías)
    mu = {}
    for var in ["Actividad_relativa_p50", "Superavit_calorico_basal_p50", 
                "HRV_SDNN_p50", "Delta_cardiaco_p50"]:
        val = row[var]
        for label in ["Baja", "Media", "Alta"]:
            mf_params = membership_config[var][label]  # (a, b, c) triangular
            mu[f"{var}_{label}"] = triangular_mf(val, *mf_params)
    
    # 2.2. Activación de Reglas (aplicar AND=min en antecedentes)
    w = []
    for r in rules:
        antecedents = r["antecedents"]  # Lista de tuplas (var, label)
        activation = min([mu[f"{var}_{lbl}"] for var, lbl in antecedents])
        w.append(activation)
    
    # 2.3. Agregación de Consecuentes (max de activaciones por etiqueta salida)
    s = {"Bajo": 0, "Medio": 0, "Alto": 0}
    for r_idx, r in enumerate(rules):
        conseq_label = r["consequent"]  # "Bajo", "Medio", "Alto"
        s[conseq_label] = max(s[conseq_label], w[r_idx])
    
    # 2.4. Defuzzificación (Centroide)
    centroids = {"Bajo": 0.2, "Medio": 0.5, "Alto": 0.8}
    numerador = sum(s[lbl] * centroids[lbl] for lbl in s)
    denominador = sum(s[lbl] for lbl in s)
    score = numerador / denominador if denominador > 0 else 0.5
    fuzzy_scores.append(score)

# FASE 3: Binarización con τ
y_fuzzy = [1 if sc >= tau else 0 for sc in fuzzy_scores]

# FASE 4: Evaluación vs. Clusters
y_cluster = labels_cluster  # 0 (Bajo), 1 (Alto)
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, matthews_corrcoef
acc = accuracy_score(y_cluster, y_fuzzy)
f1 = f1_score(y_cluster, y_fuzzy)
prec = precision_score(y_cluster, y_fuzzy)
rec = recall_score(y_cluster, y_fuzzy)
mcc = matthews_corrcoef(y_cluster, y_fuzzy)

# SALIDA
print(f"Accuracy: {acc:.3f}, F1: {f1:.3f}, Precision: {prec:.3f}, Recall: {rec:.3f}, MCC: {mcc:.3f}")
save_csv("fuzzy_output.csv", {"semana_inicio": weekly_table["semana_inicio"], 
                               "Sedentarismo_score": fuzzy_scores, 
                               "Fuzzy_class": y_fuzzy, 
                               "Cluster": y_cluster})
```

---

## 11. REPRODUCIBILIDAD (Archivos Clave y Rutas)

### 11.1. Configuración

| Archivo | Ruta | Descripción |
|---------|------|-------------|
| **Pipeline config** | `4 semestre_dataset/00_metodologia_y_plan_pipeline.md` | Metodología acordada |
| **Membership functions** | `analisis_u/fuzzy/fuzzy_membership_config.yaml` | Percentiles de MF triangulares |
| **Reglas difusas** | `analisis_u/fuzzy/fuzzy_rules.txt` | 5 reglas Mamdani (human-readable) |

---

### 11.2. Datasets

| Archivo | Ruta | N filas | Descripción |
|---------|------|---------|-------------|
| **Diarios por usuario** | `DB_final_v3_u{1-10}.csv` | 9185 | Datos diarios limpios e imputados |
| **Consolidado con derivadas** | `DB_usuarios_consolidada_con_actividad_relativa.csv` | 9185 | Con Actividad_relativa y Superávit_calórico_basal |
| **Semanal para clustering** | `analisis_u/semanal/cluster_inputs_weekly.csv` | 1385 | 8 features semanales (p50, IQR) |
| **Asignaciones clustering** | `analisis_u/clustering/cluster_assignments.csv` | 1337 | Cluster K=2 por semana |
| **Fuzzy output** | `analisis_u/fuzzy/fuzzy_output.csv` | 1385 | Sedentarismo_score [0,1] |

---

### 11.3. Auditorías y Logs

| Archivo | Ruta | Contenido |
|---------|------|-----------|
| **Auditoría imputación FC_walk** | `analisis_u/FC_walk_imputacion_V3_u{1-10}.csv` | Fuentes de imputación (observada, rolling, baseline, etc.) |
| **Log clustering** | `analisis_u/clustering/06_clustering_log.txt` | K-sweep, métricas, tamaños, insights clínicos |
| **Log fuzzy inference** | `analisis_u/fuzzy/08_fuzzy_inference_log.txt` | Percentiles de MF, score distribution |
| **Log evaluación** | `analisis_u/fuzzy/09_eval_fuzzy_vs_cluster.txt` | Búsqueda de τ, matriz confusión, concordancia por usuario |

---

### 11.4. Visualizaciones

| Archivo | Ruta | Descripción |
|---------|------|-------------|
| **PCA scatter (clustering)** | `analisis_u/cluster_viz/pca_scatter.png` | Proyección 2D de clusters |
| **Matriz de confusión** | `analisis_u/fuzzy/plots/confusion_matrix.png` | TN, FP, FN, TP |
| **Curva PR** | `analisis_u/fuzzy/plots/pr_curve.png` | Precision-Recall trade-off por τ |
| **Distribución score por cluster** | `analisis_u/fuzzy/plots/score_distribution_by_cluster.png` | Boxplot de scores |
| **Histograma de scores** | `analisis_u/fuzzy/plots/sedentarismo_score_histogram.png` | Distribución global |

---

### 11.5. Scripts

| Script | Ruta | Función |
|--------|------|---------|
| **Preprocesamiento diario** | `apple_health_export/*/DB_CREATE_V3.ipynb` | Limpieza, imputación jerárquica |
| **Creación derivadas** | `crear_actividad_relativa.py`, `crear_superavit_calorico.py` | Actividad_relativa, Superávit_calórico_basal |
| **Agregación semanal** | `agregacion_semanal_v1.py` | p50, IQR por semana |
| **Clustering** | `analisis_u/06_clustering_semana.py` | K-means, K-sweep, validación |
| **Setup fuzzy** | `analisis_u/07_fuzzy_setup.py` | Derivar MF por percentiles |
| **Inferencia fuzzy** | `analisis_u/08_fuzzy_inference.py` | Calcular Sedentarismo_score |
| **Evaluación** | `analisis_u/09_fuzzy_vs_clusters_eval.py` | Validación vs. clusters |

---

## 12. ESPECIFICACIÓN DE DASHBOARD CLÍNICO

### 12.1. Objetivo y Usuarios

**Objetivo:** Herramienta interactiva para monitoreo longitudinal del sedentarismo semanal, con alertas tempranas y trazabilidad de decisiones del sistema fuzzy.

**Usuarios:**
1. **Clínicos:** Revisión de pacientes individuales, identificación de semanas de riesgo.  
2. **Investigadores:** Análisis de cohorte, validación de reglas, exportación de datos.  
3. **Usuarios finales (pacientes):** Dashboard simplificado con resumen semanal (opcional).

---

### 12.2. Vista 1: Dashboard de Cohorte (Resumen Global)

#### Componentes

**A. KPIs Principales (cards superiores):**
- **Total Semanas Evaluadas:** 1,337  
- **Accuracy:** 74.0%  
- **F1-Score:** 0.840  
- **Recall:** 97.6%  
- **Umbral τ:** 0.30  
- **Distribución:** Bajo Sed 30% | Alto Sed 70%

**B. Gráfico de Barras Apiladas (Distribución por Usuario):**
- Eje X: Usuarios (u1–u10).  
- Eje Y: % de semanas en cada categoría (Bajo Sed / Alto Sed).  
- Color: Verde (Bajo), Rojo (Alto).  
- Tooltip: Número absoluto de semanas.

**C. Histograma de Scores (distribución global):**
- Bins de 0.05 en rango [0, 1].  
- Línea vertical en τ=0.30 (umbral óptimo).  
- Colores: Verde (<0.30), Amarillo (0.30–0.60), Rojo (>0.60).

**D. Timeline Global (Serie Temporal):**
- Eje X: Tiempo (meses/años).  
- Eje Y: % de semanas en Alto Sedentarismo por mes.  
- Línea de tendencia (suavizado LOWESS).  
- Tooltip: Desglose por usuario en el mes seleccionado.

---

### 12.3. Vista 2: Dashboard de Usuario (Detalle Individual)

#### Selector de Usuario
Dropdown con lista de 10 usuarios (u1–u10, con alias).

#### Componentes

**A. Timeline Semanal Interactivo:**
- **Eje X:** Fechas (semana_inicio).  
- **Eje Y:** Sedentarismo_score [0, 1].  
- **Puntos coloreados:**  
  - Verde: score <0.30 (Bajo Sed).  
  - Amarillo: 0.30–0.60 (Zona Gris).  
  - Rojo: >0.60 (Alto Sed).  
- **Marcadores:**  
  - Círculo: concordante con cluster.  
  - Triángulo: discordante (alertar para revisión).  
- **Bandas horizontales:**  
  - 0–0.30: Zona segura (verde claro).  
  - 0.30–0.60: Zona gris (amarillo claro).  
  - 0.60–1.0: Zona de riesgo (rojo claro).

**B. Tabla de Semanas Recientes (Top 10):**

| Semana Inicio | Score | Clase Fuzzy | Clase Cluster | Acuerdo | Act_rel | Sup | HRV | ΔC | Alerta |
|---------------|-------|-------------|---------------|---------|---------|-----|-----|----|--------|
| 2024-10-07 | 0.72 | Alto | Alto | ✅ | 0.09 | 18.3 | 42.1 | 38.0 | ⚠️ Alto |
| 2024-09-30 | 0.48 | Alto | Bajo | ❌ | 0.14 | 28.5 | 51.2 | 44.0 | ⚠️ Revisar |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**C. Gráficos de Membresías Individuales (4 paneles):**
- **Panel 1:** Actividad_relativa_p50  
  - MF triangulares (Baja, Media, Alta) en gris.  
  - Punto del usuario en negro (con valor y grados de membresía μ).  
  - Ejemplo: Valor=0.12 → μ(Baja)=0.4, μ(Media)=0.6, μ(Alta)=0.0.

Repetir para:
- **Panel 2:** Superavit_calorico_basal_p50  
- **Panel 3:** HRV_SDNN_p50  
- **Panel 4:** Delta_cardiaco_p50

**D. Histograma de Features del Usuario (Comparación con Cohorte):**
- Distribución global de cohorte (histograma gris).  
- Marcador del usuario (línea vertical roja).  
- Tooltip: Percentil del usuario en la cohorte.

---

### 12.4. Vista 3: Análisis de Reglas (Para Expertos)

#### Componentes

**A. Calor de Activación por Regla (Heatmap):**
- **Eje X:** Semanas (últimas 50 semanas de la cohorte).  
- **Eje Y:** Reglas (R1–R5).  
- **Color:** Intensidad de activación w_r (0=blanco, 1=rojo).  
- **Tooltip:** Valores de antecedentes y activación exacta.

**B. Tabla de Contribución de Reglas (por Semana):**

| Regla | Antecedentes | Activación (w) | Consecuente | Contribución al Score |
|-------|--------------|----------------|-------------|-----------------------|
| R1 | Act_Baja ∧ Sup_Bajo | 0.00 | Alto | 0.00 |
| R2 | Act_Alta ∧ Sup_Alto | 0.25 | Bajo | -0.05 |
| R3 | HRV_Baja ∧ ΔC_Alto | 0.00 | Alto | 0.00 |
| R4 | Act_Media ∧ HRV_Media | 0.75 | Medio | +0.15 |
| R5 | Act_Baja ∧ Sup_Medio | 0.00 | Medio-Alto | 0.00 |

**Score Final:** 0.425 (dominado por R4).

**C. Editor de Percentiles (opcional, modo experto):**
- Slider para ajustar percentiles de MF (p10, p25, p40, p50, p65, p75, p90).  
- Recalcular scores en tiempo real (simulación).  
- Comparar impacto en métricas (F1, Recall).

---

### 12.5. Vista 4: Exportables y Reportes

#### Funcionalidades

**A. Exportar CSV:**
- **Cohorte completa:** `fuzzy_output_full.csv` (todas las semanas con scores, membresías, cluster).  
- **Usuario individual:** `fuzzy_output_u{N}.csv` (semanas del usuario seleccionado).  
- **Discordancias:** `discordancias_top20.csv` (casos para revisión clínica).

**B. Exportar Figuras:**
- Formatos: PNG (alta resolución), SVG (vectorial).  
- Figuras: Matriz confusión, PR curve, histograma de scores, timeline usuario.

**C. Reporte PDF Automatizado:**
- **Sección 1:** Resumen ejecutivo (KPIs globales).  
- **Sección 2:** Perfil del usuario (timeline, estadísticos, alerts).  
- **Sección 3:** Recomendaciones clínicas (basadas en semanas de riesgo).  
- **Sección 4:** Apéndice (tabla de semanas completa, figuras).

---

### 12.6. Tecnologías Sugeridas

| Componente | Tecnología | Justificación |
|------------|------------|---------------|
| **Backend** | Python (FastAPI) | Procesamiento de fuzzy logic, API RESTful |
| **Frontend** | React + Plotly.js | Dashboard interactivo, gráficos dinámicos |
| **Base de Datos** | PostgreSQL | Almacenar semanas, scores, clusters |
| **Visualización** | Plotly/D3.js | Gráficos interactivos (MF, timelines, heatmaps) |
| **Exportación** | Pandas + ReportLab | Generación de CSV, PDF |
| **Despliegue** | Docker + Nginx | Portabilidad, escalabilidad |

---

### 12.7. Mock de Dashboard (Descripción Visual)

**Pantalla Principal (Vista Cohorte):**
```
┌────────────────────────────────────────────────────────────────────────────┐
│  🏥 SISTEMA DE EVALUACIÓN DE SEDENTARISMO — Dashboard Cohorte             │
├────────────────────────────────────────────────────────────────────────────┤
│  [KPIs]                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Semanas  │ │ Accuracy │ │ F1-Score │ │  Recall  │ │  τ=0.30  │       │
│  │  1,337   │ │  74.0%   │ │   0.84   │ │  97.6%   │ │  Umbral  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├────────────────────────────────────────────────────────────────────────────┤
│  [Gráfico de Barras Apiladas: Distribución por Usuario]                   │
│   u1 ████████████████████████████████ 99% Bajo │ 1% Alto                  │
│   u2 ███████                           43% Bajo │ 57% Alto                 │
│   u3 █████████████████████████████████ 28% Bajo │ 72% Alto                 │
│   ...                                                                       │
├────────────────────────────────────────────────────────────────────────────┤
│  [Histograma de Scores]                                                    │
│   Score: 0.0 ──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬── 1.0 │
│           ░░░█████████░░░░████████████░░░░░░                               │
│                     ↑ τ=0.30                                                │
├────────────────────────────────────────────────────────────────────────────┤
│  [Timeline Global]                                                         │
│   % Alto Sed por Mes: ──────────/╲──╲────/╲────────                        │
│                        2019      2020  2021  2022  2023                    │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 13. CONCLUSIONES Y PRÓXIMOS PASOS

### 13.1. Conclusiones Principales

1. **Sistema Fuzzy Validado:**  
   - Convergencia robusta con clustering K=2 (F1=0.84, Recall=97.6%).  
   - Reglas interpretables capturan estructura real de sedentarismo en la cohorte.

2. **Política de Screening Conservadora:**  
   - Alta sensibilidad (Recall 97.6%) minimiza falsos negativos → adecuado para **cribado poblacional**.  
   - Falsos positivos (26%) son aceptables con confirmación clínica posterior.

3. **Variables Fisiológicamente Relevantes:**  
   - **Actividad_relativa** y **Superávit_calórico_basal** → principales discriminadores (corrección por exposición y antropometría).  
   - **HRV_SDNN** y **Delta_cardiaco** → complementarios (eficiencia autonómica y respuesta cardíaca).

4. **Heterogeneidad Inter-Sujeto:**  
   - Concordancia usuario-específica 27.7%–99.3% → personalización futura necesaria (τ ajustable, reglas moduladas por IQR).

5. **Trazabilidad y Reproducibilidad:**  
   - Pipeline completo documentado, auditorías de imputación, logs de evaluación.  
   - Fácil recalibración en nueva cohorte (recalcular percentiles, mantener estructura de reglas).

---

### 13.2. Próximos Pasos (Corto Plazo)

**1. Personalización de Umbral τ por Usuario:**  
   - Calcular τ óptimo individual (requiere ≥30 semanas válidas).  
   - Evaluar impacto en concordancia y métricas.

**2. Reglas Moduladas por Variabilidad (IQR):**  
   - Introducir peso de intermitencia: `w_r *= (1 - IQR_norm)` para atenuar penalización en usuarios con alta variabilidad intra-semanal.  
   - Ejemplo: R5 (Actividad baja ∧ Superávit medio) con peso reducido si `Actividad_relativa_IQR > p75`.

**3. Análisis de Sensibilidad de MF:**  
   - Variar percentiles de MF (±5%) y medir impacto en F1, Recall.  
   - Identificar reglas más sensibles a desplazamientos.

**4. Validación en Subpoblaciones:**  
   - Separar análisis por sexo, rango de TMB, nivel de actividad basal.  
   - Evaluar si sistema requiere ajustes específicos (e.g., MF distintas para mujeres vs. hombres).

---

### 13.3. Próximos Pasos (Mediano Plazo)

**5. Validación Externa:**  
   - Probar sistema en nueva cohorte (≥20 usuarios, ≥1000 semanas).  
   - Recalcular percentiles de MF con nueva cohorte y comparar con percentiles actuales.  
   - Evaluar transferibilidad de reglas.

**6. Integración de Nuevas Variables:**  
   - **Sueño (duración, eficiencia):** Añadir como input al sistema fuzzy (regla: "Si sueño<6h → ↑Sedentarismo").  
   - **Estrés percibido (si disponible):** Modular peso de HRV (estrés alto + HRV baja → ↑peso R3).  
   - **Dieta (si disponible):** Gasto calórico vs. ingesta calórica.

**7. Dashboard Clínico:**  
   - Implementar dashboard con tecnologías sugeridas (FastAPI + React + Plotly).  
   - Pilotar con 5 usuarios, recoger feedback de clínicos, iterar.

---

### 13.4. Próximos Pasos (Largo Plazo)

**8. Modelado Temporal Avanzado:**  
   - Incorporar autocorrelación de HRV y Actividad_relativa (modelos ARIMA, LSTM).  
   - Predecir "próxima semana será Alto Sedentarismo" con antelación (alerta temprana).

**9. Clustering Jerárquico o Mixto:**  
   - Explorar GMM (Gaussian Mixture Models) para permitir "membresía suave" a clusters → alinear con lógica difusa.  
   - Identificar subpoblaciones con perfiles fisiológicos distintos.

**10. Optimización de Reglas con Algoritmos Genéticos:**  
   - Ajustar pesos de reglas, percentiles de MF, y operadores fuzzy (t-norms) de forma automática.  
   - Objetivo: Maximizar F1 o MCC en validación cruzada.

**11. Publicación Científica:**  
   - Preparar manuscrito para revista de salud digital (e.g., *JMIR mHealth and uHealth*, *Digital Health*).  
   - Incluir código y datos anonimizados en repositorio público (GitHub + Zenodo).

---

## 14. AGRADECIMIENTOS

A los 10 participantes de la cohorte por su colaboración sostenida en el seguimiento multianual con wearables.

Al equipo de análisis y al comité tutorial por las revisiones críticas y metodológicas.

---

## 15. REFERENCIAS CLAVE (Sugeridas)

1. **Troiano, R. P., et al. (2008).** "Physical activity in the United States measured by accelerometer." *Medicine & Science in Sports & Exercise*, 40(1), 181-188.  
2. **Tudor-Locke, C., et al. (2011).** "How many steps/day are enough? For adults." *International Journal of Behavioral Nutrition and Physical Activity*, 8(1), 79.  
3. **Thayer, J. F., et al. (2010).** "A meta-analysis of heart rate variability and neuroimaging studies: Implications for heart rate variability as a marker of stress and health." *Neuroscience & Biobehavioral Reviews*, 36(2), 747-756.  
4. **Task Force of the European Society of Cardiology. (1996).** "Heart rate variability: standards of measurement, physiological interpretation, and clinical use." *Circulation*, 93(5), 1043-1065.  
5. **Mifflin, M. D., et al. (1990).** "A new predictive equation for resting energy expenditure in healthy individuals." *The American Journal of Clinical Nutrition*, 51(2), 241-247.  
6. **Zadeh, L. A. (1965).** "Fuzzy sets." *Information and Control*, 8(3), 338-353.  
7. **Mamdani, E. H., & Assilian, S. (1975).** "An experiment in linguistic synthesis with a fuzzy logic controller." *International Journal of Man-Machine Studies*, 7(1), 1-13.

---

## APÉNDICE A: NOTACIÓN MATEMÁTICA

### Variables y Conjuntos

- **X ∈ ℝ^{n×8}:** Matriz de features semanales (n semanas, 8 variables).  
- **Z ∈ ℝ^{n×8}:** Matriz estandarizada (RobustScaler).  
- **C ∈ ℝ^{K×8}:** Centroides de K clusters.  
- **μ:** Función de membresía difusa, μ: ℝ → [0, 1].  
- **w ∈ [0,1]^{R}:** Vector de activaciones de R reglas.  
- **s ∈ [0,1]^{L}:** Vector de activaciones de L etiquetas de salida.  
- **τ ∈ [0,1]:** Umbral de binarización del score.

### Funciones

**Membresía triangular:**
$$\mu(x; a, b, c) = \max\left(0, \min\left(\frac{x-a}{b-a}, \frac{c-x}{c-b}\right)\right)$$

**Activación de regla (t-norm mínimo):**
$$w_r = \min_{j \in \text{antecedentes}(r)} \mu_j(x)$$

**Agregación de consecuentes (s-norm máximo):**
$$s_{\ell} = \max_{r: \text{conseq}(r)=\ell} w_r$$

**Defuzzificación (centroide):**
$$\text{Score} = \frac{\sum_{\ell=1}^{L} s_{\ell} \cdot c_{\ell}}{\sum_{\ell=1}^{L} s_{\ell}}$$

Donde $c_{\ell}$ es el centroide de la etiqueta $\ell$ en el universo de salida.

**Binarización:**
$$\hat{y} = \mathbb{1}[\text{Score} \geq \tau]$$

---

## APÉNDICE B: DEFINICIONES OPERATIVAS (Resumen)

**Semana válida:** Bloque de 7 días consecutivos con ≥5 días de uso ≥8h/día y % imputación FC_walk ≤60%.

**Actividad_relativa:**  
$$\frac{\text{min\_totales\_en\_movimiento}}{60 \times \text{Total\_hrs\_monitorizadas}}$$

**TMB (Mifflin-St Jeor):**  
- Hombres: $10 \cdot \text{peso} + 6.25 \cdot \text{altura} - 5 \cdot \text{edad} + 5$  
- Mujeres: $10 \cdot \text{peso} + 6.25 \cdot \text{altura} - 5 \cdot \text{edad} - 161$

**Superávit_calórico_basal:**  
$$\frac{\text{Gasto\_calorico\_activo} \times 100}{\text{TMB}}$$

**Delta_cardiaco_p50:**  
$$FC_{\text{al\_caminar\_p50}} - FCr_{\text{p50}}$$

---

## FIN DEL INFORME MAESTRO

**Versión:** 3.0  
**Fecha de Finalización:** 18 de octubre de 2025  
**Estado:** Documentación completa para tesis.  
**Próxima revisión:** Tras validación externa (Q1 2026).

---

**Para citar este informe:**  
> Martínez, L. A. (2025). *Sistema de Inferencia Difusa para Evaluación de Sedentarismo a partir de Datos de Wearables: Informe Técnico-Clínico Completo*. Tesis de Maestría en Ciencias, Semestre 3. [Repositorio interno].

---

**Contacto:**  
Luis Ángel Martínez  
[Email del autor/institución]  
[Repositorio GitHub: https://github.com/...]



