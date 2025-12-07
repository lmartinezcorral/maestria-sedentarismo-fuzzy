"""
12_recalcular_t_test_datos_correctos.py
========================================

Recalcula el t-test usando los datos CORRECTOS del Capítulo 6:
F1 LOUO = 0.780 ± 0.167 (n=10)

Datos por usuario del Capítulo 6:
u1: 0.994, u2: 0.667, u3: 0.545, u4: 0.846, u5: 0.833,
u6: 0.677, u7: 0.978, u8: 0.526, u9: 0.847, u10: 0.887
"""

import numpy as np
from scipy import stats
from scipy.stats import ttest_1samp, shapiro
import pandas as pd
from pathlib import Path

# Datos CORRECTOS del Capítulo 6
f1_scores = np.array([
    0.994,  # u1
    0.667,  # u2
    0.545,  # u3
    0.846,  # u4
    0.833,  # u5
    0.677,  # u6
    0.978,  # u7
    0.526,  # u8
    0.847,  # u9
    0.887   # u10
])

n = len(f1_scores)
mean_f1 = f1_scores.mean()
std_f1 = f1_scores.std()

print("="*80)
print("RECÁLCULO T-TEST CON DATOS CORRECTOS DEL CAPÍTULO 6")
print("="*80)
print(f"\nF1-Score LOUO: {mean_f1:.3f} ± {std_f1:.3f} (n={n})")
print(f"Hipótesis nula: F1 = 0.50 (clasificador aleatorio)")
print()

# Verificar normalidad (Shapiro-Wilk para n<50)
shapiro_stat, shapiro_p = shapiro(f1_scores)
print(f"Prueba de normalidad (Shapiro-Wilk):")
print(f"   Estadístico: {shapiro_stat:.4f}, p-value: {shapiro_p:.4f}")
is_normal = shapiro_p > 0.05
print(f"   Conclusión: {'Distribución normal' if is_normal else 'Distribución NO normal'}")
print()

# Prueba t de una muestra (H0: μ = 0.50, H1: μ > 0.50)
t_stat, p_value = ttest_1samp(f1_scores, 0.50, alternative='greater')

# Intervalo de confianza 95%
sem = std_f1 / np.sqrt(n)
t_critical = stats.t.ppf(0.975, df=n-1)  # 95% CI, two-tailed
ci_lower = mean_f1 - t_critical * sem
ci_upper = mean_f1 + t_critical * sem

print(f"Prueba t de una muestra (H0: μ = 0.50, H1: μ > 0.50):")
print(f"   t({n-1}) = {t_stat:.4f}")
print(f"   p-value = {p_value:.6f}")
print(f"   Conclusión: {'Significativo' if p_value < 0.05 else 'NO significativo'} (p < 0.05)")
print()

print(f"Intervalo de confianza 95% para F1 promedio:")
print(f"   [{ci_lower:.3f}, {ci_upper:.3f}]")
print(f"   Límite inferior: {ci_lower:.3f} {'>' if ci_lower > 0.50 else '≤'} 0.50")
print()

# Cohen's d
cohens_d = (mean_f1 - 0.50) / std_f1
print(f"Tamaño del efecto (Cohen's d):")
print(f"   d = {cohens_d:.3f}")

if abs(cohens_d) < 0.2:
    interpretacion = "Despreciable"
elif abs(cohens_d) < 0.5:
    interpretacion = "Pequeño"
elif abs(cohens_d) < 0.8:
    interpretacion = "Mediano"
else:
    interpretacion = "Grande"

print(f"   Interpretación: {interpretacion}")
print()

# Guardar resultados
OUTPUT_DIR = Path('analisis_u/resultados_cap6')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
    'shapiro_p': shapiro_p,
    'cohens_d': cohens_d,
    'interpretacion_cohens_d': interpretacion
}

df_results = pd.DataFrame([results])
output_file = OUTPUT_DIR / 't_test_significancia_louo_CORRECTO.csv'
df_results.to_csv(output_file, index=False)
print(f"✅ Guardado: {output_file}")
print()

print("="*80)
print("RESUMEN:")
print("="*80)
print(f"F1 LOUO = {mean_f1:.3f} ± {std_f1:.3f}")
print(f"t({n-1}) = {t_stat:.4f}, p = {p_value:.6f}")
print(f"IC 95%: [{ci_lower:.3f}, {ci_upper:.3f}]")
print(f"Cohen's d = {cohens_d:.3f} ({interpretacion})")
print(f"Conclusión: {'El modelo es significativamente superior al clasificador aleatorio' if p_value < 0.05 else 'El modelo NO es significativamente superior al clasificador aleatorio'}")

