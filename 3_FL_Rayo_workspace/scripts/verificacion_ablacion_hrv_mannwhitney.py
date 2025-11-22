#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICACIÓN TÉCNICA: Ablación HRV + Mann-Whitney
==================================================
Investigador: Luis Angel Martinez Corral
Fecha: 13 de Noviembre de 2025, 20:58:37
Tarea: Resolver verificaciones pendientes #2 y #3

OBJETIVO:
---------
1. Calcular ablación HRV (F1 con 4 vars vs F1 sin HRV)
2. Calcular p-value Mann-Whitney para HRV entre clusters
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("VERIFICACION TECNICA: Ablacion HRV + Mann-Whitney")
print("="*80)
print()

# ============================================================================
# CARGA DE DATOS
# ============================================================================

print("[1/4] Cargando datos...")

RUTA_BASE = "../analisis_u"

# Datos semanales con todas las variables
df_weekly = pd.read_csv(f"{RUTA_BASE}/semanal/cluster_inputs_weekly.csv")

# Asignaciones de cluster (Ground Truth Operativa)
df_cluster = pd.read_csv(f"{RUTA_BASE}/clustering/cluster_assignments.csv")

# Salida fuzzy
df_fuzzy = pd.read_csv(f"{RUTA_BASE}/fuzzy/fuzzy_output.csv")

# Merge
df = df_cluster.merge(
    df_fuzzy[['usuario_id', 'semana_inicio', 'Sedentarismo_score']],
    on=['usuario_id', 'semana_inicio'],
    how='inner'
)

print(f"   [OK] Semanas cargadas: {len(df):,}")
print(f"   [OK] Usuarios: {df['usuario_id'].nunique()}")
print()

# Umbral óptimo del sistema (del log operativo)
TAU = 0.30

# ============================================================================
# VERIFICACIÓN #2: ABLACIÓN HRV
# ============================================================================

print("="*80)
print("VERIFICACION #2: ABLACION HRV")
print("="*80)
print()

# Necesitamos recalcular el fuzzy score SIN HRV
# Para esto, cargaremos las membresías y simularemos el sistema sin HRV

# Cargar membresías de todas las variables
memb_cols_actividad = [c for c in df_fuzzy.columns if 'Actividad_relativa' in c and '_memb' in c]
memb_cols_superavit = [c for c in df_fuzzy.columns if 'Superavit_calorico' in c and '_memb' in c]
memb_cols_hrv = [c for c in df_fuzzy.columns if 'HRV_SDNN' in c and '_memb' in c]
memb_cols_delta = [c for c in df_fuzzy.columns if 'Delta_cardiaco' in c and '_memb' in c]

# Merge membresías
df = df.merge(
    df_fuzzy[['usuario_id', 'semana_inicio'] + memb_cols_actividad + memb_cols_superavit + 
             memb_cols_hrv + memb_cols_delta],
    on=['usuario_id', 'semana_inicio'],
    how='left'
)

print("Membresías cargadas:")
print(f"   Actividad: {len(memb_cols_actividad)} columnas")
print(f"   Superávit: {len(memb_cols_superavit)} columnas")
print(f"   HRV: {len(memb_cols_hrv)} columnas")
print(f"   Delta: {len(memb_cols_delta)} columnas")
print()

# ===========================================================================
# SISTEMA FUZZY SIMPLIFICADO (SIN HRV y Delta)
# ===========================================================================

print("Calculando score fuzzy sin HRV (solo Actividad + Superávit)...")
print()

# Reglas simplificadas (solo con Actividad y Superávit):
# R1: Actividad Baja AND Superávit Bajo → Sedentarismo Alto
# R2: Actividad Alta AND Superávit Alto → Sedentarismo Bajo

def fuzzy_sin_hrv_delta(row):
    """
    Sistema fuzzy simplificado con solo 2 variables:
    - Actividad_relativa_p50
    - Superavit_calorico_basal_p50
    """
    # Obtener membresías
    act_baja = row.get('Actividad_relativa_p50_Baja_memb', 0)
    act_media = row.get('Actividad_relativa_p50_Media_memb', 0)
    act_alta = row.get('Actividad_relativa_p50_Alta_memb', 0)
    
    sup_bajo = row.get('Superavit_calorico_basal_p50_Baja_memb', 0)
    sup_medio = row.get('Superavit_calorico_basal_p50_Media_memb', 0)
    sup_alto = row.get('Superavit_calorico_basal_p50_Alta_memb', 0)
    
    # Reglas (usando min para AND, max para OR)
    # R1: Actividad Baja AND Superávit Bajo → Sedentarismo Alto (1.0)
    r1 = min(act_baja, sup_bajo)
    
    # R2: Actividad Alta AND Superávit Alto → Sedentarismo Bajo (0.0)
    r2 = min(act_alta, sup_alto)
    
    # R3: Actividad Media AND Superávit Medio → Sedentarismo Medio (0.5)
    r3 = min(act_media, sup_medio)
    
    # R4: Actividad Baja AND Superávit Medio → Sedentarismo Medio-Alto (0.7)
    r4 = min(act_baja, sup_medio)
    
    # Defuzzificación (promedio ponderado)
    numerador = r1 * 1.0 + r2 * 0.0 + r3 * 0.5 + r4 * 0.7
    denominador = r1 + r2 + r3 + r4
    
    if denominador > 0:
        return numerador / denominador
    else:
        return 0.5  # Default medio si no hay activación

# Aplicar sistema sin HRV
df['Sedentarismo_score_SIN_HRV'] = df.apply(fuzzy_sin_hrv_delta, axis=1)

print(f"   [OK] Score sin HRV calculado")
print(f"   Score medio sin HRV: {df['Sedentarismo_score_SIN_HRV'].mean():.3f} +/- {df['Sedentarismo_score_SIN_HRV'].std():.3f}")
print()

# Clasificación con umbral
df['pred_completo'] = (df['Sedentarismo_score'] >= TAU).astype(int)
df['pred_sin_hrv'] = (df['Sedentarismo_score_SIN_HRV'] >= TAU).astype(int)
df['cluster_gt'] = df['cluster']

# Calcular métricas
f1_completo = f1_score(df['cluster_gt'], df['pred_completo'])
f1_sin_hrv = f1_score(df['cluster_gt'], df['pred_sin_hrv'])

acc_completo = accuracy_score(df['cluster_gt'], df['pred_completo'])
acc_sin_hrv = accuracy_score(df['cluster_gt'], df['pred_sin_hrv'])

prec_completo = precision_score(df['cluster_gt'], df['pred_completo'])
prec_sin_hrv = precision_score(df['cluster_gt'], df['pred_sin_hrv'])

rec_completo = recall_score(df['cluster_gt'], df['pred_completo'])
rec_sin_hrv = recall_score(df['cluster_gt'], df['pred_sin_hrv'])

# Calcular caída
caida_f1 = f1_completo - f1_sin_hrv
caida_f1_pct = (caida_f1 / f1_completo) * 100

print("="*80)
print("RESULTADOS ABLACIÓN HRV:")
print("="*80)
print()
print("MODELO COMPLETO (4 variables: Actividad, Superávit, HRV, Delta):")
print(f"   F1-Score: {f1_completo:.4f}")
print(f"   Accuracy: {acc_completo:.4f}")
print(f"   Precision: {prec_completo:.4f}")
print(f"   Recall: {rec_completo:.4f}")
print()
print("MODELO SIN HRV (2 variables: Actividad, Superávit):")
print(f"   F1-Score: {f1_sin_hrv:.4f}")
print(f"   Accuracy: {acc_sin_hrv:.4f}")
print(f"   Precision: {prec_sin_hrv:.4f}")
print(f"   Recall: {rec_sin_hrv:.4f}")
print()
print("ABLACIÓN (IMPACTO DE QUITAR HRV + DELTA):")
print(f"   Caída F1: {caida_f1:.4f} ({caida_f1_pct:.1f}%)")
print(f"   De F1 = {f1_completo:.4f} a F1 = {f1_sin_hrv:.4f}")
print()

if abs(caida_f1_pct - 50) < 10:
    print("   >> CONSISTENTE CON DOCUMENTACIÓN (-50%)")
elif abs(caida_f1_pct - 9.1) < 5:
    print("   >> CONSISTENTE CON REPORTE ADES (-9.1%)")
else:
    print(f"   >> VALOR DIFERENTE DE AMBOS REPORTES ({caida_f1_pct:.1f}%)")
print()

# ============================================================================
# VERIFICACIÓN #3: P-VALUE HRV MANN-WHITNEY
# ============================================================================

print("="*80)
print("VERIFICACION #3: P-VALUE HRV MANN-WHITNEY")
print("="*80)
print()

# Cargar variable HRV original
df = df.merge(
    df_weekly[['usuario_id', 'semana_inicio', 'HRV_SDNN_p50']],
    on=['usuario_id', 'semana_inicio'],
    how='left'
)

# Separar por cluster
hrv_cluster_0 = df[df['cluster'] == 0]['HRV_SDNN_p50'].dropna()
hrv_cluster_1 = df[df['cluster'] == 1]['HRV_SDNN_p50'].dropna()

print(f"HRV en Cluster 0 (Bajo Sedentarismo):")
print(f"   N: {len(hrv_cluster_0)}")
print(f"   Media: {hrv_cluster_0.mean():.2f} ms")
print(f"   Mediana: {hrv_cluster_0.median():.2f} ms")
print(f"   Std: {hrv_cluster_0.std():.2f} ms")
print()

print(f"HRV en Cluster 1 (Alto Sedentarismo):")
print(f"   N: {len(hrv_cluster_1)}")
print(f"   Media: {hrv_cluster_1.mean():.2f} ms")
print(f"   Mediana: {hrv_cluster_1.median():.2f} ms")
print(f"   Std: {hrv_cluster_1.std():.2f} ms")
print()

# Mann-Whitney U test
u_stat, p_value = stats.mannwhitneyu(hrv_cluster_0, hrv_cluster_1, alternative='two-sided')

# Cohen's d (tamaño del efecto)
mean_diff = hrv_cluster_1.mean() - hrv_cluster_0.mean()
pooled_std = np.sqrt((hrv_cluster_0.std()**2 + hrv_cluster_1.std()**2) / 2)
cohens_d = mean_diff / pooled_std

print("PRUEBA MANN-WHITNEY U:")
print(f"   U statistic: {u_stat:,.0f}")
print(f"   p-value: {p_value:.4f}")
print()

print("TAMAÑO DEL EFECTO:")
print(f"   Diferencia de medias: {mean_diff:.2f} ms")
print(f"   Cohen's d: {cohens_d:.4f}")
print()

if p_value < 0.001:
    sig_label = "p < 0.001 (ALTAMENTE SIGNIFICATIVO)"
elif p_value < 0.01:
    sig_label = "p < 0.01 (MUY SIGNIFICATIVO)"
elif p_value < 0.05:
    sig_label = "p < 0.05 (SIGNIFICATIVO)"
else:
    sig_label = f"p = {p_value:.3f} (NO SIGNIFICATIVO)"

print(f"INTERPRETACIÓN: {sig_label}")
print()

if abs(p_value - 0.123) < 0.05:
    print("   >> CONSISTENTE CON CAP 6 (p=0.123)")
elif abs(p_value - 0.562) < 0.05:
    print("   >> CONSISTENTE CON INFORME V3 (p=0.562)")
else:
    print(f"   >> VALOR DIFERENTE DE AMBOS REPORTES (p={p_value:.3f})")
print()

# Clasificación Cohen's d
if abs(cohens_d) < 0.2:
    efecto = "DESPRECIABLE"
elif abs(cohens_d) < 0.5:
    efecto = "PEQUEÑO"
elif abs(cohens_d) < 0.8:
    efecto = "MEDIANO"
else:
    efecto = "GRANDE"

print(f"Tamaño del efecto: {efecto} (d={cohens_d:.3f})")
print()

# ============================================================================
# RESUMEN EJECUTIVO
# ============================================================================

print("="*80)
print("RESUMEN EJECUTIVO")
print("="*80)
print()
print("VERIFICACIÓN #2: ABLACIÓN HRV")
print(f"   Modelo completo (4V): F1 = {f1_completo:.4f}")
print(f"   Modelo sin HRV (2V): F1 = {f1_sin_hrv:.4f}")
print(f"   Caída: {caida_f1_pct:.1f}%")
print()
if abs(caida_f1_pct - 50) < 10:
    print("   CONCLUSIÓN: Ablación -50% CONFIRMADA")
elif abs(caida_f1_pct - 9.1) < 5:
    print("   CONCLUSIÓN: Ablación -9.1% CONFIRMADA")
else:
    print(f"   CONCLUSIÓN: Ablación real es {caida_f1_pct:.1f}% (diferente de reportes previos)")
print()

print("VERIFICACIÓN #3: P-VALUE HRV")
print(f"   Mann-Whitney U: {u_stat:,.0f}")
print(f"   p-value: {p_value:.4f}")
print(f"   Cohen's d: {cohens_d:.4f} ({efecto})")
print()
if abs(p_value - 0.562) < 0.05:
    print("   CONCLUSIÓN: p=0.562 CONFIRMADO (Informe V3 correcto)")
elif abs(p_value - 0.123) < 0.05:
    print("   CONCLUSIÓN: p=0.123 CONFIRMADO (Cap 6 correcto)")
else:
    print(f"   CONCLUSIÓN: p-value real es {p_value:.3f}")
print()
print("="*80)
print("VERIFICACIÓN COMPLETADA")
print("="*80)
print()

# Guardar resultados
import os
output_dir = os.path.join(os.path.dirname(__file__), "..", "resultados")
os.makedirs(output_dir, exist_ok=True)

resultados = pd.DataFrame({
    'Metrica': ['F1_completo', 'F1_sin_HRV', 'Caida_F1_absoluta', 'Caida_F1_porcentual',
                'Mann_Whitney_U', 'p_value_HRV', 'Cohens_d_HRV'],
    'Valor': [f1_completo, f1_sin_hrv, caida_f1, caida_f1_pct,
              u_stat, p_value, cohens_d]
})

output_file = os.path.join(output_dir, "verificacion_ablacion_mannwhitney.csv")
resultados.to_csv(output_file, index=False)
print(f"[OK] Resultados guardados: {output_file}")
print()

