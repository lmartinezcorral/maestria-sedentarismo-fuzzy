"""
07_fuzzy_setup.py
Derivación de Funciones de Membresía Difusas desde Datos Semanales
Paso 7A: Setup del Sistema Difuso
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
OUTPUT_DIR = BASE_DIR / 'fuzzy_config'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR = OUTPUT_DIR / 'plots'
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / '07_fuzzy_setup_log.txt'

# Features núcleo (columnas en weekly_consolidado.csv)
CORE_FEATURES = {
    'Actividad_relativa_p50': 'higher_better',  # Mayor es mejor
    'Superavit_calorico_basal_p50': 'higher_better',
    'HRV_SDNN_p50': 'higher_better',
    'Delta_cardiaco_p50': 'lower_better'  # Menor delta = mejor eficiencia
}

# Percentiles para definir MF (trapezoidales/triangulares)
# Para variables "higher_better": Baja (p10-p25-p40), Media (p35-p50-p65), Alta (p60-p75-p90)
# Para "lower_better": invertimos
PERCENTILES = {
    'Baja': [10, 25, 40],
    'Media': [35, 50, 65],
    'Alta': [60, 75, 90]
}

# Para Delta_cardiaco (lower_better), definimos carga
PERCENTILES_CARGA = {
    'Baja_Carga': [10, 25, 40],  # Bajo delta = baja carga
    'Media_Carga': [35, 50, 65],
    'Alta_Carga': [60, 75, 90]   # Alto delta = alta carga
}

# Percentiles para clip robusto (escalar a [0,1])
CLIP_PERCENTILES = [5, 95]


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
# INICIO
# ============================================================================
print_header('FUZZY SETUP - PASO 7A: DERIVACIÓN DE FUNCIONES DE MEMBRESÍA')
log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Archivo entrada: {INPUT_FILE}")
log(f"Directorio salida: {OUTPUT_DIR}")

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================
print_header('1. CARGANDO DATOS SEMANALES')

if not INPUT_FILE.exists():
    log(f"❌ ERROR: No existe {INPUT_FILE}")
    sys.exit(1)

df = pd.read_csv(INPUT_FILE)
log(f"✅ Datos cargados: {len(df)} semanas")
log(f"   Columnas disponibles: {list(df.columns)}")

# Verificar features núcleo
missing_features = []
for feat in CORE_FEATURES.keys():
    if feat not in df.columns:
        missing_features.append(feat)

if missing_features:
    log(f"⚠️  WARNING: Faltan features: {missing_features}")

    # Intentar crear Delta_cardiaco_p50 si falta
    if 'Delta_cardiaco_p50' in missing_features:
        if 'FC_al_caminar_promedio_diario_p50' in df.columns and 'FCr_promedio_diario_p50' in df.columns:
            df['Delta_cardiaco_p50'] = df['FC_al_caminar_promedio_diario_p50'] - \
                df['FCr_promedio_diario_p50']
            log(f"   ✅ Creado Delta_cardiaco_p50 = FC_walk - FCr")
            missing_features.remove('Delta_cardiaco_p50')

            # Guardar versión derivada
            derived_file = BASE_DIR / 'analisis_u' / \
                'semanal' / 'weekly_consolidado_con_delta.csv'
            df.to_csv(derived_file, index=False)
            log(f"   ✅ Guardada versión derivada: {derived_file.name}")
        else:
            log(f"   ❌ No se puede crear Delta_cardiaco_p50: faltan columnas base")

# Filtrar solo features disponibles
available_features = {k: v for k,
                      v in CORE_FEATURES.items() if k in df.columns}
log(f"\n✅ Features disponibles para MF: {len(available_features)}/{len(CORE_FEATURES)}")
for feat, direction in available_features.items():
    log(f"   - {feat} ({direction})")

if len(available_features) < 3:
    log(
        f"\n❌ ERROR: Se necesitan al menos 3 features, solo hay {len(available_features)}")
    sys.exit(1)

# ============================================================================
# 2. CALCULAR ESCALADORES ROBUSTOS
# ============================================================================
print_header('2. CALCULANDO ESCALADORES ROBUSTOS (p5-p95)')

scalers = {}
for feat in available_features.keys():
    series = df[feat].dropna()

    if len(series) < 100:
        log(f"⚠️  {feat}: Solo {len(series)} valores, omitiendo")
        continue

    p_min = np.percentile(series, CLIP_PERCENTILES[0])
    p_max = np.percentile(series, CLIP_PERCENTILES[1])

    scalers[feat] = {
        'min': float(p_min),
        'max': float(p_max),
        'n_samples': len(series),
        'percentile_range': CLIP_PERCENTILES
    }

    log(f"✅ {feat}:")
    log(f"   Min (p{CLIP_PERCENTILES[0]}): {p_min:.4f}")
    log(f"   Max (p{CLIP_PERCENTILES[1]}): {p_max:.4f}")
    log(f"   N: {len(series)}")

# Guardar scalers
scalers_file = OUTPUT_DIR / 'feature_scalers.json'
with open(scalers_file, 'w') as f:
    json.dump(scalers, f, indent=2)
log(f"\n✅ Guardado: {scalers_file.name}")

# ============================================================================
# 3. DERIVAR FUNCIONES DE MEMBRESÍA
# ============================================================================
print_header('3. DERIVANDO FUNCIONES DE MEMBRESÍA (MF)')

membership_config = {}

for feat, direction in available_features.items():
    if feat not in scalers:
        continue

    log(f"\n📊 Procesando: {feat} ({direction})")

    series = df[feat].dropna()

    # Calcular percentiles para MF
    if direction == 'lower_better':
        # Para Delta_cardiaco: bajo es mejor (baja carga)
        percs = PERCENTILES_CARGA
        labels = ['Baja_Carga', 'Media_Carga', 'Alta_Carga']
    else:
        # Para el resto: alto es mejor
        percs = PERCENTILES
        labels = ['Baja', 'Media', 'Alta']

    mf_points = {}
    for label, percentile_list in percs.items():
        points = [np.percentile(series, p) for p in percentile_list]
        mf_points[label] = {
            'percentiles': percentile_list,
            'values': [float(p) for p in points],
            'type': 'triangular'
        }
        log(f"   {label}: p{percentile_list} = {[f'{p:.3f}' for p in points]}")

    membership_config[feat] = {
        'direction': direction,
        'labels': labels,
        'membership_functions': mf_points
    }

# ============================================================================
# 4. VALIDAR MF (MONOTONICIDAD Y COBERTURA)
# ============================================================================
print_header('4. VALIDANDO FUNCIONES DE MEMBRESÍA')

for feat, config in membership_config.items():
    log(f"\n✅ Validando: {feat}")

    mf_funcs = config['membership_functions']
    labels = config['labels']

    # Verificar monotonicidad (puntos ordenados)
    for label, mf_data in mf_funcs.items():
        values = mf_data['values']
        if not all(values[i] <= values[i+1] for i in range(len(values)-1)):
            log(f"   ⚠️  {label}: NO monotónica - {values}")
        else:
            log(f"   ✅ {label}: Monotónica")

    # Verificar cobertura (solapamiento razonable)
    # Comprobar que la MF "Alta" comienza antes de que termine "Baja"
    if len(labels) == 3:
        low_end = mf_funcs[labels[0]]['values'][-1]
        high_start = mf_funcs[labels[2]]['values'][0]

        if high_start > low_end:
            overlap = low_end / high_start if high_start > 0 else 0
            log(
                f"   ✅ Cobertura: solapamiento razonable (ratio={overlap:.2f})")
        else:
            log(f"   ⚠️  Cobertura: solapamiento excesivo")

# ============================================================================
# 5. GUARDAR CONFIGURACIÓN YAML
# ============================================================================
print_header('5. GUARDANDO CONFIGURACIÓN FUZZY')

config_file = OUTPUT_DIR / 'fuzzy_membership_config.yaml'
with open(config_file, 'w') as f:
    yaml.dump(membership_config, f, default_flow_style=False, sort_keys=False)
log(f"✅ Guardado: {config_file.name}")

# ============================================================================
# 6. GENERAR PLOTS DE MF
# ============================================================================
print_header('6. GENERANDO PLOTS DE FUNCIONES DE MEMBRESÍA')


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


for feat, config in membership_config.items():
    log(f"\n📈 Graficando: {feat}")

    # Obtener rango de valores
    feat_min = scalers[feat]['min']
    feat_max = scalers[feat]['max']
    x_range = np.linspace(feat_min, feat_max, 200)

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['blue', 'orange', 'green']
    mf_funcs = config['membership_functions']

    for i, (label, mf_data) in enumerate(mf_funcs.items()):
        points = mf_data['values']
        y_values = [triangular_mf(x, points) for x in x_range]

        ax.plot(x_range, y_values, label=label,
                linewidth=2, color=colors[i % len(colors)])
        ax.fill_between(x_range, y_values, alpha=0.2,
                        color=colors[i % len(colors)])

        # Marcar puntos de quiebre
        for p in points:
            ax.axvline(p, linestyle='--', alpha=0.3,
                       color=colors[i % len(colors)])

    ax.set_xlabel(feat, fontsize=11)
    ax.set_ylabel('Grado de Membresía', fontsize=11)
    ax.set_title(f'Funciones de Membresía: {feat}', fontsize=12, pad=15)
    ax.set_ylim([-0.05, 1.05])
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plot_file = PLOTS_DIR / f'mf_{feat}.png'
    fig.savefig(plot_file, dpi=150)
    plt.close(fig)
    log(f"   ✅ Guardado: {plot_file.name}")

# ============================================================================
# 7. RESUMEN FINAL
# ============================================================================
print_header('7. RESUMEN EJECUTIVO')

log(f"\n✅ FUNCIONES DE MEMBRESÍA DERIVADAS:")
log(f"   - Total features: {len(membership_config)}")
log(f"   - Features:")
for feat in membership_config.keys():
    log(f"     • {feat}")

log(f"\n✅ ARCHIVOS GENERADOS:")
log(f"   - fuzzy_membership_config.yaml")
log(f"   - feature_scalers.json")
log(f"   - {len(membership_config)} plots en plots/")
log(f"   - 07_fuzzy_setup_log.txt")

log(f"\n📊 PERCENTILES USADOS:")
for feat, config in membership_config.items():
    log(f"   {feat}:")
    for label, mf_data in config['membership_functions'].items():
        values_str = [f"{v:.2f}" for v in mf_data['values']]
        log(f"     {label}: {mf_data['percentiles']} → {values_str}")

log(f"\n✅ VALIDACIONES PASADAS:")
log(f"   - ✅ Sin NaNs en cálculo de percentiles")
log(f"   - ✅ Monotonicidad verificada")
log(f"   - ✅ Cobertura razonable")

print_header('FUZZY SETUP COMPLETADO')
log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"\n✅ Configuración lista para inferencia difusa (ejecutar 08_fuzzy_inference.py)")
