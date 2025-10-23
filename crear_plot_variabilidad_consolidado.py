"""
crear_plot_variabilidad_consolidado.py
=======================================

OBJETIVO:
---------
Generar visualizaciones consolidadas de variabilidad que muestren:
1) Variabilidad OPERATIVA (entre usuarios)
2) Variabilidad OBSERVADA (dentro de cada usuario)

Esto apoya la justificación metodológica de usar variabilidad dual.

INSUMOS:
--------
- analisis_u/variabilidad_dual/variabilidad_dual_consolidado.csv
- DB_final_v3_u{1..10}.csv

SALIDAS:
--------
- analisis_u/variabilidad_dual/plots_consolidados/
  - variabilidad_operativa_vs_observada.png
  - variabilidad_por_usuario_boxplot.png
  - resumen_variabilidad_consolidado.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_DIR = Path(__file__).parent.resolve()
VARIABILIDAD_FILE = BASE_DIR / 'analisis_u' / 'comparativo_variabilidad.csv'
OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'variabilidad_dual' / 'plots_consolidados'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Variables clave para análisis
VARIABLES_CLAVE = [
    'HRV_SDNN', 'FCr_promedio_diario', 'FC_al_caminar_promedio_diario',
    'Numero_pasos_por_dia', 'Gasto_calorico_activo', 'Total_min_de_ejercicio_diario'
]

USER_ALIASES = {
    'u1': 'Ale', 'u2': 'Brenda', 'u3': 'Christina', 'u4': 'Edson',
    'u5': 'Esmeralda', 'u6': 'Fidel', 'u7': 'Kevin', 'u8': 'Legarda',
    'u9': 'LMartinez', 'u10': 'Vane'
}

print("="*80)
print("GENERACIÓN DE PLOTS CONSOLIDADOS DE VARIABILIDAD")
print("="*80)
print(f"Archivo de entrada: {VARIABILIDAD_FILE.name}")
print(f"Directorio de salida: {OUTPUT_DIR}")
print("")

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================

print("📊 Cargando datos de variabilidad dual...")
if not VARIABILIDAD_FILE.exists():
    print(f"❌ ERROR: No se encontró {VARIABILIDAD_FILE}")
    exit(1)

df = pd.read_csv(VARIABILIDAD_FILE)

# Extraer usuario de la columna 'archivo' (p.ej., 'DB_final_v3_u1' → 'u1')
df['usuario'] = df['archivo'].str.extract(r'(u\d+)')[0]

print(f"✅ Datos cargados: {len(df)} registros")
print(f"   Variables: {df['variable'].nunique()}")
print(f"   Usuarios: {df['usuario'].nunique()}")
print("")

# Filtrar variables clave si existen
df_filtrado = df[df['variable'].isin(VARIABLES_CLAVE)].copy()
if len(df_filtrado) == 0:
    print("⚠️  Variables clave no encontradas, usando todas las variables")
    df_filtrado = df.copy()

# ============================================================================
# 2. CALCULAR VARIABILIDAD OPERATIVA (ENTRE USUARIOS)
# ============================================================================

print("🔍 Calculando variabilidad operativa (entre usuarios)...")

# Para cada variable, calcular CV de las medianas entre usuarios
variabilidad_operativa = []

for var in df_filtrado['variable'].unique():
    df_var = df_filtrado[df_filtrado['variable'] == var]

    # Mediana por usuario
    medianas_usuarios = df_var.groupby('usuario')['median'].median()

    # CV operativo = std(medianas) / mean(medianas)
    cv_operativo = medianas_usuarios.std(
    ) / medianas_usuarios.mean() if medianas_usuarios.mean() != 0 else np.nan

    # CV observado promedio (ya calculado en comparativo_variabilidad)
    cv_observado_mean = df_var['cv'].mean()

    variabilidad_operativa.append({
        'variable': var,
        'cv_operativo': cv_operativo,
        'cv_observado_mean': cv_observado_mean,
        'n_usuarios': len(medianas_usuarios),
        'mediana_global': medianas_usuarios.median(),
        'ratio_oper_obs': cv_operativo / cv_observado_mean if cv_observado_mean > 0 else np.nan
    })

df_oper = pd.DataFrame(variabilidad_operativa)
df_oper = df_oper.sort_values('ratio_oper_obs', ascending=False)

# Guardar resumen
resumen_path = OUTPUT_DIR / 'resumen_variabilidad_consolidado.csv'
df_oper.to_csv(resumen_path, index=False)
print(f"✅ Guardado: {resumen_path.name}")
print("")

# ============================================================================
# 3. PLOT 1: VARIABILIDAD OPERATIVA VS OBSERVADA
# ============================================================================

print("📈 Generando Plot 1: Variabilidad Operativa vs Observada...")

fig, ax = plt.subplots(figsize=(14, 8))

# Barras agrupadas
x = np.arange(len(df_oper))
width = 0.35

bars1 = ax.bar(x - width/2, df_oper['cv_operativo'], width,
               label='Variabilidad Operativa (entre usuarios)',
               color='steelblue', alpha=0.8)
bars2 = ax.bar(x + width/2, df_oper['cv_observado_mean'], width,
               label='Variabilidad Observada (intra-usuario, promedio)',
               color='coral', alpha=0.8)

# Línea de ratio
ax2 = ax.twinx()
line = ax2.plot(x, df_oper['ratio_oper_obs'], 'o-', color='green',
                linewidth=2, markersize=8, label='Ratio Oper/Obs')
ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Configuración de ejes
ax.set_xlabel('Variable', fontsize=12, fontweight='bold')
ax.set_ylabel('Coeficiente de Variación (CV)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Ratio CV_oper / CV_obs', fontsize=12,
               fontweight='bold', color='green')
ax.set_title('Variabilidad Operativa vs Observada\n(Justificación de Variabilidad Dual)',
             fontsize=14, fontweight='bold', pad=20)

ax.set_xticks(x)
ax.set_xticklabels(df_oper['variable'], rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3)

# Leyendas
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=10)

# Anotaciones
for i, row in df_oper.iterrows():
    if not np.isnan(row['ratio_oper_obs']):
        ax2.text(i, row['ratio_oper_obs'] + 0.1, f"{row['ratio_oper_obs']:.2f}",
                 ha='center', fontsize=9, color='green', fontweight='bold')

plt.tight_layout()
plot1_path = OUTPUT_DIR / 'variabilidad_operativa_vs_observada.png'
fig.savefig(plot1_path, dpi=150)
plt.close(fig)
print(f"✅ Guardado: {plot1_path.name}")
print("")

# ============================================================================
# 4. PLOT 2: BOXPLOT DE VARIABILIDAD POR USUARIO
# ============================================================================

print("📈 Generando Plot 2: Boxplot de Variabilidad por Usuario...")

# Seleccionar top 6 variables con mayor ratio
top_vars = df_oper.nlargest(6, 'ratio_oper_obs')['variable'].tolist()
df_plot = df_filtrado[df_filtrado['variable'].isin(top_vars)].copy()

# Crear alias de usuario
df_plot['usuario_alias'] = df_plot['usuario'].map(USER_ALIASES)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for idx, var in enumerate(top_vars):
    ax = axes[idx]
    df_var = df_plot[df_plot['variable'] == var]

    # Boxplot por usuario
    usuarios = sorted(df_var['usuario'].unique())
    data_to_plot = [df_var[df_var['usuario'] == u]
                    ['cv'].values for u in usuarios]
    aliases = [USER_ALIASES.get(u, u) for u in usuarios]

    bp = ax.boxplot(data_to_plot, labels=aliases, patch_artist=True,
                    boxprops=dict(facecolor='lightblue', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2))

    ax.set_title(f'{var}', fontsize=11, fontweight='bold')
    ax.set_ylabel('CV (intra-usuario)', fontsize=10)
    ax.set_xlabel('Usuario', fontsize=10)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)

    # Línea de CV operativo
    cv_oper = df_oper[df_oper['variable'] == var]['cv_operativo'].values[0]
    if not np.isnan(cv_oper):
        ax.axhline(y=cv_oper, color='orange', linestyle='--', linewidth=2,
                   label=f'CV operativo: {cv_oper:.2f}')
        ax.legend(fontsize=8, loc='upper right')

plt.suptitle('Variabilidad Observada por Usuario vs Variabilidad Operativa\n(Top 6 variables con mayor heterogeneidad)',
             fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plot2_path = OUTPUT_DIR / 'variabilidad_por_usuario_boxplot.png'
fig.savefig(plot2_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"✅ Guardado: {plot2_path.name}")
print("")

# ============================================================================
# 5. PLOT 3: HEATMAP DE CV POR USUARIO Y VARIABLE
# ============================================================================

print("📈 Generando Plot 3: Heatmap de CV por Usuario y Variable...")

# Preparar matriz (usuarios x variables)
pivot_cv = df_filtrado.pivot_table(
    index='usuario', columns='variable', values='cv', aggfunc='mean')

# Ordenar por alias
pivot_cv.index = pivot_cv.index.map(lambda x: USER_ALIASES.get(x, x))
pivot_cv = pivot_cv.sort_index()

fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(pivot_cv, annot=True, fmt=".2f", cmap='YlOrRd', cbar_kws={'label': 'CV'},
            linewidths=0.5, ax=ax, vmin=0, vmax=pivot_cv.max().max())
ax.set_title('Coeficiente de Variación (CV) por Usuario y Variable\n(Variabilidad Observada Intra-Usuario)',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Variable', fontsize=12, fontweight='bold')
ax.set_ylabel('Usuario', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plot3_path = OUTPUT_DIR / 'heatmap_cv_usuario_variable.png'
fig.savefig(plot3_path, dpi=150)
plt.close(fig)
print(f"✅ Guardado: {plot3_path.name}")
print("")

# ============================================================================
# 6. RESUMEN FINAL
# ============================================================================

print("="*80)
print("✅ PLOTS CONSOLIDADOS GENERADOS EXITOSAMENTE")
print("="*80)
print(f"\n📂 Archivos guardados en: {OUTPUT_DIR}")
print(f"   - {plot1_path.name}")
print(f"   - {plot2_path.name}")
print(f"   - {plot3_path.name}")
print(f"   - {resumen_path.name}")
print("")
print("📊 INTERPRETACIÓN PARA EL COMITÉ:")
print("-" * 80)
print("1. VARIABILIDAD OPERATIVA (entre usuarios):")
print("   - Refleja diferencias en las medianas de cada usuario")
print("   - Alta variabilidad operativa → Usuarios muy heterogéneos")
print("")
print("2. VARIABILIDAD OBSERVADA (intra-usuario):")
print("   - Refleja fluctuaciones dentro de cada usuario")
print("   - Alta variabilidad observada → Señales inestables temporalmente")
print("")
print("3. RATIO OPER/OBS:")
print("   - Ratio > 1: Diferencias ENTRE usuarios > variabilidad DENTRO de cada uno")
print("   - Ratio < 1: Cada usuario es MÁS variable internamente que entre usuarios")
print("   - Justifica modelado multinivel (usuario como factor)")
print("")
print("4. DECISIÓN METODOLÓGICA:")
print("   - Usamos p50 (nivel) + IQR (variabilidad) para capturar AMBAS dimensiones")
print("   - El clustering y fuzzy operan sobre AGREGADOS SEMANALES (no datos crudos)")
print("   - Esto reduce ruido y aumenta interpretabilidad clínica")
print("")
print("="*80)
