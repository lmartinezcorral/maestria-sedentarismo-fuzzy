#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crear archivo CSV consolidado con todos los usuarios
"""

import pandas as pd
import os


def crear_csv_consolidado():
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

    # Leer y consolidar todos los archivos
    dataframes = []
    resumen_data = []

    for archivo in archivos:
        if os.path.exists(archivo):
            df = pd.read_csv(archivo)
            numero_usuario = archivo.split('_u')[1].split('.')[0]
            df['Usuario'] = f"Usuario_{numero_usuario}"
            dataframes.append(df)

            # Agregar al resumen
            resumen_data.append({
                'Usuario': f"Usuario_{numero_usuario}",
                'Total_Registros': len(df),
                'Fecha_Inicio': df['Fecha'].min(),
                'Fecha_Fin': df['Fecha'].max(),
                'Promedio_Pasos': round(df['Numero_pasos_por_dia'].mean(), 0),
                'Promedio_Distancia_km': round(df['distancia_caminada_en_km'].mean(), 2),
                'Promedio_FC_Reposo': round(df['FCr_promedio_diario'].mean(), 2),
                'Promedio_HRV_SDNN': round(df['HRV_SDNN'].mean(), 2)
            })

            print(f"✅ {archivo}: {len(df)} registros")

    if not dataframes:
        print("❌ No se encontraron archivos para procesar.")
        return

    # Consolidar todos los datos
    df_consolidado = pd.concat(dataframes, ignore_index=True)
    df_resumen = pd.DataFrame(resumen_data)

    # Guardar archivo consolidado
    archivo_consolidado = "DB_usuarios_consolidada.csv"
    archivo_resumen = "DB_usuarios_resumen.csv"

    print(f"\n📊 Creando archivos consolidados...")

    try:
        # Guardar archivo principal
        df_consolidado.to_csv(archivo_consolidado, index=False)
        print(f"✅ Archivo principal: {archivo_consolidado}")
        print(f"   📈 Total registros: {len(df_consolidado):,}")

        # Guardar resumen
        df_resumen.to_csv(archivo_resumen, index=False)
        print(f"✅ Archivo resumen: {archivo_resumen}")
        print(f"   📊 Usuarios: {len(df_resumen)}")

        print(f"\n🎉 ARCHIVOS CREADOS EXITOSAMENTE")
        print("=" * 60)
        print(f"📁 Archivo principal: {archivo_consolidado}")
        print(f"📁 Archivo resumen: {archivo_resumen}")
        print(f"📊 Total registros: {len(df_consolidado):,}")
        print(f"👥 Total usuarios: {len(df_resumen)}")
        print()

        print("📋 RESUMEN POR USUARIO:")
        print("=" * 60)
        print(df_resumen.to_string(index=False))

        print(f"\n💡 INSTRUCCIONES:")
        print(f"   1. Abre {archivo_consolidado} en Excel")
        print(f"   2. Usa filtros para ver datos por usuario")
        print(f"   3. Consulta {archivo_resumen} para estadísticas")
        print(f"   4. Los archivos CSV son compatibles con Excel, Google Sheets, etc.")

    except Exception as e:
        print(f"❌ Error al crear archivos: {e}")


if __name__ == "__main__":
    crear_csv_consolidado()




