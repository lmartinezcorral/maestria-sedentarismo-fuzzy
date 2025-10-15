#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar el contenido del archivo Excel consolidado
"""

import pandas as pd
import os


def verificar_archivo_consolidado():
    """
    Verifica el contenido del archivo Excel consolidado
    """

    archivo_excel = "DB_consolidada_usuarios.xlsx"

    if not os.path.exists(archivo_excel):
        print(f"❌ El archivo {archivo_excel} no existe.")
        return

    try:
        # Leer el archivo Excel usando openpyxl
        excel_file = pd.ExcelFile(archivo_excel, engine='openpyxl')

        print(f"📊 ARCHIVO EXCEL CONSOLIDADO: {archivo_excel}")
        print("=" * 60)
        print(f"📋 Total de hojas: {len(excel_file.sheet_names)}")
        print(f"📄 Hojas disponibles: {', '.join(excel_file.sheet_names)}")
        print()

        # Mostrar información de cada hoja
        total_registros = 0
        for hoja in excel_file.sheet_names:
            df = pd.read_excel(
                archivo_excel, sheet_name=hoja, engine='openpyxl')
            registros = len(df)
            total_registros += registros

            if hoja == 'Resumen':
                print(f"📈 HOJA: {hoja}")
                print(f"   📊 Resumen estadístico de {registros} usuarios")
                print(f"   📋 Columnas: {', '.join(df.columns.tolist())}")
            else:
                print(f"👤 HOJA: {hoja}")
                print(f"   📊 Registros: {registros:,}")
                print(
                    f"   📅 Período: {df['Fecha'].min()} a {df['Fecha'].max()}")
                print(
                    f"   📋 Columnas: {len(df.columns)} ({', '.join(df.columns.tolist()[:5])}...)")

            print()

        print("=" * 60)
        print(f"🎯 RESUMEN GENERAL:")
        print(f"   📊 Total de registros: {total_registros:,}")
        print(f"   👥 Total de usuarios: {len(excel_file.sheet_names) - 1}")
        print(
            f"   📁 Tamaño del archivo: {os.path.getsize(archivo_excel) / 1024:.1f} KB")

        # Mostrar muestra de la hoja de resumen
        print("\n" + "=" * 60)
        print("📈 MUESTRA DE LA HOJA DE RESUMEN:")
        print("=" * 60)

        df_resumen = pd.read_excel(
            archivo_excel, sheet_name='Resumen', engine='openpyxl')
        print(df_resumen.to_string(index=False))

    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")


if __name__ == "__main__":
    verificar_archivo_consolidado()
