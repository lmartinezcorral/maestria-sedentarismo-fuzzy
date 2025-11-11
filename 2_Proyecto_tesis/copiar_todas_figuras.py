#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para copiar TODAS las figuras importantes del proyecto
"""

import os
import shutil
from pathlib import Path

# Configuración
FIGURAS_DIR = Path("figuras")
BASE_DIR = Path(
    r"C:\Users\hulkmtz\Documents\luis angel\Maestria\Asesoria\Semestre 3\Convocatoria\Datos")

# Crear directorio de figuras
FIGURAS_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("COPIANDO TODAS LAS FIGURAS IMPORTANTES")
print("=" * 80)

# Directorios a copiar
directories_to_copy = [
    ("4 semestre_dataset/analisis_u", ["*.png"]),
    ("4 semestre_dataset/analisis_u/missingness_y_acf", ["*.png"]),
    ("4 semestre_dataset/analisis_u/missingness_y_acf/acf_plots", ["*.png"]),
    ("4 semestre_dataset/analisis_u/missingness_y_acf/pacf_plots", ["*.png"]),
    ("4 semestre_dataset/analisis_u/variabilidad", ["*.png"]),
    ("4 semestre_dataset/analisis_u/clustering", ["*.png"]),
    ("4 semestre_dataset/analisis_u/fuzzy", ["*.png"]),
    ("4 semestre_dataset", ["variabilidad*.png", "heatmap*.png"]),
    ("documentos_tesis/plots", ["*.png"]),
]

copied_count = 0
existing_files = set()

for dir_path, patterns in directories_to_copy:
    source_dir = BASE_DIR / dir_path

    if not source_dir.exists():
        print(f"\n⚠️  Directorio no existe: {dir_path}")
        continue

    print(f"\n📁 Procesando: {dir_path}")

    for pattern in patterns:
        for source_file in source_dir.glob(pattern):
            if source_file.is_file():
                # Crear nombre único para evitar colisiones
                base_name = source_file.stem
                extension = source_file.suffix

                # Si el archivo ya existe con el mismo nombre, añadir sufijo del directorio
                dest_name = source_file.name
                counter = 1
                while dest_name in existing_files:
                    dest_name = f"{base_name}_{counter}{extension}"
                    counter += 1

                dest_file = FIGURAS_DIR / dest_name

                try:
                    shutil.copy2(source_file, dest_file)
                    existing_files.add(dest_name)
                    copied_count += 1
                    print(f"  ✅ {dest_name}")
                except Exception as e:
                    print(f"  ❌ Error copiando {source_file.name}: {e}")

print("\n" + "=" * 80)
print(f"✅ PROCESO COMPLETADO")
print("=" * 80)
print(f"📊 Total de figuras copiadas: {copied_count}")
print(f"📁 Ubicación: {FIGURAS_DIR.absolute()}")

# Listar todas las figuras
print("\n📋 Figuras disponibles:")
all_figures = sorted(list(FIGURAS_DIR.glob("*.png")))
for i, fig in enumerate(all_figures[:30], 1):  # Primeras 30
    print(f"  {i:2d}. {fig.name}")
if len(all_figures) > 30:
    print(f"  ... y {len(all_figures) - 30} más")

print(f"\n✅ Total: {len(all_figures)} figuras listas para usar")
