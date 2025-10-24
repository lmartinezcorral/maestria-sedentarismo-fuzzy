# 📊 RESUMEN: ACTUALIZACIÓN DE ANÁLISIS DESCRIPTIVO Y VISUALIZACIONES PROFESIONALES

**Fecha:** 24 de octubre de 2025  
**Script:** `generar_analisis_descriptivo_visual_v2.py`  
**Objetivo:** Generar estadísticos descriptivos actualizados desde datos LIMPIOS (post-winsorización, imputación, manejo de outliers) y producir visualizaciones profesionales para el Capítulo 4 del Informe Técnico LaTeX.

---

## ✅ TRABAJO COMPLETADO

### 📊 **Estadísticos Descriptivos Actualizados**

**Datos analizados:**
- **N = 9,185 registros** (nivel diario)
- **10 usuarios** (u1-u10)
- **8 variables clave**

**Tabla generada:**
| Variable | n | Media | DE | CV (%) | Mediana | Q1 | Q3 | IQR |
|----------|---|-------|-----|--------|---------|-----|-----|------|
| Pasos Diarios | 9,185 | 6,001.63 | 3,283.59 | 54.7 | 5,489.0 | 3,779.0 | 7,657.0 | 3,878.0 |
| Calorías Activas (kcal) | 9,185 | 595.87 | 450.65 | 75.6 | 517.72 | 322.09 | 767.4 | 445.31 |
| FC Reposo (lpm) | 9,185 | 54.24 | 8.72 | 16.1 | 53.0 | 48.0 | 59.0 | 11.0 |
| FC al Caminar (lpm) | 9,185 | 97.77 | 12.38 | 12.7 | 97.75 | 90.5 | 105.0 | 14.5 |
| HRV SDNN (ms) | 9,185 | 49.39 | 17.17 | 34.8 | 48.36 | 36.17 | 60.4 | 24.23 |
| Hrs Monitorizadas | 9,185 | 15.42 | 5.21 | 33.8 | 15.0 | 13.0 | 18.0 | 5.0 |
| Actividad Relativa (prop.) | 9,185 | 0.14 | 0.10 | 73.2 | 0.13 | 0.08 | 0.18 | 0.09 |
| Superávit Calórico (%) | 9,185 | 32.64 | 23.03 | 70.6 | 28.0 | 19.87 | 40.91 | 21.04 |

**Archivo exportados:**
- `analisis_u/descriptivos_visuales/tabla_descriptivos_actualizados.csv`
- `analisis_u/descriptivos_visuales/tabla_descriptivos_actualizados.tex`

---

### 🎨 **Visualizaciones Profesionales Generadas (6 figuras PNG)**

**Ubicación:** `4 semestre_dataset/analisis_u/descriptivos_visuales/`

#### 1. **Violin Plots por Usuario** (`violin_plots_por_usuario.png`)
- **Tipo:** Violin plots 
- **Variables:** 8 variables clave
- **Descripción:** Muestra distribuciones completas (densidad + cuartiles) por usuario, evidenciando heterogeneidad inter-sujeto.
- **Uso:** Capítulo 4 - Caracterización de la Cohorte

#### 2. **Grouped Bar Chart: Medianas por Usuario** (`grouped_bar_medianas_por_usuario.png`)
- **Tipo:** Gráfico de barras agrupadas
- **Variables:** 8 variables normalizadas [0-1]
- **Descripción:** Comparación rápida de perfiles individuales de comportamiento, mostrando niveles relativos de cada variable por usuario.
- **Uso:** Capítulo 4 - Perfiles de Usuario

#### 3. **Heatmap de Patrón Semanal** (`heatmap_patron_semanal.png`)
- **Tipo:** Mapa de calor
- **Ejes:** Usuario (Y) × Día de la Semana (X)
- **Valor:** Mediana de Pasos Diarios
- **Descripción:** Identifica patrones temporales (e.g., menor actividad fines de semana) y heterogeneidad por usuario.
- **Uso:** Capítulo 4 - Variabilidad Temporal

#### 4. **Scatter Matrix: Relaciones Bivariadas** (`scatter_matrix_relaciones.png`)
- **Tipo:** Matriz de dispersión (pairplot)
- **Variables:** Pasos, HRV_SDNN, Actividad Relativa, Superávit Calórico
- **Muestra:** n=2,000 días (sample aleatorio para performance)
- **Descripción:** Explora relaciones bivariadas entre variables clave, coloreado por usuario. Diagonal: histogramas. Arriba: scatter plots. Abajo: KDE.
- **Uso:** Capítulo 9 - Análisis de Correlación (contexto exploratorio)

#### 5. **Boxplots Comparativos** (`boxplots_comparativos.png`)
- **Tipo:** Boxplots con media superpuesta (diamante rojo)
- **Variables:** 8 variables clave
- **Descripción:** Detecta outliers, muestra rango IQR, y compara medianas vs. medias por usuario. Evidencia asimetría en distribuciones.
- **Uso:** Capítulo 4 - Manejo de Outliers (post-winsorización)

#### 6. **Histogramas con KDE** (`histogramas_con_kde.png`)
- **Tipo:** Histogramas + Kernel Density Estimation
- **Variables:** 8 variables clave
- **Descripción:** Distribuciones generales (todas las observaciones), con media y mediana superpuestas. Incluye CV% para cuantificar variabilidad.
- **Uso:** Capítulo 4 - Análisis Exploratorio de Datos

---

## 🔍 **HALLAZGOS CLAVE**

### 1. **Alta Variabilidad Intra-Cohorte (CVs > 50%)**
- Calorías Activas: CV = 75.6%
- Actividad Relativa: CV = 73.2%
- Superávit Calórico: CV = 70.6%
- Pasos Diarios: CV = 54.7%

**Implicación:** Justifica el uso de **medianas y IQR** (estadísticos robustos) en lugar de medias para caracterización. Respalda la necesidad de modelado personalizado (fuzzy logic con 5 reglas, no regresión lineal global).

### 2. **Violación de Normalidad (Todas las Variables, p < 0.001)**
- **Test:** Kolmogorov-Smirnov (n=9,185 > 5,000)
- **Resultado:** Rechaza normalidad en todas las variables

**Implicación:** Justifica el uso de **pruebas no paramétricas** (Mann-Whitney U, Kruskal-Wallis) en análisis posteriores (Capítulo 10 - Clustering).

### 3. **Heterogeneidad Temporal (Heatmap Semanal)**
- Patrones semanales variables entre usuarios
- Algunos usuarios muestran menor actividad fines de semana, otros no

**Implicación:** Respalda la necesidad de **agregación semanal** (p50) en lugar de promedios globales para capturar comportamiento típico.

### 4. **Relaciones No Lineales (Scatter Matrix)**
- No se observan correlaciones lineales fuertes simples
- Nubes de puntos dispersas con agrupación por usuario

**Implicación:** Justifica el uso de **fuzzy inference** (captura relaciones no lineales mediante reglas lingüísticas) en lugar de regresión lineal.

---

## 📝 **INTEGRACIÓN AL INFORME LÁTEX**

### **Capítulo 4: Exploración y Limpieza de Datos**

**Sección 4.3: Estadísticos Descriptivos (Datos Limpios)**

```latex
\subsection{Estadísticos Descriptivos Post-Limpieza}

Tras aplicar las técnicas de imputación y winsorización (Sección 4.2), se calcularon 
estadísticos descriptivos actualizados para las 8 variables clave derivadas. 
La Tabla~\ref{tab:descriptivos_actualizados} presenta los resultados.

\input{analisis_u/descriptivos_visuales/tabla_descriptivos_actualizados.tex}

Se observa alta variabilidad inter-sujeto, con coeficientes de variación (CV) 
superiores al 50\% en 4 de las 8 variables. Esto respalda la necesidad de 
utilizar estadísticos robustos (medianas, IQR) en lugar de medias para 
caracterización.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\textwidth]{analisis_u/descriptivos_visuales/violin_plots_por_usuario.png}
\caption{Distribuciones de variables clave por usuario (Violin Plots). 
Se observa heterogeneidad marcada entre participantes, evidenciando la necesidad 
de modelado personalizado.}
\label{fig:violin_plots_usuarios}
\end{figure}

\textbf{Pruebas de Normalidad:} Todas las variables rechazaron normalidad 
(test de Kolmogorov-Smirnov, $p < 0.001$), justificando el uso de pruebas 
no paramétricas en análisis subsecuentes (Capítulo 10).
```

**Sección 4.4: Heterogeneidad Inter-Sujeto**

```latex
\subsection{Heterogeneidad y Perfiles de Usuario}

La Figura~\ref{fig:grouped_bar_medianas} presenta una comparación de medianas 
normalizadas por usuario, evidenciando perfiles diferenciados de comportamiento.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\textwidth]{analisis_u/descriptivos_visuales/grouped_bar_medianas_por_usuario.png}
\caption{Perfiles de usuario: medianas normalizadas [0-1] para 8 variables clave. 
Se observan patrones heterogéneos, con algunos usuarios mostrando alta actividad 
física pero baja variabilidad cardíaca, y viceversa.}
\label{fig:grouped_bar_medianas}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{analisis_u/descriptivos_visuales/heatmap_patron_semanal.png}
\caption{Patrón semanal de actividad (mediana de pasos por día de la semana). 
Se evidencia heterogeneidad temporal, con algunos usuarios mostrando reducción 
significativa de actividad en fines de semana.}
\label{fig:heatmap_semanal}
\end{figure}
```

---

## 🎯 **PRÓXIMOS PASOS (Según Plan Maestro)**

### ✅ Completado:
- [x] Script 1: Análisis descriptivo actualizado con visualizaciones profesionales
- [x] Generación de 6 figuras PNG de alta calidad (300 dpi)
- [x] Exportación de tablas en formato CSV y LaTeX

### 📋 Pendiente:
- [ ] **Script 2:** Análisis a nivel de archivos individuales (DB_CREATE_V3.ipynb)
  - Revisar proceso de extracción desde XML
  - Generar estadísticos pre-limpieza vs. post-limpieza
  - Documentar decisiones de manejo de outliers

- [ ] **Script 3:** Actualización del Capítulo 5 (Validación de Expertos + Pivote Metodológico)
  - Documentar 20 configuraciones ANN probadas (inviabilidad)
  - Justificar abandono de objetivo predictivo SF-36
  - Contextualizar rescate de HRV_SDNN (357 análisis exploratorios)

- [ ] **Actualización Informe LaTeX:**
  - Reemplazar estadísticos antiguos en Capítulo 4
  - Insertar figuras nuevas en posiciones apropiadas
  - Aplicar "Start with Why" sutilmente en introducción de cada análisis

---

## 📚 **REFERENCIAS TÉCNICAS**

**Estilo visual:**
- Paleta de colores: `tab10` (10 colores distinguibles, uno por usuario)
- Resolución: 300 dpi (calidad publicación)
- Formato: PNG (compatibilidad universal)
- Tipografía: Seaborn context `notebook` (escala 1.1)

**Decisiones estadísticas:**
- **Test de normalidad:** Kolmogorov-Smirnov (n > 5,000), Shapiro-Wilk (n < 5,000)
- **Agregación:** Medianas (robustas a outliers post-winsorización)
- **Visualización temporal:** Ventana de 90 días con mayor densidad de datos (no generada por datos dispersos)

---

**Generado automáticamente el 24 de octubre de 2025**  
**Script:** `generar_analisis_descriptivo_visual_v2.py`  
**Autor:** Luis Ángel Martínez (con asistencia de Claude AI)

