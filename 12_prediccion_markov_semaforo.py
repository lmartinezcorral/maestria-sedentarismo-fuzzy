"""
12_prediccion_markov_semaforo.py
Herramienta operativa para:
  1) Construir semáforo semanal desde Sedentarismo_score (verde/amarillo/rojo)
  2) Estimar matriz de transición de Markov (global y por usuario)
  3) Evaluar predicción 1-paso (t->t+1) con dicha matriz
  4) Predecir el estado de la próxima semana por usuario

Entradas por defecto:
  - analisis_u/fuzzy/fuzzy_output.csv (columnas: usuario_id, semana_inicio, Sedentarismo_score, ...)

Salidas:
  - analisis_u/prediccion/semaforo_semanal.csv
  - analisis_u/prediccion/matriz_transicion_global.csv
  - analisis_u/prediccion/matriz_transicion_por_usuario.csv
  - analisis_u/prediccion/predicciones_backtest.csv
  - analisis_u/prediccion/prediccion_proxima_semana_por_usuario.csv
  - analisis_u/prediccion/reporte_markov.txt
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


# ======================================================================================
# UTILIDADES DE LOG Y RUTAS
# ======================================================================================

BASE_DIR = Path(__file__).parent.resolve()
DEFAULT_INPUT = BASE_DIR / 'analisis_u' / 'fuzzy' / 'fuzzy_output.csv'
OUTPUT_DIR = BASE_DIR / 'analisis_u' / 'prediccion'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REPORTE_FILE = OUTPUT_DIR / 'reporte_markov.txt'


def log(msg: str) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(msg)
    with open(REPORTE_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {msg}\n")


# ======================================================================================
# PARAMETRIZACIÓN
# ======================================================================================

@dataclass
class Thresholds:
    green_max: float  # límite superior de verde (incluyente)
    red_min: float    # límite inferior de rojo (incluyente)

    def to_tuple(self) -> Tuple[float, float]:
        return (self.green_max, self.red_min)


# ======================================================================================
# SEMÁFORO Y ESTADOS
# ======================================================================================

ESTADO_TO_IDX = {
    'verde': 0,
    'amarillo': 1,
    'rojo': 2,
}
IDX_TO_ESTADO = {v: k for k, v in ESTADO_TO_IDX.items()}


def asignar_semaforo(score: float, th: Thresholds) -> str:
    if pd.isna(score):
        return 'amarillo'
    if score <= th.green_max:
        return 'verde'
    if score >= th.red_min:
        return 'rojo'
    return 'amarillo'


def calcular_terciles_globales(scores: pd.Series) -> Thresholds:
    scores = pd.to_numeric(scores, errors='coerce').dropna()
    if len(scores) == 0:
        # valores por defecto robustos
        return Thresholds(green_max=0.33, red_min=0.67)

    q33, q67 = np.percentile(scores, [33.33, 66.67])

    # Proteger terciles degenerados
    if not np.isfinite(q33) or not np.isfinite(q67) or q33 == q67:
        q33, q67 = 0.33, 0.67

    # Asegurar orden
    green_max = float(min(max(q33, 0.0), 1.0))
    red_min = float(min(max(q67, green_max + 1e-6), 1.0))
    return Thresholds(green_max=green_max, red_min=red_min)


# ======================================================================================
# MARKOV: MATRICES DE TRANSICIÓN
# ======================================================================================

@dataclass
class MatrizTransicion:
    counts: np.ndarray  # 3x3 conteos
    probs: np.ndarray   # 3x3 probabilidades (filas normalizadas)


def estimar_matriz_transicion(estado_idxs_ordenados: List[int]) -> MatrizTransicion:
    counts = np.zeros((3, 3), dtype=int)
    estados = [e for e in estado_idxs_ordenados if e in (0, 1, 2)]

    for i in range(len(estados) - 1):
        a = estados[i]
        b = estados[i + 1]
        counts[a, b] += 1

    probs = counts.astype(float)
    for i in range(3):
        fila_sum = probs[i, :].sum()
        if fila_sum > 0:
            probs[i, :] /= fila_sum
        else:
            # si no hay transiciones observadas desde i, asumir alta persistencia
            probs[i, i] = 1.0

    return MatrizTransicion(counts=counts, probs=probs)


def matriz_transicion_global(df: pd.DataFrame) -> MatrizTransicion:
    counts_global = np.zeros((3, 3), dtype=int)

    for _, df_u in df.groupby('usuario_id'):
        df_u = df_u.sort_values('semana_inicio')
        estados = df_u['estado_idx'].astype(int).tolist()
        mt_u = estimar_matriz_transicion(estados)
        counts_global += mt_u.counts

    probs_global = counts_global.astype(float)
    for i in range(3):
        s = probs_global[i, :].sum()
        if s > 0:
            probs_global[i, :] /= s
        else:
            probs_global[i, i] = 1.0

    return MatrizTransicion(counts=counts_global, probs=probs_global)


def matrices_transicion_por_usuario(df: pd.DataFrame) -> Dict[str, MatrizTransicion]:
    result: Dict[str, MatrizTransicion] = {}
    for user_id, df_u in df.groupby('usuario_id'):
        df_u = df_u.sort_values('semana_inicio')
        estados = df_u['estado_idx'].astype(int).tolist()
        result[user_id] = estimar_matriz_transicion(estados)
    return result


def matriz_potencia(P: np.ndarray, h: int) -> np.ndarray:
    if h <= 1:
        return P.copy()
    M = np.eye(P.shape[0])
    A = P.copy()
    e = h
    # exponenciación binaria
    while e > 0:
        if e % 2 == 1:
            M = M @ A
        A = A @ A
        e //= 2
    return M


# ======================================================================================
# PREDICCIONES Y MÉTRICAS
# ======================================================================================

@dataclass
class PrediccionBacktest:
    user: str
    fecha_t: pd.Timestamp
    estado_t: int
    estado_t1_real: int
    estado_t1_pred: int


def predecir_siguiente_estado(P: np.ndarray, estado_actual: int) -> Tuple[int, np.ndarray]:
    probs = P[estado_actual, :]
    return int(np.argmax(probs)), probs


def evaluar_backtest_un_paso(df: pd.DataFrame, P: np.ndarray) -> Tuple[pd.DataFrame, float]:
    registros: List[Dict] = []

    for user_id, df_u in df.groupby('usuario_id'):
        df_u = df_u.sort_values('semana_inicio').reset_index(drop=True)
        estados = df_u['estado_idx'].astype(int).tolist()
        fechas = pd.to_datetime(df_u['semana_inicio'])

        for i in range(len(estados) - 1):
            estado_t = estados[i]
            estado_t1_real = estados[i + 1]
            estado_t1_pred, _ = predecir_siguiente_estado(P, estado_t)
            registros.append({
                'usuario_id': user_id,
                'semana_inicio_t': fechas.iloc[i].date(),
                'estado_t': estado_t,
                'estado_t_label': IDX_TO_ESTADO[estado_t],
                'estado_t1_real': estado_t1_real,
                'estado_t1_real_label': IDX_TO_ESTADO[estado_t1_real],
                'estado_t1_pred': estado_t1_pred,
                'estado_t1_pred_label': IDX_TO_ESTADO[estado_t1_pred],
                'acierto': int(estado_t1_pred == estado_t1_real),
            })

    df_bt = pd.DataFrame(registros)
    acc = float(df_bt['acierto'].mean()) if not df_bt.empty else float('nan')
    return df_bt, acc


def predecir_proxima_semana_por_usuario(df: pd.DataFrame, P: np.ndarray, horizon_weeks: int = 1) -> pd.DataFrame:
    filas: List[Dict] = []

    for user_id, df_u in df.groupby('usuario_id'):
        df_u = df_u.sort_values('semana_inicio')
        if df_u.empty:
            continue
        last_row = df_u.iloc[-1]
        estado_actual = int(last_row['estado_idx'])
        fecha_ultima = pd.to_datetime(last_row['semana_inicio'])

        P_h = matriz_potencia(P, horizon_weeks)
        pred_idx, probs = predecir_siguiente_estado(P_h, estado_actual)

        filas.append({
            'usuario_id': user_id,
            'semana_ultima_observada': fecha_ultima.date(),
            'estado_actual_idx': estado_actual,
            'estado_actual_label': IDX_TO_ESTADO[estado_actual],
            'horizonte_semanas': horizon_weeks,
            'semana_predicha_inicio': (fecha_ultima + timedelta(days=7 * horizon_weeks)).date(),
            'estado_predicho_idx': int(pred_idx),
            'estado_predicho_label': IDX_TO_ESTADO[int(pred_idx)],
            'prob_verde': float(probs[0]),
            'prob_amarillo': float(probs[1]),
            'prob_rojo': float(probs[2]),
        })

    return pd.DataFrame(filas)


# ======================================================================================
# MAIN
# ======================================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description='Predicción temporal con matriz de transición de Markov y semáforo semanal')
    parser.add_argument('--input', type=str, default=str(DEFAULT_INPUT), help='Ruta de fuzzy_output.csv')
    parser.add_argument('--output-dir', type=str, default=str(OUTPUT_DIR), help='Directorio de salida')
    parser.add_argument('--threshold-mode', type=str, choices=['global_terciles', 'fixed'], default='global_terciles', help='Modo para definir semáforo')
    parser.add_argument('--green-max', type=float, default=0.3333, help='Umbral superior verde (cuando threshold-mode=fixed)')
    parser.add_argument('--red-min', type=float, default=0.6667, help='Umbral inferior rojo (cuando threshold-mode=fixed)')
    parser.add_argument('--horizon', type=int, default=1, help='Horizonte de predicción en semanas (para próxima semana por usuario)')

    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Limpiar reporte previo
    if REPORTE_FILE.exists():
        REPORTE_FILE.unlink()

    log('=' * 100)
    log('PREDICCIÓN MARKOV + SEMÁFORO - PASO 12')
    log('=' * 100)

    if not input_path.exists():
        log(f'❌ ERROR: No existe {input_path}')
        return

    # ----------------------------------------------------------------------------------
    # 1) CARGA DE DATOS
    # ----------------------------------------------------------------------------------
    df = pd.read_csv(input_path)
    if 'usuario_id' not in df.columns or 'semana_inicio' not in df.columns or 'Sedentarismo_score' not in df.columns:
        log('❌ ERROR: fuzzy_output.csv no contiene las columnas requeridas: usuario_id, semana_inicio, Sedentarismo_score')
        return

    df['semana_inicio'] = pd.to_datetime(df['semana_inicio'], errors='coerce')
    df = df.dropna(subset=['semana_inicio']).sort_values(['usuario_id', 'semana_inicio']).reset_index(drop=True)

    log(f'✅ Datos cargados: {len(df)} semanas, {df["usuario_id"].nunique()} usuarios')

    # ----------------------------------------------------------------------------------
    # 2) SEMÁFORO SEMANAL
    # ----------------------------------------------------------------------------------
    if args.threshold_mode == 'global_terciles':
        th = calcular_terciles_globales(df['Sedentarismo_score'])
    else:
        th = Thresholds(green_max=float(args.green_max), red_min=float(args.red_min))
        # Validación básica
        if not (0.0 <= th.green_max < th.red_min <= 1.0):
            log('⚠️  Umbrales inválidos; usando valores por defecto 0.33 y 0.67')
            th = Thresholds(0.33, 0.67)

    log(f'🟢 Umbral verde (≤): {th.green_max:.4f} | 🔴 Umbral rojo (≥): {th.red_min:.4f}')

    df['semaforo'] = df['Sedentarismo_score'].apply(lambda x: asignar_semaforo(x, th))
    df['estado_idx'] = df['semaforo'].map(ESTADO_TO_IDX).astype(int)

    semaforo_out = out_dir / 'semaforo_semanal.csv'
    df[['usuario_id', 'semana_inicio', 'Sedentarismo_score', 'semaforo', 'estado_idx']].to_csv(semaforo_out, index=False)
    log(f'✅ Guardado semáforo semanal: {semaforo_out.name}')

    # ----------------------------------------------------------------------------------
    # 3) MATRIZ DE TRANSICIÓN (GLOBAL y POR USUARIO)
    # ----------------------------------------------------------------------------------
    mt_global = matriz_transicion_global(df)

    # Guardar matrices globales
    trans_counts_path = out_dir / 'matriz_transicion_global.csv'
    trans_probs_path = out_dir / 'matriz_transicion_global_probs.csv'

    counts_df = pd.DataFrame(mt_global.counts, index=[f'act_{IDX_TO_ESTADO[i]}' for i in range(3)], columns=[f'next_{IDX_TO_ESTADO[j]}' for j in range(3)])
    probs_df = pd.DataFrame(mt_global.probs, index=[f'act_{IDX_TO_ESTADO[i]}' for i in range(3)], columns=[f'next_{IDX_TO_ESTADO[j]}' for j in range(3)])

    counts_df.to_csv(trans_counts_path)
    probs_df.to_csv(trans_probs_path)
    log(f'✅ Guardada matriz de transición global (conteos): {trans_counts_path.name}')
    log(f'✅ Guardada matriz de transición global (probs): {trans_probs_path.name}')

    # Por usuario
    mt_por_usuario = matrices_transicion_por_usuario(df)
    filas_mt_u: List[Dict] = []
    for user_id, mt in mt_por_usuario.items():
        fila = {'usuario_id': user_id}
        # aplanar conteos y probs con etiquetas legibles
        for i in range(3):
            for j in range(3):
                fila[f'count_{IDX_TO_ESTADO[i]}_to_{IDX_TO_ESTADO[j]}'] = int(mt.counts[i, j])
                fila[f'prob_{IDX_TO_ESTADO[i]}_to_{IDX_TO_ESTADO[j]}'] = float(mt.probs[i, j])
        filas_mt_u.append(fila)

    df_mt_u = pd.DataFrame(filas_mt_u)
    trans_user_path = out_dir / 'matriz_transicion_por_usuario.csv'
    df_mt_u.to_csv(trans_user_path, index=False)
    log(f'✅ Guardada matriz de transición por usuario: {trans_user_path.name}')

    # ----------------------------------------------------------------------------------
    # 4) BACKTEST 1-PASO (t -> t+1)
    # ----------------------------------------------------------------------------------
    df_bt, acc = evaluar_backtest_un_paso(df, mt_global.probs)
    bt_out = out_dir / 'predicciones_backtest.csv'
    df_bt.to_csv(bt_out, index=False)
    n_pred = len(df_bt)
    log(f'✅ Guardado backtest 1-paso ({n_pred} transiciones): {bt_out.name}')
    log(f'🎯 Precisión 1-paso (global): {acc:.3f}' if n_pred > 0 else '⚠️  Sin transiciones suficientes para backtest')

    # ----------------------------------------------------------------------------------
    # 5) PREDICCIÓN PRÓXIMA SEMANA POR USUARIO
    # ----------------------------------------------------------------------------------
    df_next = predecir_proxima_semana_por_usuario(df, mt_global.probs, horizon_weeks=int(args.horizon))
    next_out = out_dir / 'prediccion_proxima_semana_por_usuario.csv'
    df_next.to_csv(next_out, index=False)
    log(f'✅ Guardado: {next_out.name}')

    # ----------------------------------------------------------------------------------
    # 6) RESUMEN EN REPORTE
    # ----------------------------------------------------------------------------------
    log('')
    log('📊 RESUMEN MATRIZ GLOBAL (Probs):')
    for i in range(3):
        fila = ', '.join([f"P({IDX_TO_ESTADO[i]}→{IDX_TO_ESTADO[j]})={mt_global.probs[i, j]:.2f}" for j in range(3)])
        log(f"  {fila}")

    log('')
    log('✅ Proceso completado. Artefactos en analisis_u/prediccion/')


if __name__ == '__main__':
    main()
