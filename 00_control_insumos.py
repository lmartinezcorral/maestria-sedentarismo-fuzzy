"""
Control de Insumos - Pipeline de Sedentarismo
==============================================
Prepara zona de trabajo copiando auditorías FC_walk y verificando datasets diarios.

Tareas:
1. Copiar FC_walk_imputacion_V3.csv desde carpetas inmutables → analisis_u/
2. Verificar presencia de DB_final_v3_uN.csv en zona de trabajo
3. Generar log de control con estadísticas

Autor: Pipeline automatizado
Fecha: 2025-10-16
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

# Mapeo usuario ↔ carpeta original
USUARIOS = {
    'u1': 'ale',
    'u2': 'brenda',
    'u3': 'christina',
    'u4': 'edson',
    'u5': 'esmeralda',
    'u6': 'fidel',
    'u7': 'kevin',
    'u8': 'legarda',
    'u9': 'lmartinez',
    'u10': 'vane'
}

# Rutas base
BASE_DIR = Path('.').resolve()  # Resolver a ruta absoluta
# Subir un nivel desde "4 semestre_dataset" para llegar a "Datos", luego bajar a "apple_health_export"
ORIGEN_BASE = BASE_DIR.parent / 'apple_health_export'
DESTINO_AUDITORIAS = BASE_DIR / 'analisis_u'

# Archivos
AUDITORIA_ORIGINAL = 'FC_walk_imputacion_V3.csv'
DATASET_TRABAJO = 'DB_final_v3'

# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================


def crear_carpetas():
    """Crea carpetas de salida si no existen."""
    DESTINO_AUDITORIAS.mkdir(exist_ok=True)
    print(f"✅ Carpeta {DESTINO_AUDITORIAS} lista")


def copiar_auditoria(usuario_id, usuario_nombre):
    """
    Copia auditoría FC_walk desde carpeta inmutable a zona de trabajo.

    Args:
        usuario_id: 'u1', 'u2', ..., 'u10'
        usuario_nombre: 'ale', 'brenda', ..., 'vane'

    Returns:
        dict con estadísticas de la auditoría
    """
    # Ruta origen (INMUTABLE - solo lectura)
    origen = ORIGEN_BASE / \
        f'apple_health_export_{usuario_nombre}' / AUDITORIA_ORIGINAL

    # Ruta destino (zona de trabajo)
    destino = DESTINO_AUDITORIAS / f'FC_walk_imputacion_V3_{usuario_id}.csv'

    stats = {
        'usuario_id': usuario_id,
        'usuario_nombre': usuario_nombre,
        'origen': str(origen),
        'destino': str(destino),
        'existe_origen': False,
        'copiado': False,
        'n_registros': 0,
        'fuente_counts': {},
        'fecha_min': None,
        'fecha_max': None
    }

    # Verificar existencia del origen
    if not origen.exists():
        print(f"❌ {usuario_id} ({usuario_nombre}): No se encontró {origen}")
        return stats

    stats['existe_origen'] = True

    # Leer auditoría original (solo lectura)
    try:
        df = pd.read_csv(origen)
        stats['n_registros'] = len(df)

        # Estadísticas de fuentes de imputación
        if 'FC_walk_fuente' in df.columns:
            stats['fuente_counts'] = df['FC_walk_fuente'].value_counts().to_dict()

        # Rango de fechas
        if 'Fecha' in df.columns:
            stats['fecha_min'] = df['Fecha'].min()
            stats['fecha_max'] = df['Fecha'].max()

        # Copiar a zona de trabajo con nuevo nombre
        df.to_csv(destino, index=False)
        stats['copiado'] = True

        print(
            f"✅ {usuario_id} ({usuario_nombre}): {stats['n_registros']} registros copiados")

    except Exception as e:
        print(f"❌ {usuario_id} ({usuario_nombre}): Error al copiar - {e}")

    return stats


def verificar_dataset_trabajo(usuario_id, usuario_nombre):
    """
    Verifica existencia y consistencia de DB_final_v3_uN.csv en zona de trabajo.

    Args:
        usuario_id: 'u1', 'u2', ..., 'u10'
        usuario_nombre: 'ale', 'brenda', ..., 'vane'

    Returns:
        dict con estadísticas del dataset
    """
    archivo = BASE_DIR / f'{DATASET_TRABAJO}_{usuario_id}.csv'

    stats = {
        'usuario_id': usuario_id,
        'usuario_nombre': usuario_nombre,
        'archivo': str(archivo),
        'existe': False,
        'n_registros': 0,
        'n_columnas': 0,
        'columnas': [],
        'fecha_min': None,
        'fecha_max': None,
        'nans_totales': 0,
        'tiene_actividad_relativa': False,
        'tiene_superavit_calorico': False
    }

    if not archivo.exists():
        print(f"⚠️  {usuario_id} ({usuario_nombre}): No existe {archivo.name}")
        return stats

    stats['existe'] = True

    try:
        df = pd.read_csv(archivo)
        stats['n_registros'] = len(df)
        stats['n_columnas'] = len(df.columns)
        stats['columnas'] = df.columns.tolist()
        stats['nans_totales'] = int(df.isna().sum().sum())

        # Verificar variables derivadas clave
        stats['tiene_actividad_relativa'] = 'Actividad_relativa' in df.columns
        stats['tiene_superavit_calorico'] = 'Superavit_calorico_basal' in df.columns

        # Rango de fechas
        if 'Fecha' in df.columns:
            stats['fecha_min'] = df['Fecha'].min()
            stats['fecha_max'] = df['Fecha'].max()

        # Mensaje de estado
        if stats['tiene_actividad_relativa'] and stats['tiene_superavit_calorico']:
            print(
                f"✅ {usuario_id} ({usuario_nombre}): {stats['n_registros']} registros, {stats['n_columnas']} columnas, variables derivadas OK")
        else:
            vars_faltantes = []
            if not stats['tiene_actividad_relativa']:
                vars_faltantes.append('Actividad_relativa')
            if not stats['tiene_superavit_calorico']:
                vars_faltantes.append('Superavit_calorico_basal')
            print(
                f"⚠️  {usuario_id} ({usuario_nombre}): Faltan variables: {', '.join(vars_faltantes)}")

    except Exception as e:
        print(f"❌ {usuario_id} ({usuario_nombre}): Error al leer - {e}")

    return stats


def generar_log(auditorias_stats, datasets_stats):
    """
    Genera log de control de insumos con estadísticas detalladas.

    Args:
        auditorias_stats: Lista de dicts con estadísticas de auditorías
        datasets_stats: Lista de dicts con estadísticas de datasets
    """
    log_file = BASE_DIR / 'control_insumos_log.txt'

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("CONTROL DE INSUMOS - PIPELINE DE SEDENTARISMO\n")
        f.write("="*80 + "\n")
        f.write(
            f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Directorio de trabajo: {BASE_DIR.resolve()}\n")
        f.write("\n")

        # Sección 1: Auditorías FC_walk
        f.write("-"*80 + "\n")
        f.write("1. AUDITORÍAS FC_WALK_IMPUTACION_V3\n")
        f.write("-"*80 + "\n")

        total_copiadas = sum(1 for s in auditorias_stats if s['copiado'])
        total_esperadas = len(USUARIOS)

        f.write(f"Archivos copiados: {total_copiadas}/{total_esperadas}\n\n")

        for stats in auditorias_stats:
            f.write(f"{stats['usuario_id']} ({stats['usuario_nombre']}):\n")
            f.write(f"  Origen: {stats['origen']}\n")
            f.write(f"  Destino: {stats['destino']}\n")
            f.write(f"  Existe origen: {stats['existe_origen']}\n")
            f.write(f"  Copiado: {stats['copiado']}\n")

            if stats['copiado']:
                f.write(f"  Registros: {stats['n_registros']}\n")
                f.write(
                    f"  Fechas: {stats['fecha_min']} → {stats['fecha_max']}\n")
                f.write(f"  Fuentes de imputación:\n")
                for fuente, count in sorted(stats['fuente_counts'].items(), key=lambda x: -x[1]):
                    pct = (count / stats['n_registros']) * 100
                    f.write(f"    {fuente:20s}: {count:5d} ({pct:5.1f}%)\n")
            f.write("\n")

        # Sección 2: Datasets de trabajo
        f.write("-"*80 + "\n")
        f.write("2. DATASETS DE TRABAJO (DB_final_v3_uN.csv)\n")
        f.write("-"*80 + "\n")

        total_existentes = sum(1 for s in datasets_stats if s['existe'])
        total_con_derivadas = sum(1 for s in datasets_stats
                                  if s['tiene_actividad_relativa'] and s['tiene_superavit_calorico'])

        f.write(f"Archivos existentes: {total_existentes}/{total_esperadas}\n")
        f.write(
            f"Con variables derivadas completas: {total_con_derivadas}/{total_esperadas}\n\n")

        for stats in datasets_stats:
            f.write(f"{stats['usuario_id']} ({stats['usuario_nombre']}):\n")
            f.write(f"  Archivo: {stats['archivo']}\n")
            f.write(f"  Existe: {stats['existe']}\n")

            if stats['existe']:
                f.write(f"  Registros: {stats['n_registros']}\n")
                f.write(f"  Columnas: {stats['n_columnas']}\n")
                f.write(
                    f"  Fechas: {stats['fecha_min']} → {stats['fecha_max']}\n")
                f.write(f"  NaNs totales: {stats['nans_totales']}\n")
                f.write(
                    f"  Tiene Actividad_relativa: {stats['tiene_actividad_relativa']}\n")
                f.write(
                    f"  Tiene Superavit_calorico_basal: {stats['tiene_superavit_calorico']}\n")

                # Columnas presentes (sample)
                f.write(f"  Columnas presentes ({len(stats['columnas'])}):\n")
                for col in stats['columnas'][:10]:
                    f.write(f"    - {col}\n")
                if len(stats['columnas']) > 10:
                    f.write(
                        f"    ... (+{len(stats['columnas']) - 10} columnas)\n")
            f.write("\n")

        # Resumen consolidado
        f.write("-"*80 + "\n")
        f.write("3. RESUMEN CONSOLIDADO\n")
        f.write("-"*80 + "\n")

        total_registros = sum(s['n_registros']
                              for s in datasets_stats if s['existe'])

        f.write(f"Total usuarios procesados: {len(USUARIOS)}\n")
        f.write(f"Auditorías copiadas: {total_copiadas}/{total_esperadas}\n")
        f.write(
            f"Datasets verificados: {total_existentes}/{total_esperadas}\n")
        f.write(
            f"Datasets con derivadas completas: {total_con_derivadas}/{total_esperadas}\n")
        f.write(f"Total de registros diarios: {total_registros:,}\n")
        f.write("\n")

        # Estado del pipeline
        f.write("-"*80 + "\n")
        f.write("4. ESTADO DEL PIPELINE\n")
        f.write("-"*80 + "\n")

        if total_copiadas == total_esperadas and total_existentes == total_esperadas:
            f.write(
                "✅ INSUMOS COMPLETOS: Todos los archivos necesarios están disponibles.\n")

            if total_con_derivadas == total_esperadas:
                f.write(
                    "✅ VARIABLES DERIVADAS: Actividad_relativa y Superavit_calorico_basal presentes.\n")
                f.write("\nPróximo paso: Paso 3 - Análisis de Variabilidad Dual\n")
            else:
                f.write(
                    "⚠️  VARIABLES DERIVADAS INCOMPLETAS: Ejecutar scripts de creación.\n")
                f.write(
                    "\nPróximo paso: Completar variables derivadas antes de análisis.\n")
        else:
            f.write("❌ INSUMOS INCOMPLETOS: Faltan archivos necesarios.\n")
            f.write(
                "\nAcción requerida: Revisar archivos faltantes antes de continuar.\n")

        f.write("\n")
        f.write("="*80 + "\n")
        f.write("FIN DEL LOG\n")
        f.write("="*80 + "\n")

    print(f"\n📄 Log generado: {log_file}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("="*80)
    print("CONTROL DE INSUMOS - PIPELINE DE SEDENTARISMO")
    print("="*80)
    print()

    # Paso 1: Crear carpetas
    print("📁 Paso 1: Creando carpetas de trabajo...")
    crear_carpetas()
    print()

    # Paso 2: Copiar auditorías FC_walk
    print("📋 Paso 2: Copiando auditorías FC_walk_imputacion_V3...")
    auditorias_stats = []
    for usuario_id, usuario_nombre in USUARIOS.items():
        stats = copiar_auditoria(usuario_id, usuario_nombre)
        auditorias_stats.append(stats)
    print()

    # Paso 3: Verificar datasets de trabajo
    print("🔍 Paso 3: Verificando datasets de trabajo DB_final_v3_uN...")
    datasets_stats = []
    for usuario_id, usuario_nombre in USUARIOS.items():
        stats = verificar_dataset_trabajo(usuario_id, usuario_nombre)
        datasets_stats.append(stats)
    print()

    # Paso 4: Generar log
    print("📝 Paso 4: Generando log de control...")
    generar_log(auditorias_stats, datasets_stats)
    print()

    # Resumen en consola
    print("="*80)
    print("RESUMEN")
    print("="*80)
    total_copiadas = sum(1 for s in auditorias_stats if s['copiado'])
    total_existentes = sum(1 for s in datasets_stats if s['existe'])
    total_con_derivadas = sum(1 for s in datasets_stats
                              if s['tiene_actividad_relativa'] and s['tiene_superavit_calorico'])

    print(f"Auditorías copiadas: {total_copiadas}/10")
    print(f"Datasets verificados: {total_existentes}/10")
    print(f"Datasets con derivadas completas: {total_con_derivadas}/10")

    if total_copiadas == 10 and total_existentes == 10 and total_con_derivadas == 10:
        print("\n✅ CONTROL DE INSUMOS EXITOSO")
        print("   Listo para Paso 3: Análisis de Variabilidad Dual")
    elif total_con_derivadas < 10:
        print("\n⚠️  VARIABLES DERIVADAS INCOMPLETAS")
        print("   Ejecutar scripts de creación antes de continuar")
    else:
        print("\n❌ INSUMOS INCOMPLETOS")
        print("   Revisar log para detalles")

    print("="*80)


if __name__ == '__main__':
    main()
