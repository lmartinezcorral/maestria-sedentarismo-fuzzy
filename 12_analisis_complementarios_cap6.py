"""
12_analisis_complementarios_cap6.py
====================================

OBJETIVO:
---------
Ejecutar análisis complementarios para el Capítulo 6 de Resultados:
1. Prueba estadística de significancia (t-test) para F1 LOUO vs clasificador aleatorio
2. Análisis de distribución de scores fuzzy (histograma por cluster)
3. Análisis sistemático de errores (FP vs FN, patrones)
4. Análisis de tamaño del efecto (Cohen's d, etc.)

SALIDAS:
--------
- analisis_u/resultados_cap6/
  - t_test_significancia_louo.csv
  - distribucion_scores_fuzzy.csv
  - analisis_errores.csv
  - effect_size_analysis.csv
  - plots/
    - distribucion_scores_fuzzy.png
    - analisis_errores.png
    - effect_size_visualization.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_1samp, mannwhitneyu, normaltest
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_DIR = Path(__file__).parent.resolve()
FUZZY_OUTPUT = BASE_DIR / 'analisis_u' / 'fuzzy' / 'fuzzy_output.csv'
CLUSTER_ASSIGNMENTS = BASE_DIR / 'analisis_u' / 'clustering' / 'cluster_assignments.csv'
LOUO_SUMMARY = BASE_DIR / 'analisis_u' / 'louo_results' / 'louo_summary.csv'

OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'resultados_cap6'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / 'plots').mkdir(exist_ok=True)

LOG_FILE = OUTPUT_DIR / '12_analisis_complementarios_log.txt'

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
# ANÁLISIS 1: PRUEBA T-TEST DE SIGNIFICANCIA LOUO
# ============================================================================


def analisis_t_test_louo(df_louo):
    """Prueba t-test: ¿F1 LOUO es significativamente > 0.50 (clasificador aleatorio)?"""
    print_header('ANÁLISIS 1: PRUEBA T-TEST DE SIGNIFICANCIA LOUO')
    
    f1_scores = df_louo['f1_test'].values
    n = len(f1_scores)
    mean_f1 = f1_scores.mean()
    std_f1 = f1_scores.std()
    
    log(f"F1-Score LOUO: {mean_f1:.3f} ± {std_f1:.3f} (n={n})")
    log(f"Hipótesis nula: F1 = 0.50 (clasificador aleatorio)")
    log("")
    
    # Verificar normalidad (Shapiro-Wilk para n<50)
    if n < 50:
        shapiro_stat, shapiro_p = stats.shapiro(f1_scores)
        log(f"Prueba de normalidad (Shapiro-Wilk):")
        log(f"   Estadístico: {shapiro_stat:.4f}, p-value: {shapiro_p:.4f}")
        is_normal = shapiro_p > 0.05
    else:
        # Para n>=50, usar D'Agostino
        dagostino_stat, dagostino_p = normaltest(f1_scores)
        log(f"Prueba de normalidad (D'Agostino):")
        log(f"   Estadístico: {dagostino_stat:.4f}, p-value: {dagostino_p:.4f}")
        is_normal = dagostino_p > 0.05
    
    log(f"   Conclusión: {'Distribución normal' if is_normal else 'Distribución NO normal'}")
    log("")
    
    # Prueba t de una muestra (H0: μ = 0.50)
    t_stat, p_value = ttest_1samp(f1_scores, 0.50, alternative='greater')
    
    # Intervalo de confianza 95%
    sem = std_f1 / np.sqrt(n)
    t_critical = stats.t.ppf(0.975, df=n-1)  # 95% CI, two-tailed
    ci_lower = mean_f1 - t_critical * sem
    ci_upper = mean_f1 + t_critical * sem
    
    log(f"Prueba t de una muestra (H0: μ = 0.50, H1: μ > 0.50):")
    log(f"   t({n-1}) = {t_stat:.4f}")
    log(f"   p-value = {p_value:.6f}")
    log(f"   Conclusión: {'Significativo' if p_value < 0.05 else 'NO significativo'} (p < 0.05)")
    log("")
    
    log(f"Intervalo de confianza 95% para F1 promedio:")
    log(f"   [{ci_lower:.3f}, {ci_upper:.3f}]")
    log(f"   Límite inferior: {ci_lower:.3f} {'>' if ci_lower > 0.50 else '≤'} 0.50")
    log("")
    
    # Guardar resultados
    results = {
        'n': n,
        'mean_f1': mean_f1,
        'std_f1': std_f1,
        't_statistic': t_stat,
        'p_value': p_value,
        'ci_95_lower': ci_lower,
        'ci_95_upper': ci_upper,
        'is_significant': p_value < 0.05,
        'is_normal': is_normal,
        'shapiro_p' if n < 50 else 'dagostino_p': shapiro_p if n < 50 else dagostino_p
    }
    
    df_results = pd.DataFrame([results])
    output_file = OUTPUT_DIR / 't_test_significancia_louo.csv'
    df_results.to_csv(output_file, index=False)
    log(f"✅ Guardado: {output_file.name}")
    log("")
    
    return results

# ============================================================================
# ANÁLISIS 2: DISTRIBUCIÓN DE SCORES FUZZY
# ============================================================================


def analisis_distribucion_scores(df_fuzzy, df_clusters):
    """Análisis de distribución de scores fuzzy por cluster"""
    print_header('ANÁLISIS 2: DISTRIBUCIÓN DE SCORES FUZZY')
    
    # Merge
    df = df_fuzzy.merge(
        df_clusters[['usuario_id', 'semana_inicio', 'cluster']],
        on=['usuario_id', 'semana_inicio'],
        how='inner'
    )
    
    scores = df['Sedentarismo_score'].values
    clusters = df['cluster'].values
    
    log(f"Total semanas: {len(df)}")
    log(f"Cluster 0 (ACTIVO): {(clusters==0).sum()} semanas")
    log(f"Cluster 1 (SEDENTARIO): {(clusters==1).sum()} semanas")
    log("")
    
    # Estadísticos por cluster
    scores_activo = scores[clusters == 0]
    scores_sedentario = scores[clusters == 1]
    
    log(f"Estadísticos de scores por cluster:")
    log(f"   Cluster 0 (ACTIVO):")
    log(f"      Media: {scores_activo.mean():.3f} ± {scores_activo.std():.3f}")
    log(f"      Mediana: {np.median(scores_activo):.3f}")
    log(f"      IQR: [{np.percentile(scores_activo, 25):.3f}, {np.percentile(scores_activo, 75):.3f}]")
    log("")
    log(f"   Cluster 1 (SEDENTARIO):")
    log(f"      Media: {scores_sedentario.mean():.3f} ± {scores_sedentario.std():.3f}")
    log(f"      Mediana: {np.median(scores_sedentario):.3f}")
    log(f"      IQR: [{np.percentile(scores_sedentario, 25):.3f}, {np.percentile(scores_sedentario, 75):.3f}]")
    log("")
    
    # Prueba Mann-Whitney U (no paramétrica, no requiere normalidad)
    u_stat, u_p = mannwhitneyu(scores_activo, scores_sedentario, alternative='two-sided')
    log(f"Prueba Mann-Whitney U (diferencias entre clusters):")
    log(f"   U = {u_stat:.0f}, p-value = {u_p:.6f}")
    log(f"   Conclusión: {'Significativo' if u_p < 0.05 else 'NO significativo'} (p < 0.05)")
    log("")
    
    # Solapamiento: calcular porcentaje de solapamiento
    min_activo = scores_activo.min()
    max_activo = scores_activo.max()
    min_sedentario = scores_sedentario.min()
    max_sedentario = scores_sedentario.max()
    
    overlap_range = [max(min_activo, min_sedentario), min(max_activo, max_sedentario)]
    overlap_pct_activo = ((scores_activo >= overlap_range[0]) & (scores_activo <= overlap_range[1])).sum() / len(scores_activo) * 100
    overlap_pct_sedentario = ((scores_sedentario >= overlap_range[0]) & (scores_sedentario <= overlap_range[1])).sum() / len(scores_sedentario) * 100
    
    log(f"Análisis de solapamiento:")
    log(f"   Rango solapamiento: [{overlap_range[0]:.3f}, {overlap_range[1]:.3f}]")
    log(f"   % Cluster ACTIVO en rango solapado: {overlap_pct_activo:.1f}%")
    log(f"   % Cluster SEDENTARIO en rango solapado: {overlap_pct_sedentario:.1f}%")
    log("")
    
    # Guardar resultados
    results = {
        'cluster': [0, 1],
        'n_weeks': [len(scores_activo), len(scores_sedentario)],
        'mean_score': [scores_activo.mean(), scores_sedentario.mean()],
        'std_score': [scores_activo.std(), scores_sedentario.std()],
        'median_score': [np.median(scores_activo), np.median(scores_sedentario)],
        'q25': [np.percentile(scores_activo, 25), np.percentile(scores_sedentario, 25)],
        'q75': [np.percentile(scores_activo, 75), np.percentile(scores_sedentario, 75)],
        'min': [scores_activo.min(), scores_sedentario.min()],
        'max': [scores_activo.max(), scores_sedentario.max()]
    }
    
    df_results = pd.DataFrame(results)
    output_file = OUTPUT_DIR / 'distribucion_scores_fuzzy.csv'
    df_results.to_csv(output_file, index=False)
    log(f"✅ Guardado: {output_file.name}")
    log("")
    
    # Crear figura: Histograma superpuesto
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Subplot 1: Histograma superpuesto
    ax = axes[0]
    ax.hist(scores_activo, bins=50, alpha=0.6, label='Cluster 0 (ACTIVO)', 
            color='#F1B253', edgecolor='black', linewidth=0.5)
    ax.hist(scores_sedentario, bins=50, alpha=0.6, label='Cluster 1 (SEDENTARIO)', 
            color='#5C025D', edgecolor='black', linewidth=0.5)
    ax.axvline(x=0.30, color='red', linestyle='--', linewidth=2, label='Umbral τ=0.30')
    ax.set_xlabel('Score Fuzzy (Sedentarismo)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
    ax.set_title('Distribución de Scores Fuzzy por Cluster', fontsize=14, fontweight='bold', pad=15)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    # Subplot 2: Densidad KDE
    ax = axes[1]
    sns.kdeplot(data=df, x='Sedentarismo_score', hue='cluster', ax=ax, 
                palette={0: '#F1B253', 1: '#5C025D'}, fill=True, alpha=0.6)
    ax.axvline(x=0.30, color='red', linestyle='--', linewidth=2, label='Umbral τ=0.30')
    ax.set_xlabel('Score Fuzzy (Sedentarismo)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Densidad', fontsize=12, fontweight='bold')
    ax.set_title('Densidad de Scores Fuzzy (KDE)', fontsize=14, fontweight='bold', pad=15)
    ax.legend(['Cluster 0 (ACTIVO)', 'Cluster 1 (SEDENTARIO)', 'Umbral τ=0.30'], fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plot_file = OUTPUT_DIR / 'plots' / 'distribucion_scores_fuzzy.png'
    fig.savefig(plot_file, dpi=150, bbox_inches='tight')
    plt.close(fig)
    log(f"✅ Guardado: plots/distribucion_scores_fuzzy.png")
    log("")
    
    return {
        'u_stat': u_stat,
        'u_p': u_p,
        'overlap_range': overlap_range,
        'overlap_pct_activo': overlap_pct_activo,
        'overlap_pct_sedentario': overlap_pct_sedentario
    }

# ============================================================================
# ANÁLISIS 3: ANÁLISIS SISTEMÁTICO DE ERRORES
# ============================================================================


def analisis_errores(df_fuzzy, df_clusters):
    """Análisis sistemático de errores de clasificación"""
    print_header('ANÁLISIS 3: ANÁLISIS SISTEMÁTICO DE ERRORES')
    
    # Merge
    df = df_fuzzy.merge(
        df_clusters[['usuario_id', 'semana_inicio', 'cluster']],
        on=['usuario_id', 'semana_inicio'],
        how='inner'
    )
    
    # Binarizar con umbral τ=0.30
    tau = 0.30
    df['y_pred'] = (df['Sedentarismo_score'] >= tau).astype(int)
    df['y_true'] = df['cluster'].astype(int)
    
    # Calcular TP, FP, TN, FN
    df['TP'] = ((df['y_pred'] == 1) & (df['y_true'] == 1)).astype(int)
    df['FP'] = ((df['y_pred'] == 1) & (df['y_true'] == 0)).astype(int)
    df['TN'] = ((df['y_pred'] == 0) & (df['y_true'] == 0)).astype(int)
    df['FN'] = ((df['y_pred'] == 0) & (df['y_true'] == 1)).astype(int)
    
    # Errores totales
    total_errores = df['FP'].sum() + df['FN'].sum()
    total_correctos = df['TP'].sum() + df['TN'].sum()
    
    log(f"Total semanas: {len(df)}")
    log(f"Clasificaciones correctas: {total_correctos} ({total_correctos/len(df)*100:.1f}%)")
    log(f"Errores totales: {total_errores} ({total_errores/len(df)*100:.1f}%)")
    log("")
    
    # Desglose de errores
    fp_total = df['FP'].sum()
    fn_total = df['FN'].sum()
    
    log(f"Desglose de errores:")
    log(f"   Falsos Positivos (FP): {fp_total} ({fp_total/total_errores*100:.1f}% de errores)")
    log(f"   Falsos Negativos (FN): {fn_total} ({fn_total/total_errores*100:.1f}% de errores)")
    log("")
    
    # Análisis por usuario
    errores_por_usuario = []
    for usuario in sorted(df['usuario_id'].unique()):
        df_user = df[df['usuario_id'] == usuario]
        fp_user = df_user['FP'].sum()
        fn_user = df_user['FN'].sum()
        total_user = len(df_user)
        pct_error = (fp_user + fn_user) / total_user * 100
        
        errores_por_usuario.append({
            'usuario_id': usuario,
            'n_semanas': total_user,
            'fp': fp_user,
            'fn': fn_user,
            'total_errores': fp_user + fn_user,
            'pct_errores': pct_error,
            'pct_fp': fp_user / (fp_user + fn_user) * 100 if (fp_user + fn_user) > 0 else 0,
            'pct_fn': fn_user / (fp_user + fn_user) * 100 if (fp_user + fn_user) > 0 else 0
        })
    
    df_errores = pd.DataFrame(errores_por_usuario)
    
    log(f"Errores por usuario:")
    for _, row in df_errores.iterrows():
        log(f"   {row['usuario_id']}: {row['total_errores']} errores ({row['pct_errores']:.1f}%) - "
            f"FP: {row['fp']} ({row['pct_fp']:.1f}%), FN: {row['fn']} ({row['pct_fn']:.1f}%)")
    log("")
    
    # Usuarios con más errores
    top_errores = df_errores.nlargest(3, 'total_errores')
    log(f"Top 3 usuarios con más errores:")
    for _, row in top_errores.iterrows():
        log(f"   {row['usuario_id']}: {row['total_errores']} errores ({row['pct_errores']:.1f}%)")
    log("")
    
    # Guardar resultados
    output_file = OUTPUT_DIR / 'analisis_errores.csv'
    df_errores.to_csv(output_file, index=False)
    log(f"✅ Guardado: {output_file.name}")
    log("")
    
    # Paleta Maracuyada Natural
    PALETA_MARACUYADA = {
        'morado_muy_oscuro': '#3F0340',
        'morado_profundo': '#612073',
        'morado_medio': '#772B8C',
        'dorado_natural': '#BFA556',
        'marron_dorado': '#8C5C03'
    }
    
    # Crear figura: Análisis de errores
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Subplot 1: Errores por usuario (barras)
    ax = axes[0]
    x_pos = np.arange(len(df_errores))
    width = 0.35
    ax.bar(x_pos - width/2, df_errores['fp'], width, label='Falsos Positivos (FP)', 
           color=PALETA_MARACUYADA['dorado_natural'], edgecolor='black', linewidth=0.5)
    ax.bar(x_pos + width/2, df_errores['fn'], width, label='Falsos Negativos (FN)', 
           color=PALETA_MARACUYADA['morado_profundo'], edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Usuario', fontsize=12, fontweight='bold')
    ax.set_ylabel('Número de Errores', fontsize=12, fontweight='bold')
    ax.set_title('Errores de Clasificación por Usuario', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df_errores['usuario_id'], fontsize=10)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Porcentaje de errores por usuario
    ax = axes[1]
    ax.bar(x_pos, df_errores['pct_errores'], color=PALETA_MARACUYADA['morado_medio'], 
           edgecolor='black', linewidth=0.5)
    ax.axhline(y=df_errores['pct_errores'].mean(), color=PALETA_MARACUYADA['marron_dorado'], 
               linestyle='--', linewidth=2, label=f'Media: {df_errores["pct_errores"].mean():.1f}%')
    ax.set_xlabel('Usuario', fontsize=12, fontweight='bold')
    ax.set_ylabel('% de Errores', fontsize=12, fontweight='bold')
    ax.set_title('Porcentaje de Errores por Usuario', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df_errores['usuario_id'], fontsize=10)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plot_file = OUTPUT_DIR / 'plots' / 'analisis_errores.png'
    fig.savefig(plot_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    log(f"✅ Guardado: plots/analisis_errores.png")
    log("")
    
    return df_errores

# ============================================================================
# ANÁLISIS 4: TAMAÑO DEL EFECTO
# ============================================================================


def analisis_tamano_efecto(df_fuzzy, df_clusters, df_louo):
    """Análisis de tamaño del efecto (Cohen's d, etc.)"""
    print_header('ANÁLISIS 4: TAMAÑO DEL EFECTO')
    
    # ========================================================================
    # 4.1: Tamaño del efecto para F1 LOUO vs clasificador aleatorio
    # ========================================================================
    
    f1_scores = df_louo['f1_test'].values
    mean_f1 = f1_scores.mean()
    std_f1 = f1_scores.std()
    baseline_f1 = 0.50  # Clasificador aleatorio
    
    # Cohen's d para una muestra
    cohens_d_f1 = (mean_f1 - baseline_f1) / std_f1
    
    log(f"4.1. Tamaño del efecto: F1 LOUO vs Clasificador Aleatorio (F1=0.50)")
    log(f"   F1 promedio: {mean_f1:.3f} ± {std_f1:.3f}")
    log(f"   Baseline (aleatorio): {baseline_f1:.3f}")
    log(f"   Cohen's d: {cohens_d_f1:.3f}")
    
    # Interpretación de Cohen's d
    if abs(cohens_d_f1) < 0.2:
        interpretacion = "Despreciable"
    elif abs(cohens_d_f1) < 0.5:
        interpretacion = "Pequeño"
    elif abs(cohens_d_f1) < 0.8:
        interpretacion = "Mediano"
    else:
        interpretacion = "Grande"
    
    log(f"   Interpretación: {interpretacion} (|d| < 0.2: despreciable, < 0.5: pequeño, < 0.8: mediano, ≥ 0.8: grande)")
    log("")
    
    # ========================================================================
    # 4.2: Tamaño del efecto para scores fuzzy entre clusters
    # ========================================================================
    
    df = df_fuzzy.merge(
        df_clusters[['usuario_id', 'semana_inicio', 'cluster']],
        on=['usuario_id', 'semana_inicio'],
        how='inner'
    )
    
    scores_activo = df[df['cluster'] == 0]['Sedentarismo_score'].values
    scores_sedentario = df[df['cluster'] == 1]['Sedentarismo_score'].values
    
    # Cohen's d para dos muestras independientes
    mean_activo = scores_activo.mean()
    mean_sedentario = scores_sedentario.mean()
    std_activo = scores_activo.std()
    std_sedentario = scores_sedentario.std()
    
    # Pooled standard deviation
    n_activo = len(scores_activo)
    n_sedentario = len(scores_sedentario)
    pooled_std = np.sqrt(((n_activo - 1) * std_activo**2 + (n_sedentario - 1) * std_sedentario**2) / 
                         (n_activo + n_sedentario - 2))
    
    cohens_d_scores = (mean_sedentario - mean_activo) / pooled_std
    
    log(f"4.2. Tamaño del efecto: Scores Fuzzy entre Clusters")
    log(f"   Cluster 0 (ACTIVO): {mean_activo:.3f} ± {std_activo:.3f} (n={n_activo})")
    log(f"   Cluster 1 (SEDENTARIO): {mean_sedentario:.3f} ± {std_sedentario:.3f} (n={n_sedentario})")
    log(f"   Diferencia de medias: {mean_sedentario - mean_activo:.3f}")
    log(f"   Cohen's d: {cohens_d_scores:.3f}")
    
    if abs(cohens_d_scores) < 0.2:
        interpretacion_scores = "Despreciable"
    elif abs(cohens_d_scores) < 0.5:
        interpretacion_scores = "Pequeño"
    elif abs(cohens_d_scores) < 0.8:
        interpretacion_scores = "Mediano"
    else:
        interpretacion_scores = "Grande"
    
    log(f"   Interpretación: {interpretacion_scores}")
    log("")
    
    # ========================================================================
    # 4.3: Tamaño del efecto para métricas LOUO
    # ========================================================================
    
    metrics = ['f1_test', 'accuracy_test', 'precision_test', 'recall_test', 'mcc_test']
    baseline_values = {
        'f1_test': 0.50,
        'accuracy_test': 0.50,  # Asumiendo balance de clases
        'precision_test': 0.50,
        'recall_test': 0.50,
        'mcc_test': 0.00
    }
    
    effect_sizes = []
    
    for metric in metrics:
        values = df_louo[metric].values
        mean_val = values.mean()
        std_val = values.std()
        baseline = baseline_values[metric]
        
        cohens_d = (mean_val - baseline) / std_val
        
        if abs(cohens_d) < 0.2:
            interpret = "Despreciable"
        elif abs(cohens_d) < 0.5:
            interpret = "Pequeño"
        elif abs(cohens_d) < 0.8:
            interpret = "Mediano"
        else:
            interpret = "Grande"
        
        effect_sizes.append({
            'metrica': metric,
            'mean': mean_val,
            'std': std_val,
            'baseline': baseline,
            'cohens_d': cohens_d,
            'interpretacion': interpret
        })
    
    df_effect = pd.DataFrame(effect_sizes)
    
    log(f"4.3. Tamaño del efecto para métricas LOUO:")
    for _, row in df_effect.iterrows():
        log(f"   {row['metrica']}: d={row['cohens_d']:.3f} ({row['interpretacion']})")
    log("")
    
    # Guardar resultados
    results_combined = {
        'analisis': ['F1_LOUO_vs_Aleatorio', 'Scores_Fuzzy_Clusters', 'F1_LOUO_vs_Aleatorio', 
                     'Accuracy_LOUO_vs_Aleatorio', 'Precision_LOUO_vs_Aleatorio', 
                     'Recall_LOUO_vs_Aleatorio', 'MCC_LOUO_vs_Aleatorio'],
        'mean': [mean_f1, mean_sedentario, df_louo['f1_test'].mean(), 
                 df_louo['accuracy_test'].mean(), df_louo['precision_test'].mean(),
                 df_louo['recall_test'].mean(), df_louo['mcc_test'].mean()],
        'std': [std_f1, pooled_std, df_louo['f1_test'].std(),
                df_louo['accuracy_test'].std(), df_louo['precision_test'].std(),
                df_louo['recall_test'].std(), df_louo['mcc_test'].std()],
        'baseline': [0.50, mean_activo, 0.50, 0.50, 0.50, 0.50, 0.00],
        'cohens_d': [cohens_d_f1, cohens_d_scores, df_effect.loc[0, 'cohens_d'],
                     df_effect.loc[1, 'cohens_d'], df_effect.loc[2, 'cohens_d'],
                     df_effect.loc[3, 'cohens_d'], df_effect.loc[4, 'cohens_d']],
        'interpretacion': [interpretacion, interpretacion_scores] + df_effect['interpretacion'].tolist()
    }
    
    df_results = pd.DataFrame(results_combined)
    output_file = OUTPUT_DIR / 'effect_size_analysis.csv'
    df_results.to_csv(output_file, index=False)
    log(f"✅ Guardado: {output_file.name}")
    log("")
    
    # Paleta Maracuyada Natural
    PALETA_MARACUYADA = {
        'morado_muy_oscuro': '#3F0340',
        'morado_profundo': '#612073',
        'morado_medio': '#772B8C',
        'dorado_natural': '#BFA556',
        'marron_dorado': '#8C5C03'
    }
    
    # Crear figura: Visualización de tamaños del efecto
    fig, ax = plt.subplots(figsize=(12, 6))
    
    metricas_nombres = ['F1 LOUO', 'Accuracy LOUO', 'Precision LOUO', 'Recall LOUO', 'MCC LOUO']
    cohens_d_values = [df_effect.loc[0, 'cohens_d'], df_effect.loc[1, 'cohens_d'],
                       df_effect.loc[2, 'cohens_d'], df_effect.loc[3, 'cohens_d'],
                       df_effect.loc[4, 'cohens_d']]
    
    # Colores según tamaño del efecto usando paleta Maracuyada
    colors = []
    for d in cohens_d_values:
        if abs(d) >= 0.8:
            colors.append(PALETA_MARACUYADA['morado_profundo'])  # Grande - morado profundo
        elif abs(d) >= 0.5:
            colors.append(PALETA_MARACUYADA['morado_medio'])      # Mediano - morado medio
        else:
            colors.append(PALETA_MARACUYADA['dorado_natural'])    # Pequeño - dorado natural
    
    bars = ax.barh(metricas_nombres, cohens_d_values, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.axvline(x=0.2, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Pequeño (d=0.2)')
    ax.axvline(x=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Mediano (d=0.5)')
    ax.axvline(x=0.8, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Grande (d=0.8)')
    ax.set_xlabel("Cohen's d", fontsize=12, fontweight='bold')
    ax.set_ylabel('Métrica', fontsize=12, fontweight='bold')
    ax.set_title("Tamaño del Efecto: Métricas LOUO vs Clasificador Aleatorio", 
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(axis='x', alpha=0.3)
    ax.legend(fontsize=9)
    
    # Anotar valores
    for i, (bar, d) in enumerate(zip(bars, cohens_d_values)):
        ax.text(d + 0.05 if d >= 0 else d - 0.05, i, f"{d:.3f}", 
                va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plot_file = OUTPUT_DIR / 'plots' / 'effect_size_visualization.png'
    fig.savefig(plot_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    log(f"✅ Guardado: plots/effect_size_visualization.png")
    log("")
    
    return df_results

# ============================================================================
# MAIN
# ============================================================================


def main():
    print_header('ANÁLISIS COMPLEMENTARIOS CAPÍTULO 6 - PASO 12')
    log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Directorio salida: {OUTPUT_DIR}")
    log("")
    
    # Cargar datos
    print_header('CARGANDO DATOS')
    
    if not FUZZY_OUTPUT.exists():
        log(f"❌ ERROR: No existe {FUZZY_OUTPUT}")
        return 1
    
    if not CLUSTER_ASSIGNMENTS.exists():
        log(f"❌ ERROR: No existe {CLUSTER_ASSIGNMENTS}")
        return 1
    
    if not LOUO_SUMMARY.exists():
        log(f"⚠️  ADVERTENCIA: No existe {LOUO_SUMMARY}")
        log("   Continuando sin análisis LOUO...")
        df_louo = None
    else:
        df_louo = pd.read_csv(LOUO_SUMMARY)
        log(f"✅ LOUO summary cargado: {len(df_louo)} usuarios")
    
    df_fuzzy = pd.read_csv(FUZZY_OUTPUT)
    df_clusters = pd.read_csv(CLUSTER_ASSIGNMENTS)
    
    log(f"✅ Fuzzy output cargado: {len(df_fuzzy)} semanas")
    log(f"✅ Cluster assignments cargado: {len(df_clusters)} semanas")
    log("")
    
    # Ejecutar análisis
    results = {}
    
    # Análisis 1: T-test
    if df_louo is not None:
        results['t_test'] = analisis_t_test_louo(df_louo)
    
    # Análisis 2: Distribución scores
    results['distribucion'] = analisis_distribucion_scores(df_fuzzy, df_clusters)
    
    # Análisis 3: Errores
    results['errores'] = analisis_errores(df_fuzzy, df_clusters)
    
    # Análisis 4: Tamaño del efecto
    if df_louo is not None:
        results['effect_size'] = analisis_tamano_efecto(df_fuzzy, df_clusters, df_louo)
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    
    print_header('RESUMEN EJECUTIVO')
    
    if df_louo is not None:
        log(f"✅ Prueba t-test de significancia: {'Significativo' if results['t_test']['is_significant'] else 'NO significativo'}")
        log(f"   F1 LOUO = {results['t_test']['mean_f1']:.3f} ± {results['t_test']['std_f1']:.3f}")
        log(f"   p-value = {results['t_test']['p_value']:.6f}")
        log("")
    
    log(f"✅ Distribución de scores fuzzy:")
    log(f"   Mann-Whitney U: p = {results['distribucion']['u_p']:.6f}")
    log(f"   Solapamiento: [{results['distribucion']['overlap_range'][0]:.3f}, {results['distribucion']['overlap_range'][1]:.3f}]")
    log("")
    
    log(f"✅ Análisis de errores:")
    log(f"   Total errores: {results['errores']['total_errores'].sum()}")
    log(f"   FP: {results['errores']['fp'].sum()}, FN: {results['errores']['fn'].sum()}")
    log("")
    
    if df_louo is not None:
        log(f"✅ Tamaño del efecto:")
        log(f"   F1 LOUO vs aleatorio: Cohen's d = {results['effect_size'].loc[0, 'cohens_d']:.3f}")
        log(f"   Scores fuzzy clusters: Cohen's d = {results['effect_size'].loc[1, 'cohens_d']:.3f}")
        log("")
    
    # Guardar log
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG_LINES))
    
    print_header('ANÁLISIS COMPLEMENTARIOS COMPLETADOS')
    log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"\n✅ Todos los resultados en: {OUTPUT_DIR}")
    log("")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

