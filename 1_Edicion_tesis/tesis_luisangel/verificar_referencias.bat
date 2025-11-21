@echo off
REM ============================================================================
REM Script para verificar referencias bibliográficas en múltiples bases de datos
REM Autor: Luis Angel Martínez Corral
REM Fecha: Noviembre 2025
REM ============================================================================

echo.
echo ============================================================================
echo   VERIFICADOR DE REFERENCIAS BIBLIOGRÁFICAS
echo   Verificación en múltiples bases de datos académicas
echo ============================================================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    echo Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado
python --version
echo.

REM Verificar que el archivo referencias.bib existe
if not exist "referencias.bib" (
    echo [ERROR] No se encontró el archivo referencias.bib
    echo.
    echo Por favor asegúrate de que el archivo referencias.bib esté en la misma
    echo carpeta que este script.
    echo.
    pause
    exit /b 1
)

echo [OK] Archivo referencias.bib encontrado
echo.

REM Instalar dependencias si es necesario
echo [INFO] Verificando dependencias...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando biblioteca 'requests'...
    python -m pip install --quiet requests
    if errorlevel 1 (
        echo [ERROR] No se pudo instalar la biblioteca 'requests'
        echo.
        echo Intenta instalar manualmente con: pip install requests
        echo.
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas correctamente
) else (
    echo [OK] Dependencias ya instaladas
)
echo.

REM Ejecutar el script de verificación
echo ============================================================================
echo   Iniciando verificación de referencias...
echo ============================================================================
echo.
echo NOTA: Este proceso puede tardar varios minutos dependiendo del número
echo       de referencias en el archivo .bib
echo.

python verificar_multiple_bases_datos.py

if errorlevel 1 (
    echo.
    echo [ERROR] Ocurrió un error durante la ejecución
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo   Verificación completada exitosamente
echo ============================================================================
echo.
echo Archivos generados:
echo   - referencias_multiple_bases_datos.csv
echo   - referencias_multiple_bases_datos.json
echo.
echo Puedes abrir el archivo CSV con Excel o cualquier editor de texto.
echo.
pause

