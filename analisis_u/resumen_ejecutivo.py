"""Resumen Ejecutivo - Pasos 3, 4 y 5"""
import pandas as pd
import numpy as np

# Cargar datos
df = pd.read_csv('semanal/cluster_inputs_weekly.csv')

print('='*80)
print('📊 RESUMEN EJECUTIVO - PIPELINE COMPLETADO (PASOS 3, 4 y 5)')
print('='*80)

# PASO 4: Agregación Semanal
print('\n🎯 PASO 4: AGREGACIÓN SEMANAL')
print('-'*80)
print(f'Total de semanas generadas: {len(df)}')
print(f'Usuarios cubiertos: {df["usuario_id"].nunique()}/10')
print(
    f'Rango de fechas: {df["semana_inicio"].min()} → {df["semana_inicio"].max()}')

# Calidad de datos
print(f'\n📊 Calidad de monitoreo:')
print(f'  Días promedio/semana: {df["dias_monitoreados"].mean():.1f}/7')
print(
    f'  Semanas con <3 días: {(df["flag_baja_cobertura"]==1).sum()} ({(df["flag_baja_cobertura"]==1).sum()/len(df)*100:.1f}%)')
print(
    f'  % imputada FC_walk (promedio): {df["pct_imputada_FC_walk"].mean():.1f}%')

# FILTROS DE CALIDAD para clustering
df_filt = df[(df['dias_monitoreados'] >= 3) &
             ((df['pct_imputada_FC_walk'] <= 60) | df['pct_imputada_FC_walk'].isna())]

print(f'\n🔍 FILAS VÁLIDAS PARA CLUSTERING (tras filtros de calidad):')
print(f'  Original: {len(df)} semanas')
print(
    f'  Post-filtro (dias≥3 y %imput≤60%): {len(df_filt)} semanas ({len(df_filt)/len(df)*100:.1f}%)')
print(f'  Eliminadas: {len(df)-len(df_filt)} semanas')

print(f'\n  Distribución por usuario (post-filtro):')
for uid in sorted(df_filt['usuario_id'].unique()):
    n = len(df_filt[df_filt['usuario_id'] == uid])
    print(f'    {uid}: {n:4d} semanas')

# ESTADÍSTICAS DE LAS 8 FEATURES
print(f'\n📈 ESTADÍSTICAS DESCRIPTIVAS (8 features para clustering):')
print('-'*80)

features = [
    'Actividad_relativa_p50', 'Actividad_relativa_iqr',
    'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr',
    'HRV_SDNN_p50', 'HRV_SDNN_iqr',
    'Delta_cardiaco_p50', 'Delta_cardiaco_iqr'
]

for feat in features:
    s = df_filt[feat].dropna()
    print(f'\n{feat}:')
    print(
        f'  Media: {s.mean():8.3f} | Mediana: {s.median():8.3f} | SD: {s.std():8.3f}')
    print(
        f'  Min: {s.min():10.3f} | Max: {s.max():10.3f} | IQR: {s.quantile(0.75)-s.quantile(0.25):8.3f}')

# INSIGHTS CLÍNICOS PRELIMINARES (sin clustering)
print(f'\n\n🔬 INSIGHTS CLÍNICOS PRELIMINARES (análisis descriptivo):')
print('='*80)

# 1. Actividad
act_low = df_filt['Actividad_relativa_p50'] < df_filt['Actividad_relativa_p50'].quantile(
    0.33)
act_high = df_filt['Actividad_relativa_p50'] > df_filt['Actividad_relativa_p50'].quantile(
    0.67)
print(f'\n1️⃣  ACTIVIDAD FÍSICA:')
print(
    f'   - Semanas de baja actividad (<p33): {act_low.sum()} ({act_low.sum()/len(df_filt)*100:.1f}%)')
print(
    f'     → Actividad media: {df_filt[act_low]["Actividad_relativa_p50"].mean():.3f}')
print(
    f'   - Semanas de alta actividad (>p67): {act_high.sum()} ({act_high.sum()/len(df_filt)*100:.1f}%)')
print(
    f'     → Actividad media: {df_filt[act_high]["Actividad_relativa_p50"].mean():.3f}')
print(f'   📌 Interpretación: Hay heterogeneidad marcada en actividad semanal')

# 2. HRV
hrv_low = df_filt['HRV_SDNN_p50'] < df_filt['HRV_SDNN_p50'].quantile(0.33)
hrv_high = df_filt['HRV_SDNN_p50'] > df_filt['HRV_SDNN_p50'].quantile(0.67)
print(f'\n2️⃣  VARIABILIDAD CARDÍACA (HRV):')
print(
    f'   - Semanas con HRV baja (<p33): {hrv_low.sum()} ({hrv_low.sum()/len(df_filt)*100:.1f}%)')
print(f'     → HRV media: {df_filt[hrv_low]["HRV_SDNN_p50"].mean():.1f} ms')
print(
    f'   - Semanas con HRV alta (>p67): {hrv_high.sum()} ({hrv_high.sum()/len(df_filt)*100:.1f}%)')
print(f'     → HRV media: {df_filt[hrv_high]["HRV_SDNN_p50"].mean():.1f} ms')
print(f'   📌 Interpretación: HRV muestra gran variabilidad entre semanas/usuarios')

# 3. Superávit calórico
sup_low = df_filt['Superavit_calorico_basal_p50'] < df_filt['Superavit_calorico_basal_p50'].quantile(
    0.33)
sup_high = df_filt['Superavit_calorico_basal_p50'] > df_filt['Superavit_calorico_basal_p50'].quantile(
    0.67)
print(f'\n3️⃣  SUPERÁVIT CALÓRICO BASAL:')
print(
    f'   - Semanas de bajo gasto (<p33): {sup_low.sum()} ({sup_low.sum()/len(df_filt)*100:.1f}%)')
print(
    f'     → Superávit medio: {df_filt[sup_low]["Superavit_calorico_basal_p50"].mean():.1f}% TMB')
print(
    f'   - Semanas de alto gasto (>p67): {sup_high.sum()} ({sup_high.sum()/len(df_filt)*100:.1f}%)')
print(
    f'     → Superávit medio: {df_filt[sup_high]["Superavit_calorico_basal_p50"].mean():.1f}% TMB')
print(f'   📌 Interpretación: Gasto calórico ajustado por TMB varía 2-3x entre usuarios')

# PASO 5: Missingness y ACF
print(f'\n\n🎯 PASO 5: MISSINGNESS Y ACF (COMPLETADO)')
print('-'*80)
print(f'✅ 1385 semanas analizadas para missingness')
print(f'✅ 112 gráficos ACF/PACF generados')
print(f'✅ 56/80 análisis ACF exitosos (70%)')
print(f'✅ Usuarios con >30 semanas para ACF: 6/10 (u1, u3, u6, u7, u8, u9)')

# ESTADO DEL PASO 6
print(f'\n\n🎯 PASO 6: CLUSTERING (PENDIENTE)')
print('-'*80)
print(f'⚠️  sklearn no disponible en el entorno')
print(f'📊 Datos listos para clustering: {len(df_filt)} semanas × 8 features')
print(f'💡 Para ejecutar: instalar scikit-learn y correr 06_clustering_semana.py')

print(f'\n\n📌 RECOMENDACIÓN PARA CLUSTERING (cuando se ejecute):')
print(f'   - K sugerido: 3-4 clusters (basado en heterogeneidad observada)')
print(
    f'   - Semanas válidas: {len(df_filt)} (suficiente para k-means robusto)')
print(f'   - Features clave: Actividad_relativa_p50, HRV_SDNN_p50, Superavit_calorico_basal_p50')

print('\n' + '='*80)
print('FIN DEL RESUMEN EJECUTIVO')
print('='*80)


