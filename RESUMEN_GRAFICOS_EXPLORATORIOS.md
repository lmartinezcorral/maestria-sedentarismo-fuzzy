# Resumen: Generación de Gráficos Exploratorios (EDA)

**Fecha**: Octubre 23, 2025  
**Script ejecutado**: `generar_graficos_exploratorios.py`  
**Datos utilizados**: `DB_usuarios_consolidada_con_actividad_relativa.csv` (9,185 días)

---

## 🎯 Objetivo

Generar los 3 gráficos exploratorios citados en el **Capítulo 4** del informe técnico LaTeX pero que no existían físicamente en el directorio.

---

## ✅ Gráficos Generados

### **1. Histogramas de Variables Clave**
- **Archivo**: `analisis_u/histogramas_variables_clave.png`
- **Contenido**: 4 histogramas (2×2) con:
  - **Variables**: Actividad Relativa, Superávit Calórico Basal, HRV SDNN, Delta Cardiaco
  - **Elementos visuales**:
    - Histograma (barras azules)
    - KDE (curva roja suavizada)
    - Media (línea naranja punteada)
    - Mediana (línea verde punteada)
    - Estadísticos: n, CV%
- **Dimensiones**: 14×10 pulgadas, DPI=150
- **Interpretación**: Muestra la distribución de las 4 variables clave a nivel diario

---

### **2. Q-Q Plots de Normalidad**
- **Archivo**: `analisis_u/qqplots_normalidad.png`
- **Contenido**: 4 Q-Q plots (2×2) con:
  - **Variables**: Las mismas 4 variables
  - **Pruebas estadísticas**:
    - **Shapiro-Wilk** (para n < 5,000)
    - **Kolmogorov-Smirnov** (para n ≥ 5,000)
  - **Elementos visuales**:
    - Puntos observados vs teóricos
    - Línea de referencia
    - p-valor y decisión (color codificado):
      - 🔴 Rojo: p < 0.001 (rechaza normalidad)
      - 🟠 Naranja: 0.001 ≤ p < 0.05 (rechaza normalidad)
      - 🟢 Verde: p ≥ 0.05 (no rechaza normalidad)
- **Dimensiones**: 14×10 pulgadas, DPI=150
- **Interpretación**: Confirma que las variables **no** siguen distribución normal (esperado para datos de actividad física)

---

### **3. Boxplots por Usuario**
- **Archivo**: `analisis_u/boxplots_por_usuario.png`
- **Contenido**: 4 boxplots (2×2) con:
  - **Variables**: Las mismas 4 variables
  - **Agrupación**: Por usuario (u1 - u10)
  - **Elementos visuales**:
    - Boxplot estándar (mediana, Q1, Q3, IQR)
    - Valores atípicos (puntos)
    - Media por usuario (diamantes rojos)
    - Paleta de colores: Set2 (seaborn)
- **Dimensiones**: 16×12 pulgadas, DPI=150
- **Interpretación**: Muestra la variabilidad **inter-usuario** de las variables, evidenciando diferencias en perfiles de actividad

---

## 📊 Variables Analizadas

| Variable | Descripción | Unidad |
|----------|-------------|--------|
| **Actividad_relativa** | Pasos / Horas monitorizadas | kilopasos/hora |
| **Superavit_calorico_basal** | (Calorías activas / TMB) × 100 | % |
| **HRV_SDNN** | Variabilidad de frecuencia cardíaca | ms |
| **Delta_cardiaco** | FC al caminar - FC en reposo | lpm |

**Nota**: `Delta_cardiaco` se calculó durante la ejecución del script a partir de:
```python
Delta_cardiaco = FC_al_caminar_promedio_diario - FCr_promedio_diario
```

---

## 📁 Ubicaciones de Archivos

### **Generados inicialmente:**
```
4 semestre_dataset/
└── analisis_u/
    ├── histogramas_variables_clave.png
    ├── qqplots_normalidad.png
    └── boxplots_por_usuario.png
```

### **Copiados a:**
```
documentos_tesis/
└── figuras/
    ├── histogramas_variables_clave.png
    ├── qqplots_normalidad.png
    └── boxplots_por_usuario.png
```

---

## 🔍 Hallazgos Clave (Visibles en los Gráficos)

### **Histogramas:**
1. **Actividad Relativa**: Distribución asimétrica positiva (cola derecha), indicando días con actividad excepcional
2. **Superávit Calórico**: Similar asimetría, con picos en días de ejercicio intenso
3. **HRV SDNN**: Distribución más simétrica, centrada ~50 ms
4. **Delta Cardiaco**: Distribución normal-like, centrada ~37 lpm

### **Q-Q Plots:**
- ✅ **Confirmado**: Ninguna variable sigue distribución normal estricta
- ⚠️ **Implicación**: Uso de métodos no paramétricos (medianas, Mann-Whitney U, etc.) es **obligatorio**

### **Boxplots por Usuario:**
- 📊 **Variabilidad inter-usuario** visible, especialmente en:
  - Actividad Relativa (usuarios activos vs sedentarios)
  - Superávit Calórico (gasto energético variable)
- 🎯 **HRV y Delta Cardiaco**: Más homogéneos entre usuarios (características fisiológicas intrínsecas)

---

## 🚀 Integración con el Informe LaTeX

Estos gráficos están **referenciados** en el **Capítulo 4** del documento LaTeX:

```latex
\textit{Ver Figuras:}
\begin{itemize}[noitemsep]
    \item \texttt{4 semestre\_dataset/analisis\_u/histogramas\_variables\_clave.png}
    \item \texttt{4 semestre\_dataset/analisis\_u/qqplots\_normalidad.png}
    \item \texttt{4 semestre\_dataset/analisis\_u/boxplots\_por\_usuario.png}
\end{itemize}
```

**Estado actual**: Nota informativa en el LaTeX, gráficos disponibles en `figuras/`

**Opción futura**: Si se desea embeber en el documento, usar:
```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.95\textwidth]{figuras/histogramas_variables_clave.png}
\caption{Distribución de Variables Clave (Nivel Diario)}
\label{fig:histogramas_eda}
\end{figure}
```

---

## ✅ Checklist de Completitud

- ✅ Script generado y funcional
- ✅ 3 gráficos creados correctamente
- ✅ Archivos copiados a `documentos_tesis/figuras/`
- ✅ Datos diarios utilizados (9,185 observaciones)
- ✅ Delta_cardiaco calculado dinámicamente
- ✅ Pruebas de normalidad ejecutadas
- ✅ Variables por usuario visualizadas

---

## 🎨 Especificaciones Técnicas

| Aspecto | Valor |
|---------|-------|
| **Bibliotecas** | pandas, numpy, matplotlib, seaborn, scipy |
| **Resolución** | 150 DPI |
| **Formato** | PNG con transparencia |
| **Tamaño típico** | ~200-250 KB por figura |
| **Estilo matplotlib** | default |
| **Paleta seaborn** | husl (histogramas), Set2 (boxplots) |

---

## 📝 Notas Adicionales

1. **Nivel de datos**: Los gráficos utilizan datos **diarios** (9,185 días), no semanales, para capturar la variabilidad completa antes de la agregación temporal.

2. **Normalización**: Las variables ya están normalizadas antropométricamente (Actividad_relativa por horas de uso, Superávit_calórico por TMB).

3. **Warnings de seaborn**: Los warnings sobre `palette` sin `hue` son esperados y no afectan la salida (deprecation warnings de seaborn 0.13+).

4. **Reproducibilidad**: El script es completamente reproducible con los datos del archivo CSV consolidado.

---

**¿Siguiente paso?**: Los gráficos están listos para ser referenciados en el documento LaTeX o embebidos si se requiere mayor integración visual.

