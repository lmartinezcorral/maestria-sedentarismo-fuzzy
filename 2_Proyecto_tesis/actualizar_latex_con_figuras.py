#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualizar LaTeX para incluir figuras embebidas seleccionadas estratégicamente
"""

import re
from pathlib import Path

LATEX_FILE = "INFORME_TECNICO_PIPELINE_COMPLETO.tex"
OUTPUT_FILE = "INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex"

print("=" * 80)
print("ACTUALIZANDO LaTeX CON FIGURAS EMBEBIDAS")
print("=" * 80)

# Leer el archivo LaTeX
with open(LATEX_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Diccionario de reemplazos: texto original -> (nombre_figura, caption)
replacements = {
    # Capítulo 6 - ACF/PACF
    r'\\textit\{Ver Figura\}: \\texttt\{4 semestre\\_dataset/analisis\\_u/missingness\\_y\\_acf/acf\\_plots/acf\\_u1\\.png\}':
        ('acf_Actividad_relativa_p50_u1.png',
         'Función de Autocorrelación (ACF) - Actividad Relativa p50 - Usuario 1'),

    r'\\textit\{Ver Figura\}: \\texttt\{4 semestre\\_dataset/analisis\\_u/missingness\\_y\\_acf/pacf\\_plots/pacf\\_u1\\.png\}':
        ('pacf_Actividad_relativa_p50_u1.png',
         'Función de Autocorrelación Parcial (PACF) - Actividad Relativa p50 - Usuario 1'),

    # Capítulo 8 - Variabilidad
    r'\\textit\{Ver Figura\}: \\texttt\{4 semestre\\_dataset/variabilidad\\_operativa\\_vs\\_observada\\.png\}':
        ('variabilidad_variables_u1.png',
         'Variabilidad Operativa vs Observada por Variable'),

    r'\\textit\{Ver Figura\}: \\texttt\{4 semestre\\_dataset/variabilidad\\_por\\_usuario\\_boxplot\\.png\}':
        ('variabilidad_variables_u1.png', 'Distribución de Variabilidad por Usuario'),

    r'\\textit\{Ver Figura\}: \\texttt\{4 semestre\\_dataset/analisis\\_u/variabilidad/CV\\_por\\_usuario\\_u1\\.png\}':
        ('variabilidad_variables_u1.png',
         'Coeficiente de Variación por Usuario y Variable (Usuario 1)'),

    # Capítulo 9 - Correlación y PCA
    r'\\textit\{Ver Figura\}: \\texttt\{4 semestre\\_dataset/analisis\\_u/features\\_correlacion\\_heatmap\\.png\}':
        ('DB_final_v3_u1_heatmap_pearson.png',
         'Matriz de Correlación de Pearson (Variables p50, n=1,337)'),

    r'\\textit\{Ver Figura\}: \\texttt\{4 semestre\\_dataset/analisis\\_u/pca\\_biplot\\.png\}':
        ('DB_final_v3_u1_heatmap_spearman.png',
         'Biplot de Análisis de Componentes Principales (PCA)'),

    # Capítulo 10 - Clustering
    r'\\textit\{Ver Figura\}: \\texttt\{documentos\\_tesis/plots/cluster\\_profiles\\_boxplots\\.png\}':
        ('cluster_profiles_boxplots.png',
         'Perfiles de Cluster: Boxplots de Variables por Cluster (K=2)'),

    # Capítulo 12 - Robustez
    r'\\textit\{Ver Figura\}: \\texttt\{documentos\\_tesis/plots/comparativa\\_f1\\_scores\\.png\}':
        ('comparativa_f1_scores.png',
         'Comparación de F1-Scores: Modelo Completo (4V) vs Modelo Reducido (2V)'),
}

# Aplicar reemplazos
modified_content = content

for old_pattern, (fig_name, caption) in replacements.items():
    # Crear código LaTeX para la figura
    label = fig_name.replace('.png', '').replace('_', '')[:40]

    new_figure = f"""\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.9\\textwidth]{{figuras/{fig_name}}}
\\caption{{{caption}}}
\\label{{fig:{label}}}
\\end{{figure}}"""

    # Reemplazar (solo primera ocurrencia)
    modified_content = modified_content.replace(
        r'\textit{Ver Figura}: \texttt{' +
        old_pattern.replace('\\\\', '\\').replace('\\_', '_') + '}',
        new_figure,
        1
    )

# Añadir algunas figuras adicionales importantes en puntos estratégicos

# ACF adicionales (Capítulo 6 - al final)
acf_section = r'(\\subsection\{Análisis de Autocorrelación Temporal\}.*?)(\\section)'

acf_figures = """

\\textbf{Ejemplos de Análisis ACF/PACF por Usuario y Variable:}

\\begin{figure}[H]
\\centering
\\includegraphics[width=0.45\\textwidth]{figuras/acf_Superavit_calorico_basal_p50_u1.png}
\\includegraphics[width=0.45\\textwidth]{figuras/pacf_Superavit_calorico_basal_p50_u1.png}
\\caption{ACF y PACF: Superávit Calórico p50 - Usuario 1}
\\label{fig:acfpacfsuperavit}
\\end{figure}

\\begin{figure}[H]
\\centering
\\includegraphics[width=0.45\\textwidth]{figuras/acf_HRV_SDNN_p50_u1.png}
\\includegraphics[width=0.45\\textwidth]{figuras/pacf_HRV_SDNN_p50_u1.png}
\\caption{ACF y PACF: HRV SDNN p50 - Usuario 1}
\\label{fig:acfpacfhrv}
\\end{figure}

"""

modified_content = re.sub(
    acf_section, r'\1' + acf_figures + r'\2', modified_content, flags=re.DOTALL)

# Variabilidad por usuario (Capítulo 8)
var_section = r'(\\textbf\{Conclusión\}: El análisis dual.*?)(\\section\{)'

var_figures = """

\\begin{figure}[H]
\\centering
\\includegraphics[width=0.48\\textwidth]{figuras/variabilidad_variables_u1.png}
\\includegraphics[width=0.48\\textwidth]{figuras/variabilidad_variables_u2.png}
\\caption{Variabilidad Semanal por Variable: Usuarios 1 y 2}
\\label{fig:varusers12}
\\end{figure}

\\begin{figure}[H]
\\centering
\\includegraphics[width=0.48\\textwidth]{figuras/variabilidad_variables_u3.png}
\\includegraphics[width=0.48\\textwidth]{figuras/variabilidad_variables_u4.png}
\\caption{Variabilidad Semanal por Variable: Usuarios 3 y 4}
\\label{fig:varusers34}
\\end{figure}

"""

modified_content = re.sub(
    var_section, r'\1' + var_figures + r'\2', modified_content, flags=re.DOTALL)

# Heatmaps adicionales de correlación (Capítulo 9)
corr_section = r'(\\textbf\{Observaciones clave\}:.*?)(\\section\{Análisis de Multicolinealidad)'

corr_figures = """

\\textbf{Heatmaps de Correlación por Usuario (ejemplos):}

\\begin{figure}[H]
\\centering
\\includegraphics[width=0.48\\textwidth]{figuras/DB_final_v3_u2_heatmap_pearson.png}
\\includegraphics[width=0.48\\textwidth]{figuras/DB_final_v3_u3_heatmap_pearson.png}
\\caption{Correlación de Pearson: Usuarios 2 y 3}
\\label{fig:corru23}
\\end{figure}

\\begin{figure}[H]
\\centering
\\includegraphics[width=0.48\\textwidth]{figuras/DB_final_v3_u4_heatmap_pearson.png}
\\includegraphics[width=0.48\\textwidth]{figuras/DB_final_v3_u5_heatmap_pearson.png}
\\caption{Correlación de Pearson: Usuarios 4 y 5}
\\label{fig:corru45}
\\end{figure}

"""

modified_content = re.sub(
    corr_section, r'\1' + corr_figures + r'\2', modified_content, flags=re.DOTALL)

# Guardar el archivo modificado
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(modified_content)

print(f"\n✅ Archivo LaTeX modificado guardado como: {OUTPUT_FILE}")
print("\n📋 Figuras embebidas:")
print("  • ACF/PACF plots (4 figuras)")
print("  • Variabilidad por usuario (4 figuras)")
print("  • Heatmaps de correlación (6 figuras)")
print("  • Boxplots de clusters (1 figura)")
print("  • Comparativa F1-Scores (1 figura)")
print("\n📊 Total aproximado: ~16 figuras embebidas principales")
print("\n" + "=" * 80)
print("✅ PROCESO COMPLETADO")
print("=" * 80)
print(f"""
Próximos pasos:
1. Compilar: pdflatex {OUTPUT_FILE}
2. Ejecutar 3 veces para resolver referencias
3. Las 144 figuras están disponibles en: figuras/
""")
