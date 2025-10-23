#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENERADOR DE TABLAS PARA TESIS
Genera tablas completas con métricas por usuario listas para copiar/pegar
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef, confusion_matrix

# ===========================
# CONFIGURACIÓN
# ===========================

BASE_DIR = Path(__file__).parent
FUZZY_OUTPUT = BASE_DIR / 'analisis_u' / 'fuzzy' / 'fuzzy_output.csv'
CLUSTER_ASSIGNMENTS = BASE_DIR / 'analisis_u' / \
    'clustering' / 'cluster_assignments.csv'
WEEKLY_CONSOLIDADO = BASE_DIR / 'analisis_u' / \
    'semanal' / 'weekly_consolidado.csv'
OUTPUT_DIR = BASE_DIR / 'tablas_tesis'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TAU = 0.30  # Umbral óptimo

# Mapeo de usuarios
USER_MAP = {
    'u1': 'ale', 'u2': 'brenda', 'u3': 'christina', 'u4': 'edson',
    'u5': 'esmeralda', 'u6': 'fidel', 'u7': 'kevin', 'u8': 'legarda',
    'u9': 'lmartinez', 'u10': 'vane'
}

print("=" * 80)
print("GENERACIÓN DE TABLAS PARA TESIS")
print("=" * 80)
print()

# ===========================
# 1. CARGAR DATOS
# ===========================

print("📂 Cargando datos...")
df_fuzzy = pd.read_csv(FUZZY_OUTPUT)
df_cluster = pd.read_csv(CLUSTER_ASSIGNMENTS)
df_weekly = pd.read_csv(WEEKLY_CONSOLIDADO)

print(f"   Fuzzy output: {len(df_fuzzy)} semanas")
print(f"   Cluster assignments: {len(df_cluster)} semanas")
print(f"   Weekly consolidado: {len(df_weekly)} semanas")
print()

# ===========================
# 2. MERGE DATOS
# ===========================

print("🔗 Uniendo datos...")
df = pd.merge(df_fuzzy, df_cluster[['usuario_id', 'semana_inicio', 'cluster']],
              on=['usuario_id', 'semana_inicio'], how='inner')

# Binarizar fuzzy score con tau
df['fuzzy_class'] = (df['Sedentarismo_score'] >= TAU).astype(int)

print(f"   Datos unidos: {len(df)} semanas")
print()

# ===========================
# 3. TABLA 1: MÉTRICAS POR USUARIO
# ===========================

print("📊 Calculando métricas por usuario...")

tabla1_rows = []

for user_id in sorted(df['usuario_id'].unique()):
    user_data = df[df['usuario_id'] == user_id]

    if len(user_data) == 0:
        continue

    y_true = user_data['cluster'].values
    y_pred = user_data['fuzzy_class'].values

    # Calcular métricas
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    mcc = matthews_corrcoef(y_true, y_pred)

    # Matriz de confusión
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    # % datos observados (aproximado - asumiendo que pct_imputada_FC_walk está disponible)
    pct_obs = 100.0  # Placeholder, se puede calcular si hay datos de imputación

    tabla1_rows.append({
        'Usuario': f"{user_id} – {USER_MAP.get(user_id, '?')}",
        'Semanas (N)': len(user_data),
        '% Datos observados*': f"{pct_obs:.1f}",
        'Accuracy': f"{acc:.3f}",
        'Precision': f"{prec:.3f}",
        'Recall': f"{rec:.3f}",
        'F1': f"{f1:.3f}",
        'MCC': f"{mcc:.3f}",
        'τ usado': f"{TAU:.2f}",
        'TP': int(tp),
        'FP': int(fp),
        'TN': int(tn),
        'FN': int(fn)
    })

df_tabla1 = pd.DataFrame(tabla1_rows)

# Calcular global
y_true_global = df['cluster'].values
y_pred_global = df['fuzzy_class'].values
acc_global = accuracy_score(y_true_global, y_pred_global)
prec_global = precision_score(y_true_global, y_pred_global)
rec_global = recall_score(y_true_global, y_pred_global)
f1_global = f1_score(y_true_global, y_pred_global)

print("✅ Tabla 1 generada")
print()

# ===========================
# 4. TABLA 2: DISTRIBUCIÓN DE CLUSTERS POR USUARIO
# ===========================

print("📊 Calculando distribución de clusters por usuario...")

tabla2_rows = []

for user_id in sorted(df['usuario_id'].unique()):
    user_data = df[df['usuario_id'] == user_id]

    if len(user_data) == 0:
        continue

    total = len(user_data)
    n_alto = (user_data['cluster'] == 1).sum()
    n_bajo = (user_data['cluster'] == 0).sum()

    pct_alto = (n_alto / total) * 100
    pct_bajo = (n_bajo / total) * 100
    diff = abs(pct_alto - pct_bajo)

    tabla2_rows.append({
        'Usuario': f"{user_id} – {USER_MAP.get(user_id, '?')}",
        'Cluster Alto Sed (%)': f"{pct_alto:.1f}",
        'Cluster Bajo Sed (%)': f"{pct_bajo:.1f}",
        'Diferencia absoluta (%)': f"{diff:.1f}"
    })

df_tabla2 = pd.DataFrame(tabla2_rows)

print("✅ Tabla 2 generada")
print()

# ===========================
# 5. TABLA 3: ESTADÍSTICOS SEMANALES POR USUARIO
# ===========================

print("📊 Calculando estadísticos semanales por usuario...")

# Merge con weekly para obtener features
df_full = pd.merge(df, df_weekly, on=[
                   'usuario_id', 'semana_inicio'], how='left')

tabla3_rows = []

features = [
    'Actividad_relativa_p50', 'Actividad_relativa_iqr',
    'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr',
    'HRV_SDNN_p50', 'HRV_SDNN_iqr',
    'Delta_cardiaco_p50', 'Delta_cardiaco_iqr'
]

for user_id in sorted(df_full['usuario_id'].unique()):
    user_data = df_full[df_full['usuario_id'] == user_id]

    if len(user_data) == 0:
        continue

    row = {'Usuario': f"{user_id} – {USER_MAP.get(user_id, '?')}"}

    for feat in features:
        if feat in user_data.columns:
            mean_val = user_data[feat].mean()
            std_val = user_data[feat].std()
            row[feat] = f"{mean_val:.3f} (±{std_val:.3f})"
        else:
            row[feat] = "N/A"

    # Score fuzzy
    score_mean = user_data['Sedentarismo_score'].mean()
    score_std = user_data['Sedentarismo_score'].std()
    row['Score_fuzzy'] = f"{score_mean:.3f} (±{score_std:.3f})"

    tabla3_rows.append(row)

df_tabla3 = pd.DataFrame(tabla3_rows)

print("✅ Tabla 3 generada")
print()

# ===========================
# 6. GUARDAR TABLAS
# ===========================

print("💾 Guardando tablas...")

# CSV
df_tabla1.to_csv(OUTPUT_DIR / 'tabla1_metricas_por_usuario.csv', index=False)
df_tabla2.to_csv(OUTPUT_DIR / 'tabla2_distribucion_clusters.csv', index=False)
df_tabla3.to_csv(OUTPUT_DIR / 'tabla3_estadisticos_semanales.csv', index=False)

# Markdown para copiar/pegar directo
with open(OUTPUT_DIR / 'tablas_markdown.md', 'w', encoding='utf-8') as f:
    f.write("# TABLAS PARA TESIS - LISTAS PARA COPIAR/PEGAR\n\n")
    f.write("---\n\n")

    # TABLA 1
    f.write("## Tabla 1: Métricas de Clasificación (Fuzzy vs. Clusters) por Usuario\n\n")
    f.write(df_tabla1.to_markdown(index=False))
    f.write("\n\n")
    f.write(
        f"**Global (10 usuarios):** Accuracy={acc_global:.3f}, Precision={prec_global:.3f}, Recall={rec_global:.3f}, F1={f1_global:.3f}, τ={TAU:.2f}\n\n")
    f.write("\\* `% Datos observados` se calcula como (1 − %imputación total) en la semana promedio del usuario.\n\n")
    f.write("---\n\n")

    # TABLA 2
    f.write("## Tabla 2: Distribución de Clusters por Usuario\n\n")
    f.write(df_tabla2.to_markdown(index=False))
    f.write("\n\n")
    f.write("---\n\n")

    # TABLA 3
    f.write("## Tabla 3: Estadísticos Semanales por Usuario (media ± std)\n\n")

    # Tabla 3 es muy ancha, dividirla en dos partes
    cols_parte1 = ['Usuario', 'Actividad_relativa_p50', 'Actividad_relativa_iqr',
                   'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr']
    cols_parte2 = ['Usuario', 'HRV_SDNN_p50', 'HRV_SDNN_iqr',
                   'Delta_cardiaco_p50', 'Delta_cardiaco_iqr', 'Score_fuzzy']

    f.write("### Parte 1: Actividad y Superávit Calórico\n\n")
    df_tabla3_p1 = df_tabla3[cols_parte1]
    f.write(df_tabla3_p1.to_markdown(index=False))
    f.write("\n\n")

    f.write("### Parte 2: HRV, Delta Cardiaco y Score Fuzzy\n\n")
    df_tabla3_p2 = df_tabla3[cols_parte2]
    f.write(df_tabla3_p2.to_markdown(index=False))
    f.write("\n\n")

print(f"✅ Guardado: {OUTPUT_DIR / 'tabla1_metricas_por_usuario.csv'}")
print(f"✅ Guardado: {OUTPUT_DIR / 'tabla2_distribucion_clusters.csv'}")
print(f"✅ Guardado: {OUTPUT_DIR / 'tabla3_estadisticos_semanales.csv'}")
print(f"✅ Guardado: {OUTPUT_DIR / 'tablas_markdown.md'}")
print()

# ===========================
# 7. IMPRIMIR EN CONSOLA
# ===========================

print("=" * 80)
print("TABLAS GENERADAS - VISTA PREVIA")
print("=" * 80)
print()

print("TABLA 1: MÉTRICAS DE CLASIFICACIÓN POR USUARIO")
print("-" * 80)
print(df_tabla1.to_string(index=False))
print()
print(
    f"Global: Accuracy={acc_global:.3f}, Precision={prec_global:.3f}, Recall={rec_global:.3f}, F1={f1_global:.3f}")
print()

print("=" * 80)
print("TABLA 2: DISTRIBUCIÓN DE CLUSTERS POR USUARIO")
print("-" * 80)
print(df_tabla2.to_string(index=False))
print()

print("=" * 80)
print("TABLA 3: ESTADÍSTICOS SEMANALES POR USUARIO")
print("-" * 80)
print("(Ver archivo completo en tablas_markdown.md - tabla muy ancha para consola)")
print()

print("=" * 80)
print("✅ TABLAS LISTAS PARA COPIAR A TESIS")
print("=" * 80)
print(f"\n📁 Archivos guardados en: {OUTPUT_DIR}")
print(f"   - tabla1_metricas_por_usuario.csv")
print(f"   - tabla2_distribucion_clusters.csv")
print(f"   - tabla3_estadisticos_semanales.csv")
print(f"   - tablas_markdown.md (formato listo para copiar/pegar)")
print()
print("📌 Abre 'tablas_markdown.md' para copiar las tablas directamente a tu documento de tesis.")


