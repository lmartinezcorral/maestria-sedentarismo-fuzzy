#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRACTOR DE PDFs Y DOCUMENTOS PARA ADES - JUEZ DEL INFRAMUNDO
================================================================

Propósito: Extraer texto de PDFs protegidos/encriptados y archivos .doc
         para análisis crítico de tesis según estándares Q1

Autor: Ades - Juez del Inframundo
Fecha: 6 de Noviembre de 2025
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Directorios
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "guias_texto_extraidas"

# Documentos a procesar (en orden de prioridad)
DOCUMENTOS = {
    "criticos": [
        {
            "archivo": "Lista de cotejo general  Tesis.doc",
            "salida": "01_CRITICO_lista_cotejo_tesis.txt",
            "tipo": "doc",
            "prioridad": 1
        },
        {
            "archivo": "Chispas_Tips_para_escribir_mejor.pdf",
            "salida": "02_CRITICO_chispas_redaccion.txt",
            "tipo": "pdf",
            "prioridad": 1
        },
        {
            "archivo": "Rúbrica Analítica.pdf",
            "salida": "03_CRITICO_rubrica_analitica_uach.txt",
            "tipo": "pdf",
            "prioridad": 1
        }
    ],
    "altos": [
        {
            "archivo": "Guia-Normas-APA-7ma-edicion.pdf",
            "salida": "04_ALTO_guia_apa7.txt",
            "tipo": "pdf",
            "prioridad": 2,
            "paginas_clave": [1, 50]  # Primeras 50 páginas (formato, citas)
        },
        {
            "archivo": "Metodología de la Investigación -sampieri- 6ta EDICION (1).pdf",
            "salida": "05_ALTO_metodologia_sampieri6.txt",
            "tipo": "pdf",
            "prioridad": 2,
            "paginas_clave": [1, 100]  # Caps 1-3: Enfoque, diseño, muestreo
        },
        {
            "archivo": "Guía-práctica-de-investigación-en-salud.OPS-2008.pdf",
            "salida": "06_ALTO_guia_ops_salud.txt",
            "tipo": "pdf",
            "prioridad": 2
        }
    ],
    "medios": [
        {
            "archivo": "Reglamento general de investigación y posgrado.pdf",
            "salida": "07_MEDIO_reglamento_uach.txt",
            "tipo": "pdf",
            "prioridad": 3
        },
        {
            "archivo": "Marco conceptual en el proceso de investigación.pdf",
            "salida": "08_BAJO_marco_conceptual.txt",
            "tipo": "pdf",
            "prioridad": 3
        },
        {
            "archivo": "Guía para el análisis crítico de publicaciones científicas .pdf",
            "salida": "09_BAJO_analisis_critico_pub.txt",
            "tipo": "pdf",
            "prioridad": 3
        }
    ]
}

# ============================================================================
# FUNCIONES DE EXTRACCIÓN
# ============================================================================

def log(mensaje, nivel="INFO"):
    """Logger simple con timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    simbolo = {"INFO": "ℹ️", "OK": "✅", "ERROR": "❌", "WARN": "⚠️"}
    print(f"[{timestamp}] {simbolo.get(nivel, 'ℹ️')} {mensaje}")


def instalar_dependencias():
    """Instala dependencias necesarias si no están disponibles"""
    log("Verificando dependencias...")
    
    dependencias = {
        "pdfplumber": "pdfplumber",
        "PyPDF2": "PyPDF2",
        "python-docx": "python-docx"
    }
    
    instaladas = []
    faltantes = []
    
    for nombre, paquete in dependencias.items():
        try:
            __import__(nombre.replace("-", "_"))
            instaladas.append(nombre)
        except ImportError:
            faltantes.append(paquete)
    
    if instaladas:
        log(f"Dependencias disponibles: {', '.join(instaladas)}", "OK")
    
    if faltantes:
        log(f"Faltan dependencias: {', '.join(faltantes)}", "WARN")
        log("Instalando dependencias faltantes...")
        for paquete in faltantes:
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", paquete, "--quiet"])
                log(f"✓ Instalado: {paquete}", "OK")
            except Exception as e:
                log(f"✗ Error instalando {paquete}: {e}", "ERROR")
                return False
    
    return True


def extraer_pdf_pdfplumber(ruta_pdf, paginas_clave=None):
    """Extrae texto de PDF usando pdfplumber (mejor con PDFs protegidos)"""
    try:
        import pdfplumber
        
        texto_completo = []
        
        with pdfplumber.open(ruta_pdf) as pdf:
            total_paginas = len(pdf.pages)
            
            if paginas_clave:
                inicio, fin = paginas_clave
                paginas_a_leer = range(min(inicio - 1, total_paginas), min(fin, total_paginas))
                log(f"  → Leyendo páginas {inicio}-{min(fin, total_paginas)} de {total_paginas}")
            else:
                paginas_a_leer = range(total_paginas)
                log(f"  → Leyendo todas las páginas ({total_paginas})")
            
            for i in paginas_a_leer:
                try:
                    pagina = pdf.pages[i]
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo.append(f"\n{'='*80}\n")
                        texto_completo.append(f"PÁGINA {i+1}\n")
                        texto_completo.append(f"{'='*80}\n\n")
                        texto_completo.append(texto)
                except Exception as e:
                    log(f"  ⚠️  Error página {i+1}: {str(e)[:50]}", "WARN")
                    continue
        
        return "\n".join(texto_completo) if texto_completo else None
        
    except Exception as e:
        log(f"  ✗ Error pdfplumber: {str(e)[:80]}", "WARN")
        return None


def extraer_pdf_pypdf2(ruta_pdf, paginas_clave=None):
    """Extrae texto de PDF usando PyPDF2 (fallback)"""
    try:
        import PyPDF2
        
        texto_completo = []
        
        with open(ruta_pdf, 'rb') as archivo:
            lector = PyPDF2.PdfReader(archivo)
            total_paginas = len(lector.pages)
            
            if paginas_clave:
                inicio, fin = paginas_clave
                paginas_a_leer = range(min(inicio - 1, total_paginas), min(fin, total_paginas))
            else:
                paginas_a_leer = range(total_paginas)
            
            for i in paginas_a_leer:
                try:
                    pagina = lector.pages[i]
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo.append(f"\n{'='*80}\n")
                        texto_completo.append(f"PÁGINA {i+1}\n")
                        texto_completo.append(f"{'='*80}\n\n")
                        texto_completo.append(texto)
                except Exception as e:
                    continue
        
        return "\n".join(texto_completo) if texto_completo else None
        
    except Exception as e:
        log(f"  ✗ Error PyPDF2: {str(e)[:80]}", "WARN")
        return None


def extraer_doc(ruta_doc):
    """Extrae texto de archivo .doc/.docx"""
    try:
        from docx import Document
        
        doc = Document(ruta_doc)
        texto_completo = []
        
        for i, parrafo in enumerate(doc.paragraphs, 1):
            if parrafo.text.strip():
                texto_completo.append(parrafo.text)
        
        log(f"  → Extraídos {len(texto_completo)} párrafos")
        return "\n\n".join(texto_completo) if texto_completo else None
        
    except Exception as e:
        log(f"  ✗ Error extrayendo .doc: {e}", "ERROR")
        return None


def procesar_documento(info_doc):
    """Procesa un documento y guarda el texto extraído"""
    ruta_entrada = BASE_DIR / info_doc["archivo"]
    ruta_salida = OUTPUT_DIR / info_doc["salida"]
    
    if not ruta_entrada.exists():
        log(f"✗ No encontrado: {info_doc['archivo']}", "ERROR")
        return False
    
    log(f"Procesando: {info_doc['archivo']}")
    
    # Extraer según tipo
    texto = None
    
    if info_doc["tipo"] == "pdf":
        paginas = info_doc.get("paginas_clave", None)
        
        # Intentar pdfplumber primero
        texto = extraer_pdf_pdfplumber(ruta_entrada, paginas)
        
        # Fallback a PyPDF2
        if not texto:
            log("  → Intentando método alternativo (PyPDF2)...", "WARN")
            texto = extraer_pdf_pypdf2(ruta_entrada, paginas)
    
    elif info_doc["tipo"] == "doc":
        texto = extraer_doc(ruta_entrada)
    
    # Guardar resultado
    if texto:
        try:
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                # Header
                f.write("=" * 80 + "\n")
                f.write(f"DOCUMENTO: {info_doc['archivo']}\n")
                f.write(f"EXTRAÍDO: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"PRIORIDAD: {'🔥 CRÍTICA' if info_doc['prioridad'] == 1 else '⚠️ ALTA' if info_doc['prioridad'] == 2 else '🔍 MEDIA'}\n")
                f.write("=" * 80 + "\n\n")
                
                # Contenido
                f.write(texto)
                
                # Footer
                f.write("\n\n" + "=" * 80 + "\n")
                f.write(f"FIN DEL DOCUMENTO - {len(texto.split())} palabras extraídas\n")
                f.write("=" * 80 + "\n")
            
            # Estadísticas
            palabras = len(texto.split())
            lineas = len(texto.split('\n'))
            tamano_kb = len(texto.encode('utf-8')) / 1024
            
            log(f"✓ Guardado: {info_doc['salida']}", "OK")
            log(f"  📊 {palabras:,} palabras | {lineas:,} líneas | {tamano_kb:.1f} KB")
            return True
            
        except Exception as e:
            log(f"✗ Error guardando: {e}", "ERROR")
            return False
    else:
        log(f"✗ No se pudo extraer texto de: {info_doc['archivo']}", "ERROR")
        return False


def generar_resumen():
    """Genera archivo resumen con estadísticas de extracción"""
    ruta_resumen = OUTPUT_DIR / "00_RESUMEN_EXTRACCION.txt"
    
    archivos_extraidos = sorted([f for f in OUTPUT_DIR.glob("*.txt") if f.name != "00_RESUMEN_EXTRACCION.txt"])
    
    with open(ruta_resumen, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RESUMEN DE EXTRACCIÓN DE GUÍAS - ADES JUEZ DEL INFRAMUNDO\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%d de %B de %Y, %H:%M:%S')}\n")
        f.write(f"Total archivos extraídos: {len(archivos_extraidos)}\n\n")
        
        f.write("ARCHIVOS GENERADOS:\n")
        f.write("-" * 80 + "\n\n")
        
        for archivo in archivos_extraidos:
            with open(archivo, 'r', encoding='utf-8') as contenido:
                texto = contenido.read()
                palabras = len(texto.split())
                lineas = len(texto.split('\n'))
                tamano_kb = archivo.stat().st_size / 1024
            
            f.write(f"📄 {archivo.name}\n")
            f.write(f"   Palabras: {palabras:,} | Líneas: {lineas:,} | Tamaño: {tamano_kb:.1f} KB\n\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("PRÓXIMOS PASOS:\n")
        f.write("=" * 80 + "\n\n")
        f.write("1. Revisar archivos CRÍTICOS (01, 02, 03) para validar extracción\n")
        f.write("2. Ades leerá archivos en orden de prioridad\n")
        f.write("3. Rúbrica será actualizada con criterios reales UACH\n")
        f.write("4. Revisión profunda iniciará con base sólida\n\n")
        f.write("💀 Ades - Juez del Inframundo | Listo para juzgar con evidencia\n")
    
    log(f"✓ Resumen generado: {ruta_resumen.name}", "OK")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("💀 EXTRACTOR DE GUÍAS PARA ADES - JUEZ DEL INFRAMUNDO")
    print("=" * 80 + "\n")
    
    # Verificar e instalar dependencias
    if not instalar_dependencias():
        log("Instalación de dependencias falló. Verifica manualmente.", "ERROR")
        return 1
    
    # Crear directorio de salida
    OUTPUT_DIR.mkdir(exist_ok=True)
    log(f"Directorio de salida: {OUTPUT_DIR}", "OK")
    
    # Procesar documentos
    total = 0
    exitosos = 0
    
    for categoria, documentos in DOCUMENTOS.items():
        log(f"\n📂 Procesando categoría: {categoria.upper()}")
        print("-" * 80)
        
        for doc in documentos:
            total += 1
            if procesar_documento(doc):
                exitosos += 1
            print()  # Separador
    
    # Generar resumen
    print("\n" + "-" * 80)
    generar_resumen()
    
    # Reporte final
    print("\n" + "=" * 80)
    print("📊 REPORTE FINAL")
    print("=" * 80)
    print(f"✓ Exitosos: {exitosos}/{total}")
    print(f"✗ Fallidos:  {total - exitosos}/{total}")
    print(f"📂 Archivos en: {OUTPUT_DIR}")
    print("\n💀 Ades está listo para leer las guías y asumir su rol completo.")
    print("=" * 80 + "\n")
    
    return 0 if exitosos == total else 1


if __name__ == "__main__":
    sys.exit(main())

