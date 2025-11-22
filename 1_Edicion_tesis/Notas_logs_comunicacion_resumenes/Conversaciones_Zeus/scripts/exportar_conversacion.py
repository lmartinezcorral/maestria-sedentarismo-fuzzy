#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para exportar conversaciones con Zeus a archivos Markdown
Autor: Zeus (Agente de Asistencia)
Fecha: 21 de noviembre de 2025
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import argparse

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent.parent.parent
CONVERSACIONES_DIR = BASE_DIR / "Conversaciones_Zeus" / "conversaciones"
TEMPLATE_DIR = BASE_DIR / "Conversaciones_Zeus" / "templates"
TEMPLATE_FILE = TEMPLATE_DIR / "template_conversacion.md"

def cargar_template():
    """Carga el template de conversación"""
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️  Template no encontrado en {TEMPLATE_FILE}")
        return None

def crear_archivo_conversacion(tema, contenido_conversacion, resumen="", acciones=[], archivos_modificados=[], comandos=[]):
    """
    Crea un archivo markdown con la conversación
    
    Args:
        tema: Tema principal de la conversación
        contenido_conversacion: Lista de tuplas (usuario/zeus, mensaje, hora)
        resumen: Resumen ejecutivo
        acciones: Lista de acciones realizadas
        archivos_modificados: Lista de archivos modificados
        comandos: Lista de comandos ejecutados
    """
    # Asegurar que el directorio existe
    CONVERSACIONES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre de archivo
    fecha = datetime.now().strftime("%Y-%m-%d")
    tema_slug = tema.lower().replace(" ", "_").replace("/", "-")[:50]
    nombre_archivo = f"{fecha}_{tema_slug}.md"
    ruta_archivo = CONVERSACIONES_DIR / nombre_archivo
    
    # Cargar template
    template = cargar_template()
    if not template:
        # Crear template básico si no existe
        template = """# Conversación con Zeus - {fecha}

**Participante:** Luis Angel Martínez Corral  
**Agente:** Zeus ⚡  
**Fecha:** {fecha_hora}  
**Tema Principal:** {tema}  
**Estado:** ✅ Completado

---

## 📋 Resumen Ejecutivo

{resumen}

---

## 💬 Conversación Completa

{conversacion}

---

## ✅ Acciones Realizadas

{acciones}

---

## 📁 Archivos Modificados/Creados

{archivos}

---

## 🔧 Comandos Ejecutados

{comandos}

---

*Conversación exportada por Zeus el {fecha}*
"""
    
    # Formatear conversación
    conversacion_texto = ""
    for tipo, mensaje, hora in contenido_conversacion:
        emoji = "👤" if tipo.lower() == "usuario" else "⚡"
        nombre = "Usuario" if tipo.lower() == "usuario" else "Zeus"
        conversacion_texto += f"### {emoji} {nombre} - {hora}\n{mensaje}\n\n---\n\n"
    
    # Formatear acciones
    acciones_texto = "\n".join([f"- [x] {accion}" for accion in acciones])
    
    # Formatear archivos
    archivos_texto = "\n".join([f"- `{archivo}`" for archivo in archivos_modificados])
    
    # Formatear comandos
    comandos_texto = "\n".join([f"```bash\n{cmd}\n```" for cmd in comandos])
    
    # Reemplazar en template
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M")
    contenido = template.format(
        fecha=fecha,
        fecha_hora=fecha_hora,
        tema=tema,
        resumen=resumen or "Conversación sobre " + tema,
        conversacion=conversacion_texto,
        acciones=acciones_texto or "- Ninguna acción registrada",
        archivos=archivos_texto or "- Ningún archivo modificado",
        comandos=comandos_texto or "# No se ejecutaron comandos"
    )
    
    # Escribir archivo
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Conversación exportada a: {ruta_archivo}")
    return ruta_archivo

def main():
    parser = argparse.ArgumentParser(description='Exportar conversación con Zeus a Markdown')
    parser.add_argument('--tema', required=True, help='Tema principal de la conversación')
    parser.add_argument('--resumen', default='', help='Resumen ejecutivo')
    parser.add_argument('--archivo', help='Nombre del archivo de salida (opcional)')
    parser.add_argument('--interactivo', action='store_true', help='Modo interactivo para ingresar conversación')
    
    args = parser.parse_args()
    
    if args.interactivo:
        print("📝 Modo interactivo - Ingresa la conversación (Ctrl+D o Ctrl+Z para finalizar):\n")
        conversacion = []
        tipo_actual = "usuario"
        
        try:
            while True:
                print(f"\n[{tipo_actual.upper()}] Ingresa mensaje (o 'cambiar' para cambiar de usuario/zeus, 'fin' para terminar):")
                mensaje = input()
                
                if mensaje.lower() == 'fin':
                    break
                elif mensaje.lower() == 'cambiar':
                    tipo_actual = "zeus" if tipo_actual == "usuario" else "usuario"
                    continue
                
                hora = datetime.now().strftime("%H:%M")
                conversacion.append((tipo_actual, mensaje, hora))
        except EOFError:
            pass
        
        acciones = []
        print("\n📋 Ingresa acciones realizadas (una por línea, Enter vacío para terminar):")
        while True:
            accion = input()
            if not accion:
                break
            acciones.append(accion)
        
        archivos = []
        print("\n📁 Ingresa archivos modificados (uno por línea, Enter vacío para terminar):")
        while True:
            archivo = input()
            if not archivo:
                break
            archivos.append(archivo)
        
        crear_archivo_conversacion(
            tema=args.tema,
            contenido_conversacion=conversacion,
            resumen=args.resumen,
            acciones=acciones,
            archivos_modificados=archivos
        )
    else:
        # Modo simple - solo crea estructura básica
        crear_archivo_conversacion(
            tema=args.tema,
            contenido_conversacion=[],
            resumen=args.resumen or f"Conversación sobre {args.tema}",
            acciones=[],
            archivos_modificados=[]
        )

if __name__ == "__main__":
    main()

