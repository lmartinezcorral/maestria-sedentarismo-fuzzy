@echo off
chcp 65001 >nul
title Herramienta de Bibliografía para LaTeX - UACH

echo.
echo ================================================================================
echo   HERRAMIENTA DE BIBLIOGRAFÍA PARA LATEX
echo   Facultad de Medicina y Ciencias Biomédicas - UACH
echo ================================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado
    echo.
    echo Para instalar Python:
    echo 1. Ve a https://www.python.org/downloads/
    echo 2. Descarga la versión más reciente
    echo 3. Durante la instalación, marca "Add Python to PATH"
    echo 4. Reinicia esta ventana y vuelve a ejecutar
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Verificar conexión a internet
ping google.com -n 1 >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: No hay conexión a internet
    echo    Esta herramienta necesita internet para funcionar
    echo.
    pause
    exit /b 1
)

echo ✅ Conexión a internet verificada
echo.

REM Verificar que hay PDFs en la carpeta
dir *.pdf >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: No se encontraron archivos PDF en esta carpeta
    echo.
    echo Para usar esta herramienta:
    echo 1. Coloca tus archivos PDF en esta misma carpeta
    echo 2. Vuelve a ejecutar este archivo
    echo.
    pause
    exit /b 1
)

echo ✅ Archivos PDF encontrados
echo.

REM Ejecutar el script Python
echo 🚀 Iniciando procesamiento...
echo.
python generar_referencias.py

echo.
echo ================================================================================
echo   PROCESO COMPLETADO
echo ================================================================================
echo.
echo Los archivos se han generado en esta misma carpeta:
echo   • referencias.csv - Tabla con todas las referencias
echo   • referencias.bib - Archivo BibTeX para LaTeX
echo.
echo Para usar en tu tesis:
echo 1. Copia referencias.bib a tu carpeta de tesis
echo 2. En tu archivo .tex, usa: \cite{autor2024}
echo.
pause