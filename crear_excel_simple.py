#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para crear archivo Excel consolidado
"""

import pandas as pd
import os


def crear_excel_simple():
    # Lista de archivos
    archivos = [
        "DB_final_v3_u1.csv",
        "DB_final_v3_u2.csv",
        "DB_final_v3_u3.csv",
        "DB_final_v3_u4.csv",
        "DB_final_v3_u5.csv",
        "DB_final_v3_u6.csv",
        "DB_final_v3_u7.csv",
        "DB_final_v3_u8.csv",
        "DB_final_v3_u9.csv",
        "DB_final_v3_u10.csv"
    ]

    print("📂 Leyendo archivos CSV...")

    # Leer todos los archivos
    dataframes = {}
    for archivo in archivos:
        if os.path.exists(archivo):
            df = pd.read_csv(archivo)
            numero_usuario = archivo.split('_u')[1].split('.')[0]
            df['Usuario'] = f"Usuario_{numero_usuario}"
            dataframes[f"Usuario_{numero_usuario}"] = df
            print(f"✅ {archivo}: {len(df)} registros")

    # Crear archivo Excel
    archivo_excel = "DB_usuarios_consolidada.xlsx"

    print(f"\n📊 Creando {archivo_excel}...")

    try:
        with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
            # Escribir cada hoja
            for nombre, df in dataframes.items():
                df.to_excel(writer, sheet_name=nombre, index=False)
                print(f"✅ Hoja: {nombre}")

            # Crear resumen
            resumen = []
            for nombre, df in dataframes.items():
                resumen.append({
                    'Usuario': nombre,
                    'Registros': len(df),
                    'Fecha_Inicio': df['Fecha'].min(),
                    'Fecha_Fin': df['Fecha'].max(),
                    'Promedio_Pasos': round(df['Numero_pasos_por_dia'].mean(), 0),
                    'Promedio_Distancia': round(df['distancia_caminada_en_km'].mean(), 2)
                })

            df_resumen = pd.DataFrame(resumen)
            df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
            print(f"✅ Hoja: Resumen")

        print(f"\n🎉 Archivo creado: {archivo_excel}")
        print(
            f"📊 Total registros: {sum(len(df) for df in dataframes.values()):,}")

        # Mostrar resumen
        print(f"\n📋 RESUMEN:")
        print(df_resumen.to_string(index=False))

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    crear_excel_simple()
