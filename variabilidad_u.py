# -*- coding: utf-8 -*-
"""
variabilidad_u.py
Genera gráficos de variabilidad (desviación estándar) por usuario y
exporta un CSV con los std de cada variable.

- No hace limpieza (usa los datos tal cual).
- Busca archivos: DB_final_v3_u*.csv en la carpeta del script.
- Salida: ./analisis_u/variabilidad/std_<usuario>.csv
          ./analisis_u/variabilidad/variabilidad_variables_<usuario>.png
"""

from pathlib import Path
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------- Config -----------------
# Si quieres mapear u1..u10 a nombres, ponlos aquí (opcional):
ALIAS = {
    # "u1": "Ale", "u2": "Brenda", "u3": "Cristina", ...
}

# Variables que intentaremos graficar (si no existen en un archivo, se omiten)
VARIABLES_CLAVE = [
    "Gasto_calorico_activo",
    "Total_min_de_ejercicio_diario",
    "HRV_SDNN",
    "FCr_promedio_diario",
    "Total_hrs_monitorizadas",
    "Numero_horas_estacionarias",
    "Numero_pasos_por_dia",
    "distancia_caminada_en_km",
    "min_totales_en_movimiento",
    "FC_al_caminar_promedio_diario",
]

# Tamaño y DPI de las figuras
FIGSIZE = (12, 7)
DPI = 300
# ------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
PATRON_ARCHIVOS = str(SCRIPT_DIR / "DB_final_v3_u*.csv")
OUT_DIR = SCRIPT_DIR / "analisis_u" / "variabilidad"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def nombre_usuario_desde_archivo(path: Path) -> str:
    """Intenta sacar 'uX' del nombre y mapear a alias si existe."""
    stem = path.stem  # p.ej., DB_final_v3_u3
    # Busca el segmento 'uN'
    usuario = None
    for parte in stem.split("_"):
        if parte.startswith("u") and parte[1:].isdigit():
            usuario = parte
            break
    if usuario is None:
        usuario = stem  # fallback
    return ALIAS.get(usuario, usuario)


def anotar_barras(ax, valores):
    """Escribe el valor encima de cada barra."""
    for i, v in enumerate(valores):
        if np.isfinite(v):
            ax.text(i, v, f"{v:.2f}", ha="center",
                    va="bottom", fontsize=9, rotation=0)


def procesar_archivo(csv_path: str):
    path = Path(csv_path)
    usuario = nombre_usuario_desde_archivo(path)
    df = pd.read_csv(path)

    # Selección de columnas a analizar
    cols = [c for c in VARIABLES_CLAVE if c in df.columns]
    if not cols:
        # fallback: todas las numéricas excepto 'Fecha'
        cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cols = [c for c in cols if c.lower() != "fecha"]

    if not cols:
        print(
            f"[AVISO] {path.name}: no se encontraron columnas numéricas para analizar.")
        return

    # Desviación estándar (ddof=1, el default de pandas)
    std_series = df[cols].std().sort_values(ascending=False)

    # ---- CSV con std ----
    std_df = std_series.rename("std").to_frame()
    std_csv = OUT_DIR / f"std_{usuario}.csv"
    std_df.to_csv(std_csv, index=True)

    # ---- Figura ----
    fig, ax = plt.subplots(figsize=FIGSIZE)
    vals = std_series.values
    labels = std_series.index.tolist()

    ax.bar(range(len(vals)), vals)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("Desviación estándar")
    ax.set_title(f"Variabilidad de variables (std) - {usuario}")
    anotar_barras(ax, vals)
    fig.tight_layout()

    out_png = OUT_DIR / f"variabilidad_variables_{usuario}.png"
    fig.savefig(out_png, dpi=DPI)
    plt.close(fig)

    print(f"OK: {path.name} -> {out_png.name} / {std_csv.name}")


def main():
    files = sorted(glob.glob(PATRON_ARCHIVOS))
    if not files:
        print(
            f"[ERROR] No se encontraron archivos con el patrón:\n  {PATRON_ARCHIVOS}")
        return
    for f in files:
        procesar_archivo(f)
    print(f"\nListo. Resultados en: {OUT_DIR}")


if __name__ == "__main__":
    main()
