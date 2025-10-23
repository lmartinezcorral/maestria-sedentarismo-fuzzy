"""
Agregar Variables Derivadas - Pipeline de Sedentarismo
========================================================
Agrega Actividad_relativa y Superavit_calorico_basal a cada archivo individual DB_final_v3_uN.csv

Variables derivadas:
- Actividad_relativa = min_totales_en_movimiento / (60 * Total_hrs_monitorizadas)
- Superavit_calorico_basal = (Gasto_calorico_activo * 100) / TMB

Nota: SUSTITUYE (no duplica) variables base para evitar multicolinealidad:
- Actividad_relativa → sustituye min_totales_en_movimiento
- Superavit_calorico_basal → sustituye Gasto_calorico_activo

Autor: Pipeline automatizado
Fecha: 2025-10-16
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

# Mapeo usuario ↔ características antropométricas
USUARIOS_INFO = {
    'u1': {'nombre': 'ale', 'sexo': 'Mujer', 'estatura': 170, 'peso': 68, 'edad': 34},
    'u2': {'nombre': 'brenda', 'sexo': 'Mujer', 'estatura': 169, 'peso': 76, 'edad': 37},
    'u3': {'nombre': 'christina', 'sexo': 'Mujer', 'estatura': 164, 'peso': 77, 'edad': 39},
    'u4': {'nombre': 'edson', 'sexo': 'Hombre', 'estatura': 180, 'peso': 100, 'edad': 25},
    'u5': {'nombre': 'esmeralda', 'sexo': 'Mujer', 'estatura': 160, 'peso': 64, 'edad': 28},
    'u6': {'nombre': 'fidel', 'sexo': 'Hombre', 'estatura': 180, 'peso': 100, 'edad': 34},
    'u7': {'nombre': 'kevin', 'sexo': 'Hombre', 'estatura': 156, 'peso': 92, 'edad': 32},
    'u8': {'nombre': 'legarda', 'sexo': 'Hombre', 'estatura': 181, 'peso': 92, 'edad': 29},
    'u9': {'nombre': 'lmartinez', 'sexo': 'Hombre', 'estatura': 185, 'peso': 124, 'edad': 32},
    'u10': {'nombre': 'vane', 'sexo': 'Mujer', 'estatura': 164, 'peso': 58, 'edad': 28}
}

BASE_DIR = Path('.').resolve()

# ==============================================================================
# FUNCIONES
# ==============================================================================


def calcular_tmb(sexo, peso, estatura, edad):
    """
    Calcula la Tasa Metabólica Basal según la fórmula de Mifflin-St Jeor.

    Hombres: TMB = (10 * peso) + (6.25 * estatura) - (5 * edad) + 5
    Mujeres: TMB = (10 * peso) + (6.25 * estatura) - (5 * edad) - 161

    Args:
        sexo: 'Hombre' o 'Mujer'
        peso: peso en kg
        estatura: estatura en cm
        edad: edad en años

    Returns:
        TMB en kcal/día
    """
    tmb_base = (10 * peso) + (6.25 * estatura) - (5 * edad)

    if sexo == 'Hombre':
        return tmb_base + 5
    else:  # Mujer
        return tmb_base - 161


def agregar_variables_derivadas(usuario_id, info):
    """
    Agrega variables derivadas a archivo individual de usuario.

    Args:
        usuario_id: 'u1', 'u2', ..., 'u10'
        info: dict con {nombre, sexo, estatura, peso, edad}

    Returns:
        dict con estadísticas del procesamiento
    """
    archivo = BASE_DIR / f'DB_final_v3_{usuario_id}.csv'

    stats = {
        'usuario_id': usuario_id,
        'usuario_nombre': info['nombre'],
        'archivo': str(archivo),
        'existe': False,
        'procesado': False,
        'n_registros': 0,
        'tmb': 0.0,
        'actividad_relativa_mean': 0.0,
        'superavit_calorico_mean': 0.0,
        'error': None
    }

    if not archivo.exists():
        stats['error'] = f"Archivo no encontrado: {archivo}"
        print(f"❌ {usuario_id} ({info['nombre']}): Archivo no encontrado")
        return stats

    stats['existe'] = True

    try:
        # Leer dataset
        df = pd.read_csv(archivo)
        stats['n_registros'] = len(df)

        # Calcular TMB (constante por usuario)
        tmb = calcular_tmb(info['sexo'], info['peso'],
                           info['estatura'], info['edad'])
        stats['tmb'] = tmb

        # 1. Calcular Actividad_relativa
        # Formula: min_totales_en_movimiento / (60 * Total_hrs_monitorizadas)
        # Evita división por cero
        df['Actividad_relativa'] = np.where(
            df['Total_hrs_monitorizadas'] > 0,
            df['min_totales_en_movimiento'] /
            (60 * df['Total_hrs_monitorizadas']),
            0.0
        )

        # 2. Agregar TMB como metadata (útil para trazabilidad, pero no para modelado)
        df['TMB'] = tmb

        # 3. Calcular Superavit_calorico_basal
        # Formula: (Gasto_calorico_activo * 100) / TMB
        # Evita división por cero (aunque TMB nunca debería ser 0)
        if 'Gasto_calorico_activo' in df.columns:
            df['Superavit_calorico_basal'] = (
                df['Gasto_calorico_activo'] * 100) / tmb
        else:
            stats['error'] = "Falta columna Gasto_calorico_activo"
            print(
                f"❌ {usuario_id} ({info['nombre']}): Falta Gasto_calorico_activo")
            return stats

        # 4. SUSTITUIR variables base (no duplicar)
        # Eliminar min_totales_en_movimiento (sustituido por Actividad_relativa)
        if 'min_totales_en_movimiento' in df.columns:
            df = df.drop(columns=['min_totales_en_movimiento'])

        # Eliminar Gasto_calorico_activo (sustituido por Superavit_calorico_basal)
        if 'Gasto_calorico_activo' in df.columns:
            df = df.drop(columns=['Gasto_calorico_activo'])

        # Reordenar columnas (variables derivadas al final, TMB penúltima)
        cols_base = [c for c in df.columns if c not in [
            'Actividad_relativa', 'TMB', 'Superavit_calorico_basal']]
        df = df[cols_base + ['Actividad_relativa',
                             'Superavit_calorico_basal', 'TMB']]

        # Estadísticas de las nuevas variables
        stats['actividad_relativa_mean'] = df['Actividad_relativa'].mean()
        stats['superavit_calorico_mean'] = df['Superavit_calorico_basal'].mean()

        # Guardar archivo actualizado
        df.to_csv(archivo, index=False)
        stats['procesado'] = True

        print(f"✅ {usuario_id} ({info['nombre']}): {stats['n_registros']} registros, "
              f"TMB={tmb:.1f}, Act_rel_mean={stats['actividad_relativa_mean']:.3f}, "
              f"Sup_cal_mean={stats['superavit_calorico_mean']:.1f}%")

    except Exception as e:
        stats['error'] = str(e)
        print(f"❌ {usuario_id} ({info['nombre']}): Error - {e}")

    return stats


def generar_reporte(all_stats):
    """Genera reporte de procesamiento."""
    reporte_file = BASE_DIR / 'reporte_variables_derivadas.txt'

    with open(reporte_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("REPORTE: VARIABLES DERIVADAS AGREGADAS\n")
        f.write("="*80 + "\n\n")

        total_procesados = sum(1 for s in all_stats if s['procesado'])
        total_esperados = len(USUARIOS_INFO)

        f.write(
            f"Archivos procesados: {total_procesados}/{total_esperados}\n\n")

        f.write("-"*80 + "\n")
        f.write("DETALLES POR USUARIO\n")
        f.write("-"*80 + "\n\n")

        for stats in all_stats:
            f.write(f"{stats['usuario_id']} ({stats['usuario_nombre']}):\n")
            f.write(f"  Archivo: {stats['archivo']}\n")
            f.write(f"  Procesado: {stats['procesado']}\n")

            if stats['procesado']:
                f.write(f"  Registros: {stats['n_registros']}\n")
                f.write(f"  TMB: {stats['tmb']:.2f} kcal/día\n")
                f.write(
                    f"  Actividad_relativa (media): {stats['actividad_relativa_mean']:.4f}\n")
                f.write(
                    f"  Superavit_calorico_basal (media): {stats['superavit_calorico_mean']:.2f}%\n")
            else:
                f.write(f"  Error: {stats['error']}\n")
            f.write("\n")

        f.write("-"*80 + "\n")
        f.write("RESUMEN\n")
        f.write("-"*80 + "\n")
        f.write(f"Total procesados: {total_procesados}/{total_esperados}\n")

        if total_procesados == total_esperados:
            f.write("\n✅ TODAS LAS VARIABLES DERIVADAS AGREGADAS EXITOSAMENTE\n")
            f.write("   Próximo paso: Paso 3 - Análisis de Variabilidad Dual\n")
        else:
            f.write("\n⚠️  PROCESAMIENTO INCOMPLETO\n")
            f.write("   Revisar errores arriba\n")

        f.write("\n" + "="*80 + "\n")

    print(f"\n📄 Reporte generado: {reporte_file}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("="*80)
    print("AGREGAR VARIABLES DERIVADAS")
    print("="*80)
    print()
    print("Variables a agregar:")
    print("  1. Actividad_relativa = min_totales_en_movimiento / (60 * Total_hrs_monitorizadas)")
    print("  2. Superavit_calorico_basal = (Gasto_calorico_activo * 100) / TMB")
    print()
    print("Sustituciones (evitar multicolinealidad):")
    print("  - Actividad_relativa → sustituye min_totales_en_movimiento")
    print("  - Superavit_calorico_basal → sustituye Gasto_calorico_activo")
    print()
    print("-"*80)

    all_stats = []

    for usuario_id, info in USUARIOS_INFO.items():
        stats = agregar_variables_derivadas(usuario_id, info)
        all_stats.append(stats)

    print()
    print("="*80)
    print("GENERANDO REPORTE")
    print("="*80)

    generar_reporte(all_stats)

    total_procesados = sum(1 for s in all_stats if s['procesado'])

    print()
    print("="*80)
    print("RESUMEN")
    print("="*80)
    print(f"Archivos procesados: {total_procesados}/10")

    if total_procesados == 10:
        print("\n✅ VARIABLES DERIVADAS COMPLETADAS")
        print("   Listo para Paso 3: Análisis de Variabilidad Dual")
    else:
        print("\n⚠️  PROCESAMIENTO INCOMPLETO")
        print("   Revisar errores en reporte")

    print("="*80)


if __name__ == '__main__':
    main()

