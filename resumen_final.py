#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resumen final de la consolidación de archivos de usuarios
"""

import pandas as pd
import os


def mostrar_resumen_final():
    print("🎉 CONSOLIDACIÓN DE ARCHIVOS DE USUARIOS COMPLETADA")
    print("=" * 70)

    # Verificar archivos creados
    archivos_creados = [
        "DB_usuarios_consolidada.csv",
        "DB_usuarios_resumen.csv",
        "DB_usuarios_consolidada.xlsx"
    ]

    print("📁 ARCHIVOS CREADOS:")
    print("-" * 30)

    for archivo in archivos_creados:
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo) / 1024
            print(f"✅ {archivo} ({tamaño:.1f} KB)")
        else:
            print(f"❌ {archivo} (no encontrado)")

    print()

    # Leer y mostrar información del archivo consolidado
    try:
        df_consolidado = pd.read_csv("DB_usuarios_consolidada.csv")
        df_resumen = pd.read_csv("DB_usuarios_resumen.csv")

        print("📊 ESTADÍSTICAS GENERALES:")
        print("-" * 30)
        print(f"👥 Total de usuarios: {len(df_resumen)}")
        print(f"📈 Total de registros: {len(df_consolidado):,}")
        print(
            f"📅 Período de datos: {df_consolidado['Fecha'].min()} a {df_consolidado['Fecha'].max()}")
        print(f"📋 Columnas de datos: {len(df_consolidado.columns)}")

        print()
        print("📋 COLUMNAS DISPONIBLES:")
        print("-" * 30)
        columnas = df_consolidado.columns.tolist()
        for i, col in enumerate(columnas, 1):
            print(f"{i:2d}. {col}")

        print()
        print("👥 RESUMEN POR USUARIO:")
        print("-" * 30)
        print(df_resumen.to_string(index=False))

        print()
        print("💡 INSTRUCCIONES DE USO:")
        print("-" * 30)
        print("1. 📊 DB_usuarios_consolidada.csv:")
        print("   - Contiene TODOS los datos de los 10 usuarios")
        print("   - Usa filtros en Excel para ver datos por usuario")
        print("   - Columna 'Usuario' identifica cada participante")

        print()
        print("2. 📈 DB_usuarios_resumen.csv:")
        print("   - Estadísticas resumidas por usuario")
        print("   - Promedios de pasos, distancia, frecuencia cardíaca, etc.")
        print("   - Fechas de inicio y fin de cada usuario")

        print()
        print("3. 📁 DB_usuarios_consolidada.xlsx:")
        print("   - Versión Excel del archivo consolidado")
        print("   - Compatible con Microsoft Excel")
        print("   - Puede tener problemas de compatibilidad")

        print()
        print("🔧 RECOMENDACIONES:")
        print("-" * 30)
        print("• Usa los archivos CSV para máxima compatibilidad")
        print("• Abre en Excel, Google Sheets, o cualquier editor de datos")
        print("• Usa filtros para analizar datos por usuario")
        print("• El archivo consolidado permite análisis comparativos")

    except Exception as e:
        print(f"❌ Error al leer archivos: {e}")


if __name__ == "__main__":
    mostrar_resumen_final()
