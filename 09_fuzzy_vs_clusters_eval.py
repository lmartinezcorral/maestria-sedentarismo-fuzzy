"""
09_fuzzy_vs_clusters_eval.py
Evaluación de Concordancia: Sistema Difuso vs Clustering K=2
Paso 7C: Validación cruzada
"""

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, precision_score, recall_score
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

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
BASE_DIR = Path(__file__).parent.resolve()
FUZZY_FILE = BASE_DIR / 'analisis_u' / 'fuzzy' / 'fuzzy_output.csv'
CLUSTER_FILE = BASE_DIR / 'analisis_u' / \
    'clustering' / 'cluster_assignments.csv'

OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'fuzzy'
PLOTS_DIR = OUTPUT_DIR / 'plots'
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / '09_eval_fuzzy_vs_cluster.txt'
DISCORD_FILE = OUTPUT_DIR / 'discordancias_top20.csv'


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
print_header('FUZZY VS CLUSTERS - PASO 7C: EVALUACIÓN DE CONCORDANCIA')
log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"Fuzzy output: {FUZZY_FILE}")
log(f"Cluster assignments: {CLUSTER_FILE}")

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================
print_header('1. CARGANDO DATOS')

# Verificar archivos
if not FUZZY_FILE.exists():
    log(f"❌ ERROR: No existe {FUZZY_FILE}")
    log(f"   Ejecuta primero: python 08_fuzzy_inference.py")
    sys.exit(1)

if not CLUSTER_FILE.exists():
    log(f"❌ ERROR: No existe {CLUSTER_FILE}")
    log(f"   El clustering (Paso 6) debe haberse ejecutado antes")
    sys.exit(1)

df_fuzzy = pd.read_csv(FUZZY_FILE)
df_cluster = pd.read_csv(CLUSTER_FILE)

log(f"✅ Fuzzy output: {len(df_fuzzy)} semanas")
log(f"✅ Cluster assignments: {len(df_cluster)} semanas")

# ============================================================================
# 2. UNIR DATOS
# ============================================================================
print_header('2. UNIENDO FUZZY Y CLUSTERS')

# Identificar columnas clave para merge
# Fuzzy tiene: usuario_id, semana_inicio
# Cluster tiene: usuario_id, semana_inicio (o similar)

fuzzy_cols = list(df_fuzzy.columns)
cluster_cols = list(df_cluster.columns)

log(f"Columnas en fuzzy: {fuzzy_cols[:5]}...")
log(f"Columnas en cluster: {cluster_cols[:5]}...")

# Normalizar nombres de columnas para merge
# Asumiendo que ambos tienen 'usuario_id' y 'semana_inicio'
merge_keys = ['usuario_id', 'semana_inicio']

# Verificar que las llaves existan
for key in merge_keys:
    if key not in df_fuzzy.columns:
        log(f"⚠️  WARNING: {key} no está en df_fuzzy")
    if key not in df_cluster.columns:
        log(f"⚠️  WARNING: {key} no está en df_cluster")

# Intentar merge
df_merged = df_fuzzy.merge(df_cluster[merge_keys + ['cluster']],
                           on=merge_keys,
                           how='inner',
                           suffixes=('_fuzzy', '_cluster'))

log(f"✅ Merged: {len(df_merged)} semanas")
log(f"   Pérdida por merge: {len(df_fuzzy) - len(df_merged)} semanas")

if len(df_merged) < 500:
    log(f"⚠️  WARNING: Solo {len(df_merged)} semanas válidas para evaluación")

# ============================================================================
# 3. DETERMINAR MAPEO CLUSTER → SEDENTARISMO
# ============================================================================
print_header('3. ANALIZANDO MAPEO CLUSTER → SEDENTARISMO')

# Calcular score medio por cluster
cluster_stats = df_merged.groupby('cluster')['Sedentarismo_score'].agg([
    'mean', 'median', 'std', 'count'])
log(f"\nEstadísticas de Sedentarismo_score por cluster:")
log(f"\n{cluster_stats}")

# Determinar qué cluster corresponde a "Alto Sedentarismo"
# Asumimos: cluster con MAYOR score medio = Alto Sedentarismo
cluster_high_sed = cluster_stats['mean'].idxmax()
cluster_low_sed = cluster_stats['mean'].idxmin()

log(f"\n✅ Mapeo determinado:")
log(
    f"   Cluster {cluster_high_sed}: Alto Sedentarismo (score medio={cluster_stats.loc[cluster_high_sed, 'mean']:.3f})")
log(
    f"   Cluster {cluster_low_sed}: Bajo Sedentarismo (score medio={cluster_stats.loc[cluster_low_sed, 'mean']:.3f})")

# Crear label binario para clusters
df_merged['cluster_alto_sed'] = (
    df_merged['cluster'] == cluster_high_sed).astype(int)

# ============================================================================
# 4. BÚSQUEDA DE UMBRAL ÓPTIMO
# ============================================================================
print_header('4. BÚSQUEDA DE UMBRAL ÓPTIMO (τ)')


# Grid de umbrales
thresholds = np.linspace(0.3, 0.7, 41)
metrics_list = []

for tau in thresholds:
    # Binarizar fuzzy
    fuzzy_bin = (df_merged['Sedentarismo_score'] >= tau).astype(int)
    cluster_bin = df_merged['cluster_alto_sed']

    # Calcular métricas
    acc = accuracy_score(cluster_bin, fuzzy_bin)
    f1 = f1_score(cluster_bin, fuzzy_bin, zero_division=0)
    mcc = matthews_corrcoef(cluster_bin, fuzzy_bin)
    prec = precision_score(cluster_bin, fuzzy_bin, zero_division=0)
    rec = recall_score(cluster_bin, fuzzy_bin, zero_division=0)

    metrics_list.append({
        'tau': tau,
        'accuracy': acc,
        'f1': f1,
        'mcc': mcc,
        'precision': prec,
        'recall': rec
    })

df_metrics = pd.DataFrame(metrics_list)

# Encontrar mejor τ por F1
best_idx = df_metrics['f1'].idxmax()
best_tau = df_metrics.loc[best_idx, 'tau']
best_f1 = df_metrics.loc[best_idx, 'f1']
best_acc = df_metrics.loc[best_idx, 'accuracy']
best_mcc = df_metrics.loc[best_idx, 'mcc']

log(f"\n✅ Umbral óptimo encontrado:")
log(f"   τ = {best_tau:.3f}")
log(f"   Accuracy: {best_acc:.3f}")
log(f"   F1: {best_f1:.3f}")
log(f"   MCC: {best_mcc:.3f}")
log(f"   Precision: {df_metrics.loc[best_idx, 'precision']:.3f}")
log(f"   Recall: {df_metrics.loc[best_idx, 'recall']:.3f}")

# Advertencia si concordancia es baja
if best_f1 < 0.60:
    log(f"\n⚠️  WARNING: Concordancia baja (F1 < 0.60)")
    log(f"   Considerar ajustar:")
    log(f"   - Pesos de reglas difusas")
    log(f"   - Percentiles de funciones de membresía")
    log(f"   - Agregar reglas moduladoras")
elif best_f1 < 0.70:
    log(f"\n🟡 Concordancia moderada (0.60 ≤ F1 < 0.70)")
    log(f"   Aceptable para datos reales; considerar ajustes menores")
else:
    log(f"\n✅ Concordancia buena (F1 ≥ 0.70)")

# ============================================================================
# 5. ANÁLISIS CON UMBRAL ÓPTIMO
# ============================================================================
print_header('5. ANÁLISIS CON UMBRAL ÓPTIMO')

# Aplicar umbral óptimo
df_merged['fuzzy_alto_sed'] = (
    df_merged['Sedentarismo_score'] >= best_tau).astype(int)

# Matriz de confusión

cm = confusion_matrix(
    df_merged['cluster_alto_sed'], df_merged['fuzzy_alto_sed'])
log(f"\nMatriz de Confusión (Cluster vs Fuzzy):")
log(f"   Predicho→")
log(f"Real↓   0(Bajo)  1(Alto)")
log(f"  0     {cm[0,0]:6d}  {cm[0,1]:6d}")
log(f"  1     {cm[1,0]:6d}  {cm[1,1]:6d}")

# Concordancia/Discordancia
concordantes = (df_merged['cluster_alto_sed'] ==
                df_merged['fuzzy_alto_sed']).sum()
discordantes = len(df_merged) - concordantes

log(f"\nConcordancia:")
log(f"   Concordantes: {concordantes} ({concordantes/len(df_merged)*100:.1f}%)")
log(f"   Discordantes: {discordantes} ({discordantes/len(df_merged)*100:.1f}%)")

# ============================================================================
# 6. ANÁLISIS POR USUARIO
# ============================================================================
print_header('6. ANÁLISIS POR USUARIO')

user_concordance = df_merged.groupby('usuario_id').apply(
    lambda x: (x['cluster_alto_sed'] == x['fuzzy_alto_sed']).mean()
).sort_values()

log(f"\nConcordancia por usuario:")
for user_id, conc in user_concordance.items():
    log(f"   {user_id}: {conc*100:.1f}%")

log(f"\n   Media: {user_concordance.mean()*100:.1f}%")
log(f"   Min: {user_concordance.min()*100:.1f}% ({user_concordance.idxmin()})")
log(f"   Max: {user_concordance.max()*100:.1f}% ({user_concordance.idxmax()})")

# ============================================================================
# 7. TOP 20 DISCORDANCIAS
# ============================================================================
print_header('7. IDENTIFICANDO DISCORDANCIAS (TOP 20)')

# Filtrar discordantes
df_discord = df_merged[df_merged['cluster_alto_sed']
                       != df_merged['fuzzy_alto_sed']].copy()

# Ordenar por diferencia absoluta en score
df_discord['score_diff'] = abs(df_discord['Sedentarismo_score'] - best_tau)
df_discord_top = df_discord.nlargest(20, 'score_diff')

# Seleccionar columnas relevantes
discord_cols = ['usuario_id', 'semana_inicio', 'Sedentarismo_score',
                'cluster', 'cluster_alto_sed', 'fuzzy_alto_sed', 'score_diff']

# Agregar features si existen
for col in df_discord_top.columns:
    if 'Actividad_relativa_p50' in col or 'Superavit' in col or 'HRV' in col:
        if col not in discord_cols:
            discord_cols.append(col)

df_discord_top[discord_cols[:10]].to_csv(DISCORD_FILE, index=False)
log(f"\n✅ Guardado: {DISCORD_FILE.name}")
log(f"   Top 20 discordancias para revisión clínica")

# ============================================================================
# 8. VISUALIZACIONES
# ============================================================================
print_header('8. GENERANDO VISUALIZACIONES')

# 8.1 Matriz de Confusión
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Bajo Sed', 'Alto Sed'],
            yticklabels=['Bajo Sed', 'Alto Sed'],
            ax=ax, cbar_kws={'label': 'Frecuencia'})
ax.set_xlabel('Predicción Fuzzy', fontsize=11)
ax.set_ylabel('Cluster Real', fontsize=11)
ax.set_title(f'Matriz de Confusión (τ={best_tau:.2f}, Acc={best_acc:.2f})',
             fontsize=12, pad=15)
plt.tight_layout()

cm_file = PLOTS_DIR / 'confusion_matrix.png'
fig.savefig(cm_file, dpi=150)
plt.close(fig)
log(f"✅ Guardado: {cm_file.name}")

# 8.2 Curva PR (Precision-Recall)

precisions, recalls, thresholds_pr = precision_recall_curve(
    df_merged['cluster_alto_sed'],
    df_merged['Sedentarismo_score']
)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(recalls, precisions, linewidth=2, color='steelblue', label='PR Curve')
ax.scatter([df_metrics.loc[best_idx, 'recall']],
           [df_metrics.loc[best_idx, 'precision']],
           color='red', s=100, zorder=5, label=f'τ óptimo={best_tau:.2f}')
ax.set_xlabel('Recall', fontsize=11)
ax.set_ylabel('Precision', fontsize=11)
ax.set_title(f'Curva Precision-Recall (F1={best_f1:.3f})', fontsize=12, pad=15)
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()

pr_file = PLOTS_DIR / 'pr_curve.png'
fig.savefig(pr_file, dpi=150)
plt.close(fig)
log(f"✅ Guardado: {pr_file.name}")

# 8.3 Distribución de scores por cluster
fig, ax = plt.subplots(figsize=(10, 6))
for cluster_id in sorted(df_merged['cluster'].unique()):
    scores = df_merged[df_merged['cluster']
                       == cluster_id]['Sedentarismo_score']
    label = f"Cluster {cluster_id} ({'Alto' if cluster_id == cluster_high_sed else 'Bajo'} Sed)"
    ax.hist(scores, bins=30, alpha=0.6, label=label, edgecolor='black')

ax.axvline(best_tau, color='red', linestyle='--', linewidth=2,
           label=f'τ óptimo={best_tau:.2f}')
ax.set_xlabel('Sedentarismo Score', fontsize=11)
ax.set_ylabel('Frecuencia', fontsize=11)
ax.set_title('Distribución de Scores por Cluster', fontsize=12, pad=15)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()

dist_file = PLOTS_DIR / 'score_distribution_by_cluster.png'
fig.savefig(dist_file, dpi=150)
plt.close(fig)
log(f"✅ Guardado: {dist_file.name}")

# ============================================================================
# 9. RESUMEN FINAL
# ============================================================================
print_header('9. RESUMEN EJECUTIVO')

log(f"\n📊 DATOS EVALUADOS:")
log(f"   - Semanas válidas: {len(df_merged)}")
log(f"   - Usuarios: {df_merged['usuario_id'].nunique()}")

log(f"\n🎯 UMBRAL ÓPTIMO:")
log(f"   - τ = {best_tau:.3f}")
log(f"   - Sedentarismo_score ≥ τ → Alto Sedentarismo")

log(f"\n📈 MÉTRICAS DE CONCORDANCIA:")
log(f"   - Accuracy: {best_acc:.3f}")
log(f"   - F1-Score: {best_f1:.3f}")
log(f"   - MCC: {best_mcc:.3f}")
log(f"   - Precision: {df_metrics.loc[best_idx, 'precision']:.3f}")
log(f"   - Recall: {df_metrics.loc[best_idx, 'recall']:.3f}")

log(f"\n📊 MATRIZ DE CONFUSIÓN:")
log(f"   TN={cm[0,0]}, FP={cm[0,1]}, FN={cm[1,0]}, TP={cm[1,1]}")

log(f"\n👥 CONCORDANCIA POR USUARIO:")
log(f"   - Media: {user_concordance.mean()*100:.1f}%")
log(f"   - Rango: {user_concordance.min()*100:.1f}% - {user_concordance.max()*100:.1f}%")

log(f"\n✅ ARCHIVOS GENERADOS:")
log(f"   - 09_eval_fuzzy_vs_cluster.txt")
log(f"   - discordancias_top20.csv")
log(f"   - plots/confusion_matrix.png")
log(f"   - plots/pr_curve.png")
log(f"   - plots/score_distribution_by_cluster.png")

# Sugerencias si concordancia baja
if best_f1 < 0.70:
    log(f"\n💡 SUGERENCIAS DE AJUSTE:")
    if best_f1 < 0.60:
        log(f"   🔴 Concordancia baja - Ajustes recomendados:")
    else:
        log(f"   🟡 Concordancia moderada - Considerar:")

    log(f"   1. Revisar pesos de reglas (R5 tiene peso 0.7, ajustar)")
    log(f"   2. Agregar reglas moduladoras con IQR (variabilidad intra-semana)")
    log(f"   3. Ajustar percentiles de MF si distribución es asimétrica")
    log(f"   4. Revisar top 20 discordancias para detectar patrones")
    log(f"   5. Validar que Delta_cardiaco esté correctamente calculado")

print_header('EVALUACIÓN FUZZY VS CLUSTERS COMPLETADA')
log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log(f"\n✅ Evaluación completa. Revisar métricas y ajustar si F1 < 0.70")


