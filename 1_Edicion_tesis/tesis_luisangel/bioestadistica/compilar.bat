@echo off
REM ============================================================================
REM Script de Compilación - Documento Bioestadística
REM Universidad Autónoma de Chihuahua (UACH)
REM Facultad de Medicina y Ciencias Biomédicas
REM ============================================================================

echo.
echo ========================================
echo COMPILACION - DOCUMENTO BIOESTADISTICA
echo ========================================
echo.

REM Obtener fecha actual en formato DDMMYY
for /f "tokens=1-3 delims=/" %%a in ('date /t') do (
    set fecha=%%a%%b%%c
)

REM Nombre del archivo de salida con fecha
set OUTPUT=bioestadistica_LAMC_%fecha:~0,2%%fecha:~3,2%%fecha:~6,2%.pdf

echo Generando: %OUTPUT%
echo.

REM ============================================================================
REM PASADA 1: Compilación inicial
REM ============================================================================
echo [1/4] Primera pasada de pdflatex...
pdflatex -interaction=nonstopmode main.tex > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo en primera pasada
    echo Revisa el archivo main.log para detalles
    pause
    exit /b 1
)

REM ============================================================================
REM PASADA 2: Procesamiento de bibliografía
REM ============================================================================
echo [2/4] Procesando bibliografia con biber...
biber main > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ADVERTENCIA: Biber reporto errores (puede ser normal si no hay citas)
)

REM ============================================================================
REM PASADA 3: Actualización de referencias
REM ============================================================================
echo [3/4] Segunda pasada de pdflatex...
pdflatex -interaction=nonstopmode main.tex > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo en segunda pasada
    pause
    exit /b 1
)

REM ============================================================================
REM PASADA 4: Compilación final
REM ============================================================================
echo [4/4] Tercera pasada de pdflatex (final)...
pdflatex -interaction=nonstopmode main.tex > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo en pasada final
    pause
    exit /b 1
)

REM ============================================================================
REM RENOMBRAR PDF CON FECHA
REM ============================================================================
if exist main.pdf (
    echo.
    echo Renombrando main.pdf a %OUTPUT%...
    move /Y main.pdf %OUTPUT% > nul
    echo.
    echo ========================================
    echo COMPILACION EXITOSA
    echo ========================================
    echo.
    echo Archivo generado: %OUTPUT%
    echo.
) else (
    echo ERROR: No se genero main.pdf
    echo Revisa main.log para detalles
    pause
    exit /b 1
)

REM ============================================================================
REM LIMPIEZA DE ARCHIVOS TEMPORALES
REM ============================================================================
echo Limpiando archivos temporales...
del /Q main.aux main.log main.out main.toc main.lof main.lot main.bbl main.bcf main.blg main.run.xml 2>nul

echo.
echo Compilacion completa. Archivo listo para revision.
echo.
pause

