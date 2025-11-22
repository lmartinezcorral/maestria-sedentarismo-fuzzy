#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para aplicar formato de cursiva (\textit{}) a anglicismos y extranjerismos
en archivos LaTeX según normas de redacción en español.
"""

import re
import os
from pathlib import Path
from typing import List, Tuple

# Mapeo de anglicismos a sus versiones con cursiva
# Formato: (patrón_regex, reemplazo_con_cursiva, flags)
ANGLICISMOS_CURSIVA = [
    # Dispositivos y tecnologías (solo si no están ya en cursiva)
    (r'\bApple Watch\b', r'\\textit{Apple Watch}', re.IGNORECASE),
    (r'\bHealthKit\b', r'\\textit{HealthKit}', re.IGNORECASE),
    (r'\bwearables?\b', r'\\textit{wearable\\textsubscript{s}}' if 's' else r'\\textit{wearable}', re.IGNORECASE),
    (r'\bBYOD\b', r'\\textit{BYOD}', re.IGNORECASE),
    (r'\bGPS\b', r'\\textit{GPS}', re.IGNORECASE),
    (r'\bPPG\b', r'\\textit{PPG}', re.IGNORECASE),
    (r'\bLED\b', r'\\textit{LED}', re.IGNORECASE),
    (r'\bSDK\b', r'\\textit{SDK}', re.IGNORECASE),
    (r'\bAPI\b', r'\\textit{API}', re.IGNORECASE),
    
    # Métricas y siglas técnicas
    (r'\bHRV[-_]?SDNN\b', r'\\textit{HRV-SDNN}', re.IGNORECASE),
    (r'\bHRV\b(?![-_])', r'\\textit{HRV}', re.IGNORECASE),  # HRV solo si no es parte de HRV-SDNN
    (r'\bSDNN\b', r'\\textit{SDNN}', re.IGNORECASE),
    (r'\bLOUO\b', r'\\textit{LOUO}', re.IGNORECASE),
    (r'\bLOOU\b', r'\\textit{LOOU}', re.IGNORECASE),
    (r'\bF1[- ]Score\b', r'\\textit{F1-Score}', re.IGNORECASE),
    (r'\bRecall\b', r'\\textit{Recall}', re.IGNORECASE),
    (r'\bPrecision\b', r'\\textit{Precision}', re.IGNORECASE),
    (r'\bAccuracy\b', r'\\textit{Accuracy}', re.IGNORECASE),
    (r'\bMCC\b', r'\\textit{MCC}', re.IGNORECASE),
    (r'\bCV\b(?!\w)', r'\\textit{CV}', 0),  # CV solo si es palabra completa (no Ciudad de México en contexto)
    (r'\bIQR\b', r'\\textit{IQR}', re.IGNORECASE),
    (r'\bMET\b', r'\\textit{MET}', re.IGNORECASE),
    (r'\bSpO2\b', r'\\textit{SpO\\textsubscript{2}}', re.IGNORECASE),
    (r'\bVO2\b', r'\\textit{VO\\textsubscript{2}}', re.IGNORECASE),
    (r'\bFCmax\b', r'\\textit{FC\\textsubscript{max}}', re.IGNORECASE),
    (r'\bFCmáx\b', r'\\textit{FC\\textsubscript{máx}}', re.IGNORECASE),
    
    # Métodos y algoritmos
    (r'\bK[- ]Means\b', r'\\textit{K-Means}', re.IGNORECASE),
    (r'\bclustering\b', r'\\textit{clustering}', re.IGNORECASE),
    (r'\bfuzzy\b', r'\\textit{fuzzy}', re.IGNORECASE),
    (r'\bMamdani\b', r'\\textit{Mamdani}', re.IGNORECASE),
    (r'\bBig data\b', r'\\textit{Big data}', re.IGNORECASE),
    (r'\bWorld Wide Web\b', r'\\textit{World Wide Web}', re.IGNORECASE),
    (r'\binternet\b', r'\\textit{internet}', re.IGNORECASE),
    
    # Lenguajes y herramientas
    (r'\bPython\b', r'\\textit{Python}', re.IGNORECASE),
    (r'\bSwift\b', r'\\textit{Swift}', re.IGNORECASE),
    (r'\bpandas\b', r'\\textit{pandas}', re.IGNORECASE),
    (r'\bnumpy\b', r'\\textit{numpy}', re.IGNORECASE),
    (r'\bpytz\b', r'\\textit{pytz}', re.IGNORECASE),
    (r'\bGitHub\b', r'\\textit{GitHub}', re.IGNORECASE),
    (r'\bDataFrame\b', r'\\textit{DataFrame}', re.IGNORECASE),
    (r'\bCSV\b', r'\\textit{CSV}', re.IGNORECASE),
    (r'\bXML\b', r'\\textit{XML}', re.IGNORECASE),
    
    # Términos generales
    (r'\bet al\.', r'\\textit{et al.}', re.IGNORECASE),
    (r'\boutput\b', r'\\textit{output}', re.IGNORECASE),
    (r'\binput\b', r'\\textit{input}', re.IGNORECASE),
    (r'\bfeedback\b', r'\\textit{feedback}', re.IGNORECASE),
    (r'\bbaseline\b', r'\\textit{baseline}', re.IGNORECASE),
    (r'\bsoftware\b', r'\\textit{software}', re.IGNORECASE),
    (r'\bhardware\b', r'\\textit{hardware}', re.IGNORECASE),
    (r'\bdataset\b', r'\\textit{dataset}', re.IGNORECASE),
]

# Patrones que NO deben ser modificados
EXCEPCIONES = [
    r'\\textit\{',      # Ya está en cursiva
    r'\\cite\{',        # Comandos de citación
    r'\\citep\{',
    r'\\citet\{',
    r'\\path\{',        # Comandos de path
    r'\\nolinkurl\{',
    r'\\texttt\{',      # Texto tipo máquina
    r'\\textbf\{',      # Texto en negrita
    r'\\Cref\{',        # Referencias cruzadas
    r'\\cref\{',
    r'\\ref\{',
    r'\\label\{',
    r'\\caption\{',
    r'\\begin\{',       # Entornos LaTeX
    r'\\end\{',
    r'\\section\{',
    r'\\subsection\{',
    r'\\subsubsection\{',
    r'\\chapter\{',
    r'\\usepackage',
    r'\\documentclass',
    r'\\newcommand',
    r'\\renewcommand',
    r'\\newenvironment',
    r'\\def',
    r'\\let',
    r'\\makeatletter',
    r'\\makeatother',
    r'%',               # Comentarios
]

def esta_en_excepcion(texto: str, posicion: int) -> bool:
    """Verifica si una posición está dentro de una excepción."""
    for patron_excepcion in EXCEPCIONES:
        # Buscar todas las ocurrencias del patrón de excepción
        for match in re.finditer(patron_excepcion, texto):
            if match.start() <= posicion <= match.end():
                return True
    return False

def ya_esta_en_cursiva(texto: str, posicion: int) -> bool:
    """Verifica si el texto en la posición ya está dentro de \textit{}."""
    # Buscar \textit{ más cercano antes de la posición
    antes = texto[:posicion]
    patron_cursiva = r'\\textit\{'
    matches = list(re.finditer(patron_cursiva, antes))
    
    if not matches:
        return False
    
    # Encontrar el último \textit{ antes de la posición
    ultimo_match = matches[-1]
    inicio_cursiva = ultimo_match.end()
    
    # Contar llaves para encontrar el cierre
    nivel_llaves = 1
    i = inicio_cursiva
    while i < len(texto) and nivel_llaves > 0:
        if texto[i] == '{':
            nivel_llaves += 1
        elif texto[i] == '}':
            nivel_llaves -= 1
        i += 1
    
    fin_cursiva = i - 1
    
    # Verificar si la posición está dentro del rango de cursiva
    return inicio_cursiva <= posicion <= fin_cursiva

def aplicar_cursiva_anglicismo(texto: str, patron: str, reemplazo: str, flags: int) -> Tuple[str, int]:
    """
    Aplica cursiva a un anglicismo si no está ya en cursiva o en excepción.
    Retorna (texto_modificado, numero_cambios).
    """
    cambios = 0
    texto_modificado = texto
    
    # Buscar todas las ocurrencias
    matches = list(re.finditer(patron, texto, flags))
    
    # Procesar de atrás hacia adelante para no afectar las posiciones
    for match in reversed(matches):
        inicio = match.start()
        fin = match.end()
        texto_original = match.group(0)
        
        # Verificar excepciones
        if esta_en_excepcion(texto, inicio):
            continue
        
        # Verificar si ya está en cursiva
        if ya_esta_en_cursiva(texto, inicio):
            continue
        
        # Aplicar reemplazo
        # Ajustar reemplazo para mantener el texto original si es necesario
        reemplazo_ajustado = reemplazo
        if '\\textsubscript{s}' in reemplazo and texto_original.endswith('s'):
            # Mantener la 's' fuera de cursiva si es plural
            reemplazo_ajustado = reemplazo.replace('\\textsubscript{s}', 's')
        
        texto_modificado = texto_modificado[:inicio] + reemplazo_ajustado + texto_modificado[fin:]
        cambios += 1
    
    return texto_modificado, cambios

def procesar_archivo(archivo_path: Path) -> Tuple[int, List[str]]:
    """Procesa un archivo LaTeX aplicando cursiva a anglicismos."""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        return 0, [f"Error leyendo {archivo_path}: {e}"]
    
    contenido_original = contenido
    total_cambios = 0
    errores = []
    
    # Aplicar cada patrón de anglicismo
    for patron, reemplazo, flags in ANGLICISMOS_CURSIVA:
        try:
            contenido, cambios = aplicar_cursiva_anglicismo(contenido, patron, reemplazo, flags)
            total_cambios += cambios
        except Exception as e:
            errores.append(f"Error aplicando {patron}: {e}")
    
    # Guardar solo si hubo cambios
    if total_cambios > 0:
        try:
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
        except Exception as e:
            errores.append(f"Error guardando {archivo_path}: {e}")
    
    return total_cambios, errores

def main():
    """Función principal."""
    base_dir = Path(__file__).parent.parent
    capitulos_dir = base_dir / 'capitulos'
    main_file = base_dir / 'main.tex'
    
    archivos_tex = []
    if capitulos_dir.exists():
        archivos_tex.extend(capitulos_dir.glob('*.tex'))
    if main_file.exists():
        archivos_tex.append(main_file)
    
    total_global = 0
    todos_errores = []
    
    print("Aplicando cursiva a anglicismos...\n")
    
    for archivo in archivos_tex:
        cambios, errores = procesar_archivo(archivo)
        total_global += cambios
        todos_errores.extend(errores)
        if cambios > 0:
            print(f"✅ {archivo.name}: {cambios} cambios aplicados")
        else:
            print(f"⚪ {archivo.name}: sin cambios")
    
    print(f"\n✅ Total de cambios aplicados: {total_global}")
    if todos_errores:
        print(f"⚠️  Errores encontrados: {len(todos_errores)}")
        for error in todos_errores:
            print(f"   - {error}")
    
    return total_global, todos_errores

if __name__ == '__main__':
    main()

