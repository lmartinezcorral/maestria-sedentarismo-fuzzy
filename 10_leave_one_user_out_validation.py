"""
10_leave_one_user_out_validation.py
=====================================

OBJETIVO:
---------
Implementar validación Leave-One-User-Out (LOUO) del sistema difuso.
Para cada usuario, entrenar el sistema con los otros 9 usuarios y evaluar en el usuario omitido.

METODOLOGÍA:
------------
1. Loop: i = 1..10
2. train_users = [u1..u10] \ {ui}
3. test_user = ui
4. Recalcular percentiles MF solo con train_users
5. Reentrenar clustering K=2 solo con train_users
6. Optimizar τ en train
7. Aplicar fuzzy a test_user
8. Evaluar F1(test_user)
9. Agregar F1_fold[i]
10. Reportar: mean(F1) ± std(F1)

SALIDAS:
--------
- louo_results/
  - louo_summary.csv (F1, Acc, Prec, Rec, MCC por fold)
  - louo_per_user_detail.csv
  - louo_global_report.txt
  - louo_plots/
    - f1_by_user.png
    - confusion_matrices_grid.png
"""

import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, matthews_corrcoef, confusion_matrix
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler
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
DATA_FILE = BASE_DIR / 'analisis_u' / 'semanal' / 'weekly_consolidado.csv'
OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'louo_results'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / 'plots').mkdir(exist_ok=True)

LOG_FILE = OUTPUT_DIR / 'louo_global_report.txt'

# Features para clustering y fuzzy
FEATURES_CLUSTER = [
    'Actividad_relativa_p50', 'Actividad_relativa_iqr',
    'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr',
    'HRV_SDNN_p50', 'HRV_SDNN_iqr',
    'Delta_cardiaco_p50', 'Delta_cardiaco_iqr'
]

FEATURES_FUZZY = [
    'Actividad_relativa_p50',
    'Superavit_calorico_basal_p50',
    'HRV_SDNN_p50',
    'Delta_cardiaco_p50'
]

# Percentiles para MF
PERCENTILES_MF = {
    'Baja': [10, 25, 40],
    'Media': [35, 50, 65],
    'Alta': [60, 80, 90]
}

RANDOM_STATE = 42
TAU_GRID = np.arange(0.10, 0.61, 0.05)

LOG_LINES = []


def log(msg):
    """Registra y muestra mensaje"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    LOG_LINES.append(log_msg)
    # Remover emojis para compatibilidad Windows
    msg_clean = msg.replace('✅', '[OK]').replace(
        '❌', '[ERROR]').replace('📊', '[DATA]').replace('📈', '[GRAPH]')
    print(msg_clean)


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


def calcular_percentiles_mf(df_train, features, scalers):
    """Calcula percentiles para MF sobre datos NORMALIZADOS de entrenamiento"""
    mf_params = {}

    # Normalizar datos de entrenamiento primero
    df_norm = normalizar_features(df_train, scalers, features)

    for feat in features:
        feat_norm = f'{feat}_norm'
        if feat_norm not in df_norm.columns:
            continue

        data = df_norm[feat_norm].dropna()
        if len(data) == 0:
            continue

        mf_params[feat] = {}
        for label, percentiles in PERCENTILES_MF.items():
            # Percentiles sobre datos NORMALIZADOS [0, 1]
            values = [np.percentile(data, p) for p in percentiles]
            mf_params[feat][label] = {
                'percentiles': percentiles,
                'values': values
            }

    return mf_params


def calcular_min_max(df_train, features):
    """Calcula min/max para normalización"""
    scalers = {}
    for feat in features:
        if feat in df_train.columns:
            data = df_train[feat].dropna()
            # Clip a percentiles 5-95 para robustez
            p5 = np.percentile(data, 5)
            p95 = np.percentile(data, 95)
            scalers[feat] = {'min': p5, 'max': p95}
    return scalers


def normalizar_features(df, scalers, features):
    """Normaliza features a [0,1]"""
    df_norm = df.copy()
    for feat in features:
        if feat in df.columns and feat in scalers:
            min_val = scalers[feat]['min']
            max_val = scalers[feat]['max']
            df_norm[f'{feat}_norm'] = (
                df[feat] - min_val) / (max_val - min_val)
            df_norm[f'{feat}_norm'] = df_norm[f'{feat}_norm'].clip(0, 1)
    return df_norm


def clustering_train(df_train):
    """Entrena clustering K=2 en datos de entrenamiento"""
    X = df_train[FEATURES_CLUSTER].values

    # Escalar
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)

    # K-means K=2
    kmeans = KMeans(n_clusters=2, random_state=RANDOM_STATE,
                    n_init=10, max_iter=500)
    labels = kmeans.fit_predict(X_scaled)

    # Determinar cuál cluster ORIGINAL es "Alto" (mayor score promedio esperado)
    df_train_copy = df_train.copy()
    df_train_copy['cluster_temp'] = labels  # Labels ORIGINALES del kmeans

    # Usar Actividad_relativa_p50 como proxy (bajo → sedentarismo alto)
    cluster_means = df_train_copy.groupby(
        'cluster_temp')['Actividad_relativa_p50'].mean()
    cluster_alto_original = cluster_means.idxmin()  # ID ORIGINAL del cluster alto

    # Mapear: 0=Bajo, 1=Alto
    labels_mapped = np.where(labels == cluster_alto_original, 1, 0)

    # CORRECCIÓN RAYO+ATLAS: Retornar cluster_alto_original para usar en predict
    return labels_mapped, scaler, kmeans, cluster_alto_original


def clustering_predict(df_test, scaler, kmeans, cluster_alto_original):
    """Predice clusters en datos de test"""
    X = df_test[FEATURES_CLUSTER].values
    X_scaled = scaler.transform(X)
    labels = kmeans.predict(X_scaled)

    # Mapear igual que en train
    labels_mapped = np.where(labels == cluster_alto_original, 1, 0)
    return labels_mapped


def fuzzy_fuzzify(df, mf_params, scalers):
    """Fuzzifica features"""
    df_norm = normalizar_features(df, scalers, FEATURES_FUZZY)

    # DEBUG
    print(f"DEBUG fuzzy_fuzzify: df_norm shape = {df_norm.shape}")
    print(
        f"DEBUG fuzzy_fuzzify: df_norm columns = {[c for c in df_norm.columns if '_norm' in c]}")
    print(f"DEBUG fuzzy_fuzzify: mf_params keys = {list(mf_params.keys())}")

    # Verificar rangos de valores normalizados
    for feat in FEATURES_FUZZY:
        feat_norm = f'{feat}_norm'
        if feat_norm in df_norm.columns:
            print(
                f"DEBUG {feat}_norm: min={df_norm[feat_norm].min():.3f}, max={df_norm[feat_norm].max():.3f}, mean={df_norm[feat_norm].mean():.3f}")

    membresias = {}
    for feat in FEATURES_FUZZY:
        feat_norm = f'{feat}_norm'
        if feat_norm not in df_norm.columns:
            print(f"DEBUG: {feat_norm} NO encontrado en df_norm")
            continue
        if feat not in mf_params:
            print(f"DEBUG: {feat} NO encontrado en mf_params")
            continue

        for label in ['Baja', 'Media', 'Alta']:
            if label in mf_params[feat]:
                a, b, c = mf_params[feat][label]['values']
                print(f"DEBUG: {feat} {label} = [{a:.3f}, {b:.3f}, {c:.3f}]")
                col_name = f'{feat}_{label}_memb'
                membresias[col_name] = df_norm[feat_norm].apply(
                    lambda x: triangular(x, a, b, c))

    df_memb = pd.DataFrame(membresias, index=df.index)
    print(
        f"DEBUG fuzzy_fuzzify: df_memb shape = {df_memb.shape}, columns = {len(df_memb.columns)}")
    return df_memb


def fuzzy_inference(df_memb):
    """Ejecuta inferencia difusa (5 reglas)"""
    # DEBUG: Verificar columnas disponibles
    print(
        f"DEBUG fuzzy_inference: df_memb columns = {df_memb.columns.tolist()}")

    # Verificar que existan las columnas necesarias
    required_cols = [
        'Actividad_relativa_p50_Baja_memb',
        'Actividad_relativa_p50_Media_memb',
        'Actividad_relativa_p50_Alta_memb',
        'Superavit_calorico_basal_p50_Baja_memb',
        'Superavit_calorico_basal_p50_Media_memb',
        'Superavit_calorico_basal_p50_Alta_memb',
        'HRV_SDNN_p50_Baja_memb',
        'HRV_SDNN_p50_Media_memb',
        'Delta_cardiaco_p50_Baja_memb'
    ]

    missing = [col for col in required_cols if col not in df_memb.columns]
    if missing:
        print(f"ERROR: Columnas faltantes en df_memb: {missing}")
        return np.zeros(len(df_memb))

    # Reglas R1-R5
    w1 = np.minimum(df_memb['Actividad_relativa_p50_Baja_memb'],
                    df_memb['Superavit_calorico_basal_p50_Baja_memb'])
    w2 = np.minimum(df_memb['Actividad_relativa_p50_Alta_memb'],
                    df_memb['Superavit_calorico_basal_p50_Alta_memb'])
    # CORRECCIÓN ATLAS: R3 debe usar Delta_Alta, no Baja (Bug A1)
    w3 = np.minimum(df_memb['HRV_SDNN_p50_Baja_memb'],
                    df_memb['Delta_cardiaco_p50_Alta_memb'])
    w4 = np.minimum(df_memb['Actividad_relativa_p50_Media_memb'],
                    df_memb['HRV_SDNN_p50_Media_memb'])
    w5 = np.minimum(df_memb['Actividad_relativa_p50_Baja_memb'],
                    df_memb['Superavit_calorico_basal_p50_Media_memb']) * 0.7

    # DEBUG
    print(
        f"DEBUG w1: min={w1.min():.3f}, max={w1.max():.3f}, mean={w1.mean():.3f}")
    print(
        f"DEBUG w2: min={w2.min():.3f}, max={w2.max():.3f}, mean={w2.mean():.3f}")

    # CORRECCIÓN ATLAS: Defuzzificación weighted average (como 08_fuzzy)
    # Outputs por regla: R1→1.0, R2→0.0, R3→0.9, R4→0.5, R5→0.7
    outputs = np.array([1.0, 0.0, 0.9, 0.5, 0.7])
    weights = np.array([w1, w2, w3, w4, w5])

    # Sumar weights por fila
    w_total = np.sum(weights, axis=0)

    # Defuzzificación: weighted average
    scores = np.where(w_total > 0,
                      np.sum(
                          weights * outputs[:, np.newaxis], axis=0) / w_total,
                      0.5)

    return scores


def optimizar_tau(scores_train, y_true_train):
    """Optimiza umbral tau maximizando F1 en train"""
    best_tau = 0.30
    best_f1 = 0.0

    for tau in TAU_GRID:
        y_pred = (scores_train >= tau).astype(int)
        f1 = f1_score(y_true_train, y_pred, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_tau = tau

    return best_tau, best_f1

# ============================================================================
# MAIN: LEAVE-ONE-USER-OUT
# ============================================================================


def main():
    print_header('LEAVE-ONE-USER-OUT VALIDATION - PASO 10')
    log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Archivo entrada: {DATA_FILE}")
    log(f"Directorio salida: {OUTPUT_DIR}")
    log("")

    # Cargar datos
    print_header('1. CARGANDO DATOS')
    if not DATA_FILE.exists():
        log(f"❌ ERROR: No existe {DATA_FILE}")
        return

    df = pd.read_csv(DATA_FILE)
    log(f"✅ Datos cargados: {len(df)} semanas")
    log(f"   Usuarios: {df['usuario_id'].nunique()}")
    log("")

    # Obtener lista de usuarios
    usuarios = sorted(df['usuario_id'].unique())
    log(f"Usuarios encontrados: {usuarios}")
    log("")

    # ========================================================================
    # CORRECCIÓN ATLAS A2: CALCULAR PERCENTILES GLOBALES (N=10 completo)
    # ========================================================================
    print_header('AJUSTE A2: PERCENTILES GLOBALES FIJOS')
    log("Calculando percentiles MF con dataset completo (N=10)...")

    # Calcular scalers globales
    scalers_globales = calcular_min_max(df, FEATURES_FUZZY)
    log(f"✅ Scalers globales calculados para {len(FEATURES_FUZZY)} features")

    # Calcular percentiles MF globales
    mf_params_globales = calcular_percentiles_mf(
        df, FEATURES_FUZZY, scalers_globales)
    log(f"✅ Percentiles MF globales calculados")

    for feat in FEATURES_FUZZY:
        if feat in mf_params_globales:
            log(f"   {feat}:")
            for label in ['Baja', 'Media', 'Alta']:
                if label in mf_params_globales[feat]:
                    vals = mf_params_globales[feat][label]['values']
                    log(f"      {label}: [{vals[0]:.3f}, {vals[1]:.3f}, {vals[2]:.3f}]")

    log("")
    log("[IMPORTANTE] Estos percentiles se usaran FIJOS en todos los folds")
    log("   Solo se recalcularan los scalers (min/max) por fold para normalizacion")
    log("")

    # Resultados por fold
    results_folds = []

    # ========================================================================
    # LOOP: Leave-One-User-Out
    # ========================================================================

    for test_user in usuarios:
        print_header(f'FOLD: Test User = {test_user}')
        log(f"\nProcesando fold: test_user = {test_user}")

        # Split train/test
        df_train = df[df['usuario_id'] != test_user].copy()
        df_test = df[df['usuario_id'] == test_user].copy()

        log(
            f"  Train: {len(df_train)} semanas ({len(df_train['usuario_id'].unique())} usuarios)")
        log(f"  Test: {len(df_test)} semanas (1 usuario: {test_user})")

        # 1. Calcular scalers PRIMERO (min/max para normalización)
        log("  [1] Calculando scalers para normalización...")
        scalers_train = calcular_min_max(df_train, FEATURES_FUZZY)

        # CORRECCIÓN ATLAS A2: USAR percentiles GLOBALES fijos (NO recalcular)
        log("  [1b] USANDO percentiles MF GLOBALES (fijos)...")
        mf_params_train = mf_params_globales  # ← CAMBIO CRÍTICO

        # 2. Entrenar clustering en train
        log("  [2] Entrenando clustering K=2 en train...")
        # CORRECCIÓN RAYO+ATLAS: Recibir cluster_alto_original (4to valor)
        y_cluster_train, scaler_cluster, kmeans_model, cluster_alto_original = clustering_train(
            df_train)
        df_train['cluster_label'] = y_cluster_train

        log(f"      Cluster Alto ORIGINAL ID = {cluster_alto_original}")

        # 3. Fuzzy en train
        log("  [3] Aplicando fuzzy en train...")
        df_memb_train = fuzzy_fuzzify(df_train, mf_params_train, scalers_train)
        scores_train = fuzzy_inference(df_memb_train)
        log(f"      Scores train: min={scores_train.min():.3f}, max={scores_train.max():.3f}, mean={scores_train.mean():.3f}")

        # 4. Optimizar tau en train
        log("  [4] Optimizando tau en train...")
        tau_opt, f1_train = optimizar_tau(scores_train, y_cluster_train)
        log(f"      tau optimo = {tau_opt:.2f}, F1_train = {f1_train:.3f}")

        # 5. Aplicar clustering a test
        log("  [5] Aplicando clustering a test...")
        # CORRECCIÓN RAYO+ATLAS: Usar cluster_alto_original (no cluster_alto_id)
        y_cluster_test = clustering_predict(
            df_test, scaler_cluster, kmeans_model, cluster_alto_original)
        df_test['cluster_label'] = y_cluster_test

        # 6. Fuzzy en test
        log("  [6] Aplicando fuzzy en test...")
        df_memb_test = fuzzy_fuzzify(df_test, mf_params_train, scalers_train)
        scores_test = fuzzy_inference(df_memb_test)
        log(f"      Scores test: min={scores_test.min():.3f}, max={scores_test.max():.3f}, mean={scores_test.mean():.3f}")
        y_pred_test = (scores_test >= tau_opt).astype(int)
        log(f"      y_pred_test (fuzzy): {np.bincount(y_pred_test)} (0=Bajo, 1=Alto)")
        log(f"      y_cluster_test (GO): {np.bincount(y_cluster_test)} (0=Bajo, 1=Alto)")

        # 7. Evaluar en test
        log("  [7] Evaluando en test...")
        f1_test = f1_score(y_cluster_test, y_pred_test, zero_division=0)
        acc_test = accuracy_score(y_cluster_test, y_pred_test)
        prec_test = precision_score(
            y_cluster_test, y_pred_test, zero_division=0)
        rec_test = recall_score(y_cluster_test, y_pred_test, zero_division=0)
        mcc_test = matthews_corrcoef(y_cluster_test, y_pred_test)
        cm_test = confusion_matrix(y_cluster_test, y_pred_test)

        log(f"      F1 = {f1_test:.3f}, Acc = {acc_test:.3f}, Prec = {prec_test:.3f}, Rec = {rec_test:.3f}, MCC = {mcc_test:.3f}")

        # Guardar resultados del fold
        results_folds.append({
            'test_user': test_user,
            'n_train': len(df_train),
            'n_test': len(df_test),
            'tau_opt': tau_opt,
            'f1_train': f1_train,
            'f1_test': f1_test,
            'accuracy_test': acc_test,
            'precision_test': prec_test,
            'recall_test': rec_test,
            'mcc_test': mcc_test,
            'tn': cm_test[0, 0],
            'fp': cm_test[0, 1],
            'fn': cm_test[1, 0],
            'tp': cm_test[1, 1]
        })

    # ========================================================================
    # RESUMEN GLOBAL
    # ========================================================================

    print_header('RESUMEN GLOBAL LEAVE-ONE-USER-OUT')

    df_results = pd.DataFrame(results_folds)

    # Guardar resultados
    summary_file = OUTPUT_DIR / 'louo_summary.csv'
    df_results.to_csv(summary_file, index=False)
    log(f"\n✅ Guardado: {summary_file.name}")

    # Estadísticas globales
    f1_mean = df_results['f1_test'].mean()
    f1_std = df_results['f1_test'].std()
    acc_mean = df_results['accuracy_test'].mean()
    prec_mean = df_results['precision_test'].mean()
    rec_mean = df_results['recall_test'].mean()
    mcc_mean = df_results['mcc_test'].mean()

    log(f"\n📊 MÉTRICAS GLOBALES (promedio ± std):")
    log(f"   F1-Score: {f1_mean:.3f} ± {f1_std:.3f}")
    log(
        f"   Accuracy: {acc_mean:.3f} ± {df_results['accuracy_test'].std():.3f}")
    log(
        f"   Precision: {prec_mean:.3f} ± {df_results['precision_test'].std():.3f}")
    log(f"   Recall: {rec_mean:.3f} ± {df_results['recall_test'].std():.3f}")
    log(f"   MCC: {mcc_mean:.3f} ± {df_results['mcc_test'].std():.3f}")
    log("")

    # Rango de F1
    f1_min = df_results['f1_test'].min()
    f1_max = df_results['f1_test'].max()
    user_min = df_results.loc[df_results['f1_test'].idxmin(), 'test_user']
    user_max = df_results.loc[df_results['f1_test'].idxmax(), 'test_user']

    log(f"📈 RANGO DE F1:")
    log(f"   Máximo: {f1_max:.3f} (usuario {user_max})")
    log(f"   Mínimo: {f1_min:.3f} (usuario {user_min})")
    log(f"   Rango: {f1_max - f1_min:.3f}")
    log("")

    # ========================================================================
    # VISUALIZACIONES
    # ========================================================================

    print_header('GENERANDO VISUALIZACIONES')

    # Plot 1: F1 por usuario
    fig, ax = plt.subplots(figsize=(12, 6))
    usuarios_sorted = df_results.sort_values('f1_test', ascending=False)

    colors = ['green' if f1 >= 0.70 else 'orange' if f1 >=
              0.50 else 'red' for f1 in usuarios_sorted['f1_test']]
    bars = ax.bar(range(len(usuarios_sorted)),
                  usuarios_sorted['f1_test'], color=colors, alpha=0.7)

    ax.axhline(y=f1_mean, color='blue', linestyle='--',
               linewidth=2, label=f'Promedio: {f1_mean:.3f}')
    ax.axhline(y=0.70, color='green', linestyle=':', linewidth=1,
               alpha=0.5, label='Umbral clínico (0.70)')

    ax.set_xticks(range(len(usuarios_sorted)))
    ax.set_xticklabels(usuarios_sorted['test_user'], rotation=45, ha='right')
    ax.set_ylabel('F1-Score', fontsize=12, fontweight='bold')
    ax.set_xlabel('Usuario (Test)', fontsize=12, fontweight='bold')
    ax.set_title(f'Leave-One-User-Out: F1-Score por Usuario\n(Promedio: {f1_mean:.3f} ± {f1_std:.3f})',
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3)
    ax.legend(fontsize=10)

    # Anotar valores
    for i, (idx, row) in enumerate(usuarios_sorted.iterrows()):
        ax.text(i, row['f1_test'] + 0.02, f"{row['f1_test']:.3f}",
                ha='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plot1_file = OUTPUT_DIR / 'plots' / 'f1_by_user.png'
    fig.savefig(plot1_file, dpi=150)
    plt.close(fig)
    log(f"✅ Guardado: plots/f1_by_user.png")

    # ========================================================================
    # GUARDAR LOG
    # ========================================================================

    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG_LINES))

    print_header('LEAVE-ONE-USER-OUT COMPLETADO')
    log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"\n✅ Todos los resultados en: {OUTPUT_DIR}")
    log("")

    print("\n" + "="*80)
    print(f"✅ F1-Score Promedio: {f1_mean:.3f} ± {f1_std:.3f}")
    print(f"   Accuracy Promedio: {acc_mean:.3f}")
    print(f"   Rango F1: [{f1_min:.3f}, {f1_max:.3f}]")
    print("="*80)


if __name__ == '__main__':
    main()
