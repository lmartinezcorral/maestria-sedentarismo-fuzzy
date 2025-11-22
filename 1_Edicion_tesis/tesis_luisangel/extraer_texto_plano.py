#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer texto plano de archivos LaTeX
Elimina comandos LaTeX y mantiene solo el texto legible
"""

import re
import os

def limpiar_latex(texto):
    """Elimina comandos LaTeX y mantiene solo el texto"""
    
    # Eliminar comentarios
    texto = re.sub(r'%.*', '', texto)
    
    # Eliminar comandos de formato comunes (mantener el contenido entre llaves)
    texto = re.sub(r'\\chapter\{([^}]+)\}', r'\n\n=== CAPÍTULO: \1 ===\n\n', texto)
    texto = re.sub(r'\\section\{([^}]+)\}', r'\n\n--- SECCIÓN: \1 ---\n\n', texto)
    texto = re.sub(r'\\subsection\{([^}]+)\}', r'\n\n--- Subsección: \1 ---\n\n', texto)
    texto = re.sub(r'\\subsubsection\{([^}]+)\}', r'\n\n--- Subsubsección: \1 ---\n\n', texto)
    
    # Eliminar otros comandos LaTeX comunes
    texto = re.sub(r'\\label\{[^}]+\}', '', texto)
    texto = re.sub(r'\\cite\{[^}]+\}', '[CITA]', texto)
    texto = re.sub(r'\\citep\{[^}]+\}', '[CITA]', texto)
    texto = re.sub(r'\\citet\{[^}]+\}', '[CITA]', texto)
    texto = re.sub(r'\\ref\{[^}]+\}', '[REF]', texto)
    texto = re.sub(r'\\Cref\{[^}]+\}', '[REF]', texto)
    texto = re.sub(r'\\cref\{[^}]+\}', '[REF]', texto)
    texto = re.sub(r'\\textbf\{([^}]+)\}', r'\1', texto)
    texto = re.sub(r'\\textit\{([^}]+)\}', r'\1', texto)
    texto = re.sub(r'\\emph\{([^}]+)\}', r'\1', texto)
    texto = re.sub(r'\\underline\{([^}]+)\}', r'\1', texto)
    texto = re.sub(r'\\noindent', '', texto)
    texto = re.sub(r'\\vspace\{[^}]+\}', '\n', texto)
    texto = re.sub(r'\\hspace\{[^}]+\}', ' ', texto)
    texto = re.sub(r'\\newpage', '\n\n--- NUEVA PÁGINA ---\n\n', texto)
    texto = re.sub(r'\\clearpage', '\n\n--- NUEVA PÁGINA ---\n\n', texto)
    
    # Eliminar entornos de figuras y tablas (mantener solo el caption)
    texto = re.sub(r'\\begin\{figure\}[^}]*\}.*?\\caption\{([^}]+)\}.*?\\end\{figure\}', 
                   r'\n[FIGURA: \1]\n', texto, flags=re.DOTALL)
    texto = re.sub(r'\\begin\{table\}[^}]*\}.*?\\caption\{([^}]+)\}.*?\\end\{table\}', 
                   r'\n[TABLA: \1]\n', texto, flags=re.DOTALL)
    texto = re.sub(r'\\begin\{longtable\}[^}]*\}.*?\\caption\{([^}]+)\}.*?\\end\{longtable\}', 
                   r'\n[TABLA: \1]\n', texto, flags=re.DOTALL)
    
    # Eliminar ecuaciones (mantener solo una referencia)
    texto = re.sub(r'\\begin\{equation\}[^}]*\}.*?\\end\{equation\}', '[ECUACIÓN]', texto, flags=re.DOTALL)
    texto = re.sub(r'\\begin\{align\}[^}]*\}.*?\\end\{align\}', '[ECUACIÓN]', texto, flags=re.DOTALL)
    texto = re.sub(r'\$[^$]+\$', '[FÓRMULA]', texto)
    texto = re.sub(r'\$\$[^$]+\$\$', '[FÓRMULA]', texto)
    
    # Eliminar comandos de listas pero mantener el contenido
    texto = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', 
                   lambda m: re.sub(r'\\item\s*', '\n- ', m.group(0)), texto, flags=re.DOTALL)
    texto = re.sub(r'\\begin\{itemize\}.*?\\end\{itemize\}', 
                   lambda m: re.sub(r'\\item\s*', '\n- ', m.group(0)), texto, flags=re.DOTALL)
    texto = re.sub(r'\\item\s*', '\n- ', texto)
    
    # Eliminar comandos restantes
    texto = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})*', '', texto)
    
    # Limpiar caracteres especiales LaTeX
    texto = texto.replace('~', ' ')
    texto = texto.replace('&', ' ')
    texto = texto.replace('\\\\', '\n')
    texto = texto.replace('\\', '')
    
    # Limpiar llaves y corchetes vacíos
    texto = re.sub(r'\{[^}]*\}', lambda m: m.group(0)[1:-1] if len(m.group(0)) > 2 else '', texto)
    texto = texto.replace('{', '').replace('}', '')
    
    # Limpiar espacios múltiples y saltos de línea excesivos
    texto = re.sub(r' +', ' ', texto)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    
    return texto.strip()

def procesar_archivo(ruta):
    """Procesa un archivo LaTeX y retorna el texto limpio"""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return limpiar_latex(contenido)
    except Exception as e:
        return f"[ERROR al procesar {ruta}: {str(e)}]"

def main():
    # Archivos a procesar
    archivos = [
        'main.tex',
        'capitulos/01_introduccion.tex',
        'capitulos/02_marco_teorico_antecedentes.tex',
        'capitulos/03_delimitacion.tex',
        'capitulos/04_justificacion.tex',
        'capitulos/05_materiales_metodos.tex',
        'capitulos/06_resultados.tex',
        'capitulos/07_discusion.tex',
        'capitulos/08_conclusiones.tex',
        'capitulos/09_anexos.tex'
    ]
    
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("TESIS - TEXTO PLANO PARA REVISIÓN DE SINTAXIS Y ORTOGRAFÍA")
    output_lines.append("=" * 80)
    output_lines.append("")
    output_lines.append("NOTA: Este archivo contiene el texto extraído de los archivos LaTeX")
    output_lines.append("sin formato. Los comandos LaTeX han sido eliminados o reemplazados")
    output_lines.append("por marcadores simples ([CITA], [REF], [FIGURA], [TABLA], [ECUACIÓN]).")
    output_lines.append("")
    output_lines.append("=" * 80)
    output_lines.append("")
    
    for archivo in archivos:
        if os.path.exists(archivo):
            output_lines.append("\n" + "=" * 80)
            output_lines.append(f"ARCHIVO: {archivo}")
            output_lines.append("=" * 80 + "\n")
            texto_limpio = procesar_archivo(archivo)
            output_lines.append(texto_limpio)
            output_lines.append("\n")
        else:
            output_lines.append(f"\n[ARCHIVO NO ENCONTRADO: {archivo}]\n")
    
    # Escribir archivo de salida
    output_text = '\n'.join(output_lines)
    with open('tesis_texto_plano.txt', 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    print(f"Archivo generado: tesis_texto_plano.txt")
    print(f"Tamaño: {len(output_text)} caracteres")

if __name__ == '__main__':
    main()

