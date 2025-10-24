@echo off
echo ============================================
echo COMPILANDO INFORME LATEX FINAL V2
echo ============================================
echo.

cd "C:\Users\hulkmtz\Documents\luis angel\Maestria\Asesoria\Semestre 3\Convocatoria\Datos\4 semestre_dataset\documentos_tesis"

echo [1/4] Primera pasada de pdflatex...
pdflatex -interaction=nonstopmode INFORME_TECNICO_FINAL_V2.tex > NUL 2>&1

echo [2/4] Segunda pasada (referencias cruzadas)...
pdflatex -interaction=nonstopmode INFORME_TECNICO_FINAL_V2.tex > NUL 2>&1

echo [3/4] Tercera pasada (tabla de contenidos)...
pdflatex -interaction=nonstopmode INFORME_TECNICO_FINAL_V2.tex > NUL 2>&1

echo [4/4] Limpiando archivos auxiliares...
del INFORME_TECNICO_FINAL_V2.aux INFORME_TECNICO_FINAL_V2.log INFORME_TECNICO_FINAL_V2.out INFORME_TECNICO_FINAL_V2.toc 2>NUL

echo.
echo ============================================
echo COMPILACION COMPLETADA
echo ============================================
echo PDF generado: INFORME_TECNICO_FINAL_V2.pdf
echo.
pause
