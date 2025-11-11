@echo off
:: ============================================================================
:: SCRIPT DE COMPILACIÓN AUTOMÁTICA PARA TESIS
:: ============================================================================
:: Este script compila tu tesis LaTeX automáticamente
:: Uso: Doble click en este archivo
:: ============================================================================

echo.
echo ========================================
echo   COMPILANDO TU TESIS...
echo ========================================
echo.

:: Nombre del archivo principal (sin extensión .tex)
set ARCHIVO=plantilla_tesis

:: Paso 0: Limpiar archivos auxiliares previos (evita problemas de cache)
echo [0/4] Limpiando archivos auxiliares previos...
del %ARCHIVO%.aux %ARCHIVO%.log %ARCHIVO%.out %ARCHIVO%.toc %ARCHIVO%.lof %ARCHIVO%.lot %ARCHIVO%.bbl %ARCHIVO%.blg %ARCHIVO%.bcf %ARCHIVO%.run.xml 2>nul
del capitulos\*.aux 2>nul
echo.

:: Paso 1: Primera compilación con pdflatex
echo [1/4] Primera compilacion (pdflatex)...
pdflatex -interaction=nonstopmode %ARCHIVO%.tex
if errorlevel 1 (
    echo.
    echo ERROR: Fallo en la primera compilacion
    echo Revisa el archivo %ARCHIVO%.log para detalles
    pause
    exit /b 1
)

:: Paso 2: Generar bibliografía con biber (biblatex)
echo [2/4] Generando bibliografia (biber)...
biber %ARCHIVO%
if errorlevel 1 (
    echo.
    echo ADVERTENCIA: Hubo problemas con la bibliografia
    echo Continuando...
)

:: Paso 3: Segunda compilación (actualizar referencias)
echo [3/4] Segunda compilacion (actualizando referencias)...
pdflatex -interaction=nonstopmode %ARCHIVO%.tex > nul

:: Paso 4: Tercera compilación (finalizar índices)
echo [4/4] Tercera compilacion (finalizando)...
pdflatex -interaction=nonstopmode %ARCHIVO%.tex > nul

:: Limpiar archivos auxiliares (conserva .log y .bbl para debug)
echo.
echo Limpiando archivos temporales (conservando .log y .bbl)...
del %ARCHIVO%.aux %ARCHIVO%.out %ARCHIVO%.toc %ARCHIVO%.lof %ARCHIVO%.lot %ARCHIVO%.blg %ARCHIVO%.bcf %ARCHIVO%.run.xml 2>nul
del capitulos\*.aux 2>nul
:: NOTA: NO borrar .bbl - es necesario para que las referencias aparezcan en el PDF

:: Renombrar PDF con nombre de proyecto + fecha automática (DDMMAA)
echo.
echo Generando PDF con nombre de proyecto...
:: Obtener fecha actual en formato DDMMAA (PowerShell)
for /f %%i in ('powershell -Command "Get-Date -Format ddMMyy"') do set FECHA=%%i
set PROYECTO=proyecto_tesis_LAMC_%FECHA%.pdf
move %ARCHIVO%.pdf %PROYECTO% > nul
echo PDF generado: %PROYECTO% (fecha: %FECHA%)

echo.
echo ========================================
echo   COMPILACION EXITOSA!
echo ========================================
echo.
echo Tu PDF esta listo: %PROYECTO%
echo.

:: Abrir el PDF automáticamente
start %PROYECTO%

pause


