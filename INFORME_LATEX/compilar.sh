#!/bin/bash
# ============================================================================
# Script de Compilación LaTeX para Linux/Mac
# ============================================================================
# 
# Este script compila el documento LaTeX en PDF con bibliografía
# 
# USO:
#   chmod +x compilar.sh
#   ./compilar.sh
#
# REQUISITOS:
#   - TeX Live instalado
#   - pdflatex y bibtex en el PATH
#
# ============================================================================

echo "============================================================"
echo "  COMPILACIÓN DE DOCUMENTO LATEX A PDF"
echo "============================================================"
echo ""

# Verificar que pdflatex está instalado
if ! command -v pdflatex &> /dev/null; then
    echo "[ERROR] pdflatex no encontrado. Instala TeX Live."
    echo "        Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "        macOS: brew install mactex"
    exit 1
fi
echo "[OK] pdflatex encontrado"

# Verificar que bibtex está instalado
if ! command -v bibtex &> /dev/null; then
    echo "[ERROR] bibtex no encontrado."
    exit 1
fi
echo "[OK] bibtex encontrado"

echo ""
echo "============================================================"
echo "  INICIANDO COMPILACIÓN"
echo "============================================================"
echo ""

# Paso 1: Primera compilación de pdflatex (genera .aux)
echo "[1/5] Primera pasada: pdflatex..."
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if [ $? -ne 0 ]; then
    echo "[ERROR] Falló la primera compilación. Revisa errores en main.log"
    exit 1
fi
echo "      [OK] Primera pasada completada"

# Paso 2: Compilar bibliografía con bibtex
echo "[2/5] Generando bibliografía: bibtex..."
bibtex main
if [ $? -ne 0 ]; then
    echo "[ADVERTENCIA] bibtex reportó errores (puede ser normal si no hay citas)"
fi
echo "      [OK] Bibliografía procesada"

# Paso 3: Segunda compilación de pdflatex (integra bibliografía)
echo "[3/5] Segunda pasada: pdflatex..."
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if [ $? -ne 0 ]; then
    echo "[ERROR] Falló la segunda compilación"
    exit 1
fi
echo "      [OK] Segunda pasada completada"

# Paso 4: Tercera compilación de pdflatex (resuelve referencias cruzadas)
echo "[4/5] Tercera pasada: pdflatex..."
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if [ $? -ne 0 ]; then
    echo "[ERROR] Falló la tercera compilación"
    exit 1
fi
echo "      [OK] Tercera pasada completada"

# Paso 5: Limpieza de archivos temporales (opcional)
echo "[5/5] Limpiando archivos temporales..."
rm -f *.aux *.log *.bbl *.blg *.toc *.out
echo "      [OK] Limpieza completada"

echo ""
echo "============================================================"
echo "  ✓ COMPILACIÓN EXITOSA"
echo "============================================================"
echo ""
echo "Archivo generado: main.pdf"
echo ""
echo "Para ver el PDF, ejecuta:"
echo "  open main.pdf        (macOS)"
echo "  xdg-open main.pdf    (Linux)"
echo ""



