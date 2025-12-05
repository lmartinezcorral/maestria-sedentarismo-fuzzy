#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_analisis_descriptivo_visual_v2.py

Análisis descriptivo completo con visualizaciones profesionales y atractivas
para el Informe Técnico LaTeX (Capítulo 4 - EDA).

Objetivo: Generar estadísticos descriptivos actualizados desde datos LIMPIOS
(post-winsorización, imputación, manejo de outliers) y producir gráficos
explicativos/argumentativos de alta calidad visual.

Input:
  - DB_final_v3_u{1-10}.csv (datos diarios limpios por usuario)
  - DB_usuarios_consolidada_con_actividad_relativa.csv (consolidado)

Output:
  - tabla_descriptivos_actualizados.csv
  - tabla_descriptivos_actualizados.tex (formato LaTeX)
  - 15+ figuras PNG (alta resolución, estilo profesional):
    * Violin plots (distribuciones por usuario)
    * Grouped bar charts (medianas comparativas)
    * Heatmaps (patrones temporales)
    * Scatter matrix (relaciones bivariadas)
    * Boxplots comparativos
    * Time series (últimos 90 días, ejemplo visual)

Notas:
  - Anonimización: usuarios como u1-u10
  - Visualizaciones argumentativas (no dashboards exhaustivos)
  - Estilo profesional: paletas coherentes, tipografía clara, grids sutiles
"""

import os
import glob
import warnings
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, kstest

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Directorios
BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "analisis_u" / "descriptivos_visuales"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Archivos de entrada
CONSOLIDADO_FILE = BASE_DIR / "DB_usuarios_consolidada_con_actividad_relativa.csv"
DB_USUARIOS_PATTERN = str(BASE_DIR / "DB_final_v3_u*.csv")

# Archivos para KDE multi-distribución (con cluster)
DATA_SEMANAL_CLUSTER = BASE_DIR / "analisis_u" / "semanal" / "cluster_inputs_weekly.csv"
CLUSTER_ASSIGNMENTS = BASE_DIR / "analisis_u" / "clustering" / "cluster_assignments.csv"

# Estilo visual profesional
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("notebook", font_scale=1.1)
sns.set_palette("Set2")

# Colores coherentes para usuarios (10 colores distinguibles)
USER_COLORS = sns.color_palette("tab10", 10)

# Variables clave a analizar
VARIABLES_CLAVE = [
    'Numero_pasos_por_dia',
    'Gasto_calorico_activo',
    'FCr_promedio_diario',
    'FC_al_caminar_promedio_diario',
    'HRV_SDNN',
    'Total_hrs_monitorizadas',
    'Actividad_relativa',
    'Superavit_calorico_basal'
]

# Nombres amigables para gráficos
NOMBRES_AMIGABLES = {
    'Numero_pasos_por_dia': 'Pasos Diarios',
    'Gasto_calorico_activo': 'Calorías Activas (kcal)',
    'FCr_promedio_diario': 'FC Reposo (lpm)',
    'FC_al_caminar_promedio_diario': 'FC al Caminar (lpm)',
    'HRV_SDNN': 'HRV SDNN (ms)',
    'Total_hrs_monitorizadas': 'Hrs Monitorizadas',
    'Actividad_relativa': 'Actividad Relativa (prop.)',
    'Superavit_calorico_basal': 'Superávit Calórico (%)'
}


# ============================================================================
# UTILIDADES
# ============================================================================

def cargar_datos_consolidados():
    """Carga el dataset consolidado."""
    print(f"📂 Cargando datos consolidados: {CONSOLIDADO_FILE.name}")
    if not CONSOLIDADO_FILE.exists():
        raise FileNotFoundError(f"No se encontró: {CONSOLIDADO_FILE}")

    df = pd.read_csv(CONSOLIDADO_FILE)
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df = df.dropna(subset=['Fecha']).sort_values(
        ['Usuario', 'Fecha']).reset_index(drop=True)

    print(
        f"✅ Cargados: {len(df):,} registros, {df['Usuario'].nunique()} usuarios")
    return df


def cargar_datos_individuales():
    """Carga archivos DB_final_v3_u*.csv en un DataFrame consolidado."""
    archivos = sorted(glob.glob(DB_USUARIOS_PATTERN))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos: {DB_USUARIOS_PATTERN}")

    print(f"📂 Cargando {len(archivos)} archivos individuales...")

    dfs = []
    for archivo in archivos:
        nombre = Path(archivo).stem  # DB_final_v3_u1 -> u1
        usuario_id = nombre.split('_')[-1]  # u1, u2, etc.

        df_temp = pd.read_csv(archivo)
        df_temp['Usuario'] = usuario_id
        df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'], errors='coerce')
        dfs.append(df_temp)

    df_consolidado = pd.concat(dfs, ignore_index=True)
    df_consolidado = df_consolidado.dropna(subset=['Fecha']).sort_values(
        ['Usuario', 'Fecha']).reset_index(drop=True)

    print(
        f"✅ Consolidados: {len(df_consolidado):,} registros, {df_consolidado['Usuario'].nunique()} usuarios")
    return df_consolidado


def calcular_estadisticos_descriptivos(df, variables):
    """Calcula estadísticos descriptivos completos para variables clave."""
    resultados = []

    for var in variables:
        if var not in df.columns:
            print(f"⚠️  Variable {var} no encontrada, omitiendo...")
            continue

        data = df[var].dropna()

        if len(data) < 10:
            print(
                f"⚠️  Variable {var} con muy pocos datos ({len(data)}), omitiendo...")
            continue

        # Estadísticos básicos
        media = data.mean()
        de = data.std()
        mediana = data.median()
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        minimo = data.min()
        maximo = data.max()
        cv = (de / media * 100) if media > 0 else np.nan

        # Prueba de normalidad
        if len(data) < 5000:
            stat_norm, p_norm = shapiro(data)
            test_norm = "Shapiro-Wilk"
        else:
            stat_norm, p_norm = kstest(data, 'norm', args=(media, de))
            test_norm = "Kolmogorov-Smirnov"

        resultados.append({
            'Variable': NOMBRES_AMIGABLES.get(var, var),
            'n': len(data),
            'Media': round(media, 2),
            'DE': round(de, 2),
            'CV (%)': round(cv, 1),
            'Mediana': round(mediana, 2),
            'Q1': round(q1, 2),
            'Q3': round(q3, 2),
            'IQR': round(iqr, 2),
            'Min': round(minimo, 2),
            'Max': round(maximo, 2),
            'Test Normalidad': test_norm,
            'p-valor': f"{p_norm:.4f}" if p_norm >= 0.001 else "< 0.001"
        })

    return pd.DataFrame(resultados)


def exportar_tabla_latex(df_tabla, output_file):
    """Exporta tabla de estadísticos en formato LaTeX (generación manual)."""

    # Generar LaTeX manualmente
    n_cols = len(df_tabla.columns)
    col_format = 'l' + 'r' * (n_cols - 1)

    latex_lines = []
    latex_lines.append("\\begin{table}[htbp]")
    latex_lines.append("\\centering")
    latex_lines.append(
        "\\caption{Estadísticos Descriptivos Actualizados (Datos Post-Limpieza)}")
    latex_lines.append("\\label{tab:descriptivos_actualizados}")
    latex_lines.append(f"\\begin{{tabular}}{{{col_format}}}")
    latex_lines.append("\\toprule")

    # Header
    header = " & ".join(df_tabla.columns) + " \\\\"
    latex_lines.append(header)
    latex_lines.append("\\midrule")

    # Rows
    for _, row in df_tabla.iterrows():
        row_str = " & ".join([str(val) for val in row.values]) + " \\\\"
        latex_lines.append(row_str)

    latex_lines.append("\\bottomrule")
    latex_lines.append("\\end{tabular}")
    latex_lines.append("\\end{table}")

    latex_str = "\n".join(latex_lines)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_str)

    print(f"📄 Tabla LaTeX exportada: {output_file.name}")


# ============================================================================
# VISUALIZACIONES
# ============================================================================

def plot_violin_por_usuario(df, variables, output_dir):
    """
    Violin plots: Distribuciones de variables clave por usuario.
    Muestra heterogeneidad inter-sujeto.
    """
    print("🎻 Generando violin plots por usuario...")

    n_vars = len(variables)
    n_cols = 2
    n_rows = (n_vars + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
    axes = axes.flatten() if n_vars > 1 else [axes]

    fig.suptitle('Distribución de Variables Clave por Usuario\n(Violin Plots - Heterogeneidad Inter-Sujeto)',
                 fontsize=16, fontweight='bold', y=0.995)

    for idx, var in enumerate(variables):
        ax = axes[idx]

        if var not in df.columns:
            ax.text(0.5, 0.5, f'{var}\nNo disponible',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue

        df_plot = df[['Usuario', var]].dropna()

        sns.violinplot(data=df_plot, x='Usuario', y=var, ax=ax, palette=USER_COLORS,
                       inner='quartile', cut=0, linewidth=1.5)

        ax.set_xlabel('Usuario', fontsize=11, fontweight='bold')
        ax.set_ylabel(NOMBRES_AMIGABLES.get(var, var),
                      fontsize=11, fontweight='bold')
        ax.set_title(NOMBRES_AMIGABLES.get(var, var),
                     fontsize=12, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)

    # Ocultar ejes sobrantes
    for idx in range(n_vars, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    output_file = output_dir / 'violin_plots_por_usuario.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ {output_file.name}")


def plot_grouped_bar_medianas(df, variables, output_dir):
    """
    Grouped bar chart: Medianas de variables por usuario.
    Comparación visual rápida de niveles.
    """
    print("📊 Generando grouped bar chart (medianas por usuario)...")

    # Calcular medianas por usuario
    medianas = df.groupby('Usuario')[variables].median()

    # Normalizar por variable para comparabilidad (escala 0-1)
    medianas_norm = (medianas - medianas.min()) / \
        (medianas.max() - medianas.min())

    fig, ax = plt.subplots(figsize=(14, 6))

    x = np.arange(len(medianas.index))
    width = 0.1
    multiplier = 0

    # Limitar a 8 vars para legibilidad
    for idx, var in enumerate(variables[:8]):
        if var in medianas_norm.columns:
            offset = width * multiplier
            ax.bar(x + offset, medianas_norm[var], width,
                   label=NOMBRES_AMIGABLES.get(var, var)[:20], alpha=0.85)
            multiplier += 1

    ax.set_xlabel('Usuario', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mediana Normalizada [0-1]', fontsize=12, fontweight='bold')
    ax.set_title('Comparación de Medianas por Usuario (Normalizadas)\nPerfiles de Comportamiento Individual',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 3.5)
    ax.set_xticklabels(medianas.index)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=9)
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    output_file = output_dir / 'grouped_bar_medianas_por_usuario.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ {output_file.name}")


def plot_heatmap_temporal(df, output_dir):
    """
    Heatmap: Patrón semanal de actividad por usuario.
    Muestra día de la semana vs usuario, color = mediana de pasos.
    """
    print("🔥 Generando heatmap de patrones temporales...")

    # Añadir día de la semana
    df_temp = df.copy()
    df_temp['Dia_Semana'] = df_temp['Fecha'].dt.day_name()

    # Orden de días
    dias_orden = ['Monday', 'Tuesday', 'Wednesday',
                  'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Pivot: Usuario x Día de Semana, valor = mediana pasos
    if 'Numero_pasos_por_dia' in df_temp.columns:
        pivot = df_temp.pivot_table(
            values='Numero_pasos_por_dia',
            index='Usuario',
            columns='Dia_Semana',
            aggfunc='median'
        )[dias_orden]

        fig, ax = plt.subplots(figsize=(10, 6))

        sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Mediana Pasos'},
                    linewidths=0.5, ax=ax, vmin=pivot.min().min() * 0.8, vmax=pivot.max().max() * 1.1)

        ax.set_xlabel('Día de la Semana', fontsize=12, fontweight='bold')
        ax.set_ylabel('Usuario', fontsize=12, fontweight='bold')
        ax.set_title('Patrón Semanal de Actividad (Mediana Pasos por Día)\nHeterogeneidad Temporal por Usuario',
                     fontsize=14, fontweight='bold')
        ax.set_xticklabels(['Lun', 'Mar', 'Mié', 'Jue',
                           'Vie', 'Sáb', 'Dom'], rotation=0)

        plt.tight_layout()
        output_file = output_dir / 'heatmap_patron_semanal.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✅ {output_file.name}")


def plot_scatter_matrix(df, variables, output_dir):
    """
    Scatter matrix: Relaciones bivariadas entre variables clave.
    Sample de datos para performance (máx 2000 puntos).
    """
    print("🔍 Generando scatter matrix (relaciones bivariadas)...")

    # Seleccionar 4 variables más importantes para legibilidad
    vars_principales = [
        'Numero_pasos_por_dia',
        'HRV_SDNN',
        'Actividad_relativa',
        'Superavit_calorico_basal'
    ]

    vars_disponibles = [v for v in vars_principales if v in df.columns]

    if len(vars_disponibles) < 2:
        print("  ⚠️  Insuficientes variables para scatter matrix")
        return

    # Sample para performance
    df_sample = df[vars_disponibles + ['Usuario']
                   ].dropna().sample(min(2000, len(df)), random_state=42)

    # Renombrar columnas
    df_sample_renamed = df_sample.rename(columns=NOMBRES_AMIGABLES)

    # Scatter matrix con colores por usuario
    g = sns.PairGrid(df_sample_renamed, hue='Usuario',
                     palette=USER_COLORS, height=2.5, aspect=1)
    g.map_upper(sns.scatterplot, alpha=0.5, s=20)
    g.map_lower(sns.kdeplot, alpha=0.6)
    g.map_diag(sns.histplot, kde=True, alpha=0.6)
    g.add_legend(title='Usuario', bbox_to_anchor=(
        1.05, 0.5), loc='center left', fontsize=9)

    g.fig.suptitle('Matriz de Dispersión: Relaciones Bivariadas\n(Muestra n=2,000 días, Coloreado por Usuario)',
                   fontsize=14, fontweight='bold', y=1.01)

    plt.tight_layout()
    output_file = output_dir / 'scatter_matrix_relaciones.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ {output_file.name}")


def plot_boxplots_comparativos(df, variables, output_dir):
    """
    Boxplots comparativos - VERSIÓN APA 7 CON PALETA FACULTAD
    
    Distribución de variables con outliers visibles,
    aplicando etiquetas (a), (b), (c)... según convención APA 7
    y colores oficiales de la Facultad de Medicina y Ciencias Biomédicas.
    """
    print("📦 Generando boxplots comparativos (APA 7 + paleta facultad)...")
    
    # ============ COLORES OFICIALES FACULTAD ============
    COLORES_FACULTAD = {
        'morado_oscuro': '#571E72',
        'magenta': '#AA03C0',
        'morado_medio': '#A733EA',
        'rosa_purpura': '#A4579F',
        'dorado': '#D0A433',
        'crema_claro': '#FEF7CD',
        'crema': '#F1F0D9',
        'morado_oscuro2': '#750CA3'
    }
    
    # Para boxplots, usaremos una paleta personalizada derivada de los colores oficiales
    COLORES_BOXPLOT = [COLORES_FACULTAD['morado_medio'], COLORES_FACULTAD['magenta'], 
                       COLORES_FACULTAD['rosa_purpura'], COLORES_FACULTAD['morado_oscuro2'],
                       COLORES_FACULTAD['dorado'], COLORES_FACULTAD['morado_oscuro'],
                       COLORES_FACULTAD['magenta'], COLORES_FACULTAD['morado_medio'],
                       COLORES_FACULTAD['rosa_purpura'], COLORES_FACULTAD['morado_oscuro']]
    
    COLORES_USO = {
        'media': COLORES_FACULTAD['dorado'],
        'borde': COLORES_FACULTAD['morado_oscuro'],
        'grid': COLORES_FACULTAD['crema']
    }
    # ==================================================

    n_vars = len(variables)
    n_cols = 2
    n_rows = (n_vars + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
    axes = axes.flatten() if n_vars > 1 else [axes]

    fig.suptitle('Distribución de Variables con Detección de Outliers\n(Boxplots + Media Superpuesta)',
                 fontsize=16, fontweight='bold', y=0.995)

    for idx, var in enumerate(variables):
        ax = axes[idx]

        if var not in df.columns:
            ax.text(0.5, 0.5, f'{var}\nNo disponible',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue

        df_plot = df[['Usuario', var]].dropna()

        # ========== BOXPLOT CON COLORES FACULTAD ==========
        bp = sns.boxplot(data=df_plot, x='Usuario', y=var, ax=ax, palette=COLORES_BOXPLOT,
                         width=0.6, linewidth=1.5, showfliers=True, fliersize=3)

        # ========== SUPERPONER MEDIAS CON COLOR FACULTAD ==========
        medias = df_plot.groupby('Usuario')[var].mean()
        usuarios = medias.index
        ax.scatter(range(len(usuarios)), medias.values, 
                  color=COLORES_USO['media'],  # #D0A433 (dorado)
                  s=100, zorder=3,
                  marker='D', label='Media', 
                  edgecolors=COLORES_USO['borde'],  # #571E72
                  linewidth=1.5)

        # ========== ⭐ ETIQUETA APA 7 EN TÍTULO (CORREGIDO) ==========
        label = chr(97 + idx)  # a, b, c, d, e, f, g, h
        
        ax.set_xlabel('Usuario', fontsize=11, fontweight='bold')
        ax.set_ylabel(NOMBRES_AMIGABLES.get(var, var),
                      fontsize=11, fontweight='bold')
        ax.set_title(f'({label}) {NOMBRES_AMIGABLES.get(var, var)}',
                     fontsize=12, fontweight='bold')
        
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, axis='y', alpha=0.3, color=COLORES_USO['grid'])  # #F1F0D9

    # Ocultar ejes sobrantes
    for idx in range(n_vars, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout(pad=1.5)
    output_file = output_dir / 'boxplots_comparativos.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✅ {output_file.name} regenerado (APA 7 + paleta facultad)")


def plot_time_series_ultimos_90_dias(df, variables, output_dir):
    """
    Time series: Ventana de 90 días con mayor densidad de datos (ejemplo visual).
    Líneas suavizadas (rolling mean 7 días) por usuario.
    """
    print("📈 Generando time series (ventana de 90 días, ejemplo visual)...")

    # Buscar ventana de 90 días con mayor densidad de datos
    fecha_max = df['Fecha'].max()
    fecha_min = df['Fecha'].min()

    # Probar diferentes ventanas
    mejor_ventana = None
    max_registros = 0

    for dias_offset in [0, 180, 365, 545]:  # Últimos 90d, hace 6m, hace 1a, hace 1.5a
        fecha_fin = fecha_max - timedelta(days=dias_offset)
        fecha_inicio = fecha_fin - timedelta(days=90)

        if fecha_inicio < fecha_min:
            continue

        df_ventana = df[(df['Fecha'] >= fecha_inicio)
                        & (df['Fecha'] <= fecha_fin)]
        n_registros = len(df_ventana)

        if n_registros > max_registros:
            max_registros = n_registros
            mejor_ventana = (fecha_inicio, fecha_fin)

    if mejor_ventana is None or max_registros < 50:
        print("  ⚠️  Insuficientes datos para time series (probado múltiples ventanas)")
        return

    fecha_min_90d, fecha_max_90d = mejor_ventana
    df_90d = df[(df['Fecha'] >= fecha_min_90d) & (
        df['Fecha'] <= fecha_max_90d)].copy()

    print(
        f"  📅 Ventana seleccionada: {fecha_min_90d.date()} a {fecha_max_90d.date()} (n={len(df_90d):,})")

    # Seleccionar 4 variables clave
    vars_ts = [
        'Numero_pasos_por_dia',
        'FCr_promedio_diario',
        'HRV_SDNN',
        'Actividad_relativa'
    ]

    vars_disponibles = [v for v in vars_ts if v in df_90d.columns]

    if not vars_disponibles:
        print("  ⚠️  Variables no disponibles para time series")
        return

    n_vars = len(vars_disponibles)
    fig, axes = plt.subplots(n_vars, 1, figsize=(14, 3 * n_vars), sharex=True)
    axes = [axes] if n_vars == 1 else axes

    fig.suptitle('Series Temporales Recientes (Últimos 90 Días)\nEjemplo Visual de Variabilidad Intra-Sujeto',
                 fontsize=16, fontweight='bold', y=0.995)

    for idx, var in enumerate(vars_disponibles):
        ax = axes[idx]

        for user_idx, usuario in enumerate(sorted(df_90d['Usuario'].unique())):
            df_user = df_90d[df_90d['Usuario'] == usuario][[
                'Fecha', var]].dropna().sort_values('Fecha')

            if len(df_user) < 5:
                continue

            # Suavizado rolling mean 7 días
            df_user['valor_suavizado'] = df_user[var].rolling(
                window=7, min_periods=1, center=True).mean()

            ax.plot(df_user['Fecha'], df_user['valor_suavizado'],
                    color=USER_COLORS[user_idx], alpha=0.8, linewidth=2, label=usuario)

        ax.set_ylabel(NOMBRES_AMIGABLES.get(var, var),
                      fontsize=11, fontweight='bold')
        ax.set_title(NOMBRES_AMIGABLES.get(var, var),
                     fontsize=12, fontweight='bold')
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=8, ncol=1)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))

    axes[-1].set_xlabel('Fecha (últimos 90 días)',
                        fontsize=12, fontweight='bold')
    plt.setp(axes[-1].xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    output_file = output_dir / 'time_series_ultimos_90_dias.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ {output_file.name}")


def plot_kde_multi_distribucion(df_diario, variables, output_dir):
    """
    KDE Multi-Distribución (ACTIVO vs. SEDENTARIO) - VERSIÓN MEJORADA
    
    Genera gráficos KDE puros (sin histograma) comparando distribuciones
    de ACTIVO vs. SEDENTARIO para cada variable, aplicando técnica de
    overlapping density plots recomendada por Seaborn best practices.
    
    Paleta: Captura Custom (morados + dorado naranja)
    Técnica: sns.kdeplot() con fill=True, alpha=0.5, comparación directa
    """
    print("📊 Generando KDE Multi-Distribución (ACTIVO vs. SEDENTARIO)...")
    
    # ============ PALETA CAPTURA CUSTOM ============
    PALETA_CAPTURA_CUSTOM = {
        'purpura_intenso': '#5C025D',
        'purpura_brillante': '#94268F',
        'naranja_dorado': '#F1B253',
        'marron_claro': '#C19A6B',
        'purpura_apagado': '#6A3877',
        'beige_claro': '#ECE1D3'
    }
    
    COLORES_USO_CAPTURA = {
        'activo': PALETA_CAPTURA_CUSTOM['naranja_dorado'],      # #F1B253 (dorado)
        'sedentario': PALETA_CAPTURA_CUSTOM['purpura_brillante'], # #94268F (púrpura)
        'mediana_activo': PALETA_CAPTURA_CUSTOM['marron_claro'],   # #C19A6B
        'mediana_sedentario': PALETA_CAPTURA_CUSTOM['purpura_intenso'], # #5C025D
        'borde': PALETA_CAPTURA_CUSTOM['purpura_intenso'],      # #5C025D
        'grid': PALETA_CAPTURA_CUSTOM['beige_claro']            # #ECE1D3
    }
    # ==================================================
    
    # Cargar datos semanales con cluster
    print("  📂 Cargando datos semanales con cluster...")
    
    if not DATA_SEMANAL_CLUSTER.exists() or not CLUSTER_ASSIGNMENTS.exists():
        print("  ⚠️  Archivos de cluster no encontrados, generando KDE global...")
        return plot_histogramas_con_kde_original(df_diario, variables, output_dir)
    
    try:
        df_semanal = pd.read_csv(DATA_SEMANAL_CLUSTER)
        df_cluster = pd.read_csv(CLUSTER_ASSIGNMENTS)
        
        # Merge
        df = pd.merge(df_semanal, 
                     df_cluster[['usuario_id', 'semana_inicio', 'cluster']], 
                     on=['usuario_id', 'semana_inicio'], 
                     how='inner')
        
        print(f"  ✅ Datos semanales con cluster: {len(df):,} semanas")
        
        # Mapear nombres de variables diarias a semanales (p50)
        variables_semanales = []
        for var in variables:
            var_semanal = f"{var}_p50" if f"{var}_p50" in df.columns else var
            if var_semanal in df.columns:
                variables_semanales.append(var_semanal)
            else:
                print(f"  ⚠️  Variable {var} no encontrada en datos semanales")
        
        if not variables_semanales:
            print("  ⚠️  No se encontraron variables compatibles, usando versión original...")
            return plot_histogramas_con_kde_original(df_diario, variables, output_dir)
        
    except Exception as e:
        print(f"  ❌ Error al cargar datos con cluster: {e}")
        return plot_histogramas_con_kde_original(df_diario, variables, output_dir)
    
    n_vars = len(variables_semanales)
    n_cols = 2
    n_rows = (n_vars + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows))
    axes = axes.flatten() if n_vars > 1 else [axes]
    
    fig.suptitle('Comparación de Distribuciones: ACTIVO vs. SEDENTARIO\nKDE Multi-Distribución (Nivel Semanal)',
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Usar nombre original para labels (sin _p50)
    variables_originales = [v.replace('_p50', '') for v in variables_semanales]
    
    for idx, (var, var_original) in enumerate(zip(variables_semanales, variables_originales)):
        ax = axes[idx]
        
        if var not in df.columns:
            ax.text(0.5, 0.5, f'{var_original}\nNo disponible',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue
        
        # Datos por cluster (usar columna de cluster)
        cluster_col = 'cluster'
        data_activo = df[df[cluster_col] == 0][var].dropna()
        data_sedentario = df[df[cluster_col] == 1][var].dropna()
        
        if len(data_activo) < 10 or len(data_sedentario) < 10:
            ax.text(0.5, 0.5, f'{var}\nDatos insuficientes',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue
        
        # ========== KDE MULTI-DISTRIBUCIÓN (TÉCNICA SEABORN) ==========
        
        # KDE para ACTIVO (dorado)
        sns.kdeplot(data=data_activo, ax=ax,
                   fill=True, 
                   color=COLORES_USO_CAPTURA['activo'],  # #F1B253 (naranja dorado)
                   alpha=0.5,
                   linewidth=3,
                   label=f'ACTIVO (n={len(data_activo)})')
        
        # KDE para SEDENTARIO (púrpura)
        sns.kdeplot(data=data_sedentario, ax=ax,
                   fill=True,
                   color=COLORES_USO_CAPTURA['sedentario'],  # #94268F (púrpura brillante)
                   alpha=0.5,
                   linewidth=3,
                   label=f'SEDENTARIO (n={len(data_sedentario)})')
        
        # ========== MEDIANAS CON LÍNEAS VERTICALES ==========
        median_activo = data_activo.median()
        median_sedentario = data_sedentario.median()
        
        ax.axvline(median_activo,
                  color=COLORES_USO_CAPTURA['activo'],  # #F1B253
                  linestyle='--',
                  linewidth=2.5,
                  alpha=0.9,
                  label=f'Mediana ACTIVO: {median_activo:.1f}')
        
        ax.axvline(median_sedentario,
                  color=COLORES_USO_CAPTURA['sedentario'],  # #94268F
                  linestyle='--',
                  linewidth=2.5,
                  alpha=0.9,
                  label=f'Mediana SEDENTARIO: {median_sedentario:.1f}')
        
        # ========== ETIQUETA APA 7 EN TÍTULO ==========
        label = chr(97 + idx)  # a, b, c, d, e, f, g, h
        
        ax.set_xlabel(NOMBRES_AMIGABLES.get(var_original, var_original),
                      fontsize=11, fontweight='bold')
        ax.set_ylabel('Densidad', fontsize=11)
        ax.set_title(f'({label}) {NOMBRES_AMIGABLES.get(var_original, var_original)}',
                     fontsize=12, fontweight='bold')
        
        ax.legend(loc='best', fontsize=8.5, framealpha=0.95)
        ax.grid(True, alpha=0.25, color=COLORES_USO_CAPTURA['grid'], linewidth=0.8)
        ax.set_axisbelow(True)
    
    # Ocultar ejes sobrantes
    for idx in range(n_vars, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout(pad=1.5)
    output_file = output_dir / 'kde_multi_distribucion_activo_sedentario.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✅ {output_file.name} generado (KDE Multi-Distribución + Paleta Captura)")
    
    return output_file


def plot_hibrido_histograma_kde_6_variables(df, variables, output_dir):
    """
    Híbrido Histograma + KDE (6 Variables Clave) - Paleta Custom Seleccionada
    
    Combina lo mejor de ambos mundos:
    - Barras de histograma (estructura clara, bins visibles)
    - KDE superpuesto (tendencia suave, densidad)
    
    Variables incluidas (solo las más relevantes):
    - Pasos diarios, FC reposo, FC caminar, HRV SDNN, Superávit calórico, Actividad relativa
    
    Paleta Custom (selección específica de Luis):
    - Barras: #8C5C03 (marrón dorado)
    - KDE: #392840 (morado profundo, alpha=0.2)
    - Media: #F1B253 (naranja dorado)
    - Mediana: #F2BB77 (dorado luminoso)
    """
    print("📊 Generando Híbrido Histograma+KDE (6 variables clave, paleta custom)...")
    
    # ============ PALETA CUSTOM SELECCIONADA (FINAL - PERFECCIÓN) ============
    COLORES_HIBRIDO = {
        'histograma': '#392840',      # #392840 - Morado profundo (barras, alpha=0.8)
        'kde_area': '#8C5C03',        # #8C5C03 - Marrón dorado (KDE área, alpha=0.3)
        'kde_linea': '#F2B544',       # #F2B544 - Dorado vibrante (KDE línea, alpha=0.9, lw=3.8)
        'media': '#5C025D',           # #5C025D - Púrpura intenso (línea media)
        'mediana': '#750CA3',         # #750CA3 - Morado oscuro 2 (línea mediana)
        'borde': '#3F0340',           # #3F0340 - Morado muy oscuro (bordes barras)
        'grid': '#ECE1D3'             # #ECE1D3 - Beige claro (grid)
    }
    # ==================================================
    
    # Solo 6 variables clave - ORDEN ESPECÍFICO:
    # Izquierda: Actividad/Metabolismo, Derecha: Cardíacas
    variables_seleccionadas = [
        'Numero_pasos_por_dia',       # (a) Izquierda
        'FCr_promedio_diario',        # (b) Derecha
        'Actividad_relativa',         # (c) Izquierda
        'FC_al_caminar_promedio_diario', # (d) Derecha
        'Superavit_calorico_basal',   # (e) Izquierda
        'HRV_SDNN'                    # (f) Derecha
    ]
    
    # Filtrar solo las que existen en el dataset
    variables_disponibles = [v for v in variables_seleccionadas if v in df.columns]
    
    if not variables_disponibles:
        print("  ⚠️  Ninguna de las variables seleccionadas está disponible")
        return None
    
    print(f"  ✅ Variables a graficar: {len(variables_disponibles)}")
    
    n_vars = len(variables_disponibles)
    n_cols = 2
    n_rows = (n_vars + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows))
    axes = axes.flatten() if n_vars > 1 else [axes]
    
    fig.suptitle('Distribuciones de Variables Clave (Nivel Diario)\nHíbrido Histograma + KDE - Paleta Custom',
                 fontsize=16, fontweight='bold', y=0.995)
    
    for idx, var in enumerate(variables_disponibles):
        ax = axes[idx]
        
        data = df[var].dropna()
        
        if len(data) < 10:
            ax.text(0.5, 0.5, f'{var}\nDatos insuficientes',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue
        
        # ========== HISTOGRAMA (BARRAS) - Morado Profundo (alpha=0.8) ==========
        n, bins, patches = ax.hist(data, bins=50, density=True, 
                                   alpha=0.8,
                                   color=COLORES_HIBRIDO['histograma'],  # #392840 (morado profundo)
                                   edgecolor=COLORES_HIBRIDO['borde'],    # #3F0340 (muy oscuro)
                                   linewidth=1.2)
        
        # ========== KDE SUPERPUESTO - Marrón Dorado + Dorado Vibrante ==========
        try:
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(data)
            xs = np.linspace(data.min(), data.max(), 300)
            
            # KDE con área rellena (marrón dorado, transparencia 30% - AJUSTE FINAL)
            ax.fill_between(xs, kde(xs),
                           alpha=0.3,
                           color=COLORES_HIBRIDO['kde_area'],  # #8C5C03 (marrón dorado)
                           label='KDE')
            
            # Línea de contorno del KDE (dorado vibrante, grosor aumentado - AJUSTE FINAL)
            ax.plot(xs, kde(xs),
                   color=COLORES_HIBRIDO['kde_linea'],  # #F2B544 (dorado vibrante)
                   linewidth=3.8,
                   alpha=0.9)
        except Exception as e:
            print(f"  ⚠️  Error al calcular KDE para {var}: {e}")
        
        # ========== MEDIA - Púrpura Intenso ==========
        mean_val = data.mean()
        ax.axvline(mean_val,
                  color=COLORES_HIBRIDO['media'],  # #5C025D (púrpura intenso)
                  linestyle='--',
                  linewidth=3.5,
                  label=f'Media: {mean_val:.1f}',
                  zorder=3,
                  alpha=0.95)
        
        # ========== MEDIANA - Magenta ==========
        median_val = data.median()
        ax.axvline(median_val,
                  color=COLORES_HIBRIDO['mediana'],  # #AA03C0 (magenta)
                  linestyle='-',
                  linewidth=3.5,
                  label=f'Mediana: {median_val:.1f}',
                  zorder=3,
                  alpha=0.95)
        
        # ========== ETIQUETA APA 7 EN TÍTULO ==========
        label = chr(97 + idx)  # a, b, c, d, e, f
        
        ax.set_xlabel(NOMBRES_AMIGABLES.get(var, var),
                      fontsize=11, fontweight='bold')
        ax.set_ylabel('Densidad', fontsize=11)
        ax.set_title(f'({label}) {NOMBRES_AMIGABLES.get(var, var)}\n(n={len(data):,}, CV={data.std()/data.mean()*100:.1f}%)',
                     fontsize=12, fontweight='bold')
        
        # ========== AJUSTES DE EJES SEGÚN VARIABLE ==========
        # Limitar eje X para variables específicas (mejorar zoom en datos relevantes)
        if var == 'Superavit_calorico_basal':
            ax.set_xlim(0, 250)  # Reducir a 250% (foco en datos típicos)
        elif var == 'Actividad_relativa':
            ax.set_xlim(0, 0.8)  # Reducir a 0.8 (foco en rango normal)
        
        ax.legend(loc='best', fontsize=9.5, framealpha=0.95)
        ax.grid(True, alpha=0.25, color=COLORES_HIBRIDO['grid'], linewidth=0.8)
        ax.set_axisbelow(True)
    
    # Ocultar ejes sobrantes
    for idx in range(n_vars, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout(pad=1.5)
    output_file = output_dir / 'hibrido_histograma_kde_6_variables.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✅ {output_file.name} generado (Híbrido 6V + Paleta Custom)")
    
    return output_file


def plot_kde_puro_8_variables(df, variables, output_dir):
    """
    KDE Puro (SIN HISTOGRAMA) - 8 Variables con Paleta Captura Custom
    
    Genera gráficos de densidad KDE suaves (sin barras de histograma)
    para las 8 variables clave, aplicando técnica moderna de visualización
    y Paleta Captura Custom (naranja dorado + púrpuras).
    
    Técnica: sns.kdeplot() con fill=True, curvas suaves, sin bins
    Paleta: Captura Custom (#F1B253, #94268F, #5C025D, #C19A6B)
    """
    print("📊 Generando KDE Puro (sin histograma, 8 variables)...")
    
    # ============ PALETA CAPTURA CUSTOM ============
    PALETA_CAPTURA_CUSTOM = {
        'purpura_intenso': '#5C025D',
        'purpura_brillante': '#94268F',
        'naranja_dorado': '#F1B253',
        'marron_claro': '#C19A6B',
        'purpura_apagado': '#6A3877',
        'beige_claro': '#ECE1D3'
    }
    
    COLORES_USO_CAPTURA = {
        'kde_area': PALETA_CAPTURA_CUSTOM['purpura_brillante'],     # #94268F
        'kde_linea': PALETA_CAPTURA_CUSTOM['purpura_intenso'],      # #5C025D
        'media': PALETA_CAPTURA_CUSTOM['naranja_dorado'],           # #F1B253 ⭐
        'mediana': PALETA_CAPTURA_CUSTOM['marron_claro'],           # #C19A6B
        'borde': PALETA_CAPTURA_CUSTOM['purpura_intenso'],          # #5C025D
        'grid': PALETA_CAPTURA_CUSTOM['beige_claro']                # #ECE1D3
    }
    # ==================================================
    
    n_vars = len(variables)
    n_cols = 2
    n_rows = (n_vars + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows))
    axes = axes.flatten() if n_vars > 1 else [axes]
    
    fig.suptitle('Distribuciones de Variables Clave (Nivel Diario)\nDensidad KDE - Paleta Captura Custom',
                 fontsize=16, fontweight='bold', y=0.995)
    
    for idx, var in enumerate(variables):
        ax = axes[idx]
        
        if var not in df.columns:
            ax.text(0.5, 0.5, f'{var}\nNo disponible',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue
        
        data = df[var].dropna()
        
        if len(data) < 10:
            ax.text(0.5, 0.5, f'{var}\nDatos insuficientes',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue
        
        # ========== KDE PURO CON ÁREA RELLENA (SIN HISTOGRAMA) ==========
        sns.kdeplot(data=data, ax=ax,
                   fill=True,
                   color=COLORES_USO_CAPTURA['kde_area'],  # #94268F (púrpura brillante)
                   alpha=0.6,
                   linewidth=0,  # Sin línea de borde (solo área)
                   label='Densidad KDE')
        
        # Línea de contorno del KDE (más oscura)
        sns.kdeplot(data=data, ax=ax,
                   fill=False,
                   color=COLORES_USO_CAPTURA['kde_linea'],  # #5C025D (púrpura intenso)
                   linewidth=3,
                   label=None)  # No duplicar en leyenda
        
        # ========== MEDIA Y MEDIANA CON COLORES CAPTURA ==========
        mean_val = data.mean()
        median_val = data.median()
        
        ax.axvline(mean_val,
                  color=COLORES_USO_CAPTURA['media'],  # #F1B253 (naranja dorado) ⭐
                  linestyle='--',
                  linewidth=3,
                  label=f'Media: {mean_val:.1f}',
                  zorder=3)
        
        ax.axvline(median_val,
                  color=COLORES_USO_CAPTURA['mediana'],  # #C19A6B (marrón claro)
                  linestyle='-',
                  linewidth=3,
                  label=f'Mediana: {median_val:.1f}',
                  zorder=3)
        
        # ========== ETIQUETA APA 7 EN TÍTULO ==========
        label = chr(97 + idx)  # a, b, c, d, e, f, g, h
        
        ax.set_xlabel(NOMBRES_AMIGABLES.get(var, var),
                      fontsize=11, fontweight='bold')
        ax.set_ylabel('Densidad', fontsize=11)
        ax.set_title(f'({label}) {NOMBRES_AMIGABLES.get(var, var)}\n(n={len(data):,}, CV={data.std()/data.mean()*100:.1f}%)',
                     fontsize=12, fontweight='bold')
        
        ax.legend(loc='best', fontsize=9, framealpha=0.95)
        ax.grid(True, alpha=0.25, color=COLORES_USO_CAPTURA['grid'], linewidth=0.8)
        ax.set_axisbelow(True)
    
    # Ocultar ejes sobrantes
    for idx in range(n_vars, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout(pad=1.5)
    output_file = output_dir / 'kde_puro_8_variables_captura_custom.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✅ {output_file.name} generado (KDE Puro 8V + Paleta Captura Custom)")
    
    return output_file


def plot_histogramas_con_kde_original(df, variables, output_dir):
    """
    Histogramas con KDE - VERSIÓN APA 7 CON PALETA FACULTAD
    
    Genera histogramas con curvas KDE para múltiples variables,
    aplicando etiquetas (a), (b), (c)... según convención APA 7
    y colores oficiales de la Facultad de Medicina y Ciencias Biomédicas.
    """
    print("📊 Generando histogramas con KDE (APA 7 + paleta facultad)...")
    
    # ============ COLORES OFICIALES FACULTAD ============
    COLORES_FACULTAD = {
        'morado_oscuro': '#571E72',
        'magenta': '#AA03C0',
        'morado_medio': '#A733EA',
        'rosa_purpura': '#A4579F',
        'dorado': '#D0A433',
        'crema_claro': '#FEF7CD',
        'crema': '#F1F0D9',
        'morado_oscuro2': '#750CA3'
    }
    
    COLORES_USO = {
        'histograma': COLORES_FACULTAD['morado_medio'],
        'kde': COLORES_FACULTAD['magenta'],
        'media': COLORES_FACULTAD['dorado'],
        'mediana': COLORES_FACULTAD['morado_oscuro'],
        'borde': COLORES_FACULTAD['morado_oscuro'],
        'grid': COLORES_FACULTAD['crema']
    }
    # ==================================================

    n_vars = len(variables)
    n_cols = 2
    n_rows = (n_vars + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows))
    axes = axes.flatten() if n_vars > 1 else [axes]

    fig.suptitle('Distribuciones de Variables Clave (Nivel Diario)\nHistogramas + Densidad (KDE)',
                 fontsize=16, fontweight='bold', y=0.995)

    for idx, var in enumerate(variables):
        ax = axes[idx]

        if var not in df.columns:
            ax.text(0.5, 0.5, f'{var}\nNo disponible',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue

        data = df[var].dropna()

        if len(data) < 10:
            ax.text(0.5, 0.5, f'{var}\nDatos insuficientes',
                    ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            continue

        # ========== HISTOGRAMA CON COLORES FACULTAD ==========
        ax.hist(data, bins=50, density=True, alpha=0.7,
                color=COLORES_USO['histograma'],  # #A733EA
                edgecolor=COLORES_USO['borde'],    # #571E72
                linewidth=1.5)

        # ========== KDE CON COLOR FACULTAD ==========
        try:
            from scipy.stats import gaussian_kde
            density = gaussian_kde(data)
            xs = np.linspace(data.min(), data.max(), 200)
            ax.plot(xs, density(xs),
                   color=COLORES_USO['kde'],  # #AA03C0
                   linewidth=2.5,
                   label='KDE')
        except:
            pass

        # ========== MEDIA Y MEDIANA CON COLORES FACULTAD ==========
        mean_val = data.mean()
        median_val = data.median()
        
        ax.axvline(mean_val,
                  color=COLORES_USO['media'],     # #D0A433
                  linestyle='--',
                  linewidth=2,
                  label=f'Media: {mean_val:.1f}')
        
        ax.axvline(median_val,
                  color=COLORES_USO['mediana'],   # #571E72
                  linestyle='--',
                  linewidth=2,
                  label=f'Mediana: {median_val:.1f}')

        # ========== ⭐ ETIQUETA APA 7 EN TÍTULO (CORREGIDO) ==========
        label = chr(97 + idx)  # a, b, c, d, e, f, g, h
        
        ax.set_xlabel(NOMBRES_AMIGABLES.get(var, var),
                      fontsize=11, fontweight='bold')
        ax.set_ylabel('Densidad', fontsize=11)
        ax.set_title(f'({label}) {NOMBRES_AMIGABLES.get(var, var)}\n(n={len(data):,}, CV={data.std()/data.mean()*100:.1f}%)',
                     fontsize=12, fontweight='bold')
        
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3, color=COLORES_USO['grid'])  # #F1F0D9

    # Ocultar ejes sobrantes
    for idx in range(n_vars, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout(pad=1.5)
    output_file = output_dir / 'histogramas_con_kde.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✅ {output_file.name} regenerado (APA 7 + paleta facultad)")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print("🔬 ANÁLISIS DESCRIPTIVO ACTUALIZADO + VISUALIZACIONES PROFESIONALES")
    print("=" * 80)
    print()

    # Cargar datos
    try:
        df_consolidado = cargar_datos_consolidados()
    except FileNotFoundError:
        print(
            "⚠️  Archivo consolidado no encontrado, intentando con archivos individuales...")
        df_consolidado = cargar_datos_individuales()

    # Calcular estadísticos descriptivos
    print("\n📊 Calculando estadísticos descriptivos...")
    df_stats = calcular_estadisticos_descriptivos(
        df_consolidado, VARIABLES_CLAVE)

    # Exportar tabla
    output_csv = OUTPUT_DIR / "tabla_descriptivos_actualizados.csv"
    output_tex = OUTPUT_DIR / "tabla_descriptivos_actualizados.tex"

    df_stats.to_csv(output_csv, index=False)
    print(f"✅ Tabla CSV: {output_csv.name}")

    exportar_tabla_latex(df_stats, output_tex)

    # Mostrar tabla en consola
    print("\n" + "=" * 80)
    print("📋 ESTADÍSTICOS DESCRIPTIVOS ACTUALIZADOS")
    print("=" * 80)
    print(df_stats.to_string(index=False))
    print()

    # Generar visualizaciones
    print("\n" + "=" * 80)
    print("🎨 GENERANDO VISUALIZACIONES PROFESIONALES")
    print("=" * 80)
    print()

    plot_violin_por_usuario(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
    plot_grouped_bar_medianas(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
    plot_heatmap_temporal(df_consolidado, OUTPUT_DIR)
    plot_scatter_matrix(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
    plot_boxplots_comparativos(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
    
    # Versión híbrida óptima: Histograma + KDE (6 variables clave) ⭐ RECOMENDADA
    plot_hibrido_histograma_kde_6_variables(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
    
    # Versiones alternativas (comentadas, disponibles si se necesitan):
    # plot_kde_puro_8_variables(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
    # plot_kde_multi_distribucion(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
    # plot_histogramas_con_kde_original(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
    
    plot_time_series_ultimos_90_dias(
        df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)

    # Resumen final
    print("\n" + "=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)
    print(f"📂 Directorio de salida: {OUTPUT_DIR}")
    print(f"📊 Tabla CSV: tabla_descriptivos_actualizados.csv")
    print(f"📄 Tabla LaTeX: tabla_descriptivos_actualizados.tex")
    print(
        f"🎨 Figuras generadas: {len(list(OUTPUT_DIR.glob('*.png')))} archivos PNG")
    print()
    print("🎯 Listo para integrar al Capítulo 4 del Informe LaTeX")
    print("=" * 80)


if __name__ == "__main__":
    main()
