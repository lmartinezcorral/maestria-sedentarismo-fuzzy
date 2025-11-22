#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REGRESION LINEAL: Actividad Relativa vs Superavit Calorico
============================================================
Investigador: Luis Angel Martinez Corral
Fecha: 12 de Noviembre de 2025

OBJETIVO:
---------
Explorar si existe relacion lineal entre:
- X: Actividad_relativa (pasos/km - medida de densidad de movimiento)
- Y: Superavit_calorico_basal (cal/TMB - medida de gasto energetico)

HIPOTESIS:
----------
¿La actividad relativa (pasos/km) predice el superavit calorico (cal/TMB)?
¿Podemos usar una variable para predecir la otra?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Configuracion
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 11

COLORS = {
    'cluster_0': '#2E86AB',
    'cluster_1': '#A23B72',
    'regression': '#F18F01'
}

# ============================================================================
# FUNCIONES
# ============================================================================

def calcular_ic_coeficientes(X, y, model, alpha=0.05):
    """Calcula IC 95% para coeficientes (estilo SPSS)"""
    n = len(y)
    k = X.shape[1] if len(X.shape) > 1 else 1
    
    y_pred = model.predict(X.reshape(-1, 1) if len(X.shape) == 1 else X)
    residuals = y - y_pred
    
    mse = np.sum(residuals**2) / (n - k - 1)
    see = np.sqrt(mse)
    
    if len(X.shape) == 1:
        X_design = np.column_stack([np.ones(n), X])
    else:
        X_design = np.column_stack([np.ones(n), X])
    
    cov_matrix = mse * np.linalg.inv(X_design.T @ X_design)
    se_coefs = np.sqrt(np.diag(cov_matrix))
    
    coefs = np.array([model.intercept_] + list(model.coef_ if hasattr(model.coef_, '__iter__') else [model.coef_]))
    t_stats = coefs / se_coefs
    p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), n - k - 1))
    
    t_critical = stats.t.ppf(1 - alpha/2, n - k - 1)
    ci_lower = coefs - t_critical * se_coefs
    ci_upper = coefs + t_critical * se_coefs
    
    return {
        'coef': coefs,
        'se': se_coefs,
        't': t_stats,
        'p': p_values,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'see': see
    }

# ============================================================================
# CARGA DE DATOS
# ============================================================================

print("="*80)
print("REGRESION LINEAL: Actividad Relativa vs Superavit Calorico")
print("="*80)
print()

RUTA_BASE = "../analisis_u"

print("[1/4] Cargando datos...")

df_weekly = pd.read_csv(f"{RUTA_BASE}/semanal/cluster_inputs_weekly.csv")
df_cluster = pd.read_csv(f"{RUTA_BASE}/clustering/cluster_assignments.csv")

# Merge
df = df_weekly.merge(
    df_cluster[['usuario_id', 'semana_inicio', 'cluster']], 
    on=['usuario_id', 'semana_inicio'],
    how='inner'
)

# Limpiar NaNs
df = df.dropna(subset=['Actividad_relativa_p50', 'Superavit_calorico_basal_p50'])

print(f"   [OK] Semanas cargadas: {len(df):,}")
print(f"   [OK] Usuarios: {df['usuario_id'].nunique()}")
print()

df['Cluster_label'] = df['cluster'].map({
    0: 'Bajo Sedentarismo',
    1: 'Alto Sedentarismo'
})

# ============================================================================
# ESTADISTICOS DESCRIPTIVOS
# ============================================================================

print("[2/4] Estadisticos descriptivos:")
print()

desc = df[['Actividad_relativa_p50', 'Superavit_calorico_basal_p50']].describe()
print("MUESTRA COMPLETA (N = {:,}):".format(len(df)))
print(desc)
print()

# Correlacion de Pearson
pearson_r, pearson_p = stats.pearsonr(df['Actividad_relativa_p50'], 
                                        df['Superavit_calorico_basal_p50'])
print(f"CORRELACION DE PEARSON:")
print(f"   r = {pearson_r:.4f}")
print(f"   p = {pearson_p:.4e}")
if pearson_p < 0.001:
    print(f"   >> Correlacion ALTAMENTE SIGNIFICATIVA (p < 0.001)")
elif pearson_p < 0.01:
    print(f"   >> Correlacion MUY SIGNIFICATIVA (p < 0.01)")
elif pearson_p < 0.05:
    print(f"   >> Correlacion SIGNIFICATIVA (p < 0.05)")
else:
    print(f"   >> Correlacion NO SIGNIFICATIVA (p >= 0.05)")
print()

# Interpretacion fuerza
if abs(pearson_r) >= 0.7:
    fuerza = "FUERTE"
elif abs(pearson_r) >= 0.4:
    fuerza = "MODERADA"
elif abs(pearson_r) >= 0.2:
    fuerza = "DEBIL"
else:
    fuerza = "MUY DEBIL o NULA"

direccion = "POSITIVA" if pearson_r > 0 else "NEGATIVA"
print(f"   Interpretacion: Correlacion {fuerza} {direccion}")
print()

# ============================================================================
# REGRESION LINEAL SIMPLE
# ============================================================================

print("="*80)
print("ANALISIS DE REGRESION LINEAL")
print("="*80)
print()

X = df['Actividad_relativa_p50'].values.reshape(-1, 1)
y = df['Superavit_calorico_basal_p50'].values

# Ajustar modelo
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# Metricas
r2 = r2_score(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))
r2_adj = 1 - (1 - r2) * (len(y) - 1) / (len(y) - 2)

# Calcular IC
stats_reg = calcular_ic_coeficientes(X.flatten(), y, model)

print("ECUACION DE REGRESION:")
print(f"   Superavit_calorico = {model.intercept_:.4f} + {model.coef_[0]:.4f} x Actividad_relativa")
print()

print("RESUMEN DEL MODELO:")
print(f"   R = {np.sqrt(r2):.4f}")
print(f"   R cuadrado = {r2:.4f} ({r2*100:.2f}% de varianza explicada)")
print(f"   R cuadrado ajustado = {r2_adj:.4f}")
print(f"   Error estandar de la estimacion = {stats_reg['see']:.4f}")
print(f"   RMSE = {rmse:.4f}")
print()

# ANOVA
ss_total = np.sum((y - y.mean())**2)
ss_regression = np.sum((y_pred - y.mean())**2)
ss_residual = np.sum((y - y_pred)**2)
df_regression = 1
df_residual = len(y) - 2
ms_regression = ss_regression / df_regression
ms_residual = ss_residual / df_residual
f_stat = ms_regression / ms_residual
f_pvalue = 1 - stats.f.cdf(f_stat, df_regression, df_residual)

print("ANOVA:")
anova_df = pd.DataFrame({
    'Fuente': ['Regresion', 'Residual', 'Total'],
    'SC': [ss_regression, ss_residual, ss_total],
    'gl': [df_regression, df_residual, df_regression + df_residual],
    'MC': [ms_regression, ms_residual, np.nan],
    'F': [f_stat, np.nan, np.nan],
    'Sig.': [f_pvalue, np.nan, np.nan]
})
print(anova_df.to_string(index=False))
print()

# Tabla coeficientes
print("COEFICIENTES (ESTILO SPSS):")
tabla_coef = pd.DataFrame({
    'Variable': ['Constante', 'Actividad_relativa'],
    'B': stats_reg['coef'],
    'Error est.': stats_reg['se'],
    't': stats_reg['t'],
    'Sig.': stats_reg['p'],
    'IC 95% Inferior': stats_reg['ci_lower'],
    'IC 95% Superior': stats_reg['ci_upper']
})
print(tabla_coef.to_string(index=False))
print()

# Interpretacion
print("INTERPRETACION:")
print(f"   Beta = {model.coef_[0]:.4f} (IC 95%: [{stats_reg['ci_lower'][1]:.4f}, {stats_reg['ci_upper'][1]:.4f}])")
print(f"   t = {stats_reg['t'][1]:.4f}, p = {stats_reg['p'][1]:.4e}")
print()
if model.coef_[0] > 0:
    print(f"   >> Por cada unidad adicional de Actividad_relativa (pasos/km),")
    print(f"      el Superavit_calorico AUMENTA {model.coef_[0]:.4f} unidades (cal/TMB)")
    print()
    print(f"   >> Interpretacion: A MAYOR densidad de movimiento (pasos/km),")
    print(f"      MAYOR gasto calorico relativo a TMB")
else:
    print(f"   >> Por cada unidad adicional de Actividad_relativa (pasos/km),")
    print(f"      el Superavit_calorico DISMINUYE {abs(model.coef_[0]):.4f} unidades (cal/TMB)")
    print()
    print(f"   >> Interpretacion: A MAYOR densidad de movimiento (pasos/km),")
    print(f"      MENOR gasto calorico relativo a TMB (contraintuitivo)")
print()

# Capacidad predictiva
print("CAPACIDAD PREDICTIVA:")
if r2 >= 0.7:
    print(f"   >> EXCELENTE (R2 = {r2:.2f}): La Actividad_relativa es un EXCELENTE predictor")
elif r2 >= 0.5:
    print(f"   >> BUENA (R2 = {r2:.2f}): La Actividad_relativa es un BUEN predictor")
elif r2 >= 0.3:
    print(f"   >> MODERADA (R2 = {r2:.2f}): La Actividad_relativa es un predictor MODERADO")
elif r2 >= 0.1:
    print(f"   >> BAJA (R2 = {r2:.2f}): La Actividad_relativa es un predictor DEBIL")
else:
    print(f"   >> MUY BAJA (R2 = {r2:.2f}): La Actividad_relativa NO es buen predictor")
print()
print(f"   El modelo explica {r2*100:.1f}% de la varianza del Superavit_calorico")
print(f"   {(1-r2)*100:.1f}% de la varianza NO es explicada por la relacion lineal")
print()

# ============================================================================
# VISUALIZACION
# ============================================================================

print("[3/4] Generando visualizaciones...")
print()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('REGRESION LINEAL: Actividad Relativa vs Superavit Calorico\n' +
             f'N=1,337 semanas | r = {pearson_r:.3f}, R2 = {r2:.3f}',
             fontsize=14, fontweight='bold')

# ============================================================================
# PLOT 1: SCATTER + REGRESION
# ============================================================================
ax1 = axes[0]

# Scatter por cluster
for cluster_id, label, color in [(0, 'Bajo Sedentarismo', COLORS['cluster_0']),
                                   (1, 'Alto Sedentarismo', COLORS['cluster_1'])]:
    mask = df['cluster'] == cluster_id
    ax1.scatter(df[mask]['Actividad_relativa_p50'], 
                df[mask]['Superavit_calorico_basal_p50'],
                alpha=0.4, s=25, label=label, color=color, 
                edgecolors='black', linewidth=0.3)

# Linea de regresion
x_range = np.linspace(df['Actividad_relativa_p50'].min(), 
                       df['Actividad_relativa_p50'].max(), 100).reshape(-1, 1)
y_range_pred = model.predict(x_range)
ax1.plot(x_range, y_range_pred, color=COLORS['regression'], linewidth=3, 
         label=f'Regresion (R2={r2:.3f})', zorder=5)

# IC 95%
x_mean = X.mean()
x_var = np.sum((X - X.mean())**2)
ci = 1.96 * stats_reg['see'] * np.sqrt(1/len(y) + (x_range.flatten() - x_mean)**2 / x_var)
ax1.fill_between(x_range.flatten(), 
                  y_range_pred.flatten() - ci, 
                  y_range_pred.flatten() + ci,
                  alpha=0.2, color='gray', label='IC 95%')

ax1.set_xlabel('Actividad Relativa (pasos/km)', fontweight='bold')
ax1.set_ylabel('Superavit Calorico Basal (cal/TMB)', fontweight='bold')
ax1.set_title(f'A) Scatter Plot + Regresion Lineal\n' +
              f'Beta = {model.coef_[0]:.4f}, p < 0.001',
              fontweight='bold', pad=15)
ax1.legend(loc='best', framealpha=0.9, fontsize=9)
ax1.grid(True, alpha=0.3)

# Ecuacion
eq_text = f'y = {model.intercept_:.2f} + {model.coef_[0]:.2f}x'
ax1.text(0.98, 0.05, eq_text, transform=ax1.transAxes,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
         fontsize=10, ha='right', va='bottom')

# ============================================================================
# PLOT 2: RESIDUALES
# ============================================================================
ax2 = axes[1]

residuals = y - y_pred

ax2.scatter(y_pred, residuals, alpha=0.4, s=25, color='steelblue', 
            edgecolors='black', linewidth=0.3)
ax2.axhline(y=0, color='red', linestyle='--', linewidth=2, label='y = 0')

# Tendencia LOESS
from scipy.signal import savgol_filter
sorted_idx = np.argsort(y_pred)
y_sorted = y_pred[sorted_idx]
res_sorted = residuals[sorted_idx]
if len(y_sorted) > 51:
    res_smooth = savgol_filter(res_sorted, window_length=51, polyorder=3)
    ax2.plot(y_sorted, res_smooth, color='orange', linewidth=2, label='Tendencia')

ax2.set_xlabel('Valores Predichos (Superavit Calorico)', fontweight='bold')
ax2.set_ylabel('Residuales', fontweight='bold')
ax2.set_title(f'B) Diagnostico: Residuales vs Predichos\n' +
              f'RMSE = {rmse:.4f}, Homocedasticidad',
              fontweight='bold', pad=15)
ax2.legend(loc='upper right', framealpha=0.9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# Guardar
import os
output_dir = os.path.join(os.path.dirname(__file__), "..", "resultados")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "regresion_actividad_vs_superavit.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   [OK] Figura guardada: {output_path}")
print()

# Guardar tabla
tabla_coef.to_csv(os.path.join(output_dir, "tabla_coef_actividad_superavit.csv"), index=False)
print(f"   [OK] Tabla guardada: resultados/tabla_coef_actividad_superavit.csv")
print()

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("="*80)
print("RESUMEN EJECUTIVO")
print("="*80)
print()
print("PREGUNTA DE INVESTIGACION:")
print("   ¿La Actividad_relativa (pasos/km) predice el Superavit_calorico (cal/TMB)?")
print()
print("RESPUESTA:")
if pearson_p < 0.05 and r2 >= 0.3:
    print(f"   >> SI, existe relacion {fuerza} {direccion} (r = {pearson_r:.3f}, p < 0.001)")
    print(f"   >> La Actividad_relativa explica {r2*100:.1f}% de la varianza")
    calidad = "BUENO" if r2 >= 0.5 else "MODERADO"
    print(f"   >> ES un predictor {calidad}")
elif pearson_p < 0.05 and r2 < 0.3:
    print(f"   >> SI, existe relacion estadisticamente significativa (p < 0.05)")
    print(f"   >> Pero la relacion es {fuerza} (r = {pearson_r:.3f})")
    print(f"   >> La Actividad_relativa explica solo {r2*100:.1f}% de la varianza")
    print(f"   >> NO es un buen predictor (R2 < 0.30)")
else:
    print(f"   >> NO, no existe relacion significativa (p = {pearson_p:.3f})")
    print(f"   >> La Actividad_relativa NO puede predecir el Superavit_calorico")
print()
print("ECUACION PREDICTIVA:")
print(f"   Superavit_calorico = {model.intercept_:.4f} + {model.coef_[0]:.4f} x Actividad_relativa")
print()
print("EJEMPLO PRACTICO:")
ejemplo_x = df['Actividad_relativa_p50'].median()
ejemplo_y_pred = model.predict([[ejemplo_x]])[0]
print(f"   Si Actividad_relativa = {ejemplo_x:.4f} (mediana),")
print(f"   entonces Superavit_calorico predicho = {ejemplo_y_pred:.2f} cal/TMB")
print()
print("="*80)
print("[4/4] ANALISIS COMPLETADO")
print("="*80)
print()

plt.show()

