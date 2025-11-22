@echo off
REM ============================================================================
REM Script de Compilación para Artículo IEEE JBHI
REM Proyecto: Sistema de Inferencia Difusa para Clasificación de CS
REM ============================================================================
REM Creado por: Ades - adaptado de compilar.bat de Rayo Veloz
REM Fecha: 10 de noviembre de 2025
REM ============================================================================

echo ============================================================
echo    COMPILACION ARTICULO IEEE - main_esp.tex
echo ============================================================
echo.

REM Definir archivo principal
set PROYECTO=main_esp

echo [1/5] Compilacion inicial LaTeX...
pdflatex -interaction=nonstopmode %PROYECTO%.tex
if errorlevel 1 (
    echo ERROR: Fallo en primera compilacion LaTeX
    pause
    exit /b 1
)

echo.
echo [2/5] Procesando bibliografia con BibTeX...
bibtex %PROYECTO%
if errorlevel 1 (
    echo ADVERTENCIA: BibTeX reporto errores (puede ser normal)
)

echo.
echo [3/5] Segunda compilacion LaTeX (integrando bibliografia)...
pdflatex -interaction=nonstopmode %PROYECTO%.tex
if errorlevel 1 (
    echo ERROR: Fallo en segunda compilacion LaTeX
    pause
    exit /b 1
)

echo.
echo [4/5] Tercera compilacion LaTeX (referencias cruzadas)...
pdflatex -interaction=nonstopmode %PROYECTO%.tex
if errorlevel 1 (
    echo ERROR: Fallo en tercera compilacion LaTeX
    pause
    exit /b 1
)

echo.
echo [5/5] Limpiando archivos auxiliares...
REM IMPORTANTE: NO borrar .bbl (bibliografia procesada)
del %PROYECTO%.aux 2>nul
del %PROYECTO%.log 2>nul
del %PROYECTO%.out 2>nul
del %PROYECTO%.toc 2>nul
del %PROYECTO%.blg 2>nul
REM .bbl se PRESERVA (contiene bibliografia formateada)

echo.
echo ============================================================
echo    COMPILACION COMPLETADA EXITOSAMENTE
echo    PDF generado: %PROYECTO%.pdf
echo ============================================================
echo.

REM Abrir PDF automáticamente
echo Abriendo PDF...
start %PROYECTO%.pdf

echo.
echo Presione cualquier tecla para cerrar...
pause >nul

