#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crea la columna Actividad_relativa (fracción 0–1):
Actividad_relativa = min_totales_en_movimiento / (60 * Total_hrs_monitorizadas)

Entrada : DB_usuarios_consolidada.csv
Salida  : DB_usuarios_consolidada_con_actividad_relativa.csv
"""

import os
import numpy as np
import pandas as pd


def crear_actividad_relativa():
    archivo_entrada = "DB_usuarios_consolidada.csv"
    archivo_salida  = "DB_usuarios_consolidada_con_actividad_relativa.csv"

    print("🔧 CREANDO COLUMNA ACTIVIDAD_RELATIVA (fracción 0–1)")
    print("=" * 70)

    # 1) Verificación de archivo
    if not os.path.exists(archivo_entrada):
        print(f"❌ Error: No se encuentra el archivo {archivo_entrada}")
        return False

    try:
        # 2) Carga
        print(f"📂 Leyendo: {archivo_entrada}")
        df = pd.read_csv(archivo_entrada)

        # 3) Resumen básico
        print("📊 Resumen:")
        n_usuarios = df["Usuario"].nunique() if "Usuario" in df.columns else "N/D"
        print(f"   - Registros: {len(df):,}")
        print(f"   - Usuarios : {n_usuarios}")
        print(f"   - Columnas : {len(df.columns)}\n")

        # 4) Validación de columnas requeridas
        requeridas = ["min_totales_en_movimiento", "Total_hrs_monitorizadas"]
        faltantes = [c for c in requeridas if c not in df.columns]
        if faltantes:
            print(f"❌ Faltan columnas: {faltantes}")
            return False

        # 5) Cálculo de Actividad_relativa (fracción 0–1)
        #    Manejo de división por cero: si Total_hrs_monitorizadas <= 0 → NaN
        print("🧮 Calculando Actividad_relativa = min_mov / (60 * hrs_monit) ...")
        denom = 60.0 * df["Total_hrs_monitorizadas"].astype(float)
        df["Actividad_relativa"] = np.where(
            denom > 0,
            df["min_totales_en_movimiento"].astype(float) / denom,
            np.nan
        )

        # 6) Estadísticas globales
        print("\n📈 ESTADÍSTICAS GLOBALES (Actividad_relativa):")
        print("-" * 70)
        ar = df["Actividad_relativa"]
        print(f"   - Válidos: {ar.notna().sum():,}")
        print(f"   - Nulos  : {ar.isna().sum():,}")
        if ar.notna().any():
            print(f"   - Media  : {ar.mean():.4f}")
            print(f"   - Mediana: {ar.median():.4f}")
            print(f"   - Std    : {ar.std():.4f}")
            print(f"   - Mín    : {ar.min():.4f}")
            print(f"   - Máx    : {ar.max():.4f}")

        # 7) Estadísticas por usuario (si existe la columna)
        if "Usuario" in df.columns:
            print("\n👥 ESTADÍSTICAS POR USUARIO (Actividad_relativa):")
            print("-" * 70)
            stats_u = df.groupby("Usuario")["Actividad_relativa"].agg(
                count="count", mean="mean", median="median",
                std="std", min="min", max="max"
            ).round(4)
            for usuario, row in stats_u.iterrows():
                print(f"   {usuario}:")
                print(f"     - Registros: {int(row['count'])}")
                print(f"     - Promedio : {row['mean']:.4f}")
                print(f"     - Mediana  : {row['median']:.4f}")
                print(f"     - Desv.Est.: {row['std']:.4f}")
                print(f"     - Rango    : {row['min']:.4f} – {row['max']:.4f}")
                print()

        # 8) Chequeos de plausibilidad / calidad
        print("🔍 CHEQUEOS DE PLAUSIBILIDAD:")
        print("-" * 70)

        # a) más minutos de movimiento que minutos monitorizados
        minutos_monitorizados = 60.0 * df["Total_hrs_monitorizadas"].astype(float)
        mask_mov_excede = df["min_totales_en_movimiento"].astype(float) > minutos_monitorizados
        n_excede = int(mask_mov_excede.sum())
        if n_excede > 0:
            print(f"   ⚠️ Registros donde min_mov > 60*hrs_monit: {n_excede}")
            ej = df.loc[mask_mov_excede, ["Usuario", "Fecha",
                                          "Total_hrs_monitorizadas",
                                          "min_totales_en_movimiento",
                                          "Actividad_relativa"]].head(5)
            print("   Ejemplos:")
            for _, r in ej.iterrows():
                u = r["Usuario"] if "Usuario" in r else "N/D"
                f = r["Fecha"] if "Fecha" in r else "N/D"
                print(f"     - {u} ({f}): hrs={r['Total_hrs_monitorizadas']}, "
                      f"min_mov={r['min_totales_en_movimiento']}, "
                      f"AR={r['Actividad_relativa']:.4f}")
        else:
            print("   ✅ Ningún caso con min_mov > 60*hrs_monit")

        # b) horas monitorizadas > 24 (improbable)
        mask_hrs_24 = df["Total_hrs_monitorizadas"].astype(float) > 24
        n_hrs_24 = int(mask_hrs_24.sum())
        if n_hrs_24 > 0:
            print(f"   ⚠️ Registros con Total_hrs_monitorizadas > 24: {n_hrs_24}")
        else:
            print("   ✅ Ningún caso con hrs_monit > 24")

        # c) Actividad_relativa fuera de [0,1]
        mask_fuera = (ar < 0) | (ar > 1)
        n_fuera = int(mask_fuera.sum())
        if n_fuera > 0:
            print(f"   ⚠️ Registros con Actividad_relativa fuera de [0,1]: {n_fuera}")
            print("      (revisar escalas / consistencia de origen)")
        else:
            print("   ✅ Actividad_relativa en [0,1] para todos los válidos")

        # 9) Reordenar columna: colocar después de min_totales_en_movimiento
        cols = list(df.columns)
        # quitar si ya está
        if "Actividad_relativa" in cols:
            cols.remove("Actividad_relativa")
        # insertar después de min_totales_en_movimiento (si existe)
        if "min_totales_en_movimiento" in cols:
            pos = cols.index("min_totales_en_movimiento")
            cols.insert(pos + 1, "Actividad_relativa")
        else:
            cols.append("Actividad_relativa")
        df = df[cols]

        # 10) Guardar
        print(f"\n💾 Guardando: {archivo_salida}")
        df.to_csv(archivo_salida, index=False)

        # 11) Verificación rápida de tamaños
        kb_in  = os.path.getsize(archivo_entrada) / 1024
        kb_out = os.path.getsize(archivo_salida) / 1024
        print("✅ Archivo guardado con éxito")
        print(f"   - Tamaño original : {kb_in:.1f} KB")
        print(f"   - Tamaño actualizado: {kb_out:.1f} KB")
        print("   - Nueva columna: 'Actividad_relativa' (fracción 0–1)")
        print("   - Posición: después de 'min_totales_en_movimiento'")

        # 12) Muestra
        print("\n📋 MUESTRA (10 filas):")
        print("-" * 70)
        cols_demo = ["Fecha", "Usuario", "Total_hrs_monitorizadas",
                     "min_totales_en_movimiento", "Actividad_relativa"]
        cols_demo = [c for c in cols_demo if c in df.columns]
        print(df[cols_demo].head(10).to_string(index=False))

        return True

    except Exception as e:
        print(f"❌ Error al procesar: {e}")
        return False


if __name__ == "__main__":
    crear_actividad_relativa()


