"""
08_fuzzy_inference.py
Sistema de Inferencia Difusa para Clasificación de Sedentarismo
Paso 7B: Inferencia semanal usando MF derivadas
"""

import warnings
import yaml
import json
from datetime import datetime
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
BASE_DIR = Path(__file__).parent.resolve()
INPUT_FILE = BASE_DIR / 'analisis_u' / 'semanal' / 'weekly_consolidado.csv'
CONFIG_DIR = BASE_DIR / 'fuzzy_config'
CONFIG_FILE = CONFIG_DIR / 'fuzzy_membership_config.yaml'
SCALERS_FILE = CONFIG_DIR / 'feature_scalers.json'

OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'fuzzy'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR = OUTPUT_DIR / 'plots'
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / '08_fuzzy_inference_log.txt'
OUTPUT_FILE = OUTPUT_DIR / 'fuzzy_output.csv'


def log(msg):
    """Escribe en log y consola"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')


def print_header(title):
    """Imprime encabezado visual"""
    print('\n' + '='*80)
    print(title)
    print('='*80)
    log(f"\n{'='*80}\n{title}\n{'='*80}")

# ============================================================================
# FUNCIONES DE MEMBRESÍA Y OPERADORES
# ============================================================================


def triangular_mf(x, points):
    """Función de membresía triangular"""
    a, b, c = points
    if x <= a:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a) if b > a else 0.0
    elif b < x <= c:
        return (c - x) / (c - b) if c > b else 0.0
    else:
        return 0.0


def fuzzy_and(a, b):
    """Operador AND (mínimo)"""
    return min(a, b)


def fuzzy_or(a, b):
    """Operador OR (máximo)"""
    return max(a, b)


def defuzzify_centroid(memberships, output_range=(0, 1), n_points=100):
    """Defuzzificación por centroide"""
    x = np.linspace(output_range[0], output_range[1], n_points)
    numerator = sum(m * xi for m, xi in zip(memberships, x))
    denominator = sum(memberships)

    if denominator == 0:
        return 0.5  # Valor neutral si no hay activación

    return numerator / denominator


# ============================================================================
# INICIO
# ============================================================================
print_header('FUZZY INFERENCE - PASO 7B: INFERENCIA DIFUSA SEMANAL')
log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Archivo entrada: {INPUT_FILE}")
log(f"Config MF: {CONFIG_FILE}")
log(f"Scalers: {SCALERS_FILE}")

# ============================================================================
# 1. CARGAR CONFIGURACIÓN
# ============================================================================
print_header('1. CARGANDO CONFIGURACIÓN FUZZY')

# Verificar archivos
if not CONFIG_FILE.exists():
    log(f"❌ ERROR: No existe {CONFIG_FILE}")
    log(f"   Ejecuta primero: python 07_fuzzy_setup.py")
    sys.exit(1)

if not SCALERS_FILE.exists():
    log(f"❌ ERROR: No existe {SCALERS_FILE}")
    sys.exit(1)

# Cargar config
with open(CONFIG_FILE, 'r') as f:
    fuzzy_config = yaml.safe_load(f)

with open(SCALERS_FILE, 'r') as f:
    scalers = json.load(f)

log(f"✅ Configuración cargada:")
log(f"   Features con MF: {len(fuzzy_config)}")
for feat in fuzzy_config.keys():
    log(f"     - {feat}")

# ============================================================================
# 2. CARGAR DATOS SEMANALES
# ============================================================================
print_header('2. CARGANDO DATOS SEMANALES')

# Intentar cargar versión con delta si existe
delta_file = BASE_DIR / 'analisis_u' / \
    'semanal' / 'weekly_consolidado_con_delta.csv'
if delta_file.exists():
    df = pd.read_csv(delta_file)
    log(f"✅ Usando versión con Delta: {delta_file.name}")
else:
    df = pd.read_csv(INPUT_FILE)
    log(f"✅ Usando versión original: {INPUT_FILE.name}")

log(f"   Total semanas: {len(df)}")

# Verificar columnas necesarias
required_cols = list(fuzzy_config.keys()) + ['usuario_id', 'semana_inicio']
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    log(f"⚠️  WARNING: Faltan columnas: {missing_cols}")

# ============================================================================
# 3. ESCALAR FEATURES
# ============================================================================
print_header('3. ESCALANDO FEATURES A [0,1]')

df_scaled = df.copy()
scaled_features = []

for feat in fuzzy_config.keys():
    if feat not in df.columns:
        log(f"⚠️  Omitiendo {feat}: no está en el dataset")
        continue

    if feat not in scalers:
        log(f"⚠️  Omitiendo {feat}: no tiene scaler")
        continue

    scaler = scalers[feat]
    feat_min = scaler['min']
    feat_max = scaler['max']

    # Escalar y clipear a [0,1]
    df_scaled[f'{feat}_scaled'] = df[feat].clip(feat_min, feat_max)
    df_scaled[f'{feat}_scaled'] = (
        df_scaled[f'{feat}_scaled'] - feat_min) / (feat_max - feat_min)

    scaled_features.append(feat)
    log(f"✅ {feat}: escalado con min={feat_min:.3f}, max={feat_max:.3f}")

log(f"\n✅ Features escaladas: {len(scaled_features)}")

# ============================================================================
# 4. EVALUAR MEMBRESÍAS
# ============================================================================
print_header('4. EVALUANDO MEMBRESÍAS POR SEMANA')

# Para cada feature y cada etiqueta, calcular membresía
for feat in scaled_features:
    mf_config = fuzzy_config[feat]['membership_functions']

    for label, mf_data in mf_config.items():
        points = mf_data['values']

        # Escalar puntos de quiebre a [0,1]
        feat_min = scalers[feat]['min']
        feat_max = scalers[feat]['max']
        points_scaled = [(p - feat_min) / (feat_max - feat_min)
                         for p in points]
        points_scaled = [max(0, min(1, p)) for p in points_scaled]  # clip

        # Calcular membresía para cada semana
        df_scaled[f'{feat}_{label}_memb'] = df_scaled[f'{feat}_scaled'].apply(
            lambda x: triangular_mf(
                x, points_scaled) if not pd.isna(x) else 0.0
        )

log(f"✅ Membresías calculadas para {len(scaled_features)} features")

# ============================================================================
# 5. APLICAR REGLAS DIFUSAS (MAMDANI)
# ============================================================================
print_header('5. APLICANDO REGLAS DIFUSAS')

# Definir reglas (hardcoded por ahora, fácil de parametrizar después)
# R1: IF Actividad es Baja AND Superavit es Bajo → Sedentarismo Alto
# R2: IF Actividad es Alta AND Superavit es Alto → Sedentarismo Bajo
# R3: IF HRV es Baja AND Delta es Alta_Carga → Sedentarismo Alto
# R4: IF Actividad es Media AND HRV es Media → Sedentarismo Medio
# R5: IF Actividad es Baja AND Superavit es Medio → Sedentarismo Medio-Alto (peso 0.7)

rules = []

# Verificar qué features están disponibles
has_actividad = 'Actividad_relativa_p50' in scaled_features
has_superavit = 'Superavit_calorico_basal_p50' in scaled_features
has_hrv = 'HRV_SDNN_p50' in scaled_features
has_delta = 'Delta_cardiaco_p50' in scaled_features

log(f"\n📋 Definiendo reglas:")
log(f"   Features disponibles: Actividad={has_actividad}, Superavit={has_superavit}, HRV={has_hrv}, Delta={has_delta}")

# R1: Actividad Baja AND Superavit Bajo → Sedentarismo Alto (1.0)
if has_actividad and has_superavit:
    rules.append({
        'id': 'R1',
        'conditions': ['Actividad_relativa_p50_Baja_memb', 'Superavit_calorico_basal_p50_Baja_memb'],
        'output': 1.0,  # Alto sedentarismo
        'weight': 1.0,
        'description': 'Actividad Baja AND Superavit Bajo → Sedentarismo Alto'
    })
    log(f"   ✅ R1: Actividad Baja AND Superavit Bajo → Sedentarismo Alto")

# R2: Actividad Alta AND Superavit Alto → Sedentarismo Bajo (0.0)
if has_actividad and has_superavit:
    rules.append({
        'id': 'R2',
        'conditions': ['Actividad_relativa_p50_Alta_memb', 'Superavit_calorico_basal_p50_Alta_memb'],
        'output': 0.0,  # Bajo sedentarismo
        'weight': 1.0,
        'description': 'Actividad Alta AND Superavit Alto → Sedentarismo Bajo'
    })
    log(f"   ✅ R2: Actividad Alta AND Superavit Alto → Sedentarismo Bajo")

# R3: HRV Baja AND Delta Alta_Carga → Sedentarismo Alto (0.9)
if has_hrv and has_delta:
    rules.append({
        'id': 'R3',
        'conditions': ['HRV_SDNN_p50_Baja_memb', 'Delta_cardiaco_p50_Alta_Carga_memb'],
        'output': 0.9,  # Alto sedentarismo con riesgo CV
        'weight': 1.0,
        'description': 'HRV Baja AND Delta Alta_Carga → Sedentarismo Alto'
    })
    log(f"   ✅ R3: HRV Baja AND Delta Alta_Carga → Sedentarismo Alto")

# R4: Actividad Media AND HRV Media → Sedentarismo Medio (0.5)
if has_actividad and has_hrv:
    rules.append({
        'id': 'R4',
        'conditions': ['Actividad_relativa_p50_Media_memb', 'HRV_SDNN_p50_Media_memb'],
        'output': 0.5,  # Medio sedentarismo
        'weight': 1.0,
        'description': 'Actividad Media AND HRV Media → Sedentarismo Medio'
    })
    log(f"   ✅ R4: Actividad Media AND HRV Media → Sedentarismo Medio")

# R5: Actividad Baja AND Superavit Medio → Sedentarismo Medio-Alto (0.7, peso 0.7)
if has_actividad and has_superavit:
    rules.append({
        'id': 'R5',
        'conditions': ['Actividad_relativa_p50_Baja_memb', 'Superavit_calorico_basal_p50_Media_memb'],
        'output': 0.7,  # Medio-Alto sedentarismo
        'weight': 0.7,  # Peso modulado
        'description': 'Actividad Baja AND Superavit Medio → Sedentarismo Medio-Alto'
    })
    log(f"   ✅ R5: Actividad Baja AND Superavit Medio → Sedentarismo Medio-Alto (peso 0.7)")

log(f"\n✅ Total reglas activas: {len(rules)}")

# ============================================================================
# 6. INFERENCIA POR SEMANA
# ============================================================================
print_header('6. EJECUTANDO INFERENCIA DIFUSA')

sedentarismo_scores = []
firing_strengths_all = []

for idx, row in df_scaled.iterrows():
    # Calcular firing strength de cada regla
    firing_strengths = []
    outputs = []

    for rule in rules:
        # Evaluar condiciones (AND = min)
        conditions_memb = []
        for cond_col in rule['conditions']:
            if cond_col in row:
                conditions_memb.append(row[cond_col])
            else:
                conditions_memb.append(0.0)

        # Firing strength = min de condiciones * peso
        fs = min(conditions_memb) * rule['weight'] if conditions_memb else 0.0
        firing_strengths.append(fs)
        outputs.append(rule['output'])

    firing_strengths_all.append(firing_strengths)

    # Defuzzificación: weighted average (simplificado)
    if sum(firing_strengths) > 0:
        score = sum(fs * out for fs, out in zip(firing_strengths,
                    outputs)) / sum(firing_strengths)
    else:
        score = 0.5  # Neutral si no hay activación

    sedentarismo_scores.append(score)

df_scaled['Sedentarismo_score'] = sedentarismo_scores

log(f"✅ Inferencia completada: {len(sedentarismo_scores)} semanas")
log(f"   Score medio: {np.mean(sedentarismo_scores):.3f} ± {np.std(sedentarismo_scores):.3f}")
log(f"   Min: {np.min(sedentarismo_scores):.3f}, Max: {np.max(sedentarismo_scores):.3f}")

# Validar distribución
if np.std(sedentarismo_scores) < 0.05:
    log(f"⚠️  WARNING: Distribución degenerada (std < 0.05)")
else:
    log(
        f"✅ Distribución no degenerada (std = {np.std(sedentarismo_scores):.3f})")

# ============================================================================
# 7. GUARDAR SALIDA
# ============================================================================
print_header('7. GUARDANDO RESULTADOS')

# Preparar DataFrame de salida
output_cols = ['usuario_id', 'semana_inicio', 'Sedentarismo_score']

# Agregar membresías opcionales (top 3 por brevedad)
for feat in scaled_features[:3]:
    mf_labels = fuzzy_config[feat]['labels']
    for label in mf_labels:
        col_name = f'{feat}_{label}_memb'
        if col_name in df_scaled.columns:
            output_cols.append(col_name)

# Agregar firing strengths
for i, rule in enumerate(rules):
    df_scaled[f'firing_{rule["id"]}'] = [fs[i] for fs in firing_strengths_all]
    output_cols.append(f'firing_{rule["id"]}')

df_output = df_scaled[output_cols].copy()
df_output.to_csv(OUTPUT_FILE, index=False)
log(f"✅ Guardado: {OUTPUT_FILE.name}")
log(f"   Columnas: {len(output_cols)}")
log(f"   Filas: {len(df_output)}")

# Validar NaNs
nan_count = df_output['Sedentarismo_score'].isna().sum()
if nan_count > 0:
    log(f"⚠️  WARNING: {nan_count} semanas con NaN en score")
else:
    log(f"✅ Sin NaNs en Sedentarismo_score")

# ============================================================================
# 8. ANÁLISIS POR TERCILES
# ============================================================================
print_header('8. ANÁLISIS POR TERCILES')

terciles = np.percentile(sedentarismo_scores, [33.33, 66.67])
log(f"Terciles: p33={terciles[0]:.3f}, p67={terciles[1]:.3f}")

# Manejar caso de terciles duplicados
bins = [0, terciles[0], terciles[1], 1.0]
unique_bins = sorted(set(bins))

if len(unique_bins) < len(bins):
    log(f"⚠️  WARNING: Terciles duplicados, usando bins únicos: {unique_bins}")
    # Usar bins únicos y ajustar labels
    if len(unique_bins) == 2:
        df_output['tercil'] = pd.cut(df_output['Sedentarismo_score'],
                                     bins=unique_bins,
                                     labels=['Bajo-Medio', 'Alto'],
                                     include_lowest=True, duplicates='drop')
    elif len(unique_bins) == 3:
        df_output['tercil'] = pd.cut(df_output['Sedentarismo_score'],
                                     bins=unique_bins,
                                     labels=['Bajo', 'Medio-Alto'],
                                     include_lowest=True, duplicates='drop')
    else:
        df_output['tercil'] = pd.cut(df_output['Sedentarismo_score'],
                                     bins=unique_bins,
                                     labels=['Bajo', 'Medio',
                                             'Alto'][:len(unique_bins)-1],
                                     include_lowest=True, duplicates='drop')
else:
    df_output['tercil'] = pd.cut(df_output['Sedentarismo_score'],
                                 bins=[0, terciles[0], terciles[1], 1.0],
                                 labels=['Bajo', 'Medio', 'Alto'],
                                 include_lowest=True)

tercil_counts = df_output['tercil'].value_counts()
log(f"\nDistribución por terciles:")
for tercil, count in tercil_counts.items():
    pct = count / len(df_output) * 100
    log(f"   {tercil}: {count} semanas ({pct:.1f}%)")

# ============================================================================
# 9. PLOTS OPCIONALES
# ============================================================================
print_header('9. GENERANDO VISUALIZACIONES')

# Histograma de scores
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(sedentarismo_scores, bins=50,
        edgecolor='black', alpha=0.7, color='steelblue')
ax.axvline(terciles[0], color='orange', linestyle='--',
           linewidth=2, label=f'p33={terciles[0]:.2f}')
ax.axvline(terciles[1], color='red', linestyle='--',
           linewidth=2, label=f'p67={terciles[1]:.2f}')
ax.set_xlabel('Sedentarismo Score [0=Bajo, 1=Alto]', fontsize=11)
ax.set_ylabel('Frecuencia', fontsize=11)
ax.set_title(
    f'Distribución de Sedentarismo Score (N={len(sedentarismo_scores)})', fontsize=12, pad=15)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()

hist_file = PLOTS_DIR / 'sedentarismo_score_histogram.png'
fig.savefig(hist_file, dpi=150)
plt.close(fig)
log(f"✅ Guardado: {hist_file.name}")

# ============================================================================
# 10. RESUMEN FINAL
# ============================================================================
print_header('10. RESUMEN EJECUTIVO')

log(f"\n📊 DATOS PROCESADOS:")
log(f"   - Semanas totales: {len(df_output)}")
log(f"   - Features usadas: {len(scaled_features)}")
log(f"   - Reglas activas: {len(rules)}")

log(f"\n📈 SEDENTARISMO SCORE:")
log(f"   - Media: {np.mean(sedentarismo_scores):.3f}")
log(f"   - Desv. Std: {np.std(sedentarismo_scores):.3f}")
log(f"   - Min: {np.min(sedentarismo_scores):.3f}")
log(f"   - Max: {np.max(sedentarismo_scores):.3f}")

log(f"\n📊 DISTRIBUCIÓN POR TERCILES:")
for tercil, count in tercil_counts.items():
    pct = count / len(df_output) * 100
    log(f"   - {tercil}: {count} semanas ({pct:.1f}%)")

log(f"\n✅ ARCHIVOS GENERADOS:")
log(f"   - fuzzy_output.csv")
log(f"   - plots/sedentarismo_score_histogram.png")
log(f"   - 08_fuzzy_inference_log.txt")

print_header('FUZZY INFERENCE COMPLETADO')
log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"\n✅ Listo para evaluación vs clusters (ejecutar 09_fuzzy_vs_clusters_eval.py)")
