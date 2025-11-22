#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige las dobles barras invertidas en \textit{}"""

from pathlib import Path
import re

def corregir_archivo(archivo_path):
    """Corrige dobles barras en \textit{}"""
    with open(archivo_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Reemplazar \\textit{ por \textit{
    contenido_corregido = contenido.replace('\\\\textit{', '\\textit{')
    
    if contenido != contenido_corregido:
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)
        cambios = len(re.findall(r'\\\\textit\{', contenido))
        return cambios
    return 0

def main():
    base_dir = Path(__file__).parent.parent
    capitulos_dir = base_dir / 'capitulos'
    main_file = base_dir / 'main.tex'
    
    archivos_tex = []
    if capitulos_dir.exists():
        archivos_tex.extend(capitulos_dir.glob('*.tex'))
    if main_file.exists():
        archivos_tex.append(main_file)
    
    total = 0
    for archivo in archivos_tex:
        cambios = corregir_archivo(archivo)
        total += cambios
        if cambios > 0:
            print(f"✅ {archivo.name}: {cambios} correcciones")
    
    print(f"\n✅ Total: {total} correcciones")

if __name__ == '__main__':
    main()

