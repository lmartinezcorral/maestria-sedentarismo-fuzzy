#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor de PDF de Tesis para Revisión de Ades
"""

import pdfplumber
from pathlib import Path

pdf_path = Path("plantilla_tesis.pdf")
output_path = Path("notas_proceso/TESIS_COMPLETA_TEXTO_6NOV.txt")

print(f"Extrayendo: {pdf_path}")

with pdfplumber.open(pdf_path) as pdf:
    total_paginas = len(pdf.pages)
    print(f"Total páginas: {total_paginas}")
    
    texto_completo = []
    
    for i, pagina in enumerate(pdf.pages, 1):
        try:
            texto = pagina.extract_text()
            if texto:
                texto_completo.append(f"\n{'='*80}\n")
                texto_completo.append(f"PÁGINA {i}\n")
                texto_completo.append(f"{'='*80}\n\n")
                texto_completo.append(texto)
            print(f"✓ Página {i}/{total_paginas}", end='\r')
        except Exception as e:
            print(f"✗ Error página {i}: {e}")
            continue
    
    # Guardar
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("TESIS COMPLETA - TEXTO EXTRAÍDO PARA REVISIÓN ADES\n")
        f.write("="*80 + "\n\n")
        f.write(f"Documento: {pdf_path}\n")
        f.write(f"Total páginas: {total_paginas}\n")
        f.write(f"Extraído: 6 de Noviembre 2025, 09:40 hrs\n\n")
        f.write("="*80 + "\n\n")
        f.write("\n".join(texto_completo))
        f.write("\n\n" + "="*80 + "\n")
        f.write(f"FIN DEL DOCUMENTO - {len(' '.join(texto_completo).split())} palabras\n")
        f.write("="*80 + "\n")
    
    print(f"\n✓ Guardado: {output_path}")
    print(f"  Palabras: {len(' '.join(texto_completo).split()):,}")

