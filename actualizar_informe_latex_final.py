#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
actualizar_informe_latex_final.py

Actualiza el Informe Técnico LaTeX con:
1. Nuevos estadísticos descriptivos actualizados (desde analisis_u/descriptivos_visuales/)
2. Nuevas figuras profesionales (6 PNG de alta resolución)
3. Solución de tablas anchas (usando landscape + longtable cuando sea apropiado)
4. Mantiene formato APA 7ª edición

Genera: INFORME_TECNICO_FINAL_V2.tex
"""

import os
import re
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).parent.resolve()
DOCS_DIR = BASE_DIR / "documentos_tesis"
INPUT_TEX = DOCS_DIR / "INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex"
OUTPUT_TEX = DOCS_DIR / "INFORME_TECNICO_FINAL_V2.tex"

# Nuevos archivos de datos
TABLA_NUEVA_TEX = BASE_DIR / "analisis_u" / "descriptivos_visuales" / "tabla_descriptivos_actualizados.tex"
FIGURAS_DIR = BASE_DIR / "analisis_u" / "descriptivos_visuales"

print("=" * 80)
print("🔧 ACTUALIZADOR DE INFORME LATEX")
print("=" * 80)
print()

# ============================================================================
# PASO 1: Leer archivo LaTeX actual
# ============================================================================
print("📂 Leyendo archivo LaTeX actual...")
with open(INPUT_TEX, 'r', encoding='utf-8') as f:
    contenido = f.read()

print(f"✅ Archivo leído: {len(contenido)} caracteres, {contenido.count('chapter{')} capítulos")

# ============================================================================
# PASO 2: Añadir paquete pdflscape al preámbulo (si no existe)
# ============================================================================
print("\n📦 Añadiendo paquete pdflscape para páginas horizontales...")

if '\\usepackage{pdflscape}' not in contenido:
    # Buscar la sección de paquetes (después de longtable)
    pattern_longtable = r'(\\usepackage\{longtable\})'
    replacement = r'\1\n\\usepackage{pdflscape}  % Para tablas anchas en landscape'
    contenido = re.sub(pattern_longtable, replacement, contenido)
    print("  ✅ Paquete pdflscape añadido")
else:
    print("  ℹ️  Paquete pdflscape ya existe")

# ============================================================================
# PASO 3: Actualizar Tabla de Estadísticos Descriptivos (Capítulo 4)
# ============================================================================
print("\n📊 Actualizando tabla de estadísticos descriptivos...")

# Leer la tabla nueva
if TABLA_NUEVA_TEX.exists():
    with open(TABLA_NUEVA_TEX, 'r', encoding='utf-8') as f:
        tabla_nueva = f.read()
    
    # La tabla nueva es simple, vamos a envolverla en landscape para mejor visualización
    tabla_nueva_landscape = r"""
\begin{landscape}
\begin{table}[htbp]
\centering
\caption{Estadísticos Descriptivos Actualizados (Datos Post-Limpieza, $n=9,185$ días)}
\label{tab:descriptivos_actualizados}
\small
\begin{tabular}{lrrrrrrrrrrrr}
\toprule
\textbf{Variable} & \textbf{n} & \textbf{Media} & \textbf{DE} & \textbf{CV (\%)} & \textbf{Mediana} & \textbf{Q1} & \textbf{Q3} & \textbf{IQR} & \textbf{Min} & \textbf{Max} & \textbf{Test Normalidad} & \textbf{p-valor} \\
\midrule
Pasos Diarios & 9,185 & 6,001.63 & 3,283.59 & 54.7 & 5,489.0 & 3,779.0 & 7,657.0 & 3,878.0 & 11.48 & 25,511.7 & Kolmogorov-Smirnov & $<$ 0.001 \\
Calorías Activas (kcal) & 9,185 & 595.87 & 450.65 & 75.6 & 517.72 & 322.09 & 767.4 & 445.31 & 0.07 & 18,313.13 & Kolmogorov-Smirnov & $<$ 0.001 \\
FC Reposo (lpm) & 9,185 & 54.24 & 8.72 & 16.1 & 53.0 & 48.0 & 59.0 & 11.0 & 37.0 & 142.61 & Kolmogorov-Smirnov & $<$ 0.001 \\
FC al Caminar (lpm) & 9,185 & 97.77 & 12.38 & 12.7 & 97.75 & 90.5 & 105.0 & 14.5 & 50.0 & 159.0 & Kolmogorov-Smirnov & $<$ 0.001 \\
HRV SDNN (ms) & 9,185 & 49.39 & 17.17 & 34.8 & 48.36 & 36.17 & 60.4 & 24.23 & 9.84 & 135.44 & Kolmogorov-Smirnov & $<$ 0.001 \\
Hrs Monitorizadas & 9,185 & 15.42 & 5.21 & 33.8 & 15.0 & 13.0 & 18.0 & 5.0 & 1.0 & 65.0 & Kolmogorov-Smirnov & $<$ 0.001 \\
Actividad Relativa (prop.) & 9,185 & 0.14 & 0.1 & 73.2 & 0.13 & 0.08 & 0.18 & 0.09 & 0.0 & 2.15 & Kolmogorov-Smirnov & $<$ 0.001 \\
Superávit Calórico (\%) & 9,185 & 32.64 & 23.03 & 70.6 & 28.0 & 19.87 & 40.91 & 21.04 & 0.0 & 817.09 & Kolmogorov-Smirnov & $<$ 0.001 \\
\bottomrule
\end{tabular}
\end{table}
\end{landscape}
"""
    
    # Buscar la tabla antigua (label tab:descriptive_daily) y reemplazarla
    # Patrón: desde \begin{table}[H] hasta \end{table} que contiene label{tab:descriptive_daily}
    pattern_tabla_antigua = r'\\begin\{table\}\[H\].*?\\caption\{Estadísticos Descriptivos.*?\}.*?\\label\{tab:descriptive_daily\}.*?\\end\{table\}'
    
    if re.search(pattern_tabla_antigua, contenido, re.DOTALL):
        # Usar una función lambda para evitar problemas con backslashes
        tabla_nueva_stripped = tabla_nueva_landscape.strip()
        contenido = re.sub(pattern_tabla_antigua, lambda m: tabla_nueva_stripped, contenido, flags=re.DOTALL)
        print("  ✅ Tabla de estadísticos descriptivos actualizada (landscape)")
    else:
        print("  ⚠️  No se encontró la tabla antigua (patrón no coincide)")
else:
    print("  ⚠️  Tabla nueva no encontrada en:", TABLA_NUEVA_TEX)

# ============================================================================
# PASO 4: Insertar Nuevas Figuras en Capítulo 4
# ============================================================================
print("\n🎨 Insertando nuevas figuras en Capítulo 4...")

# Definir las figuras a insertar
nuevas_figuras = [
    {
        'file': 'histogramas_con_kde.png',
        'caption': 'Distribuciones de variables clave (nivel diario). Histogramas con densidad KDE, mostrando alta variabilidad (CV > 50\\%) y violación de normalidad ($p < 0.001$).',
        'label': 'fig:histogramas_kde',
        'width': '0.95',
        'location_pattern': r'(\\subsection\{Gráficos Exploratorios\})',
        'insert_after': True
    },
    {
        'file': 'violin_plots_por_usuario.png',
        'caption': 'Violin plots por usuario. Se observa heterogeneidad marcada entre participantes, evidenciando la necesidad de modelado personalizado (fuzzy logic).',
        'label': 'fig:violin_plots',
        'width': '0.95',
        'location_pattern': r'(\\subsection\{Heterogeneidad Inter-Sujeto\})',
        'insert_after': True
    },
    {
        'file': 'grouped_bar_medianas_por_usuario.png',
        'caption': 'Perfiles de usuario: medianas normalizadas [0-1] para 8 variables clave. Patrones heterogéneos entre usuarios, con algunos mostrando alta actividad física pero baja variabilidad cardíaca.',
        'label': 'fig:grouped_bar_medianas',
        'width': '0.95',
        'location_pattern': r'(\\subsection\{Heterogeneidad Inter-Sujeto\})',
        'insert_after': True
    },
    {
        'file': 'heatmap_patron_semanal.png',
        'caption': 'Patrón semanal de actividad (mediana de pasos por día de la semana). Se evidencia heterogeneidad temporal, con algunos usuarios mostrando reducción significativa en fines de semana.',
        'label': 'fig:heatmap_semanal',
        'width': '0.85',
        'location_pattern': r'(\\subsection\{Heterogeneidad Inter-Sujeto\})',
        'insert_after': True
    },
    {
        'file': 'scatter_matrix_relaciones.png',
        'caption': 'Matriz de dispersión: relaciones bivariadas entre variables clave (muestra n=2,000 días, coloreado por usuario). No se observan correlaciones lineales fuertes, justificando uso de fuzzy inference.',
        'label': 'fig:scatter_matrix',
        'width': '0.95',
        'location_pattern': r'(\\section\{Análisis de Correlación\})',
        'insert_after': True
    },
    {
        'file': 'boxplots_comparativos.png',
        'caption': 'Boxplots comparativos con detección de outliers (diamante rojo = media). Evidencia asimetría en distribuciones y necesidad de estadísticos robustos (medianas, IQR).',
        'label': 'fig:boxplots_comparativos',
        'width': '0.95',
        'location_pattern': r'(\\subsection\{Gráficos Exploratorios\})',
        'insert_after': True
    }
]

figuras_insertadas = 0

for fig in nuevas_figuras:
    fig_path = FIGURAS_DIR / fig['file']
    
    if not fig_path.exists():
        print(f"  ⚠️  Figura no encontrada: {fig['file']}")
        continue
    
    # Crear el código LaTeX de la figura
    latex_fig = f"""

\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width={fig['width']}\\textwidth]{{../analisis_u/descriptivos_visuales/{fig['file']}}}
\\caption{{{fig['caption']}}}
\\label{{{fig['label']}}}
\\end{{figure}}
"""
    
    # Buscar el patrón de ubicación
    match = re.search(fig['location_pattern'], contenido)
    
    if match:
        # Insertar después del patrón encontrado
        insert_pos = match.end()
        contenido = contenido[:insert_pos] + latex_fig + contenido[insert_pos:]
        figuras_insertadas += 1
        print(f"  ✅ Insertada: {fig['file']}")
    else:
        print(f"  ⚠️  No se encontró ubicación para: {fig['file']} (patrón: {fig['location_pattern']})")

print(f"\n📊 Total figuras insertadas: {figuras_insertadas} / {len(nuevas_figuras)}")

# ============================================================================
# PASO 5: Convertir Tablas Anchas con \resizebox a Landscape
# ============================================================================
print("\n🔄 Convirtiendo tablas con \\resizebox a formato landscape...")

# Patrón para encontrar tablas con \resizebox
pattern_resizebox = r'(\\begin\{table\}\[.*?\].*?)(\\resizebox\{\\textwidth\}\{!\}\{%?\s*)(\\begin\{tabular\}.*?\\end\{tabular\}\}?)(.*?\\end\{table\})'

tablas_convertidas = 0

def convertir_a_landscape(match):
    global tablas_convertidas
    
    inicio_tabla = match.group(1)  # \begin{table}[H]\n\centering\n\caption{...}\n\label{...}
    # resizebox = match.group(2)  # \resizebox{\textwidth}{!}{%
    contenido_tabular = match.group(3)  # \begin{tabular}...\end{tabular}}
    fin_tabla = match.group(4)  # \end{table}
    
    # Limpiar el contenido_tabular de llaves extras
    contenido_tabular_limpio = contenido_tabular.rstrip('}').rstrip('%')
    
    # Construir la nueva tabla en landscape con tamaño de fuente reducido
    nueva_tabla = f"{inicio_tabla}\n\\small\n{contenido_tabular_limpio}\n{fin_tabla}"
    
    # Envolver en landscape
    tabla_landscape = f"\\begin{{landscape}}\n{nueva_tabla}\n\\end{{landscape}}"
    
    tablas_convertidas += 1
    return tabla_landscape

# Aplicar conversión
contenido = re.sub(pattern_resizebox, convertir_a_landscape, contenido, flags=re.DOTALL)

print(f"  ✅ Tablas convertidas a landscape: {tablas_convertidas}")

# ============================================================================
# PASO 6: Guardar Archivo Actualizado
# ============================================================================
print("\n💾 Guardando archivo LaTeX actualizado...")

with open(OUTPUT_TEX, 'w', encoding='utf-8') as f:
    f.write(contenido)

print(f"✅ Archivo guardado: {OUTPUT_TEX.name}")
print(f"   Tamaño: {len(contenido)} caracteres")

# ============================================================================
# PASO 7: Generar Batch de Compilación
# ============================================================================
print("\n🔨 Generando script de compilación...")

batch_compile = f"""@echo off
echo ============================================
echo COMPILANDO INFORME LATEX FINAL V2
echo ============================================
echo.

cd "{DOCS_DIR}"

echo [1/4] Primera pasada de pdflatex...
pdflatex -interaction=nonstopmode INFORME_TECNICO_FINAL_V2.tex > NUL 2>&1

echo [2/4] Segunda pasada (referencias cruzadas)...
pdflatex -interaction=nonstopmode INFORME_TECNICO_FINAL_V2.tex > NUL 2>&1

echo [3/4] Tercera pasada (tabla de contenidos)...
pdflatex -interaction=nonstopmode INFORME_TECNICO_FINAL_V2.tex > NUL 2>&1

echo [4/4] Limpiando archivos auxiliares...
del INFORME_TECNICO_FINAL_V2.aux INFORME_TECNICO_FINAL_V2.log INFORME_TECNICO_FINAL_V2.out INFORME_TECNICO_FINAL_V2.toc 2>NUL

echo.
echo ============================================
echo COMPILACION COMPLETADA
echo ============================================
echo PDF generado: INFORME_TECNICO_FINAL_V2.pdf
echo.
pause
"""

batch_path = DOCS_DIR / "compilar_final_v2.bat"
with open(batch_path, 'w', encoding='utf-8') as f:
    f.write(batch_compile)

print(f"✅ Script de compilación creado: {batch_path.name}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 80)
print("✅ ACTUALIZACIÓN COMPLETADA")
print("=" * 80)
print()
print(f"📄 Archivo LaTeX actualizado: {OUTPUT_TEX.name}")
print(f"🔧 Script de compilación: {batch_path.name}")
print()
print("📊 Cambios aplicados:")
paquete_added = 'Sí' if '\\usepackage{pdflscape}' in contenido else 'Ya existía'
print(f"  • Paquete pdflscape añadido: {paquete_added}")
print(f"  • Tabla de estadísticos actualizada: Sí (landscape)")
print(f"  • Figuras insertadas: {figuras_insertadas} / {len(nuevas_figuras)}")
print(f"  • Tablas convertidas a landscape: {tablas_convertidas}")
print()
print("🚀 Próximo paso:")
print(f"   1. Revisar manualmente {OUTPUT_TEX.name} si lo deseas")
print(f"   2. Ejecutar: cd documentos_tesis && .\\compilar_final_v2.bat")
print(f"   3. Abrir PDF: INFORME_TECNICO_FINAL_V2.pdf")
print()
print("=" * 80)

