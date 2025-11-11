#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HERRAMIENTA PORTABLE DE BIBLIOGRAFÍA PARA LATEX - VERSIÓN SIMPLE
Facultad de Medicina y Ciencias Biomédicas - UACH
Versión que funciona sin IA, solo con extracción local inteligente
"""

import os
import sys
import csv
import re
from pathlib import Path
from datetime import datetime

# ==================== FUNCIONES ====================

def instalar_dependencias():
    """Instala las dependencias necesarias automáticamente"""
    print("🔧 Verificando dependencias...")
    
    try:
        import fitz
        print("✅ Dependencias ya instaladas")
        return True
    except ImportError:
        print("📦 Instalando dependencias necesarias...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf", "--quiet"])
            print("✅ Dependencias instaladas correctamente")
            return True
        except Exception as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False

def buscar_pdfs():
    """Busca todos los PDFs en el directorio actual"""
    print("📂 Buscando archivos PDF...")
    
    pdfs = []
    directorio_actual = os.getcwd()
    
    for archivo in Path(directorio_actual).glob("*.pdf"):
        pdfs.append(str(archivo))
    
    print(f"✅ Encontrados {len(pdfs)} archivos PDF")
    return pdfs

def extraer_texto_pdf(ruta_pdf):
    """Extrae texto del PDF usando PyMuPDF"""
    try:
        import fitz
        
        doc = fitz.open(ruta_pdf)
        texto = ""
        
        # Extraer texto de las primeras 2 páginas
        for i in range(min(2, len(doc))):
            pagina = doc[i]
            texto += pagina.get_text() + "\n\n"
        
        doc.close()
        
        return texto[:2000]  # Limitar a 2000 caracteres
        
    except Exception as e:
        print(f"⚠️  Error extrayendo texto: {e}")
        return ""

def extraer_metadatos_inteligente(texto, nombre_archivo):
    """Extrae metadatos usando patrones inteligentes"""
    
    metadatos = {
        'archivo': nombre_archivo,
        'titulo': nombre_archivo.replace('.pdf', ''),
        'autores': 'Autor desconocido',
        'anio': datetime.now().year,
        'revista': 'No disponible',
        'tipo': 'artículo',
        'doi': None,
        'resumen': 'No disponible',
        'palabras_clave': ''
    }
    
    # Buscar título (líneas que empiezan con mayúscula y terminan con punto)
    titulo_match = re.search(r'^([A-Z][^.!?]*[.!?])\s*$', texto, re.MULTILINE)
    if titulo_match:
        titulo = titulo_match.group(1).strip()
        if 10 < len(titulo) < 200:
            metadatos['titulo'] = titulo
    
    # Buscar autores (patrón: Apellido, Nombre y Apellido, Nombre)
    autores_match = re.search(r'^([A-Z][a-z]+,\s+[A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+,\s+[A-Z][a-z]+)*)', texto, re.MULTILINE)
    if autores_match:
        autores = autores_match.group(1).strip()
        if 5 < len(autores) < 200:
            metadatos['autores'] = autores
    
    # Buscar año (cualquier año entre 1900 y actual)
    anio_match = re.search(r'\b(19|20)\d{2}\b', texto)
    if anio_match:
        anio = int(anio_match.group(0))
        if 1900 <= anio <= datetime.now().year:
            metadatos['anio'] = anio
    
    # Buscar revista (líneas que contienen "Journal", "Revista", etc.)
    revista_match = re.search(r'(?:Journal|Revista|Published in)[:\s]+([^\n]+)', texto, re.IGNORECASE)
    if revista_match:
        revista = revista_match.group(1).strip()
        if 3 < len(revista) < 100:
            metadatos['revista'] = revista
    
    # Buscar DOI
    doi_match = re.search(r'10\.\d+/[^\s]+', texto)
    if doi_match:
        metadatos['doi'] = doi_match.group(0)
    
    # Mejorar título basado en el nombre del archivo
    nombre_limpio = nombre_archivo.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
    
    # Si el título es muy genérico, usar el nombre del archivo mejorado
    if metadatos['titulo'] == nombre_archivo.replace('.pdf', ''):
        palabras = nombre_limpio.split()
        if len(palabras) > 3:
            titulo_mejorado = ' '.join([palabra.capitalize() for palabra in palabras])
            metadatos['titulo'] = titulo_mejorado
    
    # Detectar tipo de documento
    texto_lower = texto.lower()
    if 'thesis' in texto_lower or 'tesis' in texto_lower:
        metadatos['tipo'] = 'tesis'
    elif 'book' in texto_lower or 'libro' in texto_lower:
        metadatos['tipo'] = 'libro'
    elif 'conference' in texto_lower or 'conferencia' in texto_lower:
        metadatos['tipo'] = 'conferencia'
    
    return metadatos

def generar_bibtex(datos):
    """Genera entrada BibTeX"""
    # Generar clave de cita
    autores = datos.get('autores', 'autor')
    if autores and autores != 'Autor desconocido':
        primer_apellido = autores.split(',')[0].split()[-1] if ',' in autores else autores.split()[-1]
    else:
        primer_apellido = 'autor'
    
    año = datos.get('anio', datetime.now().year)
    clave = f"{primer_apellido.lower()}{año}"
    
    # Determinar tipo
    tipo_map = {
        'artículo': 'article',
        'libro': 'book',
        'tesis': 'phdthesis',
        'conferencia': 'inproceedings'
    }
    tipo_bibtex = tipo_map.get(datos.get('tipo', 'artículo').lower(), 'article')
    
    # Limpiar campos
    titulo = str(datos.get('titulo', 'Sin título')).replace('{', '').replace('}', '')
    autores_clean = str(autores).replace('{', '').replace('}', '')
    revista = str(datos.get('revista', '')).replace('{', '').replace('}', '')
    doi = datos.get('doi')
    
    # Construir BibTeX
    bibtex = f"@{tipo_bibtex}{{{clave},\n"
    bibtex += f"  title = {{{titulo}}},\n"
    
    if autores and autores != 'Autor desconocido':
        bibtex += f"  author = {{{autores_clean}}},\n"
    
    if datos.get('anio'):
        bibtex += f"  year = {{{datos.get('anio')}}},\n"
    
    if revista and revista != 'No disponible':
        if tipo_bibtex == 'article':
            bibtex += f"  journal = {{{revista}}},\n"
        else:
            bibtex += f"  publisher = {{{revista}}},\n"
    
    if doi:
        bibtex += f"  doi = {{{doi}}},\n"
        bibtex += f"  url = {{https://doi.org/{doi}}},\n"
    
    bibtex += "}\n\n"
    
    return bibtex

def main():
    """Función principal"""
    print("=" * 70)
    print("  HERRAMIENTA DE BIBLIOGRAFÍA PARA LATEX - VERSIÓN SIMPLE")
    print("  Facultad de Medicina y Ciencias Biomédicas - UACH")
    print("=" * 70)
    print()
    
    # 1. Instalar dependencias
    if not instalar_dependencias():
        print("❌ No se pudieron instalar las dependencias")
        input("Presiona Enter para salir...")
        return
    
    # 2. Buscar PDFs
    pdfs = buscar_pdfs()
    
    if not pdfs:
        print("❌ No se encontraron archivos PDF en esta carpeta")
        print("   Coloca tus PDFs aquí y vuelve a ejecutar")
        input("Presiona Enter para salir...")
        return
    
    # 3. Procesar cada PDF
    print(f"\n📚 Procesando {len(pdfs)} archivos...")
    resultados = []
    bibtex_completo = ""
    
    for i, pdf in enumerate(pdfs, 1):
        print(f"\n[{i}/{len(pdfs)}] {Path(pdf).name}")
        
        # Extraer texto
        texto = extraer_texto_pdf(pdf)
        
        # Extraer metadatos
        print("  🔍 Extrayendo metadatos...")
        datos = extraer_metadatos_inteligente(texto, Path(pdf).name)
        
        resultados.append(datos)
        
        # Generar BibTeX
        bibtex = generar_bibtex(datos)
        bibtex_completo += bibtex
        
        print(f"  ✅ {datos.get('titulo', 'Sin título')[:50]}...")
    
    # 4. Guardar archivos
    print(f"\n💾 Guardando archivos...")
    
    # CSV
    archivo_csv = "referencias.csv"
    with open(archivo_csv, 'w', encoding='utf-8', newline='') as f:
        if resultados:
            writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
            writer.writeheader()
            writer.writerows(resultados)
    
    print(f"✅ {archivo_csv}")
    
    # BibTeX
    archivo_bib = "referencias.bib"
    with open(archivo_bib, 'w', encoding='utf-8') as f:
        f.write("% Referencias bibliográficas generadas automáticamente\n")
        f.write(f"% Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"% Total: {len(resultados)} referencias\n\n")
        f.write(bibtex_completo)
    
    print(f"✅ {archivo_bib}")
    
    # 5. Resumen final
    print("\n" + "=" * 70)
    print("  ✅ PROCESO COMPLETADO")
    print("=" * 70)
    print(f"\n📊 Archivos generados:")
    print(f"   • {archivo_csv} - Tabla con todas las referencias")
    print(f"   • {archivo_bib} - Archivo BibTeX para LaTeX")
    print(f"\n📝 Para usar en tu tesis:")
    print(f"   1. Copia {archivo_bib} a tu carpeta de tesis")
    print(f"   2. En tu .tex, usa: \\cite{{autor{datetime.now().year}}}")
    print(f"\n🎉 ¡Listo! {len(resultados)} referencias procesadas")
    
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
