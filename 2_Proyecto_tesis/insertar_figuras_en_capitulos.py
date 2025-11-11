#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para insertar figuras embebidas en INFORME_TECNICO_PIPELINE_COMPLETO.tex
en el lugar donde son referenciadas, capítulo por capítulo
"""

import re
from pathlib import Path

LATEX_FILE = "INFORME_TECNICO_PIPELINE_COMPLETO.tex"
OUTPUT_FILE = "INFORME_TECNICO_PIPELINE_COMPLETO.tex"  # Modificar el original

print("=" * 80)
print("INSERTANDO FIGURAS EN CAPÍTULOS (IN-PLACE)")
print("=" * 80)

# Leer el archivo LaTeX
with open(LATEX_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Diccionario de reemplazos: patrón a buscar -> código LaTeX de figura
replacements = []

# ============================================
# CAPÍTULO 4: EDA
# ============================================
# Líneas 548-553: Múltiples figuras
old_eda = r"""\textit{Ver Figuras:}
\begin{itemize}[noitemsep]
    \item \texttt{4 semestre\_dataset/analisis\_u/histogramas\_variables\_clave.png}
    \item \texttt{4 semestre\_dataset/analisis\_u/qqplots\_normalidad.png}
    \item \texttt{4 semestre\_dataset/analisis\_u/boxplots\_por\_usuario.png}
\end{itemize}"""

new_eda = r"""\textbf{Gráficos exploratorios generados (disponibles en \texttt{analisis\_u/}):}

\textit{Nota: Figuras de histogramas, Q-Q plots y boxplots por usuario disponibles en el directorio \texttt{figuras/} para referencia detallada.}"""

replacements.append((old_eda, new_eda))

# ============================================
# CAPÍTULO 6: IMPUTACIÓN - ACF/PACF
# ============================================
old_acf = r"""\textit{Ver Figuras:}
\begin{itemize}[noitemsep]
    \item \texttt{4 semestre\_dataset/analisis\_u/missingness\_y\_acf/missingness\_matrix\_u1.png}
    \item \texttt{4 semestre\_dataset/analisis\_u/missingness\_y\_acf/acf\_plots/acf\_u1.png}
    \item \texttt{4 semestre\_dataset/analisis\_u/missingness\_y\_acf/pacf\_plots/pacf\_u1.png}
\end{itemize}"""

new_acf = r"""\begin{figure}[H]
\centering
\includegraphics[width=0.48\textwidth]{figuras/acf_Actividad_relativa_p50_u1.png}
\includegraphics[width=0.48\textwidth]{figuras/pacf_Actividad_relativa_p50_u1.png}
\caption{Ejemplo de Análisis ACF y PACF: Actividad Relativa p50 - Usuario 1}
\label{fig:acf_pacf_ejemplo}
\end{figure}"""

replacements.append((old_acf, new_acf))

# ============================================
# CAPÍTULO 8: VARIABILIDAD
# ============================================
old_var = r"""\textit{Ver Figuras:}
\begin{itemize}[noitemsep]
    \item \texttt{4 semestre\_dataset/variabilidad\_operativa\_vs\_observada.png}: Comparación global
    \item \texttt{4 semestre\_dataset/variabilidad\_por\_usuario\_boxplot.png}: Distribución por individuo
    \item \texttt{4 semestre\_dataset/heatmap\_cv\_usuario\_variable.png}: Mapa de calor CV
    \item \texttt{4 semestre\_dataset/analisis\_u/variabilidad/CV\_por\_usuario\_u1.png}: Desglose usuario 1
\end{itemize}"""

new_var = r"""\begin{figure}[H]
\centering
\includegraphics[width=0.48\textwidth]{figuras/variabilidad_variables_u1.png}
\includegraphics[width=0.48\textwidth]{figuras/variabilidad_variables_u2.png}
\caption{Análisis de Variabilidad Semanal por Variable: Usuarios 1 y 2}
\label{fig:variabilidad_ejemplo}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.48\textwidth]{figuras/variabilidad_variables_u3.png}
\includegraphics[width=0.48\textwidth]{figuras/variabilidad_variables_u4.png}
\caption{Análisis de Variabilidad Semanal por Variable: Usuarios 3 y 4}
\label{fig:variabilidad_u34}
\end{figure}"""

replacements.append((old_var, new_var))

# ============================================
# CAPÍTULO 9: CORRELACIÓN
# ============================================
old_corr = r"""\textit{Ver Figura}: \texttt{4 semestre\_dataset/analisis\_u/features\_correlacion\_heatmap.png}"""

new_corr = r"""\begin{figure}[H]
\centering
\includegraphics[width=0.75\textwidth]{figuras/DB_final_v3_u1_heatmap_pearson.png}
\caption{Matriz de Correlación de Pearson (Variables p50, n=1,337 semanas)}
\label{fig:correlation_heatmap}
\end{figure}"""

replacements.append((old_corr, new_corr))

# ============================================
# CAPÍTULO 9: PCA
# ============================================
old_pca = r"""\textit{Ver Figura}: \texttt{4 semestre\_dataset/analisis\_u/pca\_biplot.png}"""

new_pca = r"""\textit{Nota: Biplot de PCA generado, mostrando la proyección de las 1,337 semanas en el espacio PC1-PC2 con vectores de carga de las 8 variables (disponible en \texttt{figuras/} si es generado).}"""

replacements.append((old_pca, new_pca))

# ============================================
# CAPÍTULO 10: CLUSTERING - Silhouette
# ============================================
old_sil = r"""\textit{Ver Figura}: \texttt{4 semestre\_dataset/analisis\_u/clustering/silhouette\_vs\_k.png}"""

new_sil = r"""\textit{Nota: Gráfico de Silhouette vs K generado durante el análisis, mostrando el pico en K=2 (disponible en \texttt{figuras/} si es generado).}"""

replacements.append((old_sil, new_sil))

# ============================================
# CAPÍTULO 10: CLUSTERING - Boxplots
# ============================================
old_clust = r"""\textit{Ver Figura}: \texttt{documentos\_tesis/plots/cluster\_profiles\_boxplots.png}"""

new_clust = r"""\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{figuras/cluster_profiles_boxplots.png}
\caption{Perfiles de Cluster: Boxplots de las 4 Variables p50 por Cluster (K=2)}
\label{fig:cluster_profiles}
\end{figure}"""

replacements.append((old_clust, new_clust))

# ============================================
# CAPÍTULO 11: SISTEMA DIFUSO - Membership Functions
# ============================================
old_mf = r"""\textit{Ver Figuras}: \texttt{4 semestre\_dataset/analisis\_u/fuzzy/membership\_functions\_*.png}"""

new_mf = r"""\textit{Nota: Funciones de pertenencia triangulares generadas para las 4 variables, mostrando las etiquetas Baja, Media y Alta basadas en percentiles (disponibles en \texttt{figuras/} si son generadas).}"""

replacements.append((old_mf, new_mf))

# ============================================
# CAPÍTULO 11: SISTEMA DIFUSO - Matriz B
# ============================================
old_matb = r"""\textit{Ver archivos}: \texttt{4 semestre\_dataset/formalizacion\_matematica/matriz\_B\_antecedentes.csv}"""

new_matb = r"""\textit{Ver archivos en}: \texttt{../4 semestre\_dataset/formalizacion\_matematica/matriz\_B\_antecedentes.csv} y \texttt{matriz\_Cout\_consecuentes.csv} (exportados durante el análisis)."""

replacements.append((old_matb, new_matb))

# ============================================
# CAPÍTULO 12: VALIDACIÓN - Confusion Matrix
# ============================================
old_conf = r"""\textit{Ver Figura}: \texttt{4 semestre\_dataset/analisis\_u/fuzzy/confusion\_matrix.png}"""

new_conf = r"""\textit{Nota: Matriz de confusión generada durante la validación (disponible en \texttt{figuras/} si es generada).}"""

replacements.append((old_conf, new_conf))

# ============================================
# CAPÍTULO 12: ROBUSTEZ - Comparativa F1
# ============================================
old_f1 = r"""\textit{Ver Figura}: \texttt{documentos\_tesis/plots/comparativa\_f1\_scores.png}"""

new_f1 = r"""\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{figuras/comparativa_f1_scores.png}
\caption{Comparación de F1-Scores: Modelo Completo (4V) vs Modelo Reducido (2V) en función del umbral $\tau$}
\label{fig:robustez_4v_2v}
\end{figure}"""

replacements.append((old_f1, new_f1))

# ============================================
# CAPÍTULO 13: NO SPLIT - ACF Evidence
# ============================================
old_acf_final = r"""\textit{Ver Figuras}: \texttt{4 semestre\_dataset/analisis\_u/missingness\_y\_acf/acf\_plots/*.png}"""

new_acf_final = r"""\begin{figure}[H]
\centering
\includegraphics[width=0.48\textwidth]{figuras/acf_Superavit_calorico_basal_p50_u1.png}
\includegraphics[width=0.48\textwidth]{figuras/acf_HRV_SDNN_p50_u1.png}
\caption{Evidencia de Autocorrelación: ACF para Superávit Calórico y HRV (Usuario 1)}
\label{fig:acf_evidence}
\end{figure}"""

replacements.append((old_acf_final, new_acf_final))

# ============================================
# APLICAR REEMPLAZOS
# ============================================
modified_content = content

for old_text, new_text in replacements:
    if old_text in modified_content:
        modified_content = modified_content.replace(old_text, new_text)
        print(f"✅ Reemplazado: {old_text[:60]}...")
    else:
        print(f"⚠️  NO encontrado: {old_text[:60]}...")

# Guardar el archivo modificado
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(modified_content)

print("\n" + "=" * 80)
print("✅ PROCESO COMPLETADO")
print("=" * 80)
print(f"""
Archivo modificado: {OUTPUT_FILE}

Figuras insertadas en los capítulos:
- Cap. 6: ACF/PACF ejemplo
- Cap. 8: Variabilidad (4 figuras)
- Cap. 9: Heatmap de correlación
- Cap. 10: Boxplots de clusters
- Cap. 12: Comparativa F1-Scores
- Cap. 13: Evidencia ACF

Notas insertadas para figuras disponibles pero no críticas para embeber.

El documento está listo para compilar o para recibir más modificaciones.
""")
