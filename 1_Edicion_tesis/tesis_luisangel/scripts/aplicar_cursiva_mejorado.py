#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mejorado para aplicar formato de cursiva (\textit{}) a anglicismos
y extranjerismos en archivos LaTeX de forma selectiva y precisa.
"""

import re
from pathlib import Path
from typing import List, Tuple

# Lista de anglicismos con sus reemplazos (solo los más críticos y claros)
ANGLICISMOS = [
    # Dispositivos y tecnologías
    ('Apple Watch', r'\\textit{Apple Watch}'),
    ('HealthKit', r'\\textit{HealthKit}'),
    ('wearables', r'\\textit{wearables}'),
    ('wearable', r'\\textit{wearable}'),
    ('BYOD', r'\\textit{BYOD}'),
    ('GPS', r'\\textit{GPS}'),
    ('PPG', r'\\textit{PPG}'),
    ('LED', r'\\textit{LED}'),
    ('SDK', r'\\textit{SDK}'),
    ('API', r'\\textit{API}'),
    
    # Métricas y siglas técnicas
    ('HRV-SDNN', r'\\textit{HRV-SDNN}'),
    ('HRV_SDNN', r'\\textit{HRV-SDNN}'),
    ('HRV', r'\\textit{HRV}'),
    ('SDNN', r'\\textit{SDNN}'),
    ('LOUO', r'\\textit{LOUO}'),
    ('LOOU', r'\\textit{LOOU}'),
    ('F1-Score', r'\\textit{F1-Score}'),
    ('F1 Score', r'\\textit{F1-Score}'),
    ('Recall', r'\\textit{Recall}'),
    ('Precision', r'\\textit{Precision}'),
    ('Accuracy', r'\\textit{Accuracy}'),
    ('MCC', r'\\textit{MCC}'),
    ('IQR', r'\\textit{IQR}'),
    ('MET', r'\\textit{MET}'),
    ('SpO2', r'\\textit{SpO\\textsubscript{2}}'),
    ('VO2', r'\\textit{VO\\textsubscript{2}}'),
    ('FCmax', r'\\textit{FC\\textsubscript{max}}'),
    ('FCmáx', r'\\textit{FC\\textsubscript{máx}}'),
    
    # Métodos y algoritmos
    ('K-Means', r'\\textit{K-Means}'),
    ('K Means', r'\\textit{K-Means}'),
    ('clustering', r'\\textit{clustering}'),
    ('fuzzy', r'\\textit{fuzzy}'),
    ('Mamdani', r'\\textit{Mamdani}'),
    ('Big data', r'\\textit{Big data}'),
    ('World Wide Web', r'\\textit{World Wide Web}'),
    ('internet', r'\\textit{internet}'),
    
    # Lenguajes y herramientas
    ('Python', r'\\textit{Python}'),
    ('Swift', r'\\textit{Swift}'),
    ('pandas', r'\\textit{pandas}'),
    ('numpy', r'\\textit{numpy}'),
    ('pytz', r'\\textit{pytz}'),
    ('GitHub', r'\\textit{GitHub}'),
    ('DataFrame', r'\\textit{DataFrame}'),
    ('CSV', r'\\textit{CSV}'),
    ('XML', r'\\textit{XML}'),
    
    # Términos generales
    ('et al.', r'\\textit{et al.}'),
    ('et al', r'\\textit{et al.}'),
    ('output', r'\\textit{output}'),
    ('input', r'\\textit{input}'),
    ('feedback', r'\\textit{feedback}'),
    ('baseline', r'\\textit{baseline}'),
    ('software', r'\\textit{software}'),
    ('hardware', r'\\textit{hardware}'),
    ('dataset', r'\\textit{dataset}'),
]

def esta_en_comando_latex(texto: str, pos: int) -> bool:
    """Verifica si la posición está dentro de un comando LaTeX."""
    # Buscar comandos LaTeX comunes
    patrones_comandos = [
        r'\\[a-zA-Z]+\{',  # \comando{
        r'\\[a-zA-Z@]+',    # \comando
        r'%',               # Comentarios
    ]
    
    # Verificar si está dentro de llaves de comando
    antes = texto[:pos]
    despues = texto[pos:]
    
    # Contar llaves abiertas y cerradas antes de la posición
    llaves_abiertas = antes.count('{') - antes.count('}')
    
    # Si hay llaves abiertas sin cerrar, probablemente está dentro de un comando
    if llaves_abiertas > 0:
        # Buscar el último comando antes de la posición
        ultimo_comando = re.search(r'\\[a-zA-Z@]+\{?', antes)
        if ultimo_comando:
            return True
    
    # Verificar si está en comentario
    if '%' in antes:
        ultimo_comentario = antes.rfind('%')
        if ultimo_comentario > antes.rfind('\n'):
            return True
    
    return False

def ya_esta_en_cursiva(texto: str, pos: int) -> bool:
    """Verifica si el texto ya está en \textit{}."""
    antes = texto[:pos]
    
    # Buscar todos los \textit{ antes de la posición
    matches = list(re.finditer(r'\\textit\{', antes))
    
    if not matches:
        return False
    
    # Verificar cada \textit{ para ver si la posición está dentro
    for match in matches:
        inicio_cursiva = match.end()
        # Contar llaves para encontrar el cierre
        nivel = 1
        i = inicio_cursiva
        while i < len(texto) and nivel > 0:
            if texto[i] == '{':
                nivel += 1
            elif texto[i] == '}':
                nivel -= 1
            i += 1
        
        fin_cursiva = i - 1
        if inicio_cursiva <= pos <= fin_cursiva:
            return True
    
    return False

def aplicar_cursiva_archivo(archivo_path: Path) -> Tuple[int, List[str]]:
    """Aplica cursiva a anglicismos en un archivo."""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        return 0, [f"Error: {e}"]
    
    contenido_original = contenido
    cambios = 0
    errores = []
    
    # Aplicar cada anglicismo (de más largo a más corto para evitar solapamientos)
    anglicismos_ordenados = sorted(ANGLICISMOS, key=lambda x: len(x[0]), reverse=True)
    
    for anglicismo, reemplazo in anglicismos_ordenados:
        # Crear patrón que busque la palabra completa
        patron = r'\b' + re.escape(anglicismo) + r'\b'
        
        # Buscar todas las ocurrencias
        matches = list(re.finditer(patron, contenido, re.IGNORECASE))
        
        # Procesar de atrás hacia adelante
        for match in reversed(matches):
            inicio = match.start()
            fin = match.end()
            
            # Verificar excepciones
            if esta_en_comando_latex(contenido, inicio):
                continue
            
            if ya_esta_en_cursiva(contenido, inicio):
                continue
            
            # Verificar si está en contexto especial (por ejemplo, en \cite{})
            contexto_antes = contenido[max(0, inicio-20):inicio]
            contexto_despues = contenido[fin:min(len(contenido), fin+20)]
            
            # No modificar si está en comandos de citación
            if '\\cite' in contexto_antes or '\\citep' in contexto_antes or '\\citet' in contexto_antes:
                continue
            
            # No modificar si está en \path{} o \texttt{}
            if '\\path{' in contexto_antes or '\\texttt{' in contexto_antes:
                continue
            
            # Aplicar reemplazo
            contenido = contenido[:inicio] + reemplazo + contenido[fin:]
            cambios += 1
    
    # Guardar solo si hubo cambios
    if cambios > 0:
        try:
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
        except Exception as e:
            errores.append(f"Error guardando: {e}")
    
    return cambios, errores

def main():
    """Función principal."""
    base_dir = Path(__file__).parent.parent
    capitulos_dir = base_dir / 'capitulos'
    main_file = base_dir / 'main.tex'
    
    archivos_tex = []
    if capitulos_dir.exists():
        archivos_tex.extend(sorted(capitulos_dir.glob('*.tex')))
    if main_file.exists():
        archivos_tex.append(main_file)
    
    total_cambios = 0
    todos_errores = []
    
    print("Aplicando cursiva a anglicismos...\n")
    
    for archivo in archivos_tex:
        cambios, errores = aplicar_cursiva_archivo(archivo)
        total_cambios += cambios
        todos_errores.extend(errores)
        if cambios > 0:
            print(f"✅ {archivo.name}: {cambios} cambios")
        else:
            print(f"⚪ {archivo.name}: sin cambios")
    
    print(f"\n✅ Total: {total_cambios} cambios aplicados")
    if todos_errores:
        print(f"⚠️  Errores: {len(todos_errores)}")
    
    return total_cambios

if __name__ == '__main__':
    main()

