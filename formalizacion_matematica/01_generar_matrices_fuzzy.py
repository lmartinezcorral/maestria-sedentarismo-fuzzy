"""
01_generar_matrices_fuzzy.py
==============================

OBJETIVO:
---------
Generar las matrices B (antecedentes) y C_out (consecuentes) del sistema difuso
de forma explícita y exportarlas en múltiples formatos para documentación.

SALIDAS:
--------
- matriz_B_antecedentes.csv        # Matriz 5×12 (5 reglas × 12 etiquetas)
- matriz_Cout_consecuentes.csv     # Matriz 5×3 (5 reglas × 3 salidas)
- reglas_descripcion.csv            # Descripción textual de cada regla
- reglas_ecuaciones_latex.tex      # Ecuaciones en LaTeX
- pseudocodigo_inference.txt       # Pseudocódigo del proceso de inferencia
- ejemplo_worked_out.csv           # Ejemplo con 10 semanas reales
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import yaml

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cargar configuración de MF
CONFIG_DIR = BASE_DIR.parent / 'fuzzy_config'
MF_CONFIG_FILE = CONFIG_DIR / 'fuzzy_membership_config.yaml'
SCALERS_FILE = CONFIG_DIR / 'feature_scalers.json'

# Cargar datos para ejemplo worked-out
DATA_FILE = BASE_DIR.parent / 'analisis_u' / 'semanal' / 'weekly_consolidado.csv'

print("="*80)
print("GENERACIÓN DE MATRICES FUZZY - FORMALIZACIÓN MATEMÁTICA")
print("="*80)
print(f"Directorio de salida: {OUTPUT_DIR}")
print("")

# ============================================================================
# 1. DEFINIR ORDEN DE ETIQUETAS (12 columnas)
# ============================================================================

print("📋 Definiendo orden de etiquetas...")

# 4 variables × 3 etiquetas = 12 columnas
FEATURES = [
    'Actividad_relativa_p50',
    'Superavit_calorico_basal_p50',
    'HRV_SDNN_p50',
    'Delta_cardiaco_p50'
]

LABELS = ['Baja', 'Media', 'Alta']

# Orden de columnas: Act_B, Act_M, Act_A, Sup_B, Sup_M, Sup_A, HRV_B, HRV_M, HRV_A, DC_B, DC_M, DC_A
COLUMN_NAMES = []
for feat in FEATURES:
    feat_short = feat.replace('_p50', '').replace('_', '')
    if 'Actividad' in feat:
        feat_short = 'Act'
    elif 'Superavit' in feat:
        feat_short = 'Sup'
    elif 'HRV' in feat:
        feat_short = 'HRV'
    elif 'Delta' in feat:
        feat_short = 'DC'

    for label in LABELS:
        COLUMN_NAMES.append(f"{feat_short}_{label}")

print(f"✅ Orden de columnas (12): {COLUMN_NAMES}")
print("")

# ============================================================================
# 2. DEFINIR REGLAS Y CONSTRUIR MATRIZ B
# ============================================================================

print("🔧 Construyendo matriz B (antecedentes)...")

# Reglas actuales del sistema (R1-R5)
RULES = [
    {
        'id': 'R1',
        'descripcion': 'Actividad Baja AND Superávit Bajo → Sedentarismo Alto',
        'antecedentes': ['Act_Baja', 'Sup_Baja'],
        'consecuente': 'Alto',
        'peso': 1.0,
        'justificacion': 'Inactividad física combinada con bajo gasto energético indica sedentarismo severo'
    },
    {
        'id': 'R2',
        'descripcion': 'Actividad Alta AND Superávit Alto → Sedentarismo Bajo',
        'antecedentes': ['Act_Alta', 'Sup_Alta'],
        'consecuente': 'Bajo',
        'peso': 1.0,
        'justificacion': 'Alta actividad y alto gasto energético indica estilo de vida activo'
    },
    {
        'id': 'R3',
        'descripcion': 'HRV Baja AND Delta Cardíaco Bajo → Sedentarismo Alto',
        'antecedentes': ['HRV_Baja', 'DC_Baja'],
        'consecuente': 'Alto',
        'peso': 1.0,
        'justificacion': 'Pobre variabilidad cardíaca y respuesta cardiovascular baja indica desacondicionamiento'
    },
    {
        'id': 'R4',
        'descripcion': 'Actividad Media AND HRV Media → Sedentarismo Medio',
        'antecedentes': ['Act_Media', 'HRV_Media'],
        'consecuente': 'Medio',
        'peso': 1.0,
        'justificacion': 'Estado intermedio balanceado entre actividad y función autonómica'
    },
    {
        'id': 'R5',
        'descripcion': 'Actividad Baja AND Superávit Medio → Sedentarismo Medio-Alto',
        'antecedentes': ['Act_Baja', 'Sup_Media'],
        'consecuente': 'Alto',
        'peso': 0.7,
        'justificacion': 'Baja actividad parcialmente compensada por gasto moderado (peso reducido)'
    }
]

# Construir matriz B (5×12)
B = np.zeros((len(RULES), len(COLUMN_NAMES)), dtype=int)

for i, rule in enumerate(RULES):
    for antecedente in rule['antecedentes']:
        # Parsear antecedente: 'Act_Baja' → columna 'Act_Baja'
        col_name = antecedente.replace('Baja', 'Baja').replace(
            'Media', 'Media').replace('Alta', 'Alta')
        if col_name in COLUMN_NAMES:
            j = COLUMN_NAMES.index(col_name)
            B[i, j] = 1

# Crear DataFrame
df_B = pd.DataFrame(B, columns=COLUMN_NAMES, index=[r['id'] for r in RULES])

# Guardar
b_file = OUTPUT_DIR / 'matriz_B_antecedentes.csv'
df_B.to_csv(b_file)
print(f"✅ Guardado: {b_file.name}")
print(f"   Forma: {df_B.shape} (5 reglas × 12 etiquetas)")
print("")

# ============================================================================
# 3. CONSTRUIR MATRIZ C_out (CONSECUENTES)
# ============================================================================

print("🔧 Construyendo matriz C_out (consecuentes)...")

# Columnas: Sed_Bajo, Sed_Medio, Sed_Alto
CONSECUENTES = ['Bajo', 'Medio', 'Alto']

C_out = np.zeros((len(RULES), len(CONSECUENTES)), dtype=float)

for i, rule in enumerate(RULES):
    cons = rule['consecuente']
    peso = rule['peso']
    j = CONSECUENTES.index(cons)
    C_out[i, j] = peso

# Crear DataFrame
df_Cout = pd.DataFrame(C_out, columns=[f'Sed_{c}' for c in CONSECUENTES], index=[
                       r['id'] for r in RULES])

# Guardar
cout_file = OUTPUT_DIR / 'matriz_Cout_consecuentes.csv'
df_Cout.to_csv(cout_file)
print(f"✅ Guardado: {cout_file.name}")
print(f"   Forma: {df_Cout.shape} (5 reglas × 3 salidas)")
print("")

# ============================================================================
# 4. EXPORTAR DESCRIPCIÓN DE REGLAS
# ============================================================================

print("📝 Exportando descripción de reglas...")

df_reglas = pd.DataFrame(RULES)
reglas_file = OUTPUT_DIR / 'reglas_descripcion.csv'
df_reglas.to_csv(reglas_file, index=False)
print(f"✅ Guardado: {reglas_file.name}")
print("")

# ============================================================================
# 5. GENERAR ECUACIONES LATEX
# ============================================================================

print("📐 Generando ecuaciones LaTeX...")

latex_content = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage[margin=2cm]{geometry}

\title{Formalización Matemática del Sistema Difuso de Sedentarismo}
\author{Luis Ángel Martínez - UACH}
\date{\today}

\begin{document}
\maketitle

\section{Notación}

Sea la unidad de análisis la \textbf{semana} $i \in \{1, \dots, n\}$. Para cada semana construimos el vector de rasgos normalizados a $[0,1]$:

\[
\mathbf{x}_i = \begin{bmatrix}
\text{Act}_{p50} \\
\text{Sup}_{p50} \\
\text{HRV}_{p50} \\
\Delta\text{Card}_{p50}
\end{bmatrix}_i \in [0,1]^4
\]

\section{Funciones de Membresía}

Para cada variable $x_{ij}$ definimos tres etiquetas lingüísticas: \{Baja, Media, Alta\} con funciones de membresía \textbf{triangulares}:

\[
\mu^{\text{Baja}}(x; a, b, c), \quad \mu^{\text{Media}}(x; a, b, c), \quad \mu^{\text{Alta}}(x; a, b, c)
\]

donde la triangular estándar es:

\[
\mu(x; a, b, c) = \begin{cases}
0, & x \le a \text{ o } x \ge c \\
\frac{x - a}{b - a}, & a < x < b \\
\frac{c - x}{c - b}, & b \le x < c
\end{cases}
\]

Los parámetros $(a, b, c)$ se determinan por percentiles:
\begin{itemize}
    \item Baja: $(p_{10}, p_{25}, p_{40})$
    \item Media: $(p_{35}, p_{50}, p_{65})$
    \item Alta: $(p_{60}, p_{80}, p_{90})$
\end{itemize}

\section{Vector de Membresías}

Para cada semana $i$, el vector de membresías es:

\[
\boldsymbol{\mu}_i = \begin{bmatrix}
\mu_{\text{Act}_B}, \mu_{\text{Act}_M}, \mu_{\text{Act}_A}, \\
\mu_{\text{Sup}_B}, \mu_{\text{Sup}_M}, \mu_{\text{Sup}_A}, \\
\mu_{\text{HRV}_B}, \mu_{\text{HRV}_M}, \mu_{\text{HRV}_A}, \\
\mu_{\text{DC}_B}, \mu_{\text{DC}_M}, \mu_{\text{DC}_A}
\end{bmatrix}_i \in [0,1]^{12}
\]

\section{Base de Reglas}

Definimos $R = 5$ reglas (conjunciones de antecedentes $\to$ consecuente):

\subsection*{Matriz de Antecedentes $\mathbf{B} \in \{0,1\}^{5 \times 12}$}

\[
\mathbf{B} = \begin{bmatrix}
1 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ % R1: Act_B, Sup_B
0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ % R2: Act_A, Sup_A
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 \\ % R3: HRV_B, DC_B
0 & 1 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ % R4: Act_M, HRV_M
1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0   % R5: Act_B, Sup_M
\end{bmatrix}
\]

Columnas: $[\text{Act}_B, \text{Act}_M, \text{Act}_A, \text{Sup}_B, \text{Sup}_M, \text{Sup}_A, \text{HRV}_B, \text{HRV}_M, \text{HRV}_A, \text{DC}_B, \text{DC}_M, \text{DC}_A]$

\subsection*{Matriz de Consecuentes $\mathbf{C}_{\text{out}} \in \mathbb{R}^{5 \times 3}$}

\[
\mathbf{C}_{\text{out}} = \begin{bmatrix}
0 & 0 & 1.0 \\ % R1 -> Alto
1.0 & 0 & 0 \\ % R2 -> Bajo
0 & 0 & 1.0 \\ % R3 -> Alto
0 & 1.0 & 0 \\ % R4 -> Medio
0 & 0 & 0.7   % R5 -> Alto (peso 0.7)
\end{bmatrix}
\]

Columnas: $[\text{Sed}_{\text{Bajo}}, \text{Sed}_{\text{Medio}}, \text{Sed}_{\text{Alto}}]$

\section{Inferencia Mamdani}

\subsection{Activación (AND = mín)}

Para cada regla $r$, calculamos la activación:

\[
w_{i,r} = \min \{ \mu_{i,j} \mid B_{rj} = 1 \}
\]

\subsection{Agregación (suma ponderada)}

\[
\mathbf{s}_i = \mathbf{w}_i^\top \mathbf{C}_{\text{out}} = \begin{bmatrix}
s_{i,\text{Bajo}} \\
s_{i,\text{Medio}} \\
s_{i,\text{Alto}}
\end{bmatrix}
\]

\subsection{Defuzzificación (centroide discreto)}

\[
\text{score}_i = \frac{0.2 \cdot s_{i,\text{Bajo}} + 0.5 \cdot s_{i,\text{Medio}} + 0.8 \cdot s_{i,\text{Alto}}}{s_{i,\text{Bajo}} + s_{i,\text{Medio}} + s_{i,\text{Alto}}}
\]

\subsection{Binarización}

\[
\hat{y}_i = \mathbb{1}[\text{score}_i \ge \tau], \quad \tau = 0.30
\]

\section{Pseudocódigo}

\begin{verbatim}
Input: X ∈ ℝ^{n×4} (weekly features, normalized)
Output: scores ∈ [0,1]^n, labels ∈ {0,1}^n

1. Para cada semana i:
   1.1. Fuzzificar: μ_i ← fuzzify(x_i; MF_params)
   1.2. Activar reglas: w_i[r] ← min(μ_i[j] : B[r,j]=1), r=1..5
   1.3. Agregar: s_i ← w_i^T · C_out
   1.4. Defuzzificar: score_i ← (0.2·s_B + 0.5·s_M + 0.8·s_A) / ||s_i||_1
   1.5. Binarizar: ŷ_i ← [score_i ≥ τ]
2. Retornar: scores, labels
\end{verbatim}

\end{document}
"""

latex_file = OUTPUT_DIR / 'reglas_ecuaciones_latex.tex'
with open(latex_file, 'w', encoding='utf-8') as f:
    f.write(latex_content)
print(f"✅ Guardado: {latex_file.name}")
print("")

# ============================================================================
# 6. GENERAR PSEUDOCÓDIGO DETALLADO
# ============================================================================

print("💻 Generando pseudocódigo detallado...")

pseudocode = """
PSEUDOCÓDIGO: SISTEMA DE INFERENCIA DIFUSA MAMDANI
===================================================

ENTRADA:
    - X: matriz n×4 de features semanales normalizadas [0,1]
      (Actividad_p50, Superávit_p50, HRV_p50, DeltaCard_p50)
    - MF_params: parámetros de funciones de membresía (percentiles)
    - B: matriz 5×12 de antecedentes (binaria)
    - C_out: matriz 5×3 de consecuentes (real, con pesos)
    - τ: umbral de binarización (default=0.30)

SALIDA:
    - scores: vector n×1 de scores de sedentarismo [0,1]
    - labels: vector n×1 de etiquetas binarias {0=Bajo, 1=Alto}

ALGORITMO:

1. FUZZIFICACIÓN
   PARA cada semana i en 1..n:
       PARA cada feature j en 1..4:
           x_ij ← X[i, j]  # valor normalizado [0,1]
           
           # Calcular 3 membresías por feature
           μ_Baja[j] ← triangular(x_ij, MF_params[j]['Baja'])
           μ_Media[j] ← triangular(x_ij, MF_params[j]['Media'])
           μ_Alta[j] ← triangular(x_ij, MF_params[j]['Alta'])
       FIN PARA
       
       # Concatenar en vector μ_i ∈ [0,1]^12
       μ_i ← [μ_Baja[1], μ_Media[1], μ_Alta[1], ..., μ_Alta[4]]
   FIN PARA

2. ACTIVACIÓN DE REGLAS (Mamdani AND = mín)
   PARA cada semana i en 1..n:
       PARA cada regla r en 1..5:
           # Encontrar índices de antecedentes activos
           indices ← {j : B[r,j] = 1}
           
           # Activación = mínimo de membresías de antecedentes
           w_i[r] ← min{ μ_i[j] : j ∈ indices }
       FIN PARA
   FIN PARA

3. AGREGACIÓN (suma ponderada de consecuentes)
   PARA cada semana i en 1..n:
       # Producto matricial: w_i^T · C_out
       s_i ← [0, 0, 0]  # [Sed_Bajo, Sed_Medio, Sed_Alto]
       
       PARA cada regla r en 1..5:
           PARA cada salida k en 1..3:
               s_i[k] ← s_i[k] + w_i[r] · C_out[r, k]
           FIN PARA
       FIN PARA
       
       # s_i contiene activaciones agregadas por salida
   FIN PARA

4. DEFUZZIFICACIÓN (centroide discreto)
   PARA cada semana i en 1..n:
       SI ||s_i||_1 > 0 ENTONCES
           # Centroide con niveles [0.2, 0.5, 0.8]
           numerador ← 0.2·s_i[Bajo] + 0.5·s_i[Medio] + 0.8·s_i[Alto]
           denominador ← s_i[Bajo] + s_i[Medio] + s_i[Alto]
           score_i ← numerador / denominador
       SINO
           score_i ← 0.0  # caso degenerado (no se activa ninguna regla)
       FIN SI
   FIN PARA

5. BINARIZACIÓN
   PARA cada semana i en 1..n:
       SI score_i ≥ τ ENTONCES
           label_i ← 1  # Alto Sedentarismo
       SINO
           label_i ← 0  # Bajo Sedentarismo
       FIN SI
   FIN PARA

6. RETORNAR
   RETORNAR (scores, labels)

FIN ALGORITMO

---

COMPLEJIDAD:
    - Fuzzificación: O(n · 4 · 3) = O(12n)
    - Activación: O(n · 5 · 2_avg) = O(10n)  # 2_avg = antecedentes promedio por regla
    - Agregación: O(n · 5 · 3) = O(15n)
    - Defuzzificación: O(n)
    - Binarización: O(n)
    TOTAL: O(38n) → O(n)  # Lineal en número de semanas

---

FUNCIONES AUXILIARES:

FUNCIÓN triangular(x, params):
    # params = (a, b, c)  donde a < b < c
    a, b, c ← params
    
    SI x ≤ a O x ≥ c ENTONCES
        RETORNAR 0
    SINO SI a < x < b ENTONCES
        RETORNAR (x - a) / (b - a)
    SINO  # b ≤ x < c
        RETORNAR (c - x) / (c - b)
    FIN SI
FIN FUNCIÓN

---

EJEMPLO WORKED-OUT (ver archivo ejemplo_worked_out.csv)
"""

pseudo_file = OUTPUT_DIR / 'pseudocodigo_inference.txt'
with open(pseudo_file, 'w', encoding='utf-8') as f:
    f.write(pseudocode)
print(f"✅ Guardado: {pseudo_file.name}")
print("")

# ============================================================================
# 7. GENERAR EJEMPLO WORKED-OUT (10 SEMANAS REALES)
# ============================================================================

print("🔬 Generando ejemplo worked-out con 10 semanas reales...")

# Cargar datos
if DATA_FILE.exists():
    df_weekly = pd.read_csv(DATA_FILE)

    # Cargar configuración MF
    with open(MF_CONFIG_FILE, 'r') as f:
        mf_config = yaml.safe_load(f)

    with open(SCALERS_FILE, 'r') as f:
        scalers = json.load(f)

    # Seleccionar 10 semanas aleatorias (seed fijo para reproducibilidad)
    np.random.seed(42)
    sample_indices = np.random.choice(
        len(df_weekly), size=min(10, len(df_weekly)), replace=False)
    df_sample = df_weekly.iloc[sample_indices].copy()

    # Resetear índice
    df_sample = df_sample.reset_index(drop=True)

    # Normalizar features
    for feat in FEATURES:
        if feat in df_sample.columns and feat in scalers:
            min_val = scalers[feat]['min']
            max_val = scalers[feat]['max']
            df_sample[f'{feat}_norm'] = (
                df_sample[feat] - min_val) / (max_val - min_val)
            df_sample[f'{feat}_norm'] = df_sample[f'{feat}_norm'].clip(0, 1)

    # Función triangular
    def triangular(x, a, b, c):
        if x <= a or x >= c:
            return 0.0
        elif a < x < b:
            return (x - a) / (b - a) if (b - a) > 0 else 0.0
        else:  # b <= x < c
            return (c - x) / (c - b) if (c - b) > 0 else 0.0

    # Calcular membresías para cada semana
    worked_out_rows = []

    for idx, row in df_sample.iterrows():
        semana_data = {
            'semana_idx': idx,
            'usuario_id': row.get('usuario_id', 'NA'),
            'semana_inicio': row.get('semana_inicio', 'NA')
        }

        # Valores normalizados
        for feat in FEATURES:
            feat_norm = f'{feat}_norm'
            if feat_norm in df_sample.columns:
                semana_data[f'{feat}_valor'] = row[feat]
                semana_data[f'{feat}_norm'] = row[feat_norm]

        # Calcular membresías
        mu_vector = []
        for feat in FEATURES:
            feat_norm = f'{feat}_norm'
            if feat_norm in df_sample.columns and feat in mf_config:
                x = row[feat_norm]
                mf = mf_config[feat]

                for label in ['Baja', 'Media', 'Alta']:
                    if label in mf:
                        a, b, c = mf[label]['values']
                        mu = triangular(x, a, b, c)
                        mu_vector.append(mu)

                        feat_short = feat.replace('_p50', '').replace('_', '')
                        if 'Actividad' in feat:
                            feat_short = 'Act'
                        elif 'Superavit' in feat:
                            feat_short = 'Sup'
                        elif 'HRV' in feat:
                            feat_short = 'HRV'
                        elif 'Delta' in feat:
                            feat_short = 'DC'

                        semana_data[f'mu_{feat_short}_{label}'] = mu

        # Activación de reglas
        w = np.zeros(5)
        for r, rule in enumerate(RULES):
            # Extraer membresías de antecedentes
            mus_ant = []
            for ant in rule['antecedentes']:
                col_name = f"mu_{ant.replace('Baja', 'Baja').replace('Media', 'Media').replace('Alta', 'Alta')}"
                if col_name in semana_data:
                    mus_ant.append(semana_data[col_name])

            if mus_ant:
                w[r] = min(mus_ant)
                semana_data[f'w_{rule["id"]}'] = w[r]

        # Agregación
        s = np.dot(w, C_out)
        semana_data['s_Bajo'] = s[0]
        semana_data['s_Medio'] = s[1]
        semana_data['s_Alto'] = s[2]

        # Defuzzificación
        s_sum = s.sum()
        if s_sum > 0:
            score = (0.2 * s[0] + 0.5 * s[1] + 0.8 * s[2]) / s_sum
        else:
            score = 0.0

        semana_data['Sedentarismo_score'] = score
        semana_data['Sedentarismo_label'] = 1 if score >= 0.30 else 0

        worked_out_rows.append(semana_data)

    df_worked_out = pd.DataFrame(worked_out_rows)

    # Guardar
    worked_out_file = OUTPUT_DIR / 'ejemplo_worked_out.csv'
    df_worked_out.to_csv(worked_out_file, index=False)
    print(f"✅ Guardado: {worked_out_file.name}")
    print(f"   Semanas procesadas: {len(df_worked_out)}")
    print("")

else:
    print(f"⚠️  No se encontró {DATA_FILE.name}, omitiendo ejemplo worked-out")
    print("")

# ============================================================================
# 8. RESUMEN FINAL
# ============================================================================

print("="*80)
print("✅ FORMALIZACIÓN MATEMÁTICA COMPLETADA")
print("="*80)
print(f"\n📂 Archivos generados en: {OUTPUT_DIR}")
print("   1. matriz_B_antecedentes.csv (5×12)")
print("   2. matriz_Cout_consecuentes.csv (5×3)")
print("   3. reglas_descripcion.csv")
print("   4. reglas_ecuaciones_latex.tex")
print("   5. pseudocodigo_inference.txt")
print("   6. ejemplo_worked_out.csv (10 semanas)")
print("")
print("📌 PRÓXIMOS PASOS:")
print("   - Compilar reglas_ecuaciones_latex.tex → PDF (pdflatex)")
print("   - Revisar ejemplo_worked_out.csv para validación")
print("   - Incluir matrices en documento de tesis")
print("")



