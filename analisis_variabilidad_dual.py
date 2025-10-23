"""
Análisis de Variabilidad Dual - Paso 3 del Pipeline
====================================================

PROPÓSITO:
----------
Comparar la variabilidad de variables biométricas en dos escenarios:
  - Panel A (observada): Solo días con FC_walk observada (sin imputación)
  - Panel B (operativa): Dataset completo post-imputación (usado para modelado)

OBJETIVO METODOLÓGICO:
----------------------
Cuantificar el impacto del pipeline de imputación sobre la variabilidad fisiológica.
Panel A sirve como "piso fisiológico" (datos reales capturados por el dispositivo).
Panel B es la "realidad operativa" (datos con los que trabajaremos en modelado).

SUPUESTOS:
----------
1. Los archivos DB_final_v3_u{N}.csv ya contienen variables derivadas 
   (Actividad_relativa, Superavit_calorico_basal).
2. Las auditorías FC_walk_imputacion_V3_u{N}.csv marcan la fuente de cada registro.
3. NO re-imputamos, NO re-winzorizamos: este script es diagnóstico puro.

DECISIONES TÉCNICAS:
--------------------
- CV (coeficiente de variación): protegido con ε=1e-8 para evitar explosiones cerca de cero.
  Si |mean| < ε, reportamos NaN (documentado como inestabilidad).
- MAD: escalado con 1.4826 para comparabilidad con σ en distribuciones normales.
- IQR: robusto a outliers; complementa SD para distribuciones asimétricas.
- Ratio_std: mide compresión/expansión de variabilidad (>1 = imputación aumentó dispersión).
- Delta_iqr: diferencia absoluta; útil cuando las escalas difieren entre usuarios.

ZONA DE TRABAJO:
----------------
Entrada: 4 semestre_dataset/DB_final_v3_u{N}.csv + analisis_u/FC_walk_imputacion_V3_u{N}.csv
Salida:  4 semestre_dataset/analisis_u/variabilidad/**

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

# Suprimir warnings de pandas para limpieza de output
warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

BASE_DIR = Path('.').resolve()
AUDITORIA_DIR = BASE_DIR / 'analisis_u'
OUTPUT_DIR = AUDITORIA_DIR / 'variabilidad'

# Crear directorio de salida si no existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Variables a analizar (orden de prioridad)
VARIABLES = [
    "Actividad_relativa",
    "Superavit_calorico_basal",
    "HRV_SDNN",
    "FC_al_caminar_promedio_diario",
    "FCr_promedio_diario",
    "Delta_cardiaco"  # Se deriva en runtime
]

# Mapeo usuario ID → alias
USER_MAP = {
    1: "ale", 2: "brenda", 3: "christina", 4: "edson", 5: "esmeralda",
    6: "fidel", 7: "kevin", 8: "legarda", 9: "lmartinez", 10: "vane"
}

# Parámetros de robustez
EPSILON_CV = 1e-8  # Protección para CV
MAD_SCALE = 1.4826  # Factor de escala para comparabilidad con σ

# Log global
LOG_LINES = []


# ==============================================================================
# FUNCIONES UTILITARIAS
# ==============================================================================

def log(msg):
    """Registra mensaje en log y imprime en consola"""
    LOG_LINES.append(msg)
    print(msg)


def safe_metrics(series):
    """
    Calcula métricas de variabilidad robustas para una serie numérica.

    Returns:
        dict con n, mean, std, iqr, mad, cv, p10, p50, p90
    """
    # Filtrar NaN y convertir a numérico
    s = pd.to_numeric(series, errors='coerce').dropna()

    if len(s) == 0:
        return {
            'n': 0, 'mean': np.nan, 'std': np.nan, 'iqr': np.nan,
            'mad': np.nan, 'cv': np.nan, 'p10': np.nan, 'p50': np.nan, 'p90': np.nan
        }

    # Estadísticas básicas
    n = len(s)
    mean = s.mean()
    std = s.std(ddof=1) if n > 1 else 0.0

    # Percentiles
    p10, p50, p90 = s.quantile([0.10, 0.50, 0.90]).values

    # IQR
    q1, q3 = s.quantile([0.25, 0.75]).values
    iqr = q3 - q1

    # MAD (Median Absolute Deviation) escalado
    mad = MAD_SCALE * np.median(np.abs(s - p50))

    # CV (protegido contra divisor cercano a cero)
    if abs(mean) > EPSILON_CV:
        cv = std / abs(mean)
    else:
        cv = np.nan  # Inestable, reportar como NaN

    return {
        'n': n,
        'mean': mean,
        'std': std,
        'iqr': iqr,
        'mad': mad,
        'cv': cv,
        'p10': p10,
        'p50': p50,
        'p90': p90
    }


def compute_panel_metrics(df, variables):
    """
    Calcula métricas para todas las variables disponibles en un DataFrame.

    Args:
        df: DataFrame con las variables
        variables: lista de nombres de variables a evaluar

    Returns:
        DataFrame con una fila por variable y columnas de métricas
    """
    results = []

    for var in variables:
        if var not in df.columns:
            continue

        metrics = safe_metrics(df[var])
        metrics['variable'] = var
        results.append(metrics)

    if not results:
        return pd.DataFrame()

    # Reorganizar columnas: variable primero
    df_out = pd.DataFrame(results)
    cols = ['variable'] + [c for c in df_out.columns if c != 'variable']
    return df_out[cols]


def make_dual_compare(df_obs, df_op):
    """
    Construye tabla comparativa Panel A vs Panel B.

    Args:
        df_obs: métricas observadas (Panel A)
        df_op: métricas operativas (Panel B)

    Returns:
        DataFrame con comparativos y flags
    """
    # Merge por variable
    comp = pd.merge(
        df_obs.add_suffix('_obs'),
        df_op.add_suffix('_op'),
        left_on='variable_obs',
        right_on='variable_op',
        how='outer'
    )

    # Limpiar nombres duplicados
    comp['variable'] = comp['variable_obs'].fillna(comp['variable_op'])
    comp = comp.drop(columns=['variable_obs', 'variable_op'])

    # Calcular comparativos
    comp['ratio_std'] = comp['std_op'] / comp['std_obs'].replace(0, EPSILON_CV)
    comp['delta_iqr'] = comp['iqr_op'] - comp['iqr_obs']

    # Generar flags interpretativos
    def make_flag(row):
        flags = []

        # Tamaño de panel A
        if row['n_obs'] < 30:
            flags.append(f"piso_A_chico(n={int(row['n_obs'])})")

        # Ratio de variabilidad
        if pd.notna(row['ratio_std']):
            if row['ratio_std'] > 1.2:
                flags.append(f"↑var(ratio={row['ratio_std']:.2f})")
            elif row['ratio_std'] < 0.8:
                flags.append(f"↓var(ratio={row['ratio_std']:.2f})")

        # CV inestable
        if pd.isna(row['cv_obs']) or pd.isna(row['cv_op']):
            flags.append("CV_inestable(media≈0)")

        # Delta IQR significativo
        if pd.notna(row['delta_iqr']) and abs(row['delta_iqr']) > 0.1 * abs(row['iqr_obs']):
            flags.append(f"Δiqr={row['delta_iqr']:.3f}")

        return " | ".join(flags) if flags else "OK"

    comp['nota_flags'] = comp.apply(make_flag, axis=1)

    # Reorganizar columnas
    cols_order = ['variable',
                  'n_obs', 'mean_obs', 'std_obs', 'iqr_obs', 'mad_obs', 'cv_obs', 'p10_obs', 'p50_obs', 'p90_obs',
                  'n_op', 'mean_op', 'std_op', 'iqr_op', 'mad_op', 'cv_op', 'p10_op', 'p50_op', 'p90_op',
                  'ratio_std', 'delta_iqr', 'nota_flags']

    return comp[[c for c in cols_order if c in comp.columns]]


def load_user_data(u_id):
    """
    Carga dataset de trabajo y auditoría para un usuario.

    Args:
        u_id: número de usuario (1-10)

    Returns:
        tuple (df_trabajo, df_auditoria) o (None, None) si falla
    """
    # Cargar dataset de trabajo
    trabajo_path = BASE_DIR / f"DB_final_v3_u{u_id}.csv"
    if not trabajo_path.exists():
        log(f"  ❌ No se encontró: {trabajo_path.name}")
        return None, None

    try:
        df_trabajo = pd.read_csv(trabajo_path)
        df_trabajo['Fecha'] = pd.to_datetime(
            df_trabajo['Fecha'], errors='coerce')
        df_trabajo = df_trabajo.sort_values('Fecha').reset_index(drop=True)
    except Exception as e:
        log(f"  ❌ Error al leer {trabajo_path.name}: {e}")
        return None, None

    # Cargar auditoría
    audit_path = AUDITORIA_DIR / f"FC_walk_imputacion_V3_u{u_id}.csv"
    if not audit_path.exists():
        log(f"  ⚠️  No se encontró auditoría: {audit_path.name}")
        return df_trabajo, None

    try:
        df_audit = pd.read_csv(audit_path)
        df_audit['Fecha'] = pd.to_datetime(df_audit['Fecha'], errors='coerce')
    except Exception as e:
        log(f"  ⚠️  Error al leer auditoría: {e}")
        return df_trabajo, None

    return df_trabajo, df_audit


def derive_delta_cardiaco(df):
    """Deriva Delta_cardiaco si existen las columnas base"""
    if 'FC_al_caminar_promedio_diario' in df.columns and 'FCr_promedio_diario' in df.columns:
        df['Delta_cardiaco'] = df['FC_al_caminar_promedio_diario'] - \
            df['FCr_promedio_diario']
        return True
    return False


def process_user(u_id):
    """
    Procesa un usuario: calcula Panel A, Panel B y comparativo.

    Args:
        u_id: número de usuario (1-10)

    Returns:
        dict con status y métricas agregadas (para consolidado)
    """
    alias = USER_MAP.get(u_id, f"u{u_id}")
    log(f"\n{'='*80}")
    log(f"Usuario u{u_id} ({alias})")
    log(f"{'='*80}")

    # Cargar datos
    df_trabajo, df_audit = load_user_data(u_id)

    if df_trabajo is None:
        return {'status': 'FAIL', 'reason': 'archivo_no_encontrado'}

    n_total = len(df_trabajo)
    log(f"  📊 Registros totales: {n_total}")

    # Derivar Delta_cardiaco
    has_delta = derive_delta_cardiaco(df_trabajo)
    if has_delta:
        log(f"  ✅ Delta_cardiaco derivado en memoria")

    # Verificar columnas disponibles
    vars_disponibles = [v for v in VARIABLES if v in df_trabajo.columns]
    vars_faltantes = [v for v in VARIABLES if v not in df_trabajo.columns]

    if vars_faltantes:
        log(f"  ⚠️  Variables no disponibles: {', '.join(vars_faltantes)}")

    if not vars_disponibles:
        log(f"  ❌ Ninguna variable disponible para análisis")
        return {'status': 'FAIL', 'reason': 'sin_variables'}

    log(f"  ✅ Variables a analizar ({len(vars_disponibles)}): {', '.join(vars_disponibles)}")

    # =========================================================================
    # PANEL B (OPERATIVA): Todo el dataset
    # =========================================================================
    log(f"\n  📈 Calculando Panel B (operativa, n={n_total})...")
    df_metrics_op = compute_panel_metrics(df_trabajo, vars_disponibles)

    if df_metrics_op.empty:
        log(f"  ❌ Panel B vacío (sin métricas calculables)")
        return {'status': 'FAIL', 'reason': 'panel_B_vacio'}

    # Guardar Panel B
    path_op = OUTPUT_DIR / f"variabilidad_operativa_u{u_id}.csv"
    df_metrics_op.to_csv(path_op, index=False)
    log(f"  ✅ Guardado: {path_op.name}")

    # =========================================================================
    # PANEL A (OBSERVADA): Solo días con FC_walk observada
    # =========================================================================
    if df_audit is None:
        log(f"  ⚠️  Sin auditoría → Panel A = Panel B (no podemos filtrar observados)")
        df_metrics_obs = df_metrics_op.copy()
        df_metrics_obs.columns = [
            c + '_obs' if c != 'variable' else c for c in df_metrics_obs.columns]
        n_obs = n_total
        pct_obs = 100.0
    else:
        # Filtrar solo observados en auditoría
        fechas_obs = df_audit[df_audit['FC_walk_fuente']
                              == 'observada']['Fecha'].dropna()

        if len(fechas_obs) == 0:
            log(f"  ⚠️  Auditoría sin registros observados → Panel A vacío")
            # Panel A vacío: métricas NaN
            df_metrics_obs = pd.DataFrame({
                'variable': vars_disponibles,
                'n_obs': 0,
                'mean_obs': np.nan,
                'std_obs': np.nan,
                'iqr_obs': np.nan,
                'mad_obs': np.nan,
                'cv_obs': np.nan,
                'p10_obs': np.nan,
                'p50_obs': np.nan,
                'p90_obs': np.nan
            })
            n_obs = 0
            pct_obs = 0.0
        else:
            # Inner join por Fecha
            df_obs = df_trabajo[df_trabajo['Fecha'].isin(fechas_obs)].copy()
            n_obs = len(df_obs)
            pct_obs = (n_obs / n_total * 100) if n_total > 0 else 0.0

            log(
                f"  📉 Calculando Panel A (observada, n={n_obs}, {pct_obs:.1f}% del total)...")
            df_metrics_obs = compute_panel_metrics(df_obs, vars_disponibles)

            if df_metrics_obs.empty:
                log(f"  ⚠️  Panel A vacío (sin métricas calculables)")

    # Guardar Panel A
    path_obs = OUTPUT_DIR / f"variabilidad_observada_u{u_id}.csv"
    df_metrics_obs.to_csv(path_obs, index=False)
    log(f"  ✅ Guardado: {path_obs.name}")

    # =========================================================================
    # COMPARATIVO DUAL
    # =========================================================================
    log(f"\n  🔀 Generando comparativo dual...")
    df_dual = make_dual_compare(df_metrics_obs, df_metrics_op)

    # Guardar comparativo
    path_dual = OUTPUT_DIR / f"variabilidad_dual_u{u_id}.csv"
    df_dual.to_csv(path_dual, index=False)
    log(f"  ✅ Guardado: {path_dual.name}")

    # =========================================================================
    # PREPARAR FILA PARA CONSOLIDADO
    # =========================================================================
    # Añadir identificadores de usuario
    df_dual_export = df_dual.copy()
    df_dual_export.insert(0, 'usuario_alias', alias)
    df_dual_export.insert(0, 'usuario_id', f"u{u_id}")

    log(f"\n  ✅ Usuario u{u_id} completado exitosamente")
    log(f"     Panel A: {n_obs} registros ({pct_obs:.1f}%)")
    log(f"     Panel B: {n_total} registros")
    log(f"     Variables: {len(vars_disponibles)}")

    return {
        'status': 'OK',
        'n_obs': n_obs,
        'n_op': n_total,
        'pct_obs': pct_obs,
        'n_vars': len(vars_disponibles),
        'df_consolidado': df_dual_export
    }


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    log("="*80)
    log("ANÁLISIS DE VARIABILIDAD DUAL - PASO 3")
    log("="*80)
    log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Directorio base: {BASE_DIR}")
    log(f"Directorio salida: {OUTPUT_DIR}")
    log("")

    # Procesar todos los usuarios
    resultados = []
    consolidado_frames = []

    for u_id in range(1, 11):
        result = process_user(u_id)
        resultados.append({
            'usuario_id': f"u{u_id}",
            'alias': USER_MAP.get(u_id, f"u{u_id}"),
            **result
        })

        if result['status'] == 'OK' and 'df_consolidado' in result:
            consolidado_frames.append(result['df_consolidado'])

    # =========================================================================
    # CONSOLIDADO GLOBAL
    # =========================================================================
    log(f"\n{'='*80}")
    log("GENERANDO CONSOLIDADO GLOBAL")
    log(f"{'='*80}")

    if consolidado_frames:
        df_consolidado = pd.concat(consolidado_frames, ignore_index=True)
        path_consolidado = OUTPUT_DIR / "variabilidad_dual_consolidado.csv"
        df_consolidado.to_csv(path_consolidado, index=False)
        log(f"✅ Consolidado guardado: {path_consolidado.name}")
        log(f"   Registros totales: {len(df_consolidado)}")
        log(f"   Usuarios cubiertos: {df_consolidado['usuario_id'].nunique()}")
        log(f"   Variables únicas: {df_consolidado['variable'].nunique()}")
    else:
        log(f"❌ No se pudo generar consolidado (sin datos válidos)")
        df_consolidado = pd.DataFrame()

    # =========================================================================
    # RESUMEN FINAL Y TOP CAMBIOS
    # =========================================================================
    log(f"\n{'='*80}")
    log("RESUMEN FINAL POR USUARIO")
    log(f"{'='*80}")
    log(f"{'Usuario':<12} {'Alias':<12} {'Status':<8} {'n_obs':<8} {'n_op':<8} {'%obs':<8} {'vars':<6}")
    log("-"*80)

    for r in resultados:
        status = r['status']
        alias = r['alias']
        u_id = r['usuario_id']

        if status == 'OK':
            log(
                f"{u_id:<12} {alias:<12} {status:<8} {r['n_obs']:<8} {r['n_op']:<8} {r['pct_obs']:<8.1f} {r['n_vars']:<6}")
        else:
            reason = r.get('reason', 'unknown')
            log(f"{u_id:<12} {alias:<12} {status:<8} {reason}")

    # Contadores
    n_ok = sum(1 for r in resultados if r['status'] == 'OK')
    n_fail = len(resultados) - n_ok

    log("")
    log(f"Usuarios completados: {n_ok}/10")
    log(f"Usuarios fallidos:    {n_fail}/10")

    # =========================================================================
    # TOP CAMBIOS DE VARIABILIDAD
    # =========================================================================
    if not df_consolidado.empty and 'ratio_std' in df_consolidado.columns:
        log(f"\n{'='*80}")
        log("TOP 10 CAMBIOS EN VARIABILIDAD (por |ratio_std - 1|)")
        log(f"{'='*80}")

        df_top = df_consolidado.copy()
        df_top['abs_ratio_diff'] = (df_top['ratio_std'] - 1.0).abs()
        df_top = df_top.dropna(subset=['abs_ratio_diff']).sort_values(
            'abs_ratio_diff', ascending=False).head(10)

        if not df_top.empty:
            log(f"{'Usuario':<10} {'Variable':<30} {'ratio_std':<12} {'delta_iqr':<12} {'Flags'}")
            log("-"*100)
            for _, row in df_top.iterrows():
                log(f"{row['usuario_id']:<10} {row['variable']:<30} {row['ratio_std']:<12.3f} {row['delta_iqr']:<12.3f} {row.get('nota_flags', '')}")
        else:
            log("(No hay cambios significativos calculables)")

    # =========================================================================
    # FINALIZACIÓN
    # =========================================================================
    log(f"\n{'='*80}")
    log("ANÁLISIS COMPLETADO")
    log(f"{'='*80}")
    log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("")
    log(f"📂 Todos los resultados en: {OUTPUT_DIR.relative_to(BASE_DIR)}")
    log("")

    # Guardar log
    log_path = OUTPUT_DIR / "03_variabilidad_dual_log.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG_LINES))

    print(f"\n✅ Log guardado en: {log_path.name}")

    return 0 if n_ok == 10 else 1


if __name__ == '__main__':
    sys.exit(main())
