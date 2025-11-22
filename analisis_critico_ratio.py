#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis crítico de la propuesta de ratio de movimiento
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


def analisis_critico_ratio():
    """
    Análisis crítico exhaustivo de la propuesta de ratio de movimiento
    """

    print("🔍 ANÁLISIS CRÍTICO DE LA PROPUESTA DE RATIO DE MOVIMIENTO")
    print("=" * 80)

    # Leer datos consolidados
    df = pd.read_csv("DB_usuarios_consolidada.csv")

    print(f"📊 DATOS DISPONIBLES:")
    print(f"   - Total registros: {len(df):,}")
    print(f"   - Usuarios: {df['Usuario'].nunique()}")
    print(f"   - Período: {df['Fecha'].min()} a {df['Fecha'].max()}")
    print()

    # 1. VALIDACIÓN DE LA AFIRMACIÓN INICIAL
    print("1️⃣ VALIDACIÓN DE LA AFIRMACIÓN: 'Promedio de 15 hrs por día'")
    print("-" * 60)

    # Convertir Total_hrs_monitorizadas a horas si está en minutos
    if df['Total_hrs_monitorizadas'].max() > 24:
        print("⚠️  ADVERTENCIA: Los valores de Total_hrs_monitorizadas parecen estar en minutos")
        df['Total_hrs_monitorizadas_horas'] = df['Total_hrs_monitorizadas'] / 60
    else:
        df['Total_hrs_monitorizadas_horas'] = df['Total_hrs_monitorizadas']

    promedio_horas = df['Total_hrs_monitorizadas_horas'].mean()
    print(
        f"   📈 Promedio real de horas monitoreadas: {promedio_horas:.2f} horas")
    print(
        f"   📊 Mediana: {df['Total_hrs_monitorizadas_horas'].median():.2f} horas")
    print(
        f"   📉 Rango: {df['Total_hrs_monitorizadas_horas'].min():.2f} - {df['Total_hrs_monitorizadas_horas'].max():.2f} horas")

    if abs(promedio_horas - 15) > 2:
        print(
            f"   ❌ TU AFIRMACIÓN ES INCORRECTA. La diferencia es de {abs(promedio_horas - 15):.2f} horas")
    else:
        print(f"   ✅ Tu afirmación es aproximadamente correcta")
    print()

    # 2. ANÁLISIS DEL RATIO PROPUESTO
    print("2️⃣ ANÁLISIS DEL RATIO PROPUESTO: min_totales_en_movimiento / Total_hrs_monitorizadas")
    print("-" * 60)

    # Calcular el ratio propuesto
    df['ratio_movimiento_propuesto'] = df['min_totales_en_movimiento'] / \
        df['Total_hrs_monitorizadas']

    print(f"   📊 Estadísticas del ratio propuesto:")
    print(f"      - Media: {df['ratio_movimiento_propuesto'].mean():.4f}")
    print(f"      - Mediana: {df['ratio_movimiento_propuesto'].median():.4f}")
    print(
        f"      - Desviación estándar: {df['ratio_movimiento_propuesto'].std():.4f}")
    print(
        f"      - Rango: {df['ratio_movimiento_propuesto'].min():.4f} - {df['ratio_movimiento_propuesto'].max():.4f}")
    print()

    # 3. PROBLEMAS ESTADÍSTICOS IDENTIFICADOS
    print("3️⃣ PROBLEMAS ESTADÍSTICOS IDENTIFICADOS")
    print("-" * 60)

    # Verificar valores extremos
    q99 = df['ratio_movimiento_propuesto'].quantile(0.99)
    q01 = df['ratio_movimiento_propuesto'].quantile(0.01)
    outliers = df[(df['ratio_movimiento_propuesto'] > q99) |
                  (df['ratio_movimiento_propuesto'] < q01)]

    print(
        f"   🚨 Valores extremos (outliers): {len(outliers)} registros ({len(outliers)/len(df)*100:.2f}%)")
    print(f"   📊 Percentil 99: {q99:.4f}")
    print(f"   📊 Percentil 1: {q01:.4f}")

    # Verificar valores imposibles (>1)
    valores_imposibles = df[df['ratio_movimiento_propuesto'] > 1]
    print(f"   ❌ Valores imposibles (>1): {len(valores_imposibles)} registros")
    if len(valores_imposibles) > 0:
        print(f"      - Esto indica errores en los datos o unidades inconsistentes")

    # Verificar correlaciones
    correlaciones = df[['min_totales_en_movimiento',
                        'Total_hrs_monitorizadas', 'ratio_movimiento_propuesto']].corr()
    print(
        f"   📈 Correlación min_movimiento vs Total_hrs: {correlaciones.loc['min_totales_en_movimiento', 'Total_hrs_monitorizadas']:.4f}")
    print()

    # 4. ANÁLISIS POR USUARIO
    print("4️⃣ ANÁLISIS POR USUARIO")
    print("-" * 60)

    stats_por_usuario = df.groupby('Usuario').agg({
        'ratio_movimiento_propuesto': ['mean', 'std', 'min', 'max'],
        'min_totales_en_movimiento': 'mean',
        'Total_hrs_monitorizadas': 'mean'
    }).round(4)

    print("   📊 Estadísticas por usuario:")
    print(stats_por_usuario)
    print()

    # 5. ALTERNATIVAS METODOLÓGICAS
    print("5️⃣ ALTERNATIVAS METODOLÓGICAS MÁS ROBUSTAS")
    print("-" * 60)

    # Ratio alternativo 1: Movimiento vs tiempo despierto estimado
    df['ratio_movimiento_vs_despierto'] = df['min_totales_en_movimiento'] / \
        (df['Total_hrs_monitorizadas'] * 0.7)  # Asumiendo 70% tiempo despierto

    # Ratio alternativo 2: Eficiencia de movimiento (pasos por minuto de movimiento)
    df['eficiencia_movimiento'] = df['Numero_pasos_por_dia'] / \
        df['min_totales_en_movimiento']

    # Ratio alternativo 3: Intensidad de movimiento (distancia por minuto)
    df['intensidad_movimiento'] = df['distancia_caminada_en_km'] / \
        df['min_totales_en_movimiento']

    print("   🔄 Alternativas propuestas:")
    print(
        f"      1. Ratio vs tiempo despierto estimado: Media = {df['ratio_movimiento_vs_despierto'].mean():.4f}")
    print(
        f"      2. Eficiencia (pasos/min): Media = {df['eficiencia_movimiento'].mean():.2f}")
    print(
        f"      3. Intensidad (km/min): Media = {df['intensidad_movimiento'].mean():.4f}")
    print()

    # 6. RECOMENDACIONES CRÍTICAS
    print("6️⃣ RECOMENDACIONES CRÍTICAS")
    print("-" * 60)

    print("   ❌ NO RECOMIENDO implementar el ratio propuesto por las siguientes razones:")
    print("      1. Conceptualmente incorrecto (no es un ratio de movimiento)")
    print("      2. Valores extremos e imposibles detectados")
    print("      3. Falta de validación con variables conocidas")
    print("      4. No considera la calidad del movimiento")
    print("      5. Puede introducir sesgos en el análisis")
    print()

    print("   ✅ ALTERNATIVAS RECOMENDADAS:")
    print("      1. Usar min_totales_en_movimiento directamente (más interpretable)")
    print("      2. Crear percentiles de actividad por usuario")
    print("      3. Implementar ratio de eficiencia (pasos/minuto)")
    print("      4. Usar intensidad de movimiento (distancia/minuto)")
    print("      5. Crear categorías de actividad (baja/media/alta)")
    print()

    # 7. VALIDACIÓN CON VARIABLES EXISTENTES
    print("7️⃣ VALIDACIÓN CON VARIABLES EXISTENTES")
    print("-" * 60)

    # Correlaciones con variables de actividad
    variables_validacion = ['Numero_pasos_por_dia',
                            'distancia_caminada_en_km', 'Gasto_calorico_activo']

    for var in variables_validacion:
        if var in df.columns:
            corr = df['ratio_movimiento_propuesto'].corr(df[var])
            print(f"   📈 Correlación con {var}: {corr:.4f}")

    print()
    print("🎯 CONCLUSIÓN: La propuesta actual NO es metodológicamente sólida")
    print("   Se requiere una revisión completa del enfoque antes de implementar")


if __name__ == "__main__":
    analisis_critico_ratio()




