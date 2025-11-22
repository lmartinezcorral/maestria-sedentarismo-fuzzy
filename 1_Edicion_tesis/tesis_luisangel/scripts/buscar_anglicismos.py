#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para identificar anglicismos y extranjerismos en archivos LaTeX
que requieren formato de cursiva según normas de redacción en español.
"""

import re
import os
from pathlib import Path

# Lista de anglicismos y extranjerismos comunes en el documento
ANGLICISMOS = [
    # Dispositivos y tecnologías
    r'Apple Watch',
    r'HealthKit',
    r'wearable[s]?',
    r'BYOD',
    r'GPS',
    r'PPG',
    r'LED',
    r'SDK',
    r'API',
    
    # Métricas y siglas técnicas
    r'HRV[-_]?SDNN',
    r'HRV',
    r'SDNN',
    r'LOUO',
    r'LOOU',
    r'F1[- ]Score',
    r'Recall',
    r'Precision',
    r'Accuracy',
    r'MCC',
    r'CV\b',  # Coeficiente de variación (no Ciudad de México)
    r'IQR',
    r'MET',
    r'SpO2',
    r'VO2',
    r'FCmax',
    r'FCmáx',
    
    # Métodos y algoritmos
    r'K[- ]Means',
    r'clustering',
    r'fuzzy',
    r'Mamdani',
    r'Big data',
    r'World Wide Web',
    r'internet',
    
    # Lenguajes y herramientas
    r'Python',
    r'Swift',
    r'pandas',
    r'numpy',
    r'pytz',
    r'GitHub',
    r'DataFrame',
    r'CSV',
    r'XML',
    
    # Variables y nombres técnicos
    r'sourceName',
    r'startDate',
    r'endDate',
    r'Record',
    r'ActiveEnergyBurned',
    r'AppleExerciseTime',
    r'AppleStandHour',
    r'AppleStandTime',
    r'DistanceWalkingRunning',
    r'HeartRate',
    r'StepCount',
    r'WalkingHeartRateAverage',
    r'export\.zip',
    r'DB_u',
    r'apple_health_data_converter\.py',
    
    # Términos generales
    r'\bet al\.',
    r'output',
    r'input',
    r'feedback',
    r'baseline',
    r'software',
    r'hardware',
    r'dataset',
    
    # Siglas médicas (algunas pueden ser anglicismos)
    r'CVRS',
    r'ENT',
    r'AF\b',  # Actividad Física (no siempre anglicismo, pero puede serlo en contexto)
    r'EF\b',  # Ejercicio Físico
    r'CS\b',  # Comportamiento Sedentario
    r'PA\b',  # Presión Arterial
    r'FR\b',  # Frecuencia Respiratoria
    r'GPAQ',
    r'SF[- ]36',
    r'OMS\b',  # Organización Mundial de la Salud (no anglicismo, pero verificar)
    r'WHO\b',  # World Health Organization
    r'IEC\b',  # International Electrotechnical Commission
    r'TC\b',   # Technical Committee
    r'NR\b',   # No reportado
    r'DMD\b',  # Distrofia Muscular de Duchenne
]

# Patrones que NO deben ser modificados (ya están en cursiva o son parte de comandos LaTeX)
EXCEPCIONES = [
    r'\\textit\{',  # Ya está en cursiva
    r'\\cite\{',    # Comandos de citación
    r'\\citep\{',
    r'\\citet\{',
    r'\\path\{',    # Comandos de path
    r'\\nolinkurl\{',
    r'\\texttt\{',  # Texto tipo máquina
    r'\\textbf\{', # Texto en negrita
    r'\\Cref\{',    # Referencias cruzadas
    r'\\cref\{',
    r'\\ref\{',
]

def buscar_anglicismos_en_archivo(archivo_path):
    """Busca anglicismos en un archivo LaTeX."""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"Error leyendo {archivo_path}: {e}")
        return []
    
    anglicismos_encontrados = []
    lineas = contenido.split('\n')
    
    for num_linea, linea in enumerate(lineas, 1):
        # Saltar líneas que son comentarios LaTeX
        if linea.strip().startswith('%'):
            continue
        
        # Verificar si la línea contiene algún comando LaTeX que ya formatea
        tiene_formato = any(re.search(patron, linea) for patron in EXCEPCIONES)
        
        for patron in ANGLICISMOS:
            # Buscar el patrón (case-insensitive)
            matches = re.finditer(patron, linea, re.IGNORECASE)
            for match in matches:
                texto_encontrado = match.group(0)
                
                # Verificar que no esté ya en cursiva
                inicio = match.start()
                fin = match.end()
                
                # Buscar si está dentro de \textit{...}
                antes = linea[:inicio]
                despues = linea[fin:]
                
                # Verificar si ya está en cursiva
                ya_en_cursiva = False
                if '\\textit{' in antes:
                    # Contar llaves abiertas y cerradas
                    antes_cursiva = antes.split('\\textit{')[-1]
                    if antes_cursiva.count('{') > antes_cursiva.count('}'):
                        ya_en_cursiva = True
                
                if not ya_en_cursiva and not tiene_formato:
                    anglicismos_encontrados.append({
                        'archivo': str(archivo_path),
                        'linea': num_linea,
                        'texto': texto_encontrado,
                        'contexto': linea.strip()[:100]
                    })
    
    return anglicismos_encontrados

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
    
    todos_anglicismos = []
    
    for archivo in archivos_tex:
        print(f"Buscando en: {archivo.name}...")
        anglicismos = buscar_anglicismos_en_archivo(archivo)
        todos_anglicismos.extend(anglicismos)
        print(f"  Encontrados: {len(anglicismos)}")
    
    # Agrupar por tipo de anglicismo
    anglicismos_por_tipo = {}
    for item in todos_anglicismos:
        texto = item['texto']
        if texto not in anglicismos_por_tipo:
            anglicismos_por_tipo[texto] = []
        anglicismos_por_tipo[texto].append(item)
    
    # Generar reporte
    reporte = []
    reporte.append("# ANGLICISMOS Y EXTRANJERISMOS ENCONTRADOS EN LA TESIS\n")
    reporte.append(f"**Fecha:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    reporte.append(f"**Total de ocurrencias:** {len(todos_anglicismos)}\n")
    reporte.append(f"**Total de tipos únicos:** {len(anglicismos_por_tipo)}\n\n")
    reporte.append("---\n\n")
    
    # Ordenar por frecuencia
    anglicismos_ordenados = sorted(anglicismos_por_tipo.items(), 
                                   key=lambda x: len(x[1]), 
                                   reverse=True)
    
    for texto, ocurrencias in anglicismos_ordenados:
        reporte.append(f"## {texto}\n")
        reporte.append(f"**Frecuencia:** {len(ocurrencias)} ocurrencias\n\n")
        reporte.append("**Ubicaciones:**\n\n")
        for ocurrencia in ocurrencias[:10]:  # Mostrar máximo 10 por tipo
            reporte.append(f"- `{ocurrencia['archivo']}` línea {ocurrencia['linea']}: `{ocurrencia['contexto']}`\n")
        if len(ocurrencias) > 10:
            reporte.append(f"- ... y {len(ocurrencias) - 10} más\n")
        reporte.append("\n")
    
    # Guardar reporte
    reporte_path = base_dir.parent / 'Notas_logs_comunicacion_resumenes' / 'ANGLICISMOS_ENCONTRADOS_TESIS.md'
    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write(''.join(reporte))
    
    print(f"\n✅ Reporte guardado en: {reporte_path}")
    print(f"✅ Total de anglicismos encontrados: {len(todos_anglicismos)}")
    print(f"✅ Tipos únicos: {len(anglicismos_por_tipo)}")
    
    return todos_anglicismos, anglicismos_por_tipo

if __name__ == '__main__':
    main()

