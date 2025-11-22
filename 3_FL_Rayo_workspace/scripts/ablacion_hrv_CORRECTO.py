#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ABLACIÓN HRV - MÉTODO CORRECTO
================================
Fecha: 13 de Noviembre de 2025, 21:25:00
Investigador: Luis Angel Martinez Corral

OBJETIVO:
---------
Re-ejecutar ablación HRV usando el método CORRECTO del script original:
- Usar firing_R1, firing_R2, firing_R5 del fuzzy_output.csv
- NO recalcular membresías
- Comparar F1 modelo 4V vs 2V
"""

import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, matthews_corrcoef
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("ABLACION HRV - METODO CORRECTO")
print("="*80)
print()

# ============================================================================
# 1. CARGAR DATOS
# ============================================================================

print("[1/5] Cargando datos...")

RUTA_BASE = "../analisis_u"

df_fuzzy = pd.read_csv(f"{RUTA_BASE}/fuzzy/fuzzy_output.csv")
df_cluster = pd.read_csv(f"{RUTA_BASE}/clustering/cluster_assignments.csv")

# Merge
df = df_fuzzy.merge(
    df_cluster[['usuario_id', 'semana_inicio', 'cluster']],
    on=['usuario_id', 'semana_inicio'],
    how='inner'
)

print(f"   [OK] Semanas cargadas: {len(df):,}")
print(f"   [OK] Usuarios: {df['usuario_id'].nunique()}")
print()

# Verificar columnas firing_R
firing_cols = [c for c in df.columns if 'firing_R' in c]
print(f"   [OK] Columnas firing_R encontradas: {firing_cols}")
print()

# ============================================================================
# 2. MODELO COMPLETO (4V) - SISTEMA ORIGINAL
# ============================================================================

print("="*80)
print("[2/5] MODELO COMPLETO (4V)")
print("="*80)
print()

# Score completo (ya calculado en fuzzy_output.csv)
scores_4v = df['Sedentarismo_score'].values
y_true = df['cluster'].values

# Buscar tau optimo para 4V
tau_grid = np.arange(0.10, 0.61, 0.01)
resultados_4v = []

for tau in tau_grid:
    y_pred = (scores_4v >= tau).astype(int)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    resultados_4v.append({'tau': tau, 'f1': f1})

df_tau_4v = pd.DataFrame(resultados_4v)
idx_max = df_tau_4v['f1'].idxmax()
tau_4v = df_tau_4v.loc[idx_max, 'tau']
f1_max_4v = df_tau_4v.loc[idx_max, 'f1']

print(f"Tau optimo (4V): {tau_4v:.2f}")
print(f"F1 maximo (4V): {f1_max_4v:.4f}")
print()

# Metricas con tau optimo
y_pred_4v = (scores_4v >= tau_4v).astype(int)

metricas_4v = {
    'accuracy': accuracy_score(y_true, y_pred_4v),
    'precision': precision_score(y_true, y_pred_4v, zero_division=0),
    'recall': recall_score(y_true, y_pred_4v, zero_division=0),
    'f1': f1_score(y_true, y_pred_4v, zero_division=0),
    'mcc': matthews_corrcoef(y_true, y_pred_4v)
}

print("Metricas Modelo Completo (4V):")
for k, v in metricas_4v.items():
    print(f"   {k.capitalize()}: {v:.4f}")
print()

# ============================================================================
# 3. MODELO REDUCIDO (2V) - MÉTODO CORRECTO
# ============================================================================

print("="*80)
print("[3/5] MODELO REDUCIDO (2V) - METODO CORRECTO")
print("="*80)
print()

print("Calculando score reducido usando firing_R1, firing_R2, firing_R5...")
print("(Excluye R3 [HRV+Delta] y R4 [Act_Media+HRV_Media])")
print()

# Función del script original
def calcular_score_reducido_2v(row):
    """
    Modelo reducido usando solo R1, R2, R5 (sin HRV ni Delta)
    
    Agregación:
    - s_Alto = firing_R1 + (firing_R5 * 0.7)
    - s_Bajo = firing_R2
    - s_Medio = 0 (R4 excluida)
    
    Defuzzificación (centroide):
    score = (0.2*s_Bajo + 0.5*s_Medio + 0.8*s_Alto) / (s_Bajo + s_Medio + s_Alto)
    """
    s_bajo = row['firing_R2']
    s_medio = 0.0  # R4 excluida (usa HRV)
    s_alto = row['firing_R1'] + (row['firing_R5'] * 0.7)
    
    s_total = s_bajo + s_medio + s_alto
    
    if s_total > 0:
        score = (0.2 * s_bajo + 0.5 * s_medio + 0.8 * s_alto) / s_total
    else:
        score = 0.0
    
    return score

# Aplicar
df['Sedentarismo_score_2V'] = df.apply(calcular_score_reducido_2v, axis=1)
scores_2v = df['Sedentarismo_score_2V'].values

print(f"   [OK] Score 2V calculado")
print(f"   Score medio (2V): {scores_2v.mean():.3f} +/- {scores_2v.std():.3f}")
print()

# Buscar tau optimo para 2V
resultados_2v = []

for tau in tau_grid:
    y_pred = (scores_2v >= tau).astype(int)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    resultados_2v.append({'tau': tau, 'f1': f1})

df_tau_2v = pd.DataFrame(resultados_2v)
idx_max = df_tau_2v['f1'].idxmax()
tau_2v = df_tau_2v.loc[idx_max, 'tau']
f1_max_2v = df_tau_2v.loc[idx_max, 'f1']

print(f"Tau optimo (2V): {tau_2v:.2f}")
print(f"F1 maximo (2V): {f1_max_2v:.4f}")
print()

# Metricas con tau optimo
y_pred_2v = (scores_2v >= tau_2v).astype(int)

metricas_2v = {
    'accuracy': accuracy_score(y_true, y_pred_2v),
    'precision': precision_score(y_true, y_pred_2v, zero_division=0),
    'recall': recall_score(y_true, y_pred_2v, zero_division=0),
    'f1': f1_score(y_true, y_pred_2v, zero_division=0),
    'mcc': matthews_corrcoef(y_true, y_pred_2v)
}

print("Metricas Modelo Reducido (2V):")
for k, v in metricas_2v.items():
    print(f"   {k.capitalize()}: {v:.4f}")
print()

# ============================================================================
# 4. COMPARACIÓN
# ============================================================================

print("="*80)
print("[4/5] COMPARACION FINAL")
print("="*80)
print()

diff_f1 = metricas_4v['f1'] - metricas_2v['f1']
diff_f1_pct = (diff_f1 / metricas_4v['f1']) * 100

print("MODELO COMPLETO (4V):")
print(f"   F1-Score: {metricas_4v['f1']:.4f}")
print(f"   Tau optimo: {tau_4v:.2f}")
print()

print("MODELO REDUCIDO (2V):")
print(f"   F1-Score: {metricas_2v['f1']:.4f}")
print(f"   Tau optimo: {tau_2v:.2f}")
print()

print("ABLACION (4V -> 2V):")
print(f"   Delta F1: {diff_f1:.4f}")
print(f"   Caida porcentual: {diff_f1_pct:.1f}%")
print()

if abs(diff_f1_pct - 50) < 5:
    print("   >> CONSISTENTE CON LOG ORIGINAL (-50%)")
elif abs(diff_f1_pct - 9.1) < 5:
    print("   >> CONSISTENTE CON REPORTE ADES (-9.1%)")
elif abs(diff_f1_pct) < 1:
    print("   >> CAIDA MINIMA (< 1%)")
else:
    print(f"   >> CAIDA REAL: {diff_f1_pct:.1f}%")
print()

# ============================================================================
# 5. VERIFICACIÓN CON LOG ORIGINAL
# ============================================================================

print("="*80)
print("[5/5] VERIFICACION CON LOG ORIGINAL")
print("="*80)
print()

print("LOG ORIGINAL (20-Oct-2025):")
print("   F1 Completo (4V): 0.840")
print("   F1 Reducido (2V): 0.420")
print("   Caida: -50.0%")
print()

print("RE-EJECUCIÓN ACTUAL (13-Nov-2025):")
print(f"   F1 Completo (4V): {metricas_4v['f1']:.3f}")
print(f"   F1 Reducido (2V): {metricas_2v['f1']:.3f}")
print(f"   Caida: {diff_f1_pct:.1f}%")
print()

# Tolerancia
if abs(metricas_4v['f1'] - 0.840) < 0.01 and abs(metricas_2v['f1'] - 0.420) < 0.01:
    print("   >> CONFIRMADO: Resultados identicos al log original")
    print("   >> ABLACION -50% CERTIFICADA")
else:
    print(f"   >> DIFERENCIA detectada:")
    print(f"      F1 (4V): log=0.840 vs actual={metricas_4v['f1']:.3f} (Δ={metricas_4v['f1']-0.840:.3f})")
    print(f"      F1 (2V): log=0.420 vs actual={metricas_2v['f1']:.3f} (Δ={metricas_2v['f1']-0.420:.3f})")
print()

# Guardar resultados
import os
output_dir = os.path.join(os.path.dirname(__file__), "..", "resultados")
os.makedirs(output_dir, exist_ok=True)

resultados = pd.DataFrame({
    'Modelo': ['Completo_4V', 'Reducido_2V'],
    'F1': [metricas_4v['f1'], metricas_2v['f1']],
    'Accuracy': [metricas_4v['accuracy'], metricas_2v['accuracy']],
    'Precision': [metricas_4v['precision'], metricas_2v['precision']],
    'Recall': [metricas_4v['recall'], metricas_2v['recall']],
    'MCC': [metricas_4v['mcc'], metricas_2v['mcc']],
    'Tau_optimo': [tau_4v, tau_2v]
})

resultados.to_csv(f"{output_dir}/ablacion_hrv_CORRECTO.csv", index=False)

print("="*80)
print("ABLACION COMPLETADA")
print("="*80)
print()
print(f"[OK] Resultados guardados: resultados/ablacion_hrv_CORRECTO.csv")
print()

