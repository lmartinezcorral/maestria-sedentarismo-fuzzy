"""
Análisis de Missingness y Autocorrelación (ACF/PACF) - Paso 5
==============================================================

OBJETIVO:
---------
Caracterizar cobertura de datos y estructura temporal de señales semanales
para apoyar decisiones de clustering/fuzzy.

INSUMOS:
--------
- analisis_u/semanal/weekly_u{1..10}.csv
- analisis_u/FC_walk_imputacion_V3_u{1..10}.csv (auditoría)

SALIDAS:
--------
- missingness_y_acf/05_missingness_y_acf_log.txt
- missingness_y_acf/missingness_resumen_u{1..10}.csv
- missingness_y_acf/acf_stats_u{1..10}.csv
- missingness_y_acf/acf_plots/*.png
- missingness_y_acf/pacf_plots/*.png
- missingness_y_acf/missingness_consolidado.csv
- missingness_y_acf/acf_consolidado.csv

Autor: Pipeline automatizado
Fecha: 2025-10-16
"""

import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import warnings
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI

warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

BASE_DIR = Path(__file__).parent.resolve()  # analisis_u/
SEMANAL_DIR = BASE_DIR / 'semanal'
AUDIT_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / 'missingness_y_acf'

# Crear directorios
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / 'acf_plots').mkdir(exist_ok=True)
(OUTPUT_DIR / 'pacf_plots').mkdir(exist_ok=True)

# Variables de interés para ACF
ACF_VARIABLES = [
    'Actividad_relativa_p50', 'Actividad_relativa_iqr',
    'Superavit_calorico_basal_p50', 'Superavit_calorico_basal_iqr',
    'HRV_SDNN_p50', 'HRV_SDNN_iqr',
    'Delta_cardiaco_p50', 'Delta_cardiaco_iqr'
]

USER_MAP = {
    1: "ale", 2: "brenda", 3: "christina", 4: "edson", 5: "esmeralda",
    6: "fidel", 7: "kevin", 8: "legarda", 9: "lmartinez", 10: "vane"
}

MIN_WEEKS_ACF = 30  # Mínimo de semanas para ACF significativo

LOG_LINES = []

# ==============================================================================
# FUNCIONES
# ==============================================================================


def log(msg):
    """Registra y muestra mensaje"""
    LOG_LINES.append(msg)
    print(msg)


def analyze_missingness(df_weekly, u_id):
    """
    Analiza cobertura y missingness por semana.

    Returns:
        DataFrame con métricas por semana
    """
    results = []

    for idx, row in df_weekly.iterrows():
        semana = row.get('semana_inicio', 'NA')
        dias = row.get('dias_monitoreados', 0)
        pct_imput = row.get('pct_imputada_FC_walk', np.nan)
        flag_baja = row.get('flag_baja_cobertura', 0)

        # Aproximar run de faltantes (si dias < 7)
        max_run_faltantes = 7 - dias if dias < 7 else 0

        results.append({
            'usuario_id': f"u{u_id}",
            'semana_inicio': semana,
            'dias_monitoreados': dias,
            'dias_faltantes': 7 - dias,
            'max_run_faltantes': max_run_faltantes,
            'pct_imputada_FC_walk': pct_imput,
            'flag_baja_cobertura': flag_baja
        })

    return pd.DataFrame(results)


def compute_acf_manual(series, max_lag=20):
    """
    Calcula ACF manualmente usando pandas.Series.autocorr
    """
    s = pd.Series(series)
    acf_values = []
    for lag in range(max_lag + 1):
        try:
            acf_values.append(s.autocorr(lag=lag))
        except:
            acf_values.append(np.nan)
    return np.array(acf_values)


def compute_acf_stats(series, var_name, u_id, max_lags=20):
    """
    Calcula estadísticas ACF (simplificado sin statsmodels).

    Returns:
        dict con estadísticas
    """
    s = pd.to_numeric(series, errors='coerce').dropna()

    if len(s) < MIN_WEEKS_ACF:
        return {
            'usuario_id': f"u{u_id}",
            'variable': var_name,
            'n_weeks': len(s),
            'acf_lag1': np.nan,
            'acf_lag2': np.nan,
            'acf_lag4': np.nan,
            'status': 'insuficiente'
        }

    try:
        # ACF manual para lags específicos
        acf_lag1 = pd.Series(s).autocorr(lag=1) if len(s) > 1 else np.nan
        acf_lag2 = pd.Series(s).autocorr(lag=2) if len(s) > 2 else np.nan
        acf_lag4 = pd.Series(s).autocorr(lag=4) if len(s) > 4 else np.nan

        return {
            'usuario_id': f"u{u_id}",
            'variable': var_name,
            'n_weeks': len(s),
            'acf_lag1': acf_lag1,
            'acf_lag2': acf_lag2,
            'acf_lag4': acf_lag4,
            'status': 'OK'
        }
    except Exception as e:
        log(f"    ⚠️  Error en ACF stats para {var_name}: {e}")
        return {
            'usuario_id': f"u{u_id}",
            'variable': var_name,
            'n_weeks': len(s),
            'acf_lag1': np.nan,
            'acf_lag2': np.nan,
            'acf_lag4': np.nan,
            'status': 'error'
        }


def plot_acf_pacf(series, var_name, u_id, alias):
    """
    Genera gráficos ACF y PACF usando statsmodels.
    """
    s = pd.to_numeric(series, errors='coerce').dropna()

    if len(s) < MIN_WEEKS_ACF:
        log(f"    ⚠️  {var_name}: solo {len(s)} semanas, se omite gráfico ACF")
        return False

    try:
        # Intentar importar statsmodels
        try:
            from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
            from statsmodels.tsa.stattools import acf, pacf
            HAS_STATSMODELS = True
        except ImportError:
            HAS_STATSMODELS = False
            log(f"    ⚠️  statsmodels no disponible, usando método manual")

        max_lag = min(20, len(s)//2)

        if HAS_STATSMODELS:
            # ACF con statsmodels
            fig_acf, ax_acf = plt.subplots(figsize=(10, 4))
            plot_acf(s, lags=max_lag, ax=ax_acf, alpha=0.05)
            ax_acf.set_title(
                f'ACF: {var_name} - {alias} (u{u_id})', fontsize=10)
            ax_acf.set_xlabel('Lag (semanas)')
            plt.tight_layout()
            acf_path = OUTPUT_DIR / 'acf_plots' / f'acf_{var_name}_u{u_id}.png'
            fig_acf.savefig(acf_path, dpi=100)
            plt.close(fig_acf)

            # PACF con statsmodels
            fig_pacf, ax_pacf = plt.subplots(figsize=(10, 4))
            plot_pacf(s, lags=max_lag, ax=ax_pacf, alpha=0.05, method='ywm')
            ax_pacf.set_title(
                f'PACF: {var_name} - {alias} (u{u_id})', fontsize=10)
            ax_pacf.set_xlabel('Lag (semanas)')
            plt.tight_layout()
            pacf_path = OUTPUT_DIR / 'pacf_plots' / \
                f'pacf_{var_name}_u{u_id}.png'
            fig_pacf.savefig(pacf_path, dpi=100)
            plt.close(fig_pacf)

        else:
            # Fallback manual (ACF)
            acf_values = compute_acf_manual(s, max_lag)
            conf_int = 1.96 / np.sqrt(len(s))

            fig_acf, ax_acf = plt.subplots(figsize=(10, 4))
            lags = np.arange(len(acf_values))
            ax_acf.stem(lags, acf_values, linefmt='C0-',
                        markerfmt='C0o', basefmt=' ')
            ax_acf.axhline(y=conf_int, linestyle='--', color='gray', alpha=0.5)
            ax_acf.axhline(y=-conf_int, linestyle='--',
                           color='gray', alpha=0.5)
            ax_acf.axhline(y=0, linestyle='-', color='black', linewidth=0.8)
            ax_acf.set_title(
                f'ACF: {var_name} - {alias} (u{u_id})', fontsize=10)
            ax_acf.set_xlabel('Lag (semanas)')
            ax_acf.set_ylabel('Autocorrelación')
            ax_acf.set_ylim([-1, 1])
            plt.tight_layout()
            acf_path = OUTPUT_DIR / 'acf_plots' / f'acf_{var_name}_u{u_id}.png'
            fig_acf.savefig(acf_path, dpi=100)
            plt.close(fig_acf)

            # PACF placeholder si no hay statsmodels
            pacf_path = OUTPUT_DIR / 'pacf_plots' / \
                f'pacf_{var_name}_u{u_id}.png'
            fig_dummy, ax_dummy = plt.subplots(figsize=(10, 4))
            ax_dummy.text(0.5, 0.5, 'PACF omitido\n(requiere statsmodels)',
                          ha='center', va='center', fontsize=12)
            ax_dummy.set_title(
                f'PACF: {var_name} - {alias} (u{u_id})', fontsize=10)
            ax_dummy.axis('off')
            plt.tight_layout()
            fig_dummy.savefig(pacf_path, dpi=100)
            plt.close(fig_dummy)

        return True

    except Exception as e:
        log(f"    ❌ Error al graficar {var_name}: {e}")
        return False


def process_user(u_id):
    """
    Procesa missingness y ACF para un usuario.

    Returns:
        tuple (df_missing, df_acf_stats, n_plots)
    """
    alias = USER_MAP.get(u_id, f"u{u_id}")
    log(f"\n{'='*80}")
    log(f"Usuario u{u_id} ({alias})")
    log(f"{'='*80}")

    # Cargar datos semanales
    weekly_path = SEMANAL_DIR / f"weekly_u{u_id}.csv"
    if not weekly_path.exists():
        log(f"  ❌ No se encontró: {weekly_path.name}")
        return None, None, 0

    try:
        df_weekly = pd.read_csv(weekly_path)
        n_weeks = len(df_weekly)
        log(f"  ✅ Datos semanales cargados: {n_weeks} semanas")
    except Exception as e:
        log(f"  ❌ Error al leer {weekly_path.name}: {e}")
        return None, None, 0

    # Análisis de missingness
    log(f"\n  📊 Analizando missingness...")
    df_missing = analyze_missingness(df_weekly, u_id)

    dias_promedio = df_missing['dias_monitoreados'].mean()
    pct_baja_cob = (
        df_missing['flag_baja_cobertura'].sum() / len(df_missing) * 100)
    pct_imput_mean = df_missing['pct_imputada_FC_walk'].mean()

    log(f"     - Días monitoreados (promedio): {dias_promedio:.1f}/7")
    log(f"     - Semanas con baja cobertura: {pct_baja_cob:.1f}%")
    if not np.isnan(pct_imput_mean):
        log(f"     - % imputada FC_walk (promedio): {pct_imput_mean:.1f}%")

    # Guardar missingness individual
    miss_path = OUTPUT_DIR / f"missingness_resumen_u{u_id}.csv"
    df_missing.to_csv(miss_path, index=False)
    log(f"  ✅ Guardado: {miss_path.name}")

    # ACF/PACF analysis
    log(f"\n  📈 Analizando ACF/PACF...")

    acf_stats_list = []
    n_plots = 0

    for var in ACF_VARIABLES:
        if var not in df_weekly.columns:
            log(f"    ⚠️  Variable {var} no encontrada")
            continue

        # Estadísticas ACF
        stats = compute_acf_stats(df_weekly[var], var, u_id)
        acf_stats_list.append(stats)

        # Gráficos
        if stats['status'] == 'OK':
            if plot_acf_pacf(df_weekly[var], var, u_id, alias):
                n_plots += 2  # ACF + PACF

    df_acf_stats = pd.DataFrame(acf_stats_list)

    # Guardar ACF stats
    acf_path = OUTPUT_DIR / f"acf_stats_u{u_id}.csv"
    df_acf_stats.to_csv(acf_path, index=False)
    log(f"  ✅ Guardado: {acf_path.name}")
    log(f"  ✅ Gráficos generados: {n_plots}")

    return df_missing, df_acf_stats, n_plots


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    log("="*80)
    log("ANÁLISIS DE MISSINGNESS Y ACF - PASO 5")
    log("="*80)
    log(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Directorio base: {BASE_DIR}")
    log(f"Directorio salida: {OUTPUT_DIR}")
    log("")

    missing_frames = []
    acf_frames = []
    total_plots = 0

    for u_id in range(1, 11):
        df_miss, df_acf, n_plots = process_user(u_id)

        if df_miss is not None:
            missing_frames.append(df_miss)
        if df_acf is not None:
            acf_frames.append(df_acf)

        total_plots += n_plots

    # =========================================================================
    # CONSOLIDADOS
    # =========================================================================
    log(f"\n{'='*80}")
    log("GENERANDO CONSOLIDADOS")
    log(f"{'='*80}")

    if missing_frames:
        df_miss_consol = pd.concat(missing_frames, ignore_index=True)
        miss_consol_path = OUTPUT_DIR / "missingness_consolidado.csv"
        df_miss_consol.to_csv(miss_consol_path, index=False)
        log(f"✅ Missingness consolidado: {miss_consol_path.name}")
        log(f"   Registros: {len(df_miss_consol)} semanas")
    else:
        log(f"❌ Sin datos de missingness")

    if acf_frames:
        df_acf_consol = pd.concat(acf_frames, ignore_index=True)
        acf_consol_path = OUTPUT_DIR / "acf_consolidado.csv"
        df_acf_consol.to_csv(acf_consol_path, index=False)
        log(f"✅ ACF consolidado: {acf_consol_path.name}")
        log(f"   Registros: {len(df_acf_consol)} análisis")
    else:
        log(f"❌ Sin datos de ACF")

    # =========================================================================
    # RESUMEN Y VALIDACIONES
    # =========================================================================
    log(f"\n{'='*80}")
    log("RESUMEN Y VALIDACIONES")
    log(f"{'='*80}")

    log(f"Total de gráficos ACF/PACF generados: {total_plots}")
    log(f"Esperado mínimo: 60 (permitir variación por datos insuficientes)")

    if total_plots >= 60:
        log(f"✅ Criterio cumplido (≥60 gráficos)")
    else:
        log(f"⚠️  Menos de 60 gráficos generados (posibles usuarios con <30 semanas)")

    # Validar archivos consolidados
    if missing_frames and len(df_miss_consol) > 100:
        log(f"✅ Missingness consolidado con datos suficientes")
    else:
        log(f"⚠️  Missingness consolidado con pocos datos")

    if acf_frames:
        n_ok = (df_acf_consol['status'] == 'OK').sum()
        log(f"✅ ACF stats: {n_ok}/{len(df_acf_consol)} análisis exitosos")

    # =========================================================================
    # FINALIZACIÓN
    # =========================================================================
    log(f"\n{'='*80}")
    log("ANÁLISIS COMPLETADO")
    log(f"{'='*80}")
    log(f"Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("")
    log(f"📂 Salidas generadas:")
    log(f"   - 10 archivos missingness_resumen_uN.csv")
    log(f"   - 10 archivos acf_stats_uN.csv")
    log(f"   - {total_plots} gráficos ACF/PACF")
    log(f"   - 2 archivos consolidados")
    log("")

    # Guardar log
    log_path = OUTPUT_DIR / "05_missingness_y_acf_log.txt"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG_LINES))

    print(f"\n✅ Log guardado en: {log_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
