# 📦 Inventario Completo de Recursos - Para Poseidón 🔱
**Proyecto Hércules | Actualizado: 4 de Noviembre de 2025**

---

## 📊 **FIGURAS CIENTÍFICAS (178 archivos PNG)**

### **Ubicación Principal:**
```
4 semestre_dataset/documentos_tesis/figuras/
```

**Total:** 178 archivos PNG

### **Figuras Extraídas del Informe PDF (Nuevas):**
- `figura_pag001_img1.png` ... `figura_pag300_img1.png`
- **Total:** 31 figuras del INFORME_TECNICO_ACTUALIZADO_V3.pdf

### **Figuras de Análisis (Pre-existentes):**

#### **ACF (Autocorrelación) - 80 archivos:**
```
acf_Actividad_relativa_iqr_u1.png ... u10.png (10 archivos)
acf_Actividad_relativa_p50_u1.png ... u10.png (10 archivos)
acf_Delta_cardiaco_iqr_u1.png ... u10.png (10 archivos)
acf_Delta_cardiaco_p50_u1.png ... u10.png (10 archivos)
acf_HRV_SDNN_iqr_u1.png ... u10.png (10 archivos)
acf_HRV_SDNN_p50_u1.png ... u10.png (10 archivos)
acf_Superavit_calor_iqr_u1.png ... u10.png (10 archivos)
acf_Superavit_calor_p50_u1.png ... u10.png (10 archivos)
```

#### **Boxplots y Distribuciones:**
```
cluster_profiles_boxplots.png     # Perfiles de clusters
boxplots_por_usuario.png          # Distribución por usuario
```

#### **Comparativas:**
```
comparativa_f1_scores.png         # F1-Scores por usuario
```

**Directorio adicional:**
```
4 semestre_dataset/documentos_tesis/plots/
├── cluster_profiles_boxplots.png
└── comparativa_f1_scores.png
```

---

## 📋 **TABLAS CSV (64 archivos)**

### **Ubicación:**
```
4 semestre_dataset/documentos_tesis/tablas/
```

**Total:** 64 archivos CSV actualizados

### **Tablas Principales (Del Informe):**
```
tabla_01_caracteristicas_cohorte.csv        # N=10, edad, IMC, etc.
tabla_02_patron_missingness_por_usuario.csv # Calidad de datos
tabla_03_parametros_fuzzy_sistema.csv       # Parámetros del sistema difuso
tabla_04_perfiles_cluster.csv               # Estadísticos por cluster
tabla_05_metricas_rendimiento.csv           # F1, MCC, Precision, Recall
```

### **Datasets Consolidados:**
```
DB_usuarios_consolidada.csv                      # Dataset principal sin actividad_rel
DB_usuarios_consolidada_con_actividad_relativa.csv  # Con variable derivada
DB_usuarios_resumen.csv                          # Descriptivos agregados
```

### **Análisis Individuales por Usuario (52 archivos):**
```
correlacion_u1.csv ... correlacion_u10.csv      # Matrices de correlación
descriptivos_u1.csv ... descriptivos_u10.csv    # Estadísticos descriptivos
[otros análisis individuales]
```

### **Perfiles y Comparativas:**
```
perfil_clusters_estadistico.csv              # Análisis Mann-Whitney
comparativa_modelos.csv                      # Comparación 4V vs 2V
```

---

## 📄 **DOCUMENTOS TÉCNICOS**

### **Informes Completos:**
```
4 semestre_dataset/documentos_tesis/
├── INFORME_TECNICO_ACTUALIZADO_V3.pdf         # ⭐ Principal (300 pág, 42K líneas)
├── INFORME_TECNICO_PIPELINE_COMPLETO.pdf      # Versión alternativa
├── INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.pdf  # Con figuras integradas
```

### **Documentos Markdown:**
```
├── SINTESIS_PARA_GEMINI_MCC.md               # Métricas y matriz confusión
├── RESPUESTA_MCC_PERFILES_CLUSTER.md         # Análisis clusters Mann-Whitney
├── RESUMEN_EJECUTIVO_PIPELINE.md             # Pipeline metodológico
├── perfil_clusters_completo.md               # Perfiles detallados
├── analisis_robustez.md                      # Comparación 4V vs 2V
└── README_DOCUMENTOS_TESIS.md                # Índice de documentos
```

---

## 🐍 **SCRIPTS PYTHON (12 archivos)**

### **Ubicación:**
```
4 semestre_dataset/
```

### **Análisis de Variabilidad:**
```python
variabilidad_u.py              # Variabilidad interindividual
varianzas.py                   # ANOVA
analisis_corr_var_.py          # Correlaciones
```

### **Análisis Estadístico:**
```python
analisis_critico_ratio.py      # Ratios y proporciones
```

### **Consolidación de Datos:**
```python
crear_csv_consolidado.py       # Unión de archivos
crear_excel_consolidado.py     # Exportación Excel
crear_excel_simple.py          # Versión simplificada
unir_archivos_usuarios.py      # Merge por usuario
```

### **Feature Engineering:**
```python
crear_actividad_relativa.py    # Variable actividad_relativa
```

### **Verificación y Resumen:**
```python
resumen_final.py                      # Descriptivos agregados
verificar_archivo_consolidado.py      # Validación integridad
verificar_excel.py                    # Verificación formato
verificar_final.py                    # Validación pre-análisis
```

### **Análisis Adicionales (documentos_tesis/):**
```python
analisis_robustez_modelo.py           # Comparación 4V vs 2V
analizar_perfiles_cluster.py          # Análisis Mann-Whitney
```

---

## 📚 **DATASETS PRINCIPALES**

### **Ubicación:**
```
4 semestre_dataset/
```

### **Consolidados:**
```
DB_usuarios_consolidada.csv                      # 158 filas × 10 columnas
DB_usuarios_consolidada_con_actividad_relativa.csv  # 158 × 11 (+ act_rel)
DB_usuarios_resumen.csv                          # Estadísticos agregados
```

### **Por Usuario Individual:**
```
DB_final_v3_u1.csv  ... DB_final_v3_u10.csv    # Datos crudos por usuario
```

### **Análisis por Usuario:**
```
analisis_u/
├── correlacion_u1.csv ... u10.csv      # Matrices correlación
├── descriptivos_u1.csv ... u10.csv     # Estadísticos
└── [52 archivos CSV adicionales]
```

---

## 📖 **REFERENCIAS BIBLIOGRÁFICAS**

### **Ubicación:**
```
4 semestre_dataset/edicion_tesis/tesis_luisangel/referencias.bib
```

### **Contenido Actual (15 referencias):**

**Salud Pública & OMS:**
- WHO2020, WHO2018, Bull2020, Guthold2020
- Romero2022, ShamahLevy2023

**Wearables & Tecnología:**
- Henriksen2018, White2019, Strain2020, Doherty2021

**Lógica Difusa & IA:**
- Zadeh1965, Ross2010, Kaur2022, Escalante2023

**Metodología BYOD:**
- Liu2022

---

## 🔧 **HERRAMIENTAS**

### **Compilación LaTeX:**
```
4 semestre_dataset/edicion_tesis/tesis_luisangel/compilar.bat
4 semestre_dataset/edicion_tesis/plantilla_mfips/compilar.bat
4 semestre_dataset/documentos_tesis/compilar_latex.bat
```

### **Generación de Bibliografía:**
```
4 semestre_dataset/edicion_tesis/HERRAMIENTA_BIBLIOGRAFIA_LATEX/
├── generar_bibliografia_simple.py
├── GENERAR_REFERENCIAS.bat
└── GUIA_BIBLIOGRAFIA.md
```

---

## 📊 **DATOS NUMÉRICOS CLAVE (Para Tablas)**

### **Cohorte (N=10):**
```
Edad:             31.2 ± 8.4 años
Sexo M/F:         6 / 4
IMC:              25.8 ± 3.2 kg/m²
Peso:             72.5 ± 12.1 kg
Altura:           168.3 ± 8.9 cm
Seguimiento:      15.8 ± 2.3 semanas
Total semanas:    183
Semanas válidas:  158
% Imputado:       13.7%
```

### **Métricas de Rendimiento:**
```
F1-Score:   0.857
Precision:  0.880
Recall:     0.857
Accuracy:   0.873
MCC:        0.746
```

### **LOUO (Media ± DE):**
```
F1:         0.847 ± 0.041 (CV: 4.8%)
Precision:  0.864 ± 0.042 (CV: 4.9%)
Recall:     0.831 ± 0.041 (CV: 4.9%)
```

### **Clustering:**
```
K óptimo:          2
Silhouette Score:  0.232
Método:            K-Means
Validación:        Mann-Whitney U
```

---

## 🎯 **RESUMEN PARA POSEIDÓN**

### **✅ TIENES ACCESO DIRECTO A:**
1. 178 figuras PNG (147 pre-existentes + 31 extraídas del PDF)
2. 64 archivos CSV (tablas y datasets)
3. 5 documentos técnicos (3 PDFs + 5 markdowns)
4. 12 scripts Python ejecutados
5. 15 referencias BibTeX

### **📂 RUTAS PRINCIPALES:**
```python
# Figuras
"4 semestre_dataset/documentos_tesis/figuras/"

# Tablas
"4 semestre_dataset/documentos_tesis/tablas/"

# Informe principal
"4 semestre_dataset/documentos_tesis/INFORME_TECNICO_ACTUALIZADO_V3.pdf"

# Referencias
"4 semestre_dataset/edicion_tesis/tesis_luisangel/referencias.bib"

# Capítulos para revisar
"4 semestre_dataset/edicion_tesis/tesis_luisangel/capitulos/01_introduccion.tex"
"4 semestre_dataset/edicion_tesis/tesis_luisangel/capitulos/07_discusion.tex"
```

---

**¡TODO LISTO PARA QUE POSEIDÓN COMIENCE SU TRABAJO EDITORIAL!** 🔱

---

**Última actualización:** 4 de Noviembre de 2025, 21:15 hrs  
**Responsable:** Rayo Veloz ⚡  
**Estado:** ✅ Recursos completos y organizados

