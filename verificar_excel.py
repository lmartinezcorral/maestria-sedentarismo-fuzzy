#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para verificar el archivo Excel consolidado
"""

import pandas as pd
import os


def verificar_excel():
    archivo = "DB_consolidada_usuarios_final.xlsx"

    if not os.path.exists(archivo):
        print(f"❌ El archivo {archivo} no existe.")
        return

    try:
        # Leer las hojas del archivo
        excel_file = pd.ExcelFile(archivo, engine='openpyxl')

        print(f"📊 ARCHIVO: {archivo}")
        print(f"📋 Hojas: {len(excel_file.sheet_names)}")
        print(f"📄 Nombres: {excel_file.sheet_names}")

        # Mostrar información básica de cada hoja
        for hoja in excel_file.sheet_names:
            df = pd.read_excel(archivo, sheet_name=hoja, engine='openpyxl')
            print(f"  {hoja}: {len(df)} registros")

            if hoja == 'Resumen':
                print("  📈 Contenido del resumen:")
                print(df.to_string(index=False))

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    verificar_excel()
