#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación final del archivo Excel consolidado
"""

import pandas as pd
import os


def verificar_final():
    archivo = "DB_usuarios_consolidada.xlsx"

    if not os.path.exists(archivo):
        print(f"❌ El archivo {archivo} no existe.")
        return

    try:
        # Leer el archivo
        excel_file = pd.ExcelFile(archivo, engine='openpyxl')

        print("🎉 ARCHIVO EXCEL CONSOLIDADO CREADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📁 Archivo: {archivo}")
        print(f"📊 Tamaño: {os.path.getsize(archivo) / 1024:.1f} KB")
        print(f"📋 Total de hojas: {len(excel_file.sheet_names)}")
        print(f"📄 Hojas: {', '.join(excel_file.sheet_names)}")
        print()

        # Información de cada hoja
        total_registros = 0
        for hoja in excel_file.sheet_names:
            df = pd.read_excel(archivo, sheet_name=hoja, engine='openpyxl')
            registros = len(df)
            total_registros += registros

            if hoja == 'Resumen':
                print(f"📈 {hoja}: Resumen estadístico")
            else:
                print(f"👤 {hoja}: {registros:,} registros")

        print()
        print("=" * 60)
        print(f"📊 RESUMEN GENERAL:")
        print(f"   👥 Usuarios: {len(excel_file.sheet_names) - 1}")
        print(f"   📈 Total registros: {total_registros:,}")
        print(f"   📅 Período: Datos de actividad física y biométricos")
        print()

        # Mostrar muestra del resumen
        df_resumen = pd.read_excel(
            archivo, sheet_name='Resumen', engine='openpyxl')
        print("📋 ESTADÍSTICAS POR USUARIO:")
        print("=" * 60)
        print(df_resumen.to_string(index=False))

        print()
        print(
            "✅ El archivo está listo para usar en Excel o cualquier aplicación compatible.")

    except Exception as e:
        print(f"❌ Error al verificar el archivo: {e}")


if __name__ == "__main__":
    verificar_final()


