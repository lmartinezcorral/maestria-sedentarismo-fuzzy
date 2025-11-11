@echo off
REM Script para compilar el informe técnico LaTeX a PDF
REM Requiere: MiKTeX o TeX Live instalado

echo ============================================
echo Compilando INFORME_TECNICO_PIPELINE_COMPLETO.tex
echo ============================================

REM Primera compilación (genera .aux, .toc)
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO.tex

REM Segunda compilación (resuelve referencias)
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO.tex

REM Tercera compilación (bibliografía y TOC final)
pdflatex -interaction=nonstopmode INFORME_TECNICO_PIPELINE_COMPLETO.tex

echo.
echo ============================================
echo Compilación completada!
echo Archivo generado: INFORME_TECNICO_PIPELINE_COMPLETO.pdf
echo ============================================

REM Limpiar archivos auxiliares
del *.aux *.log *.out *.toc *.lot *.lof 2>nul

pause

