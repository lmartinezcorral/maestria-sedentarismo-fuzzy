"""
generar_analisis_robustez.py
============================

OBJETIVO:
---------
Generar figura analisis_robustez.png con gráfico de barras comparativo
Modelo Completo (4V) vs Modelo Reducido (2V)

COLORES APLICADOS:
------------------
- Modelo Completo (4V): #F1B253 (Naranja dorado)
- Modelo Reducido (2V): #5C025D (Púrpura intenso)

DATOS CERTIFICADOS:
-------------------
- Modelo 4V: F1=0.840, Recall=0.976, Precision=0.737, MCC=0.294
- Modelo 2V: F1=0.420, Recall=0.294, Precision=0.737, MCC=0.051
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'resultados_cap6' / 'plots'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_TESIS = BASE_DIR / '1_Edicion_tesis' / 'tesis_luisangel' / 'figuras'
OUTPUT_TESIS.mkdir(parents=True, exist_ok=True)

# ============================================================================
# COLORES DE LA PALETA
# ============================================================================

# Colores solicitados
COLOR_4V = '#F1B253'  # Naranja dorado (Modelo Completo)
COLOR_2V = '#5C025D'  # Púrpura intenso (Modelo Reducido)

# ============================================================================
# DATOS CERTIFICADOS
# ============================================================================

# Métricas del análisis de robustez (datos certificados)
metrics = ['F1-Score', 'Precision', 'Recall', 'MCC']
model_4v = [0.840, 0.737, 0.976, 0.294]  # Modelo Completo (4V)
model_2v = [0.420, 0.356, 0.521, -0.051]  # Modelo Reducido (2V)

# Diferencias porcentuales
deltas_pct = ['-50.0%', '-51.7%', '-46.6%', '-117.3%']

# ============================================================================
# GENERAR FIGURA
# ============================================================================

def generar_analisis_robustez():
    """Genera gráfico de barras comparativo Modelo 4V vs 2V"""
    
    print("="*80)
    print("GENERANDO FIGURA: analisis_robustez.png")
    print("="*80)
    print()
    
    # Configuración del gráfico
    x = np.arange(len(metrics))
    width = 0.35
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Barras agrupadas
    bars1 = ax.bar(x - width/2, model_4v, width, 
                   label='Modelo Completo (4V)',
                   color=COLOR_4V,  # #F1B253 - Naranja dorado
                   edgecolor='white', 
                   linewidth=2,
                   alpha=0.9)
    
    bars2 = ax.bar(x + width/2, model_2v, width,
                   label='Modelo Reducido (2V)',
                   color=COLOR_2V,  # #5C025D - Púrpura intenso
                   edgecolor='white',
                   linewidth=2,
                   alpha=0.9)
    
    # Anotaciones de valores en las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            # Ajustar posición del texto para valores negativos (MCC)
            if height < 0:
                y_text = height - 0.05
                va_text = 'top'
            else:
                y_text = height + 0.02
                va_text = 'bottom'
            
            ax.text(bar.get_x() + bar.get_width()/2., y_text,
                   f'{height:.3f}', 
                   ha='center', 
                   va=va_text, 
                   fontsize=11, 
                   fontweight='bold',
                   color='white' if height < 0.3 else 'black')
    
    # Anotaciones de diferencias porcentuales
    for i, delta in enumerate(deltas_pct):
        y_pos = max(model_4v[i], model_2v[i]) + 0.08
        if model_2v[i] < 0:  # Para MCC negativo
            y_pos = max(model_4v[i], abs(model_2v[i])) + 0.08
        
        color_delta = 'red' if '-' in delta and delta != '0.0%' else 'green'
        ax.text(i, y_pos, f'Δ = {delta}', 
               ha='center', 
               fontsize=10,
               color=color_delta,
               weight='bold',
               bbox=dict(boxstyle='round,pad=0.4', 
                        facecolor='white', 
                        edgecolor=color_delta,
                        linewidth=1.5,
                        alpha=0.9))
    
    # Etiquetas y título
    ax.set_ylabel('Valor de Métrica', fontsize=13, fontweight='bold')
    ax.set_xlabel('Métrica de Evaluación', fontsize=13, fontweight='bold')
    ax.set_title('Análisis de Robustez: Modelo Completo vs. Modelo Reducido',
                 fontsize=15, fontweight='bold', pad=20)
    
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=12, fontweight='bold')
    
    # Leyenda
    ax.legend(loc='upper right', 
             frameon=True, 
             edgecolor='black',
             fontsize=11,
             framealpha=0.95)
    
    # Límites del eje Y (ajustar para incluir valores negativos de MCC)
    y_min = min(min(model_2v), -0.1) if min(model_2v) < 0 else 0
    y_max = max(max(model_4v), max(model_2v)) + 0.15
    ax.set_ylim(y_min, y_max)
    
    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1)
    ax.set_axisbelow(True)
    
    # Línea de referencia en 0.5 (umbral de clasificador aleatorio)
    ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=1.5, 
              alpha=0.5, label='Umbral=0.5')
    
    # Línea de referencia en 0.0 (para MCC)
    ax.axhline(y=0.0, color='black', linestyle='-', linewidth=1, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar en directorio de análisis
    output_file_analisis = OUTPUT_DIR / 'analisis_robustez.png'
    fig.savefig(output_file_analisis, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Guardado: {output_file_analisis}")
    
    # Copiar a directorio de tesis
    output_file_tesis = OUTPUT_TESIS / 'analisis_robustez.png'
    fig.savefig(output_file_tesis, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Copiado a: {output_file_tesis}")
    
    plt.close(fig)
    
    print()
    print("="*80)
    print("✅ FIGURA GENERADA EXITOSAMENTE")
    print("="*80)
    print()
    print(f"Colores aplicados:")
    print(f"  - Modelo Completo (4V): {COLOR_4V} (Naranja dorado)")
    print(f"  - Modelo Reducido (2V): {COLOR_2V} (Púrpura intenso)")
    print()
    
    return output_file_tesis

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    generar_analisis_robustez()

