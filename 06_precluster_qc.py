"""
06_precluster_qc.py
Análisis Pre-Clustering: Correlaciones, VIF, Escalado, PCA, K-Sweep
Complementario al clustering ya ejecutado (06_clustering_semana.py)
"""

from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LinearRegression
import warnings
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
warnings.filterwarnings('ignore')

# Configuración de rutas
BASE_DIR = Path(__file__).parent.resolve()
INPUT_FILE = BASE_DIR / 'analisis_u' / 'semanal' / 'cluster_inputs_weekly.csv'
OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'semanal' / 'precluster'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / '06_precluster_qc_log.txt'

# Features para clustering (8)
FEATURES = [
    'Actividad_relativa_p50', 'Actividad_relativa_iqr',
    'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr',
    'HRV_SDNN_p50', 'HRV_SDNN_iqr',
    'Delta_cardiaco_p50', 'Delta_cardiaco_iqr'
]

# Configuración de clustering exploratorio
K_RANGE = range(2, 7)  # K=2..6
RANDOM_STATE = 42


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
print_header('ANÁLISIS PRE-CLUSTERING (QC) - PASO 6 COMPLEMENTARIO')
log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Archivo entrada: {INPUT_FILE}")
log(f"Directorio salida: {OUTPUT_DIR}")

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================
print_header('1. CARGANDO DATOS')

if not INPUT_FILE.exists():
    log(f"❌ ERROR: No existe {INPUT_FILE}")
    sys.exit(1)

df = pd.read_csv(INPUT_FILE)
log(f"✅ Datos cargados: {len(df)} semanas")
log(f"   Columnas: {list(df.columns)}")

# Verificar que existen las 8 features
missing_features = [f for f in FEATURES if f not in df.columns]
if missing_features:
    log(f"❌ ERROR: Faltan features: {missing_features}")
    sys.exit(1)
log(f"✅ Las 8 features están presentes")

# ============================================================================
# 2. LIMPIEZA Y FILTRADO
# ============================================================================
print_header('2. LIMPIEZA Y FILTRADO')

log(f"📊 Datos originales: {len(df)} semanas")

# Dropear filas con NaNs en las 8 features
df_clean = df.dropna(subset=FEATURES).copy()
n_dropped = len(df) - len(df_clean)
log(f"   Eliminadas por NaN en features: {n_dropped} semanas")
log(f"✅ Datos limpios: {len(df_clean)} semanas")

if len(df_clean) < 100:
    log(f"⚠️  WARNING: Solo {len(df_clean)} semanas válidas, clustering puede ser inestable")

# Extraer matriz de features
X = df_clean[FEATURES].values
log(f"✅ Matriz de features: {X.shape}")

# ============================================================================
# 3. ANÁLISIS DE CORRELACIÓN
# ============================================================================
print_header('3. MATRIZ DE CORRELACIÓN (PEARSON)')

corr_matrix = df_clean[FEATURES].corr()
corr_file = OUTPUT_DIR / 'features_correlacion.csv'
corr_matrix.to_csv(corr_file)
log(f"✅ Guardado: {corr_file.name}")

# Detectar correlaciones altas (>0.8)
high_corr = []
for i in range(len(FEATURES)):
    for j in range(i+1, len(FEATURES)):
        corr_val = abs(corr_matrix.iloc[i, j])
        if corr_val > 0.8:
            high_corr.append((FEATURES[i], FEATURES[j], corr_val))
            log(
                f"   ⚠️  Alta correlación: {FEATURES[i]} ↔ {FEATURES[j]}: {corr_val:.3f}")

if not high_corr:
    log(f"   ✅ No hay correlaciones >0.8")

# Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title('Matriz de Correlación - Features de Clustering',
             fontsize=12, pad=15)
plt.tight_layout()
heatmap_file = OUTPUT_DIR / 'features_correlacion_heatmap.png'
fig.savefig(heatmap_file, dpi=150)
plt.close(fig)
log(f"✅ Guardado: {heatmap_file.name}")

# ============================================================================
# 4. ANÁLISIS VIF (MULTICOLINEALIDAD)
# ============================================================================
print_header('4. VARIANCE INFLATION FACTOR (VIF)')


vif_data = []
for i, feature in enumerate(FEATURES):
    # Para cada feature, predecir desde las demás
    X_others = df_clean[FEATURES].drop(columns=[feature]).values
    y = df_clean[feature].values

    # Regresión lineal
    lr = LinearRegression()
    lr.fit(X_others, y)
    r_squared = lr.score(X_others, y)

    # VIF = 1 / (1 - R²)
    if r_squared >= 0.9999:  # Evitar división por cero
        vif = 999.0
        log(f"   ⚠️  {feature}: VIF extremo (R²≈1), colinealidad perfecta")
    else:
        vif = 1 / (1 - r_squared)

    vif_data.append({
        'feature': feature,
        'VIF': vif,
        'R_squared': r_squared,
        'flag': 'ALTO' if vif > 10 else ('MODERADO' if vif > 5 else 'OK')
    })

    flag_emoji = "🔴" if vif > 10 else ("🟡" if vif > 5 else "🟢")
    log(f"   {flag_emoji} {feature}: VIF={vif:.2f}, R²={r_squared:.3f}")

vif_df = pd.DataFrame(vif_data)
vif_file = OUTPUT_DIR / 'features_vif.csv'
vif_df.to_csv(vif_file, index=False)
log(f"✅ Guardado: {vif_file.name}")

# Resumen VIF
high_vif = vif_df[vif_df['VIF'] > 10]
if len(high_vif) > 0:
    log(f"\n⚠️  ALERTA: {len(high_vif)} features con VIF>10 (multicolinealidad alta)")
    log(f"   Considerar remover o combinar: {list(high_vif['feature'])}")
else:
    log(f"\n✅ Todos los VIF ≤ 10 (multicolinealidad aceptable)")

# ============================================================================
# 5. ESCALADO ROBUSTO
# ============================================================================
print_header('5. ESCALADO ROBUSTO (RobustScaler)')


scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)

log(f"✅ RobustScaler entrenado (mediana/IQR)")
log(f"   Shape: {X_scaled.shape}")
log(f"   Media post-escalado: {X_scaled.mean(axis=0).mean():.4f} (debería estar cerca de 0)")
log(f"   Std post-escalado: {X_scaled.std(axis=0).mean():.4f}")

# Guardar matriz escalada
df_scaled = df_clean.copy()
for i, feat in enumerate(FEATURES):
    df_scaled[f'{feat}_scaled'] = X_scaled[:, i]

scaled_file = OUTPUT_DIR / 'scaled_matrix.csv'
df_scaled.to_csv(scaled_file, index=False)
log(f"✅ Guardado: {scaled_file.name}")

# ============================================================================
# 6. PCA 2D
# ============================================================================
print_header('6. ANÁLISIS DE COMPONENTES PRINCIPALES (PCA 2D)')


pca = PCA(n_components=2, random_state=RANDOM_STATE)
X_pca = pca.fit_transform(X_scaled)

var_explained = pca.explained_variance_ratio_
var_cum = var_explained.cumsum()

log(f"✅ PCA completado")
log(f"   PC1: {var_explained[0]*100:.2f}% varianza explicada")
log(f"   PC2: {var_explained[1]*100:.2f}% varianza explicada")
log(f"   Acumulada (PC1+PC2): {var_cum[1]*100:.2f}%")

# Guardar coordenadas PCA
df_pca = df_clean[['usuario_id', 'semana_inicio']].copy()
df_pca['PC1'] = X_pca[:, 0]
df_pca['PC2'] = X_pca[:, 1]
pca_file = OUTPUT_DIR / 'pca_2d.csv'
df_pca.to_csv(pca_file, index=False)
log(f"✅ Guardado: {pca_file.name}")

# Biplot
fig, ax = plt.subplots(figsize=(12, 8))

# Puntos (muestra 10% para legibilidad)
sample_idx = np.random.choice(
    len(X_pca), size=int(len(X_pca)*0.1), replace=False)
ax.scatter(X_pca[sample_idx, 0], X_pca[sample_idx, 1],
           alpha=0.3, s=20, c='steelblue', edgecolors='none')

# Cargas (loadings)
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
for i, feature in enumerate(FEATURES):
    ax.arrow(0, 0, loadings[i, 0]*3, loadings[i, 1]*3,
             head_width=0.15, head_length=0.15, fc='red', ec='red', alpha=0.7)
    ax.text(loadings[i, 0]*3.3, loadings[i, 1]*3.3, feature,
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.6))

ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
ax.axvline(0, color='gray', linewidth=0.5, linestyle='--')
ax.set_xlabel(f'PC1 ({var_explained[0]*100:.1f}% var.)', fontsize=11)
ax.set_ylabel(f'PC2 ({var_explained[1]*100:.1f}% var.)', fontsize=11)
ax.set_title(f'PCA Biplot - 8 Features Clustering\n(10% muestra, {len(df_clean)} semanas)',
             fontsize=12, pad=15)
ax.grid(alpha=0.3)
plt.tight_layout()

biplot_file = OUTPUT_DIR / 'pca_biplot.png'
fig.savefig(biplot_file, dpi=150)
plt.close(fig)
log(f"✅ Guardado: {biplot_file.name}")

# ============================================================================
# 7. K-SWEEP (ELBOW + SILHOUETTE)
# ============================================================================
print_header('7. K-SWEEP: MÉTRICAS DE VIABILIDAD (K=2..6)')


k_metrics = []

for k in K_RANGE:
    log(f"\n  Evaluando K={k}...")

    # KMeans
    kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE,
                    n_init=10, max_iter=500)
    labels = kmeans.fit_predict(X_scaled)

    # Inertia (suma de distancias al cuadrado)
    inertia = kmeans.inertia_

    # Silhouette
    if k > 1:
        sil_scores = silhouette_samples(X_scaled, labels)
        sil_mean = sil_scores.mean()
        sil_std = sil_scores.std()
    else:
        sil_mean = np.nan
        sil_std = np.nan

    # Tamaños de clusters
    unique, counts = np.unique(labels, return_counts=True)
    sizes = dict(zip(unique, counts))

    k_metrics.append({
        'k': k,
        'inertia': inertia,
        'silhouette_mean': sil_mean,
        'silhouette_std': sil_std,
        'cluster_sizes': str(sizes)
    })

    log(f"    Inertia: {inertia:.2f}")
    log(f"    Silhouette: {sil_mean:.3f} ± {sil_std:.3f}")
    log(f"    Tamaños: {sizes}")

k_metrics_df = pd.DataFrame(k_metrics)
k_metrics_file = OUTPUT_DIR / 'k_sweep_metrics.csv'
k_metrics_df.to_csv(k_metrics_file, index=False)
log(f"\n✅ Guardado: {k_metrics_file.name}")

# Advertencias
max_sil = k_metrics_df['silhouette_mean'].max()
if max_sil < 0.15:
    log(f"\n⚠️  WARNING: Silhouette máximo = {max_sil:.3f} < 0.15")
    log(f"   Los clusters son débiles; considerar features adicionales o reducir K")
elif max_sil < 0.25:
    log(f"\n🟡 Silhouette máximo = {max_sil:.3f} (moderado, típico en datos reales)")
else:
    log(f"\n✅ Silhouette máximo = {max_sil:.3f} (buena separación)")

# Gráficos de K-sweep
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Elbow plot
axes[0].plot(k_metrics_df['k'], k_metrics_df['inertia'],
             marker='o', linewidth=2, markersize=8, color='steelblue')
axes[0].set_xlabel('Número de Clusters (K)', fontsize=11)
axes[0].set_ylabel('Inertia (within-cluster SS)', fontsize=11)
axes[0].set_title('Elbow Plot', fontsize=12, pad=10)
axes[0].grid(alpha=0.3)
axes[0].set_xticks(K_RANGE)

# Silhouette plot
axes[1].errorbar(k_metrics_df['k'], k_metrics_df['silhouette_mean'],
                 yerr=k_metrics_df['silhouette_std'],
                 marker='o', linewidth=2, markersize=8,
                 color='coral', ecolor='gray', capsize=5)
axes[1].axhline(0.15, color='red', linestyle='--',
                linewidth=1, alpha=0.5, label='Umbral débil')
axes[1].axhline(0.25, color='orange', linestyle='--',
                linewidth=1, alpha=0.5, label='Umbral moderado')
axes[1].set_xlabel('Número de Clusters (K)', fontsize=11)
axes[1].set_ylabel('Silhouette Score (mean ± std)', fontsize=11)
axes[1].set_title('Silhouette vs K', fontsize=12, pad=10)
axes[1].grid(alpha=0.3)
axes[1].set_xticks(K_RANGE)
axes[1].legend(fontsize=9)

plt.tight_layout()
k_sweep_file = OUTPUT_DIR / 'k_sweep_plots.png'
fig.savefig(k_sweep_file, dpi=150)
plt.close(fig)
log(f"✅ Guardado: {k_sweep_file.name}")

# ============================================================================
# 8. RESUMEN FINAL
# ============================================================================
print_header('8. RESUMEN EJECUTIVO')

log(f"\n📊 DATOS PROCESADOS:")
log(f"   - Semanas válidas: {len(df_clean)}")
log(f"   - Features: {len(FEATURES)}")
log(f"   - Usuarios: {df_clean['usuario_id'].nunique()}")

log(f"\n📈 MULTICOLINEALIDAD:")
log(f"   - Features con VIF>10: {len(high_vif)}")
log(f"   - Features con VIF>5: {len(vif_df[vif_df['VIF'] > 5])}")
log(f"   - Correlaciones >0.8: {len(high_corr)}")

log(f"\n🔍 PCA:")
log(f"   - Varianza PC1+PC2: {var_cum[1]*100:.2f}%")

log(f"\n🎯 K-SWEEP:")
best_k = k_metrics_df.loc[k_metrics_df['silhouette_mean'].idxmax(), 'k']
best_sil = k_metrics_df['silhouette_mean'].max()
log(f"   - Mejor K (por Silhouette): {int(best_k)}")
log(f"   - Silhouette máximo: {best_sil:.3f}")
log(f"   - Recomendación: Evaluar K={int(best_k)} y K±1 en clustering final")

log(f"\n📂 ARCHIVOS GENERADOS:")
log(f"   - features_correlacion.csv")
log(f"   - features_correlacion_heatmap.png")
log(f"   - features_vif.csv")
log(f"   - scaled_matrix.csv")
log(f"   - pca_2d.csv")
log(f"   - pca_biplot.png")
log(f"   - k_sweep_metrics.csv")
log(f"   - k_sweep_plots.png")
log(f"   - 06_precluster_qc_log.txt")

print_header('ANÁLISIS PRE-CLUSTERING COMPLETADO')
log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"\n✅ Todos los artefactos en: {OUTPUT_DIR}")
log(f"\n💡 Este análisis es COMPLEMENTARIO al clustering ya ejecutado.")
log(f"   Úsalo para validar la robustez de la metodología y explorar K alternos.")
