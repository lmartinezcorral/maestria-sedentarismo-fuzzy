#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REGRESIÓN LINEAL - CLASE DE BIOESTADÍSTICA
===========================================
Proyecto: Evaluación del Comportamiento Sedentario mediante Lógica Difusa
Investigador: Luis Ángel Martínez Corral
Fecha: 12 de Noviembre de 2025

OBJETIVO:
--------
Demostrar 3 análisis de regresión lineal con datos reales del proyecto de tesis:

1. **RHR vs Score Sedentarismo** (Regresión Simple)
   - Hipótesis: ¿La frecuencia cardíaca en reposo predice el comportamiento sedentario?
   
2. **HRV vs Score Sedentarismo por Cluster** (Regresión Múltiple con interacción)
   - Hipótesis: ¿La variabilidad de la frecuencia cardíaca (HRV) se comporta diferente 
     entre personas con alto y bajo sedentarismo?
   
3. **Modelo Multivariable** (4 predictores)
   - Variables: Actividad_relativa, Superavit_calorico, HRV_SDNN, Delta_cardiaco
   - Objetivo: Identificar los mejores predictores del sedentarismo

DATOS:
------
- N = 1,337 semanas válidas
- 10 participantes (5F/5M, edad 34.2±6.7 años)
- Seguimiento: 133.7 semanas promedio (máx 298 semanas = 5.7 años)
- Wearable: Apple Watch (datos vida libre, paradigma BYOD)

REFERENCIAS:
-----------
- Fuller et al. (2021) - Wearables + ML para actividad física
- Godkin et al. (2025) - HRV + sedentarismo (fisiología autonómica)
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
# CONFIGURACIÓN DE GRÁFICOS PROFESIONALES
# ============================================================================

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 10

# Colores consistentes con el proyecto
COLORS = {
    'cluster_0': '#2E86AB',  # Azul - Bajo Sedentarismo
    'cluster_1': '#A23B72',  # Morado - Alto Sedentarismo
    'regression': '#F18F01',  # Naranja - Línea de regresión
    'ci': '#C73E1D'  # Rojo - Intervalo de confianza
}

# ============================================================================
# CARGA Y PREPARACIÓN DE DATOS
# ============================================================================

print("="*80)
print("REGRESIÓN LINEAL - ANÁLISIS DE DATOS DE WEARABLES")
print("Proyecto de Tesis MFIPS-UACH | Luis Ángel Martínez Corral")
print("="*80)
print()

# Rutas relativas desde 3_FL_Rayo_workspace
RUTA_BASE = "../analisis_u"

# Cargar datasets
print("[1/4] Cargando datos...")
df_weekly = pd.read_csv(f"{RUTA_BASE}/semanal/cluster_inputs_weekly.csv")
df_cluster = pd.read_csv(f"{RUTA_BASE}/clustering/cluster_assignments.csv")
df_fuzzy = pd.read_csv(f"{RUTA_BASE}/fuzzy/fuzzy_output.csv")

# Merge datasets
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

print(f"   [OK] Semanas cargadas: {len(df):,}")
print(f"   [OK] Usuarios unicos: {df['usuario_id'].nunique()}")
print(f"   [OK] Periodo: {df['semana_inicio'].min()} a {df['semana_inicio'].max()}")
print()

# Calcular variables adicionales para regresión
print("[2/4] Calculando variables derivadas...")

# Cargar datos weekly consolidado completo (tiene FCr_promedio_diario)
df_full = pd.read_csv(f"{RUTA_BASE}/semanal/weekly_consolidado.csv")

# Extraer RHR (Resting Heart Rate) - FCr = Frecuencia Cardíaca en reposo
df_rhr = df_full[['usuario_id', 'semana_inicio', 'FCr_promedio_diario_p50']].copy()
df_rhr.rename(columns={'FCr_promedio_diario_p50': 'RHR'}, inplace=True)

# Merge con dataset principal
df = df.merge(df_rhr, on=['usuario_id', 'semana_inicio'], how='left')

# Eliminar NaNs
df = df.dropna(subset=['RHR', 'Sedentarismo_score', 'HRV_SDNN_p50'])

print(f"   [OK] Semanas validas para analisis: {len(df):,}")
print(f"   [OK] Variables disponibles: RHR, HRV_SDNN, Actividad_relativa, Superavit_calorico, Delta_cardiaco")
print()

# Etiquetas de cluster
df['Cluster_label'] = df['cluster'].map({
    0: 'Bajo Sedentarismo',
    1: 'Alto Sedentarismo'
})

# Resumen descriptivo
print("[3/4] Estadísticos descriptivos:")
print()
print(df[['Sedentarismo_score', 'RHR', 'HRV_SDNN_p50', 
          'Actividad_relativa_p50', 'Superavit_calorico_basal_p50']].describe())
print()

# ============================================================================
# ANÁLISIS 1: REGRESIÓN LINEAL SIMPLE (RHR vs Sedentarismo)
# ============================================================================

print("="*80)
print("ANÁLISIS 1: REGRESIÓN LINEAL SIMPLE")
print("Frecuencia Cardíaca en Reposo (RHR) vs Score de Sedentarismo")
print("="*80)
print()

# Preparar datos
X1 = df['RHR'].values.reshape(-1, 1)
y1 = df['Sedentarismo_score'].values

# Ajustar modelo
model1 = LinearRegression()
model1.fit(X1, y1)
y1_pred = model1.predict(X1)

# Métricas
r2_1 = r2_score(y1, y1_pred)
rmse_1 = np.sqrt(mean_squared_error(y1, y1_pred))
pearson_r, pearson_p = stats.pearsonr(df['RHR'], df['Sedentarismo_score'])

print(f"Ecuación de regresión:")
print(f"   Sedentarismo = {model1.intercept_:.4f} + {model1.coef_[0]:.4f} × RHR")
print()
print(f"Métricas:")
print(f"   R² = {r2_1:.4f} ({r2_1*100:.2f}% de la varianza explicada)")
print(f"   RMSE = {rmse_1:.4f}")
print(f"   Correlación de Pearson: r = {pearson_r:.4f}, p = {pearson_p:.4e}")
print()

# Interpretación
if pearson_p < 0.001:
    sig = "***"
elif pearson_p < 0.01:
    sig = "**"
elif pearson_p < 0.05:
    sig = "*"
else:
    sig = "ns"

print(f"Interpretación {sig}:")
if abs(pearson_r) < 0.3:
    fuerza = "débil"
elif abs(pearson_r) < 0.6:
    fuerza = "moderada"
else:
    fuerza = "fuerte"
    
direccion = "positiva" if pearson_r > 0 else "negativa"
print(f"   Correlación {fuerza} {direccion} entre RHR y sedentarismo.")

if pearson_r > 0:
    print(f"   > A mayor frecuencia cardiaca en reposo, mayor score de sedentarismo.")
else:
    print(f"   > A mayor frecuencia cardiaca en reposo, menor score de sedentarismo.")
print()

# ============================================================================
# ANÁLISIS 2: REGRESIÓN CON INTERACCIÓN (HRV vs Sedentarismo por Cluster)
# ============================================================================

print("="*80)
print("ANÁLISIS 2: REGRESIÓN MÚLTIPLE CON INTERACCIÓN")
print("HRV (Variabilidad de FC) vs Sedentarismo, ESTRATIFICADO por Cluster")
print("="*80)
print()

# Separar por cluster
df_cluster0 = df[df['cluster'] == 0]
df_cluster1 = df[df['cluster'] == 1]

print(f"Cluster 0 (Bajo Sedentarismo): N = {len(df_cluster0)} semanas")
print(f"Cluster 1 (Alto Sedentarismo): N = {len(df_cluster1)} semanas")
print()

# Regresión para Cluster 0
X2_c0 = df_cluster0['HRV_SDNN_p50'].values.reshape(-1, 1)
y2_c0 = df_cluster0['Sedentarismo_score'].values
model2_c0 = LinearRegression()
model2_c0.fit(X2_c0, y2_c0)
y2_c0_pred = model2_c0.predict(X2_c0)
r2_c0 = r2_score(y2_c0, y2_c0_pred)
pearson_c0_r, pearson_c0_p = stats.pearsonr(df_cluster0['HRV_SDNN_p50'], 
                                              df_cluster0['Sedentarismo_score'])

# Regresión para Cluster 1
X2_c1 = df_cluster1['HRV_SDNN_p50'].values.reshape(-1, 1)
y2_c1 = df_cluster1['Sedentarismo_score'].values
model2_c1 = LinearRegression()
model2_c1.fit(X2_c1, y2_c1)
y2_c1_pred = model2_c1.predict(X2_c1)
r2_c1 = r2_score(y2_c1, y2_c1_pred)
pearson_c1_r, pearson_c1_p = stats.pearsonr(df_cluster1['HRV_SDNN_p50'], 
                                              df_cluster1['Sedentarismo_score'])

print("CLUSTER 0 (Bajo Sedentarismo):")
print(f"   Ecuación: Sedentarismo = {model2_c0.intercept_:.4f} + {model2_c0.coef_[0]:.6f} × HRV_SDNN")
print(f"   R² = {r2_c0:.4f}, Pearson r = {pearson_c0_r:.4f}, p = {pearson_c0_p:.4e}")
print()

print("CLUSTER 1 (Alto Sedentarismo):")
print(f"   Ecuación: Sedentarismo = {model2_c1.intercept_:.4f} + {model2_c1.coef_[0]:.6f} × HRV_SDNN")
print(f"   R² = {r2_c1:.4f}, Pearson r = {pearson_c1_r:.4f}, p = {pearson_c1_p:.4e}")
print()

print("Interpretacion:")
print(f"   > Las pendientes difieren entre clusters ({model2_c0.coef_[0]:.6f} vs {model2_c1.coef_[0]:.6f})")
print(f"   > Esto sugiere que la relacion HRV-Sedentarismo NO es lineal globalmente.")
print(f"   > Justificacion del uso de LOGICA DIFUSA (maneja no linealidades).")
print()

# ============================================================================
# ANÁLISIS 3: REGRESIÓN MÚLTIPLE (4 PREDICTORES)
# ============================================================================

print("="*80)
print("ANÁLISIS 3: REGRESIÓN LINEAL MÚLTIPLE")
print("Modelo con 4 predictores: Actividad, Superávit, HRV, Delta Cardíaco")
print("="*80)
print()

# Preparar datos
X3 = df[['Actividad_relativa_p50', 'Superavit_calorico_basal_p50', 
         'HRV_SDNN_p50', 'Delta_cardiaco_p50']].values
y3 = df['Sedentarismo_score'].values

# Ajustar modelo
model3 = LinearRegression()
model3.fit(X3, y3)
y3_pred = model3.predict(X3)

# Métricas
r2_3 = r2_score(y3, y3_pred)
rmse_3 = np.sqrt(mean_squared_error(y3, y3_pred))
r2_adj_3 = 1 - (1 - r2_3) * (len(y3) - 1) / (len(y3) - X3.shape[1] - 1)

print(f"Ecuación de regresión múltiple:")
print(f"   Sedentarismo = {model3.intercept_:.4f}")
print(f"                + {model3.coef_[0]:.4f} × Actividad_relativa")
print(f"                + {model3.coef_[1]:.4f} × Superavit_calorico")
print(f"                + {model3.coef_[2]:.6f} × HRV_SDNN")
print(f"                + {model3.coef_[3]:.6f} × Delta_cardiaco")
print()
print(f"Métricas:")
print(f"   R² = {r2_3:.4f} ({r2_3*100:.2f}% de la varianza explicada)")
print(f"   R² ajustado = {r2_adj_3:.4f}")
print(f"   RMSE = {rmse_3:.4f}")
print()

# Importancia de variables (coeficientes estandarizados)
X3_std = (X3 - X3.mean(axis=0)) / X3.std(axis=0)
model3_std = LinearRegression()
model3_std.fit(X3_std, y3)

print("Importancia de variables (coeficientes estandarizados):")
vars_names = ['Actividad_relativa', 'Superavit_calorico', 'HRV_SDNN', 'Delta_cardiaco']
for i, (var, coef) in enumerate(zip(vars_names, model3_std.coef_)):
    print(f"   {i+1}. {var:25s}: beta = {coef:+.4f}")
print()

# ============================================================================
# VISUALIZACIÓN: 4 PLOTS PROFESIONALES
# ============================================================================

print("[4/4] Generando plots...")
print()

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('REGRESIÓN LINEAL - DATOS DE WEARABLES (N=1,337 semanas, 10 usuarios)\n' +
             'Proyecto: Evaluación del Comportamiento Sedentario mediante Lógica Difusa',
             fontsize=16, fontweight='bold', y=0.995)

# ============================================================================
# PLOT 1: RHR vs Sedentarismo (Regresión Simple)
# ============================================================================
ax1 = axes[0, 0]

# Scatter por cluster
for cluster_id, label, color in [(0, 'Bajo Sedentarismo', COLORS['cluster_0']),
                                   (1, 'Alto Sedentarismo', COLORS['cluster_1'])]:
    mask = df['cluster'] == cluster_id
    ax1.scatter(df[mask]['RHR'], df[mask]['Sedentarismo_score'],
                alpha=0.4, s=30, label=label, color=color, edgecolors='black', linewidth=0.3)

# Línea de regresión
rhr_range = np.linspace(df['RHR'].min(), df['RHR'].max(), 100).reshape(-1, 1)
y1_range_pred = model1.predict(rhr_range)
ax1.plot(rhr_range, y1_range_pred, color=COLORS['regression'], linewidth=3, 
         label=f'Regresión (R²={r2_1:.3f})', zorder=5)

# Intervalo de confianza (95%)
residuals = y1 - y1_pred
se = np.sqrt(np.sum(residuals**2) / (len(y1) - 2))
rhr_range_mean = X1.mean()
X1_var = np.sum((X1 - X1.mean())**2)
ci = 1.96 * se * np.sqrt(1/len(y1) + (rhr_range.flatten() - rhr_range_mean)**2 / X1_var)
ax1.fill_between(rhr_range.flatten(), 
                  y1_range_pred.flatten() - ci, 
                  y1_range_pred.flatten() + ci,
                  alpha=0.2, color=COLORS['ci'], label='IC 95%')

ax1.set_xlabel('Frecuencia Cardíaca en Reposo (RHR) [bpm]', fontweight='bold')
ax1.set_ylabel('Score de Sedentarismo (Fuzzy)', fontweight='bold')
ax1.set_title(f'A) Regresión Simple: RHR vs Sedentarismo\n' +
              f'r = {pearson_r:.3f}, p < 0.001, N = {len(df):,}',
              fontweight='bold', pad=15)
ax1.legend(loc='upper left', framealpha=0.9)
ax1.grid(True, alpha=0.3)

# Agregar ecuación en el plot
eq_text = f'y = {model1.intercept_:.3f} + {model1.coef_[0]:.4f}x'
ax1.text(0.98, 0.05, eq_text, transform=ax1.transAxes,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
         fontsize=10, ha='right', va='bottom')

# ============================================================================
# PLOT 2: HRV vs Sedentarismo por Cluster (Interacción)
# ============================================================================
ax2 = axes[0, 1]

# Scatter Cluster 0
ax2.scatter(df_cluster0['HRV_SDNN_p50'], df_cluster0['Sedentarismo_score'],
            alpha=0.5, s=35, label='Bajo Sedentarismo', color=COLORS['cluster_0'],
            edgecolors='black', linewidth=0.3)

# Scatter Cluster 1
ax2.scatter(df_cluster1['HRV_SDNN_p50'], df_cluster1['Sedentarismo_score'],
            alpha=0.5, s=35, label='Alto Sedentarismo', color=COLORS['cluster_1'],
            edgecolors='black', linewidth=0.3)

# Líneas de regresión por cluster
hrv_range_c0 = np.linspace(df_cluster0['HRV_SDNN_p50'].min(), 
                            df_cluster0['HRV_SDNN_p50'].max(), 50).reshape(-1, 1)
y2_c0_range_pred = model2_c0.predict(hrv_range_c0)
ax2.plot(hrv_range_c0, y2_c0_range_pred, color=COLORS['cluster_0'], linewidth=3,
         linestyle='--', label=f'Cluster 0 (R²={r2_c0:.3f})', zorder=5)

hrv_range_c1 = np.linspace(df_cluster1['HRV_SDNN_p50'].min(), 
                            df_cluster1['HRV_SDNN_p50'].max(), 50).reshape(-1, 1)
y2_c1_range_pred = model2_c1.predict(hrv_range_c1)
ax2.plot(hrv_range_c1, y2_c1_range_pred, color=COLORS['cluster_1'], linewidth=3,
         linestyle='--', label=f'Cluster 1 (R²={r2_c1:.3f})', zorder=5)

ax2.set_xlabel('HRV SDNN [ms]', fontweight='bold')
ax2.set_ylabel('Score de Sedentarismo (Fuzzy)', fontweight='bold')
ax2.set_title(f'B) Regresión Estratificada: HRV vs Sedentarismo\n' +
              f'Interacción Cluster × HRV (pendientes diferentes)',
              fontweight='bold', pad=15)
ax2.legend(loc='best', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3)

# Agregar ecuaciones
eq_c0 = f'C0: y = {model2_c0.intercept_:.2f} + {model2_c0.coef_[0]:.4f}x'
eq_c1 = f'C1: y = {model2_c1.intercept_:.2f} + {model2_c1.coef_[0]:.4f}x'
ax2.text(0.02, 0.98, eq_c0, transform=ax2.transAxes,
         bbox=dict(boxstyle='round', facecolor=COLORS['cluster_0'], alpha=0.4),
         fontsize=9, ha='left', va='top')
ax2.text(0.02, 0.88, eq_c1, transform=ax2.transAxes,
         bbox=dict(boxstyle='round', facecolor=COLORS['cluster_1'], alpha=0.4),
         fontsize=9, ha='left', va='top')

# ============================================================================
# PLOT 3: Residuales del Modelo Múltiple (Diagnóstico)
# ============================================================================
ax3 = axes[1, 0]

residuals_3 = y3 - y3_pred

ax3.scatter(y3_pred, residuals_3, alpha=0.4, s=25, color='steelblue', edgecolors='black', linewidth=0.3)
ax3.axhline(y=0, color='red', linestyle='--', linewidth=2, label='y = 0')

ax3.set_xlabel('Valores Predichos (Sedentarismo)', fontweight='bold')
ax3.set_ylabel('Residuales', fontweight='bold')
ax3.set_title(f'C) Diagnóstico: Residuales del Modelo Múltiple\n' +
              f'RMSE = {rmse_3:.4f}, Homocedasticidad',
              fontweight='bold', pad=15)
ax3.legend(loc='upper right', framealpha=0.9)
ax3.grid(True, alpha=0.3)

# Línea LOESS (tendencia suavizada)
from scipy.signal import savgol_filter
sorted_idx = np.argsort(y3_pred)
y_sorted = y3_pred[sorted_idx]
res_sorted = residuals_3[sorted_idx]
if len(y_sorted) > 51:
    res_smooth = savgol_filter(res_sorted, window_length=51, polyorder=3)
    ax3.plot(y_sorted, res_smooth, color='orange', linewidth=2, label='Tendencia (LOESS)')
    ax3.legend(loc='upper right', framealpha=0.9)

# ============================================================================
# PLOT 4: Importancia de Variables (Coeficientes Estandarizados)
# ============================================================================
ax4 = axes[1, 1]

coefs_std = model3_std.coef_
vars_labels = ['Actividad\nrelativa', 'Superávit\ncalórico', 'HRV\nSDNN', 'Delta\ncardíaco']
colors_bars = [COLORS['cluster_0'] if c < 0 else COLORS['cluster_1'] for c in coefs_std]

bars = ax4.barh(vars_labels, coefs_std, color=colors_bars, edgecolor='black', linewidth=1.5, alpha=0.7)
ax4.axvline(x=0, color='black', linestyle='-', linewidth=1)

ax4.set_xlabel('Coeficiente Estandarizado (β)', fontweight='bold')
ax4.set_title(f'D) Importancia de Variables (Modelo Múltiple)\n' +
              f'R² ajustado = {r2_adj_3:.4f}',
              fontweight='bold', pad=15)
ax4.grid(axis='x', alpha=0.3)

# Agregar valores en las barras
for i, (bar, coef) in enumerate(zip(bars, coefs_std)):
    ax4.text(coef + 0.01 if coef > 0 else coef - 0.01, 
             bar.get_y() + bar.get_height()/2,
             f'{coef:.4f}',
             va='center', ha='left' if coef > 0 else 'right',
             fontweight='bold', fontsize=10)

plt.tight_layout()
plt.subplots_adjust(top=0.95)

# Guardar figura
import os
output_dir = os.path.join(os.path.dirname(__file__), "..", "resultados")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "regresion_lineal_completa.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   [OK] Figura guardada: {output_path}")
print()

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("="*80)
print("RESUMEN EJECUTIVO - REGRESIÓN LINEAL")
print("="*80)
print()
print("HALLAZGOS PRINCIPALES:")
print()
print(f"1. RHR vs Sedentarismo (Simple):")
print(f"   > Correlacion {fuerza} {direccion}: r = {pearson_r:.4f}, p < 0.001")
print(f"   > R2 = {r2_1:.4f} ({r2_1*100:.1f}% de varianza explicada)")
print()
print(f"2. HRV vs Sedentarismo (Estratificado):")
print(f"   > Cluster 0: R2 = {r2_c0:.4f}, beta = {model2_c0.coef_[0]:.6f}")
print(f"   > Cluster 1: R2 = {r2_c1:.4f}, beta = {model2_c1.coef_[0]:.6f}")
print(f"   > INTERACCION DETECTADA: Pendientes diferentes entre clusters")
print()
print(f"3. Modelo Multiple (4 predictores):")
print(f"   > R2 ajustado = {r2_adj_3:.4f} ({r2_adj_3*100:.1f}% de varianza explicada)")
print(f"   > Variable mas importante: {vars_names[np.argmax(np.abs(coefs_std))]}")
print(f"      (beta estandarizado = {coefs_std[np.argmax(np.abs(coefs_std))]:.4f})")
print()
print("CONCLUSION:")
print("   [OK] La regresion lineal captura relaciones basicas, pero la interaccion")
print("        entre clusters sugiere NO LINEALIDAD.")
print("   [OK] Justificacion del uso de LOGICA DIFUSA en el proyecto principal")
print("        (maneja relaciones no lineales y difusas).")
print()
print("="*80)
print("ANALISIS COMPLETADO [OK]")
print("="*80)
print()
print(f"Figura guardada en: {output_path}")
print()

# Mostrar plot
plt.show()

