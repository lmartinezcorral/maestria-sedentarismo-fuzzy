# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 14:30:43 2025

@author: Usuario Asignado
"""


# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 11:53:21 2025

Autor: Usuario Asignado
Descripción: Calcula media, std y varianza de variables seleccionadas y
             grafica la desviación estándar para varios nombres.
"""

import matplotlib.pyplot as plt
import os
import pandas as pd

# === Nombres a procesar (reemplazan "Ale" en el nombre del archivo) ===
names = ["u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8", "u9", "u10"]

# === Variables a usar ===
features = [
    "Numero_horas_estacionarias",
    "Total_hrs_monitorizadas",
    "Total_min_de_ejercicio_diario",
    "FCr_promedio_diario",
    "Gasto_calorico_activo",
    "HRV_SDNN",
    "FC_al_caminar_promedio_diario",
    "Numero_pasos_por_dia",
    "distancia_caminada_en_km"
]

# Carpeta de salida opcional
OUT_DIR = "variabilidad"
os.makedirs(OUT_DIR, exist_ok=True)

for name in names:
    file_path = f"outputs_corr\\DB_final_v3_{name}_train__zero_clean.csv"
    print(f"\n=== Procesando: {file_path} ===")
    if not os.path.exists(file_path):
        print(f"[AVISO] No se encontró el archivo: {file_path}. Se omite.")
        continue

    # 1) Cargar datos
    df = pd.read_csv(file_path)

    # 2) Validar columnas y filtrar; si falta alguna, se ignora con aviso
    missing = [c for c in features if c not in df.columns]
    if missing:
        print(
            f"[AVISO] Faltan columnas en {name}: {missing}. Se usarán sólo las disponibles.")
    use_cols = [c for c in features if c in df.columns]
    if not use_cols:
        print(
            f"[AVISO] {name}: no hay columnas válidas para analizar. Se omite.")
        continue

    df_vars = df[use_cols].dropna()

    if df_vars.empty:
        print(
            f"[AVISO] {name}: después de dropna() no quedaron filas. Se omite.")
        continue

    # 3) Resumen (media, std, var) y orden por mayor variabilidad (std)
    resumen = pd.DataFrame({
        "mean": df_vars.mean(),
        "std": df_vars.std(),
        "var": df_vars.var()
    }).sort_values("std", ascending=False)

    print("\nResumen de estadísticas:")
    print(resumen.round(3))

    # 4) Gráfica de desviación estándar
    plt.figure(figsize=(8, 5))
    resumen["std"].plot(kind="bar", edgecolor="k")
    plt.title(f"Variabilidad de variables (std) - {name}")
    plt.ylabel("Desviación estándar")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out_png = os.path.join(OUT_DIR, f"variabilidad_variables_{name}.png")
    plt.savefig(out_png, dpi=150)
    plt.show()

    # (Opcional) guardar el resumen como CSV
    resumen.to_csv(os.path.join(OUT_DIR, f"resumen_variabilidad_{name}.csv"))
