#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear GitHub Issues desde conversaciones con Zeus
Autor: Zeus (Agente de Asistencia)
Fecha: 21 de noviembre de 2025

Requisitos:
    pip install PyGithub
"""

import os
import sys
from pathlib import Path
import argparse
from datetime import datetime

try:
    from github import Github
except ImportError:
    print("❌ Error: PyGithub no está instalado.")
    print("   Instala con: pip install PyGithub")
    sys.exit(1)

# Configuración
REPO_OWNER = "lmartinezcorral"
REPO_NAME = "maestria-sedentarismo-fuzzy"

def leer_archivo_conversacion(ruta_archivo):
    """Lee el contenido de un archivo de conversación"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_archivo}")
        return None

def crear_issue_desde_conversacion(github_token, titulo, cuerpo, etiquetas=None, asignado=None):
    """
    Crea un GitHub Issue desde una conversación
    
    Args:
        github_token: Token de GitHub (GITHUB_TOKEN o desde variable de entorno)
        titulo: Título del issue
        cuerpo: Cuerpo del issue (puede ser markdown)
        etiquetas: Lista de etiquetas
        asignado: Usuario a asignar (opcional)
    """
    # Obtener token
    if not github_token:
        github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("❌ Error: Se requiere un token de GitHub")
        print("   Configura la variable de entorno GITHUB_TOKEN o usa --token")
        return None
    
    try:
        # Conectar a GitHub
        g = Github(github_token)
        repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
        
        # Crear issue
        issue = repo.create_issue(
            title=titulo,
            body=cuerpo,
            labels=etiquetas or []
        )
        
        # Asignar si se especifica
        if asignado:
            try:
                issue.add_to_assignees(asignado)
            except Exception as e:
                print(f"⚠️  No se pudo asignar a {asignado}: {e}")
        
        print(f"✅ Issue creado: #{issue.number}")
        print(f"   URL: {issue.html_url}")
        return issue
        
    except Exception as e:
        print(f"❌ Error al crear issue: {e}")
        return None

def formatear_cuerpo_issue(conversacion_md, resumen=""):
    """
    Formatea el contenido de una conversación para un GitHub Issue
    """
    cuerpo = f"""## 📋 Resumen

{resumen or "Issue creado desde conversación con Zeus"}

---

## 💬 Conversación Completa

<details>
<summary>Ver conversación completa</summary>

{conversacion_md}

</details>

---

## ✅ Acciones

- [ ] Revisar conversación
- [ ] Implementar cambios sugeridos
- [ ] Verificar funcionamiento

---

*Issue creado automáticamente por Zeus el {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    return cuerpo

def main():
    parser = argparse.ArgumentParser(description='Crear GitHub Issue desde conversación con Zeus')
    parser.add_argument('--titulo', required=True, help='Título del issue')
    parser.add_argument('--cuerpo', help='Cuerpo del issue (markdown)')
    parser.add_argument('--archivo', help='Archivo de conversación a incluir')
    parser.add_argument('--token', help='Token de GitHub (o usar GITHUB_TOKEN)')
    parser.add_argument('--etiquetas', nargs='+', help='Etiquetas para el issue', default=['zeus', 'conversacion'])
    parser.add_argument('--asignado', help='Usuario a asignar el issue')
    parser.add_argument('--resumen', default='', help='Resumen para el issue')
    
    args = parser.parse_args()
    
    # Preparar cuerpo
    if args.archivo:
        conversacion = leer_archivo_conversacion(args.archivo)
        if conversacion:
            cuerpo = formatear_cuerpo_issue(conversacion, args.resumen)
        else:
            cuerpo = args.cuerpo or "Issue creado desde conversación con Zeus"
    else:
        cuerpo = args.cuerpo or "Issue creado desde conversación con Zeus"
    
    # Crear issue
    crear_issue_desde_conversacion(
        github_token=args.token,
        titulo=args.titulo,
        cuerpo=cuerpo,
        etiquetas=args.etiquetas,
        asignado=args.asignado
    )

if __name__ == "__main__":
    main()

