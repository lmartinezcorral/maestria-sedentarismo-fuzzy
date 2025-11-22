# 📄 PLAN DE COMPILACIÓN PDF - INFORME TÉCNICO LÁTEX

**Fecha:** 24 de octubre de 2025  
**Estado actual:** El script automático de actualización generó errores en tablas landscape

---

## 🚨 PROBLEMA IDENTIFICADO

El script `actualizar_informe_latex_final.py` convirtió automáticamente tablas con `\resizebox` a `landscape`, pero generó estructuras LaTeX malformadas que impiden la compilación.

**Errores principales:**
1. Tablas con `\begin{tabular}` cerradas incorrectamente
2. Anidamiento incorrecto de entornos `landscape`
3. Espacios extra en comandos LaTeX (`\end{tabular }`)

---

## ✅ SOLUCIÓN PROPUESTA (ENFOQUE CONSERVADOR)

### **Opción 1: Usar Archivo Original + Ajustes Manuales Mínimos** (RECOMENDADO)

**Pasos:**

1. **Usar el archivo original:** `INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex`
   - Este archivo ya compila (tenemos el PDF generado)
   - Tiene 147 figuras ya integradas
   - Tablas funcionan (aunque algunas usan `\resizebox`)

2. **Reemplazar solo la tabla de estadísticos descriptivos (Capítulo 4):**
   - Buscar: `\label{tab:descriptive_daily}`
   - Reemplazar con la tabla nueva en formato horizontal (landscape)
   - Manual, línea por línea, sin regex

3. **Añadir las 6 nuevas figuras manualmente en posiciones específicas:**
   - `histogramas_con_kde.png` → después de "\subsection{Gráficos Exploratorios}"
   - `violin_plots_por_usuario.png` → en Capítulo 4, sección de heterogeneidad
   - `grouped_bar_medianas_por_usuario.png` → junto a violin plots
   - `heatmap_patron_semanal.png` → patrones temporales
   - `scatter_matrix_relaciones.png` → análisis de correlación
   - `boxplots_comparativos.png` → junto a histogramas

4. **Para tablas anchas problemáticas:**
   - **Opción A (más simple):** Usar `\small` o `\footnotesize` antes de `\begin{tabular}`
   - **Opción B:** Usar `adjustbox` package: `\begin{adjustbox}{max width=\textwidth}`
   - **Opción C:** Transponer tabla (convertir filas a columnas) si tiene sentido

---

### **Opción 2: Compilar PDF con el Archivo Actual (Tiene Errores)**

Si quieres ver el resultado parcial a pesar de los errores:

```bash
cd documentos_tesis
pdflatex -interaction=nonstopmode -file-line-error INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex
```

**Resultado esperado:**
- PDF parcial con algunas secciones compiladas
- Errores en tablas específicas (se omitirán)
- Útil para revisar secciones que sí funcionan

---

## 🛠️ HERRAMIENTAS DISPONIBLES

### **Scripts creados hoy:**

1. `generar_analisis_descriptivo_visual_v2.py` ✅ (FUNCIONA)
   - Genera estadísticos actualizados (n=9,185)
   - 6 visualizaciones profesionales (300 dpi)
   - Output: `analisis_u/descriptivos_visuales/`

2. `actualizar_informe_latex_final.py` ❌ (GENERA ERRORES)
   - Convierte tablas automáticamente a landscape
   - **NO usar hasta corregir regex**

### **Archivos generados:**

- ✅ `tabla_descriptivos_actualizados.csv`
- ✅ `tabla_descriptivos_actualizados.tex` (tabla simple, sin landscape)
- ✅ 6 figuras PNG (histogramas, violin, bar, heatmap, scatter, boxplots)

---

## 📋 PRÓXIMA SESIÓN: PASOS CONCRETOS

### **Tarea 1: Actualizar Tabla de Estadísticos (15 min)**

**Archivo:** `INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex`  
**Ubicación:** Capítulo 4, línea ~522

**Código actual (aprox. línea 520-538):**
```latex
\begin{table}[H]
\centering
\caption{Estadísticos Descriptivos de Variables Clave (Nivel Diario, $n=8,380$ días)}
\label{tab:descriptive_daily}
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}lrrrrrrc@{}}
\toprule
\textbf{Variable} & \textbf{Media} & \textbf{DE} & \textbf{Mediana} & \textbf{IQR} & \textbf{Min} & \textbf{Max} & \textbf{SW $p$-valor} \\
\midrule
Pasos             & 6,842 & 4,231 & 6,120 & 4,890 & 0    & 28,450 & $<0.001$ \\
Calorías activas  & 385   & 287   & 342   & 298   & 0    & 1,892  & $<0.001$ \\
...
\bottomrule
\end{tabular}%
}
\end{table}
```

**Reemplazo sugerido (con landscape):**
```latex
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
... (copiar resto de filas de tabla_descriptivos_actualizados.tex)
\bottomrule
\end{tabular}
\end{table}
\end{landscape}
```

**Notas:**
- Eliminar `\resizebox` (ya no necesario en landscape)
- Añadir `\usepackage{pdflscape}` al preámbulo si no existe
- La tabla en landscape rotará la página automáticamente

---

### **Tarea 2: Insertar Figuras Nuevas (30 min)**

**Ubicaciones sugeridas:**

1. **Histogramas con KDE** (`histogramas_con_kde.png`)
   - **Ubicación:** Capítulo 4, después de "\subsection{Gráficos Exploratorios}"
   - **Código:**
   ```latex
   \begin{figure}[htbp]
   \centering
   \includegraphics[width=0.95\textwidth]{../analisis_u/descriptivos_visuales/histogramas_con_kde.png}
   \caption{Distribuciones de variables clave (nivel diario). Histogramas con densidad KDE, mostrando alta variabilidad (CV > 50\%) y violación de normalidad ($p < 0.001$).}
   \label{fig:histogramas_kde}
   \end{figure}
   ```

2. **Violin Plots** (`violin_plots_por_usuario.png`)
   - **Ubicación:** Capítulo 4, sección "Caracterización de Variables Biométricas"
   - **Código:** Similar al anterior, cambiar nombre de archivo y caption

3-6. **Resto de figuras:** Seguir mismo patrón.

---

### **Tarea 3: Solucionar Tablas Anchas Restantes (20 min)**

**Para cada tabla con `\resizebox` que sea difícil de leer:**

**Opción A (más rápida):** Reducir tamaño de fuente
```latex
\begin{table}[htbp]
\centering
\caption{...}
\small  % ← Añadir esta línea
\begin{tabular}{...}
...
\end{tabular}
\end{table}
```

**Opción B (mejor visualización):** Landscape para tablas muy anchas
```latex
\begin{landscape}
\begin{table}[htbp]
... (tabla completa)
\end{table}
\end{landscape}
```

**Tabla prioritaria:** Matriz de Correlación SF-36 vs Biométricos (label: `tab:correlation_sf36`)

---

### **Tarea 4: Compilar y Verificar (10 min)**

**Comandos:**
```bash
cd "C:\Users\hulkmtz\Documents\luis angel\Maestria\Asesoria\Semestre 3\Convocatoria\Datos\4 semestre_dataset\documentos_tesis"

# Primera pasada
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex

# Segunda pasada (referencias cruzadas)
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex

# Tercera pasada (tabla de contenidos)
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex
```

**Verificar:**
- PDF se genera sin errores fatales
- Tabla de estadísticos se ve correctamente (landscape)
- Nuevas figuras aparecen en las secciones correctas
- Tablas anchas legibles (no texto microscópico)

---

## 📚 RECURSOS ADICIONALES

### **Paquetes LaTeX útiles para tablas anchas:**

1. **pdflscape**: Rota páginas completas
   ```latex
   \usepackage{pdflscape}
   \begin{landscape} ... \end{landscape}
   ```

2. **adjustbox**: Ajusta ancho automáticamente
   ```latex
   \usepackage{adjustbox}
   \begin{adjustbox}{max width=\textwidth}
   \begin{tabular}{...} ... \end{tabular}
   \end{adjustbox}
   ```

3. **longtable**: Tablas multi-página
   ```latex
   \usepackage{longtable}
   \begin{longtable}{...}
   \caption{...} \\
   \toprule
   ... (contenido de tabla)
   \bottomrule
   \end{longtable}
   ```

4. **Reducción de fuente:**
   - `\small`: Reduce ~10%
   - `\footnotesize`: Reduce ~20%
   - `\scriptsize`: Reduce ~30% (no recomendado, muy pequeño)

---

## 🎯 OBJETIVO FINAL

**PDF compilado con:**
- ✅ Estadísticos descriptivos actualizados (n=9,185)
- ✅ 6 nuevas figuras profesionales integradas
- ✅ Tablas anchas legibles (landscape o fuente ajustada)
- ✅ Formato APA 7ª edición mantenido
- ✅ Referencias cruzadas funcionando
- ✅ Tabla de contenidos actualizada

**Tiempo estimado total:** ~1.5 horas (próxima sesión)

---

**Generado el 24 de octubre de 2025, 23:55 hrs**  
**Autor:** Claude AI (con contexto del proyecto de Luis Ángel Martínez)

