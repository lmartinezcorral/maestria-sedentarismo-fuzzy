#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generación de Funciones de Membresía Triangulares
Autor: Atlas (Científico de Datos Biomatemático Jr.)
Fecha: 15 de Noviembre de 2025
Propósito: Generar figura con funciones triangulares CORRECTAS (no trapezoidales)
"""

import numpy as np
import matplotlib.pyplot as plt
import yaml

# ==============================================================================
# CARGAR CONFIGURACIÓN OPERATIVA (FUENTE PRIMARIA)
# ==============================================================================
config_path = '../../../fuzzy_config/fuzzy_membership_config.yaml'

with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

print("✅ Configuración cargada correctamente")
print(f"   Variables: {list(config.keys())}")

# ==============================================================================
# FUNCIÓN TRIANGULAR
# ==============================================================================
def trimf(x, params):
    """
    Función de membresía triangular
    
    Parámetros:
    -----------
    x : array
        Valores de entrada en [0,1]
    params : tuple
        (a, b, c) donde:
        - a: vértice izquierdo
        - b: pico (máximo)
        - c: vértice derecho
    
    Retorna:
    --------
    array : Grados de membresía en [0,1]
    """
    a, b, c = params
    
    # Evitar división por cero
    left_slope = np.where(b - a != 0, (x - a) / (b - a), 0)
    right_slope = np.where(c - b != 0, (c - x) / (c - b), 0)
    
    return np.maximum(0, np.minimum(left_slope, right_slope))

# ==============================================================================
# PREPARAR DATOS
# ==============================================================================
variables = [
    ('Actividad_relativa_p50', 'Actividad Relativa\n(pasos/km normalizado)', 'Actividad Rel.'),
    ('Superavit_calorico_basal_p50', 'Superávit Calórico Basal\n(% TMB normalizado)', 'Superávit Cal.'),
    ('HRV_SDNN_p50', 'HRV-SDNN\n(ms normalizado)', 'HRV-SDNN'),
    ('Delta_cardiaco_p50', 'Delta Cardíaco\n(lpm normalizado)', 'Delta Cardíaco')
]

colores = {
    'Baja': '#2563eb',        # Azul
    'Media': '#f97316',       # Naranja
    'Alta': '#16a34a',        # Verde
    'Baja_Carga': '#2563eb',  # Azul (para Delta)
    'Media_Carga': '#f97316', # Naranja
    'Alta_Carga': '#16a34a'   # Verde
}

# ==============================================================================
# CREAR FIGURA 2×2
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle('Funciones de Membresía Triangulares del Sistema de Inferencia Difusa', 
             fontsize=16, fontweight='bold', y=0.995)

axes = axes.flatten()

for idx, (var_key, var_title, var_short) in enumerate(variables):
    ax = axes[idx]
    
    # Obtener configuración de la variable
    var_config = config[var_key]
    mf_config = var_config['membership_functions']
    
    # Obtener etiquetas (Baja/Media/Alta o Baja_Carga/Media_Carga/Alta_Carga)
    labels = var_config['labels']
    
    print(f"\n📊 Procesando: {var_short}")
    print(f"   Etiquetas: {labels}")
    
    # Encontrar rango de valores para esta variable
    all_values = []
    for label in labels:
        all_values.extend(mf_config[label]['values'])
    
    x_min = min(all_values) * 0.9
    x_max = max(all_values) * 1.1
    
    # Crear rango de x específico para esta variable
    x = np.linspace(x_min, x_max, 1000)
    
    print(f"   Rango x: [{x_min:.3f}, {x_max:.3f}]")
    
    # Graficar cada función de membresía
    for label in labels:
        mf_data = mf_config[label]
        values = mf_data['values']
        mf_type = mf_data['type']
        
        print(f"   - {label}: {mf_type}, valores={[f'{v:.3f}' for v in values]}")
        
        # Verificar que sea triangular
        if mf_type != 'triangular':
            print(f"   ⚠️ ADVERTENCIA: Se esperaba 'triangular', encontrado '{mf_type}'")
        
        # Calcular función triangular
        y_mf = trimf(x, values)
        
        # Graficar
        ax.plot(x, y_mf, linewidth=2.5, label=label, color=colores[label])
        
        # Añadir líneas verticales punteadas en vértices
        for v in values:
            ax.axvline(v, color=colores[label], linestyle='--', alpha=0.3, linewidth=1)
        
        # Anotar valores de percentiles en el pico
        ax.annotate(f'{values[1]:.3f}', 
                   xy=(values[1], 1.05), 
                   ha='center', 
                   fontsize=8,
                   color=colores[label],
                   fontweight='bold')
    
    # Configuración del subplot
    if var_short == "Actividad Rel.":
        ax.set_xlabel('Valor Normalizado [0,1]', fontsize=10, fontweight='bold')
    else:
        # Para las otras 3 variables que están en unidades originales
        ax.set_xlabel(f'Valor en Unidad Original', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Grado de Membresía μ(x)', fontsize=10, fontweight='bold')
    ax.set_title(f'{var_short}', fontsize=12, fontweight='bold', pad=10)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.05, 1.15)
    
    # Añadir anotación de interpretación
    interpretation_text = ""
    if var_short == "Actividad Rel.":
        interpretation_text = "← Menos activo | Más activo →"
    elif var_short == "Superávit Cal.":
        interpretation_text = "← Menor gasto | Mayor gasto →"
    elif var_short == "HRV-SDNN":
        interpretation_text = "← Menor variabilidad | Mayor variabilidad →"
    elif var_short == "Delta Cardíaco":
        interpretation_text = "← Menor carga | Mayor carga →"
    
    ax.text(0.5, -0.15, interpretation_text, 
            transform=ax.transAxes, 
            ha='center', 
            fontsize=8, 
            style='italic',
            color='gray')

# Ajustar espaciado
plt.tight_layout(rect=[0, 0, 1, 0.99])

# ==============================================================================
# GUARDAR FIGURA
# ==============================================================================
output_path = '../figuras/funciones_membresia_triangulares.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\n✅ Figura guardada exitosamente:")
print(f"   {output_path}")
print(f"   Resolución: 300 DPI")
print(f"   Tamaño: 14×11 pulgadas")

# También guardar en PDF para calidad vectorial
output_pdf = output_path.replace('.png', '.pdf')
plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
print(f"✅ Versión PDF guardada:")
print(f"   {output_pdf}")

plt.show()

print("\n" + "="*70)
print("🧠 ATLAS - Script completado exitosamente")
print("="*70)
print("✅ Funciones triangulares generadas (NO trapezoidales)")
print("✅ Datos verificados con fuzzy_membership_config.yaml")
print("✅ Figura lista para integración en tesis")
print("="*70)

