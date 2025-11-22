# 🔱 SOLICITUD DE REVISIÓN CRÍTICA CAP. 5-6 PARA POSEIDÓN

**De:** Rayo Veloz ⚡ y Luis Ángel 🐢  
**Para:** Poseidón 🔱  
**Fecha:** 5 de Noviembre de 2025, 21:45 hrs  
**Prioridad:** 🔴 ALTA - Revisión quirúrgica requerida  
**Estado:** ✅ FASE 3B completada | ⚠️ Requiere pulido milimétrico

---

## 🎯 **CONTEXTO:**

Rayo Veloz completó FASE 3B (reescritura Cap. 5 + expansión Cap. 6) con 498 líneas de LaTeX científico y 15+ referencias Q1/Q2 integradas. 

**Commit:** `725e66f` | **Archivos modificados:** 2 | **Líneas:** +8,474 / -7,243

**Luis revisó el PDF compilado (páginas 38-65) e identificó 7 problemas críticos que requieren tu expertise.**

---

## 🔥 **PROBLEMAS CRÍTICOS IDENTIFICADOS POR LUIS:**

### **PROBLEMA 1: CITAS MAL FORMATEADAS** 🚨

**Ubicación:** A lo largo de todo Cap. 5 y 6

**Síntoma observado en el PDF:**
```
Healy et al. Healy2024
Prince et al. Prince2008
Gonçalves et al. Goncalves2021
Schrack2018; Ho2022 Riebe2018
```

**Diagnóstico:** Las referencias BibTeX:
- No están en `referencias.bib`, o
- Tienen claves incorrectas, o
- `biber` no se ejecutó correctamente

**Impacto:** ⛔ BLOQUEANTE para envío a comité tutorial

**Acción requerida:**
1. Verificar que TODAS las referencias citadas en Cap. 5-6 estén en `referencias.bib`
2. Validar formato BibTeX (autor, año, DOI, journal)
3. Confirmar que las claves coincidan exactamente (case-sensitive)
4. Probar compilación con `biber` (no `bibtex`)

**Referencias críticas faltantes:**
- Healy2024, Prince2008, Goncalves2021
- Schrack2018, Ho2022, Riebe2018, Yamada2019, Harris1918
- TaskForce1996, Laborde2017, Soares-Miranda2014
- Alinia2020, Crozat2025, Rousseeuw1987, Mullick2022, Kaveh2024, Ricotti2023
- Schuch2018, WHO2020

---

### **PROBLEMA 2: TIEMPOS VERBALES INCORRECTOS** ⏰

**Ubicación:** Secciones 5.2.2 (Criterios de selección) y 5.2.3 (Tamaño de muestra)

**Ejemplo observado:**
> "Los criterios de selección **se basarán** en la afinidad de los participantes..."

**Error:** Tiempo futuro, cuando el estudio **YA se realizó** (2021-2024).

**Corrección requerida:** Cambiar TODO a **pretérito**:
> "Los criterios de selección **se basaron** en la afinidad de los participantes..."

**Acción requerida:**
- Revisar secciones 5.2.2, 5.2.3, 5.2.4 (Población de Estudio)
- Cambiar "se basarán", "estará compuesta", "determinaremos" → pasado
- Validar coherencia temporal en todo Cap. 5

---

### **PROBLEMA 3: TABLA 5.1 MAL UBICADA** 📊

**Ubicación:** 
- **Referenciada en:** Sección 5.3.5 (página ~39)
- **Aparece en:** Página 42 (3 páginas después)

**Impacto:** Rompe el flujo de lectura. El lector busca la tabla y no la encuentra.

**Acción requerida:**
- Mover `\begin{table}` de Tabla 5.1 para que aparezca INMEDIATAMENTE después de su primera mención en 5.3.5
- Alternativamente, usar `[h!]` (here!) en lugar de `[p]` (page) en el entorno `table`

---

### **PROBLEMA 4: FALTA NARRATIVA CRONOLÓGICA COMPLETA** 📖

**Ubicación:** Antes de Sección 5.4 (Ingeniería de Características)

**Problema:** Saltamos directo a Feature Engineering **SIN EXPLICAR:**
1. ❌ Conversión XML → CSV (script de Gaur)
2. ❌ Variables originales extraídas de Apple Health
3. ❌ Análisis Exploratorio de Datos (EDA)
4. ❌ Problemas detectados (missingness, outliers, CV >100%)
5. ❌ Justificación del Feature Engineering como solución

**Flujo narrativo correcto (orden cronológico):**
```
5.6.1 Selección del Dispositivo (revisión 423 dispositivos)
      ↓
5.6.2 Análisis de Sensores (acelerómetro, PPG, GPS)
      ↓
5.6.3 Elección de Apple Watch (49% cuota mercado, uniformidad)
      ↓
5.6.4 Convocatoria y Reclutamiento (N=10, Facultad Medicina)
      ↓
5.6.5 Consentimientos Informados (ética, privacidad)
      ↓
5.6.6 Recepción de Datos XML (export.zip por participante)
      ↓
5.6.7 Conversión XML → CSV (apple_health_data_converter.py)
      ↓
5.6.8 Variables Originales Extraídas (Tabla 5.X)
      ↓
5.6.9 Análisis Exploratorio de Datos (EDA)
      ↓
5.6.10 Detección de Problemas (missingness, CV, outliers)
      ↓
5.4 Ingeniería de Características (solución diseñada)
```

**Acción requerida:**
- Leer los 6 archivos técnicos maestros (ver sección ARCHIVOS DE REFERENCIA)
- Extraer la narrativa completa del proceso
- Escribir **nueva sección 5.3.6 "Preprocesamiento y Análisis Exploratorio"** (~150 líneas)
- Incluir:
  - Tabla de variables originales de Apple Health
  - Figura de missingness por usuario
  - Figura de CV por variable (ya existe: `coeficiente_de_variacion.png`)
  - Justificación de por qué se crearon las 4 variables derivadas

---

### **PROBLEMA 5: FALTA TABLA DE ECUACIONES Y NOMENCLATURA** 📐

**Ubicación:** Anexos (Cap. 9)

**Problema:** El documento tiene múltiples ecuaciones matemáticas pero:
- ❌ No hay índice de ecuaciones en anexos
- ❌ No hay tabla de nomenclatura (significado de símbolos)

**Ecuaciones presentes en el documento:**
1. Actividad\_relativa (Ec. 5.1)
2. Superávit\_calórico\_basal (Ec. 5.2)
3. TMB hombres (Ec. 5.3)
4. TMB mujeres (Ec. 5.4)
5. Delta\_cardíaco (Ec. 5.5)
6. FCmáx Fox & Haskell (Ec. 2.X)
7. FCmáx Tanaka (Ec. 2.X)
8. FCobj Karvonen (Ec. 2.X)

**Acción requerida:**
- Crear **Anexo A: Índice de Ecuaciones**
- Crear **Anexo B: Tabla de Nomenclatura** con formato:

```latex
\begin{longtable}{cl}
\toprule
\textbf{Símbolo} & \textbf{Descripción} \\
\midrule
FC & Frecuencia Cardíaca (lpm) \\
FCmáx & Frecuencia Cardíaca Máxima (lpm) \\
HRV-SDNN & Heart Rate Variability - Standard Deviation of NN intervals (ms) \\
TMB & Tasa Metabólica Basal (kcal/día) \\
MET & Equivalente Metabólico \\
...
\end{longtable}
```

---

### **PROBLEMA 6: FIGURAS MAL FORMATEADAS (APA 7)** 🖼️

**Ubicación:** Figura 5.1 (y posiblemente otras)

**Problema observado en el PDF:**
```
Figura 5.1: Diagrama de flujo del proceso de implementación 
del proyecto de investigación, desde la obtención de datos 
hasta la selección, extracción, limpieza y procesamiento de 
las variables Recepción yalmacenamientosegurodedatos,los
participantes generaron un archivo export.zip...
[TEXTO LARGO PEGADO AL CAPTION]
```

**Errores:**
1. ❌ Caption demasiado largo (debe ser 1-2 líneas máximo)
2. ❌ Texto descriptivo pegado al caption (debe ir ANTES en párrafo aparte)
3. ❌ Figura no aparece DESPUÉS de su primera mención

**Formato APA 7 correcto:**

**ANTES de la figura (en el texto):**
```latex
La Figura~\ref{fig:diagrama_flujo} ilustra el proceso completo 
de implementación del proyecto, desde la recepción de archivos 
XML hasta la generación de variables derivadas. Los participantes 
generaron un archivo \texttt{export.zip} a través de la aplicación 
Apple Health...
[PÁRRAFO COMPLETO EXPLICATIVO]

\begin{figure}[h!]
    \centering
    \includegraphics[width=0.9\textwidth]{figuras/diagrama_de_flujo_fig3.png}
    \caption{Diagrama de flujo del proceso de implementación}
    \label{fig:diagrama_flujo}
\end{figure}
```

**Acción requerida:**
- Revisar TODAS las figuras en Cap. 5-6
- Separar caption (corto) de texto explicativo (largo)
- Ubicar figuras DESPUÉS de su primera mención con `[h!]` o `[htbp]`
- Validar numeración secuencial (Figura 5.1, 5.2, 5.3...)

---

### **PROBLEMA 7: SECCIONES 5.6.4 a 5.9 SIN MEJORAR** 🔧

**Ubicación:** Secciones 5.6.4 (Elección Apple Watch) hasta 5.9 (Financiamiento)

**Problema:** Estas secciones quedaron del draft anterior **SIN INTEGRAR:**
- ❌ Literatura Q1/Q2 reciente
- ❌ Conexión con el pipeline metodológico
- ❌ Redundancias con secciones anteriores

**Contenido actual (draft viejo):**
- 5.6.4: Elección del Apple Watch (narrativa básica)
- 5.7: Protocolo del Instrumento (XML → CSV, pero mal ubicado)
- 5.8: Base Metodológica del Sistema de Inferencia Difusa (incompleta)
- 5.9: Aspectos Éticos y de Bioseguridad (correcta, pero verbos en futuro)

**Acción requerida:**
- **5.6.4:** Integrar con datos de mercado (Canalys 2024)
- **5.7:** MOVER contenido a nueva sección 5.3.6 (antes de Feature Engineering)
- **5.8:** Expandir con fundamento filosófico de Zadeh (Granularidad Cognitiva, Ley de Incompatibilidad)
- **5.9:** Cambiar tiempos verbales a pasado

---

## 📚 **ARCHIVOS DE REFERENCIA TÉCNICA (LECTURA OBLIGATORIA):**

Poseidón, para reconstruir la narrativa cronológica completa, **DEBES LEER** estos 6 archivos maestros del proyecto:

### **1. Metodología y Pipeline:**
```
4 semestre_dataset/documentos_tesis/00_metodologia_y_plan_pipeline.md
```
**Contenido:** Descripción paso a paso del pipeline de 5 fases (EDA → Clustering → Fuzzy → LOUO → Robustez)

### **2. Informe Maestro Completo:**
```
4 semestre_dataset/documentos_tesis/INFORME_MAESTRO_SISTEMA_DIFUSO_SEDENTARISMO.md
```
**Contenido:** Documento consolidado con toda la investigación (metodología + resultados + análisis)

### **3. Roadmap del Proyecto:**
```
4 semestre_dataset/documentos_tesis/ROADMAP_PROYECTO_COMPLETO.md
```
**Contenido:** Visión general del proyecto, decisiones metodológicas clave, pivote SF-36

### **4. Pseudocódigo del Pipeline:**
```
4 semestre_dataset/documentos_tesis/PSEUDOCODIGO_PIPELINE_COMPLETO.txt
```
**Contenido:** Código paso a paso (XML → CSV → EDA → Feature Engineering → Clustering → Fuzzy)

### **5. Resumen EDA y Visualizaciones:**
```
4 semestre_dataset/documentos_tesis/RESUMEN_ACTUALIZACION_EDA_Y_VISUALIZACIONES.md
```
**Contenido:** Análisis exploratorio completo (missingness, outliers, CV, correlaciones)

### **6. Informe Técnico LaTeX (versión anterior):**
```
4 semestre_dataset/documentos_tesis/INFORME_TECNICO_ACTUALIZADO_V3.tex
```
**Contenido:** Versión previa del documento con descripciones detalladas (puede tener material útil)

---

## 🎯 **SOLICITUD ESPECÍFICA PARA POSEIDÓN:**

### **TAREA 1: Validación de Referencias BibTeX** ⏱️ 30 min

1. Abrir `4 semestre_dataset/edicion_tesis/tesis_luisangel/referencias.bib`
2. Verificar que existan las 20+ referencias citadas en Cap. 5-6
3. Añadir las faltantes con formato correcto (autor, título, journal, año, DOI, volume, pages)
4. Validar claves exactas (Healy2024, Prince2008, Schrack2018, etc.)
5. Probar compilación con `biber`

**Entregable:** `referencias.bib` actualizado + reporte de referencias añadidas

---

### **TAREA 2: Corrección de Tiempos Verbales** ⏱️ 15 min

1. Abrir `05_materiales_metodos.tex`
2. Buscar secciones 5.2.2, 5.2.3, 5.2.4, 5.9
3. Cambiar TODOS los verbos en futuro → pretérito
4. Validar coherencia temporal en todo el capítulo

**Entregable:** Archivo corregido

---

### **TAREA 3: Reubicación de Tabla 5.1** ⏱️ 10 min

1. Identificar primera mención de Tabla 5.1 en sección 5.3.5
2. Mover el entorno `\begin{table}` para que aparezca inmediatamente después
3. Cambiar parámetro de ubicación: `[p]` → `[h!]` o `[htbp]`

**Entregable:** Tabla correctamente ubicada

---

### **TAREA 4: Escribir Nueva Sección 5.3.6 "Preprocesamiento y EDA"** ⏱️ 2 horas

**Objetivo:** Llenar el vacío narrativo entre "recepción de datos" y "feature engineering"

**Estructura propuesta:**
```latex
\subsection{Preprocesamiento y Análisis Exploratorio de Datos}
\label{subsec:preprocesamiento_eda}

\subsubsection{Extracción de Variables desde Apple Health}
[Explicar conversión XML → CSV con script de Gaur]
[Incluir Tabla 5.X con las 9 variables originales extraídas]

\subsubsection{Análisis de Calidad de Datos}
[Describir análisis de missingness por usuario]
[Citar figura existente: coeficiente_de_variacion.png]
[Reportar CV >100% en minutos_ejercicio, justificando agregación semanal]

\subsubsection{Detección de Problemas y Justificación del Feature Engineering}
[Explicar por qué las variables raw no son comparables entre usuarios]
[Fundamentar la necesidad de normalización intra-sujeto]
[Transición natural a Sección 5.4 Feature Engineering]
```

**Fuentes:** Leer los 6 archivos técnicos listados arriba

**Entregable:** ~150 líneas LaTeX con 3 subsubsecciones + 1 tabla + 2 referencias a figuras existentes

---

### **TAREA 5: Corrección de Formato de Figuras (APA 7)** ⏱️ 45 min

1. Identificar TODAS las figuras en Cap. 5-6
2. Para cada figura:
   - Separar caption (1-2 líneas) de texto explicativo (párrafo antes de la figura)
   - Ubicar figura DESPUÉS de primera mención
   - Validar numeración secuencial
   - Aplicar formato APA 7 (ver ejemplo en Problema 6)

**Entregable:** Todas las figuras correctamente formateadas

---

### **TAREA 6: Mejora de Secciones 5.6.4 a 5.9** ⏱️ 1 hora

1. **5.6.4 (Elección Apple Watch):** Añadir datos de Canalys 2024 (49% cuota mercado)
2. **5.7 (Protocolo):** MOVER contenido técnico a nueva 5.3.6, dejar solo descripción general
3. **5.8 (Base Metodológica Fuzzy):** Expandir con:
   - Principio de Granularidad Cognitiva (Zadeh)
   - Ley de Incompatibilidad (Zadeh)
   - Teorema Stone-Weierstrass (aproximación universal)
4. **5.9 (Ética):** Cambiar verbos a pasado

**Entregable:** 4 secciones mejoradas

---

### **TAREA 7: Crear Anexos A y B** ⏱️ 30 min

**Anexo A: Índice de Ecuaciones**
```latex
\chapter{Índice de Ecuaciones}
\label{chap:indice_ecuaciones}

\begin{longtable}{cl}
\toprule
\textbf{Ecuación} & \textbf{Descripción} \\
\midrule
Ec. 2.1 & Frecuencia Cardíaca Máxima (Fox \& Haskell) \\
Ec. 2.2 & Frecuencia Cardíaca Máxima (Tanaka) \\
...
\end{longtable}
```

**Anexo B: Tabla de Nomenclatura**
[Todos los símbolos usados en ecuaciones con sus definiciones]

**Entregable:** 2 nuevos archivos en `capitulos/09_anexos.tex`

---

## ⏰ **ESTIMACIÓN TEMPORAL TOTAL:** 5-6 horas

| Tarea | Tiempo Estimado | Prioridad |
|-------|----------------|-----------|
| TAREA 1: Referencias BibTeX | 30 min | 🔴 CRÍTICA |
| TAREA 2: Tiempos verbales | 15 min | 🟡 ALTA |
| TAREA 3: Reubicación Tabla 5.1 | 10 min | 🟡 ALTA |
| TAREA 4: Nueva Sección 5.3.6 | 2 horas | 🔴 CRÍTICA |
| TAREA 5: Formato Figuras APA 7 | 45 min | 🟡 ALTA |
| TAREA 6: Mejora Secciones 5.6-5.9 | 1 hora | 🟢 MEDIA |
| TAREA 7: Anexos A y B | 30 min | 🟢 MEDIA |
| **TOTAL** | **5-6 horas** | |

---

## 📊 **ENTREGABLES FINALES:**

1. ✅ `referencias.bib` completo con 80+ referencias validadas
2. ✅ `05_materiales_metodos.tex` corregido (tiempos verbales + nueva sección 5.3.6)
3. ✅ `06_resultados.tex` con figuras APA 7
4. ✅ `09_anexos.tex` con Índice de Ecuaciones + Nomenclatura
5. ✅ Reporte de cambios realizados (Markdown)
6. ✅ PDF compilado sin errores de citación

---

## 🤝 **MENSAJE DE RAYO VELOZ:**

Poseidón, hermano del Olimpo:

Luis tiene razón en TODAS sus observaciones. En mi afán de completar FASE 3B rápido (hiperfoco de 2.5 horas), prioricé **contenido científico** sobre **pulido quirúrgico**.

**Resultado:**
- ✅ 498 líneas de ciencia Q1 escritas
- ⚠️ 7 problemas de formato/narrativa pendientes

**Tu expertise en revisión crítica es CRUCIAL para llevar esto a nivel publicable.**

**Confío en ti para:**
1. 🔍 Validar cada cita (eres el maestro de BibTeX)
2. 📖 Reconstruir la narrativa cronológica (lees mejor los archivos técnicos)
3. 🎨 Aplicar APA 7 con precisión milimétrica (tienes ojo clínico)

**Mientras Luis termina su revisión de Cap. 6, tú pulifes Cap. 5.**

**Después, revisión cruzada entre los 3 (tú, yo, Luis) para calidad final.**

---

## 🔱 **¿ACEPTAS LA MISIÓN?**

**Si aceptas:**
- Responde con "✅ MISIÓN ACEPTADA - Iniciando TAREA 1"
- Prioriza TAREA 1 (Referencias BibTeX) y TAREA 4 (Sección 5.3.6)
- Reporta avances cada 1-2 horas

**Si necesitas clarificación:**
- Pregunta lo que necesites
- Rayo Veloz está en standby para apoyar

---

**Unidos, hacia la meta final.** 🌊⚡🐢

---

---

## 🔥 **ACTUALIZACIÓN: NUEVOS PROBLEMAS IDENTIFICADOS (Revisión Luis 22:00)**

### **PROBLEMA 8: EXTRANJERISMOS SIN TRADUCIR** 🌐

**Ubicación:** Todo el documento (Cap. 5 y 6)

**Ejemplos a corregir:**
| ❌ Incorrecto | ✅ Correcto |
|--------------|-------------|
| pipeline metodológico | secuencia metodológica / tubería metodológica |
| dataset | conjunto de datos |
| features | características |
| clustering | agrupamiento / análisis de conglomerados |
| gold standard | estándar de oro / referencia de oro |
| data-driven | basado en datos / guiado por datos |
| Leave-One-User-Out (LOUO) | Validación dejando un usuario fuera |
| wearables | dispositivos portátiles |
| outliers | valores atípicos |
| missingness | datos faltantes / ausencia de datos |

**Acción requerida:** 
1. Búsqueda global de extranjerismos en Cap. 5-6
2. Reemplazar por términos en español
3. Mantener término en inglés SOLO si se explica entre paréntesis la primera vez

**Ejemplo correcto:**
> "Se implementó una validación cruzada dejando un usuario fuera (Leave-One-User-Out, LOUO)..."

---

### **PROBLEMA 9: FIGURAS MENCIONADAS PERO NO VISIBLES** 🖼️

**Ubicación:** Sección 6.1, línea ~22 de `06_resultados.tex`

**Texto que menciona figura inexistente:**
> "Como se observa en el mapa de calor de variabilidad, algunos usuarios exhiben patrones más consistentes (CV más bajos) que otros."

**Problema:** La frase dice "como se observa" pero NO HAY FIGURA visible.

**Diagnóstico:** 
- La figura existe: `coeficiente_de_variacion.png`
- Pero fue insertada con parámetro `[htbp]` que LaTeX movió a otra página
- O no se insertó en absoluto y solo quedó el texto descriptivo

**Acción requerida:**
1. Verificar que `\begin{figure}` con `coeficiente_de_variacion.png` exista ANTES de esa frase
2. Si no existe, insertar la figura con parámetro `[h!]` (here, force)
3. Si existe pero está lejos, cambiar parámetro a `[h!]`
4. Añadir referencia explícita: "Como se observa en la Figura~\ref{fig:mapa_calor_variabilidad}..."

---

### **PROBLEMA 10: CAP. 6 MUY COMPRIMIDO vs. INFORME TÉCNICO** 📊

**Estadísticas alarmantes:**
- 📄 **Informe Técnico V3:** 110 páginas
- 📄 **Cap. 6 Resultados actual:** ~15 páginas
- ⚠️ **Compresión:** Se perdió el **86% del contenido**

**Material crítico faltante en Cap. 6:**

#### **6.1 Caracterización - Falta:**
- ❌ Tabla de estadísticos descriptivos por usuario (media ± SD de las 8 variables)
- ❌ Análisis de missingness detallado (% datos faltantes por usuario/variable)
- ❌ Figura de distribuciones de variables raw (histogramas o boxplots)

#### **6.2 Clustering - Falta:**
- ❌ Análisis de VIF (multicolinealidad) - solo se menciona "VIF<5" sin tabla
- ❌ Comparación de K=2 vs K=3 vs K=4 (Silhouette scores)
- ❌ Tabla de caracterización de perfiles (mediana [IQR] por cluster)
- ❌ **Prueba Mann-Whitney U** (p-values y tamaño efecto Cohen's d entre clusters)

#### **6.3 Rendimiento - Falta:**
- ❌ Análisis de optimización de umbral τ (gráfico τ vs F1-Score)
- ❌ Boxplot de F1-Score por usuario (ya se menciona en Tabla pero no gráfico)
- ❌ Análisis de errores: ¿Qué semanas se clasifican mal y por qué?
- ❌ Comparación de distribución de score fuzzy entre clusters

#### **6.4 Robustez - Falta:**
- ❌ Gráfico de caída de rendimiento (modelo completo vs reducido)
- ❌ Análisis de sensibilidad por variable individual (qué pasa si quitamos solo HRV, solo Delta, etc.)

---

## 📊 **INVENTARIO COMPLETO DE FIGURAS DISPONIBLES:**

### **Figuras YA insertadas en Cap. 6:**
1. ✅ `coeficiente_de_variacion.png` (Figura 6.1)
2. ✅ `variabilidadoperativa_vs_observada.png` (Figura 6.2)
3. ✅ `matriz_correlacion_features_clustering.png` (Figura 6.3)
4. ✅ `PCA_elbow_vs_shilloete.png` (Figura 6.4)
5. ✅ `PCA_biplot.png` (Figura 6.5)
6. ✅ `perfiles_de_clusters.png` (Figura 6.6)
7. ✅ `analisis_robustez.png` (Figura 6.7)

### **Figuras disponibles pero NO insertadas:**
8. ⚠️ `diagrama_de_tesis.png` (debería ir en Cap. 6, sección "Tesis")
9. ⚠️ Falta: Boxplot LOUO por usuario (mencionado en texto, no existe archivo)
10. ⚠️ Falta: Gráfico de optimización de τ (threshold)
11. ⚠️ Falta: Distribución de score fuzzy por cluster

### **Figuras de Cap. 5 (Metodología):**
12. ✅ `diagrama_de_flujo_fig3.png` (Figura 5.1 - REVISAR FORMATO)
13. ✅ `Funciones_de_membresias_trapezoidales_fig4.png` (Figura 5.2)
14. ✅ `Salida_difusa_figura_5.png` (Figura 5.3)
15. ✅ `acelerometro_modelo_MMA7361.png` (Figura 2.X - Marco Teórico)
16. ✅ `PPG_modelo_ADPD1081.png` (Figura 2.X - Marco Teórico)

---

## 🎯 **TAREAS ADICIONALES PARA POSEIDÓN:**

### **TAREA 8: Eliminar Extranjerismos** ⏱️ 30 min

1. Buscar con grep todos los extranjerismos en Cap. 5-6
2. Reemplazar con términos en español (usar tabla de referencia)
3. Mantener término inglés entre paréntesis solo en primera mención

**Entregable:** Documento sin extranjerismos innecesarios

---

### **TAREA 9: Corregir Referencias a Figuras Invisibles** ⏱️ 15 min

1. Buscar todas las frases "como se observa", "como se muestra", "según la figura"
2. Verificar que la figura referenciada esté VISIBLE cerca del texto
3. Corregir parámetros de ubicación `[p]` → `[h!]`
4. Añadir referencias explícitas con `\ref{}`

**Entregable:** Todas las figuras mencionadas son visibles

---

### **TAREA 10: Expandir Cap. 6 con Material del Informe Técnico** ⏱️ 3-4 horas

**Objetivo:** Pasar de 15 páginas a ~30-35 páginas en Cap. 6

**Fuente:** `4 semestre_dataset/documentos_tesis/INFORME_TECNICO_ACTUALIZADO_V3.tex`

**Subsecciones a añadir:**

#### **6.1.1 Estadísticos Descriptivos Detallados**
- Tabla con media ± SD de las 8 variables por usuario
- Análisis de missingness (% datos faltantes)

#### **6.2.1 Análisis de Multicolinealidad**
- Tabla de VIF por variable
- Interpretación (VIF<5 confirma independencia)

#### **6.2.2 Caracterización Estadística de Perfiles**
- Tabla: Mediana [IQR] de cada variable por cluster
- Prueba Mann-Whitney U (p-values)
- Tamaño del efecto Cohen's d

#### **6.3.1 Optimización del Umbral de Decisión**
- Descripción del proceso de búsqueda de τ óptimo
- Gráfico: τ vs F1-Score (si existe en informe técnico)

#### **6.3.2 Análisis de Errores de Clasificación**
- ¿Qué usuarios tienen más errores? (u2, u3, u8)
- ¿Por qué? (alta variabilidad intra-semanal)
- Distribución de score fuzzy por cluster

**Entregable:** Cap. 6 expandido a 30-35 páginas con contenido del informe técnico

---

## ⏰ **NUEVA ESTIMACIÓN TEMPORAL TOTAL:** 10-12 horas

| Tarea Original | Tiempo | Nuevas Tareas | Tiempo |
|----------------|--------|---------------|--------|
| TAREA 1: Referencias BibTeX | 30 min | TAREA 8: Extranjerismos | 30 min |
| TAREA 2: Tiempos verbales | 15 min | TAREA 9: Figuras invisibles | 15 min |
| TAREA 3: Tabla 5.1 | 10 min | **TAREA 10: Expandir Cap. 6** | **3-4 horas** |
| TAREA 4: Sección 5.3.6 EDA | 2 horas | | |
| TAREA 5: Formato Figuras | 45 min | | |
| TAREA 6: Mejora 5.6-5.9 | 1 hora | | |
| TAREA 7: Anexos A y B | 30 min | | |
| **SUBTOTAL ORIGINAL** | **5-6 horas** | **SUBTOTAL NUEVO** | **4-5 horas** |
| | | **TOTAL GENERAL** | **10-12 horas** |

---

**Creado:** 5 Nov 2025, 21:45 hrs  
**Actualizado:** 5 Nov 2025, 22:15 hrs (+3 problemas, +3 tareas, +5 horas estimadas)  
**Estado:** 🔴 URGENTE - Revisión crítica solicitada  
**Agentes:** Rayo Veloz ⚡ + Luis Ángel 🐢 → Poseidón 🔱

