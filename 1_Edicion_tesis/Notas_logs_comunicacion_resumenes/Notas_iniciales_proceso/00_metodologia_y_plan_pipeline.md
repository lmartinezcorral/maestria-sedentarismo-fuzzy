# MODELO DE EVALUACIÓN DEL COMPORTAMIENTO SEDENTARIO MEDIANTE LÓGICA DIFUSA Y DATOS BIOMÉTRICOS

**Documento de Metodología y Plan de Trabajo**

---

**Versión:** 1.0  
**Fecha:** 16 de octubre de 2025  
**Propósito:** Este documento establece la metodología acordada, el pipeline de procesamiento de datos y el plan de trabajo para el desarrollo del modelo de lógica difusa. Define qué se hace, por qué se hace y en qué orden, sirviendo como guía de referencia para el equipo multidisciplinario (científico de datos + clínico).

**Qué cubre:** Consolidación de datos, limpieza, imputación jerárquica, creación de variables derivadas, agregación semanal, clusterización, fuzzificación y validación.

**Qué NO cubre:** Implementación de código (se realizará en prompts posteriores), análisis exploratorio profundo previo (se asume conocimiento de los datos), ni técnicas avanzadas fuera del alcance de la tesis (MICE, detección de change-points, modelos temporales complejos).

---

## 1. RESUMEN EJECUTIVO

### Problema y Motivación

El sedentarismo es un factor de riesgo cardiovascular y metabólico crítico en poblaciones contemporáneas. La evaluación objetiva del comportamiento sedentario requiere métricas que integren múltiples señales biométricas (actividad física, gasto calórico, variabilidad cardíaca) y que sean comparables entre individuos con diferentes características antropométricas.

Este proyecto desarrolla un **modelo de lógica difusa** para clasificar el nivel de sedentarismo semanal a partir de datos de Apple Health/Watch de 10 usuarios, utilizando variables normalizadas por características fisiológicas individuales (TMB, horas monitoreadas) y priorizando interpretabilidad clínica sobre complejidad algorítmica.

### Decisiones Metodológicas Clave

1. **Imputación jerárquica con gates fisiológicos**: No imputamos en condiciones de no-wear documentado (hard no-wear); usamos baselines fisiológicas (FCr + Δ*) en low-activity; aplicamos rolling mediana del pasado en condiciones normales. Evitamos data leakage temporal en todo momento.

2. **Variables derivadas que normalizan por exposición y fisiología**:
   - `Actividad_relativa` corrige por horas monitoreadas (no todos los usuarios tienen 24h de registro diario).
   - `Superávit_calórico_basal` ajusta el gasto calórico por TMB individual (400 kcal no significan lo mismo para un hombre de 124 kg que para una mujer de 58 kg).

3. **Agregación semanal robusta**: La unidad de análisis es la semana (medianas e IQR), no el día. Esto reduce presión sobre imputaciones diarias, amortigua ruido de dispositivos y se alinea con el objetivo clínico (patrones de sedentarismo sostenidos, no fluctuaciones diarias).

4. **Reporte dual de variabilidad**: Distinguimos entre variabilidad "observada pura" (sin imputados) y "operativa" (con imputados). Las varianzas post-normalización NO se interpretan como dispersión fisiológica.

5. **Trade-offs explícitos**: Reconocemos limitaciones (winsorización por mes calendario vs ventanas móviles; imputación simple vs MICE; ventana de 7 días vs 28 días fisiológicos) como decisiones operativas dentro del alcance de tesis, con sensibilidad documentada.

### Entregables del Pipeline

- **DB_final_v3_u{1-10}.csv**: Datasets diarios limpios, imputados, sin NaNs, por usuario.
- **FC_walk_imputacion_V3.csv**: Auditoría de imputación con fuentes y flags.
- **DB_semanal_features.csv**: Features semanales agregados para modelado difuso.
- **cluster_prototypes.csv**: Prototipos de clústeres con interpretación clínica.
- **fuzzy_membership_functions.yaml**: Funciones de membresía y reglas difusas.
- **resultados_sedentarismo_semanal.csv**: Clasificación de sedentarismo por semana/usuario.
- **reporte_sensibilidad.md**: Análisis de sensibilidad a parámetros clave.

---

## 2. DATOS Y VARIABLES

### Origen y Granularidad

- **Fuente**: Apple Health exportado de Apple Watch de 10 usuarios (5 hombres, 5 mujeres).
- **Granularidad original**: Registros intra-día (minutos, eventos).
- **Granularidad de trabajo**: Agregación diaria con zona horaria fijada (`America/Chihuahua`).
- **Período**: Variable por usuario (50–2070 días; total 9185 registros diarios).

### Variables Base (Diarias)

| Variable | Descripción | Unidad | Agregación Intra-día |
|----------|-------------|--------|----------------------|
| `Fecha` | Fecha del registro | YYYY-MM-DD | - |
| `Numero_horas_con_deambulacion` | Horas con registro de movimiento | horas | Conteo |
| `Numero_horas_estacionarias` | Horas sedentarias registradas | horas | Conteo |
| `Total_hrs_monitorizadas` | Suma de horas con señal del dispositivo | horas | Suma |
| `Hrs_sin_registro` | 24 - Total_hrs_monitorizadas | horas | Calculado |
| `min_totales_en_movimiento` | Minutos acumulados en movimiento | minutos | Suma |
| `Total_min_de_ejercicio_diario` | Minutos de ejercicio formal | minutos | Suma |
| `distancia_caminada_en_km` | Distancia recorrida caminando/corriendo | km | Suma |
| `Numero_pasos_por_dia` | Pasos totales | pasos | Suma |
| `FCr_promedio_diario` | Frecuencia cardíaca en reposo (mínimo diario) | lpm | Mínimo |
| `FC_al_caminar_promedio_diario` | Frecuencia cardíaca al caminar | lpm | Media |
| `Gasto_calorico_activo` | Energía activa quemada | kcal | Suma |
| `HRV_SDNN` | Variabilidad de frecuencia cardíaca (SDNN) | ms | Media |

### Variables Derivadas (Reemplazos Justificados)

#### 2.1. Actividad_relativa

**Fórmula:**
```
Actividad_relativa = min_totales_en_movimiento / (60 × Total_hrs_monitorizadas)
```

**Justificación clínica:** Dos usuarios con 30 minutos de movimiento NO son equivalentes si uno tiene 24h monitoreadas (1.25% del tiempo) y otro solo 8h (6.25% del tiempo). `Actividad_relativa` corrige por exposición de monitoreo.

**Decisión operativa:** **Sustituye** a `min_totales_en_movimiento` en análisis multivariados para evitar multicolinealidad (VIF esperado >10 si se mantienen ambas).

**Rango interpretable:** [0, 1], donde:
- 0.0–0.05 = muy baja actividad relativa
- 0.05–0.15 = actividad moderada
- >0.15 = actividad alta sostenida

---

#### 2.2. Superávit_calórico_basal

**Fórmula:**
```
Superávit_calórico_basal = (Gasto_calorico_activo × 100) / TMB
```

Donde **TMB** (Tasa Metabólica Basal) se calcula mediante la ecuación de Mifflin-St Jeor:

**Hombres:**
```
TMB = (10 × peso_kg) + (6.25 × estatura_cm) - (5 × edad_años) + 5
```

**Mujeres:**
```
TMB = (10 × peso_kg) + (6.25 × estatura_cm) - (5 × edad_años) - 161
```

**Justificación fisiológica:** 400 kcal gastadas representan ~18% del TMB para un hombre de 124 kg (TMB ≈ 2241 kcal/día) pero ~31% para una mujer de 58 kg (TMB ≈ 1304 kcal/día). `Superávit_calórico_basal` captura el **impacto fisiológico relativo** del gasto energético.

**Decisión operativa:** **Sustituye** a `Gasto_calorico_activo` en modelado difuso para permitir comparabilidad entre usuarios.

**Nota sobre multicolinealidad:** Como TMB es constante por usuario, existe correlación matemática con `Gasto_calorico_activo`. Se mitiga mediante:
1. No incluir ambas variables simultáneamente en modelos lineales.
2. Verificación de VIF ≤ 5 en el set final.
3. Para modelos no lineales (árboles/GBM), reportar importancia/SHAP.

---

## 3. PIPELINE ACORDADO (ORDEN Y RACIONALIDAD)

### 3.1. Consolidación Diaria Sin Pérdida de Información

**Proceso:**
1. Lectura de CSVs de Apple Health (AppleStandHour, AppleStandTime, AppleExerciseTime, DistanceWalkingRunning, StepCount, HeartRate, ActiveEnergyBurned, HeartRateVariabilitySDNN, WalkingHeartRateAverage).
2. Conversión de timestamps a zona horaria local (`America/Chihuahua`).
3. Agregación diaria por `sourceName` (Apple Watch del usuario) sin `fillna(0)` inicial.
4. Merge outer de todas las variables → DataFrame maestro con NaNs explícitos donde no hubo registro.

**Racionalidad:** Preservar información de missingness estructural (días sin dispositivo ≠ días con valor 0).

---

### 3.2. Limpieza Robusta Sin Borrar Filas

#### Paso 1: Ceros Imposibles → NaN

Variables fisiológicas que no pueden ser 0:
- `HRV_SDNN` = 0 → `NaN` (cero implica error de sensor o no-medición)
- `Gasto_calorico_activo` = 0 → `NaN` (incluso en reposo hay gasto basal)

**No se modifican:** `Numero_pasos_por_dia`, `min_totales_en_movimiento` (cero es plausible en día sedentario o no-wear).

---

#### Paso 2: Imputación de Features Auxiliares

**Variables:** `Gasto_calorico_activo`, `HRV_SDNN`, `distancia_caminada_en_km`, `Numero_pasos_por_dia`, `Total_min_de_ejercicio_diario`.

**Método:** Rolling mediana del pasado (ventana = 14 días, solo valores anteriores) + mediana global como fallback.

**Código conceptual:**
```python
def impute_feature_rolling_past(series, window=14):
    for i in range(len(series)):
        if isna(series[i]):
            past_values = series[max(0, i-window):i].dropna()
            series[i] = median(past_values) if len(past_values) > 0 else median(series)
```

**Justificación:** Evita leak temporal; usa información local reciente; es conservador (mediana robusta a outliers).

**Limitación reconocida:** Ventana de 14 días puede no capturar ciclos fisiológicos largos (menstruación, entrenamiento). Trade-off aceptado por simplicidad y alcance de tesis.

---

#### Paso 3: Winsorización por Mes (Estabilizador Operativo)

**Variables:** `Numero_pasos_por_dia`, `distancia_caminada_en_km`, `Total_min_de_ejercicio_diario`, `Gasto_calorico_activo`, `HRV_SDNN`, `FCr_promedio_diario`.

**Método:** Percentiles p1–p99 **por mes calendario** (YYYY-MM).

**Código conceptual:**
```python
for mes in unique_months:
    subset = data[data.mes == mes]
    if len(subset) >= 20:
        p1, p99 = subset.quantile([0.01, 0.99])
        data.loc[data.mes == mes] = clip(subset, p1, p99)
```

**Racionalidad operativa:**
- Controla outliers extremos (errores de sensor, sincronización) sin eliminar filas.
- Estabiliza comparativas multiusuario y modelos iniciales.

**Limitación conceptual reconocida:**
- El calendario no es fisiología; eventos como enfermedad pueden cruzar meses.
- Se recortan valores extremos válidos si ocurren en colas mensuales.
- Alternativa ideal (ventanas móviles, change-points) queda fuera de alcance de tesis.

**Mitigación:** 
- Winsorización **después** de imputaciones auxiliares.
- Auditoría de outliers retenidos/recortados.
- Reporte de sensibilidad a umbrales p1/p99 vs p5/p95.

---

### 3.3. Imputación Jerárquica de FC_al_caminar (Sin Leak Temporal)

**Objetivo:** Completar `FC_al_caminar_promedio_diario` con método dependiente del contexto fisiológico, evitando inventar datos en condiciones de no-wear documentado.

---

#### Gates de Clasificación de Días

**Gate 1: Hard No-Wear**
```
hard_nowear = (Total_hrs_monitorizadas < 8) OR (Hrs_sin_registro > 16)
```
**Acción:** **NO imputar.** Dejar `NaN` y marcar `FC_walk_fuente = "sin_imputar_hard"`.

**Rationale clínico:** Menos de 8h de monitoreo (o más de 16h sin señal) indica dispositivo no usado. No hay información suficiente para inferir FC al caminar; inventar datos sería metodológicamente irresponsable.

---

**Gate 2: Soft Low-Activity**
```
soft_lowact = (NOT hard_nowear) AND 
              (8 ≤ Total_hrs_monitorizadas < 12) AND 
              (Numero_pasos_por_dia < 800)
```
**Acción:** Imputar con baseline fisiológica.

**Método:**
```
FC_walk_imputada = FCr_promedio_diario + Δ*
```

Donde:
```
Δ* = median(FC_walk_observada - FCr_promedio_diario) [solo en días observados]
```

**Recorte fisiológico:** Acotar a `[P10_histórico, P90_histórico]` calculados acumulativamente hasta `t-1` (sin leak).

**Rationale:** En días con poca actividad documentada (< 800 pasos, monitoreo parcial), es fisiológicamente razonable asumir FC al caminar cercana a FCr + un desplazamiento típico del usuario.

---

**Gate 3: Normal (Actividad Suficiente)**

**Método primario: Rolling mediana del pasado**
- Ventana = 7 días anteriores con datos observados.
- Soporte mínimo = 4 observaciones en ventana.
- Si soporte insuficiente → fallback a baseline (FCr + Δ*).

**Código conceptual:**
```python
for i in range(len(data)):
    if isna(FC_walk_observada[i]) and not hard_nowear[i] and not soft_lowact[i]:
        past_7days = FC_walk_observada[max(0, i-7):i].dropna()
        if len(past_7days) >= 4:
            FC_walk_imputada[i] = median(past_7days)
            fuente[i] = "roll_mediana"
        else:
            FC_walk_imputada[i] = FCr[i] + Δ*
            fuente[i] = "baseline_FCr"
```

**Recorte fisiológico:** Igual que en soft low-activity.

---

**Método secundario opcional: Modelo Ridge (si disponible)**

**Condiciones:**
- n_obs ≥ 60 en datos observados.
- MAE de validación ≤ 8.0 lpm (umbral clínico razonable).

**Features del modelo:**
```
X = [Numero_pasos_por_dia, distancia_caminada_en_km, 
     Total_min_de_ejercicio_diario, Gasto_calorico_activo, 
     FCr_promedio_diario, HRV_SDNN]
y = FC_walk_observada
```

**Validación:** Split temporal 80/20 sobre datos observados.

**Aplicación:** Solo en días normales donde aún falta imputación tras rolling mediana.

**Recorte:** Igual que métodos anteriores.

**Marca:** `FC_walk_fuente = "modelo"`.

---

#### Auditoría y Trazabilidad

**Archivo de salida:** `FC_walk_imputacion_V3.csv`

**Columnas:**
- `Fecha`
- `FCr_promedio_diario`
- `FC_walk_observada` (original)
- `FC_walk_imputada` (resultado final)
- `FC_walk_missing` (0/1)
- `FC_walk_fuente` ("observada" | "roll_mediana" | "baseline_lowAct" | "baseline_FCr" | "modelo" | "sin_imputar_hard")
- `Numero_pasos_por_dia`
- `Total_hrs_monitorizadas`
- `Hrs_sin_registro`
- `hard_nowear_flag` (0/1)
- `soft_lowAct_flag` (0/1)

**Resumen esperado:**
```
FC_walk_fuente.value_counts():
observada         ~60-70%
roll_mediana      ~15-25%
sin_imputar_hard  ~5-10%
baseline_FCr      ~2-5%
baseline_lowAct   ~1-3%
modelo            ~0-5% (si activado)
```

---

### 3.4. Creación de Variables Derivadas

**En este punto del pipeline:**
- Todas las features base están limpias e imputadas (o marcadas como no-imputables).
- `FC_al_caminar_promedio_diario` = `FC_walk_imputada`.

**Cálculo de derivadas:**

1. **Actividad_relativa:**
```python
Actividad_relativa = min_totales_en_movimiento / (60 * Total_hrs_monitorizadas)
```

2. **TMB por usuario** (constante):
```python
if sexo == 'Hombre':
    TMB = 10*peso + 6.25*estatura - 5*edad + 5
else:  # Mujer
    TMB = 10*peso + 6.25*estatura - 5*edad - 161
```

3. **Superávit_calórico_basal:**
```python
Superavit_calorico_basal = (Gasto_calorico_activo * 100) / TMB
```

**Reemplazos en dataset final:**
- Eliminar `min_totales_en_movimiento` (sustituido por `Actividad_relativa`).
- Eliminar `Gasto_calorico_activo` original (sustituido por `Superavit_calorico_basal`).
- Mantener `TMB` como metadata, no como feature de modelado.

---

### 3.5. Dataset Final Diario

**Archivo de salida:** `DB_final_v3_u{1-10}.csv` (por usuario) o consolidado.

**Características:**
- ✅ Sin NaNs en features de modelado.
- ✅ Todas las imputaciones auditadas y marcadas.
- ✅ Variables derivadas calculadas.
- ✅ Ordenado por `Fecha` ascendente.

**Columnas finales (ejemplo):**
```
Fecha, Numero_horas_con_deambulacion, Numero_horas_estacionarias, 
Total_hrs_monitorizadas, Hrs_sin_registro, Actividad_relativa, 
Total_min_de_ejercicio_diario, distancia_caminada_en_km, 
Numero_pasos_por_dia, FCr_promedio_diario, FC_al_caminar_promedio_diario, 
Superavit_calorico_basal, HRV_SDNN, Usuario
```

---

## 4. VARIABILIDAD Y EFECTOS DE IMPUTACIÓN (DESCRIPTIVO DUAL)

### 4.1. Reportes en Unidades Originales

**Objetivo:** Cuantificar la dispersión fisiológica real ANTES de normalización.

**Vista 1: Observado Puro**
- Solo días con `FC_walk_fuente = "observada"` (sin imputados).
- Métricas por usuario: media, SD, IQR, MAD, CV (coeficiente de variación).
- Variables: `HRV_SDNN`, `Gasto_calorico_activo`, `FC_al_caminar`, `Numero_pasos_por_dia`, `Actividad_relativa`.

**Vista 2: Operativa (Con Imputación)**
- Todos los días válidos (incluye imputados, excluye `sin_imputar_hard`).
- Mismas métricas.

**Comparación:**
```
Δ_dispersión = (SD_operativa - SD_observada) / SD_observada × 100%
```

**Interpretación esperada:**
- Imputación rolling mediana tiende a **comprimir** varianza (reduce dispersión).
- Baseline fisiológica puede **expandir** ligeramente si Δ* sobreestima.
- Reporte numérico + gráficos (violín plots superpuestos).

---

### 4.2. Nota Metodológica Crítica

**Las varianzas calculadas DESPUÉS de normalización z-robust NO se usan para interpretación fisiológica.**

**Razón:** La normalización z-robust (mediana-centrada, escalada por MAD×1.4826) convierte todas las variables a escala comparable pero destruye la información de dispersión original. 

**Ejemplo:**
```
Variable A: SD_original = 1000 pasos → SD_z-robust ≈ 1.0
Variable B: SD_original = 50 ms     → SD_z-robust ≈ 1.0
```

Calcular varianza en datos ya normalizados mide "dispersión técnica relativa", no "variabilidad biológica absoluta".

**Uso correcto de datos normalizados:** Comparabilidad en clustering, modelos multivariados, cálculo de distancias. NO para reportar dispersión fisiológica.

---

### 4.3. Gráficos Obligatorios

1. **Histogramas superpuestos** (observado vs operativa) por variable clave.
2. **Violin plots** por usuario mostrando compresión/expansión de IQR.
3. **Scatter plots** de días imputados vs observados cercanos (validación cualitativa).

---

## 5. AGREGACIÓN SEMANAL PARA MODELADO DIFUSO

### 5.1. Rationale Clínico y Pragmático

**Objetivo:** El sedentarismo es un **patrón sostenido**, no un evento de un día.

**Ventajas de agregación semanal:**
1. **Reduce presión sobre imputaciones diarias:** Errores puntuales se amortiguan al promediar/medianizar.
2. **Alinea con ritmos circadianos y sociales:** Ciclo laboral semanal (5+2 días).
3. **Mejora interpretabilidad clínica:** "Usuario sedentario 3 de cada 4 semanas" es más accionable que "49 de 70 días".
4. **Robustez estadística:** Medianas semanales son menos sensibles a outliers diarios (ruido de dispositivo, eventos únicos).

**Desventaja aceptada:** Pérdida de resolución temporal fina (no detectamos cambios intra-semanales). Trade-off consciente.

---

### 5.2. Definición de Semana

**Criterio:** Bloques de 7 días consecutivos desde la primera fecha con datos del usuario.

**Regla de inclusión:** Semana válida si ≥ 5 días tienen `FC_walk_fuente ≠ "sin_imputar_hard"` (al menos 5 días con señal utilizable).

**Manejo de semanas incompletas:**
- Primera y última semana del usuario: incluir si ≥ 5 días válidos.
- Semanas intermedias con < 5 días: excluir de análisis (marcar en metadata).

---

### 5.3. Features Semanales (Robustos)

**Archivo de salida:** `DB_semanal_features.csv`

**Columnas:**

| Feature | Agregación | Justificación |
|---------|------------|---------------|
| `Usuario` | - | Identificador |
| `Semana_inicio` | Fecha del lunes | Referencia temporal |
| `Dias_validos` | Conteo | Control de calidad |
| `Actividad_relativa_p50` | Mediana | Robusta a outliers, tendencia central |
| `Actividad_relativa_p25` | Percentil 25 | Límite inferior de actividad semanal |
| `Actividad_relativa_p75` | Percentil 75 | Límite superior (variabilidad intra-semana) |
| `Superavit_calorico_basal_p50` | Mediana | Gasto energético típico semanal |
| `Superavit_calorico_basal_p75` | Percentil 75 | Días de mayor gasto |
| `HRV_SDNN_p50` | Mediana | Variabilidad cardíaca típica |
| `HRV_SDNN_iqr` | IQR (p75-p25) | Dispersión intra-semanal (estrés, recuperación) |
| `Delta_cardiaco_p50` | Mediana de (FC_walk - FCr) | Respuesta cardíaca al ejercicio |
| `Pasos_diarios_p50` | Mediana | Actividad en unidades naturales (interpretable) |
| `Pct_dias_nowear` | % días con hard_nowear_flag=1 | Calidad de señal semanal |
| `Hrs_monitorizadas_media` | Media | Exposición promedio al dispositivo |

**Nota sobre percentiles:** Se usan p25/p50/p75 en lugar de media/SD porque son más robustos a días con valores extremos (post-imputación o eventos únicos).

---

### 5.4. Calidad de Señal (Feature Crítico para Fuzzy)

**Definición:**
```python
Calidad_señal_semanal = (1 - Pct_dias_nowear) * min(Hrs_monitorizadas_media / 20, 1.0)
```

**Interpretación:**
- 0.0–0.3: Mala (alta proporción de no-wear o monitoreo muy parcial).
- 0.3–0.7: Aceptable.
- 0.7–1.0: Buena.

**Uso en reglas difusas:** Modular confianza en clasificación de sedentarismo (no clasificar como "sedentario alto" si calidad es mala).

---

## 6. MISSINGNESS Y AUTOCORRELACIÓN (LO JUSTO)

### 6.1. Caracterización de Missingness

**Tipos de missingness en este dataset:**

1. **MNAR estructural (hard no-wear):** El usuario conscientemente no usó el dispositivo. No es aleatorio; puede correlacionar con fines de semana, vacaciones, enfermedad.

2. **MAR condicionado (soft low-activity):** Faltan datos de FC_walk porque hubo poca actividad (no se activó sensor de caminata). Es Missing At Random condicionado por `Numero_pasos_por_dia`.

3. **MCAR técnico:** Errores de sincronización/batería aleatorios (minoritario).

**Estrategia adoptada:**
- **MNAR:** No imputar (respetar ausencia de información).
- **MAR:** Imputar con condicionales fisiológicas (baseline si low-act, rolling si normal).
- **MCAR:** Tratado como MAR (métodos de imputación estándar).

**Métricas reportadas:**
- % días MNAR por usuario (hard no-wear).
- % días MAR imputados (low-act + normal).
- Distribución temporal de missingness (¿clustereado en semanas específicas?).

---

### 6.2. Autocorrelación (ACF) de Features Semanales

**Objetivo:** Verificar que hay estructura temporal razonable (no ruido blanco) pero sin dependencia extrema que violaría supuestos de independencia en clusterización.

**Variables a analizar:**
- `HRV_SDNN_p50` semanal.
- `Actividad_relativa_p50` semanal.

**Test:** Autocorrelación con lag 1–4 semanas.

**Criterio de aceptación:**
- ACF(lag=1) ≈ 0.3–0.7: razonable (hay patrones sostenidos sin dependencia extrema).
- ACF(lag=1) < 0.2: señal muy ruidosa (posible problema de calidad de datos).
- ACF(lag=1) > 0.8: dependencia muy fuerte (considerar diferenciación o modelado temporal).

**Uso:** Documentar para interpretar clusters (si ACF es alta, clusters pueden reflejar "etapas temporales" más que "prototipos de usuario").

---

### 6.3. Garantía de No-Leak Temporal

**Declaración explícita:**

En TODOS los pasos que generan features usadas para clusterización, modelado o evaluación, se cumple:

✅ **Rolling mediana:** Solo usa valores `t-window` a `t-1` (pasado).  
✅ **Cuantiles acumulados:** Calculados sobre `obs[0:t-1]` (sin incluir `t`).  
✅ **Δ* (desplazamiento FCr):** Calculado solo sobre días `FC_walk_fuente = "observada"` previos a imputación.  
✅ **Normalización z-robust:** Fit en train, transform en test (split 80/20 temporal).  
✅ **Agregación semanal:** No usa información de semanas futuras.

**Verificación:** Auditoría de timestamps en logs de imputación.

---

## 7. CLUSTERIZACIÓN (ANTES DEL DIFUSO, CON LO MÍNIMO NECESARIO)

### 7.1. Objetivo

**Descubrir prototipos semanales de comportamiento sedentario** en el espacio de features normalizados, sin supervisión.

**NO comparar "tamaños" de usuarios** (eso ya está normalizado por Actividad_relativa y Superávit_calórico_basal).

**Uso:** Informar el diseño de funciones de membresía (cortes basados en centroides) y validar que las reglas difusas capturen grupos reales en los datos.

---

### 7.2. Algoritmos

**Algoritmo primario: K-Means**
- Distancia: Euclídea.
- Inicialización: k-means++ (determinista con semilla fija).
- Número de clusters: K ∈ {2, 3, 4} (evaluación por métricas).

**Algoritmo secundario: K-Medoids (PAM)**
- Robusto a outliers (usa medianas como centroides).
- Más costoso computacionalmente pero valida robustez de K-Means.

**Comparación:** Si K-Means y K-Medoids producen particiones muy distintas (Adjusted Rand Index < 0.6), indica presencia de outliers influyentes → revisar datos.

---

### 7.3. Selección de K (Número de Clusters)

**Métodos:**

1. **Coeficiente de Silueta:**
```
Silhouette = 1/n Σ (b_i - a_i) / max(a_i, b_i)
```
Donde:
- `a_i` = distancia promedio a puntos del mismo cluster.
- `b_i` = distancia promedio mínima a puntos de otros clusters.

Rango: [-1, 1]. Valores > 0.5 indican separación clara.

2. **Estabilidad por Bootstrap:**
- Resamplear datos 100 veces.
- Clusterizar cada muestra.
- Calcular Adjusted Rand Index entre particiones.
- ARI promedio > 0.7 indica clusters estables.

3. **Interpretabilidad clínica:**
- K=2: demasiado simplista (sedentario/no sedentario).
- K=3–4: óptimo (e.g., sedentario, moderado, activo + variante "activo con baja HRV").
- K>4: riesgo de overfitting; clusters difíciles de interpretar.

**Decisión esperada:** K=3 o K=4 basado en máximo de silueta y validación clínica.

---

### 7.4. Interpretación de Prototipos

**Salida:** `cluster_prototypes.csv`

**Columnas:**
```
Cluster_ID, n_semanas, Actividad_relativa_p50_mean, Superavit_calorico_basal_p50_mean, 
HRV_SDNN_p50_mean, Delta_cardiaco_p50_mean, Interpretacion_clinica
```

**Ejemplo de interpretación esperada (K=3):**

| Cluster | n_semanas | Actividad_rel | Superávit | HRV | Interpretación |
|---------|-----------|---------------|-----------|-----|----------------|
| 0 | 150 | 0.03 | 15% | 35 ms | **Sedentario puro:** muy baja actividad, bajo gasto, HRV baja (posible estrés/desacondicionamiento). |
| 1 | 400 | 0.12 | 30% | 50 ms | **Moderadamente activo:** actividad media, gasto moderado, HRV normal. |
| 2 | 80 | 0.22 | 45% | 45 ms | **Activo intermitente:** alta actividad y gasto pero HRV no óptima (posible sobreentrenamiento o recuperación insuficiente). |

---

### 7.5. Validación

**Sanity checks:**
1. ¿Los clusters se separan visualmente en PCA 2D?
2. ¿Cada cluster tiene al menos 5% de las semanas totales? (evitar clusters triviales).
3. ¿Los centroides tienen sentido fisiológico? (no hay "alta actividad + bajo gasto").

**Uso posterior:** Ajustar cortes de funciones de membresía (e.g., "Actividad_relativa Baja" = percentil 33 si K=3, anclado en frontera cluster 0–1).

---

## 8. FUZZIFICACIÓN Y REGLAS (ENFOCADAS EN SEDENTARISMO)

### 8.1. Variables Lingüísticas de Entrada

**Variable 1: Actividad_relativa**
- Universo: [0, 1]
- Conjuntos: **Baja**, **Media**, **Alta**

**Funciones de membresía (ejemplo con percentiles data-driven):**
```
Baja:  Trapezoidal(0, 0, p33, p50)
Media: Triangular(p25, p50, p75)
Alta:  Trapezoidal(p50, p67, 1, 1)
```

Donde p33, p50, p75 = percentiles de `Actividad_relativa_p50` semanal en todo el dataset.

**Ajuste por clusters:** Si clusterización encuentra K=3, alinear cortes con fronteras entre clusters.

---

**Variable 2: Superávit_calórico_basal**
- Universo: [0, 150] (% del TMB; valores >150% son raros pero posibles)
- Conjuntos: **Bajo**, **Moderado**, **Alto**

**Funciones de membresía:**
```
Bajo:     Trapezoidal(0, 0, 20, 30)
Moderado: Triangular(25, 35, 50)
Alto:     Trapezoidal(45, 60, 150, 150)
```

**Rationale:** 
- <20%: gasto casi basal (muy sedentario).
- 30–50%: gasto moderado (actividad ligera-moderada).
- >60%: gasto alto sostenido (actividad vigorosa).

---

**Variable 3: HRV_SDNN**
- Universo: [10, 100] ms (rango fisiológico observado)
- Conjuntos: **Baja**, **Media**, **Alta**

**Funciones de membresía:**
```
Baja:  Trapezoidal(10, 10, 30, 40)
Media: Triangular(35, 50, 65)
Alta:  Trapezoidal(60, 70, 100, 100)
```

**Nota clínica:** **HRV baja** generalmente indica mayor riesgo cardiovascular, estrés crónico o desacondicionamiento. En lógica difusa, HRV baja refuerza clasificación de sedentarismo alto.

---

**Variable 4: Calidad_señal_semanal**
- Universo: [0, 1]
- Conjuntos: **Mala**, **Aceptable**, **Buena**

**Funciones de membresía:**
```
Mala:      Trapezoidal(0, 0, 0.3, 0.5)
Aceptable: Triangular(0.4, 0.6, 0.8)
Buena:     Trapezoidal(0.7, 0.85, 1, 1)
```

**Uso:** Atenuar confianza en clasificación si calidad es mala.

---

### 8.2. Variable Lingüística de Salida

**Nivel_sedentarismo**
- Universo: [0, 100]
- Conjuntos: **Muy Bajo**, **Bajo**, **Moderado**, **Alto**, **Muy Alto**

**Funciones de membresía (salida):**
```
Muy Bajo:  Trapezoidal(0, 0, 10, 20)
Bajo:      Triangular(15, 25, 40)
Moderado:  Triangular(35, 50, 65)
Alto:      Triangular(60, 75, 90)
Muy Alto:  Trapezoidal(85, 95, 100, 100)
```

---

### 8.3. Base de Reglas Difusas (Pocas, Interpretables)

**Principio:** Priorizar claridad sobre exhaustividad. Reglas basadas en conocimiento clínico + validación con clusters.

**Reglas propuestas (ejemplo con 8–12 reglas):**

1. **SI** `Actividad_relativa` es **Baja** **Y** `Calidad_señal` es **Buena**  
   **ENTONCES** `Nivel_sedentarismo` es **Alto**

2. **SI** `Actividad_relativa` es **Baja** **Y** `HRV_SDNN` es **Baja**  
   **ENTONCES** `Nivel_sedentarismo` es **Muy Alto**

3. **SI** `Actividad_relativa` es **Media** **Y** `Superávit_calórico` es **Bajo**  
   **ENTONCES** `Nivel_sedentarismo` es **Moderado**

4. **SI** `Actividad_relativa` es **Media** **Y** `HRV_SDNN` es **Baja**  
   **ENTONCES** `Nivel_sedentarismo` es **Alto**

5. **SI** `Actividad_relativa` es **Alta**  
   **ENTONCES** `Nivel_sedentarismo` es **Bajo**

6. **SI** `Actividad_relativa` es **Alta** **Y** `Superávit_calórico` es **Alto** **Y** `HRV_SDNN` es **Alta**  
   **ENTONCES** `Nivel_sedentarismo` es **Muy Bajo**

7. **SI** `Calidad_señal` es **Mala**  
   **ENTONCES** `Nivel_sedentarismo` es **Moderado** (valor neutral por incertidumbre)

8. **SI** `Actividad_relativa` es **Baja** **Y** `Calidad_señal` es **Mala**  
   **ENTONCES** `Nivel_sedentarismo` es **Indeterminado** (o Moderado con flag de baja confianza)

**Operadores:**
- AND: Mínimo (Mamdani).
- OR: Máximo.

**Agregación:** Máximo de activaciones de reglas.

**Defuzzificación:** Centro de gravedad (centroid) o bisectriz.

---

### 8.4. Salidas y Ejemplos

**Archivo de salida:** `resultados_sedentarismo_semanal.csv`

**Columnas:**
```
Usuario, Semana_inicio, Nivel_sedentarismo_score (0-100), 
Nivel_sedentarismo_categoria (Muy Bajo|Bajo|Moderado|Alto|Muy Alto),
Actividad_relativa_grado_Baja, Actividad_relativa_grado_Media, Actividad_relativa_grado_Alta,
Calidad_señal_categoria, Confianza (0-1)
```

**Ejemplo de interpretación:**

| Usuario | Semana | Score | Categoría | Interpretación |
|---------|--------|-------|-----------|----------------|
| Usuario_9 | 2019-W42 | 82 | Alto | Actividad_relativa=0.04 (Baja μ=0.9), HRV=32ms (Baja μ=0.7), Calidad=0.85 (Buena) → Sedentarismo alto con alta confianza. |
| Usuario_1 | 2022-W10 | 35 | Moderado | Actividad_relativa=0.11 (Media μ=0.6), Superávit=28% (Moderado μ=0.7), Calidad=0.75 → Moderado. |
| Usuario_6 | 2021-W05 | 18 | Bajo | Actividad_relativa=0.19 (Alta μ=0.8), Superávit=42% (Alto μ=0.5) → Bajo sedentarismo. |

---

### 8.5. Validación de Reglas

**Método 1: Comparación con clusters**
- ¿Cluster 0 (sedentario) tiene mayoría de semanas clasificadas como Alto/Muy Alto?
- ¿Cluster 2 (activo) tiene mayoría clasificadas como Bajo/Muy Bajo?
- Métrica: Concordancia (% correctamente alineados).

**Método 2: Casos extremos**
- Seleccionar 10 semanas con `Actividad_relativa` < p5 → ¿todas clasificadas ≥ Alto?
- Seleccionar 10 semanas con `Actividad_relativa` > p95 → ¿todas clasificadas ≤ Bajo?

**Método 3: Experto clínico**
- Revisar manualmente 20 semanas aleatorias con sus features y clasificación fuzzy.
- ¿Acuerdo ≥ 80%?

---

## 9. VALIDACIÓN Y SENSIBILIDAD (QUÉ VAMOS A REPORTAR)

### 9.1. Análisis de Sensibilidad a Parámetros del Pipeline

**Parámetros críticos a variar:**

| Parámetro | Valor base | Variantes | Métrica de impacto |
|-----------|------------|-----------|-------------------|
| Ventana rolling (imputación FC_walk) | 7 días | 5, 10 | % cambio en SD de FC_walk_imputada |
| Umbral hard no-wear | Total_hrs < 8 | < 6, < 10 | % semanas válidas; cambio en Calidad_señal_media |
| Umbral soft low-act | pasos < 800 | < 500, < 1000 | % días imputados con baseline; cambio en FC_walk_p50 |
| Percentiles winsorización | p1–p99 | p5–p95, p2–p98 | % valores recortados; cambio en SD de features |
| Cortes de membership (Actividad_relativa Baja) | p33 | p25, p40 | % semanas clasificadas como Alto sedentarismo |

**Criterio de robustez:** Si cambiar un parámetro ±20% produce cambios < 10% en clasificaciones finales, el pipeline es robusto.

**Salida:** `reporte_sensibilidad.md` con tablas y gráficos de tornado (sensibilidad relativa).

---

### 9.2. Verificación de Multicolinealidad

**Test: Variance Inflation Factor (VIF)**

Aplicado al set de features semanales antes de clusterización:
```
VIF(X_j) = 1 / (1 - R²_j)
```

Donde R²_j = coeficiente de determinación al regresar X_j sobre las demás features.

**Criterio de aceptación:**
- VIF ≤ 5: colinealidad aceptable.
- VIF > 10: colinealidad severa → remover una de las variables correlacionadas.

**Salida esperada:**
```
Actividad_relativa_p50:      VIF = 1.8 ✅
Superavit_calorico_basal_p50: VIF = 2.1 ✅
HRV_SDNN_p50:                VIF = 1.3 ✅
Delta_cardiaco_p50:          VIF = 3.2 ✅
Pasos_diarios_p50:           VIF = 4.5 ✅
```

**Si VIF es alto:** Para modelos no lineales (árboles, GBM), reportar importancia de features (SHAP o permutación) en lugar de coeficientes lineales.

---

### 9.3. Validación de Clusters

**Métrica 1: Coeficiente de Silueta por Cluster**
- Reportar silueta promedio y por cluster.
- Clusters con silueta < 0.3 son débiles (posible fusión).

**Métrica 2: Estabilidad Bootstrap**
- 100 muestras bootstrap.
- Calcular ARI entre particiones.
- ARI_promedio > 0.7 indica clusters replicables.

**Métrica 3: Inspección Visual**
- PCA 2D coloreado por cluster → ¿separación visible?
- t-SNE (perplexity=30) → ¿agrupamientos consistentes?

---

### 9.4. Sanity Checks del Pipeline Completo

1. **Check de NaNs residuales:**
   - `assert DB_final_v3.isna().sum().sum() == 0` (excepto en sin_imputar_hard marcados).

2. **Check de rangos fisiológicos:**
   - FCr ∈ [40, 100] lpm.
   - FC_walk ∈ [60, 180] lpm.
   - HRV_SDNN ∈ [10, 150] ms.
   - Actividad_relativa ∈ [0, 1].

3. **Check de leak temporal:**
   - En set de test (20% temporal), verificar que no hay features calculadas con información del futuro.

4. **Check de consistencia de auditoría:**
   - `FC_walk_fuente.value_counts().sum() == len(DB_final_v3)`.

---

### 9.5. Limitaciones Conocidas y Declaradas

**Limitación 1: Winsorización por mes calendario**
- **Problema:** Corta eventos extremos válidos que cruzan meses.
- **Mitigación:** Auditoría de outliers; análisis de sensibilidad a percentiles.
- **Trabajo futuro:** Ventanas móviles o detección de change-points.

**Limitación 2: Imputación simple (no MICE)**
- **Problema:** No cuantificamos incertidumbre de imputación con intervalos de confianza.
- **Mitigación:** Reporte dual (observado vs operativa); flags de fuente; análisis de sensibilidad.
- **Trabajo futuro:** Implementar multiple imputation para IC robustos.

**Limitación 3: Ventana de 7 días vs ciclos fisiológicos**
- **Problema:** Ciclo menstrual (28 días) no es capturado.
- **Justificación:** No todos los usuarios tienen ciclo menstrual; variabilidad intra-sujeto es alta; alcance de tesis limita complejidad.
- **Mitigación:** Agregación semanal amortigua; gates evitan inventar en no-wear.

**Limitación 4: Generalización a nuevos usuarios**
- **Problema:** Funciones de membresía y cortes están data-driven sobre estos 10 usuarios.
- **Validación necesaria:** Probar en dataset externo antes de despliegue clínico.

---

## 10. REPRODUCIBILIDAD Y GOBERNANZA

### 10.1. Versionado de Artefactos

**Convención de nombres (acordada):**

| Artefact | Nombre | Ubicación |
|----------|--------|-----------|
| Dataset final diario (por usuario) | `DB_final_v3_u{1-10}.csv` | `4 semestre_dataset/` |
| Auditoría imputación | `FC_walk_imputacion_V3_u{1-10}.csv` | `4 semestre_dataset/analisis_u/` |
| Dataset semanal | `DB_semanal_features.csv` | `4 semestre_dataset/` |
| Prototipos de clusters | `cluster_prototypes_K{k}.csv` | `4 semestre_dataset/` |
| Funciones de membresía | `fuzzy_membership_config.yaml` | `4 semestre_dataset/` |
| Reglas difusas | `fuzzy_rules.txt` | `4 semestre_dataset/` |
| Resultados sedentarismo | `resultados_sedentarismo_semanal.csv` | `4 semestre_dataset/` |

**Versionado de scripts:**
- `DB_CREATE_V3.ipynb` → procesamiento diario.
- `agregacion_semanal_v1.py` → features semanales.
- `clusterizacion_v1.py` → K-Means/K-Medoids.
- `fuzzy_inference_v1.py` → motor de inferencia difusa.

---

### 10.2. Semillas Aleatorias y Configuración

**Semillas fijas para reproducibilidad:**
```python
RANDOM_STATE = 42  # K-Means, train/test split, bootstrap
np.random.seed(42)
```

**Archivo de configuración:** `pipeline_config.yaml`

```yaml
imputacion:
  ventana_rolling_dias: 7
  soporte_minimo: 4
  hard_nowear:
    hrs_monitorizadas_min: 8
    hrs_sin_registro_max: 16
  soft_lowact:
    hrs_monitorizadas_min: 8
    hrs_monitorizadas_max: 12
    pasos_max: 800

winsorización:
  percentil_inferior: 0.01
  percentil_superior: 0.99
  por_mes: true

agregacion_semanal:
  dias_minimos_validos: 5

clusterizacion:
  algoritmo: kmeans
  rango_k: [2, 3, 4]
  metrica_seleccion: silhouette
  n_bootstrap: 100

fuzzy:
  defuzzificacion: centroid
  operador_and: minimum
  operador_or: maximum
```

---

### 10.3. Buenas Prácticas de No-Leak

**Checklist obligatorio en cada script:**

✅ **Split temporal:** Train (primeros 80% de semanas por usuario), Test (últimos 20%).  
✅ **Rolling solo hacia atrás:** Ventanas `[t-w, t-1]` nunca incluyen `t` ni futuro.  
✅ **Normalización fit en train, transform en test.**  
✅ **Cuantiles acumulados:** Calculados sobre `data[0:t-1]`.  
✅ **No usar test para ajustar hiperparámetros:** Validación cruzada solo en train.

---

### 10.4. Logs de Experimentos

**Estructura de log (por ejecución):**

```
Fecha: 2025-10-16 14:30:00
Pipeline: DB_CREATE_V3 → Agregacion_semanal → Clusterizacion → Fuzzy
Configuración: pipeline_config.yaml (hash: a3f2d9...)
Semilla: 42
Duración: 18.3 min
Resultados:
  - Semanas totales: 1250
  - K óptimo: 3 (silhouette=0.58)
  - Clasificación sedentarismo:
      Muy Alto: 12%
      Alto: 23%
      Moderado: 35%
      Bajo: 22%
      Muy Bajo: 8%
  - VIF máximo: 4.2
Archivos generados:
  - DB_semanal_features_20251016.csv
  - cluster_prototypes_K3_20251016.csv
  - resultados_sedentarismo_20251016.csv
```

**Herramienta:** MLflow, DVC o simple logging a `pipeline_logs/YYYYMMDD_HHMMSS.txt`.

---

## 11. ROADMAP OPERATIVO (WHAT/NEXT)

### Paso 1: Consolidación y Limpieza Diaria (COMPLETO)
**Script:** `DB_CREATE_V3.ipynb` (ya existente en cada carpeta de usuario).

**Entradas:** CSVs de Apple Health.  
**Salidas:** `DB_final_v3_u{1-10}.csv`, `FC_walk_imputacion_V3.csv`.

**Criterios de aceptación:**
- ✅ 0 NaNs en features de modelado (excepto sin_imputar_hard).
- ✅ Auditoría completa con conteos por fuente.
- ✅ Rangos fisiológicos validados.

---

### Paso 2: Unificación y Creación de Variables Derivadas (COMPLETO)
**Script:** `crear_actividad_relativa.py`, `crear_superavit_calorico.py` (ya existentes).

**Entradas:** `DB_final_v3_u{1-10}.csv`.  
**Salidas:** `DB_usuarios_consolidada_con_actividad_relativa.csv` (con TMB y Superávit_calórico_basal).

**Criterios de aceptación:**
- ✅ Actividad_relativa ∈ [0, 1].
- ✅ Superávit_calórico_basal > 0.
- ✅ TMB correcto por sexo.

---

### Paso 3: Análisis de Variabilidad Dual (PENDIENTE)
**Script a crear:** `analisis_variabilidad_dual.py`.

**Entradas:** `DB_usuarios_consolidada_con_actividad_relativa.csv` + flags de imputación.  
**Salidas:**
- `variabilidad_observada.csv` (solo FC_walk_fuente="observada").
- `variabilidad_operativa.csv` (todos excepto sin_imputar_hard).
- `graficos_variabilidad/` (violín plots, histogramas).

**Criterios de aceptación:**
- ✅ Métricas reportadas en unidades originales (no normalizadas).
- ✅ Δ_dispersión calculado y explicado.
- ✅ Visualizaciones claras.

---

### Paso 4: Agregación Semanal (PENDIENTE)
**Script a crear:** `agregacion_semanal_v1.py`.

**Entradas:** `DB_usuarios_consolidada_con_actividad_relativa.csv`.  
**Salidas:** `DB_semanal_features.csv`.

**Criterios de aceptación:**
- ✅ Solo semanas con ≥ 5 días válidos.
- ✅ Percentiles p25/p50/p75 correctos.
- ✅ Calidad_señal_semanal ∈ [0, 1].
- ✅ n_semanas ≈ 1200–1300 (esperado).

---

### Paso 5: Caracterización de Missingness y ACF (PENDIENTE)
**Script a crear:** `analisis_missingness_acf.py`.

**Entradas:** `DB_usuarios_consolidada_con_actividad_relativa.csv`, `FC_walk_imputacion_V3.csv`.  
**Salidas:**
- `missingness_summary.csv` (% MNAR/MAR por usuario).
- `acf_plots/` (autocorrelación HRV y Actividad_relativa semanal).

**Criterios de aceptación:**
- ✅ % hard_nowear reportado por usuario.
- ✅ ACF(lag=1) documentado.
- ✅ Interpretación de patrones temporales.

---

### Paso 6: Normalización y Split Train/Test (PENDIENTE)
**Script a crear:** `normalizar_y_split.py`.

**Entradas:** `DB_semanal_features.csv`.  
**Salidas:**
- `DB_semanal_train.csv` (80% temporal).
- `DB_semanal_test.csv` (20% temporal).
- `normalization_params.pkl` (medianas y MAD de train).

**Criterios de aceptación:**
- ✅ Fit solo en train.
- ✅ Transform aplicado a ambos sets.
- ✅ No leak: test no influye en parámetros.

---

### Paso 7: Clusterización (PENDIENTE)
**Script a crear:** `clusterizacion_v1.py`.

**Entradas:** `DB_semanal_train.csv` (normalizado).  
**Salidas:**
- `cluster_labels_train.csv`.
- `cluster_prototypes_K{k}.csv`.
- `cluster_validation_metrics.csv` (silueta, ARI bootstrap).
- `cluster_viz/` (PCA, t-SNE).

**Criterios de aceptación:**
- ✅ K seleccionado con silhouette > 0.5.
- ✅ ARI bootstrap > 0.7.
- ✅ Interpretación clínica clara de cada cluster.
- ✅ Cada cluster con ≥ 5% de semanas.

---

### Paso 8: Diseño de Funciones de Membresía (PENDIENTE)
**Script a crear:** `disenar_membership_functions.py`.

**Entradas:** `DB_semanal_train.csv`, `cluster_prototypes_K{k}.csv`.  
**Salidas:** `fuzzy_membership_config.yaml`.

**Criterios de aceptación:**
- ✅ Cortes alineados con percentiles y/o fronteras de clusters.
- ✅ Funciones trapezoidales/triangulares bien definidas.
- ✅ Universos de discurso cubriendo rangos observados + margen.

---

### Paso 9: Definición de Reglas Difusas (PENDIENTE)
**Script a crear:** `definir_reglas_fuzzy.txt` (formato human-readable) + parser.

**Entradas:** Conocimiento clínico + validación con `cluster_labels_train.csv`.  
**Salidas:** `fuzzy_rules.txt`, `fuzzy_rules.pkl` (objeto Python).

**Criterios de aceptación:**
- ✅ 8–12 reglas interpretables.
- ✅ Cobertura de casos principales (alta actividad, baja actividad, calidad mala).
- ✅ Validación: clusters sedentarios → clasificación Alta/Muy Alta ≥ 70%.

---

### Paso 10: Motor de Inferencia Difusa (PENDIENTE)
**Script a crear:** `fuzzy_inference_v1.py`.

**Entradas:** `DB_semanal_train.csv`, `fuzzy_membership_config.yaml`, `fuzzy_rules.txt`.  
**Salidas:** `resultados_sedentarismo_train.csv`.

**Criterios de aceptación:**
- ✅ Todas las semanas clasificadas (score 0–100 + categoría).
- ✅ Distribución de categorías razonable (no 90% en una sola).
- ✅ Grados de membresía reportados.

---

### Paso 11: Validación en Test Set (PENDIENTE)
**Script a crear:** `validar_fuzzy_test.py`.

**Entradas:** `DB_semanal_test.csv`, modelos/reglas entrenadas.  
**Salidas:** `resultados_sedentarismo_test.csv`, `metricas_validacion.csv`.

**Criterios de aceptación:**
- ✅ Distribución de categorías similar a train (no drift drástico).
- ✅ Ejemplos extremos clasificados correctamente.
- ✅ Concordancia con experto clínico ≥ 80% en muestra manual.

---

### Paso 12: Análisis de Sensibilidad (PENDIENTE)
**Script a crear:** `analisis_sensibilidad.py`.

**Entradas:** Pipeline completo con parámetros variables.  
**Salidas:** `reporte_sensibilidad.md`, `sensibilidad_tornado.png`.

**Criterios de aceptación:**
- ✅ Variación de 5–7 parámetros clave.
- ✅ Impacto en clasificación final < 10% para robustez.
- ✅ Identificación de parámetros críticos.

---

### Paso 13: Documentación Final y Reporte (PENDIENTE)
**Entregables:**
- Reporte técnico completo (LaTeX/Markdown).
- Presentación de resultados (PowerPoint/Beamer).
- Repositorio con código comentado y README.

**Criterios de aceptación:**
- ✅ Todos los pasos reproducibles desde cero con semilla fija.
- ✅ Limitaciones declaradas explícitamente.
- ✅ Líneas de trabajo futuro identificadas.

---

## 12. APÉNDICE: NOTACIÓN Y FÓRMULAS CLAVE

### A. Desplazamiento Cardíaco Δ*

Mediana del incremento de FC al caminar respecto a FCr, calculada solo sobre días con datos observados:

```
Δ* = median{ FC_walk_observada[i] - FCr_promedio_diario[i] : i ∈ días_observados }
```

**Uso:** Baseline fisiológica para imputación en low-activity y normal sin soporte rolling.

---

### B. Rolling Mediana del Pasado (Sin Leak)

Para cada día `t`, calcula la mediana de los últimos `w` días **anteriores** con datos válidos:

```
roll_med[t] = median{ y[t-w], y[t-w+1], ..., y[t-1] } donde y[t-i] es not NaN
```

**Condición:** Requiere al menos `soporte_mínimo` observaciones válidas en `[t-w, t-1]`.

---

### C. Cuantiles Históricos Acumulados (Sin Leak)

Percentiles 10 y 90 calculados sobre **todos los datos observados hasta `t-1`** (no incluye `t`):

```
Q10[t] = quantile(y[0:t-1], 0.10)
Q90[t] = quantile(y[0:t-1], 0.90)
```

**Uso:** Recorte fisiológico de imputaciones (`y_imputada ← clip(ŷ, Q10[t], Q90[t])`).

---

### D. Actividad_relativa

Proporción de tiempo monitorizado que el usuario estuvo en movimiento:

```
Actividad_relativa = min_totales_en_movimiento / (60 × Total_hrs_monitorizadas)
```

**Rango:** [0, 1], donde:
- 0 = sin movimiento detectado.
- 1 = en movimiento todas las horas monitoreadas (poco probable; implicaría registro continuo de actividad).

---

### E. TMB (Tasa Metabólica Basal, Mifflin-St Jeor)

**Hombres:**
```
TMB = 10 × peso_kg + 6.25 × estatura_cm - 5 × edad_años + 5
```

**Mujeres:**
```
TMB = 10 × peso_kg + 6.25 × estatura_cm - 5 × edad_años - 161
```

**Unidades:** kcal/día (energía basal en reposo absoluto).

---

### F. Superávit_calórico_basal

Porcentaje del gasto calórico activo respecto al metabolismo basal:

```
Superávit_calórico_basal = (Gasto_calorico_activo × 100) / TMB
```

**Interpretación:**
- 10% = gasto muy bajo (casi solo basal).
- 30% = gasto moderado (actividad ligera).
- 50%+ = gasto alto (actividad vigorosa sostenida).

---

### G. Calidad_señal_semanal

Métrica compuesta de adherencia al dispositivo:

```
Calidad_señal_semanal = (1 - Pct_dias_nowear) × min(Hrs_monitorizadas_media / 20, 1.0)
```

Donde:
- `Pct_dias_nowear` = proporción de días con `hard_nowear_flag=1` en la semana.
- `Hrs_monitorizadas_media` = promedio de `Total_hrs_monitorizadas` en días válidos.
- Factor `20h` como referencia de "buen uso" (24h ideal, pero 20h es práctico).

---

### H. Normalización Z-Robust

Centrado por mediana, escalado por MAD (Median Absolute Deviation):

```
z_robust(x) = (x - median(x)) / (1.4826 × MAD(x))
```

Donde:
```
MAD(x) = median(|x - median(x)|)
```

**Factor 1.4826:** Hace que MAD sea comparable a σ bajo normalidad.

**Ventaja:** Robusto a outliers.  
**Desventaja:** No permite interpretación directa de "desviaciones estándar".

---

### I. Coeficiente de Silueta

Medida de calidad de clusterización para cada punto `i`:

```
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

Donde:
- `a(i)` = distancia promedio de `i` a otros puntos en su mismo cluster.
- `b(i)` = distancia promedio mínima de `i` a puntos del cluster más cercano.

**Rango:** [-1, 1]
- s ≈ 1: bien asignado.
- s ≈ 0: en frontera entre clusters.
- s < 0: posiblemente mal asignado.

**Promedio de silueta** sobre todos los puntos mide calidad global de partición.

---

### J. Adjusted Rand Index (ARI)

Medida de concordancia entre dos particiones, corregida por azar:

```
ARI = (RI - E[RI]) / (max(RI) - E[RI])
```

Donde `RI` = Rand Index.

**Rango:** [-1, 1] (pero típicamente [0, 1])
- ARI = 1: particiones idénticas.
- ARI ≈ 0: concordancia aleatoria.

**Uso en bootstrap:** Promediar ARI entre particiones de muestras bootstrap para medir estabilidad de clusters.

---

### K. Variance Inflation Factor (VIF)

Medida de multicolinealidad para feature `X_j`:

```
VIF(X_j) = 1 / (1 - R²_j)
```

Donde `R²_j` = coeficiente de determinación al regresar `X_j` sobre las demás features.

**Interpretación:**
- VIF = 1: sin colinealidad.
- VIF ∈ [1, 5]: colinealidad aceptable.
- VIF > 10: colinealidad severa (considerar eliminar variable).

---

### L. Funciones de Membresía Fuzzy

**Trapezoidal:**
```
μ(x; a, b, c, d) = max(0, min((x-a)/(b-a), 1, (d-x)/(d-c)))
```

Donde:
- `x ∈ [a, b]`: pendiente ascendente.
- `x ∈ [b, c]`: meseta (μ=1).
- `x ∈ [c, d]`: pendiente descendente.
- `x < a` o `x > d`: μ=0.

**Triangular:**
```
μ(x; a, b, c) = max(0, min((x-a)/(b-a), (c-x)/(c-b)))
```

Caso especial de trapezoidal con `b=c` (pico único).

---

## FIN DEL DOCUMENTO

**Fecha de última actualización:** 16 de octubre de 2025  
**Versión:** 1.0  
**Estado:** Metodología cerrada; implementación pendiente según Roadmap.

---

**Próximos pasos:** Ejecutar Paso 3 (Análisis de Variabilidad Dual) en prompt posterior. No proceder con código hasta aprobación de este documento por el equipo.



