"""
Copiar Auditoría FC_walk - Usuario Esmeralda (u5)
==================================================
Script específico para copiar la auditoría de esmeralda que tiene estructura de directorios diferente.

Ruta especial: apple_health_export_esmeralda/apple_health_export/ (nivel adicional)

Autor: Pipeline automatizado
Fecha: 2025-10-16
"""

import pandas as pd
from pathlib import Path

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

BASE_DIR = Path('.').resolve()
ORIGEN_BASE = BASE_DIR.parent / 'apple_health_export'

# Ruta especial para esmeralda (con subdirectorio adicional)
ORIGEN_ESMERALDA = ORIGEN_BASE / 'apple_health_export_esmeralda' / \
    'apple_health_export' / 'FC_walk_imputacion_V3.csv'
DESTINO_ESMERALDA = BASE_DIR / 'analisis_u' / 'FC_walk_imputacion_V3_u5.csv'

# ==============================================================================
# MAIN
# ==============================================================================


def main():
    print("="*80)
    print("COPIAR AUDITORÍA FC_WALK - ESMERALDA (u5)")
    print("="*80)
    print()

    print("Ruta especial detectada:")
    print(f"  Origen: {ORIGEN_ESMERALDA}")
    print(f"  Destino: {DESTINO_ESMERALDA}")
    print()

    # Verificar existencia del origen
    if not ORIGEN_ESMERALDA.exists():
        print(f"❌ ERROR: No se encontró el archivo en la ruta especial")
        print(f"   Ruta buscada: {ORIGEN_ESMERALDA}")
        print()
        print("Por favor verifica que la ruta sea correcta.")
        return

    print(f"✅ Archivo encontrado en ruta especial")

    try:
        # Leer auditoría original (solo lectura)
        df = pd.read_csv(ORIGEN_ESMERALDA)
        n_registros = len(df)

        print(f"📊 Registros a copiar: {n_registros}")

        # Estadísticas de fuentes de imputación
        if 'FC_walk_fuente' in df.columns:
            print(f"\n📋 Fuentes de imputación:")
            fuente_counts = df['FC_walk_fuente'].value_counts()
            for fuente, count in fuente_counts.items():
                pct = (count / n_registros) * 100
                print(f"  {fuente:20s}: {count:5d} ({pct:5.1f}%)")

        # Rango de fechas
        if 'Fecha' in df.columns:
            fecha_min = df['Fecha'].min()
            fecha_max = df['Fecha'].max()
            print(f"\n📅 Fechas: {fecha_min} → {fecha_max}")

        # Copiar a zona de trabajo
        df.to_csv(DESTINO_ESMERALDA, index=False)

        print()
        print("="*80)
        print("✅ AUDITORÍA COPIADA EXITOSAMENTE")
        print("="*80)
        print(f"Archivo creado: {DESTINO_ESMERALDA}")
        print()
        print("Ahora tienes 10/10 auditorías completas.")
        print()

    except Exception as e:
        print(f"\n❌ ERROR al copiar: {e}")
        print()


if __name__ == '__main__':
    main()

