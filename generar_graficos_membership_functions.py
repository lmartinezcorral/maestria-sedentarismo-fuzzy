#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENERADOR DE GRÁFICOS DE FUNCIONES DE MEMBRESÍA
Paso 7D: Visualización de MF Triangulares

Genera 4 gráficos (uno por variable de entrada) mostrando las funciones de membresía
triangulares (Baja, Media, Alta) en unidades originales.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json

# ===========================
# CONFIGURACIÓN
# ===========================

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'fuzzy' / 'plots'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuración de las funciones de membresía (extraída del YAML)
MF_CONFIG = {
    'Actividad_relativa_p50': {
        'labels': ['Baja', 'Media', 'Alta'],
        'values': {
            'Baja': [0.0702380952380952, 0.0954545454545454, 0.11740692640692636],
            'Media': [0.1108695652173913, 0.1309523809523809, 0.15378917378917376],
            'Alta': [0.1477777777777777, 0.1653846153846153, 0.1949477124183006]
        },
        'percentiles': {
            'Baja': [10, 25, 40],
            'Media': [35, 50, 65],
            'Alta': [60, 75, 90]
        },
        'range': [0.056, 0.216],
        'unit': 'Proporción (min/hora)',
        'interpretation': 'Mayor = más activo = MENOR sedentarismo',
        'colors': ['#d62728', '#ff7f0e', '#2ca02c']  # Rojo, Naranja, Verde
    },
    'Superavit_calorico_basal_p50': {
        'labels': ['Bajo', 'Medio', 'Alto'],
        'values': {
            'Bajo': [17.179945460943, 22.12879310344828, 25.76426115448968],
            'Medio': [24.48119050510746, 28.39616285554936, 33.452841048522025],
            'Alto': [31.59458337981037, 39.04379252649191, 51.031467826519595]
        },
        'percentiles': {
            'Bajo': [10, 25, 40],
            'Medio': [35, 50, 65],
            'Alto': [60, 75, 90]
        },
        'range': [14.0, 57.0],
        'unit': '% del TMB',
        'interpretation': 'Mayor = más gasto energético = MENOR sedentarismo',
        'colors': ['#d62728', '#ff7f0e', '#2ca02c']
    },
    'HRV_SDNN_p50': {
        'labels': ['Baja', 'Media', 'Alta'],
        'values': {
            'Baja': [30.724249500000003, 36.2839, 44.46637166666667],
            'Media': [41.5502, 49.08068333333333, 54.58566814285715],
            'Alta': [52.64108, 58.24823333333333, 64.35926000000002]
        },
        'percentiles': {
            'Baja': [10, 25, 40],
            'Media': [35, 50, 65],
            'Alta': [60, 75, 90]
        },
        'range': [28.5, 69.0],
        'unit': 'ms',
        'interpretation': 'Mayor = mejor tono vagal = MENOR sedentarismo',
        'colors': ['#d62728', '#ff7f0e', '#2ca02c']
    },
    'Delta_cardiaco_p50': {
        'labels': ['Baja Carga', 'Media Carga', 'Alta Carga'],
        'values': {
            'Baja Carga': [33.0, 37.5, 41.0],
            'Media Carga': [39.5, 43.0, 46.0],
            'Alta Carga': [45.0, 48.25, 54.0]
        },
        'percentiles': {
            'Baja Carga': [10, 25, 40],
            'Media Carga': [35, 50, 65],
            'Alta Carga': [60, 75, 90]
        },
        'range': [31.0, 59.0],
        'unit': 'lpm',
        'interpretation': 'Mayor = mejor respuesta cardíaca = MENOR sedentarismo',
        # Verde, Naranja, Rojo (invertido)
        'colors': ['#2ca02c', '#ff7f0e', '#d62728']
    }
}

# ===========================
# FUNCIÓN PARA CALCULAR MF TRIANGULAR
# ===========================


def triangular_mf(x, a, b, c):
    """
    Función de membresía triangular.

    Parámetros:
        x: valor de entrada (puede ser array)
        a, b, c: puntos de la función triangular (izq, pico, der)

    Retorna:
        Grado de membresía μ(x) ∈ [0, 1]
    """
    x = np.atleast_1d(x)
    y = np.zeros_like(x, dtype=float)

    # Pendiente ascendente (a → b)
    mask1 = (x >= a) & (x < b)
    if b > a:
        y[mask1] = (x[mask1] - a) / (b - a)

    # Pico (en b)
    mask2 = (x == b)
    y[mask2] = 1.0

    # Pendiente descendente (b → c)
    mask3 = (x > b) & (x <= c)
    if c > b:
        y[mask3] = (c - x[mask3]) / (c - b)

    return y

# ===========================
# FUNCIÓN PARA GRAFICAR MF
# ===========================


def plot_membership_functions(feature_name, config, output_dir):
    """
    Genera gráfico de funciones de membresía para una variable.
    """
    labels = config['labels']
    values = config['values']
    percentiles = config['percentiles']
    x_range = config['range']
    unit = config['unit']
    interpretation = config['interpretation']
    colors = config['colors']

    # Crear rango de valores para eje X
    x = np.linspace(x_range[0] - 5, x_range[1] + 5, 500)

    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 7))

    # Graficar cada función de membresía
    for idx, label in enumerate(labels):
        a, b, c = values[label]
        y = triangular_mf(x, a, b, c)

        # Línea de la MF
        ax.plot(x, y, linewidth=2.5, color=colors[idx],
                label=f'{label} (p{percentiles[label][0]}-p{percentiles[label][1]}-p{percentiles[label][2]})',
                alpha=0.9)

        # Rellenar área bajo la curva
        ax.fill_between(x, 0, y, color=colors[idx], alpha=0.15)

        # Marcar puntos clave (a, b, c)
        ax.plot([a, b, c], [0, 1, 0], 'o', color=colors[idx],
                markersize=8, markeredgewidth=1.5, markeredgecolor='white')

        # Anotaciones con valores
        ax.annotate(f'{b:.3f}', xy=(b, 1.0), xytext=(b, 1.1),
                    ha='center', fontsize=9, color=colors[idx], fontweight='bold')

    # Configuración del gráfico
    ax.set_xlim([x_range[0] - 2, x_range[1] + 2])
    ax.set_ylim([-0.05, 1.25])
    ax.set_xlabel(f'{feature_name.replace("_p50", "").replace("_", " ").title()} ({unit})',
                  fontsize=13, fontweight='bold')
    ax.set_ylabel('Grado de Membresía μ(x)', fontsize=13, fontweight='bold')

    # Título con interpretación
    title_main = f'Funciones de Membresía: {feature_name.replace("_p50", "").replace("_", " ").title()}'
    ax.set_title(title_main, fontsize=15, fontweight='bold', pad=15)

    # Subtítulo con interpretación clínica
    ax.text(0.5, 1.18, interpretation,
            transform=ax.transAxes, ha='center', fontsize=10,
            style='italic', color='#555', bbox=dict(boxstyle='round,pad=0.5',
                                                    facecolor='lightyellow', alpha=0.7, edgecolor='gray', linewidth=1))

    # Leyenda
    ax.legend(loc='upper left', fontsize=11, framealpha=0.95,
              edgecolor='gray', fancybox=True, shadow=True)

    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
    ax.axhline(y=0, color='black', linewidth=1.2)
    ax.axhline(y=1, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)

    # Estilo
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Guardar
    filename = f'MF_{feature_name}.png'
    filepath = output_dir / filename
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Guardado: {filepath.name}")
    plt.close()

# ===========================
# MAIN
# ===========================


def main():
    print("=" * 80)
    print("GENERACIÓN DE GRÁFICOS DE FUNCIONES DE MEMBRESÍA")
    print("=" * 80)
    print(f"Directorio de salida: {OUTPUT_DIR}")
    print()

    # Generar gráfico para cada variable
    for feature_name, config in MF_CONFIG.items():
        print(f"📊 Generando gráfico: {feature_name}")
        plot_membership_functions(feature_name, config, OUTPUT_DIR)

    print()
    print("=" * 80)
    print("✅ GRÁFICOS GENERADOS EXITOSAMENTE")
    print("=" * 80)
    print(f"\n📁 Archivos guardados en: {OUTPUT_DIR}")
    print(f"   - MF_Actividad_relativa_p50.png")
    print(f"   - MF_Superavit_calorico_basal_p50.png")
    print(f"   - MF_HRV_SDNN_p50.png")
    print(f"   - MF_Delta_cardiaco_p50.png")
    print()
    print("📌 Los gráficos están listos para incluir en el informe de tesis.")


if __name__ == '__main__':
    main()


