#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear un archivo Excel consolidado con los datos de usuarios
"""

import pandas as pd
import os
from pathlib import Path


def crear_excel_consolidado():
    """
    Crea un archivo Excel consolidado con una hoja para cada usuario
    """

    # Lista de archivos CSV de usuarios
    archivos_usuarios = [
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

    # Crear un diccionario para almacenar los DataFrames
    dataframes_usuarios = {}

    print("📂 Leyendo archivos CSV...")

    # Leer cada archivo CSV
    for archivo in archivos_usuarios:
        if os.path.exists(archivo):
            try:
                # Leer el CSV
                df = pd.read_csv(archivo)

                # Extraer el número de usuario del nombre del archivo
                numero_usuario = archivo.split('_u')[1].split('.')[0]

                # Agregar una columna con el número de usuario
                df['Usuario'] = f"Usuario_{numero_usuario}"

                # Almacenar en el diccionario
                dataframes_usuarios[f"Usuario_{numero_usuario}"] = df

                print(f"✅ Leído: {archivo} - {len(df):,} registros")

            except Exception as e:
                print(f"❌ Error al leer {archivo}: {e}")
        else:
            print(f"❌ Archivo no encontrado: {archivo}")

    if not dataframes_usuarios:
        print("❌ No se encontraron archivos para procesar.")
        return

    # Crear el archivo Excel
    nombre_archivo_excel = "DB_consolidada_usuarios_final.xlsx"

    print(f"\n📊 Creando archivo Excel: {nombre_archivo_excel}")

    try:
        # Crear el archivo Excel con múltiples hojas
        with pd.ExcelWriter(nombre_archivo_excel, engine='openpyxl') as writer:

            # Escribir cada DataFrame en una hoja separada
            for nombre_hoja, df in dataframes_usuarios.items():
                df.to_excel(writer, sheet_name=nombre_hoja, index=False)
                print(f"✅ Hoja creada: {nombre_hoja} - {len(df):,} registros")

            # Crear una hoja de resumen con estadísticas
            resumen_data = []
            for nombre_hoja, df in dataframes_usuarios.items():
                resumen_data.append({
                    'Usuario': nombre_hoja,
                    'Total_Registros': len(df),
                    'Fecha_Inicio': df['Fecha'].min(),
                    'Fecha_Fin': df['Fecha'].max(),
                    'Promedio_Pasos': df['Numero_pasos_por_dia'].mean().round(2),
                    'Promedio_Distancia_km': df['distancia_caminada_en_km'].mean().round(2),
                    'Promedio_FC_Reposo': df['FCr_promedio_diario'].mean().round(2),
                    'Promedio_HRV_SDNN': df['HRV_SDNN'].mean().round(2)
                })

            df_resumen = pd.DataFrame(resumen_data)
            df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
            print(
                f"✅ Hoja de resumen creada con estadísticas de {len(dataframes_usuarios)} usuarios")

        print(f"\n🎉 Archivo Excel creado exitosamente: {nombre_archivo_excel}")
        print(
            f"📊 Total de hojas: {len(dataframes_usuarios) + 1} (usuarios + resumen)")

        # Mostrar estadísticas finales
        total_registros = sum(len(df) for df in dataframes_usuarios.values())
        print(f"📈 Total de registros procesados: {total_registros:,}")

        # Mostrar información del archivo
        tamaño_archivo = os.path.getsize(nombre_archivo_excel) / 1024
        print(f"💾 Tamaño del archivo: {tamaño_archivo:.1f} KB")

        # Mostrar muestra del resumen
        print(f"\n📋 MUESTRA DEL RESUMEN:")
        print("=" * 80)
        print(df_resumen.to_string(index=False))

    except Exception as e:
        print(f"❌ Error al crear el archivo Excel: {e}")


if __name__ == "__main__":
    crear_excel_consolidado()




