#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para:
1. Extraer rutas de figuras del LaTeX
2. Copiar figuras a documentos_tesis/figuras/
3. Actualizar LaTeX para embeber imágenes
"""

import os
import re
import shutil
from pathlib import Path

# Configuración
LATEX_FILE = "INFORME_TECNICO_PIPELINE_COMPLETO.tex"
FIGURAS_DIR = "figuras"
BASE_DIR = Path(
    r"C:\Users\hulkmtz\Documents\luis angel\Maestria\Asesoria\Semestre 3\Convocatoria\Datos")

# Crear directorio de figuras si no existe
os.makedirs(FIGURAS_DIR, exist_ok=True)

print("=" * 80)
print("PASO 1: Leyendo archivo LaTeX...")
print("=" * 80)

# Leer el archivo LaTeX
with open(LATEX_FILE, 'r', encoding='utf-8') as f:
    latex_content = f.read()

# Extraer todas las rutas de figuras
# Patrón para encontrar: \texttt{ruta/archivo.png} o \texttt{ruta/archivo.png}
pattern = r'\\texttt\{([^}]+\.png)\}'
figure_paths = re.findall(pattern, latex_content)

print(f"\n✅ Encontradas {len(figure_paths)} referencias a figuras")
for i, path in enumerate(figure_paths, 1):
    print(f"  {i}. {path}")

print("\n" + "=" * 80)
print("PASO 2: Copiando figuras...")
print("=" * 80)

copied_files = []
missing_files = []

for fig_path in figure_paths:
    # Normalizar la ruta (reemplazar _ por espacio en algunos casos)
    original_path = BASE_DIR / fig_path.replace('\_', '_')

    # Intentar variaciones de la ruta
    possible_paths = [
        original_path,
        BASE_DIR / fig_path.replace('\\_', '_'),
        BASE_DIR / fig_path.replace('_', ' '),
    ]

    found = False
    for test_path in possible_paths:
        if test_path.exists():
            # Generar nombre de archivo limpio
            filename = test_path.name.replace(' ', '_')
            dest_path = Path(FIGURAS_DIR) / filename

            # Copiar archivo
            shutil.copy2(test_path, dest_path)
            copied_files.append((fig_path, filename))
            print(f"  ✅ Copiado: {filename}")
            found = True
            break

    if not found:
        missing_files.append(fig_path)
        print(f"  ❌ No encontrado: {fig_path}")

print(f"\n📊 Resumen:")
print(f"  ✅ Copiados: {len(copied_files)}")
print(f"  ❌ No encontrados: {len(missing_files)}")

# Copiar también figuras conocidas importantes
print("\n" + "=" * 80)
print("PASO 3: Copiando figuras adicionales conocidas...")
print("=" * 80)

additional_figures = [
    "4 semestre_dataset/analisis_u/comparativo_variabilidad.png",
    "4 semestre_dataset/variabilidad_operativa_vs_observada.png",
    "4 semestre_dataset/variabilidad_por_usuario_boxplot.png",
    "4 semestre_dataset/heatmap_cv_usuario_variable.png",
]

for fig_path in additional_figures:
    source = BASE_DIR / fig_path
    if source.exists():
        filename = source.name
        dest = Path(FIGURAS_DIR) / filename
        shutil.copy2(source, dest)
        print(f"  ✅ Copiado: {filename}")
    else:
        print(f"  ℹ️  No existe: {fig_path}")

print("\n" + "=" * 80)
print("PASO 4: Actualizando LaTeX para embeber imágenes...")
print("=" * 80)

# Crear versión modificada del LaTeX
latex_modified = latex_content

# Reemplazar cada referencia por una figura embebida
for original_path, filename in copied_files:
    # Buscar el patrón completo
    old_pattern = rf'\\textit\{{Ver Figura[s]?\}}: \\texttt\{{{re.escape(original_path)}\}}'

    # Generar nombre limpio para la etiqueta
    label = filename.replace('.png', '').replace('_', '').replace('-', '')[:30]

    # Crear el código LaTeX para la figura
    new_figure = f"""\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.85\\textwidth]{{figuras/{filename}}}
\\caption{{\\textit{{Figura}}: \\texttt{{{original_path}}}}}
\\label{{fig:{label}}}
\\end{{figure}}"""

    # Reemplazar
    latex_modified = re.sub(old_pattern, new_figure, latex_modified)

# Guardar el archivo modificado
output_file = "INFORME_TECNICO_PIPELINE_COMPLETO_CON_FIGURAS.tex"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(latex_modified)

print(f"\n✅ Archivo LaTeX modificado guardado como: {output_file}")

print("\n" + "=" * 80)
print("PASO 5: Listado de figuras en directorio figuras/")
print("=" * 80)

figuras_finales = list(Path(FIGURAS_DIR).glob("*.png"))
print(f"\n📁 Total de figuras en {FIGURAS_DIR}/: {len(figuras_finales)}")
for fig in sorted(figuras_finales)[:20]:  # Mostrar primeras 20
    print(f"  - {fig.name}")
if len(figuras_finales) > 20:
    print(f"  ... y {len(figuras_finales) - 20} más")

print("\n" + "=" * 80)
print("✅ PROCESO COMPLETADO")
print("=" * 80)
print(f"""
Próximos pasos:
1. Revisar el archivo: {output_file}
2. Compilar con: pdflatex {output_file}
3. Las figuras están en: {FIGURAS_DIR}/
""")
