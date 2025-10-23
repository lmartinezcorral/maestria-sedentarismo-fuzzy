"""
11_analisis_sensibilidad.py
============================

OBJETIVO:
---------
Analizar la robustez del sistema difuso variando:
1. Umbral τ (±0.05 alrededor del óptimo τ=0.30)
2. Percentiles de MF (±5% para cada percentil)

SALIDAS:
--------
- sensibilidad/
  - sensibilidad_tau.csv (F1, Acc, etc. por cada τ)
  - sensibilidad_mf_percentiles.csv
  - plots/
    - sensitivity_tau_curve.png
    - sensitivity_mf_heatmap.png
"""

import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, matthews_corrcoef
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import yaml
import warnings
warnings.filterwarnings('ignore')


matplotlib.use('Agg')

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_DIR = Path(__file__).parent.resolve()
FUZZY_OUTPUT = BASE_DIR / 'analisis_u' / 'fuzzy' / 'fuzzy_output.csv'
CLUSTER_ASSIGNMENTS = BASE_DIR / 'analisis_u' / \
    'clustering' / 'cluster_assignments.csv'
MF_CONFIG_FILE = BASE_DIR / 'fuzzy_config' / 'fuzzy_membership_config.yaml'
SCALERS_FILE = BASE_DIR / 'fuzzy_config' / 'feature_scalers.json'
WEEKLY_DATA = BASE_DIR / 'analisis_u' / 'semanal' / 'weekly_consolidado.csv'

OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'sensibilidad'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / 'plots').mkdir(exist_ok=True)

LOG_FILE = OUTPUT_DIR / '11_sensibilidad_log.txt'

# Parámetros de sensibilidad
TAU_BASE = 0.30
TAU_RANGE = np.arange(0.20, 0.41, 0.01)  # τ ∈ [0.20, 0.40] step 0.01

PERCENTILES_SHIFTS = [-5, -3, 0, 3, 5]  # Shifts en %

FEATURES_FUZZY = [
    'Actividad_relativa_p50',
    'Superavit_calorico_basal_p50',
    'HRV_SDNN_p50',
    'Delta_cardiaco_p50'
]

LOG_LINES = []


def log(msg):
    """Registra y muestra mensaje"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    LOG_LINES.append(log_msg)
    print(msg)


def print_header(title):
    """Imprime encabezado visual"""
    print('\n' + '='*80)
    print(title)
    print('='*80)
    log(f"\n{'='*80}\n{title}\n{'='*80}")

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================


def triangular(x, a, b, c):
    """Función de membresía triangular"""
    if x <= a or x >= c:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a) if (b - a) > 0 else 0.0
    else:
        return (c - x) / (c - b) if (c - b) > 0 else 0.0


def fuzzy_inference_with_mf(df, mf_params, scalers):
    """Ejecuta inferencia difusa completa con parámetros MF dados"""
    # Normalizar features
    df_norm = df.copy()
    for feat in FEATURES_FUZZY:
        if feat in df.columns and feat in scalers:
            min_val = scalers[feat]['min']
            max_val = scalers[feat]['max']
            df_norm[f'{feat}_norm'] = (
                df[feat] - min_val) / (max_val - min_val)
            df_norm[f'{feat}_norm'] = df_norm[f'{feat}_norm'].clip(0, 1)

    # Fuzzificar
    membresias = {}
    for feat in FEATURES_FUZZY:
        feat_norm = f'{feat}_norm'
        if feat_norm not in df_norm.columns or feat not in mf_params:
            continue

        for label in ['Baja', 'Media', 'Alta']:
            if label in mf_params[feat]:
                a, b, c = mf_params[feat][label]['values']
                col_name = f'{feat}_{label}_memb'
                membresias[col_name] = df_norm[feat_norm].apply(
                    lambda x: triangular(x, a, b, c))

    df_memb = pd.DataFrame(membresias, index=df.index)

    # Activación de reglas (R1-R5)
    w1 = np.minimum(df_memb['Actividad_relativa_p50_Baja_memb'],
                    df_memb['Superavit_calorico_basal_p50_Baja_memb'])
    w2 = np.minimum(df_memb['Actividad_relativa_p50_Alta_memb'],
                    df_memb['Superavit_calorico_basal_p50_Alta_memb'])
    w3 = np.minimum(df_memb['HRV_SDNN_p50_Baja_memb'],
                    df_memb['Delta_cardiaco_p50_Baja_memb'])
    w4 = np.minimum(df_memb['Actividad_relativa_p50_Media_memb'],
                    df_memb['HRV_SDNN_p50_Media_memb'])
    w5 = np.minimum(df_memb['Actividad_relativa_p50_Baja_memb'],
                    df_memb['Superavit_calorico_basal_p50_Media_memb']) * 0.7

    # Agregación
    s_bajo = w2
    s_medio = w4
    s_alto = w1 + w3 + w5

    # Defuzzificación
    s_total = s_bajo + s_medio + s_alto
    scores = np.where(s_total > 0, (0.2 * s_bajo + 0.5 *
                      s_medio + 0.8 * s_alto) / s_total, 0.0)

    return scores


def shift_percentiles(mf_params, shift_pct):
    """Aplica shift porcentual a todos los percentiles"""
    mf_shifted = {}
    for feat, feat_dict in mf_params.items():
        mf_shifted[feat] = {}
        # Si tiene 'membership_functions', extraerlo
        if 'membership_functions' in feat_dict:
            labels_dict = feat_dict['membership_functions']
        else:
            labels_dict = feat_dict

        for label, params in labels_dict.items():
            if isinstance(params, dict) and 'values' in params:
                values_orig = params['values']
                # Shift multiplicativo (no aditivo, para mantener orden)
                values_new = [v * (1 + shift_pct / 100.0) for v in values_orig]
                mf_shifted[feat][label] = {
                    'percentiles': params['percentiles'],
                    'values': values_new
                }
    return mf_shifted

# ============================================================================
# MAIN
# ============================================================================


def main():
    print_header('ANÁLISIS DE SENSIBILIDAD - PASO 11')
    log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Directorio salida: {OUTPUT_DIR}")
    log("")

    # Cargar datos
    print_header('1. CARGANDO DATOS')

    if not FUZZY_OUTPUT.exists():
        log(f"❌ ERROR: No existe {FUZZY_OUTPUT}")
        return

    df_fuzzy = pd.read_csv(FUZZY_OUTPUT)
    df_clusters = pd.read_csv(CLUSTER_ASSIGNMENTS)
    df_weekly = pd.read_csv(WEEKLY_DATA)

    # Merge
    df = df_fuzzy.merge(df_clusters[['usuario_id', 'semana_inicio', 'cluster']], on=[
                        'usuario_id', 'semana_inicio'], how='inner')

    log(f"✅ Datos cargados: {len(df)} semanas")
    log("")

    # Cargar configuración MF base
    with open(MF_CONFIG_FILE, 'r') as f:
        mf_config_base = yaml.safe_load(f)

    with open(SCALERS_FILE, 'r') as f:
        scalers = json.load(f)

    # ========================================================================
    # PARTE 1: SENSIBILIDAD DE τ
    # ========================================================================

    print_header('2. SENSIBILIDAD DE τ (UMBRAL)')

    log(f"Evaluando τ en rango [{TAU_RANGE.min():.2f}, {TAU_RANGE.max():.2f}] (step 0.01)")
    log("")

    # Usar scores ya calculados en fuzzy_output
    scores = df['Sedentarismo_score'].values
    y_true = df['cluster'].values

    results_tau = []

    for tau in TAU_RANGE:
        y_pred = (scores >= tau).astype(int)

        f1 = f1_score(y_true, y_pred, zero_division=0)
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        mcc = matthews_corrcoef(y_true, y_pred)

        results_tau.append({
            'tau': tau,
            'f1': f1,
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'mcc': mcc,
            'delta_f1_vs_base': f1 - f1_score(y_true, (scores >= TAU_BASE).astype(int), zero_division=0)
        })

    df_tau = pd.DataFrame(results_tau)

    # Guardar
    tau_file = OUTPUT_DIR / 'sensibilidad_tau.csv'
    df_tau.to_csv(tau_file, index=False)
    log(f"✅ Guardado: {tau_file.name}")

    # Estadísticas
    tau_optimal = df_tau.loc[df_tau['f1'].idxmax(), 'tau']
    f1_max = df_tau['f1'].max()

    # Buscar F1 en τ más cercano a base
    idx_base = (np.abs(df_tau['tau'] - TAU_BASE)).argmin()
    f1_at_base = df_tau.iloc[idx_base]['f1']
    tau_actual_base = df_tau.iloc[idx_base]['tau']

    log(f"\n📊 Estadísticas de τ:")
    log(f"   τ óptimo (F1 máximo): {tau_optimal:.2f} (F1={f1_max:.3f})")
    log(f"   τ base (0.30): F1={f1_at_base:.3f}")
    log(f"   Diferencia: ΔF1 = {f1_max - f1_at_base:.3f}")
    log("")

    # Rango estable (F1 dentro de ±0.05 del máximo)
    tau_stable = df_tau[df_tau['f1'] >= f1_max - 0.05]
    log(
        f"   Rango estable (F1 ≥ {f1_max - 0.05:.3f}): τ ∈ [{tau_stable['tau'].min():.2f}, {tau_stable['tau'].max():.2f}]")
    log(f"   Amplitud: {tau_stable['tau'].max() - tau_stable['tau'].min():.2f}")
    log("")

    # ========================================================================
    # PARTE 2: SENSIBILIDAD DE MF PERCENTILES
    # ========================================================================

    print_header('3. SENSIBILIDAD DE MF PERCENTILES')

    log(f"Evaluando shifts: {PERCENTILES_SHIFTS} %")
    log("")

    results_mf = []

    for shift in PERCENTILES_SHIFTS:
        log(f"  Procesando shift = {shift:+d}%...")

        # Aplicar shift
        mf_shifted = shift_percentiles(mf_config_base, shift)

        # Recalcular scores con MF modificadas
        scores_shifted = fuzzy_inference_with_mf(
            df_weekly, mf_shifted, scalers)

        # Evaluar con τ base
        y_pred_shifted = (scores_shifted >= TAU_BASE).astype(int)

        # Merge con clusters
        df_eval = pd.DataFrame({
            'usuario_id': df_weekly['usuario_id'],
            'semana_inicio': df_weekly['semana_inicio'],
            'score_shifted': scores_shifted,
            'y_pred_shifted': y_pred_shifted
        })

        df_eval = df_eval.merge(df_clusters[['usuario_id', 'semana_inicio', 'cluster']],
                                on=['usuario_id', 'semana_inicio'], how='inner')

        f1 = f1_score(df_eval['cluster'],
                      df_eval['y_pred_shifted'], zero_division=0)
        acc = accuracy_score(df_eval['cluster'], df_eval['y_pred_shifted'])
        prec = precision_score(
            df_eval['cluster'], df_eval['y_pred_shifted'], zero_division=0)
        rec = recall_score(df_eval['cluster'],
                           df_eval['y_pred_shifted'], zero_division=0)
        mcc = matthews_corrcoef(df_eval['cluster'], df_eval['y_pred_shifted'])

        # Calcular diferencia con base (shift=0)
        if shift == 0:
            f1_base_mf = f1

        results_mf.append({
            'shift_pct': shift,
            'f1': f1,
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'mcc': mcc
        })

    df_mf = pd.DataFrame(results_mf)

    # Calcular delta respecto a base
    df_mf['delta_f1_vs_base'] = df_mf['f1'] - \
        df_mf.loc[df_mf['shift_pct'] == 0, 'f1'].values[0]

    # Guardar
    mf_file = OUTPUT_DIR / 'sensibilidad_mf_percentiles.csv'
    df_mf.to_csv(mf_file, index=False)
    log(f"✅ Guardado: {mf_file.name}")

    # Estadísticas
    f1_base_mf = df_mf.loc[df_mf['shift_pct'] == 0, 'f1'].values[0]
    delta_max = df_mf['delta_f1_vs_base'].abs().max()

    log(f"\n📊 Estadísticas de MF:")
    log(f"   F1 base (shift=0%): {f1_base_mf:.3f}")
    log(f"   ΔF1 máximo: {delta_max:.3f}")
    log("")

    for idx, row in df_mf.iterrows():
        log(f"   Shift {row['shift_pct']:+d}%: F1={row['f1']:.3f}, ΔF1={row['delta_f1_vs_base']:+.3f}")
    log("")

    # ========================================================================
    # VISUALIZACIONES
    # ========================================================================

    print_header('4. GENERANDO VISUALIZACIONES')

    # Plot 1: Curva de sensibilidad de τ
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: F1 vs τ
    ax = axes[0]
    ax.plot(df_tau['tau'], df_tau['f1'], 'o-', linewidth=2,
            markersize=5, color='steelblue', label='F1-Score')
    ax.axvline(x=TAU_BASE, color='red', linestyle='--',
               linewidth=2, label=f'τ base ({TAU_BASE:.2f})')
    ax.axvline(x=tau_optimal, color='green', linestyle='--',
               linewidth=2, label=f'τ óptimo ({tau_optimal:.2f})')
    ax.axhspan(f1_max - 0.05, f1_max, color='green',
               alpha=0.1, label='Rango estable (ΔF1 < 0.05)')

    ax.set_xlabel('Umbral τ', fontsize=12, fontweight='bold')
    ax.set_ylabel('F1-Score', fontsize=12, fontweight='bold')
    ax.set_title('Sensibilidad del Umbral τ',
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10)

    # Subplot 2: Todas las métricas
    ax = axes[1]
    ax.plot(df_tau['tau'], df_tau['f1'], 'o-',
            linewidth=2, label='F1', color='blue')
    ax.plot(df_tau['tau'], df_tau['accuracy'], 's-',
            linewidth=2, label='Accuracy', color='green')
    ax.plot(df_tau['tau'], df_tau['precision'], '^-',
            linewidth=2, label='Precision', color='orange')
    ax.plot(df_tau['tau'], df_tau['recall'], 'v-',
            linewidth=2, label='Recall', color='red')
    ax.axvline(x=TAU_BASE, color='black',
               linestyle='--', linewidth=1, alpha=0.5)

    ax.set_xlabel('Umbral τ', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valor de Métrica', fontsize=12, fontweight='bold')
    ax.set_title('Múltiples Métricas vs τ',
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plot1_file = OUTPUT_DIR / 'plots' / 'sensitivity_tau_curve.png'
    fig.savefig(plot1_file, dpi=150)
    plt.close(fig)
    log(f"✅ Guardado: plots/sensitivity_tau_curve.png")

    # Plot 2: Sensibilidad de MF
    fig, ax = plt.subplots(figsize=(10, 6))

    x_pos = np.arange(len(df_mf))
    colors = ['red' if shift < 0 else 'green' if shift >
              0 else 'gray' for shift in df_mf['shift_pct']]

    bars = ax.bar(x_pos, df_mf['f1'], color=colors,
                  alpha=0.7, edgecolor='black')
    ax.axhline(y=f1_base_mf, color='blue', linestyle='--',
               linewidth=2, label=f'Base (shift=0%): F1={f1_base_mf:.3f}')
    ax.axhline(y=f1_base_mf - 0.05, color='orange', linestyle=':',
               linewidth=1, alpha=0.5, label='Tolerancia ΔF1 < 0.05')
    ax.axhline(y=f1_base_mf + 0.05, color='orange',
               linestyle=':', linewidth=1, alpha=0.5)

    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"{s:+d}%" for s in df_mf['shift_pct']], fontsize=11)
    ax.set_xlabel('Shift de Percentiles (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('F1-Score', fontsize=12, fontweight='bold')
    ax.set_title('Sensibilidad de Parámetros MF (Shift de Percentiles)',
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3)
    ax.legend(fontsize=10)

    # Anotar valores
    for i, (idx, row) in enumerate(df_mf.iterrows()):
        ax.text(i, row['f1'] + 0.01, f"{row['f1']:.3f}\n(Δ{row['delta_f1_vs_base']:+.3f})",
                ha='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plot2_file = OUTPUT_DIR / 'plots' / 'sensitivity_mf_shifts.png'
    fig.savefig(plot2_file, dpi=150)
    plt.close(fig)
    log(f"✅ Guardado: plots/sensitivity_mf_shifts.png")

    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================

    print_header('5. RESUMEN EJECUTIVO')

    log(f"\n📊 ROBUSTEZ DEL SISTEMA:")
    log(f"\n1. SENSIBILIDAD DE τ:")
    log(f"   - Rango estable: τ ∈ [{tau_stable['tau'].min():.2f}, {tau_stable['tau'].max():.2f}]")
    log(
        f"   - ΔF1 máximo en rango estable: {(f1_max - tau_stable['f1'].min()):.3f}")
    log(
        f"   - Conclusión: {'ROBUSTO' if (f1_max - tau_stable['f1'].min()) < 0.05 else 'MODERADO'}")
    log("")

    log(f"2. SENSIBILIDAD DE MF:")
    log(f"   - ΔF1 máximo (shift ±5%): {delta_max:.3f}")
    log(f"   - Conclusión: {'ROBUSTO' if delta_max < 0.10 else 'MODERADO' if delta_max < 0.15 else 'SENSIBLE'}")
    log("")

    # Guardar log
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG_LINES))

    print_header('ANÁLISIS DE SENSIBILIDAD COMPLETADO')
    log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"\n✅ Todos los resultados en: {OUTPUT_DIR}")
    log("")


if __name__ == '__main__':
    main()
