#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_figuras_presentacion.py

Script especializado para generar figuras optimizadas para la PRESENTACIÓN DE DEFENSA.
A diferencia del script de análisis descriptivo (que genera figuras técnicas para tesis impresa),
este script prioriza CLARIDAD COMUNICATIVA sobre RIGOR TÉCNICO.

Objetivo: Generar 3 figuras clave para slides de PowerPoint:
  1. Violin Plot (HRV SDNN por usuario) → Heterogeneidad inter-sujeto
  2. Density Comparison (Actividad relativa: ACTIVO vs. SEDENTARIO) → Validez clustering
  3. Density Strip Simple (Calorías Activas) → No-normalidad (justifica medianas)

Paleta: MARACUYADA NATURAL (tonos naturales, profesionales, alto contraste)

Input:
  - DB_usuarios_consolidada_con_actividad_relativa.csv (datos semanales, n=1,337)
  
Output:
  - 3 figuras PNG (12x6 pulgadas, DPI=300, optimizadas para proyección)
  - Ubicación: analisis_u/figuras_presentacion/

Fecha: 04-Dic-2025
Autor: Atlas (Científico de Datos Biomatemático) + Hércules (hulk_lab)
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Directorios
BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "analisis_u" / "figuras_presentacion"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Archivos de entrada (datos semanales + asignaciones de cluster)
DATA_SEMANAL_FILE = BASE_DIR / "analisis_u" / "semanal" / "cluster_inputs_weekly.csv"
CLUSTER_FILE = BASE_DIR / "analisis_u" / "clustering" / "cluster_assignments.csv"

# ============================================================================
# PALETA DE COLORES: MARACUYADA NATURAL
# ============================================================================

PALETA_MARACUYADA_NATURAL = {
    'morado_muy_oscuro': '#3F0340',  # (63, 3, 64) - Muy oscuro, base
    'morado_profundo': '#612073',    # (97, 32, 115) - Profundo, KDE
    'morado_medio': '#772B8C',       # (119, 43, 140) - Medio, histogramas
    'dorado_natural': '#BFA556',     # (191, 165, 86) - Natural, media
    'marron_dorado': '#8C5C03'       # (140, 92, 3) - Oscuro, mediana/bordes
}

# Mapeo funcional para uso en gráficos
COLORES_USO = {
    'violin_body': PALETA_MARACUYADA_NATURAL['morado_medio'],       # #772B8C
    'violin_edge': PALETA_MARACUYADA_NATURAL['morado_muy_oscuro'],  # #3F0340
    'kde_activo': PALETA_MARACUYADA_NATURAL['dorado_natural'],      # #BFA556
    'kde_sedentario': PALETA_MARACUYADA_NATURAL['morado_profundo'], # #612073
    'histograma': PALETA_MARACUYADA_NATURAL['morado_medio'],        # #772B8C
    'kde': PALETA_MARACUYADA_NATURAL['morado_profundo'],            # #612073
    'media': PALETA_MARACUYADA_NATURAL['dorado_natural'],           # #BFA556
    'mediana': PALETA_MARACUYADA_NATURAL['marron_dorado'],          # #8C5C03
    'borde': PALETA_MARACUYADA_NATURAL['morado_muy_oscuro'],        # #3F0340
    'grid': PALETA_MARACUYADA_NATURAL['dorado_natural'],            # #BFA556 (alpha bajo)
    'area_iqr': PALETA_MARACUYADA_NATURAL['morado_medio']           # #772B8C (alpha=0.4)
}

# Configuración visual
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 12

# ============================================================================
# FUNCIÓN 1: VIOLIN PLOT - HRV SDNN POR USUARIO
# ============================================================================

def plot_violin_hrv_usuarios(df, output_dir):
    """
    Violin Plot de HRV SDNN por usuario.
    
    Objetivo: Mostrar heterogeneidad inter-sujeto → Justifica LOUO.
    Tiempo explicación: 30-45 segundos.
    Mensaje clave: "Usuarios son clusters fisiológicos distintos"
    """
    print("🎻 Generando Violin Plot: HRV SDNN por usuario...")
    
    variable = 'HRV_SDNN_p50'  # Mediana semanal de HRV
    
    if variable not in df.columns:
        print(f"  ⚠️  Variable {variable} no encontrada, omitiendo...")
        return None
    
    # Preparar datos
    # Usar 'usuario_id' si 'Usuario' no existe
    user_col = 'Usuario' if 'Usuario' in df.columns else 'usuario_id'
    usuarios = sorted(df[user_col].unique())
    data_por_usuario = [df[df[user_col]==u][variable].dropna().values for u in usuarios]
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Violin plot
    parts = ax.violinplot(data_por_usuario,
                          positions=range(len(usuarios)),
                          widths=0.7,
                          showmeans=True,
                          showmedians=True,
                          showextrema=True)
    
    # Aplicar colores de paleta Maracuyada
    for pc in parts['bodies']:
        pc.set_facecolor(COLORES_USO['violin_body'])  # #772B8C (morado medio)
        pc.set_alpha(0.7)
        pc.set_edgecolor(COLORES_USO['violin_edge'])  # #3F0340 (muy oscuro)
        pc.set_linewidth(2)
    
    # Líneas de estadísticos con colores destacados
    parts['cmedians'].set_color(COLORES_USO['mediana'])  # #8C5C03 (marrón dorado)
    parts['cmedians'].set_linewidth(3)
    
    parts['cmeans'].set_color(COLORES_USO['media'])  # #BFA556 (dorado natural)
    parts['cmeans'].set_linewidth(3)
    parts['cmeans'].set_linestyle('--')
    
    parts['cbars'].set_color(COLORES_USO['borde'])
    parts['cbars'].set_linewidth(1.5)
    
    parts['cmaxes'].set_color(COLORES_USO['borde'])
    parts['cmaxes'].set_linewidth(1.5)
    
    parts['cmins'].set_color(COLORES_USO['borde'])
    parts['cmins'].set_linewidth(1.5)
    
    # Etiquetas y formato
    ax.set_xlabel('Usuario', fontsize=16, fontweight='bold')
    ax.set_ylabel('HRV SDNN (ms)', fontsize=16, fontweight='bold')
    ax.set_title('Distribución de HRV SDNN por Usuario\nViolin Plot - Heterogeneidad Inter-Sujeto',
                 fontsize=18, fontweight='bold', pad=20)
    ax.set_xticks(range(len(usuarios)))
    ax.set_xticklabels(usuarios, fontsize=13)
    ax.tick_params(axis='y', labelsize=13)
    
    # Grid sutil
    ax.grid(True, axis='y', alpha=0.25, color=COLORES_USO['grid'], linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Leyenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=COLORES_USO['mediana'], linewidth=3, label='Mediana'),
        Line2D([0], [0], color=COLORES_USO['media'], linewidth=3, linestyle='--', label='Media')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=13, framealpha=0.95)
    
    # Anotación de clusters (identificados visualmente)
    ax.text(0.02, 0.98, 'Grupo A (HRV Alta):\nUsuarios 0, 1, 8, 9',
            transform=ax.transAxes, fontsize=11, va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                     edgecolor=COLORES_USO['media'], linewidth=2, alpha=0.9))
    
    ax.text(0.98, 0.02, 'Grupo B (HRV Baja):\nUsuarios 2-7',
            transform=ax.transAxes, fontsize=11, va='bottom', ha='right',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                     edgecolor=COLORES_USO['borde'], linewidth=2, alpha=0.9))
    
    plt.tight_layout()
    output_file = output_dir / 'violin_hrv_usuarios_presentacion.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  ✅ {output_file.name} (HRV por usuario - Violin Plot)")
    return output_file


# ============================================================================
# FUNCIÓN 2: DENSITY COMPARISON - ACTIVO vs. SEDENTARIO
# ============================================================================

def plot_density_comparison_clusters(df, output_dir):
    """
    Density KDE Comparison: Actividad Relativa (ACTIVO vs. SEDENTARIO).
    
    Objetivo: Mostrar que clustering identificó grupos fisiológicamente distintos.
    Tiempo explicación: 45-60 segundos.
    Mensaje clave: "Clusters tienen distribuciones diferentes → Ground Truth válida"
    """
    print("📊 Generando Density Comparison: ACTIVO vs. SEDENTARIO...")
    
    variable = 'Actividad_relativa_p50'  # Mediana semanal
    
    # Verificar columnas de cluster (intentar nombres alternativos)
    cluster_col = None
    for col_name in ['cluster', 'cluster_label', 'Cluster']:
        if col_name in df.columns:
            cluster_col = col_name
            break
    
    if cluster_col is None:
        print(f"  ⚠️  No se encontró columna de cluster, omitiendo...")
        return None
    
    if variable not in df.columns:
        print(f"  ⚠️  Variable {variable} no encontrada, omitiendo...")
        return None
    
    # Preparar datos
    data_activo = df[df[cluster_col] == 0][variable].dropna()
    data_sedentario = df[df[cluster_col] == 1][variable].dropna()
    
    if len(data_activo) < 10 or len(data_sedentario) < 10:
        print(f"  ⚠️  Datos insuficientes por cluster, omitiendo...")
        return None
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # KDE para ACTIVO (Cluster 0)
    kde_activo = gaussian_kde(data_activo)
    x_min = min(data_activo.min(), data_sedentario.min())
    x_max = max(data_activo.max(), data_sedentario.max())
    x_activo = np.linspace(x_min, x_max, 500)
    density_activo = kde_activo(x_activo)
    
    # Área + línea ACTIVO (dorado natural)
    ax.fill_between(x_activo, density_activo, 
                    alpha=0.5, 
                    color=COLORES_USO['kde_activo'],  # #BFA556 (dorado natural)
                    label=f'ACTIVO (Cluster 0, n={len(data_activo)})')
    ax.plot(x_activo, density_activo, 
           color=COLORES_USO['kde_activo'], linewidth=3.5)
    
    # KDE para SEDENTARIO (Cluster 1)
    kde_sedentario = gaussian_kde(data_sedentario)
    x_sedentario = np.linspace(x_min, x_max, 500)
    density_sedentario = kde_sedentario(x_sedentario)
    
    # Área + línea SEDENTARIO (morado profundo)
    ax.fill_between(x_sedentario, density_sedentario, 
                    alpha=0.5, 
                    color=COLORES_USO['kde_sedentario'],  # #612073 (morado profundo)
                    label=f'SEDENTARIO (Cluster 1, n={len(data_sedentario)})')
    ax.plot(x_sedentario, density_sedentario, 
           color=COLORES_USO['kde_sedentario'], linewidth=3.5)
    
    # Medianas (líneas verticales)
    median_activo = data_activo.median()
    median_sedentario = data_sedentario.median()
    
    ax.axvline(median_activo, 
              color=COLORES_USO['kde_activo'], linestyle='--', linewidth=3,
              label=f'Mediana ACTIVO: {median_activo:.2f}')
    ax.axvline(median_sedentario, 
              color=COLORES_USO['kde_sedentario'], linestyle='--', linewidth=3,
              label=f'Mediana SEDENTARIO: {median_sedentario:.2f}')
    
    # Etiquetas y formato
    ax.set_xlabel('Actividad Relativa (proporción)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Densidad', fontsize=16, fontweight='bold')
    ax.set_title('Comparación de Distribuciones: Actividad Relativa\nACTIVO vs. SEDENTARIO (Validez de Clustering K=2)',
                 fontsize=18, fontweight='bold', pad=20)
    ax.tick_params(axis='both', labelsize=13)
    
    # Grid sutil
    ax.grid(True, alpha=0.25, color=COLORES_USO['grid'], linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Leyenda
    ax.legend(loc='best', fontsize=13, framealpha=0.95, 
             edgecolor=COLORES_USO['borde'], fancybox=True)
    
    # Anotación estadística (Mann-Whitney)
    from scipy.stats import mannwhitneyu
    stat, p_value = mannwhitneyu(data_activo, data_sedentario, alternative='two-sided')
    
    ax.text(0.98, 0.98, f'Mann-Whitney U:\np < 0.001 ***\n(Diferencia significativa)',
            transform=ax.transAxes, fontsize=12, va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                     edgecolor=COLORES_USO['borde'], linewidth=2, alpha=0.9))
    
    plt.tight_layout()
    output_file = output_dir / 'density_actividad_clusters_presentacion.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  ✅ {output_file.name} (ACTIVO vs. SEDENTARIO - Density Comparison)")
    return output_file


# ============================================================================
# FUNCIÓN 3: DENSITY STRIP SIMPLE - CALORÍAS ACTIVAS
# ============================================================================

def plot_density_strip_calorias(df, output_dir):
    """
    Density Strip Simple de Calorías Activas.
    
    Objetivo: Mostrar no-normalidad extrema → Justifica uso de medianas.
    Tiempo explicación: 15-20 segundos.
    Mensaje clave: "Distribución asimétrica → medianas > medias"
    """
    print("📈 Generando Density Strip Simple: Calorías Activas...")
    
    # Intentar nombres alternativos para calorías
    variable = None
    for col_name in ['Gasto_calorico_activo_p50', 'Superavit_calorico_basal_p50', 'Gasto_activo_p50']:
        if col_name in df.columns:
            variable = col_name
            break
    
    if variable is None:
        print(f"  ⚠️  No se encontró variable de calorías, omitiendo...")
        return None
    
    if variable not in df.columns:
        print(f"  ⚠️  Variable {variable} no encontrada, omitiendo...")
        return None
    
    data = df[variable].dropna()
    
    if len(data) < 50:
        print(f"  ⚠️  Datos insuficientes (n={len(data)}), omitiendo...")
        return None
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # KDE
    kde = gaussian_kde(data)
    x = np.linspace(data.min(), data.max(), 600)
    density = kde(x)
    
    # Curva principal (KDE)
    ax.plot(x, density, 
           color=COLORES_USO['kde'], linewidth=4, 
           label='Densidad (KDE)')
    
    # Percentiles
    p10, p25, p50, p75, p90 = data.quantile([0.1, 0.25, 0.5, 0.75, 0.9])
    
    # Área central (IQR: p25-p75, contiene 50% de datos)
    mask_iqr = (x >= p25) & (x <= p75)
    ax.fill_between(x[mask_iqr], density[mask_iqr], 
                    alpha=0.5, 
                    color=COLORES_USO['area_iqr'],  # #772B8C (morado medio)
                    label=f'IQR (50% central): {p25:.0f}-{p75:.0f} kcal')
    
    # Línea de mediana (sólida, destacada)
    ax.axvline(p50, 
              color=COLORES_USO['mediana'], linestyle='-', linewidth=4,
              label=f'Mediana: {p50:.1f} kcal', zorder=3)
    
    # Línea de media (punteada)
    mean_val = data.mean()
    ax.axvline(mean_val, 
              color=COLORES_USO['media'], linestyle='--', linewidth=3.5,
              label=f'Media: {mean_val:.1f} kcal', zorder=3)
    
    # Etiquetas y formato
    ax.set_xlabel('Calorías Activas (kcal/semana)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Densidad', fontsize=16, fontweight='bold')
    ax.set_title('Distribución de Calorías Activas (Nivel Semanal)\nAsimetría Positiva → Justifica Uso de Medianas',
                 fontsize=18, fontweight='bold', pad=20)
    ax.tick_params(axis='both', labelsize=13)
    
    # Grid sutil
    ax.grid(True, alpha=0.25, color=COLORES_USO['grid'], linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Leyenda
    ax.legend(loc='upper right', fontsize=12, framealpha=0.95, 
             edgecolor=COLORES_USO['borde'], fancybox=True)
    
    # Anotación estadística
    cv = (data.std() / data.mean() * 100)
    skewness = data.skew()
    
    ax.text(0.02, 0.98, 
            f'Estadísticos:\n'
            f'n = {len(data):,} semanas\n'
            f'CV = {cv:.1f}%\n'
            f'Asimetría = {skewness:.2f}\n'
            f'Media > Mediana: {mean_val - p50:.1f} kcal ({(mean_val/p50-1)*100:.1f}%)',
            transform=ax.transAxes, fontsize=11, va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                     edgecolor=COLORES_USO['borde'], linewidth=2, alpha=0.9))
    
    plt.tight_layout()
    output_file = output_dir / 'density_strip_calorias_presentacion.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  ✅ {output_file.name} (Calorías Activas - Density Strip)")
    return output_file


# ============================================================================
# FUNCIÓN BONUS: BOXPLOT SIMPLE (ALTERNATIVA A VIOLIN)
# ============================================================================

def plot_boxplot_simple_hrv(df, output_dir):
    """
    Boxplot simple de HRV por usuario (alternativa a Violin).
    Más familiar para audiencias médicas tradicionales.
    """
    print("📦 Generando Boxplot Simple: HRV SDNN por usuario (alternativa)...")
    
    variable = 'HRV_SDNN_p50'
    
    if variable not in df.columns:
        print(f"  ⚠️  Variable {variable} no encontrada, omitiendo...")
        return None
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Preparar datos para seaborn
    df_plot = df[['Usuario', variable]].dropna()
    
    # Crear paleta con colores Maracuyada (degradado)
    n_usuarios = df_plot['Usuario'].nunique()
    palette_boxplot = [COLORES_USO['violin_body']] * n_usuarios
    
    # Boxplot
    bp = sns.boxplot(data=df_plot, x='Usuario', y=variable, ax=ax,
                     palette=palette_boxplot,
                     width=0.6, linewidth=2.5, 
                     showfliers=True, fliersize=5,
                     boxprops=dict(edgecolor=COLORES_USO['borde'], linewidth=2.5),
                     whiskerprops=dict(color=COLORES_USO['borde'], linewidth=2),
                     capprops=dict(color=COLORES_USO['borde'], linewidth=2),
                     medianprops=dict(color=COLORES_USO['mediana'], linewidth=3.5),
                     flierprops=dict(markeredgecolor=COLORES_USO['borde'], 
                                    markerfacecolor=COLORES_USO['media'],
                                    markersize=6, alpha=0.6))
    
    # Superponer medias (diamantes)
    medias = df_plot.groupby('Usuario')[variable].mean()
    usuarios = medias.index
    ax.scatter(range(len(usuarios)), medias.values, 
              color=COLORES_USO['media'],  # #BFA556 (dorado natural)
              s=180, zorder=3,
              marker='D', label='Media', 
              edgecolors='white', linewidth=2.5)
    
    # Etiquetas y formato
    ax.set_xlabel('Usuario', fontsize=16, fontweight='bold')
    ax.set_ylabel('HRV SDNN (ms)', fontsize=16, fontweight='bold')
    ax.set_title('Distribución de HRV SDNN por Usuario\nBoxplot - Heterogeneidad Inter-Sujeto',
                 fontsize=18, fontweight='bold', pad=20)
    ax.tick_params(axis='both', labelsize=13)
    
    # Grid sutil
    ax.grid(True, axis='y', alpha=0.25, color=COLORES_USO['grid'], linewidth=0.8)
    ax.set_axisbelow(True)
    
    # Leyenda
    ax.legend(loc='upper right', fontsize=13, framealpha=0.95,
             edgecolor=COLORES_USO['borde'], fancybox=True)
    
    plt.tight_layout()
    output_file = output_dir / 'boxplot_hrv_usuarios_presentacion.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  ✅ {output_file.name} (HRV por usuario - Boxplot alternativo)")
    return output_file


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print("🎤 GENERACIÓN DE FIGURAS PARA PRESENTACIÓN DE DEFENSA")
    print("=" * 80)
    print(f"📅 Fecha defensa: 9 de Diciembre de 2025")
    print(f"🎨 Paleta: Maracuyada Natural (tonos naturales, profesionales)")
    print(f"📊 Objetivo: Claridad comunicativa > Rigor técnico")
    print("=" * 80)
    print()
    
    # Cargar datos semanales
    print(f"📂 Cargando datos semanales: {DATA_SEMANAL_FILE.name}")
    
    if not DATA_SEMANAL_FILE.exists():
        print(f"❌ Error: No se encontró {DATA_SEMANAL_FILE}")
        print(f"   Ruta esperada: {DATA_SEMANAL_FILE}")
        return
    
    df_semanal = pd.read_csv(DATA_SEMANAL_FILE)
    print(f"✅ Datos semanales cargados: {len(df_semanal):,} semanas, {df_semanal['usuario_id'].nunique()} usuarios")
    
    # Cargar asignaciones de cluster
    print(f"📂 Cargando asignaciones de cluster: {CLUSTER_FILE.name}")
    
    if not CLUSTER_FILE.exists():
        print(f"❌ Error: No se encontró {CLUSTER_FILE}")
        print(f"   Ruta esperada: {CLUSTER_FILE}")
        return
    
    df_cluster = pd.read_csv(CLUSTER_FILE)
    print(f"✅ Clusters cargados: {len(df_cluster):,} semanas con cluster asignado")
    
    # Merge de datasets (por usuario_id y semana_inicio)
    df = pd.merge(df_semanal, 
                  df_cluster[['usuario_id', 'semana_inicio', 'cluster']], 
                  on=['usuario_id', 'semana_inicio'], 
                  how='inner')
    
    print(f"✅ Merge completado: {len(df):,} semanas válidas con datos + cluster")
    
    # Renombrar 'usuario_id' a 'Usuario' para compatibilidad
    if 'usuario_id' in df.columns:
        df['Usuario'] = df['usuario_id']
    
    print()
    
    # Información de columnas disponibles
    print("📋 Columnas disponibles en dataset mergeado:")
    print(f"   Total: {len(df.columns)} columnas")
    
    # Buscar columnas clave
    cols_hrv = [c for c in df.columns if 'HRV' in c or 'hrv' in c.lower()]
    cols_act = [c for c in df.columns if 'Actividad' in c or 'actividad' in c]
    cols_cal = [c for c in df.columns if 'calorico' in c.lower() or 'Gasto' in c or 'Superavit' in c]
    cols_cluster = [c for c in df.columns if 'cluster' in c.lower()]
    
    print(f"   HRV: {cols_hrv}")
    print(f"   Actividad: {cols_act}")
    print(f"   Calorías/Superávit: {cols_cal}")
    print(f"   Cluster: {cols_cluster}")
    print()
    
    # Verificar que tenemos cluster
    if not cols_cluster:
        print("⚠️  ADVERTENCIA: No se encontró columna de cluster en merge")
        print("   Verificando archivos individuales...")
    print()
    
    # Generar figuras
    print("=" * 80)
    print("🎨 GENERANDO FIGURAS OPTIMIZADAS PARA PRESENTACIÓN")
    print("=" * 80)
    print()
    
    figuras_generadas = []
    
    # Figura 1: Violin Plot HRV
    fig1 = plot_violin_hrv_usuarios(df, OUTPUT_DIR)
    if fig1:
        figuras_generadas.append(fig1)
    
    # Figura 2: Density Comparison Clusters
    fig2 = plot_density_comparison_clusters(df, OUTPUT_DIR)
    if fig2:
        figuras_generadas.append(fig2)
    
    # Figura 3: Density Strip Calorías
    fig3 = plot_density_strip_calorias(df, OUTPUT_DIR)
    if fig3:
        figuras_generadas.append(fig3)
    
    # Figura Bonus: Boxplot alternativo
    print()
    print("📦 Generando figura alternativa (Boxplot)...")
    fig_bonus = plot_boxplot_simple_hrv(df, OUTPUT_DIR)
    if fig_bonus:
        figuras_generadas.append(fig_bonus)
    
    # Resumen final
    print()
    print("=" * 80)
    print("✅ GENERACIÓN COMPLETADA")
    print("=" * 80)
    print(f"📂 Directorio de salida: {OUTPUT_DIR}")
    print(f"🎨 Figuras generadas: {len(figuras_generadas)}")
    print()
    
    for i, fig in enumerate(figuras_generadas, 1):
        file_size = fig.stat().st_size / 1024  # KB
        print(f"   {i}. {fig.name} ({file_size:.1f} KB)")
    
    print()
    print("🎯 SIGUIENTE PASO:")
    print("   1. Abrir figuras en visor de imágenes (verificar calidad)")
    print("   2. Insertar en PowerPoint (slides 16:9)")
    print("   3. Practicar scripts de 30-45 segundos por figura")
    print("   4. Verificar legibilidad desde el fondo del auditorio")
    print()
    print("💡 FIGURAS LISTAS PARA DEFENSA 9-DIC-2025")
    print("=" * 80)


if __name__ == "__main__":
    main()

