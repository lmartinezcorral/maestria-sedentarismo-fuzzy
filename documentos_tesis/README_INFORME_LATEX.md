# Informe Técnico Pipeline Bioestadístico - LaTeX

## 📄 Descripción

Documento técnico ultra-detallado (estimado: **150+ páginas**) que documenta todo el pipeline bioestadístico del proyecto de clasificación de sedentarismo mediante lógica difusa y clustering.

## 📋 Estructura del Documento

### Capítulos Principales

1. **Planteamiento del Problema e Hipótesis Inicial**
   - Contexto epidemiológico
   - Hipótesis H₀ (CS-CVRS)
   - Marco de 6 pasos

2. **Selección de Dispositivo Wearable y Diseño de Cohorte**
   - Matriz de decisión Apple Watch vs competidores
   - Criterios inclusión/exclusión
   - Tamaño muestral (N=10, n_semanas=1,337)

3. **Protocolo de Convocatoria y Preprocesamiento**
   - Exportación Apple Health (XML → CSV)
   - Auditoría de calidad
   - Pipeline de conversión

4. **Análisis Exploratorio de Datos (EDA)**
   - Distribuciones y no-normalidad
   - Validación SF-36 (Alfa de Cronbach)
   - Rechazo de hipótesis inicial

5. **Pivote Metodológico: Del Supervisado al Data-Driven**
   - Análisis correlacional fallido
   - ANN con R² negativo
   - Reformulación: Clustering + Fuzzy

6. **Estrategia de Imputación Jerárquica**
   - Diagnóstico de missingness (Little MCAR test)
   - Algoritmo jerárquico de 5 niveles
   - Validación de plausibilidad fisiológica

7. **Ingeniería de Características**
   - Actividad_relativa (normalizada por exposición)
   - Superávit_calórico_basal (normalizado por TMB)
   - HRV_SDNN y Delta_cardiaco

8. **Agregación Temporal y Análisis de Variabilidad**
   - Justificación de agregación semanal
   - Análisis dual: observado vs operativo
   - Coeficientes de variación (CV)

9. **Análisis de Correlación y Reducción Dimensional (PCA)**
   - Matriz de correlación con valores explícitos
   - VIF (Multicolinealidad < 2.0)
   - PCA biplot: selección de 4 features p50

10. **Clustering No Supervisado: Verdad Operativa**
    - K-sweep (K=2..6), Silhouette=0.232
    - Perfiles de cluster (Mann-Whitney U)
    - Cohen's d (Actividad: 0.93, Superávit: 1.78)

11. **Sistema de Inferencia Difusa Mamdani**
    - Funciones de pertenencia triangulares (percentiles)
    - 5 reglas expertas (R1-R5)
    - Matrices B (antecedentes) y C_out (consecuentes)
    - Defuzzificación (centroide)

12. **Validación Cruzada y Análisis de Robustez**
    - Concordancia Fuzzy-Clusters (F1=0.840, MCC=0.294)
    - Leave-One-User-Out (LOUO)
    - Sensibilidad τ y MF params
    - Modelo 4V vs 2V (robustez a HRV no discriminativo)

13. **Justificación Metodológica: NO Split Train/Test**
    - Fuga temporal en series longitudinales
    - N=10 usuarios (insuficiente para split inter-sujeto)
    - Alternativas: LOUO, sensibilidad

## 🛠️ Compilación

### Requisitos

- **Windows**: MiKTeX (https://miktex.org/download)
- **macOS/Linux**: TeX Live (https://www.tug.org/texlive/)

### Compilar a PDF

**Opción 1: Windows (automático)**
```cmd
cd documentos_tesis
compilar_latex.bat
```

**Opción 2: Manual**
```bash
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO.tex
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO.tex
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO.tex
```

## 📊 Figuras y Tablas Referenciadas

### Ubicaciones de Figuras

- **Variabilidad**: `4 semestre_dataset/variabilidad_operativa_vs_observada.png`
- **Correlación**: `4 semestre_dataset/analisis_u/features_correlacion_heatmap.png`
- **PCA**: `4 semestre_dataset/analisis_u/pca_biplot.png`
- **Clustering**: `4 semestre_dataset/analisis_u/clustering/k2_scatter_pca.png`
- **Fuzzy MF**: `4 semestre_dataset/analisis_u/fuzzy/membership_functions.png`
- **Confusión**: `4 semestre_dataset/analisis_u/fuzzy/confusion_matrix.png`
- **Robustez**: `documentos_tesis/plots/comparativa_f1_scores.png`
- **Cluster profiles**: `documentos_tesis/plots/cluster_profiles_boxplots.png`

### Tablas Principales

- Tabla 2.1: Matriz de decisión wearables
- Tabla 2.2: Criterios de elegibilidad
- Tabla 3.1: Métricas de completitud por usuario
- Tabla 4.1: Estadísticos descriptivos diarios
- Tabla 4.2: Fiabilidad SF-36
- Tabla 5.1: Correlación SF-36 vs biométricos
- Tabla 5.2: Desempeño ANN
- Tabla 6.1: Tasas de imputación
- Tabla 7.1: Comparación pasos vs actividad relativa
- Tabla 7.2: TMB y superávit calórico
- Tabla 8.1: Variabilidad dual (observado vs operativo)
- Tabla 10.1: Perfiles de cluster (medianas, IQR, p-valores)
- Tabla 11.1: Matriz B (antecedentes, 5×12)
- Tabla 11.2: Matriz C_out (consecuentes, 5×3)
- Tabla 12.1: Métricas de validación (4V vs 2V)

## 📐 Ecuaciones Destacadas

- **Actividad Relativa**: $\text{Act}_{\text{rel}} = \frac{\text{Pasos}}{\text{Horas\_datos}} \times \frac{1}{1000}$
- **TMB (Harris-Benedict)**: $\text{TMB}_h = 88.362 + 13.397W + 4.799H - 5.677A$
- **Superávit Calórico**: $\text{Sup} = \frac{\text{Cal\_activas}}{\text{TMB}} \times 100\%$
- **Función Triangular**: $\mu(x;a,b,c) = \max\left(0, \min\left(\frac{x-a}{b-a}, \frac{c-x}{c-b}\right)\right)$
- **Activación Mamdani**: $w_{i,r} = \min\{\mu_{i,j} : B_{rj}=1\}$
- **Defuzzificación**: $\text{score}_i = \frac{0.2s_{i,B} + 0.5s_{i,M} + 0.8s_{i,A}}{s_{i,B}+s_{i,M}+s_{i,A}}$
- **F1-Score**: $F1 = \frac{2 \cdot \text{Prec} \cdot \text{Rec}}{\text{Prec} + \text{Rec}}$
- **MCC**: $MCC = \frac{TP \cdot TN - FP \cdot FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}$

## 🎯 Marco de los 6 Pasos (Aplicado en Cada Capítulo)

Cada fase del pipeline se analiza bajo:

1. **Planteamiento de Hipótesis** (caja azul)
2. **Selección del Estadístico/Método** (caja verde)
3. **Regla de Decisión** (caja naranja)
4. **Cálculos** (caja morada)
5. **Decisión Estadística** (caja roja)
6. **Conclusión** (caja cyan)

## 📦 Paquetes LaTeX Utilizados

- `amsmath, amssymb, amsthm`: Matemáticas
- `graphicx, subcaption`: Figuras
- `booktabs, longtable, multirow`: Tablas profesionales
- `algorithm, algpseudocode`: Algoritmos
- `tcolorbox`: Cajas de 6 pasos
- `hyperref, cleveref`: Referencias cruzadas
- `listings`: Código Python/XML

## 🚀 Próximos Pasos

1. ✅ Compilar a PDF
2. ⏳ Revisar formato de figuras (ajustar tamaños si es necesario)
3. ⏳ Añadir apéndices con código fuente completo (opcional)
4. ⏳ Exportar a Word si el comité tutorial lo requiere (Pandoc)

## 📧 Contacto

**Autor**: Luis Ángel Martínez  
**Institución**: UACH - Facultad de Medicina y Ciencias Biomédicas  
**Programa**: Maestría en Ciencias de la Salud

---

**Fecha de generación**: 2025-10-22  
**Versión del documento**: 1.0  
**Páginas estimadas**: 150-180

