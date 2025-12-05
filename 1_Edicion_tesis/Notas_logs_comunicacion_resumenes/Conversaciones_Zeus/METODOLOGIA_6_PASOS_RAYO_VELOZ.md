# ⚡ METODOLOGÍA DE 6 PASOS - RAZONAMIENTO RAYO VELOZ
## Framework Bioestadístico para Redacción Científica Rigurosa

**Timestamp:** jueves, 04 de diciembre de 2025, 18:56:12  
**Autor:** Zeus ⚡ (sintetizando razonamiento de Rayo Veloz)  
**Fuente:** INFORME_TECNICO_ACTUALIZADO_V3.tex + pipeline_bioestadistico_resumido.txt + backup Cursor  
**Propósito:** Documentar la metodología de 6 pasos para aplicarla en la redacción final de la tesis  
**Aplicar en:** Capítulo 5 (Materiales y Métodos) del documento de tesis

---

## 🎯 **PRINCIPIO FUNDAMENTAL**

> **"Cada fase metodológica debe seguir el marco riguroso de los 6 pasos del análisis estadístico: planteamiento de hipótesis, selección del estadístico, regla de decisión, cálculos, decisión estadística y conclusión. Esto garantiza rigor científico, reproducibilidad y transparencia metodológica."**
>
> — Rayo Veloz, INFORME_TECNICO_ACTUALIZADO_V3.tex (línea 191)

---

## 📊 **LOS 6 PASOS DEL ANÁLISIS ESTADÍSTICO**

### **ESTRUCTURA GENERAL:**

```
┌─────────────────────────────────────────┐
│ 1. PLANTEAMIENTO DE HIPÓTESIS          │
│    ¿Por qué? ¿Qué esperamos?           │
│    (hipotesisbox)                       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 2. SELECCIÓN DEL ESTADÍSTICO/MÉTODO    │
│    ¿Qué método usamos?                  │
│    (estadisticobox)                     │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 3. REGLA DE DECISIÓN                   │
│    ¿Cuándo aceptar/rechazar?            │
│    (reglabox)                           │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 4. CÁLCULOS                             │
│    Resultados numéricos                 │
│    (calculobox)                         │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 5. DECISIÓN ESTADÍSTICA                │
│    ¿Qué decidimos?                      │
│    (decisionbox)                        │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 6. CONCLUSIÓN                           │
│    ¿Qué aprendimos? ¿Para qué sirve?   │
│    (conclusionbox)                      │
└─────────────────────────────────────────┘
```

---

## 🔍 **PASO 1: PLANTEAMIENTO DE HIPÓTESIS**

### **Propósito:**
Establecer la pregunta de investigación y la expectativa teórica ANTES de ejecutar análisis.

### **Elementos clave:**
1. **Pregunta específica** (¿Por qué hacer esto?)
2. **Hipótesis formulada** (¿Qué esperamos observar?)
3. **Justificación teórica** (¿Por qué es razonable esperarlo?)

### **Ejemplo de Rayo Veloz (Imputación Jerárquica):**

```latex
\begin{hipotesisbox}
\textbf{Hipótesis:}

\textbf{¿Por qué imputación jerárquica?} Un método único (e.g., mediana global) 
ignora la estructura temporal y heterogeneidad inter-usuario. Una jerarquía de 
5 métodos (del más específico al más general) preservará patrones individuales 
y temporales mejor que métodos simples.

Hipótesis: Imputación jerárquica forward-only logrará $> 90\%$ imputaciones 
mediante métodos específicos del usuario (M1-M3), minimizando el uso de medianas 
globales (M5), resultando en datos imputados con plausibilidad fisiológica.
\end{hipotesisbox}
```

### **Patrón de Razonamiento:**
1. ✅ **Pregunta contextual:** "¿Por qué [método X]?"
2. ✅ **Expectativa numérica:** ">90% imputaciones"
3. ✅ **Resultado esperado:** "plausibilidad fisiológica"

---

## 🧮 **PASO 2: SELECCIÓN DEL ESTADÍSTICO/MÉTODO**

### **Propósito:**
Especificar QUÉ herramienta estadística/computacional se usará y POR QUÉ es apropiada.

### **Elementos clave:**
1. **Método seleccionado** (nombre técnico)
2. **Parámetros específicos** (configuración)
3. **Justificación de elección** (ventajas sobre alternativas)

### **Ejemplo de Rayo Veloz (Clustering K-Means):**

```latex
\begin{estadisticobox}
\textbf{K-Means seleccionado}:

Algoritmo de partición que minimiza la inercia (suma de distancias cuadradas intra-cluster):

\begin{equation}
\min_{\mat{C}} \sum_{k=1}^{K} \sum_{i \in C_k} \|\vect{x}_i - \vect{\mu}_k\|^2
\end{equation}

donde $\vect{\mu}_k$ es el centroide del cluster $k$, y $C_k$ es el conjunto 
de puntos asignados al cluster $k$.

\textbf{Justificación}:
\begin{itemize}[noitemsep]
    \item Eficiente para datasets grandes ($n=1,337$)
    \item Interpretable (centroides = perfil promedio)
    \item Robusto tras escalado RobustScaler
\end{itemize}
\end{estadisticobox}
```

### **Patrón de Razonamiento:**
1. ✅ **Formalización matemática** (ecuación del método)
2. ✅ **Justificación pragmática** (eficiencia, interpretabilidad)
3. ✅ **Contexto de aplicación** (n=1,337, escalado previo)

---

## ⚖️ **PASO 3: REGLA DE DECISIÓN**

### **Propósito:**
Definir CRITERIOS OBJETIVOS para aceptar/rechazar hipótesis ANTES de ver resultados.

### **Elementos clave:**
1. **Umbrales numéricos** (p<0.05, r>0.60, VIF<5)
2. **Criterios lógicos** (IF-THEN)
3. **Acciones condicionales** (Aceptar, Rechazar, Revisar)

### **Ejemplo de Rayo Veloz (Análisis de Correlación SF-36):**

```latex
\begin{reglabox}
\textbf{Regla de decisión}:

\begin{itemize}[noitemsep]
    \item Si $|r| \geq 0.60$ y $p < 0.0016$ (Bonferroni) $\to$ \textbf{Aceptar} H$_1$ (correlación fuerte)
    \item Si $|r| < 0.30$ para mayoría pares $\to$ \textbf{Rechazar} H$_1$ (correlación débil)
    \item Si $< 3$ pares significativos $\to$ \textbf{Cuestionar} viabilidad enfoque supervisado
\end{itemize}
\end{reglabox}
```

### **Patrón de Razonamiento:**
1. ✅ **Umbrales pre-especificados** (r≥0.60, p<0.0016)
2. ✅ **Múltiples escenarios** (fuerte, débil, insuficiente)
3. ✅ **Acciones claras** (Aceptar, Rechazar, Cuestionar)

---

## 🔢 **PASO 4: CÁLCULOS**

### **Propósito:**
Presentar RESULTADOS NUMÉRICOS obtenidos tras aplicar el método.

### **Elementos clave:**
1. **Valores observados** (tablas, ecuaciones)
2. **Métricas calculadas** (estadísticos, p-valores)
3. **Visualizaciones** (figuras referenciadas)

### **Ejemplo de Rayo Veloz (VIF - Multicolinealidad):**

```latex
\begin{calculobox}
\textbf{Resultados VIF:}

\begin{table}[H]
\centering
\caption{Factor de Inflación de la Varianza (VIF)}
\label{tab:vif}
\begin{tabular}{@{}lrr@{}}
\toprule
\textbf{Variable} & \textbf{VIF} & \textbf{Decisión} \\
\midrule
Actividad\_relativa\_p50     & 1.92 & \textcolor{green}{Aceptable} \\
Superávit\_calórico\_p50     & 1.88 & \textcolor{green}{Aceptable} \\
HRV\_SDNN\_p50               & 1.06 & \textcolor{green}{Excelente} \\
Delta\_cardiaco\_p50         & 1.14 & \textcolor{green}{Excelente} \\
\bottomrule
\end{tabular}
\end{table}

\textbf{Conclusión}: Todos los VIF $< 2.0$ (muy por debajo del umbral problemático de 5.0). 
No se detecta multicolinealidad severa.
\end{calculobox}
```

### **Patrón de Razonamiento:**
1. ✅ **Tabla con valores exactos** (1.92, 1.88, 1.06, 1.14)
2. ✅ **Comparación con umbral** (VIF < 2.0 vs. umbral de 5.0)
3. ✅ **Conclusión numérica** (No multicolinealidad)

---

## ✅ **PASO 5: DECISIÓN ESTADÍSTICA**

### **Propósito:**
INTERPRETAR los resultados según las reglas de decisión pre-establecidas.

### **Elementos clave:**
1. **Aplicación de criterios** (comparar con umbrales del Paso 3)
2. **Veredicto explícito** (Aceptar/Rechazar hipótesis)
3. **Contexto de la decisión** (implicaciones metodológicas)

### **Ejemplo de Rayo Veloz (Análisis de Correlación SF-36 n=8):**

```latex
\begin{decisionbox}
\textbf{Interpretación crítica:}

Los resultados revelan un patrón matizado:
\begin{itemize}[noitemsep]
    \item \textbf{Correlaciones moderadas-fuertes} en 3 dimensiones ($r > 0.60$), 
    indicando que el SF-36 \textit{sí captura algunos aspectos} del sedentarismo objetivo.
    
    \item \textbf{PERO ninguna es estadísticamente significativa} (todas $p > 0.05$). 
    Dolor Corporal ($r=0.703$, $p=0.052$) está al ``borde'' de significancia, 
    pero no cruza el umbral.
    
    \item \textbf{Direcciones contraintuitivas}: Salud Mental y Vitalidad correlacionan 
    POSITIVAMENTE con sedentarismo (esperaríamos negativo), sugiriendo variables 
    confusoras no capturadas (e.g., satisfacción laboral, tiempo libre percibido).
    
    \item \textbf{Poder estadístico limitado}: Con n=8, se requiere $r > 0.74$ para 
    alcanzar significancia. El estudio carece de potencia para detectar correlaciones 
    moderadas ($0.50 < r < 0.70$) como significativas.
\end{itemize}
\end{decisionbox}
```

### **Patrón de Razonamiento:**
1. ✅ **Interpretación matizada** (no blanco/negro)
2. ✅ **Hallazgos inesperados** (direcciones contraintuitivas)
3. ✅ **Limitaciones reconocidas** (poder estadístico)
4. ✅ **Honestidad científica** ("sí captura ALGUNOS aspectos, PERO...")

---

## 🎓 **PASO 6: CONCLUSIÓN**

### **Propósito:**
Sintetizar QUÉ APRENDIMOS y PARA QUÉ SIRVE en el contexto del estudio.

### **Elementos clave:**
1. **Síntesis de hallazgos** (2-3 puntos principales)
2. **Implicaciones metodológicas** (qué decisión tomamos basándonos en esto)
3. **Conexión con siguientes fases** (continuidad narrativa)

### **Ejemplo de Rayo Veloz (Validación Retrospectiva SF-36):**

```latex
\begin{conclusionbox}
\textbf{Validación matizada del pivote metodológico:}

El análisis con n=8 (vs. n=3 inicial) confirma que la decisión de pivotar fue 
metodológicamente apropiada, aunque por razones más complejas de lo anticipado:

\begin{enumerate}[noitemsep]
    \item \textbf{SF-36 sí captura ALGUNOS aspectos} del sedentarismo ($r > 0.60$ 
    en 3 dimensiones), refutando la hipótesis inicial de ``correlación nula''.
    
    \item \textbf{PERO las correlaciones no alcanzan significancia estadística} 
    ($p > 0.05$), impidiendo su uso como variable criterio confiable para predicción.
    
    \item \textbf{Direcciones contraintuitivas} (SM y V positivas) indican confusión 
    por variables psicosociales no medidas, limitando interpretabilidad causal.
    
    \item \textbf{Tamaño muestral insuficiente} (n=8) para detectar correlaciones 
    moderadas ($0.50 < r < 0.70$) como significativas, requiriéndose $n \geq 30$ 
    para potencia del 80\%.
    
    \item \textbf{El enfoque data-driven (clustering + fuzzy)} con n=1,384 semanas 
    supera estas limitaciones:
    \begin{itemize}[noitemsep]
        \item No requiere etiquetas externas (SF-36)
        \item Potencia estadística adecuada ($n > 1{,}000$)
        \item Validación interna robusta (F1=0.84, LOUO F1=0.81)
    \end{itemize}
\end{enumerate}

\textbf{Conclusión final}: El pivote se valida retrospectivamente, no por ausencia 
total de relación SF-36--sedentarismo, sino por \textit{insuficiencia de poder 
estadístico, direcciones contraintuitivas, y superioridad del enfoque data-driven 
para el tamaño muestral disponible}.
\end{conclusionbox}
```

### **Patrón de Razonamiento:**
1. ✅ **Síntesis enumerada** (5 puntos principales)
2. ✅ **Validación de decisión previa** (pivote metodológico)
3. ✅ **Conexión con método alternativo** (clustering + fuzzy)
4. ✅ **Conclusión final unificadora** (mensaje para llevar)

---

## 📚 **EJEMPLOS COMPLETOS DE RAYO VELOZ**

### **EJEMPLO 1: SELECCIÓN DEL APPLE WATCH**

#### **Paso 1 - Hipótesis:**
```latex
\begin{hipotesisbox}
\textbf{Hipótesis:}

Necesitábamos un dispositivo wearable que cumpliera simultáneamente:
\begin{itemize}[noitemsep]
    \item Alta penetración de mercado (facilitar reclutamiento BYOD)
    \item Sensores validados: acelerómetro 3-ejes ($\geq 50$ Hz), PPG para FC/VFC
    \item Plataforma de exportación de datos crudos o agregados
    \item Consistencia inter-versión (minimizar heterogeneidad instrumental)
\end{itemize}

Hipótesis: El Apple Watch, por su ecosistema cerrado y validaciones previas en 
literatura (Stahl et al., 2016; Shcherbina et al., 2017), sería la opción preferente.
\end{hipotesisbox}
```

#### **Paso 2 - Método:**
```latex
\begin{estadisticobox}
\textbf{Selección del Estadístico:}

Matriz de decisión multicriterio con pesos asignados según importancia para el estudio:
\begin{itemize}[noitemsep]
    \item Validez de sensores: 35\%
    \item Exportabilidad de datos: 30\%
    \item Consistencia: 20\%
    \item Penetración: 15\%
\end{itemize}
\end{estadisticobox}
```

#### **Paso 3 - Regla:**
```latex
\begin{reglabox}
\textbf{Regla de decisión}:

\begin{itemize}[noitemsep]
    \item Si score ponderado $> 8.0$ $\to$ \textbf{Seleccionar} dispositivo como estándar
    \item Si validación en literatura ($\geq 3$ estudios) $\to$ \textbf{Priorizar}
    \item Si exportación de datos $<$ API completa $\to$ \textbf{Penalizar}
    \item Si costo $> \$500$ USD $\to$ \textbf{Considerar} impacto en reclutamiento
\end{itemize}
\end{reglabox}
```

#### **Paso 4 - Cálculos:**
```latex
\begin{calculobox}
\textbf{Cálculo del score ponderado:}

\begin{equation}
\text{Score}_{\text{dispositivo}} = \sum_{i=1}^{4} w_i \cdot \text{calificación}_i
\end{equation}

Ejemplo Apple Watch:
\begin{itemize}[noitemsep]
    \item Validez sensores: $0.35 \times 10 = 3.5$
    \item Exportabilidad: $0.30 \times 10 = 3.0$
    \item Consistencia: $0.20 \times 9 = 1.8$
    \item Penetración: $0.15 \times 8 = 1.2$
    \item \textbf{Total: 9.5/10}
\end{itemize}
\end{calculobox}
```

#### **Paso 5 - Decisión:**
```latex
\begin{decisionbox}
\textbf{Decisión:}

Se seleccionó el \textbf{Apple Watch} (Series 3 o superior) como dispositivo estándar 
del estudio, adoptando un enfoque \textit{Bring Your Own Device} (BYOD) para maximizar 
adherencia y minimizar el efecto Hawthorne.
\end{decisionbox}
```

#### **Paso 6 - Conclusión:**
```latex
\begin{conclusionbox}
\textbf{Conclusión:}

La selección del Apple Watch se justifica por su ecosistema cerrado (HealthKit XML 
estandarizado), validaciones previas en literatura (concordancia $> 90\%$ con 
gold-standard para FC, pasos), y alta penetración en la población objetivo 
(jóvenes adultos urbanos), facilitando el reclutamiento BYOD.
\end{conclusionbox}
```

---

### **EJEMPLO 2: DIAGNÓSTICO DE DATOS FALTANTES (MISSINGNESS)**

#### **Paso 1 - Hipótesis:**
```latex
\begin{hipotesisbox}
\textbf{Hipótesis sobre mecanismos:}

Los datos faltantes en wearables no son MCAR (Missing Completely At Random), sino:
\begin{itemize}[noitemsep]
    \item \textbf{MAR (Missing At Random)}: FC/HRV ausentes durante actividades 
    acuáticas (no resistance device)
    \item \textbf{MNAR (Missing Not At Random)}: Dispositivo quitado intencionalmente 
    durante eventos sedentarios prolongados (e.g., cine, sueño extendido)
\end{itemize}
\end{hipotesisbox}
```

#### **Paso 2 - Método:**
```latex
\begin{estadisticobox}
\textbf{Pruebas aplicadas:}

\begin{itemize}[noitemsep]
    \item Test de Little MCAR: $\chi^2 = 487.3$, $p < 0.001$ $\to$ Rechazo MCAR
    \item Patrones de missingness visualizados con matrices de co-ocurrencia
    \item Análisis temporal: ACF/PACF de indicadores de missingness
\end{itemize}
\end{estadisticobox}
```

#### **Paso 3 - Regla:**
```latex
\begin{reglabox}
\textbf{Regla de decisión}:

\begin{itemize}[noitemsep]
    \item Si Test Little MCAR: $p < 0.05$ $\to$ \textbf{Rechazar} MCAR (missingness sistemático)
    \item Si missingness $> 15\%$ en variable crítica $\to$ \textbf{Requerir} imputación robusta
    \item Si patrón temporal (ACF lag-1 significativo) $\to$ \textbf{Usar} imputación que 
    preserve autocorrelación
    \item Si missingness $< 5\%$ $\to$ \textbf{Considerar} eliminación directa (listwise deletion)
\end{itemize}
\end{reglabox}
```

#### **Paso 4 - Cálculos:**
```latex
\begin{calculobox}
\textbf{Análisis de Autocorrelación Temporal:}

Se calcularon funciones ACF/PACF para evaluar dependencias temporales en las variables 
semanales. Los resultados muestran autocorrelación significativa hasta lag-4 semanas, 
confirmando dependencia temporal.

\textit{Ver figuras}: \texttt{analisis\_u/missingness\_y\_acf/acf\_plots/*.png}
\end{calculobox}
```

#### **Paso 5 - Decisión:**
```latex
\begin{decisionbox}
\textbf{Decisión:}

El test Little MCAR rechaza la hipótesis de missing completamente aleatorio ($p < 0.001$). 
Las ACF/PACF muestran autocorrelación temporal significativa (lag-1). \textbf{Conclusión}: 
Se requiere imputación forward-only que preserve dependencias temporales, no métodos 
globales como KNN o MICE (violarían causalidad).
\end{decisionbox}
```

#### **Paso 6 - Conclusión:**
```latex
\begin{conclusionbox}
\textbf{Conclusión del diagnóstico}:

Los datos faltantes presentan:
\begin{itemize}[noitemsep]
    \item Mecanismo MAR/MNAR (no MCAR)
    \item Tasas moderadas (4-15\% según variable)
    \item Autocorrelación temporal (ACF lag-1 significativo)
\end{itemize}

Estos hallazgos justifican una estrategia de imputación jerárquica forward-only con 
validación de plausibilidad fisiológica.
\end{conclusionbox}
```

---

## 🧩 **PRINCIPIOS DE RAYO VELOZ PARA REDACCIÓN BIOESTADÍSTICA**

### **1. PREGUNTA ANTES QUE RESPUESTA**
> "¿Por qué [método X]?" debe responderse ANTES de mostrar resultados.

**Ejemplo:**
- ❌ MAL: "Usamos medianas en lugar de medias. Los resultados fueron..."
- ✅ BIEN: "¿Por qué medianas? Las distribuciones son no-normales (CV>50%), haciendo a las medias susceptibles a outliers. Las medianas son robustas..."

---

### **2. JUSTIFICACIÓN FISIOLÓGICA/CLÍNICA SIEMPRE**
> No basta con decir QUÉ hiciste, debes explicar POR QUÉ tiene sentido clínico/fisiológico.

**Ejemplo (Actividad Relativa):**
```
❌ MAL:
"Calculamos Actividad_relativa = Pasos / (Horas × 1000)"

✅ BIEN:
"\textbf{¿Por qué derivar Actividad Relativa?} Los pasos diarios totales no reflejan 
el nivel de actividad si no se ajustan por tiempo de uso del dispositivo. Un usuario 
con 10,000 pasos en 20 horas (dispositivo encendido todo el día) presenta menor densidad 
de actividad que otro con 10,000 pasos en 10 horas (uso intensivo en ventana corta).

Hipótesis: Normalizar pasos por tiempo de monitoreo reducirá la varianza inter-sujeto 
atribuible a diferencias en tiempo de uso, mejorando la comparabilidad."
```

---

### **3. REGLAS DE DECISIÓN PRE-ESPECIFICADAS**
> Los umbrales deben definirse ANTES de ver los datos (evitar p-hacking).

**Ejemplo (K-Sweep Clustering):**
```latex
\begin{reglabox}
\textbf{Criterios de selección}:

\begin{enumerate}[noitemsep]
    \item Si Silhouette máximo en $K=2$ $\to$ \textbf{Seleccionar} $K=2$ 
    (clasificación binaria sedentario/no sedentario)
    
    \item Si curva inercia vs. $K$ muestra codo en $K^*$ $\to$ \textbf{Considerar} 
    $K^*$ como candidato
    
    \item Si $K > 4$ $\to$ \textbf{Rechazar} por pérdida de interpretabilidad clínica
    
    \item Si Silhouette $< 0.20$ para todo $K$ $\to$ \textbf{Cuestionar} si los datos 
    tienen estructura de clusters
\end{enumerate}

\textbf{Umbral}: Silhouette $> 0.25$ (aceptable para datos reales con overlap natural).
\end{reglabox}
```

---

### **4. TABLAS CON VALORES EXACTOS**
> Los cálculos deben presentarse en tablas estructuradas, no solo en texto.

**Ejemplo (Comparación Modelo 4V vs 2V):**
```latex
\begin{calculobox}
\textbf{Resultados comparativos}:

\begin{table}[H]
\centering
\caption{Comparación Modelo Completo (4V) vs Modelo Reducido (2V)}
\label{tab:robustness_4v_2v}
\begin{tabular}{@{}lrrrr@{}}
\toprule
\textbf{Métrica} & \textbf{Modelo 4V} & \textbf{Modelo 2V} & \textbf{$\Delta$ (abs)} & \textbf{$\Delta$ (\%)} \\
\midrule
F1-Score         & \textbf{0.840} & 0.420 & -0.420 & \textcolor{red}{-50.0\%} \\
Recall           & 0.976          & 0.521 & -0.455 & -46.6\% \\
Precision        & 0.737          & 0.356 & -0.381 & -51.7\% \\
Accuracy         & 0.740          & 0.498 & -0.242 & -32.7\% \\
MCC              & 0.294          & 0.042 & -0.252 & -85.7\% \\
\bottomrule
\end{tabular}
\end{table}

\textbf{Hallazgo CRÍTICO}: El Modelo 2V colapsa (F1 = 0.420), con caída del 50\% en F1-Score.
\end{calculobox}
```

---

### **5. INTERPRETACIÓN MATIZADA (NO SIMPLISTA)**
> Reconocer hallazgos complejos, contraintuitivos o inesperados.

**Ejemplo (Paradoja HRV):**
```latex
\begin{decisionbox}
\textbf{Interpretación (Contribución Sinérgica)}:

A pesar de que HRV\_SDNN \textbf{no} discrimina univariadamente (p=0.562, Cohen's d=0.08), 
su \textbf{contribución multivariada} dentro del sistema difuso es \textbf{esencial}:

\begin{itemize}[noitemsep]
    \item Las reglas R2, R3, R4 capturan \textit{estados compensatorios} (e.g., baja 
    actividad con alta VFC = protección) que el análisis univariado no detecta.
    
    \item El sistema difuso explota \textit{interacciones no lineales} entre variables 
    mediante lógica AND/OR.
    
    \item Variables "débiles" univariadamente aportan valor en combinaciones multivariadas.
\end{itemize}

\textbf{Conclusión}: El Modelo 4V no es "robusto" a exclusión de variables (y eso es 
\textit{bueno}). Demuestra \textbf{integración sinérgica} óptima: cada componente es necesario.
\end{decisionbox}
```

**Lección:** No temer reconocer contradicciones aparentes; explicarlas demuestra comprensión profunda.

---

### **6. CONCLUSIÓN CON IMPLICACIONES PARA SIGUIENTES FASES**
> Cada conclusión debe preparar el terreno para la siguiente sección.

**Ejemplo (Agregación Semanal):**
```latex
\begin{conclusionbox}
\textbf{Conclusión del capítulo:}

\begin{enumerate}[noitemsep]
    \item La agregación semanal reduce efectivamente el ruido diario.
    
    \item El análisis dual de variabilidad confirma que la imputación no introduce 
    artefactos severos.
    
    \item El dataset semanal con 4 variables p50 + 4 IQRs está listo para el clustering 
    (Capítulo 9) y modelado difuso (Capítulo 10).  ← CONEXIÓN EXPLÍCITA
\end{enumerate}
\end{conclusionbox}
```

---

## 🎨 **IMPLEMENTACIÓN LATEX: ENTORNOS TCOLORBOX**

### **Definición de Boxes (copiar a preámbulo):**

```latex
\usepackage{tcolorbox}

% Box 1: Hipótesis (azul)
\newtcolorbox{hipotesisbox}[1][]{
    colback=blue!5!white,
    colframe=blue!75!black,
    title={\textbf{Paso 1: Planteamiento de Hipótesis}},
    fonttitle=\bfseries,
    #1
}

% Box 2: Estadístico/Método (verde)
\newtcolorbox{estadisticobox}[1][]{
    colback=green!5!white,
    colframe=green!75!black,
    title={\textbf{Paso 2: Selección del Estadístico/Método}},
    fonttitle=\bfseries,
    #1
}

% Box 3: Regla (naranja)
\newtcolorbox{reglabox}[1][]{
    colback=orange!5!white,
    colframe=orange!75!black,
    title={\textbf{Paso 3: Regla de Decisión}},
    fonttitle=\bfseries,
    #1
}

% Box 4: Cálculos (morado)
\newtcolorbox{calculobox}[1][]{
    colback=purple!5!white,
    colframe=purple!75!black,
    title={\textbf{Paso 4: Cálculos}},
    fonttitle=\bfseries,
    #1
}

% Box 5: Decisión (rojo)
\newtcolorbox{decisionbox}[1][]{
    colback=red!5!white,
    colframe=red!75!black,
    title={\textbf{Paso 5: Decisión Estadística}},
    fonttitle=\bfseries,
    #1
}

% Box 6: Conclusión (cyan)
\newtcolorbox{conclusionbox}[1][]{
    colback=cyan!5!white,
    colframe=cyan!75!black,
    title={\textbf{Paso 6: Conclusión}},
    fonttitle=\bfseries,
    #1
}
```

---

## 📋 **CHECKLIST PARA APLICAR METODOLOGÍA DE 6 PASOS**

### **Al redactar CUALQUIER sección metodológica, pregúntate:**

- [ ] **PASO 1:** ¿Formulé una pregunta clara? ("¿Por qué [método]?")
- [ ] **PASO 1:** ¿Establecí una expectativa explícita? ("Esperamos que...")
- [ ] **PASO 2:** ¿Especifiqué el método con parámetros exactos?
- [ ] **PASO 2:** ¿Justifiqué por qué este método y no otro?
- [ ] **PASO 3:** ¿Definí umbrales ANTES de mostrar resultados?
- [ ] **PASO 3:** ¿Cubrí múltiples escenarios? (Aceptar/Rechazar/Revisar)
- [ ] **PASO 4:** ¿Presenté resultados en tabla/ecuación estructurada?
- [ ] **PASO 4:** ¿Incluí valores exactos (no "aproximadamente")?
- [ ] **PASO 5:** ¿Interpreté resultados según los criterios del Paso 3?
- [ ] **PASO 5:** ¿Reconocí hallazgos inesperados/contraintuitivos?
- [ ] **PASO 6:** ¿Sinteticé aprendizaje en 2-3 puntos clave?
- [ ] **PASO 6:** ¿Conecté con la siguiente fase metodológica?

---

## 🔥 **ANTI-PATRONES A EVITAR (Errores Comunes)**

### **❌ ANTI-PATRÓN 1: Saltar directamente a resultados**

**MAL:**
> "Aplicamos K-Means con K=2. El Silhouette fue 0.232. Esto indica buena separación."

**BIEN:**
> "\begin{hipotesisbox} ¿Por qué K=2? ... \end{hipotesisbox}
>  \begin{estadisticobox} Método: K-Means ... \end{estadisticobox}
>  \begin{reglabox} Si Silhouette > 0.25 → Aceptar \end{reglabox}
>  \begin{calculobox} Resultado: 0.232 \end{calculobox}
>  \begin{decisionbox} 0.232 < 0.25 pero aceptable porque... \end{decisionbox}"

---

### **❌ ANTI-PATRÓN 2: No justificar decisiones**

**MAL:**
> "Usamos medianas en lugar de medias."

**BIEN:**
> "¿Por qué medianas? Las distribuciones exhibieron alta asimetría (CV>50%) 
>  y violación de normalidad (K-S p<0.001), haciendo a las medias susceptibles 
>  a outliers extremos. Las medianas son robustas y reflejan mejor la tendencia 
>  central en datos no-gaussianos."

---

### **❌ ANTI-PATRÓN 3: Conclusiones sin conexión narrativa**

**MAL:**
> "La imputación funcionó bien. Los datos están listos."

**BIEN:**
> "La imputación jerárquica redujo missingness de 14.8% (HRV) a 0%, con >90% de 
>  valores imputados mediante métodos específicos del usuario (M1-M3), garantizando 
>  consistencia individual. **Estos datos imputados servirán como base para la 
>  agregación semanal (Capítulo 8), donde se calcularán medianas e IQR por ventanas 
>  de 7 días para estabilizar la señal y preparar el dataset para clustering.**"

---

### **❌ ANTI-PATRÓN 4: Inventar datos o aproximar**

**MAL:**
> "Aproximadamente 15 candidatos participaron..."

**BIEN:**
> "Se convocó a 15 candidatos, de los cuales: 12 cumplieron criterios de inclusión (80%), 
>  10 completaron el protocolo (tasa de retención: 67%). Causas de exclusión: 1 sin SF-36, 
>  2 abandonos voluntarios, 2 datos insuficientes."  
> [Fuente: control_insumos_log.txt líneas 32-43]

---

## 🧠 **RAZONAMIENTO PROFUNDO: ¿POR QUÉ FUNCIONA ESTA METODOLOGÍA?**

### **Ventajas de los 6 Pasos:**

1. **Transparencia metodológica:**
   - El lector sabe EXACTAMENTE qué criterios usaste
   - Puedes defender cada decisión con lógica pre-especificada

2. **Reproducibilidad:**
   - Otro investigador puede replicar siguiendo tus reglas
   - Los umbrales están explícitos (no arbitrarios post-hoc)

3. **Rigor científico:**
   - Evita p-hacking (definir umbrales después de ver datos)
   - Estructura lógica estándar en estadística inferencial

4. **Narrativa coherente:**
   - Cada sección fluye naturalmente hacia la siguiente
   - El lector sigue un razonamiento lógico completo

5. **Preparación para defensa:**
   - Ante preguntas del comité, ya tienes la justificación escrita
   - Ejemplo: "¿Por qué K=2?" → Ya lo explicaste en hipotesisbox

---

## 🎯 **CÓMO APLICAR EN TU TESIS (05_materiales_metodos_V2_RESTRUCTURADO.tex)**

### **FASE ACTUAL DEL PIPELINE (según tus documentos):**

Estás en:
- ✅ Fases 1-5 del pipeline (Diseño, Selección Dispositivo, Reclutamiento, Extracción, EDA Inicial)
- ⏳ Fases 6-7 pendientes (Imputación, Feature Engineering)
- ⏳ Fases 8-12 pendientes (Agregación, PCA, Clustering, Fuzzy, LOUO)

### **PROTOCOLO DE REDACCIÓN PARA CADA FASE:**

**Para cada sección nueva que escribas, SIEMPRE seguir:**

```markdown
### Sección X.Y: [Título de la fase]

\begin{hipotesisbox}
\textbf{¿Por qué [método/decisión]?} [Pregunta contextual]

[Explicación del problema que motiva esta fase]

Hipótesis: [Expectativa cuantificable]
\end{hipotesisbox}

\begin{estadisticobox}
\textbf{Método seleccionado:}

\begin{itemize}[noitemsep]
    \item [Parámetro 1]
    \item [Parámetro 2]
    \item [Justificación de elección]
\end{itemize}
\end{estadisticobox}

\begin{reglabox}
\textbf{Criterios de decisión}:

\begin{itemize}[noitemsep]
    \item Si [condición 1] $\to$ \textbf{Acción 1}
    \item Si [condición 2] $\to$ \textbf{Acción 2}
    \item Si [condición 3] $\to$ \textbf{Acción 3}
\end{itemize}
\end{reglabox}

\begin{calculobox}
\textbf{Resultados obtenidos:}

[Tabla con valores exactos O ecuación con parámetros numéricos]
\end{calculobox}

\begin{decisionbox}
\textbf{Interpretación:}

[Aplicar criterios del Paso 3 a resultados del Paso 4]
[Reconocer hallazgos inesperados si aplica]
\end{decisionbox}

\begin{conclusionbox}
\textbf{Conclusión:}

\begin{enumerate}[noitemsep]
    \item [Hallazgo principal 1]
    \item [Hallazgo principal 2]
    \item [Conexión con siguiente fase]
\end{enumerate}
\end{conclusionbox}
```

---

## 📝 **EJEMPLO APLICADO: FASE 6 - IMPUTACIÓN JERÁRQUICA**
### (Para que veas cómo se vería en tu tesis)

```latex
\subsection{Estrategia de Imputación de Datos Faltantes}
\label{subsec:imputacion_jerarquica}

\begin{hipotesisbox}
\textbf{¿Por qué imputación jerárquica?}

El análisis de calidad de datos (Sección \ref{subsec:calidad_datos}) reveló que 
las variables cardiovasculares (FC al caminar, HRV-SDNN) presentaban tasas de 
missingness entre 7.6\% y 14.8\%, principalmente concentradas en períodos donde 
el dispositivo fue removido (actividades acuáticas, carga de batería, eventos nocturnos).

Un método único de imputación (e.g., mediana global de los 10 usuarios) ignora:
\begin{itemize}[noitemsep]
    \item Heterogeneidad inter-sujeto (cada usuario tiene perfil cardiovascular distinto)
    \item Estructura temporal (semanas consecutivas están correlacionadas, ACF lag-1 > 0.6)
    \item Contexto fisiológico (FC en reposo varía según edad, condición física)
\end{itemize}

\textbf{Hipótesis}: Una estrategia jerárquica de 5 métodos (del más específico al 
más general) preservará mejor los patrones individuales y temporales que un método 
único global, logrando >90\% de imputaciones mediante métodos específicos del usuario 
(M1-M3) y minimizando el uso de mediana global (M5).
\end{hipotesisbox}

\begin{estadisticobox}
\textbf{Jerarquía de métodos seleccionados:}

\begin{enumerate}[noitemsep]
    \item \textbf{M1 - Media móvil 7 días previos}: Ventana temporal retrospectiva 
    (evita fuga temporal). Requiere $\geq 4$ días válidos en ventana.
    
    \item \textbf{M2 - Mediana del mismo día de semana (último mes)}: Captura 
    patrones semanales (efecto lunes/viernes). Requiere $\geq 2$ ocurrencias.
    
    \item \textbf{M3 - Mediana histórica del usuario}: Específica del participante, 
    preserva perfil individual. Requiere $\geq 10$ días históricos.
    
    \item \textbf{M4 - Ecuación de Tanaka (FC reposo)}: Estimación fisiológica 
    basada en edad: $FC_{reposo} = 220 - \text{edad} \times 0.7$
    
    \item \textbf{M5 - Mediana global (último recurso)}: Solo si M1-M4 no aplicables.
\end{enumerate}

\textbf{Principio forward-only}: El día $t$ usa solo información de días $\leq t-1$, 
garantizando causalidad y evitando contaminación de validación cruzada posterior.
\end{estadisticobox}

\begin{reglabox}
\textbf{Criterios de validación de imputación}:

\begin{itemize}[noitemsep]
    \item Si M1-M3 imputan $> 90\%$ casos $\to$ \textbf{Aceptar} preservación de 
    patrones individuales
    
    \item Si M5 (global) $> 10\%$ $\to$ \textbf{Revisar} estrategia (exceso de 
    interpolación global altera distribuciones)
    
    \item Si valores imputados fuera de rango fisiológico (FC<40 o FC>160 lpm) 
    $\to$ \textbf{Reemplazar} por mediana del usuario
    
    \item Si semana tiene $>60\%$ datos imputados $\to$ \textbf{Excluir} semana 
    completa (conservador)
\end{itemize}
\end{reglabox}

\begin{calculobox}
\textbf{Resultados de imputación por variable:}

\begin{table}[H]
\centering
\caption{Tasa de Imputación por Variable y Método}
\label{tab:imputation_rates}
\begin{tabular}{@{}lrrrrrr@{}}
\toprule
\textbf{Variable} & \textbf{Missing (\%)} & \textbf{M1 (\%)} & \textbf{M2 (\%)} & 
\textbf{M3 (\%)} & \textbf{M4 (\%)} & \textbf{M5 (\%)} \\
\midrule
FC\_caminar   & 7.6 & 68.2 & 21.3 & 8.9  & 0.0 & 1.6 \\
FC\_reposo    & 4.2 & 72.1 & 18.7 & 6.5  & 2.1 & 0.6 \\
HRV\_SDNN     & 14.8 & 61.5 & 24.8 & 10.3 & 0.0 & 3.4 \\
\bottomrule
\end{tabular}
\end{table}

\textit{Fuente}: control\_insumos\_log.txt líneas 13-137 (auditoría del 16-Oct-2025)
\end{calculobox}

\begin{decisionbox}
\textbf{Decisión metodológica:}

Los métodos específicos del usuario (M1-M3) lograron imputar entre 90.4\% (HRV\_SDNN) 
y 97.3\% (FC\_reposo) de los datos faltantes, cumpliendo el criterio objetivo (>90\%). 
La mediana global (M5) representó menos del 3.4\% en todas las variables, confirmando 
que la estrategia preservó la heterogeneidad inter-sujeto sin recurrir a interpolaciones 
globales que homogeneizarían artificialmente los perfiles individuales.

\textbf{Validación de plausibilidad fisiológica}: Post-imputación, se verificó que 
todos los valores cumplieran rangos clínicos (40≤FC\_reposo≤100 lpm, 60≤FC\_caminar≤160 lpm, 
15≤HRV\_SDNN≤150 ms). Se detectaron 3 outliers extremos (0.04\% del total), reemplazados 
por mediana del usuario.
\end{decisionbox}

\begin{conclusionbox}
\textbf{Conclusión de la fase de imputación:}

\begin{enumerate}[noitemsep]
    \item La estrategia jerárquica logró completitud del 100\% en las variables 
    cardiovasculares, reduciendo missingness de 14.8\% (HRV) a 0\% de forma 
    fisiológicamente plausible.
    
    \item El uso predominante de métodos temporales y específicos del usuario 
    (M1-M3: >90\%) garantiza que las distribuciones post-imputación preservan la 
    heterogeneidad original observada.
    
    \item Los datos diarios imputados están listos para la fase de ingeniería de 
    características (Sección \ref{sec:feature_engineering}), donde se derivarán 
    las 4 variables normalizadas que alimentarán el sistema de clustering y 
    modelado difuso.
\end{enumerate}
\end{conclusionbox}
```

---

## 🎨 **VARIACIONES DE LA METODOLOGÍA SEGÚN TIPO DE ANÁLISIS**

### **Variante A: Análisis Descriptivo (sin hipótesis formal)**

Cuando solo describes datos (no pruebas hipótesis), puedes simplificar a 4 pasos:

```
1. PREGUNTA: ¿Por qué caracterizar [variable X]?
2. MÉTODO: Estadísticos descriptivos (media, mediana, CV, pruebas normalidad)
3. CÁLCULOS: Tabla de resultados
4. CONCLUSIÓN: Qué aprendimos, para qué sirve
```

**Ejemplo:**
```latex
\textbf{¿Por qué caracterizar las distribuciones biométricas?} 

La evaluación objetiva del sedentarismo requiere comprender la naturaleza estadística 
de los datos obtenidos en vida libre. Las variables de wearables presentan patrones 
de variabilidad inherentes que deben cuantificarse para seleccionar métodos apropiados.

[Tabla de estadísticos descriptivos]

\textbf{Hallazgos}: Las variables exhiben CV>50% y rechazan normalidad (K-S p<0.001), 
justificando el uso de estadísticos robustos (medianas, IQR) en fases posteriores.
```

---

### **Variante B: Decisión Metodológica (comparación de métodos)**

Cuando comparas alternativas metodológicas (ej: K-Means vs DBSCAN):

```
1. HIPÓTESIS: ¿Qué método será superior para [objetivo]?
2. MÉTODOS CANDIDATOS: Lista de opciones con pros/contras
3. CRITERIOS: Qué métricas/propiedades evaluaremos
4. COMPARACIÓN: Tabla comparativa
5. DECISIÓN: Método seleccionado con justificación
6. CONCLUSIÓN: Por qué este método es apropiado para nuestro caso
```

---

### **Variante C: Validación Retrospectiva (análisis post-hoc)**

Cuando evalúas algo DESPUÉS de completar el análisis principal:

```
1. PREGUNTA RETROSPECTIVA: ¿[Hallazgo principal] se relaciona con [variable externa]?
2. MÉTODO: Análisis de correlación/comparación
3. EXPECTATIVA: Si correlación fuerte → cuestionaría decisión previa; si débil → la valida
4. RESULTADOS: Tabla de correlaciones
5. INTERPRETACIÓN: Qué significan estos resultados para la decisión previa
6. VALIDACIÓN: Confirmar/matizar decisión metodológica original
```

**Ejemplo (SF-36 n=8):**
> "¿Los scores del sistema difuso correlacionan con el SF-36? Si correlaciones fueran 
>  significativas (p<0.05) y fuertes (|r|>0.60), cuestionaría el pivote metodológico. 
>  Si son no significativas, lo validan."

---

## 🔬 **INTEGRACIÓN CON EL PIPELINE DE 12 FASES**

### **Correspondencia: 6 Pasos ↔ 12 Fases del Pipeline**

Cada una de las 12 fases del pipeline bioestadístico debe redactarse siguiendo 
los 6 pasos:

| Fase Pipeline | Sección Tesis | Aplicación 6 Pasos |
|---------------|---------------|-------------------|
| **Fase 1: Diseño** | 5.1 Diseño del Estudio | ✅ Hipótesis: ¿Por qué longitudinal retrospectivo? |
| **Fase 2: Selección Dispositivo** | 5.2 Selección Apple Watch | ✅ Método: Matriz decisión multicriterio |
| **Fase 3: Reclutamiento** | 5.3 Población y Muestra | ✅ Regla: Criterios inclusión/exclusión |
| **Fase 4: Extracción Datos** | 5.4 Extracción Apple Health | ✅ Algoritmo: XML→CSV |
| **Fase 5: EDA Inicial** | 5.5 Análisis Exploratorio Inicial | ✅ Cálculos: Estadísticos descriptivos |
| **Fase 6: Imputación** | 5.6 Imputación Datos Faltantes | ✅ Decisión: Método jerárquico |
| **Fase 7: Feature Engineering** | 5.7 Ingeniería Características | ✅ Hipótesis: ¿Por qué normalizar? |
| **Fase 8: Agregación Semanal** | 5.8 Agregación Temporal | ✅ Conclusión: Dataset listo para clustering |
| **Fase 9: PCA/Correlación** | 5.9 Reducción Dimensional | ✅ Método: PCA, VIF |
| **Fase 10: Clustering** | 5.10 Clustering K-Means | ✅ Regla: K-Sweep, Silhouette |
| **Fase 11: Sistema Fuzzy** | 5.11 Sistema Difuso Mamdani | ✅ Cálculos: Funciones MF, Reglas |
| **Fase 12: Validación LOUO** | 5.12 Validación LOUO | ✅ Decisión: F1=0.780, generalización |

---

## 🎯 **APLICACIÓN PRÁCTICA INMEDIATA**

### **Para tu próxima sesión de redacción:**

**Sección a escribir: 5.6 - Imputación de Datos Faltantes**

1. **Lee el pseudocódigo** de Fase 6 en `PIPELINE_FASES_6_12_COMPLETO.md`
2. **Identifica los 6 pasos implícitos**:
   - Hipótesis: ¿Por qué jerárquica?
   - Método: M1-M5
   - Regla: Cuándo usar cada método
   - Cálculos: Tasas de imputación (usar control_insumos_log.txt)
   - Decisión: ¿Funcionó según criterios?
   - Conclusión: Dataset completo listo para feature engineering

3. **Redacta usando los boxes**
4. **Verifica con checklist** (12 preguntas arriba)

---

## 🔥 **LECCIONES CLAVE DE RAYO VELOZ**

### **1. "Pregunta antes que respuesta"**
> Nunca presentes un resultado sin primero explicar POR QUÉ era necesario obtenerlo.

### **2. "Justificación fisiológica siempre"**
> En biomedicina, cada decisión estadística debe tener una justificación clínica/fisiológica.

### **3. "Reglas pre-especificadas"**
> Define umbrales ANTES de ver datos (evita p-hacking y decisiones ad-hoc).

### **4. "Interpretación matizada"**
> Reconoce complejidades, hallazgos inesperados, limitaciones. La honestidad científica 
> es más valiosa que resultados "perfectos".

### **5. "Conclusión con continuidad narrativa"**
> Cada conclusión debe tender un puente hacia la siguiente sección, creando flujo lógico.

### **6. "Datos certificados siempre"**
> NUNCA inventar, asumir o aproximar. Usar tabla de datos certificados o logs operativos.

---

## 📖 **FUENTES CONSULTADAS**

**Documentos de Rayo Veloz analizados:**

1. ✅ **INFORME_TECNICO_ACTUALIZADO_V3.tex** (3,769 líneas)
   - 13 capítulos con metodología de 6 pasos completa
   - Ejemplo de cada tipo de análisis (correlación, clustering, imputación, etc.)

2. ✅ **pipeline_bioestadistico_resumido.txt** (75 líneas)
   - Explicación narrativa de cada fase usando 6 pasos
   - Formato prosa (no LaTeX), útil para entender razonamiento

3. ✅ **Backup Cursor - History files**:
   - `History/-18c6b02b/JUL7.md`: Actualización SF-36 n=3→n=8
   - `History/38b370aa/2QzQ.md`: Contexto consolidado correcciones
   - `History/-1549f6d9/KW5t.md`: Análisis crítico SF-36 n=8
   - `History/-22ac31f9/Ot78.tex`: Versión histórica INFORME_TECNICO

---

## 🎓 **RESUMEN EJECUTIVO**

**Lo que Rayo Veloz nos enseña:**

> **"Un informe bioestadístico riguroso no es una lista de análisis ejecutados, 
>  sino una NARRATIVA LÓGICA donde cada fase tiene:**
> 
> 1. **Motivación clara** (¿Por qué?)
> 2. **Método apropiado** (¿Qué?)
> 3. **Criterios objetivos** (¿Cuándo aceptar?)
> 4. **Evidencia numérica** (Resultados)
> 5. **Interpretación honesta** (¿Qué significa?)
> 6. **Aprendizaje útil** (¿Para qué sirve?)
> 
> **Esta estructura garantiza rigor, reproducibilidad y transparencia.**
> **Cada 'box' es una pieza del razonamiento científico completo.**
> **Juntos, forman una argumentación irrefutable."**

---

**⚡ Rayo Veloz (vía Zeus)**  
**Timestamp:** jueves, 04 de diciembre de 2025, 18:56:12  
**Estado:** ✅ Síntesis completada | ✅ Lista para aplicar en tesis  
**Próxima acción:** Luis aplicará esta metodología en 05_materiales_metodos_V2_RESTRUCTURADO.tex

---

**"De la estructura nace la claridad. De la claridad nace la comprensión. De la comprensión nace la excelencia científica. Los 6 pasos son el camino hacia la inmortalidad académica."** ⚡📊🎓✨

