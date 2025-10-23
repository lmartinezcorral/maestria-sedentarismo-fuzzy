# -*- coding: utf-8 -*-
"""
analisis_corr_var.py

Qué hace:
1) Carga todos los archivos DB_final_v3_u*.csv
2) Para cada archivo:
   - Selecciona sólo columnas numéricas (no toca valores)
   - Calcula correlaciones Pearson y Spearman (pairwise, NaN-safe)
   - Calcula métricas de variabilidad por variable
   - Guarda CSVs y heatmaps
3) Crea resúmenes comparativos entre archivos:
   - comparativo_variabilidad.csv  (todas las variables x archivo)
   - comparativo_correlacion_flat.csv (pares de variables x archivo)

Requisitos: pandas, numpy, matplotlib (seaborn opcional).
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Si tienes seaborn instalado, se usa para heatmaps; si no, caemos a matplotlib puro
try:
    import seaborn as sns
    HAVE_SEABORN = True
except Exception:
    HAVE_SEABORN = False

# -------- Configuración --------
PATRON_ARCHIVOS = "DB_final_v3_u*.csv"   # ajusta si es necesario
OUT_DIR = "analisis_u"                   # carpeta de salida
os.makedirs(OUT_DIR, exist_ok=True)

# Si quieres analizar sólo un subconjunto de columnas, pon aquí sus nombres.
# Deja en None para usar TODAS las numéricas.
# p.ej.: ["Numero_pasos_por_dia","FCr_promedio_diario","HRV_SDNN"]
COLUMNAS_INTERES = None

# -------- Utilidades --------
MAD_SCALE = 1.4826  # para hacer MAD comparable a sigma bajo normalidad


def robust_mad(x: pd.Series) -> float:
    """MAD escalado (1.4826 * mediana(|x - mediana(x)|)). Ignora NaN."""
    med = x.median(skipna=True)
    mad = (x - med).abs().median(skipna=True)
    return float(MAD_SCALE * mad)


def make_heatmap(corr: pd.DataFrame, title: str, outpath: str):
    """Guarda un heatmap de la matriz de correlación con valores anotados."""
    plt.figure(figsize=(14, 12))
    if HAVE_SEABORN:
        # Anotar con valores (fmt=".2f" para 2 decimales)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                    vmin=-1, vmax=1, square=True, cbar=True,
                    cbar_kws={"shrink": 0.8}, annot_kws={"size": 8})
    else:
        plt.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
        plt.colorbar()
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.index)), corr.index)
        # Anotar manualmente sin seaborn
        for i in range(len(corr.index)):
            for j in range(len(corr.columns)):
                val = corr.iloc[i, j]
                if not np.isnan(val):
                    plt.text(j, i, f'{val:.2f}', ha='center', va='center',
                             color='white' if abs(val) > 0.5 else 'black',
                             fontsize=8)
    plt.title(title, fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def flatten_corr(corr_pearson: pd.DataFrame, corr_spearman: pd.DataFrame, archivo: str) -> pd.DataFrame:
    """Convierte matrices de correlación en tabla larga (pares únicos i<j)."""
    cols = corr_pearson.columns
    rows = []
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            v1, v2 = cols[i], cols[j]
            rows.append({
                "archivo": archivo,
                "var1": v1,
                "var2": v2,
                "pearson": corr_pearson.iloc[i, j],
                "spearman": corr_spearman.loc[v1, v2]
            })
    return pd.DataFrame(rows)


def analizar_archivo(path_csv: str):
    """Corre correlación y variabilidad para un archivo y guarda resultados."""
    nombre = os.path.splitext(os.path.basename(path_csv))[0]
    print(f"\n=== Analizando: {nombre} ===")

    # Cargar
    df = pd.read_csv(path_csv)

    # Quedarnos con columnas numéricas
    num = df.select_dtypes(include=[np.number]).copy()

    # Subconjunto, si se definió
    if COLUMNAS_INTERES is not None:
        existen = [c for c in COLUMNAS_INTERES if c in num.columns]
        if not existen:
            print(
                f"[AVISO] Ninguna de COLUMNAS_INTERES está en {nombre}. Se usan todas las numéricas.")
        else:
            num = num[existen].copy()

    # Remover columnas constantes (std=0) para evitar filas/columnas NaN en corr
    const_cols = [c for c in num.columns if pd.api.types.is_numeric_dtype(
        num[c]) and num[c].nunique(dropna=True) <= 1]
    if const_cols:
        print(
            f"[Nota] Columnas constantes removidas de la correlación (se mantienen en variabilidad): {const_cols}")
        num_corr = num.drop(columns=const_cols)
    else:
        num_corr = num

    # ---- Correlaciones (pairwise, sin tocar valores) ----
    if num_corr.shape[1] >= 2:
        corr_pearson = num_corr.corr(method="pearson", min_periods=1)
        corr_spearman = num_corr.corr(method="spearman", min_periods=1)

        corr_p_csv = os.path.join(OUT_DIR, f"{nombre}_corr_pearson.csv")
        corr_s_csv = os.path.join(OUT_DIR, f"{nombre}_corr_spearman.csv")
        corr_pearson.to_csv(corr_p_csv)
        corr_spearman.to_csv(corr_s_csv)

        # Heatmaps
        make_heatmap(
            corr_pearson, f"Pearson - {nombre}", os.path.join(OUT_DIR, f"{nombre}_heatmap_pearson.png"))
        make_heatmap(corr_spearman, f"Spearman - {nombre}", os.path.join(
            OUT_DIR, f"{nombre}_heatmap_spearman.png"))

        # Tabla larga de pares
        corr_flat = flatten_corr(corr_pearson, corr_spearman, nombre)
    else:
        print(
            f"[AVISO] {nombre}: <2 columnas numéricas válidas para correlación.")
        corr_flat = pd.DataFrame(
            columns=["archivo", "var1", "var2", "pearson", "spearman"])

    # ---- Variabilidad (descriptivos) ----
    stats_rows = []
    for col in num.columns:
        s = num[col]
        # Descriptivos sin modificar el vector (dropna se usa sólo para el cálculo)
        stats_rows.append({
            "archivo": nombre,
            "variable": col,
            "count": int(s.count()),
            "mean": float(s.mean(skipna=True)),
            "std": float(s.std(skipna=True)),
            "var": float(s.var(skipna=True)),
            "min": float(s.min(skipna=True)),
            "p10": float(s.quantile(0.10)),
            "median": float(s.median(skipna=True)),
            "p90": float(s.quantile(0.90)),
            "max": float(s.max(skipna=True)),
            "iqr": float(s.quantile(0.75) - s.quantile(0.25)),
            "cv": float(s.std(skipna=True) / s.mean(skipna=True)) if s.mean(skipna=True) not in (0, np.nan) else np.nan,
            "mad_scaled": robust_mad(s)
        })
    var_stats = pd.DataFrame(stats_rows)

    # Guardar variabilidad por archivo
    var_stats_path = os.path.join(OUT_DIR, f"{nombre}_variabilidad.csv")
    var_stats.to_csv(var_stats_path, index=False)

    # Top 10 pares por |Pearson|
    if not corr_flat.empty:
        top_pairs = corr_flat.assign(abs_pearson=lambda d: d["pearson"].abs())\
                             .sort_values("abs_pearson", ascending=False)\
                             .head(10)
        top_pairs.to_csv(os.path.join(
            OUT_DIR, f"{nombre}_top10_pares_pearson.csv"), index=False)

    return var_stats, corr_flat


# --------- Main ----------
all_var = []
all_corr = []

for path in sorted(glob.glob(PATRON_ARCHIVOS)):
    var_stats, corr_flat = analizar_archivo(path)
    all_var.append(var_stats)
    all_corr.append(corr_flat)

# Concatenados comparativos
if all_var:
    comparativo_var = pd.concat(all_var, ignore_index=True)
    comparativo_var.to_csv(os.path.join(
        OUT_DIR, "comparativo_variabilidad.csv"), index=False)
if all_corr:
    comparativo_corr = pd.concat(all_corr, ignore_index=True)
    comparativo_corr.to_csv(os.path.join(
        OUT_DIR, "comparativo_correlacion_flat.csv"), index=False)

print("\nListo. Resultados en la carpeta:", OUT_DIR)
