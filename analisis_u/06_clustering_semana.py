"""
Clustering Semanal - Paso 6
============================

OBJETIVO:
---------
Entrenar clustering sobre semanas con 8 features robustas,
evaluar K∈{2..6}, y generar asignaciones + visualizaciones.

INSUMOS:
--------
- analisis_u/semanal/cluster_inputs_weekly.csv

SALIDAS:
--------
- clustering/06_clustering_log.txt
- clustering/model_selection_metrics.csv
- clustering/cluster_assignments.csv
- clustering/cluster_centroids.csv
- clustering/cluster_profiles.csv
- cluster_viz/pca_scatter.png
- cluster_viz/umap_scatter.png (opcional)

Autor: Pipeline automatizado
Fecha: 2025-10-16
"""

import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import warnings
from datetime import datetime

# ML imports
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score
from sklearn.decomposition import PCA
from sklearn.utils import resample

# Plots
import matplotlib
matplotlib.use('Agg')

warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

BASE_DIR = Path(__file__).parent.resolve()  # analisis_u/
INPUT_FILE = BASE_DIR / 'semanal' / 'cluster_inputs_weekly.csv'
OUTPUT_DIR = BASE_DIR / 'clustering'
VIZ_DIR = BASE_DIR / 'cluster_viz'

# Crear directorios
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VIZ_DIR.mkdir(parents=True, exist_ok=True)

# Features para clustering
FEATURE_COLS = [
    'Actividad_relativa_p50', 'Actividad_relativa_iqr',
    'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr',
    'HRV_SDNN_p50', 'HRV_SDNN_iqr',
    'Delta_cardiaco_p50', 'Delta_cardiaco_iqr'
]

# Rango de K
K_RANGE = [2, 3, 4, 5, 6]

# Filtros de calidad
MIN_DIAS = 3
MAX_PCT_IMPUTADA = 60

# Bootstrap para estabilidad
N_BOOTSTRAP = 20
BOOTSTRAP_FRAC = 0.8

LOG_LINES = []

# ==============================================================================
# FUNCIONES
# ==============================================================================


def log(msg):
    """Registra y muestra mensaje"""
    LOG_LINES.append(msg)
    print(msg)


def filter_quality(df):
    """
    Filtra semanas por calidad mínima.

    Returns:
        DataFrame filtrado
    """
    n_original = len(df)

    # Filtro 1: días monitoreados
    df = df[df['dias_monitoreados'] >= MIN_DIAS].copy()
    n_after_dias = len(df)

    # Filtro 2: % imputada (si existe y no es NaN)
    if 'pct_imputada_FC_walk' in df.columns:
        # Solo filtrar donde tenemos datos
        mask_has_pct = df['pct_imputada_FC_walk'].notna()
        mask_quality = (df['pct_imputada_FC_walk'] <=
                        MAX_PCT_IMPUTADA) | (~mask_has_pct)
        df = df[mask_quality].copy()

    n_after_imput = len(df)

    log(f"  Filtrado de calidad:")
    log(f"    - Original: {n_original} semanas")
    log(f"    - Tras filtro dias≥{MIN_DIAS}: {n_after_dias} ({n_original-n_after_dias} eliminadas)")
    log(f"    - Tras filtro pct_imputada≤{MAX_PCT_IMPUTADA}%: {n_after_imput} ({n_after_dias-n_after_imput} eliminadas)")

    return df


def compute_stability(X, k, n_iter=N_BOOTSTRAP, frac=BOOTSTRAP_FRAC):
    """
    Calcula estabilidad del clustering mediante bootstrap.

    Returns:
        ARI promedio entre remuestreos
    """
    n_samples = len(X)
    aris = []

    # Clustering de referencia
    kmeans_ref = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_ref = kmeans_ref.fit_predict(X)

    for i in range(n_iter):
        # Resample
        idx_boot = resample(range(n_samples), n_samples=int(
            n_samples*frac), random_state=i)
        X_boot = X[idx_boot]

        # Clustering en bootstrap
        kmeans_boot = KMeans(n_clusters=k, random_state=i, n_init=10)
        labels_boot = kmeans_boot.fit_predict(X_boot)

        # ARI entre ref (subset) y boot
        labels_ref_subset = labels_ref[idx_boot]
        ari = adjusted_rand_score(labels_ref_subset, labels_boot)
        aris.append(ari)

    return np.mean(aris)


def evaluate_k(X, k):
    """
    Evalúa clustering para un K específico.

    Returns:
        dict con métricas
    """
    log(f"\n  Evaluando K={k}...")

    # KMeans
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    # Métricas
    sil = silhouette_score(X, labels)
    db = davies_bouldin_score(X, labels)

    # Estabilidad
    log(f"    - Calculando estabilidad ({N_BOOTSTRAP} bootstraps)...")
    stability = compute_stability(X, k)

    # Tamaños de clusters
    unique, counts = np.unique(labels, return_counts=True)
    sizes = dict(zip(unique, counts))

    log(f"    - Silhouette: {sil:.3f}")
    log(f"    - Davies-Bouldin: {db:.3f}")
    log(f"    - Estabilidad (ARI promedio): {stability:.3f}")
    log(f"    - Tamaños: {sizes}")

    return {
        'k': k,
        'silhouette': sil,
        'davies_bouldin': db,
        'stability_ari': stability,
        'sizes': str(sizes),
        'model': kmeans,
        'labels': labels
    }


def select_best_k(metrics_list):
    """
    Selecciona K óptimo con penalizaciones.

    Criterio: max silhouette con penalización por K alto y baja estabilidad.
    """
    df_metrics = pd.DataFrame([
        {k: v for k, v in m.items() if k not in ['model', 'labels']}
        for m in metrics_list
    ])

    # Score compuesto
    # Normalizar silhouette (0-1)
    sil_norm = (df_metrics['silhouette'] - df_metrics['silhouette'].min()) / \
               (df_metrics['silhouette'].max() -
                df_metrics['silhouette'].min())

    # Penalización por K (preferir menor K)
    k_penalty = (df_metrics['k'] - df_metrics['k'].min()) / \
                (df_metrics['k'].max() - df_metrics['k'].min())

    # Penalización por baja estabilidad
    stab_penalty = np.where(df_metrics['stability_ari'] < 0.70, 0.2, 0.0)

    # Score final
    score = sil_norm - 0.1*k_penalty - stab_penalty

    best_idx = score.argmax()
    best_k = df_metrics.loc[best_idx, 'k']

    log(f"\n  📊 Selección de K óptimo:")
    log(f"     K elegido: {best_k}")
    log(f"     Silhouette: {df_metrics.loc[best_idx, 'silhouette']:.3f}")
    log(f"     Estabilidad: {df_metrics.loc[best_idx, 'stability_ari']:.3f}")

    return int(best_k), best_idx


def create_cluster_profiles(df_original, labels, centroids_scaled, scaler):
    """
    Crea perfiles de cluster en espacio original.

    Returns:
        DataFrame con medianas e IQR por cluster
    """
    df_temp = df_original.copy()
    df_temp['cluster'] = labels

    profiles = []

    for cluster_id in sorted(df_temp['cluster'].unique()):
        subset = df_temp[df_temp['cluster'] == cluster_id]
        n_weeks = len(subset)
        n_users = subset['usuario_id'].nunique()

        profile = {
            'cluster': cluster_id,
            'n_weeks': n_weeks,
            'n_users': n_users
        }

        # Medianas e IQR por feature
        for feat in FEATURE_COLS:
            if feat in subset.columns:
                profile[f'{feat}_median'] = subset[feat].median()
                profile[f'{feat}_q25'] = subset[feat].quantile(0.25)
                profile[f'{feat}_q75'] = subset[feat].quantile(0.75)
                profile[f'{feat}_iqr'] = profile[f'{feat}_q75'] - \
                    profile[f'{feat}_q25']

        profiles.append(profile)

    return pd.DataFrame(profiles)


def plot_pca_clusters(X_scaled, labels, df_meta, k):
    """
    Proyección PCA 2D de clusters.
    """
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots(figsize=(12, 8))

    scatter = ax.scatter(
        X_pca[:, 0], X_pca[:, 1],
        c=labels, cmap='tab10', alpha=0.6, s=50, edgecolors='k', linewidth=0.3
    )

    ax.set_xlabel(
        f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
    ax.set_ylabel(
        f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
    ax.set_title(
        f'Clustering semanal (K={k}) - Proyección PCA', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)

    # Legend
    handles, _ = scatter.legend_elements()
    legend_labels = [f'Cluster {i}' for i in range(k)]
    ax.legend(handles, legend_labels, title='Cluster', loc='best')

    plt.tight_layout()
    path = VIZ_DIR / 'pca_scatter.png'
    fig.savefig(path, dpi=150)
    plt.close(fig)

    log(f"  ✅ Gráfico PCA guardado: {path.name}")


def plot_umap_clusters(X_scaled, labels, k):
    """
    Proyección UMAP 2D (opcional, si umap-learn disponible).
    """
    try:
        import umap

        reducer = umap.UMAP(n_components=2, random_state=42,
                            n_neighbors=15, min_dist=0.1)
        X_umap = reducer.fit_transform(X_scaled)

        fig, ax = plt.subplots(figsize=(12, 8))

        scatter = ax.scatter(
            X_umap[:, 0], X_umap[:, 1],
            c=labels, cmap='tab10', alpha=0.6, s=50, edgecolors='k', linewidth=0.3
        )

        ax.set_xlabel('UMAP 1', fontsize=12)
        ax.set_ylabel('UMAP 2', fontsize=12)
        ax.set_title(
            f'Clustering semanal (K={k}) - Proyección UMAP', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)

        handles, _ = scatter.legend_elements()
        legend_labels = [f'Cluster {i}' for i in range(k)]
        ax.legend(handles, legend_labels, title='Cluster', loc='best')

        plt.tight_layout()
        path = VIZ_DIR / 'umap_scatter.png'
        fig.savefig(path, dpi=150)
        plt.close(fig)

        log(f"  ✅ Gráfico UMAP guardado: {path.name}")

    except ImportError:
        log(f"  ⚠️  umap-learn no disponible, se omite gráfico UMAP")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    log("="*80)
    log("CLUSTERING SEMANAL - PASO 6")
    log("="*80)
    log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Archivo entrada: {INPUT_FILE}")
    log("")

    # =========================================================================
    # CARGA Y FILTRADO
    # =========================================================================
    log("📂 Cargando datos...")

    if not INPUT_FILE.exists():
        log(f"❌ ERROR: No se encontró {INPUT_FILE}")
        return 1

    df = pd.read_csv(INPUT_FILE)
    log(f"✅ Datos cargados: {len(df)} semanas")
    log(f"   Columnas: {list(df.columns)}")

    # Verificar features
    missing_feats = [f for f in FEATURE_COLS if f not in df.columns]
    if missing_feats:
        log(f"❌ ERROR: Features faltantes: {missing_feats}")
        return 1

    log(f"✅ Las 8 features están presentes")

    # Filtrado de calidad
    log(f"\n🔍 Aplicando filtros de calidad...")
    df_filt = filter_quality(df)

    if len(df_filt) < 100:
        log(f"❌ ERROR: Muy pocas semanas tras filtrado ({len(df_filt)})")
        return 1

    log(f"✅ Semanas válidas para clustering: {len(df_filt)}")

    # Resumen por usuario
    user_counts = df_filt['usuario_id'].value_counts().sort_index()
    log(f"\n  Semanas por usuario tras filtrado:")
    for u_id, count in user_counts.items():
        log(f"    {u_id}: {count} semanas")

    # =========================================================================
    # PREPARACIÓN DE FEATURES
    # =========================================================================
    log(f"\n🔧 Preparando features...")

    X = df_filt[FEATURE_COLS].values

    # Verificar NaNs
    n_nans = np.isnan(X).sum()
    if n_nans > 0:
        log(f"  ⚠️  Se encontraron {n_nans} NaNs en features, rellenando con mediana...")
        from sklearn.impute import SimpleImputer
        imputer = SimpleImputer(strategy='median')
        X = imputer.fit_transform(X)

    # Escalado robusto
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)

    log(f"✅ Features escaladas con RobustScaler")
    log(f"   Shape: {X_scaled.shape}")

    # =========================================================================
    # BÚSQUEDA DE K
    # =========================================================================
    log(f"\n{'='*80}")
    log(f"BÚSQUEDA DE K ÓPTIMO")
    log(f"{'='*80}")

    metrics_list = []

    for k in K_RANGE:
        result = evaluate_k(X_scaled, k)
        metrics_list.append(result)

    # Selección de K
    best_k, best_idx = select_best_k(metrics_list)
    best_model = metrics_list[best_idx]['model']
    best_labels = metrics_list[best_idx]['labels']

    # Guardar métricas
    df_metrics = pd.DataFrame([
        {k: v for k, v in m.items() if k not in ['model', 'labels']}
        for m in metrics_list
    ])
    metrics_path = OUTPUT_DIR / 'model_selection_metrics.csv'
    df_metrics.to_csv(metrics_path, index=False)
    log(f"\n✅ Métricas guardadas: {metrics_path.name}")

    # =========================================================================
    # ASIGNACIONES Y CENTROIDES
    # =========================================================================
    log(f"\n{'='*80}")
    log(f"GUARDANDO RESULTADOS (K={best_k})")
    log(f"{'='*80}")

    # Asignaciones
    df_assignments = df_filt[['usuario_id',
                              'usuario_alias', 'semana_inicio']].copy()
    df_assignments['cluster'] = best_labels

    # Añadir features escaladas
    for i, feat in enumerate(FEATURE_COLS):
        df_assignments[f'{feat}_scaled'] = X_scaled[:, i]

    assign_path = OUTPUT_DIR / 'cluster_assignments.csv'
    df_assignments.to_csv(assign_path, index=False)
    log(f"✅ Asignaciones guardadas: {assign_path.name}")
    log(f"   {len(df_assignments)} semanas asignadas")

    # Centroides
    centroids_scaled = best_model.cluster_centers_
    centroids_original = scaler.inverse_transform(centroids_scaled)

    df_centroids = pd.DataFrame(centroids_scaled, columns=[
                                f'{f}_scaled' for f in FEATURE_COLS])
    for i, feat in enumerate(FEATURE_COLS):
        df_centroids[f'{feat}_original'] = centroids_original[:, i]
    df_centroids.insert(0, 'cluster', range(best_k))

    centroids_path = OUTPUT_DIR / 'cluster_centroids.csv'
    df_centroids.to_csv(centroids_path, index=False)
    log(f"✅ Centroides guardados: {centroids_path.name}")

    # Perfiles clínicos
    df_profiles = create_cluster_profiles(
        df_filt, best_labels, centroids_scaled, scaler)
    profiles_path = OUTPUT_DIR / 'cluster_profiles.csv'
    df_profiles.to_csv(profiles_path, index=False)
    log(f"✅ Perfiles clínicos guardados: {profiles_path.name}")

    # =========================================================================
    # VISUALIZACIONES
    # =========================================================================
    log(f"\n{'='*80}")
    log(f"GENERANDO VISUALIZACIONES")
    log(f"{'='*80}")

    plot_pca_clusters(X_scaled, best_labels, df_filt, best_k)
    plot_umap_clusters(X_scaled, best_labels, best_k)

    # =========================================================================
    # INTERPRETACIÓN CLÍNICA
    # =========================================================================
    log(f"\n{'='*80}")
    log(f"INSIGHTS CLÍNICOS")
    log(f"{'='*80}")

    for idx, row in df_profiles.iterrows():
        cluster_id = int(row['cluster'])
        n_weeks = int(row['n_weeks'])
        n_users = int(row['n_users'])

        log(f"\nCluster {cluster_id} ({n_weeks} semanas, {n_users} usuarios):")

        # Actividad
        act_med = row.get('Actividad_relativa_p50_median', np.nan)
        if not np.isnan(act_med):
            log(f"  - Actividad relativa: {act_med:.3f} (mediana)")

        # HRV
        hrv_med = row.get('HRV_SDNN_p50_median', np.nan)
        if not np.isnan(hrv_med):
            log(f"  - HRV SDNN: {hrv_med:.1f} ms (mediana)")

        # Superávit calórico
        sup_med = row.get('Superavit_calorico_basal_p50_median', np.nan)
        if not np.isnan(sup_med):
            log(f"  - Superávit calórico: {sup_med:.1f}% TMB (mediana)")

    # =========================================================================
    # FINALIZACIÓN
    # =========================================================================
    log(f"\n{'='*80}")
    log(f"CLUSTERING COMPLETADO")
    log(f"{'='*80}")
    log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("")
    log(f"📂 Salidas generadas:")
    log(f"   - model_selection_metrics.csv ({len(K_RANGE)} filas)")
    log(f"   - cluster_assignments.csv ({len(df_assignments)} semanas)")
    log(f"   - cluster_centroids.csv ({best_k} centroides)")
    log(f"   - cluster_profiles.csv ({best_k} perfiles)")
    log(f"   - Visualizaciones PCA/UMAP en cluster_viz/")
    log("")

    # Guardar log
    log_path = OUTPUT_DIR / "06_clustering_log.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG_LINES))

    print(f"\n✅ Log guardado en: {log_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
