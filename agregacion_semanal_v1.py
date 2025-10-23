"""
Agregación Semanal - Paso 4 del Pipeline
=========================================

OBJETIVO:
---------
Agregar datos diarios por semana (Lunes-Domingo) y por usuario, generando
métricas robustas para clustering/fuzzy.

INSUMOS:
--------
- DB_final_v3_u{1..10}.csv (obligatorio)
- analisis_u/FC_walk_imputacion_V3_u{1..10}.csv (opcional, para calidad)

SALIDAS:
--------
- analisis_u/semanal/weekly_u{1..10}.csv
- analisis_u/semanal/weekly_consolidado.csv
- analisis_u/semanal/cluster_inputs_weekly.csv
- 04_agregacion_semanal_log.txt

METODOLOGÍA:
------------
- Semana: Lunes-Domingo (dt.to_period('W-MON'))
- Métricas robustas: p25, p50, p75, IQR, std, cv
- ac1: autocorrelación lag-1 intra-semana (si count_dias>=5)
- Calidad: %imputada_FC_walk desde auditoría cuando existe

Autor: Pipeline automatizado
Fecha: 2025-10-16
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

BASE_DIR = Path('.').resolve()
AUDITORIA_DIR = BASE_DIR / 'analisis_u'
OUTPUT_DIR = AUDITORIA_DIR / 'semanal'

# Crear directorio de salida
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Variables a analizar
VARIABLES = [
    "Actividad_relativa",
    "Superavit_calorico_basal",
    "HRV_SDNN",
    "FCr_promedio_diario",
    "FC_al_caminar_promedio_diario",
    "Delta_cardiaco"  # derivada
]

# Mapeo usuario
USER_MAP = {
    1: "ale", 2: "brenda", 3: "christina", 4: "edson", 5: "esmeralda",
    6: "fidel", 7: "kevin", 8: "legarda", 9: "lmartinez", 10: "vane"
}

# Umbral mínimo de días para calcular ac1
MIN_DIAS_AC1 = 5
MIN_DIAS_COBERTURA = 3  # Flag si <3 días en semana

# Log global
LOG_LINES = []

# ==============================================================================
# FUNCIONES UTILITARIAS
# ==============================================================================


def log(msg):
    """Registra mensaje en log y consola"""
    LOG_LINES.append(msg)
    print(msg)


def calculate_ac1(series):
    """
    Calcula autocorrelación lag-1 para una serie temporal.
    Requiere al menos 2 valores no-NaN.
    """
    s = pd.to_numeric(series, errors='coerce').dropna()
    if len(s) < 2:
        return np.nan
    try:
        return s.autocorr(lag=1)
    except:
        return np.nan


def aggregate_variable_metrics(group, var_name):
    """
    Calcula métricas de agregación para una variable en un grupo (semana).

    Returns:
        dict con sufijos: _count, _mean, _p25, _p50, _p75, _iqr, _std, _cv, _ac1
    """
    s = pd.to_numeric(group[var_name], errors='coerce').dropna()

    n = len(s)
    prefix = var_name

    if n == 0:
        return {
            f'{prefix}_count': 0,
            f'{prefix}_mean': np.nan,
            f'{prefix}_p25': np.nan,
            f'{prefix}_p50': np.nan,
            f'{prefix}_p75': np.nan,
            f'{prefix}_iqr': np.nan,
            f'{prefix}_std': np.nan,
            f'{prefix}_cv': np.nan,
            f'{prefix}_ac1': np.nan
        }

    mean = s.mean()
    p25, p50, p75 = s.quantile([0.25, 0.50, 0.75]).values
    iqr = p75 - p25
    std = s.std(ddof=1) if n > 1 else 0.0

    # CV protegido
    cv = std / abs(mean) if abs(mean) > 1e-8 else np.nan

    # AC1: solo si tenemos suficientes días
    ac1 = calculate_ac1(group[var_name]) if n >= MIN_DIAS_AC1 else np.nan

    return {
        f'{prefix}_count': n,
        f'{prefix}_mean': mean,
        f'{prefix}_p25': p25,
        f'{prefix}_p50': p50,
        f'{prefix}_p75': p75,
        f'{prefix}_iqr': iqr,
        f'{prefix}_std': std,
        f'{prefix}_cv': cv,
        f'{prefix}_ac1': ac1
    }


def aggregate_weekly(df, audit_df=None):
    """
    Agrega dataframe diario por semana (Lun-Dom).

    Args:
        df: DataFrame diario con variables
        audit_df: DataFrame de auditoría (opcional) para calidad FC_walk

    Returns:
        DataFrame semanal agregado
    """
    # Asegurar Fecha como datetime
    df = df.copy()
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df = df.dropna(subset=['Fecha']).sort_values(
        'Fecha').reset_index(drop=True)

    if len(df) == 0:
        return pd.DataFrame()

    # Crear periodo semanal (Lun-Dom)
    df['semana'] = df['Fecha'].dt.to_period('W-MON')

    # Merge con auditoría si existe
    if audit_df is not None:
        audit_df = audit_df.copy()
        audit_df['Fecha'] = pd.to_datetime(audit_df['Fecha'], errors='coerce')
        audit_df = audit_df[['Fecha', 'FC_walk_fuente']].dropna(subset=[
                                                                'Fecha'])
        df = df.merge(audit_df, on='Fecha', how='left')
    else:
        df['FC_walk_fuente'] = np.nan

    # Agregar por semana
    weekly_data = []

    for semana, group in df.groupby('semana'):
        n_dias = len(group)

        # Inicio de semana (lunes)
        semana_inicio = semana.start_time.date()

        # Métricas por variable
        row = {
            'semana_inicio': semana_inicio,
            'dias_monitoreados': n_dias,
            'flag_baja_cobertura': 1 if n_dias < MIN_DIAS_COBERTURA else 0
        }

        # Agregar cada variable
        for var in VARIABLES:
            if var in group.columns:
                metrics = aggregate_variable_metrics(group, var)
                row.update(metrics)

        # Calidad de imputación FC_walk
        if 'FC_walk_fuente' in group.columns and group['FC_walk_fuente'].notna().any():
            total_fuente = group['FC_walk_fuente'].notna().sum()
            imputada = (group['FC_walk_fuente'] != 'observada').sum()
            row['pct_imputada_FC_walk'] = (
                imputada / total_fuente * 100) if total_fuente > 0 else np.nan
        else:
            row['pct_imputada_FC_walk'] = np.nan

        weekly_data.append(row)

    return pd.DataFrame(weekly_data)


def process_user(u_id):
    """
    Procesa un usuario: carga datos diarios, agrega semanalmente.

    Returns:
        DataFrame semanal o None si falla
    """
    alias = USER_MAP.get(u_id, f"u{u_id}")
    log(f"\n{'='*80}")
    log(f"Usuario u{u_id} ({alias})")
    log(f"{'='*80}")

    # Cargar dataset diario
    trabajo_path = BASE_DIR / f"DB_final_v3_u{u_id}.csv"
    if not trabajo_path.exists():
        log(f"  ❌ No se encontró: {trabajo_path.name}")
        return None

    try:
        df = pd.read_csv(trabajo_path)
        log(f"  ✅ Dataset cargado: {len(df)} días")
    except Exception as e:
        log(f"  ❌ Error al leer dataset: {e}")
        return None

    # Verificar columnas requeridas
    missing_vars = [v for v in VARIABLES[:-1]
                    if v not in df.columns]  # excepto Delta_cardiaco
    if missing_vars:
        log(f"  ⚠️  Variables faltantes: {', '.join(missing_vars)}")

    # Derivar Delta_cardiaco
    if 'FC_al_caminar_promedio_diario' in df.columns and 'FCr_promedio_diario' in df.columns:
        df['Delta_cardiaco'] = df['FC_al_caminar_promedio_diario'] - \
            df['FCr_promedio_diario']
        log(f"  ✅ Delta_cardiaco derivado")
    else:
        log(f"  ⚠️  No se pudo derivar Delta_cardiaco (columnas faltantes)")

    # Cargar auditoría (opcional)
    audit_path = AUDITORIA_DIR / f"FC_walk_imputacion_V3_u{u_id}.csv"
    audit_df = None
    if audit_path.exists():
        try:
            audit_df = pd.read_csv(audit_path)
            log(f"  ✅ Auditoría cargada: {len(audit_df)} registros")
        except Exception as e:
            log(f"  ⚠️  Error al leer auditoría: {e}")
    else:
        log(f"  ⚠️  Auditoría no encontrada (pct_imputada_FC_walk = NaN)")

    # Agregación semanal
    try:
        df_weekly = aggregate_weekly(df, audit_df)

        if df_weekly.empty:
            log(f"  ❌ Agregación resultó vacía")
            return None

        n_semanas = len(df_weekly)
        n_baja_cob = df_weekly['flag_baja_cobertura'].sum()
        dias_promedio = df_weekly['dias_monitoreados'].mean()

        log(f"  ✅ Agregación completada:")
        log(f"     - Semanas generadas: {n_semanas}")
        log(f"     - Días promedio/semana: {dias_promedio:.1f}")
        log(
            f"     - Semanas baja cobertura (<{MIN_DIAS_COBERTURA} días): {n_baja_cob}")

        if 'pct_imputada_FC_walk' in df_weekly.columns:
            pct_imp_mean = df_weekly['pct_imputada_FC_walk'].mean()
            if not np.isnan(pct_imp_mean):
                log(
                    f"     - % imputada FC_walk (promedio): {pct_imp_mean:.1f}%")

        # Añadir identificador de usuario
        df_weekly.insert(0, 'usuario_alias', alias)
        df_weekly.insert(0, 'usuario_id', f"u{u_id}")

        # Guardar archivo individual
        output_path = OUTPUT_DIR / f"weekly_u{u_id}.csv"
        df_weekly.to_csv(output_path, index=False)
        log(f"  ✅ Guardado: {output_path.name}")

        return df_weekly

    except Exception as e:
        log(f"  ❌ Error en agregación: {e}")
        import traceback
        log(traceback.format_exc())
        return None


def build_cluster_inputs(df_consolidado):
    """
    Construye subset de features para clustering.

    Columnas esperadas:
    - usuario_id, usuario_alias, semana_inicio
    - dias_monitoreados, flag_baja_cobertura
    - pct_imputada_FC_walk
    - {var}_p50, {var}_iqr para variables clave
    """
    # Columnas de identificación y contexto
    id_cols = ['usuario_id', 'usuario_alias', 'semana_inicio',
               'dias_monitoreados', 'flag_baja_cobertura']

    # Columnas de calidad
    quality_cols = ['pct_imputada_FC_walk']

    # Features para clustering (p50 e iqr de variables clave)
    feature_cols = [
        'Actividad_relativa_p50', 'Actividad_relativa_iqr',
        'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr',
        'HRV_SDNN_p50', 'HRV_SDNN_iqr',
        'Delta_cardiaco_p50', 'Delta_cardiaco_iqr'
    ]

    # Seleccionar columnas disponibles
    all_cols = id_cols + quality_cols + feature_cols
    available_cols = [c for c in all_cols if c in df_consolidado.columns]

    return df_consolidado[available_cols].copy()


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    log("="*80)
    log("AGREGACIÓN SEMANAL - PASO 4")
    log("="*80)
    log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Directorio base: {BASE_DIR}")
    log(f"Directorio salida: {OUTPUT_DIR}")
    log("")

    # Procesar usuarios
    weekly_frames = []
    resultados = []

    for u_id in range(1, 11):
        df_weekly = process_user(u_id)

        if df_weekly is not None:
            weekly_frames.append(df_weekly)
            resultados.append({
                'usuario_id': f"u{u_id}",
                'alias': USER_MAP.get(u_id, f"u{u_id}"),
                'status': 'OK',
                'n_semanas': len(df_weekly),
                'dias_promedio': df_weekly['dias_monitoreados'].mean(),
                'pct_baja_cob': (df_weekly['flag_baja_cobertura'].sum() / len(df_weekly) * 100),
                'pct_imputada_mean': df_weekly.get('pct_imputada_FC_walk', pd.Series([np.nan])).mean()
            })
        else:
            resultados.append({
                'usuario_id': f"u{u_id}",
                'alias': USER_MAP.get(u_id, f"u{u_id}"),
                'status': 'FAIL',
                'n_semanas': 0,
                'dias_promedio': 0,
                'pct_baja_cob': 0,
                'pct_imputada_mean': np.nan
            })

    # =========================================================================
    # CONSOLIDADO
    # =========================================================================
    log(f"\n{'='*80}")
    log("GENERANDO CONSOLIDADO")
    log(f"{'='*80}")

    if not weekly_frames:
        log(f"❌ No se pudo generar consolidado (sin datos válidos)")
        return 1

    df_consolidado = pd.concat(weekly_frames, ignore_index=True)
    path_consolidado = OUTPUT_DIR / "weekly_consolidado.csv"
    df_consolidado.to_csv(path_consolidado, index=False)

    log(f"✅ Consolidado guardado: {path_consolidado.name}")
    log(f"   Registros totales: {len(df_consolidado)} semanas")
    log(f"   Usuarios cubiertos: {df_consolidado['usuario_id'].nunique()}/10")
    log(f"   Columnas: {len(df_consolidado.columns)}")

    # =========================================================================
    # CLUSTER INPUTS
    # =========================================================================
    log(f"\n{'='*80}")
    log("GENERANDO CLUSTER INPUTS")
    log(f"{'='*80}")

    df_cluster = build_cluster_inputs(df_consolidado)
    path_cluster = OUTPUT_DIR / "cluster_inputs_weekly.csv"
    df_cluster.to_csv(path_cluster, index=False)

    log(f"✅ Cluster inputs guardado: {path_cluster.name}")
    log(f"   Registros: {len(df_cluster)}")
    log(f"   Features para clustering: {len([c for c in df_cluster.columns if c.endswith(('_p50', '_iqr'))])}")
    log(f"   Columnas totales: {len(df_cluster.columns)}")
    log(f"   Columnas: {list(df_cluster.columns)}")

    # =========================================================================
    # RESUMEN FINAL
    # =========================================================================
    log(f"\n{'='*80}")
    log("RESUMEN POR USUARIO")
    log(f"{'='*80}")
    log(f"{'Usuario':<12} {'Alias':<12} {'Status':<8} {'Semanas':<8} {'Días/sem':<10} {'%BajaCob':<10} {'%Imput':<10}")
    log("-"*80)

    for r in resultados:
        if r['status'] == 'OK':
            pct_imp_str = f"{r['pct_imputada_mean']:.1f}" if not np.isnan(
                r['pct_imputada_mean']) else "N/A"
            log(f"{r['usuario_id']:<12} {r['alias']:<12} {r['status']:<8} {r['n_semanas']:<8} "
                f"{r['dias_promedio']:<10.1f} {r['pct_baja_cob']:<10.1f} {pct_imp_str:<10}")
        else:
            log(f"{r['usuario_id']:<12} {r['alias']:<12} {r['status']:<8} FAIL")

    n_ok = sum(1 for r in resultados if r['status'] == 'OK')

    log("")
    log(f"Usuarios procesados exitosamente: {n_ok}/10")
    log(f"Total de semanas generadas: {len(df_consolidado)}")

    # =========================================================================
    # TOP SEMANAS
    # =========================================================================
    log(f"\n{'='*80}")
    log("TOP 10 SEMANAS - MAYOR ACTIVIDAD_RELATIVA_IQR")
    log(f"{'='*80}")

    if 'Actividad_relativa_iqr' in df_consolidado.columns:
        top_act = df_consolidado.nlargest(10, 'Actividad_relativa_iqr')[
            ['usuario_id', 'semana_inicio',
                'Actividad_relativa_iqr', 'Actividad_relativa_p50']
        ]
        log(top_act.to_string(index=False))
    else:
        log("(Columna no disponible)")

    log(f"\n{'='*80}")
    log("TOP 10 SEMANAS - MAYOR HRV_SDNN_IQR")
    log(f"{'='*80}")

    if 'HRV_SDNN_iqr' in df_consolidado.columns:
        top_hrv = df_consolidado.nlargest(10, 'HRV_SDNN_iqr')[
            ['usuario_id', 'semana_inicio', 'HRV_SDNN_iqr', 'HRV_SDNN_p50']
        ]
        log(top_hrv.to_string(index=False))
    else:
        log("(Columna no disponible)")

    # =========================================================================
    # FINALIZACIÓN
    # =========================================================================
    log(f"\n{'='*80}")
    log("AGREGACIÓN SEMANAL COMPLETADA")
    log(f"{'='*80}")
    log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("")
    log(f"📂 Archivos generados:")
    log(f"   - {n_ok} archivos weekly_uN.csv")
    log(f"   - 1 weekly_consolidado.csv ({len(df_consolidado)} semanas)")
    log(f"   - 1 cluster_inputs_weekly.csv ({len(df_cluster)} semanas)")
    log("")

    # Guardar log
    log_path = BASE_DIR / "04_agregacion_semanal_log.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG_LINES))

    print(f"\n✅ Log guardado en: {log_path.name}")

    return 0 if n_ok == 10 else 1


if __name__ == '__main__':
    sys.exit(main())
