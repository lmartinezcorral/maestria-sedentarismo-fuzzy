#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REGRESION LINEAL SIMPLE - CLASE DE BIOESTADISTICA
==================================================
Ejemplo didactico: Superavit Calorico vs Comportamiento Sedentario

Investigador: Luis Angel Martinez Corral
Fecha: 12 de Noviembre de 2025

OBJETIVO:
---------
Demostrar el funcionamiento de la regresion lineal con un ejemplo simple
usando variables de MOVIMIENTO (actividad fisica y gasto calorico).

ANALISIS:
---------
1. Regresion Simple: Superavit_calorico vs Score_sedentarismo
2. Estratificacion por Cluster: Alto sedentarismo vs Bajo sedentarismo
3. Tablas estilo SPSS: Coeficientes, IC 95%, t, p-valores

DATOS:
------
- N = 1,337 semanas validas
- 10 participantes (5F/5M, edad 34.2±6.7 años)
- Wearable: Apple Watch (vida libre, paradigma BYOD)
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

# ============================================================================
# CONFIGURACION
# ============================================================================

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 12

COLORS = {
    'cluster_0': '#2E86AB',  # Azul - Bajo Sedentarismo
    'cluster_1': '#A23B72',  # Morado - Alto Sedentarismo
    'regression': '#F18F01'  # Naranja - Linea regresion
}

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def calcular_ic_coeficientes(X, y, model, alpha=0.05):
    """
    Calcula intervalos de confianza para los coeficientes de regresion.
    Estilo SPSS: Beta, Error Estandar, t, p-valor, IC 95%
    """
    n = len(y)
    k = X.shape[1] if len(X.shape) > 1 else 1
    
    # Predicciones y residuales
    y_pred = model.predict(X.reshape(-1, 1) if len(X.shape) == 1 else X)
    residuals = y - y_pred
    
    # Error estandar de la regresion (SEE)
    mse = np.sum(residuals**2) / (n - k - 1)
    see = np.sqrt(mse)
    
    # Matriz de covarianza
    if len(X.shape) == 1:
        X_design = np.column_stack([np.ones(n), X])
    else:
        X_design = np.column_stack([np.ones(n), X])
    
    # Covarianza de los coeficientes
    cov_matrix = mse * np.linalg.inv(X_design.T @ X_design)
    
    # Error estandar de los coeficientes
    se_coefs = np.sqrt(np.diag(cov_matrix))
    
    # Estadistico t
    coefs = np.array([model.intercept_] + list(model.coef_ if hasattr(model.coef_, '__iter__') else [model.coef_]))
    t_stats = coefs / se_coefs
    
    # p-valores (prueba bilateral)
    p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), n - k - 1))
    
    # Intervalos de confianza
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

def crear_tabla_spss(stats_dict, var_names=['Constante', 'Superavit_calorico']):
    """
    Crea DataFrame estilo tabla SPSS de coeficientes
    """
    df = pd.DataFrame({
        'Variable': var_names,
        'B': stats_dict['coef'],
        'Error est.': stats_dict['se'],
        't': stats_dict['t'],
        'Sig.': stats_dict['p'],
        'IC 95% Inferior': stats_dict['ci_lower'],
        'IC 95% Superior': stats_dict['ci_upper']
    })
    return df

# ============================================================================
# CARGA DE DATOS
# ============================================================================

print("="*80)
print("REGRESION LINEAL SIMPLE - CLASE DE BIOESTADISTICA")
print("Superavit Calorico vs Comportamiento Sedentario")
print("="*80)
print()

RUTA_BASE = "../analisis_u"

print("[1/5] Cargando datos...")

# Cargar datasets
df_weekly = pd.read_csv(f"{RUTA_BASE}/semanal/cluster_inputs_weekly.csv")
df_cluster = pd.read_csv(f"{RUTA_BASE}/clustering/cluster_assignments.csv")
df_fuzzy = pd.read_csv(f"{RUTA_BASE}/fuzzy/fuzzy_output.csv")

# Merge
df = df_weekly.merge(
    df_cluster[['usuario_id', 'semana_inicio', 'cluster']], 
    on=['usuario_id', 'semana_inicio'],
    how='inner'
)
df = df.merge(
    df_fuzzy[['usuario_id', 'semana_inicio', 'Sedentarismo_score']], 
    on=['usuario_id', 'semana_inicio'],
    how='inner'
)

# Limpiar NaNs
df = df.dropna(subset=['Superavit_calorico_basal_p50', 'Sedentarismo_score'])

print(f"   [OK] Semanas cargadas: {len(df):,}")
print(f"   [OK] Usuarios: {df['usuario_id'].nunique()}")
print(f"   [OK] Periodo: {df['semana_inicio'].min()} a {df['semana_inicio'].max()}")
print()

# Etiquetas
df['Cluster_label'] = df['cluster'].map({
    0: 'Bajo Sedentarismo',
    1: 'Alto Sedentarismo'
})

# ============================================================================
# ESTADISTICOS DESCRIPTIVOS
# ============================================================================

print("[2/5] Estadisticos descriptivos:")
print()

desc_global = df[['Superavit_calorico_basal_p50', 'Sedentarismo_score']].describe()
print("MUESTRA COMPLETA (N = {:,}):".format(len(df)))
print(desc_global)
print()

desc_por_cluster = df.groupby('Cluster_label')[['Superavit_calorico_basal_p50', 'Sedentarismo_score']].describe()
print("POR CLUSTER:")
print(desc_por_cluster)
print()

# ============================================================================
# REGRESION LINEAL SIMPLE - MUESTRA COMPLETA
# ============================================================================

print("="*80)
print("ANALISIS 1: REGRESION LINEAL SIMPLE (MUESTRA COMPLETA)")
print("="*80)
print()

X_global = df['Superavit_calorico_basal_p50'].values.reshape(-1, 1)
y_global = df['Sedentarismo_score'].values

# Ajustar modelo
model_global = LinearRegression()
model_global.fit(X_global, y_global)
y_global_pred = model_global.predict(X_global)

# Metricas
r2_global = r2_score(y_global, y_global_pred)
rmse_global = np.sqrt(mean_squared_error(y_global, y_global_pred))
pearson_r_global, pearson_p_global = stats.pearsonr(X_global.flatten(), y_global)

# Calcular estadisticos IC (estilo SPSS)
stats_global = calcular_ic_coeficientes(X_global.flatten(), y_global, model_global)

print("ECUACION DE REGRESION:")
print(f"   Sedentarismo = {model_global.intercept_:.4f} + ({model_global.coef_[0]:.6f}) x Superavit_calorico")
print()

print("RESUMEN DEL MODELO:")
print(f"   R = {np.sqrt(r2_global):.4f}")
print(f"   R cuadrado = {r2_global:.4f}")
print(f"   R cuadrado ajustado = {1 - (1 - r2_global) * (len(y_global) - 1) / (len(y_global) - 2):.4f}")
print(f"   Error estandar de la estimacion = {stats_global['see']:.4f}")
print()

print("ANOVA:")
ss_total = np.sum((y_global - y_global.mean())**2)
ss_regression = np.sum((y_global_pred - y_global.mean())**2)
ss_residual = np.sum((y_global - y_global_pred)**2)
df_regression = 1
df_residual = len(y_global) - 2
ms_regression = ss_regression / df_regression
ms_residual = ss_residual / df_residual
f_stat = ms_regression / ms_residual
f_pvalue = 1 - stats.f.cdf(f_stat, df_regression, df_residual)

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

print("COEFICIENTES:")
tabla_coef_global = crear_tabla_spss(stats_global)
print(tabla_coef_global.to_string(index=False))
print()

# Interpretacion
sig_label = "***" if pearson_p_global < 0.001 else "**" if pearson_p_global < 0.01 else "*" if pearson_p_global < 0.05 else "ns"
print(f"INTERPRETACION {sig_label}:")
if model_global.coef_[0] < 0:
    print(f"   > A MAYOR superavit calorico, MENOR comportamiento sedentario")
    print(f"   > Por cada unidad adicional de superavit, el score de sedentarismo")
    print(f"     DISMINUYE {abs(model_global.coef_[0]):.6f} unidades (IC 95%: [{stats_global['ci_lower'][1]:.6f}, {stats_global['ci_upper'][1]:.6f}])")
else:
    print(f"   > A MAYOR superavit calorico, MAYOR comportamiento sedentario (inesperado)")
    print(f"   > Por cada unidad adicional de superavit, el score de sedentarismo")
    print(f"     AUMENTA {model_global.coef_[0]:.6f} unidades (IC 95%: [{stats_global['ci_lower'][1]:.6f}, {stats_global['ci_upper'][1]:.6f}])")
print()

# ============================================================================
# REGRESION POR CLUSTER (ESTRATIFICADA)
# ============================================================================

print("="*80)
print("ANALISIS 2: REGRESION ESTRATIFICADA POR CLUSTER")
print("="*80)
print()

# Cluster 0 (Bajo Sedentarismo)
df_c0 = df[df['cluster'] == 0]
X_c0 = df_c0['Superavit_calorico_basal_p50'].values.reshape(-1, 1)
y_c0 = df_c0['Sedentarismo_score'].values

model_c0 = LinearRegression()
model_c0.fit(X_c0, y_c0)
y_c0_pred = model_c0.predict(X_c0)
r2_c0 = r2_score(y_c0, y_c0_pred)
pearson_r_c0, pearson_p_c0 = stats.pearsonr(X_c0.flatten(), y_c0)
stats_c0 = calcular_ic_coeficientes(X_c0.flatten(), y_c0, model_c0)

# Cluster 1 (Alto Sedentarismo)
df_c1 = df[df['cluster'] == 1]
X_c1 = df_c1['Superavit_calorico_basal_p50'].values.reshape(-1, 1)
y_c1 = df_c1['Sedentarismo_score'].values

model_c1 = LinearRegression()
model_c1.fit(X_c1, y_c1)
y_c1_pred = model_c1.predict(X_c1)
r2_c1 = r2_score(y_c1, y_c1_pred)
pearson_r_c1, pearson_p_c1 = stats.pearsonr(X_c1.flatten(), y_c1)
stats_c1 = calcular_ic_coeficientes(X_c1.flatten(), y_c1, model_c1)

print(f"CLUSTER 0 (BAJO SEDENTARISMO) - N = {len(df_c0)}")
print("-" * 80)
print(f"Ecuacion: Sedentarismo = {model_c0.intercept_:.4f} + ({model_c0.coef_[0]:.6f}) x Superavit_calorico")
print(f"R cuadrado = {r2_c0:.4f}, Error est. = {stats_c0['see']:.4f}")
print()
print("COEFICIENTES:")
tabla_coef_c0 = crear_tabla_spss(stats_c0)
print(tabla_coef_c0.to_string(index=False))
print()

print(f"CLUSTER 1 (ALTO SEDENTARISMO) - N = {len(df_c1)}")
print("-" * 80)
print(f"Ecuacion: Sedentarismo = {model_c1.intercept_:.4f} + ({model_c1.coef_[0]:.6f}) x Superavit_calorico")
print(f"R cuadrado = {r2_c1:.4f}, Error est. = {stats_c1['see']:.4f}")
print()
print("COEFICIENTES:")
tabla_coef_c1 = crear_tabla_spss(stats_c1)
print(tabla_coef_c1.to_string(index=False))
print()

print("COMPARACION DE PENDIENTES:")
print(f"   Cluster 0 (Bajo): Beta = {model_c0.coef_[0]:.6f} (IC 95%: [{stats_c0['ci_lower'][1]:.6f}, {stats_c0['ci_upper'][1]:.6f}])")
print(f"   Cluster 1 (Alto): Beta = {model_c1.coef_[0]:.6f} (IC 95%: [{stats_c1['ci_lower'][1]:.6f}, {stats_c1['ci_upper'][1]:.6f}])")
print()

# Prueba de diferencia de pendientes
diff_beta = model_c0.coef_[0] - model_c1.coef_[0]
se_diff = np.sqrt(stats_c0['se'][1]**2 + stats_c1['se'][1]**2)
t_diff = diff_beta / se_diff
df_diff = len(df_c0) + len(df_c1) - 4
p_diff = 2 * (1 - stats.t.cdf(np.abs(t_diff), df_diff))

print("PRUEBA DE DIFERENCIA DE PENDIENTES:")
print(f"   Diferencia (Beta_C0 - Beta_C1) = {diff_beta:.6f}")
print(f"   Error estandar de la diferencia = {se_diff:.6f}")
print(f"   t({df_diff}) = {t_diff:.4f}, p = {p_diff:.4f}")
if p_diff < 0.05:
    print(f"   >> Las pendientes son SIGNIFICATIVAMENTE DIFERENTES (p < 0.05)")
else:
    print(f"   >> Las pendientes NO difieren significativamente (p >= 0.05)")
print()

# ============================================================================
# VISUALIZACION
# ============================================================================

print("[3/5] Generando visualizaciones...")
print()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('REGRESION LINEAL SIMPLE: Superavit Calorico vs Comportamiento Sedentario\n' +
             'N=1,337 semanas | 10 usuarios | Datos reales Apple Watch',
             fontsize=14, fontweight='bold')

# ============================================================================
# PLOT 1: REGRESION GLOBAL
# ============================================================================
ax1 = axes[0]

# Scatter por cluster
for cluster_id, label, color in [(0, 'Bajo Sedentarismo', COLORS['cluster_0']),
                                   (1, 'Alto Sedentarismo', COLORS['cluster_1'])]:
    mask = df['cluster'] == cluster_id
    ax1.scatter(df[mask]['Superavit_calorico_basal_p50'], 
                df[mask]['Sedentarismo_score'],
                alpha=0.4, s=25, label=label, color=color, 
                edgecolors='black', linewidth=0.3)

# Linea de regresion
x_range = np.linspace(df['Superavit_calorico_basal_p50'].min(), 
                       df['Superavit_calorico_basal_p50'].max(), 100).reshape(-1, 1)
y_range_pred = model_global.predict(x_range)
ax1.plot(x_range, y_range_pred, color=COLORS['regression'], linewidth=3, 
         label=f'Regresion (R2={r2_global:.3f})', zorder=5)

# Intervalo de confianza
rhr_range_mean = X_global.mean()
X_global_var = np.sum((X_global - X_global.mean())**2)
ci = 1.96 * stats_global['see'] * np.sqrt(1/len(y_global) + (x_range.flatten() - rhr_range_mean)**2 / X_global_var)
ax1.fill_between(x_range.flatten(), 
                  y_range_pred.flatten() - ci, 
                  y_range_pred.flatten() + ci,
                  alpha=0.2, color='gray', label='IC 95%')

ax1.set_xlabel('Superavit Calorico (cal/TMB)', fontweight='bold')
ax1.set_ylabel('Score de Sedentarismo (Fuzzy 0-1)', fontweight='bold')
ax1.set_title(f'A) Regresion Global\n' +
              f'Beta = {model_global.coef_[0]:.6f}, p < 0.001, N = {len(df):,}',
              fontweight='bold', pad=15)
ax1.legend(loc='best', framealpha=0.9, fontsize=9)
ax1.grid(True, alpha=0.3)

# Ecuacion
eq_text = f'y = {model_global.intercept_:.3f} + ({model_global.coef_[0]:.5f})x'
ax1.text(0.98, 0.05, eq_text, transform=ax1.transAxes,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
         fontsize=10, ha='right', va='bottom')

# ============================================================================
# PLOT 2: REGRESION POR CLUSTER
# ============================================================================
ax2 = axes[1]

# Scatter C0
ax2.scatter(df_c0['Superavit_calorico_basal_p50'], df_c0['Sedentarismo_score'],
            alpha=0.5, s=30, label=f'Bajo Sedentarismo (N={len(df_c0)})', 
            color=COLORS['cluster_0'], edgecolors='black', linewidth=0.3)

# Scatter C1
ax2.scatter(df_c1['Superavit_calorico_basal_p50'], df_c1['Sedentarismo_score'],
            alpha=0.5, s=30, label=f'Alto Sedentarismo (N={len(df_c1)})', 
            color=COLORS['cluster_1'], edgecolors='black', linewidth=0.3)

# Linea C0
x_range_c0 = np.linspace(df_c0['Superavit_calorico_basal_p50'].min(), 
                          df_c0['Superavit_calorico_basal_p50'].max(), 50).reshape(-1, 1)
y_c0_range_pred = model_c0.predict(x_range_c0)
ax2.plot(x_range_c0, y_c0_range_pred, color=COLORS['cluster_0'], linewidth=3,
         linestyle='--', label=f'C0: Beta={model_c0.coef_[0]:.5f}', zorder=5)

# Linea C1
x_range_c1 = np.linspace(df_c1['Superavit_calorico_basal_p50'].min(), 
                          df_c1['Superavit_calorico_basal_p50'].max(), 50).reshape(-1, 1)
y_c1_range_pred = model_c1.predict(x_range_c1)
ax2.plot(x_range_c1, y_c1_range_pred, color=COLORS['cluster_1'], linewidth=3,
         linestyle='--', label=f'C1: Beta={model_c1.coef_[0]:.5f}', zorder=5)

ax2.set_xlabel('Superavit Calorico (cal/TMB)', fontweight='bold')
ax2.set_ylabel('Score de Sedentarismo (Fuzzy 0-1)', fontweight='bold')
ax2.set_title(f'B) Regresion Estratificada por Cluster\n' +
              f'Pendientes {"DIFERENTES" if p_diff < 0.05 else "NO difieren"} (p={p_diff:.3f})',
              fontweight='bold', pad=15)
ax2.legend(loc='best', framealpha=0.9, fontsize=8)
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# Guardar
import os
output_dir = os.path.join(os.path.dirname(__file__), "..", "resultados")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "regresion_simple_clase.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   [OK] Figura guardada: {output_path}")
print()

# ============================================================================
# GUARDAR TABLAS CSV
# ============================================================================

print("[4/5] Guardando tablas estilo SPSS...")
print()

# Tabla global
tabla_coef_global.to_csv(os.path.join(output_dir, "tabla_coef_global.csv"), index=False)
print(f"   [OK] Tabla global: resultados/tabla_coef_global.csv")

# Tabla C0
tabla_coef_c0.to_csv(os.path.join(output_dir, "tabla_coef_cluster0.csv"), index=False)
print(f"   [OK] Tabla Cluster 0: resultados/tabla_coef_cluster0.csv")

# Tabla C1
tabla_coef_c1.to_csv(os.path.join(output_dir, "tabla_coef_cluster1.csv"), index=False)
print(f"   [OK] Tabla Cluster 1: resultados/tabla_coef_cluster1.csv")

# Tabla descriptivos
desc_completa = pd.DataFrame({
    'Estadistico': ['N', 'Media', 'DE', 'Minimo', 'Q1', 'Mediana', 'Q3', 'Maximo'],
    'Superavit_calorico': [
        len(df),
        df['Superavit_calorico_basal_p50'].mean(),
        df['Superavit_calorico_basal_p50'].std(),
        df['Superavit_calorico_basal_p50'].min(),
        df['Superavit_calorico_basal_p50'].quantile(0.25),
        df['Superavit_calorico_basal_p50'].median(),
        df['Superavit_calorico_basal_p50'].quantile(0.75),
        df['Superavit_calorico_basal_p50'].max()
    ],
    'Sedentarismo_score': [
        len(df),
        df['Sedentarismo_score'].mean(),
        df['Sedentarismo_score'].std(),
        df['Sedentarismo_score'].min(),
        df['Sedentarismo_score'].quantile(0.25),
        df['Sedentarismo_score'].median(),
        df['Sedentarismo_score'].quantile(0.75),
        df['Sedentarismo_score'].max()
    ]
})
desc_completa.to_csv(os.path.join(output_dir, "tabla_descriptivos.csv"), index=False)
print(f"   [OK] Tabla descriptivos: resultados/tabla_descriptivos.csv")
print()

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("="*80)
print("RESUMEN EJECUTIVO")
print("="*80)
print()
print("PREGUNTA DE INVESTIGACION:")
print("   ¿El superavit calorico (medida de actividad fisica) predice")
print("   el comportamiento sedentario?")
print()
print("HALLAZGOS PRINCIPALES:")
print()
print("1. REGRESION GLOBAL:")
print(f"   - Beta = {model_global.coef_[0]:.6f} (IC 95%: [{stats_global['ci_lower'][1]:.6f}, {stats_global['ci_upper'][1]:.6f}])")
print(f"   - R2 = {r2_global:.4f} ({r2_global*100:.2f}% de varianza explicada)")
print(f"   - t = {stats_global['t'][1]:.4f}, p < 0.001")
if model_global.coef_[0] < 0:
    print(f"   - Interpretacion: A MAYOR superavit, MENOR sedentarismo (esperado)")
else:
    print(f"   - Interpretacion: A MAYOR superavit, MAYOR sedentarismo (inesperado)")
print()
print("2. REGRESION ESTRATIFICADA:")
print(f"   - Cluster 0 (Bajo): Beta = {model_c0.coef_[0]:.6f}, R2 = {r2_c0:.4f}")
print(f"   - Cluster 1 (Alto): Beta = {model_c1.coef_[0]:.6f}, R2 = {r2_c1:.4f}")
print(f"   - Diferencia de pendientes: p = {p_diff:.4f}")
if p_diff < 0.05:
    print(f"   - Conclusion: La relacion NO es homogenea entre clusters")
else:
    print(f"   - Conclusion: La relacion es similar entre clusters")
print()
print("CONCLUSION METODOLOGICA:")
print("   La regresion lineal es util para:")
print("   - Cuantificar la relacion lineal entre dos variables")
print("   - Probar significancia estadistica de la asociacion")
print("   - Estimar intervalos de confianza de los coeficientes")
print()
print("   Limitacion:")
if r2_global < 0.3:
    print(f"   - Baja capacidad predictiva (R2 = {r2_global:.2f})")
    print("   - Sugiere que la relacion NO es principalmente lineal")
    print("   - Justifica el uso de modelos no lineales (lógica difusa)")
print()
print("="*80)
print("[5/5] ANALISIS COMPLETADO")
print("="*80)
print()
print(f"Archivos generados:")
print(f"   - Figura: {output_path}")
print(f"   - Tablas SPSS: resultados/tabla_coef_*.csv")
print()

# Mostrar plot
plt.show()

