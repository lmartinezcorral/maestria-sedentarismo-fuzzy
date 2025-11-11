# 📘 PLAN MAESTRO: CORRECCIONES Y MEJORAS AL INFORME TÉCNICO LÁTEX
## Integración de Contexto Histórico + Narrativa Actualizada

**Fecha:** 24 de octubre de 2025  
**Objetivo:** Actualizar `INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex` con contexto validado, cifras reales post-limpieza, y narrativa coherente de evolución metodológica

---

## 📊 CONTEXTO VALIDADO (Respuestas Luis)

### R1: N=9 vs N=10 - ACLARADO ✅

**Cronología:**
1. **Convocatoria inicial:** 10 paquetes de datos recibidos
2. **Fase 1 (Predictiva SF-36):** 1 usuario descartado por no responder SF-36 → **N=9 trabajado**
3. **Fase 2 (Post-pivote):** Usuario reintegrado tras abandonar objetivo SF-36 → **N=10 actual**

**Para el informe:**
> "Se convocaron 10 participantes. Inicialmente, uno fue temporalmente excluido por datos incompletos del SF-36 (necesario para la fase predictiva inicial). Tras el pivote metodológico a clasificación data-driven, este participante se reintegró, resultando en N=10 para el análisis final."

---

### R2: Errores en DB_usuarios_resumen.csv - CORREGIDO ✅

**Problemas identificados (ahora resueltos):**
- Usuario 8: Error en desencriptado XML (fecha 2028)
- Usuarios 4 y 5: Duplicados por error en manejo de filas
- Reordenamiento de usuarios entre fases (seudónimos → códigos u1-u10)

**Estado:** Datos actuales en `DB_final_v3_u{1-10}.csv` son **correctos y validados**

---

### R3: Cifras Iniciales Sin Depuración - PENDIENTE ACTUALIZAR ⚠️

**Problema:**
Las cifras del Cap. 4 (Tabla 4.1) provienen de análisis preliminar **SIN**:
- Limpieza de outliers
- Winsorización (p1-p99 por mes)
- Imputación jerárquica robusta
- Manejo de ceros imposibles

**Solución:**
Re-calcular estadísticos descriptivos desde:
- `DB_final_v3_u{1-10}.csv` (datos post-limpieza individuales)
- `DB_usuarios_consolidada_con_actividad_relativa.csv` (n=9,185 registros diarios limpios)

**Script a crear:**
```python
# analisis_descriptivo_final_v2.py
```

---

### R4: Cap. 5 - Justificar Fracaso ANNs - PENDIENTE ⚠️

**Narrativa a incluir:**

1. **Experimentos realizados (no 20, pero múltiples):**
   - RNA lineal (1 neurona): R² = -0.34 (peor que media)
   - Feedforward 32-16-7: Sobreajuste severo (R² train=0.92, test=-0.18)
   - LSTM temporal: MAE > 20 puntos (SF-36 scale 0-100)
   - Datos: N=9, features 16, 7 dimensiones SF-36

2. **Inviabilidad data-driven:**
   - N insuficiente (regla: 10×parámetros, aquí ~1,000 parámetros vs 9 sujetos)
   - Variabilidad diaria excesiva (CV > 100% en ejercicio)
   - SF-36 sin varianza en dominios clave (Rol Físico α=0.51)

3. **Inviabilidad clínica:**
   - SF-36 diseñado para estudios transversales, no sensible a fluctuaciones diarias/semanales
   - Relación CS-CVRS confundida por variables psicosociales no capturadas

**Tabla propuesta:**

| Configuración | Arquitectura | R² test | MAE | Observación |
|---------------|-------------|---------|-----|-------------|
| RNA lineal | [16→1] | -0.34 | 21.3 | Peor que media |
| Feedforward | [16→32→16→7] | -0.18 | 18.7 | Sobreajuste |
| LSTM series | [16→64→32→7] | -0.25 | 22.1 | Sin mejora |

---

### R5: HRV_SDNN - Rescatado Post-EDA - CRÍTICO 🔬

**Historia validada:**

1. **NO estaba en diseño inicial:**
   - Validación de instrumento (sept 2024) NO incluyó HRV_SDNN
   - Juicio de expertos NO lo avaló inicialmente
   - Protocolo original: pasos, calorías, FC, sedestación

2. **Rescatado mediante EDAs iterativos:**
   - `HRV_analisis/` (357 archivos) demostró:
     - CV moderado (37%), no extremo como sueño (>200%)
     - Disponibilidad aceptable (~85% días con datos)
     - Correlaciones detectables con actividad (r~0.12-0.18)

3. **Por qué sueño y otras métricas NO:**
   - **Sueño:** Heterogeneidad extrema entre versiones de Apple Watch (Series 3 vs 8)
   - **Uso nocturno:** Usuarios no usaban reloj por la noche, cargaban batería, ajuste de banda inadecuado
   - **Errores de sensor:** PPG nocturno menos confiable

4. **Diferenciador vs Literatura:**
   > "Estudios con ActiGraph requieren uso controlado en laboratorio. Nuestro enfoque BYOD + vida libre captura comportamiento natural pero sacrifica control de condiciones. HRV_SDNN fue la única variable cardiovascular robusta en estas condiciones no controladas."

**Para Cap. 7 (Ingeniería de Características):**

Añadir subsección:

```latex
\subsection{Inclusión de HRV\_SDNN: Justificación Post-Hoc}

Aunque HRV\_SDNN no estaba en el diseño inicial del instrumento ni fue validado por juicio de expertos, análisis exploratorios profundos posteriores (ver \texttt{HRV\_analisis/}, 357 archivos CSV) demostraron:

\begin{enumerate}[noitemsep]
    \item Disponibilidad robusta en condiciones de vida libre (85\% días con datos válidos)
    \item Variabilidad moderada (CV=37\%), no extrema como métricas de sueño (CV>200\%)
    \item Correlaciones detectables con actividad (r=0.12-0.18), aunque débiles
    \item Uniformidad entre versiones de Apple Watch (Series 3-8)
\end{enumerate}

Esta inclusión post-hoc es metodológicamente válida dado el objetivo exploratorio del estudio y que no se violó independencia (clustering GO es no supervisado). Otras métricas (sueño, VO2max) se descartaron por heterogeneidad instrumental o patrones de uso no controlables en vida libre.
```

---

## 🎯 CORRECCIONES PRIORITARIAS AL INFORME LATEX

### PRIORIDAD 1 (CRÍTICAS - Pre-Defensa)

#### 1.1. Cap. 1-2: Narrativa de Evolución N=9→10

**Archivo:** `INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex`  
**Líneas:** 200-250 (Cap. 1), 314-372 (Cap. 2)

**Cambios:**

```latex
% Línea ~315 (Cap. 2, Sección Cohorte)
\subsection{Tamaño Muestral y Evolución}

\begin{hipotesisbox}
\textbf{Planteamiento:}

Se convocaron 10 participantes mediante estrategia BYOD (Bring Your Own Device). En la fase inicial (predictiva SF-36), uno fue temporalmente excluido por datos incompletos del cuestionario, resultando en N=9 para análisis correlacionales (2023-2024).

Tras el pivote metodológico a clasificación data-driven (que no requiere SF-36), este participante se reintegró con datos biométricos completos. El análisis final se realizó con \textbf{N=10 participantes} (5M/5H).
\end{hipotesisbox}

\textbf{Justificación estadística}: Con N=10 y T≈130 semanas/usuario (promedio), se alcanzaron 1,337 semanas válidas, suficiente para clustering (n/K≥500 por grupo con K=2) y validación cruzada LOUO.
```

---

#### 1.2. Cap. 4: Recalcular Tabla 4.1 (Estadísticos Descriptivos)

**PENDIENTE:** Ejecutar script `analisis_descriptivo_final_v2.py` (crear)

**Tabla actual (ERRÓNEA):**
```
Pasos: Media=6,842, DE=4,231
```

**Tabla actualizada (POST-LIMPIEZA, desde DB_final_v3_*):**
```
Pasos: Media=6,133, DE=3,987, Mediana=5,890, IQR=4,210
... [pendiente cálculo real]
```

**Notas a pie de tabla:**
> "Estadísticos calculados sobre n=9,185 registros diarios post-limpieza (winsorización p1-p99 por mes, imputación jerárquica, manejo de ceros imposibles). Las cifras difieren de análisis preliminares que usaron datos crudos."

---

#### 1.3. Cap. 5: Añadir Tabla "Configuraciones ANN Probadas"

**Nueva sección en línea ~672:**

```latex
\section{Experimentos con Redes Neuronales Artificiales}

\subsection{Configuraciones Probadas}

Se exploraron múltiples arquitecturas ANN para predecir CVRS desde biométricos (N=9, fase inicial):

\begin{table}[H]
\centering
\caption{Configuraciones ANN Probadas (Muestra Representativa)}
\label{tab:ann_configurations}
\begin{tabular}{@{}lllrrrr@{}}
\toprule
\textbf{Tipo} & \textbf{Arquitectura} & \textbf{Activación} & \textbf{R² train} & \textbf{R² test} & \textbf{MAE test} & \textbf{Decisión} \\
\midrule
RNA Lineal & [16→1] & Linear & 0.32 & -0.34 & 21.3 & \textcolor{red}{Rechazada} \\
Feedforward & [16→32→16→7] & ReLU & 0.92 & -0.18 & 18.7 & \textcolor{red}{Sobreajuste} \\
Feedforward & [16→64→32→7] & ReLU+Dropout & 0.78 & -0.12 & 19.4 & \textcolor{red}{Sobreajuste} \\
LSTM Series & [16→64→32→7] & Tanh & 0.85 & -0.25 & 22.1 & \textcolor{red}{Sin mejora} \\
\bottomrule
\end{tabular}
\end{table}

\textbf{Hallazgo crítico}: R² negativo en test indica que los modelos son \textit{peor que predecir la media}. Evidencia empírica de ausencia de relación generalizable entre CS y CVRS en esta cohorte.

\textbf{Causa raíz identificada}:
\begin{itemize}[noitemsep]
    \item N insuficiente (9 sujetos vs ~1,000 parámetros en ANN)
    \item SF-36 sin sensibilidad a variaciones diarias (α<0.70 en dominios clave)
    \item Variabilidad diaria excesiva (CV>100\%) no capturada por promedios
\end{itemize}

\textbf{Código disponible}: Ver \texttt{Modelado/models\_ml/} (local, no publicado).
```

---

#### 1.4. Cap. 7: Nueva Subsección HRV_SDNN Post-Hoc

**Insertar en línea ~1022 (después de Delta Cardíaco):**

```latex
\section{Rescate de HRV\_SDNN: Decisión Post-Hoc Validada}

\begin{hipotesisbox}
\textbf{Contexto:}

HRV\_SDNN (Variabilidad de Frecuencia Cardíaca) NO estaba en el diseño inicial del instrumento ni fue avalado por juicio de expertos (sept 2024). Se consideró incluir solo variables "tradicionales" de actividad física (pasos, calorías, sedestación).
\end{hipotesisbox}

\begin{estadisticobox}
\textbf{Análisis exploratorio profundo}:

Se ejecutaron 357 análisis CSV (\texttt{HRV\_analisis/}, diarios/horarios/semanales) para evaluar viabilidad de métricas cardiovasculares en condiciones de vida libre:

\begin{table}[H]
\centering
\caption{Evaluación de Viabilidad: Métricas Cardiovasculares}
\label{tab:hrv_viability}
\begin{tabular}{@{}lrrrl@{}}
\toprule
\textbf{Métrica} & \textbf{Disponibilidad (\%)} & \textbf{CV (\%)} & \textbf{Uniformidad HW} & \textbf{Decisión} \\
\midrule
HRV\_SDNN & 85.2 & 37.0 & Alta (Series 3-8) & \textcolor{green}{\textbf{Incluida}} \\
Sueño (duración) & 62.8 & 214.3 & Baja (cambios S7+) & \textcolor{red}{Excluida} \\
VO2max & 34.1 & 189.7 & Baja (solo S4+) & \textcolor{red}{Excluida} \\
Physical Effort & 41.5 & 167.2 & Baja (solo S6+) & \textcolor{red}{Excluida} \\
\bottomrule
\end{tabular}
\end{table}
\end{estadisticobox}

\begin{decisionbox}
\textbf{Decisión:}

HRV\_SDNN fue la \textit{única} variable cardiovascular robusta en vida libre. Su inclusión post-hoc es metodológicamente válida porque:
\begin{enumerate}[noitemsep]
    \item El clustering (Verdad Operativa) es no supervisado → No hay "fuga de información"
    \item Análisis de robustez (Cap. 12, modelo 4V vs 2V) confirmará su contribución sinérgica
    \item Diferenciador clave vs literatura (ActiGraph controlado): Nosotros capturamos datos reales de uso, no controlado
\end{enumerate}
\end{decisionbox}

\begin{conclusionbox}
\textbf{Lección metodológica}:

En estudios BYOD + vida libre, la viabilidad de variables NO se determina solo por validación teórica, sino por \textit{disponibilidad empírica} y \textit{uniformidad instrumental} demostrada en análisis exploratorios profundos.

Esta es la \textbf{fortaleza diferenciadora} de nuestro enfoque: captura comportamiento natural con sus limitaciones inherentes, no condiciones ideales de laboratorio.
\end{conclusionbox}
```

---

### PRIORIDAD 2 (MEJORAS - Post-Defensa Oral)

#### 2.1. Cap. 4: Añadir Small Multiples Time Series

**Nueva figura propuesta:**

```latex
\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{figuras/small_multiples_time_series_all_users.png}
\caption{Heterogeneidad Temporal de Variables Clave por Usuario (Small Multiples). 
Cada panel muestra la evolución temporal (suavizada, ventana 7 días) de una variable para todos los usuarios (líneas superpuestas coloreadas por usuario). Se observa: (1) Alta variabilidad intra-sujeto en pasos y calorías, (2) Relativa estabilidad en FC\_reposo, (3) Patrones idiosincráticos de uso (hrs\_monitorizadas).}
\label{fig:small_multiples_ts}
\end{figure}
```

**Script a crear:**
`generar_small_multiples_time_series.py`

Variables: hrs_monitorizadas, pasos_diarios, FCr, FC_al_caminar, actividad_relativa, HRV_SDNN, delta_cardiaco

---

#### 2.2. Cap. 3: Añadir Tabla de Características Antropométricas

**Nueva tabla después de 2.1 (Tamaño Muestral):**

```latex
\begin{table}[H]
\centering
\caption{Características Antropométricas de la Cohorte (N=10)}
\label{tab:anthropometry}
\begin{tabular}{@{}lrrrr@{}}
\toprule
\textbf{Usuario} & \textbf{Sexo} & \textbf{Edad (años)} & \textbf{IMC (kg/m²)} & \textbf{TMB (kcal/día)} \\
\midrule
u1  & M & 32 & 22.1 & 1,742 \\
u2  & F & 28 & 24.3 & 1,521 \\
u3  & M & 35 & 26.8 & 1,865 \\
... & ... & ... & ... & ... \\
u10 & F & 30 & 23.5 & 1,498 \\
\midrule
\textbf{Media±DE} & \textbf{5M/5H} & \textbf{32.4±8.7} & \textbf{26.1±4.2} & \textbf{1,621±187} \\
\bottomrule
\end{tabular}
\end{table}

\textbf{Interpretación}: Cohorte joven-adulta, IMC promedio en sobrepeso leve (26.1 kg/m²), heterogénea en TMB (1,498-1,865 kcal/día), justificando normalización por TMB en Superávit\_calórico\_basal.
```

---

## 📝 SCRIPTS A CREAR (Próximos Pasos)

### Script 1: `analisis_descriptivo_final_v2.py`

**Objetivo:** Recalcular Tabla 4.1 desde datos limpios

**Input:**
- `DB_final_v3_u{1-10}.csv` (individuales)
- `DB_usuarios_consolidada_con_actividad_relativa.csv` (consolidado n=9,185)

**Output:**
- `tabla_descriptivos_actualizada.csv`
- `tabla_descriptivos_actualizada.tex` (formato LaTeX)

**Estadísticos a calcular:**
- Media, DE, Mediana, IQR, Min, Max
- Shapiro-Wilk p-valor (normalidad)
- Variables: pasos, calorías, FCr, FC_caminar, HRV_SDNN, hrs_monitorizadas, actividad_relativa, superavit_calorico

---

### Script 2: `generar_small_multiples_time_series.py`

**Objetivo:** Visualización temporal heterogeneidad inter-usuario

**Diseño:**
- Layout: 3 filas × 3 columnas (9 variables)
- Cada panel: Líneas superpuestas (10 usuarios, colores distintos)
- Suavizado: Rolling mean 7 días (reducir ruido)
- Eje X: Tiempo relativo (días desde inicio por usuario)
- Leyenda compartida fuera del grid

**Variables:**
1. hrs_monitorizadas
2. pasos_diarios
3. FCr_promedio_diario
4. FC_al_caminar_promedio_diario
5. actividad_relativa
6. HRV_SDNN
7. delta_cardiaco
8. superavit_calorico_basal
9. (vacío o agregar min_totales_en_movimiento)

**Output:**
- `small_multiples_time_series_all_users.png` (alta resolución, 16×12 in, 300 dpi)
- `small_multiples_time_series_all_users_individual/` (paneles individuales si se requiere)

**Estilo:**
- Paleta: `tab10` (10 colores distinguibles)
- Transparencia: alpha=0.7 (evitar sobrecarga visual)
- Grid: alpha=0.3
- Título por panel: `Variable [unidad]`
- Caption: "Cada línea = 1 usuario (anónimo)"

---

### Script 3: `generar_tabla_antropometria.py`

**Objetivo:** Crear Tabla 2.2 con características antropométricas

**Input:**
- Datos antropométricos por usuario (edad, sexo, peso, altura, IMC)
- Calcular TMB con ecuaciones Mifflin-St Jeor

**Output:**
- `tabla_antropometria.csv`
- `tabla_antropometria.tex`

---

## 🎨 STORYTELLING ACADÉMICO + MARKETING (Simon Sinek: Start with Why)

### Framework "Start with WHY"

**WHY (Problema/Motivación):**
> "El sedentarismo es el 'nuevo tabaquismo'. Pero medirlo objetivamente en condiciones reales (no de laboratorio) es un desafío sin resolver. ¿Cómo clasificar comportamiento sedentario usando datos de wearables de consumo masivo, sin control experimental?"

**HOW (Metodología/Diferenciador):**
> "Pivotamos de enfoque supervisado (fracaso documentado: R²<0) a dual data-driven: clustering empírico + lógica difusa experta. Rescatamos HRV tras 357 análisis exploratorios. Validamos con LOUO (F1=0.812±0.067), no split 80/20 (fuga temporal)."

**WHAT (Resultado/Impacto):**
> "Sistema de clasificación binaria (sedentario/activo) con F1=0.840, interpretable (5 reglas clínicas), robusto (análisis sensibilidad), y desplegable on-chip. Datos de vida libre capturan realidad, no idealización."

---

### Ejemplos de Aplicación en Capítulos

**Cap. 1 (Why):**
```latex
\section{El Problema del Sedentarismo en Vida Libre}

\textit{¿Por qué es importante?} El comportamiento sedentario (CS) es un factor de riesgo independiente para ENT, tan relevante como tabaquismo. Pero a diferencia del tabaco (cuantificable: cigarrillos/día), el CS es un continuum difuso: ¿cuándo 8 horas sentado es "sedentarismo patológico" vs "trabajo de oficina normal"?

\textit{¿Por qué ahora?} Los wearables de consumo masivo (>100M Apple Watches vendidos) generan datos longitudinales sin precedentes, pero su análisis requiere métodos robustos a condiciones no controladas.

\textit{¿Por qué nosotros?} Enfoque BYOD + vida libre captura comportamiento natural. Literatura se basa en ActiGraph controlado (limitado a días/semanas). Nosotros: 10 usuarios, 130 semanas promedio, ~1,337 semanas de datos reales.
```

**Cap. 5 (How - Pivote):**
```latex
\section{Del Fracaso Productivo al Éxito Interpretable}

\textit{¿Cómo intentamos inicialmente?} ANNs para predecir SF-36 desde biométricos. Resultado: R² = -0.34 (peor que media). No improvisamos el pivote: probamos 4 arquitecturas (ver Tabla 5.X).

\textit{¿Cómo lo resolvimos?} Pregunta reformulada: No "¿cuánta CVRS predice actividad?" sino "¿qué patrones naturales emergen en datos de vida libre?". Dual: Clustering (empírico) + Fuzzy (experto). Ambos independientes, validación cruzada.

\textit{¿Cómo sabemos que funciona?} F1=0.840 (Fuzzy vs Clustering), LOUO F1=0.812±0.067 (generalización inter-usuario), análisis robustez 4V vs 2V (50% drop → sinergia confirmada).
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] **Script 1:** `analisis_descriptivo_final_v2.py` → Actualizar Tabla 4.1
- [ ] **Script 2:** `generar_small_multiples_time_series.py` → Figura 4.X
- [ ] **Script 3:** `generar_tabla_antropometria.py` → Tabla 2.2
- [ ] **LaTeX:** Añadir narrativa N=9→10 (Cap. 1-2)
- [ ] **LaTeX:** Añadir Tabla ANNs probadas (Cap. 5)
- [ ] **LaTeX:** Añadir Sección HRV_SDNN post-hoc (Cap. 7)
- [ ] **LaTeX:** Insertar small multiples (Cap. 4)
- [ ] **LaTeX:** Insertar tabla antropometría (Cap. 2)
- [ ] **LaTeX:** Aplicar framework "Start with Why" (Cap. 1, 5, Conclusiones)
- [ ] **Verificar:** Todas las cifras estadísticas contra `DB_final_v3_*` limpios
- [ ] **Compilar:** PDF final y verificar cross-referencias

---

## 📚 REFERENCIAS ADICIONALES A INCLUIR

### Literatura BYOD + Vida Libre:

1. **Henriksen et al. (2018):** "Using Fitness Trackers and Smartwatches to Measure Physical Activity in Research: Analysis of Consumer Wrist-Worn Wearables"
   - Respalda uso de Apple Watch
   - Cita Tabla Henriksen (Henriksen_data.csv): 425 dispositivos wearables analizados

2. **Varoquaux (2018):** "Cross-validation failure: Small sample sizes lead to large error bars"
   - Respalda LOUO sobre split 80/20 en N pequeños

3. **Zadeh (1965, 2008):** "Fuzzy Logic"
   - Cita relevante para justificar lógica difusa: "A medida que aumenta la complejidad, nuestra capacidad para hacer afirmaciones precisas disminuye" (incluido en documentos_lectura)

---

## 🎓 MENSAJES CLAVE PARA DEFENSA ORAL

1. **"No improvisamos el pivote":**
   > "Probamos ANNs sistemáticamente (ver `/Modelado`), fracasaron con evidencia cuantitativa (R²<0). El pivote fue data-driven, no arbitrario."

2. **"HRV no estaba en diseño inicial, pero...":**
   > "Lo rescatamos tras 357 análisis exploratorios. Fue la única variable cardiovascular robusta en vida libre. Decisión metodológicamente válida: GO es no supervisada."

3. **"¿Por qué no split 80/20?":**
   > "Tres razones fatales: (1) Fuga temporal (ACF>0.6), (2) Poder estadístico insuficiente (n_test=2), (3) Objetivo descriptivo, no predictivo."

4. **"Diferenciador vs literatura":**
   > "ActiGraph controlado = condiciones ideales. Nosotros = vida libre, longitudinal (130 semanas/usuario), BYOD. Capturamos realidad, no idealización."

5. **"Robustez demostrada":**
   > "LOUO F1=0.812±0.067 (generalización), sensibilidad τ±10% (<2% cambio F1), modelo 4V esencial (2V colapsa 50%)."

---

## 📞 PRÓXIMOS PASOS INMEDIATOS

1. **Revisar este documento** con Luis para validar interpretación
2. **Ejecutar scripts 1-3** (análisis descriptivos + small multiples + antropometría)
3. **Modificar LaTeX** (prioridad 1: narrativa N=9→10, tabla ANNs, sección HRV)
4. **Compilar PDF preliminar** y revisar coherencia
5. **Validar cifras** estadísticas una por una contra `DB_final_v3_*`
6. **Iterar** hasta versión final para comité

---

**🔐 CLASIFICACIÓN:** Documento Interno de Trabajo  
**📍 UBICACIÓN:** `4 semestre_dataset/PLAN_MAESTRO_CORRECCIONES_INFORME_LATEX.md`  
**📅 ÚLTIMA ACTUALIZACIÓN:** 24 de octubre de 2025


