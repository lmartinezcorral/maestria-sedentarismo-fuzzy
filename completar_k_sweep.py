"""Completar K-Sweep del análisis pre-clustering"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).parent.resolve()
INPUT_FILE = BASE_DIR / 'analisis_u' / 'semanal' / 'cluster_inputs_weekly.csv'
OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'semanal' / 'precluster'

FEATURES = [
    'Actividad_relativa_p50', 'Actividad_relativa_iqr',
    'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr',
    'HRV_SDNN_p50', 'HRV_SDNN_iqr',
    'Delta_cardiaco_p50', 'Delta_cardiaco_iqr'
]

print("Cargando datos...")
df = pd.read_csv(INPUT_FILE)
X = df[FEATURES].values

print("Escalando con RobustScaler...")
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)

print("\nEjecutando K-Sweep (K=2..6)...")
k_metrics = []

for k in range(2, 7):
    print(f"  K={k}...", end='', flush=True)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=500)
    labels = kmeans.fit_predict(X_scaled)

    inertia = kmeans.inertia_
    sil_scores = silhouette_samples(X_scaled, labels)
    sil_mean = sil_scores.mean()
    sil_std = sil_scores.std()

    unique, counts = np.unique(labels, return_counts=True)
    sizes = dict(zip(unique, counts))

    k_metrics.append({
        'k': k,
        'inertia': inertia,
        'silhouette_mean': sil_mean,
        'silhouette_std': sil_std,
        'cluster_sizes': str(sizes)
    })

    print(f" Inertia={inertia:.2f}, Sil={sil_mean:.3f}")

k_metrics_df = pd.DataFrame(k_metrics)
k_metrics_file = OUTPUT_DIR / 'k_sweep_metrics.csv'
k_metrics_df.to_csv(k_metrics_file, index=False)
print(f"\n✅ Guardado: {k_metrics_file}")

# Gráficos
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(k_metrics_df['k'], k_metrics_df['inertia'],
             marker='o', linewidth=2, markersize=8, color='steelblue')
axes[0].set_xlabel('Número de Clusters (K)', fontsize=11)
axes[0].set_ylabel('Inertia', fontsize=11)
axes[0].set_title('Elbow Plot', fontsize=12)
axes[0].grid(alpha=0.3)
axes[0].set_xticks(range(2, 7))

axes[1].errorbar(k_metrics_df['k'], k_metrics_df['silhouette_mean'],
                 yerr=k_metrics_df['silhouette_std'],
                 marker='o', linewidth=2, markersize=8,
                 color='coral', ecolor='gray', capsize=5)
axes[1].axhline(0.15, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[1].axhline(0.25, color='orange', linestyle='--', linewidth=1, alpha=0.5)
axes[1].set_xlabel('Número de Clusters (K)', fontsize=11)
axes[1].set_ylabel('Silhouette Score', fontsize=11)
axes[1].set_title('Silhouette vs K', fontsize=12)
axes[1].grid(alpha=0.3)
axes[1].set_xticks(range(2, 7))

plt.tight_layout()
k_sweep_file = OUTPUT_DIR / 'k_sweep_plots.png'
fig.savefig(k_sweep_file, dpi=150)
plt.close(fig)
print(f"✅ Guardado: {k_sweep_file}")

# Resumen
best_k = k_metrics_df.loc[k_metrics_df['silhouette_mean'].idxmax(), 'k']
best_sil = k_metrics_df['silhouette_mean'].max()
print(f"\n📊 Mejor K (por Silhouette): {int(best_k)}")
print(f"   Silhouette máximo: {best_sil:.3f}")
print("\n✅ K-Sweep completado")


