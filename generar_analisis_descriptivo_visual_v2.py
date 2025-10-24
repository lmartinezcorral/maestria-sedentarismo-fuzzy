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
    Boxplots comparativos: Distribución de variables con outliers visibles.
    """
    print("📦 Generando boxplots comparativos...")

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

        bp = sns.boxplot(data=df_plot, x='Usuario', y=var, ax=ax, palette=USER_COLORS,
                         width=0.6, linewidth=1.5, showfliers=True, fliersize=3)

        # Superponer medias
        medias = df_plot.groupby('Usuario')[var].mean()
        usuarios = medias.index
        ax.scatter(range(len(usuarios)), medias.values, color='red', s=100, zorder=3,
                   marker='D', label='Media', edgecolors='black', linewidth=1.5)

        ax.set_xlabel('Usuario', fontsize=11, fontweight='bold')
        ax.set_ylabel(NOMBRES_AMIGABLES.get(var, var),
                      fontsize=11, fontweight='bold')
        ax.set_title(NOMBRES_AMIGABLES.get(var, var),
                     fontsize=12, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, axis='y', alpha=0.3)

    # Ocultar ejes sobrantes
    for idx in range(n_vars, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    output_file = output_dir / 'boxplots_comparativos.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ {output_file.name}")


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


def plot_histogramas_con_kde(df, variables, output_dir):
    """
    Histogramas con KDE: Distribuciones generales (todas las observaciones).
    """
    print("📊 Generando histogramas con KDE...")

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

        # Histograma + KDE
        ax.hist(data, bins=50, density=True, alpha=0.6,
                color='steelblue', edgecolor='black')

        try:
            from scipy.stats import gaussian_kde
            density = gaussian_kde(data)
            xs = np.linspace(data.min(), data.max(), 200)
            ax.plot(xs, density(xs), 'r-', linewidth=2, label='KDE')
        except:
            pass

        # Estadísticos superpuestos
        mean_val = data.mean()
        median_val = data.median()
        ax.axvline(mean_val, color='orange', linestyle='--',
                   linewidth=2, label=f'Media: {mean_val:.1f}')
        ax.axvline(median_val, color='green', linestyle='--',
                   linewidth=2, label=f'Mediana: {median_val:.1f}')

        ax.set_xlabel(NOMBRES_AMIGABLES.get(var, var),
                      fontsize=11, fontweight='bold')
        ax.set_ylabel('Densidad', fontsize=11)
        ax.set_title(f'{NOMBRES_AMIGABLES.get(var, var)}\n(n={len(data):,}, CV={data.std()/data.mean()*100:.1f}%)',
                     fontsize=12, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)

    # Ocultar ejes sobrantes
    for idx in range(n_vars, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    output_file = output_dir / 'histogramas_con_kde.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ {output_file.name}")


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
    plot_histogramas_con_kde(df_consolidado, VARIABLES_CLAVE, OUTPUT_DIR)
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
