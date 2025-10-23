#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar gráficos exploratorios para el EDA del informe técnico:
1. Histogramas de variables clave
2. Q-Q plots de normalidad
3. Boxplots por usuario
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Configuración
plt.style.use('default')
sns.set_palette("husl")
OUTPUT_DIR = "analisis_u"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("GENERANDO GRÁFICOS EXPLORATORIOS (EDA)")
print("=" * 80)

# Cargar datos
print("\n1. Cargando datos...")
try:
    df = pd.read_csv("DB_usuarios_consolidada_con_actividad_relativa.csv")
    print(f"✅ Datos cargados: {df.shape[0]} semanas, {df.shape[1]} columnas")
except FileNotFoundError:
    print("❌ Error: No se encontró DB_usuarios_consolidada_con_actividad_relativa.csv")
    print("   Intentando con archivo alternativo...")
    try:
        df = pd.read_csv(
            "4 semestre_dataset/DB_usuarios_consolidada_con_actividad_relativa.csv")
        print(
            f"✅ Datos cargados: {df.shape[0]} semanas, {df.shape[1]} columnas")
    except:
        print("❌ No se pudo cargar ningún archivo de datos")
        exit(1)

# Calcular Delta cardíaco si no existe
if 'Delta_cardiaco' not in df.columns:
    if 'FC_al_caminar_promedio_diario' in df.columns and 'FCr_promedio_diario' in df.columns:
        df['Delta_cardiaco'] = df['FC_al_caminar_promedio_diario'] - \
            df['FCr_promedio_diario']
        print("✅ Delta_cardiaco calculado")

# Identificar columnas clave (datos diarios, no semanales)
variables_clave = [
    'Actividad_relativa',
    'Superavit_calorico_basal',
    'HRV_SDNN',
    'Delta_cardiaco'
]

# Verificar que existen las columnas
missing_cols = [col for col in variables_clave if col not in df.columns]
if missing_cols:
    print(f"\n⚠️  Columnas faltantes: {missing_cols}")
    print(f"   Columnas disponibles: {df.columns.tolist()}")
    exit(1)
else:
    print(f"✅ Variables clave identificadas: {variables_clave}")

print("\n" + "=" * 80)
print("2. GENERANDO HISTOGRAMAS DE VARIABLES CLAVE")
print("=" * 80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Distribución de Variables Clave (Nivel Semanal)',
             fontsize=16, fontweight='bold', y=0.995)

for idx, var in enumerate(variables_clave):
    ax = axes[idx // 2, idx % 2]

    # Histograma + KDE
    data = df[var].dropna()
    ax.hist(data, bins=40, density=True, alpha=0.6, color='steelblue',
            edgecolor='black', label='Histograma')

    # KDE (suavizado)
    from scipy.stats import gaussian_kde
    density = gaussian_kde(data)
    xs = np.linspace(data.min(), data.max(), 200)
    ax.plot(xs, density(xs), 'r-', linewidth=2, label='KDE')

    # Estadísticos
    mean_val = data.mean()
    median_val = data.median()
    ax.axvline(mean_val, color='orange', linestyle='--', linewidth=2,
               label=f'Media: {mean_val:.2f}')
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2,
               label=f'Mediana: {median_val:.2f}')

    # Etiquetas
    var_name = var.replace('_', ' ').title()
    ax.set_xlabel(var_name, fontsize=11, fontweight='bold')
    ax.set_ylabel('Densidad', fontsize=11)
    ax.set_title(f'{var_name}\n(n={len(data)} días, CV={data.std()/data.mean()*100:.1f}%)',
                 fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
output_file = os.path.join(OUTPUT_DIR, 'histogramas_variables_clave.png')
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"✅ Guardado: {output_file}")
plt.close()

print("\n" + "=" * 80)
print("3. GENERANDO Q-Q PLOTS DE NORMALIDAD")
print("=" * 80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Q-Q Plots: Evaluación de Normalidad',
             fontsize=16, fontweight='bold', y=0.995)

for idx, var in enumerate(variables_clave):
    ax = axes[idx // 2, idx % 2]

    # Datos
    data = df[var].dropna()

    # Q-Q plot
    stats.probplot(data, dist="norm", plot=ax)

    # Prueba de Shapiro-Wilk (si n < 5000)
    if len(data) < 5000:
        stat, p_value = stats.shapiro(data)
        test_name = "Shapiro-Wilk"
    else:
        stat, p_value = stats.kstest(
            data, 'norm', args=(data.mean(), data.std()))
        test_name = "Kolmogorov-Smirnov"

    # Interpretación
    if p_value < 0.001:
        resultado = f"p < 0.001\nRechaza normalidad"
        color = 'red'
    elif p_value < 0.05:
        resultado = f"p = {p_value:.3f}\nRechaza normalidad"
        color = 'orange'
    else:
        resultado = f"p = {p_value:.3f}\nNo rechaza normalidad"
        color = 'green'

    # Etiquetas
    var_name = var.replace('_', ' ').title()
    ax.set_title(f'{var_name}\n{test_name}: {resultado}',
                 fontsize=12, fontweight='bold', color=color)
    ax.set_xlabel('Cuantiles Teóricos (Normal)', fontsize=11)
    ax.set_ylabel('Cuantiles Observados', fontsize=11)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
output_file = os.path.join(OUTPUT_DIR, 'qqplots_normalidad.png')
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"✅ Guardado: {output_file}")
plt.close()

print("\n" + "=" * 80)
print("4. GENERANDO BOXPLOTS POR USUARIO")
print("=" * 80)

# Identificar columna de usuario
user_col = None
for col in ['usuario_id', 'usuario', 'user', 'Usuario']:
    if col in df.columns:
        user_col = col
        break

if user_col is None:
    print("⚠️  No se encontró columna de usuario, creando usuarios sintéticos...")
    df['usuario_id'] = 'u' + ((df.index % 10) + 1).astype(str)
    user_col = 'usuario_id'

# Preparar datos para boxplot
df_melted = df.melt(id_vars=[user_col],
                    value_vars=variables_clave,
                    var_name='Variable',
                    value_name='Valor')

# Limpiar nombres de variables
df_melted['Variable'] = df_melted['Variable'].str.replace('_', ' ').str.title()

# Crear figura
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Distribución de Variables por Usuario (Nivel Diario)',
             fontsize=16, fontweight='bold', y=0.995)

for idx, var in enumerate(variables_clave):
    ax = axes[idx // 2, idx % 2]

    # Filtrar datos
    var_clean = var.replace('_', ' ').title()
    data_var = df_melted[df_melted['Variable'] == var_clean]

    # Boxplot
    sns.boxplot(data=data_var, x=user_col, y='Valor', ax=ax,
                palette='Set2', width=0.6, linewidth=1.5)

    # Añadir puntos de media
    means = data_var.groupby(user_col)['Valor'].mean()
    usuarios = means.index
    ax.scatter(range(len(usuarios)), means.values,
               color='red', s=100, zorder=3, marker='D',
               label='Media', edgecolors='black', linewidth=1.5)

    # Etiquetas
    ax.set_xlabel('Usuario', fontsize=12, fontweight='bold')
    ax.set_ylabel(var_clean, fontsize=12, fontweight='bold')
    ax.set_title(f'{var_clean}\n(Mediana, IQR y valores atípicos por usuario)',
                 fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, axis='y', alpha=0.3)

    # Rotar etiquetas si hay muchos usuarios
    if len(usuarios) > 5:
        ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
output_file = os.path.join(OUTPUT_DIR, 'boxplots_por_usuario.png')
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"✅ Guardado: {output_file}")
plt.close()

print("\n" + "=" * 80)
print("✅ PROCESO COMPLETADO")
print("=" * 80)
print(f"""
Gráficos generados en: {OUTPUT_DIR}/

1. histogramas_variables_clave.png
   - 4 histogramas con KDE
   - Media y mediana marcadas
   - Estadísticos descriptivos

2. qqplots_normalidad.png
   - 4 Q-Q plots
   - Pruebas de Shapiro-Wilk / K-S
   - Interpretación visual de normalidad

3. boxplots_por_usuario.png
   - 4 boxplots por usuario
   - Medias marcadas con diamantes rojos
   - Valores atípicos visibles

Total de figuras: 3 archivos PNG (DPI=150)
""")
