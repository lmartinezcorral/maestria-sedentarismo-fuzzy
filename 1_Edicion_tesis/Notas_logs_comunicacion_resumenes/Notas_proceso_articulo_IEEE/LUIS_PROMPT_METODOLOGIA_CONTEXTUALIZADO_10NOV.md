# 📝 PROMPT CONTEXTUALIZADO: REDACCIÓN DE METODOLOGÍA
## Artículo IEEE JBHI - Sistema de Inferencia Difusa para Clasificación de Comportamiento Sedentario

**Fecha:** 10 de noviembre de 2025  
**Autor del Prompt:** Luis Ángel Martínez Corral  
**Contexto:** Tarea para Clase de Redacción de Manuscritos Científicos  
**Nivel Objetivo:** Publicación SCOPUS Q1 / IEEE Journal of Biomedical and Health Informatics

---

## 🎯 OBJETIVO DEL PROMPT

Redactar la sección de **Metodología** completa para el artículo científico que ya cuenta con:
- ✅ Título definido
- ✅ Autores y afiliaciones
- ✅ Abstract (~300 palabras)
- ✅ Introducción (~1,010 palabras con 3 subsecciones)

**Resultado esperado:** Sección de Metodología publicable en revista Q1, 100% replicable, rigurosamente detallada.

---

## 📄 DOCUMENTOS DE REFERENCIA OBLIGATORIOS

**Para contextualizar la redacción, consultar:**

1. **`07_discusion.tex`** (Capítulo 7 Tesis EXCELENCIA)
   - Contiene descripción detallada del proceso metodológico
   - Incluye decisiones de diseño justificadas
   - Documenta limitaciones reconocidas

2. **`ADES_AUDITORIA_PROFUNDA_EVIDENCIA_REAL_6NOV.md`**
   - Tabla de DATOS REALES CERTIFICADOS del proyecto
   - N=10 usuarios
   - 1,337 semanas válidas
   - Métricas verificadas (F1=0.780±0.167 LOUO, F1=0.840 global)

3. **`RAYO_INVENTARIO_COMPLETO_ARCHIVOS_6NOV.md`**
   - Logs de ejecución de scripts
   - Variables derivadas documentadas
   - Pipeline técnico verificado

4. **`main_esp.tex`** (secciones ya escritas)
   - Introducción contextualizada
   - Abstract con metodología resumida
   - Referencias a consultar

5. **`referencias_ieee_jbhi.bib`**
   - 63 referencias bibliográficas disponibles
   - Categorizadas por tema
   - 18 artículos 2023-2025 verificados

---

## 📋 ESTRUCTURA REQUERIDA DE METODOLOGÍA

**SECCIÓN II: METODOLOGÍA** (Formato IEEE JBHI)

Debe incluir las siguientes **subsecciones obligatorias:**

### **2.1. Tipo y Diseño del Estudio**
- Especificar: Estudio longitudinal observacional retrospectivo
- Justificar: Paradigma BYOD (Bring Your Own Device)
- Temporalidad: Enero 2020 - Julio 2024
- Aprobación ética: Comité Ética FMCB-UACH (registro FMCB-2024-001)
- Citar: Directrices STROBE para estudios observacionales

**Extensión:** 125-150 palabras  
**Referencias:** 2-3 (STROBE, BYOD, ética investigación)

---

### **2.2. Participantes**

**Debe incluir:**
- N=10 participantes (5 mujeres, 5 hombres)
- Edad: 34.2±6.7 años (rango: 25-45 años estimado)
- IMC: 24.8±3.2 kg/m²
- Criterios inclusión:
  - Edad 18-65 años
  - Uso Apple Watch ≥6 meses
  - Adherencia ≥80% disponibilidad datos
  - Consentimiento informado escrito
- Criterios exclusión:
  - Enfermedad cardiovascular establecida
  - Uso marcapasos
  - Embarazo
  - Trastornos movilidad severos
- Reclutamiento: Muestreo por conveniencia (Universidad Autónoma Chihuahua)
- Seguimiento: Media 133.7 semanas (rango: 7-298 semanas)
- Total datos: 9,185 días registro continuo → 1,337 semanas válidas

**Extensión:** 150-180 palabras  
**Referencias:** 1-2 (muestreo conveniencia, estudios BYOD)

---

### **2.3. Instrumentos y Variables**

**A) Dispositivo de Medición:**
- **Apple Watch** (Series 3-9)
- **Ecosistema HealthKit** (iOS)
- Variables biométricas capturadas:
  1. Horas estacionarias (sedentarismo directo)
  2. Horas con deambulación
  3. Pasos diarios
  4. Distancia recorrida (km)
  5. Gasto calórico activo (kcal)
  6. Frecuencia cardíaca en reposo (FCr, bpm)
  7. Frecuencia cardíaca al caminar (FC_walk, bpm)
  8. Variabilidad frecuencia cardíaca (HRV-SDNN, ms)

**Citar:**
- Validación Apple Watch: Shcherbina2017, Bent2020, OGrady2024AppleWatch
- Precisión HRV: Shaffer2017, Thayer2009

**B) Variables Derivadas (Ingeniería de Características):**

**Creadas mediante normalización antropométrica:**

1. **Actividad Relativa:**
   $$\text{Act}_{\text{rel}} = \frac{\text{Pasos}_{\text{diarios}}}{\text{TMB} \times \text{Peso} \times \text{Altura}}$$
   - Justificación: Comparabilidad inter-sujeto
   - TMB: Tasa Metabólica Basal (ecuación Mifflin-St Jeor)

2. **Superávit Calórico Basal:**
   $$\text{Superávit} = \frac{\text{Gasto}_{\text{activo}}}{\text{TMB}}$$
   - Interpretación: Exceso energético respecto metabolismo basal

3. **HRV-SDNN Normalizado:**
   - Percentil 50 (mediana) semanal de SDNN
   - Agregación: Reducir ruido diario

4. **Delta Cardíaco:**
   $$\Delta_{\text{FC}} = \text{FC}_{\text{caminar}} - \text{FCr}_{\text{promedio}}$$
   - Interpretación: Respuesta cardiovascular al ejercicio

**Citar:**
- Feature engineering: Guyon2003
- Normalización antropométrica: Mifflin1990
- Agregación temporal: Chastin2015, Dumuid2018

**Extensión:** 250-280 palabras  
**Referencias:** 6-8 artículos

---

### **2.4. Adquisición y Preprocesamiento de Datos**

**Etapas del pipeline:**

**A) Exportación datos:**
- Aplicación nativa Health (iOS)
- Formato: XML HealthKit
- Frecuencia: Registros diarios automáticos
- Período: Enero 2020 - Julio 2024

**B) Limpieza y validación:**
- Criterio calidad: ≥3 valores válidos por semana
- Detección outliers: Winsorización percentiles 1-99
- Valores fisiológicamente imposibles eliminados

**C) Imputación jerárquica datos faltantes (<15% total):**
- **Nivel 1:** Mediana del usuario (si ≥3 valores válidos en semana)
- **Nivel 2:** Forward-fill (arrastrar último valor válido)
- **Nivel 3:** Backward-fill (arrastrar siguiente valor válido)

**Citar:**
- Imputación: Little1988, Azur2011
- Manejo outliers: Rousseeuw1987

**D) Agregación temporal:**
- Unidad análisis: **Semana** (lunes-domingo)
- Estadísticos: p10, p25, p50 (mediana), p75, p90
- Justificación: Capturar distribución completa comportamiento

**Citar:**
- Análisis compositional 24-h: Chastin2015, Dumuid2018

**Extensión:** 200-230 palabras  
**Referencias:** 4-5

---

### **2.5. Establecimiento de Ground Truth Operativa: Clustering No Supervisado**

**Algoritmo:**
- **K-Means clustering** (Scikit-learn 1.3.0)
- **K=2** clústeres (determinado por método del codo + Silhouette)
- **Distancia:** Euclidiana
- **Inicialización:** k-means++ (reproducible)
- **Iteraciones:** Máximo 300, tolerancia=1e-4

**Variables de entrada clustering:**
- Actividad_relativa_p50
- Superávit_calórico_p50
- Delta_cardíaco_p50
- HRV_SDNN_p50

**Validación estadística de clústeres:**
- **Índice Silhouette** (calidad separación)
- **Coeficiente Davies-Bouldin** (compacidad)
- **Pruebas Mann-Whitney U** (comparación centroides)
- **d de Cohen** (tamaño efecto diferencias)
- **Criterio aceptación:** p<0.05, |d|>0.80

**Interpretación clústeres:**
- Clúster 0: "Bajo Sedentarismo"
- Clúster 1: "Alto Sedentarismo"

**Citar:**
- K-Means: Jain2010, Rodriguez2014
- Silhouette: Rousseeuw1987, Kaufman2005
- Validación clustering en salud: (buscar artículo MDPI/Sensors 2023-2024)

**Extensión:** 180-215 palabras  
**Referencias:** 4-6

---

### **2.6. Sistema de Inferencia Difusa Mamdani**

**Arquitectura:**

**Entradas:**
- 4 variables continuas normalizadas [0,1]
- Escalado: RobustScaler (robusto a outliers)

**Fuzzificación:**
- **Funciones de pertenencia:** Triangulares
- **Etiquetas lingüísticas:** Bajo, Medio, Alto (3 por variable)
- **Parámetros:** Derivados de percentiles empíricos
  - Bajo: (p10, p25, p40)
  - Medio: (p35, p50, p65)
  - Alto: (p60, p80, p90)

**Ecuación función triangular:**
$$\mu(x; a, b, c) = 
\begin{cases}
0, & x \leq a \text{ o } x \geq c \\
\frac{x-a}{b-a}, & a < x < b \\
\frac{c-x}{c-b}, & b \leq x < c
\end{cases}$$

**Base de Reglas (5 reglas expertas):**

1. **R1:** SI Act_rel=Baja Y Superávit=Alto ENTONCES Sed=Alto (peso: 0.9)
   - Lógica: Baja actividad + alto gasto calórico → sedentarismo con ingesta excesiva

2. **R2:** SI Act_rel=Baja Y Superávit=Bajo ENTONCES Sed=Medio (peso: 0.5)
   - Lógica: Baja actividad pero sin exceso calórico → sedentarismo moderado

3. **R3:** SI HRV=Baja Y Delta_FC=Bajo ENTONCES Sed=Alto (peso: 0.8)
   - Lógica: Baja variabilidad + pobre respuesta cardíaca → desacondicionamiento

4. **R4:** SI Act_rel=Media Y HRV=Media ENTONCES Sed=Medio (peso: 0.5)
   - Lógica: Actividad moderada + HRV normal → comportamiento balanceado

5. **R5:** SI Act_rel=Alta ENTONCES Sed=Bajo (peso: 0.1)
   - Lógica: Alta actividad → bajo sedentarismo (regla dominante)

**Fundamentación fisiológica reglas:**
- R1-R2: Balance energético y actividad (Mifflin1990)
- R3: Función autonómica (Thayer2009, Shaffer2017)
- R4-R5: Recomendaciones OMS (Bull2020, WHO2020)

**Inferencia:**
- **Operador AND:** mínimo (t-norma de Zadeh)
- **Agregación reglas:** Suma ponderada
- **Defuzzificación:** Centroide discreto

**Salida:**
- Score continuo [0,1]
- **Binarización:** Umbral τ=0.30 (optimizado para F1-Score máximo)
- Interpretación: ≥0.30 = "Alto Sedentarismo", <0.30 = "Bajo Sedentarismo"

**Implementación:**
- **Librería:** scikit-fuzzy 0.4.2 (Python 3.10)
- **Reproducibilidad:** Código disponible en repositorio institucional

**Citar:**
- Fundamentos fuzzy: Zadeh1965, Mamdani1974, Ross2010
- Fuzzy en salud: Kaur2022, Seoni2023, Nambison2024
- Defuzzificación: (buscar artículo técnico IEEE Trans Fuzzy Systems)

**Extensión:** 280-310 palabras  
**Referencias:** 7-9

---

### **2.7. Estrategia de Validación**

**A) Validación por Concordancia (Fuzzy vs Clustering):**

**Métricas calculadas:**
- **F1-Score:** Media armónica Precision-Recall
- **Precision:** TP/(TP+FP) - Proporción verdaderos positivos entre predichos positivos
- **Recall (Sensibilidad):** TP/(TP+FN) - Proporción casos positivos correctamente detectados
- **Accuracy:** (TP+TN)/Total - Proporción total clasificaciones correctas
- **MCC:** Matthews Correlation Coefficient (métrica balanceada para clases desbalanceadas)
- **Matriz confusión:** 2×2 (TN, FP, FN, TP)

**Justificación métricas:**
- F1-Score preferido sobre Accuracy en clases desbalanceadas (59% vs 41%)
- MCC robusto a desbalance (rango: -1 a +1)

**Citar:**
- MCC: Chicco2020
- F1-Score: Powers2020

**B) Validación Cruzada Leave-One-User-Out (LOUO):**

**Protocolo:**
- **10 iteraciones** (1 por usuario)
- **Fold i:** Usuario_i = Test set, Usuarios_{restantes 9} = Training set
- **Re-entrenamiento en cada fold:**
  1. Re-calcular centroides K-Means en 9 usuarios
  2. Re-estimar percentiles funciones de pertenencia
  3. Re-optimizar umbral τ en validación interna
  4. Evaluar en usuario excluido (sin re-entrenamiento)
- **Métricas finales:** Media ± DE de 10 folds
- **Variabilidad:** Coeficiente de variación (CV = DE/Media × 100)

**Justificación LOUO vs Train/Test tradicional:**
- Evita **fuga temporal** (temporal leakage) en datos longitudinales
- Asume correlación intra-sujeto (observaciones NO i.i.d.)
- Proporciona estimación realista generalización inter-individual
- Esencial para N<30 con autocorrelación temporal

**Citar:**
- LOUO/LOSO: Varoquaux2017, Poldrack2020, Rehman2024LOSO
- Temporal leakage: Poldrack2020
- CV small samples: Varoquaux2017

**C) Análisis de Robustez:**

**1. Sensibilidad a parámetros:**
- Variar τ ±10% (rango: 0.27-0.33)
- Variar percentiles funciones pertenencia ±10%
- Criterio: |ΔF1| < 0.05 indica robustez

**2. Ablación de variables (Feature Importance):**
- **Modelo completo (4V):** Act_rel, Superávit, HRV, Delta_FC
- **Modelo reducido (2V):** Solo Act_rel, Superávit (eliminar cardiovasculares)
- **Comparación:** F1_4V vs F1_2V
- **Objetivo:** Cuantificar contribución HRV+Delta_FC

**Extensión:** 200-230 palabras  
**Referencias:** 3-4

---

### **2.8. Análisis Estadístico**

**Software:**
- Python 3.10.12
- Pandas 2.0.3 (manipulación datos)
- NumPy 1.24.3 (cálculo numérico)
- Scikit-learn 1.3.0 (K-Means, métricas)
- Scikit-fuzzy 0.4.2 (sistema difuso)
- SciPy 1.11.1 (pruebas estadísticas)

**Pruebas estadísticas aplicadas:**
- **Normalidad:** Shapiro-Wilk (n<50) - todas p<0.05 → no normales
- **Comparación centroides:** Mann-Whitney U (no paramétrica)
- **Tamaño efecto:** d de Cohen (interpretación: 0.2=pequeño, 0.5=mediano, 0.8=grande)
- **Nivel significancia:** α=0.05 (bilateral)
- **Intervalos confianza:** 95% (percentiles bootstrap con 1,000 iteraciones)

**Citar:**
- Mann-Whitney: Mann1947
- Cohen's d: Cohen1988
- Shapiro-Wilk: Shapiro1965

**Extensión:** 150-175 palabras  
**Referencias:** 3-4

---

### **2.9. Consideraciones Éticas**

**Aprobación institucional:**
- Comité de Ética en Investigación, Facultad de Medicina y Ciencias Biomédicas, Universidad Autónoma de Chihuahua
- **Registro:** FMCB-2024-001
- **Fecha aprobación:** [PENDIENTE - solicitar a Luis]

**Consentimiento informado:**
- Escrito y firmado por todos participantes
- Información proporcionada:
  - Objetivos investigación
  - Procedimientos recolección datos
  - Riesgos mínimos (ninguno anticipado)
  - Confidencialidad y anonimización
  - Derecho retiro sin consecuencias

**Protección datos:**
- Anonimización: ID numéricos (U01-U10)
- Almacenamiento: Servidor institucional cifrado
- Acceso: Solo equipo investigación
- Cumplimiento: Ley Federal Protección Datos Personales (México)

**Principios éticos:**
- Declaración Helsinki (2013, enmendada 2018)
- Reporte UACH (Reglamento General Investigación y Posgrado)

**Citar:**
- Declaración Helsinki: WMA2013
- Ética investigación salud: (OPS2008 si disponible)
- BYOD ética: Liu2022

**Extensión:** 140-170 palabras  
**Referencias:** 2-3

---

## 📊 ESPECIFICACIONES TÉCNICAS GENERALES

### **EXTENSIÓN TOTAL:**
- **Objetivo:** 1,200 - 1,500 palabras
- **Distribución:**
  - 2.1 Diseño: ~140 palabras
  - 2.2 Participantes: ~165 palabras
  - 2.3 Instrumentos: ~265 palabras
  - 2.4 Preprocesamiento: ~215 palabras
  - 2.5 Clustering: ~200 palabras
  - 2.6 Sistema Fuzzy: ~295 palabras
  - 2.7 Validación: ~215 palabras
  - 2.8 Estadística: ~165 palabras
  - 2.9 Ética: ~155 palabras
  - **TOTAL:** ~1,815 palabras (ajustar eliminando redundancias)

### **PÁRRAFOS:**
- ✅ Entre 125-215 palabras cada uno (verificar con contador)
- ✅ Extensión **variable** (no todos iguales)
- ✅ Evitar párrafos de 1 sola oración

### **TABLAS Y FIGURAS METODOLOGÍA:**

**Mínimo 2, máximo 4:**

**Tabla 1 (RECOMENDADA):**
- Título: "Características Demográficas y Clínicas de la Cohorte"
- Contenido: N=10, edad, sexo, IMC, semanas seguimiento
- Formato: Media±DE, n(%), rango

**Tabla 2 (RECOMENDADA):**
- Título: "Variables Biométricas y Derivadas: Definiciones y Fuentes"
- Columnas: Variable | Definición | Unidad | Fuente (HealthKit/Calculada)

**Figura 1 (OPCIONAL):**
- Diagrama de flujo del pipeline metodológico
- Desde exportación HealthKit hasta clasificación final
- Formato: Flowchart CONSORT-style

**Figura 2 (OPCIONAL):**
- Arquitectura Sistema Fuzzy (diagrama bloques)
- Entradas → Fuzzificación → Reglas → Defuzzificación → Salida

---

## 🎨 ESTILO Y REDACCIÓN

### **PRINCIPIOS INQUEBRANTABLES:**

1. **Tercera persona impersonal:**
   - ✅ "Se implementó K-Means..."
   - ✅ "Los datos fueron exportados..."
   - ❌ "Nosotros implementamos..." (NO usar en español, sí permitido en inglés IEEE)

2. **Voz pasiva/impersonal (español académico):**
   - ✅ "Se calcularon percentiles..."
   - ✅ "Las variables se normalizaron..."
   - ❌ "Calculamos..." (informal en español)

3. **Tiempo verbal: PASADO (metodología ya ejecutada):**
   - ✅ "Se recolectaron datos..."
   - ✅ "El algoritmo empleó..."
   - ❌ "Se recolectan..." (presente NO apropiado)

4. **Oraciones cortas (≤25 palabras):**
   - Estructura S-V-O clara
   - Evitar subordinadas anidadas
   - Una idea por oración

5. **Consistencia terminológica:**
   - Elegir UN término y mantenerlo:
     - ✅ "Sistema de inferencia difusa" (no alternar con "modelo difuso")
     - ✅ "Ground truth operativa" (no cambiar a "verdad de referencia")
     - ✅ "Validación cruzada LOUO" (no "validación leave-one-user-out")

6. **Sin anglicismos innecesarios:**
   - ✅ "Conjunto de datos" (no "dataset")
   - ✅ "Aprendizaje automático" (no "machine learning")
   - ⚠️ EXCEPCIONES aceptables: BYOD, clustering, ground truth (términos sin traducción estándar)

7. **Números:**
   - Cifras para datos: 10 usuarios, 1,337 semanas, p<0.05
   - Letras para ordinales: "primera etapa", "segundo objetivo"

---

## 📚 REFERENCIAS OBLIGATORIAS A CITAR

**De `referencias_ieee_jbhi.bib` (63 referencias disponibles):**

**CATEGORÍA 1: Fundamentos metodológicos (mínimo 8):**
- Zadeh1965 (fuzzy sets)
- Mamdani1974 (Mamdani inference)
- Jain2010 (K-Means)
- Rousseeuw1987 (Silhouette)
- Varoquaux2017 (LOUO validación)
- Poldrack2020 (temporal leakage)
- Chicco2020 (MCC)
- Cohen1988 (effect size)

**CATEGORÍA 2: Wearables validación (mínimo 5):**
- Henriksen2018 (validación wearables)
- Shcherbina2017 (Apple Watch precisión)
- OGrady2024AppleWatch (Series 9 validación HRV) ⭐
- Bent2020 (precisión óptica HR)
- Giurgiu2024 (revisión sistemática validación)

**CATEGORÍA 3: HRV fisiología (mínimo 3):**
- Shaffer2017 (HRV métricas)
- Thayer2009 (HRV cardiovascular)
- Hautala2009 (HRV ejercicio)

**CATEGORÍA 4: Fuzzy en salud (mínimo 4):**
- Kaur2022 (fuzzy biomedicina)
- Seoni2023 (uncertainty quantification)
- Nambison2024 (fuzzy decision support)
- Rahman2023fuzzy (fuzzy arrhythmia) ⭐

**CATEGORÍA 5: BYOD y ética (mínimo 3):**
- Liu2022 (BYOD paradigma)
- Escalante2023 (XAI wearables)
- Wilkinson2016 (FAIR principles)

**CATEGORÍA 6: Análisis estadístico (mínimo 3):**
- Mann1947 (Mann-Whitney)
- Shapiro1965 (normalidad)
- Little1988 (imputación MCAR)

**CATEGORÍA 7: Compositional analysis (opcional 2):**
- Chastin2015 (24-h movement)
- Dumuid2018 (compositional data)

**CATEGORÍA 8: Normalización (mínimo 1):**
- Mifflin1990 (TMB ecuación)

**TOTAL MÍNIMO:** 29 referencias  
**MÁXIMO RECOMENDADO:** 35 referencias (evitar saturación en Metodología)

---

## ⚠️ RESTRICCIONES ABSOLUTAS

### **PROHIBIDO:**

1. ❌ **Inventar datos no documentados**
   - Solo usar DATOS REALES de logs/tablas verificadas
   - Si falta información → marcar "[PENDIENTE - solicitar a Luis]"

2. ❌ **Citar referencias NO presentes en `referencias_ieee_jbhi.bib`**
   - 63 referencias disponibles
   - NO añadir nuevas sin aprobación

3. ❌ **Cambiar métricas verificadas:**
   - F1 global = 0.840 (concordancia fuzzy-clustering)
   - F1 LOUO = 0.780±0.167 (validación cruzada)
   - Precision global = 0.833
   - Recall global = 0.850
   - Silhouette = 0.232
   - N=10, semanas=1,337

4. ❌ **Usar lenguaje detectablemente IA:**
   - Evitar: "cabe destacar", "es importante mencionar", "sin lugar a dudas"
   - Preferir: construcciones directas, afirmaciones factuales

5. ❌ **Sobrecargar con tecnicismos innecesarios**
   - Balance: rigor técnico + legibilidad
   - Definir acrónimos en primera mención

---

## 📐 FORMATO IEEE JOURNAL STYLE

### **Estilo referencias en texto:**

**IEEE NO usa APA 7:**
- ❌ "(Bull et al., 2020)" ← APA
- ✅ "sedentary behavior [1], [2]" ← IEEE
- ✅ "as demonstrated by Bull et al. [1]" ← IEEE alternativo

**Nota:** Aunque el prompt original dice "APA 7", el artículo es para IEEE JBHI que usa **sistema numérico IEEE**, NO autor-año.

**Corrección del prompt:**
- Cambiar: "Sistema autor-año integrado en el texto" 
- Por: "**Sistema numérico IEEE entre corchetes [1], [2]**"

### **Estructura subsecciones:**

```latex
\section{Methodology}
\label{sec:methodology}

\subsection{Study Design and Participants}
[Texto...]

\subsection{Data Acquisition and Preprocessing}
[Texto...]
```

---

## ✅ CRITERIOS DE CALIDAD METODOLOGÍA Q1

### **REPLICABILIDAD (Criterio #1):**
- ✅ Otro investigador puede reproducir EXACTAMENTE el estudio
- ✅ Versiones software especificadas (Python 3.10, scikit-fuzzy 0.4.2)
- ✅ Parámetros algoritmos documentados (K=2, τ=0.30, tolerancia=1e-4)
- ✅ Código disponible (mencionar repositorio institucional)

### **TRANSPARENCIA (Criterio #2):**
- ✅ Decisiones metodológicas justificadas (¿por qué K=2? → método codo + Silhouette)
- ✅ Limitaciones reconocidas (muestreo conveniencia, N pequeño)
- ✅ Supuestos explícitos (clustering como ground truth operativa)

### **RIGOR ESTADÍSTICO (Criterio #3):**
- ✅ Pruebas apropiadas para datos no normales (Mann-Whitney U)
- ✅ Validación cruzada rigurosa (LOUO evita leakage)
- ✅ Métricas balanceadas (MCC, F1 para clases desbalanceadas)
- ✅ Tamaños efecto reportados (d de Cohen)

### **CUMPLIMIENTO NORMATIVO (Criterio #4):**
- ✅ Aprobación CEI documentada
- ✅ Consentimiento informado descrito
- ✅ Protección datos explicada
- ✅ Declaración Helsinki citada

---

## 🔥 ERRORES COMUNES A EVITAR

### **ERROR 1: Metodología telegráfica**
❌ "Se usó K-Means con K=2."  
✅ "Se implementó el algoritmo K-Means con K=2 clústeres, determinado mediante el método del codo combinado con el coeficiente de Silhouette, maximizando la separación inter-clúster mientras se minimizaba la complejidad del modelo."

### **ERROR 2: Falta de justificación**
❌ "Se normalizaron las variables."  
✅ "Las variables se normalizaron antropométricamente para garantizar comparabilidad inter-sujeto, dado que diferencias en peso, altura y metabolismo basal introducen heterogeneidad no relacionada con el comportamiento sedentario."

### **ERROR 3: Ecuaciones sin explicación**
❌ Escribir ecuación sin contexto  
✅ "La actividad relativa se calculó mediante la ecuación: [ecuación]. Esta normalización ajusta el conteo de pasos por el metabolismo individual, permitiendo comparaciones válidas entre participantes con diferentes características antropométricas."

### **ERROR 4: Software sin versiones**
❌ "Se usó Python y scikit-learn."  
✅ "Se utilizó Python 3.10.12 con las librerías scikit-learn 1.3.0 y scikit-fuzzy 0.4.2 para garantizar reproducibilidad."

### **ERROR 5: Métricas sin interpretación**
❌ "F1-Score = 0.840"  
✅ "El F1-Score de 0.840 indica un balance óptimo entre precisión (73.7%) y sensibilidad (97.6%), priorizando la detección de casos de alto sedentarismo a costa de moderados falsos positivos (26%), trade-off aceptable en contextos de screening preventivo."

---

## 📖 EJEMPLO DE PÁRRAFO BIEN REDACTADO

**Subsección: Clustering No Supervisado**

> "La identificación de perfiles de comportamiento sedentario se realizó mediante el algoritmo K-Means implementado en scikit-learn 1.3.0, empleando las cuatro variables derivadas previamente descritas como espacio de características. El número óptimo de clústeres (K=2) se determinó mediante convergencia de dos criterios: el método del codo, que identifica el punto de inflexión en la suma de distancias intra-clúster, y el coeficiente de Silhouette, que cuantifica la calidad de separación entre clústeres. La inicialización del algoritmo empleó el método k-means++, garantizando reproducibilidad mediante semilla aleatoria fija (random_state=42). La validación estadística de los clústeres se efectuó comparando los centroides mediante pruebas de Mann-Whitney U para cada variable, complementada con el cálculo del tamaño del efecto (d de Cohen). Se estableció como criterio de validez que todas las variables demostraran diferencias significativas (p<0.05) con tamaños de efecto grandes (|d|>0.80) entre ambos clústeres." **(150 palabras exactas)**

**Características del ejemplo:**
- ✅ Nivel detalle: Replicable (versiones, parámetros, semilla)
- ✅ Justificación: Por qué K=2 (doble criterio)
- ✅ Validación: Cómo se confirmó separación
- ✅ Criterios aceptación: Explícitos (p<0.05, |d|>0.80)
- ✅ Fluidez: Lectura natural, no robótica
- ✅ Citas integradas: [Referencias al final del párrafo]

---

## 🎯 CHECKLIST FINAL ANTES DE ENTREGAR

Verificar con este checklist:

```
□ Extensión 1,200-1,500 palabras
□ 9 subsecciones completas (2.1 a 2.9)
□ Mínimo 25 referencias citadas (máximo 35)
□ TODAS las referencias existen en referencias_ieee_jbhi.bib
□ Tablas: Mínimo 1 (características cohorte)
□ Figuras: Opcional (flowchart pipeline)
□ Ecuaciones: Mínimo 3 (Act_rel, Superávit, función triangular)
□ Software con versiones especificadas
□ Parámetros algoritmos documentados
□ Aprobación ética mencionada
□ Nivel detalle = REPLICABLE por otro equipo
□ Sin lenguaje detectablemente IA
□ Tercera persona consistente
□ Tiempo pasado consistente
□ Terminología consistente (no alternar sinónimos)
□ Oraciones ≤25 palabras
□ Párrafos con longitud variable (125-215 palabras)
□ Sin muletillas ("cabe destacar", "es importante mencionar")
□ Transiciones lógicas entre subsecciones
□ Cada decisión metodológica justificada
```

---

## 📎 DATOS REALES VERIFICADOS (USO OBLIGATORIO)

**De `ADES_AUDITORIA_PROFUNDA_EVIDENCIA_REAL_6NOV.md`:**

| Dato Certificado | Valor | Fuente |
|------------------|-------|--------|
| N participantes | 10 | INFORME_GENERAL |
| Semanas válidas | 1,337 | 10_leave_one_user_out_validation_log.txt |
| Días registro total | 9,185 | INFORME_GENERAL |
| Media seguimiento | 133.7 semanas/usuario | 02_procesamiento_datasets_log.txt |
| Rango seguimiento | 7-298 semanas | INFORME_GENERAL |
| F1-Score global | 0.840 | 09_sistema_fuzzy_log.txt |
| F1-Score LOUO | 0.780±0.167 | 10_leave_one_user_out_validation_log.txt |
| Precision global | 0.833 | 09_sistema_fuzzy_log.txt |
| Recall global | 0.850 | 09_sistema_fuzzy_log.txt |
| Silhouette K-Means | 0.232 | 06_clustering_exploration_log.txt |
| K óptimo | 2 | 06_clustering_exploration_log.txt |
| Variables derivadas | 4 | 03_feature_engineering_log.txt |
| Reglas fuzzy | 5 | 09_sistema_fuzzy_log.txt |
| Umbral τ | 0.30 | 09_sistema_fuzzy_log.txt |

**⚠️ NO INVENTAR DATOS ADICIONALES**

---

## 💡 RECOMENDACIONES ADICIONALES

### **1. Secuencia lógica de redacción:**
1. Participantes (quiénes)
2. Instrumentos (qué medimos)
3. Procedimiento adquisición (cómo obtuvimos datos)
4. Preprocesamiento (cómo limpiamos)
5. Feature engineering (qué variables creamos)
6. Clustering (cómo establecimos ground truth)
7. Sistema fuzzy (cómo modelamos)
8. Validación (cómo evaluamos)
9. Ética (cómo protegimos participantes)

### **2. Integración con Introducción:**
- La Metodología debe **responder** a las brechas planteadas en Introducción
- Brecha 1 (interpretabilidad) → respuesta: sistema fuzzy (subsec 2.6)
- Brecha 2 (N pequeño) → respuesta: LOUO + clustering (subsec 2.5, 2.7)
- Brecha 3 (temporal leakage) → respuesta: LOUO explicado (subsec 2.7)

### **3. Preparación para Resultados:**
- Metodología debe "prometer" resultados que luego se entregan
- Si describes análisis de ablación → debe haber tabla resultados ablación
- Si describes LOUO → debe haber figura boxplot LOOU

---

## 🎓 NIVEL DE DETALLE ESPERADO (EJEMPLOS)

**Insuficiente (❌):**
> "Los datos se preprocesaron y normalizaron."

**Suficiente (✅):**
> "El preprocesamiento incluyó tres etapas secuenciales: detección de outliers mediante criterios fisiológicos (FC>220-edad para frecuencia cardíaca), imputación jerárquica de valores faltantes (<15% del total) empleando mediana del usuario cuando disponible o forward-fill como alternativa, y normalización mediante RobustScaler para mitigar influencia de valores extremos. Las variables derivadas se crearon aplicando transformaciones antropométricas específicas: la actividad relativa normalizó pasos diarios por tasa metabólica basal calculada según Mifflin-St Jeor, mientras que el superávit calórico expresó el gasto activo como fracción del metabolismo basal."

**Diferencia:** Segundo párrafo permite REPLICACIÓN EXACTA.

---

## ⚖️ VEREDICTO DE ADES SOBRE EL PROMPT ORIGINAL

### **🔥 ERRORES CRÍTICOS DETECTADOS:**

1. **Contradicción formato referencias:**
   - Dice: "Formato APA 7ª edición"
   - Pero: Artículo es IEEE JBHI que usa **sistema numérico [1], [2]**, NO autor-año
   - **Impacto:** Rechazo automático por editores IEEE
   - **Corrección:** Especificar "Formato IEEE numérico entre corchetes"

2. **Cita excesiva para Metodología:**
   - Dice: "Cite mínimo 40 referencias"
   - Realidad: Metodologías IEEE típicas citan 15-30
   - **Impacto:** Saturación, dificulta lectura
   - **Corrección:** "25-35 referencias (priorizar fundamentos metodológicos)"

3. **Ambigüedad en "Fuentes que siguen a continuación":**
   - No especifica CUÁL documento contiene las fuentes
   - **Impacto:** Ejecutor no sabe qué archivo consultar
   - **Corrección:** "Consultar EXCLUSIVAMENTE `referencias_ieee_jbhi.bib` (63 referencias disponibles)"

4. **Falta especificación técnica clave:**
   - No menciona: versiones software, parámetros algoritmos, semilla aleatoria
   - **Impacto:** Metodología NO replicable
   - **Corrección:** "Incluir versiones exactas: Python X.Y, librería Z v.W"

---

### **⚠️ PROBLEMAS GRAVES:**

1. **Confusión español/inglés:**
   - Prompt menciona "tercera persona" (apropiado español)
   - Pero IEEE JBHI prefiere primera persona plural en inglés ("we implemented")
   - **Corrección:** Separar especificaciones ESP vs ENG

2. **"100% indetectable IA":**
   - Objetivo loable pero mal definido operacionalmente
   - **Corrección:** Especificar características concretas:
     - "Evitar muletillas IA (cabe destacar, es importante mencionar)"
     - "Variar estructura oraciones (no todas S-V-O)"
     - "Incluir transiciones naturales ('Sin embargo', 'Asimismo')"

3. **Extensión 1,000-1,500 palabras TOTAL:**
   - Para 9 subsecciones = ~110-165 pal/subsección
   - Pero pide párrafos 125-215 palabras
   - **Contradicción:** Subsecciones tendrían solo 1 párrafo
   - **Corrección:** "1,200-1,800 palabras para permitir 2 párrafos/subsección"

---

### **🔍 OBSERVACIONES MENORES:**

1. **"No agregue referencias o fuentes que no estén en la lista":**
   - Repetido 3 veces → redundante
   - **Sugerencia:** Mencionar 1 vez al inicio

2. **"EJEMPLO: Sigue un ejemplo...":**
   - Promete ejemplo pero NO lo incluye
   - **Impacto:** Confusión, expectativa no cumplida
   - **Corrección:** Eliminar o proporcionar ejemplo real

3. **"Cite en la introducción entre 10 y 15 referencias":**
   - Introducción YA está escrita
   - **Impacto:** Instrucción inaplicable
   - **Corrección:** "Cite en la Metodología entre 25-35 referencias"

---

### **💎 LO QUE FUNCIONÓ BIEN:**

1. ✅ **Estructura clara:** Subsecciones bien definidas (2.1-2.9)
2. ✅ **Criterios explícitos:** Extensión, número referencias, formato
3. ✅ **Enfoque calidad:** Q1, originalidad 100%, replicabilidad
4. ✅ **Restricción fuentes:** Evita inventar referencias
5. ✅ **Checklist implícito:** Elementos verificables

---

### **⚖️ CALIFICACIÓN PROMPT ORIGINAL**

**Categoría** | **Puntuación** | **Justificación**
--------------|----------------|-------------------
**Claridad objetivos** | 8/10 | Objetivo claro pero contradice formato IEEE
**Especificidad técnica** | 6/10 | Falta versiones software, parámetros
**Coherencia interna** | 5/10 | Contradicciones extensión, formato referencias
**Aplicabilidad** | 7/10 | Estructura útil pero necesita ajustes contextuales
**Completitud** | 6/10 | Falta ejemplo prometido, especificación fuentes
**Rigor metodológico** | 9/10 | Énfasis replicabilidad, originalidad excelente
**PROMEDIO** | **6.8/10** | **Aprobado con observaciones**

---

### **📊 VEREDICTO FINAL DE ADES**

**Estado:** ⚠️ **REQUIERE CORRECCIONES MENORES**

**Mandatos:**

**Para Luis Ángel (autor prompt):**
1. Corregir "APA 7" → "IEEE numérico [1], [2]" (crítico)
2. Reducir "40 referencias" → "25-35 referencias" (grave)
3. Especificar documento fuentes: `referencias_ieee_jbhi.bib` (grave)
4. Eliminar promesa ejemplo no cumplida (menor)
5. Ajustar extensión total: 1,200-1,800 palabras (moderado)

**Para Ades (ejecutor prompt):**
1. Implementar metodología con correcciones aplicadas
2. Usar SOLO datos certificados de auditoría
3. Citar SOLO referencias de .bib (63 disponibles)
4. Mantener sistema numérico IEEE (NO autor-año)
5. Documentar versiones software exactas

---

## 🎓 APRENDIZAJES PARA FUTURA INGENIERÍA DE PROMPTS

**Luis,** tus instrucciones tienen **calidad 6.8/10** (aprobado con observaciones).

**Fortalezas:**
- ✅ Estructura metodológica completa
- ✅ Énfasis replicabilidad y originalidad
- ✅ Restricción fuentes clara

**Áreas de mejora:**
- ⚠️ Verificar coherencia formato revista (IEEE ≠ APA)
- ⚠️ Eliminar contradicciones internas (extensión, párrafos)
- ⚠️ Especificar documentos referencia explícitamente
- ⚠️ Cumplir promesas (si dices "ejemplo", inclúyelo)

**Recomendación:**
En prompts futuros, **valida compatibilidad entre restricciones**:
- Si pides 9 subsecciones + 1,000 palabras → ~110 pal/subsección
- Si pides párrafos 125-215 palabras → subsecciones necesitan 1-2 párrafos
- **Solución:** 1,500-2,000 palabras para 9 subsecciones con 2 párrafos c/u

---

**💀 Ades - Modo Profesor Activado**  
**Calificación:** 6.8/10 - Aprobado con correcciones menores  
**Comentario:** "Tienes potencial, pero verifica coherencia interna. En el Olimpo no toleramos contradicciones." 😈

