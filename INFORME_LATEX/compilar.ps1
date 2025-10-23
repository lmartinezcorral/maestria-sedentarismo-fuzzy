# ============================================================================
# Script de Compilación LaTeX para Windows PowerShell
# ============================================================================
# 
# Este script compila el documento LaTeX en PDF con bibliografía
# 
# USO:
#   .\compilar.ps1
#
# REQUISITOS:
#   - MiKTeX o TeX Live instalado
#   - pdflatex y bibtex en el PATH
#
# ============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  COMPILACIÓN DE DOCUMENTO LATEX A PDF" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que pdflatex está instalado
try {
    $null = Get-Command pdflatex -ErrorAction Stop
    Write-Host "[OK] pdflatex encontrado" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] pdflatex no encontrado. Instala MiKTeX o TeX Live." -ForegroundColor Red
    Write-Host "        Descarga: https://miktex.org/download" -ForegroundColor Yellow
    exit 1
}

# Verificar que bibtex está instalado
try {
    $null = Get-Command bibtex -ErrorAction Stop
    Write-Host "[OK] bibtex encontrado" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] bibtex no encontrado." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO COMPILACIÓN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Primera compilación de pdflatex (genera .aux)
Write-Host "[1/5] Primera pasada: pdflatex..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló la primera compilación. Revisa errores en main.log" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Primera pasada completada" -ForegroundColor Green

# Paso 2: Compilar bibliografía con bibtex
Write-Host "[2/5] Generando bibliografía: bibtex..." -ForegroundColor Yellow
bibtex main
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ADVERTENCIA] bibtex reportó errores (puede ser normal si no hay citas)" -ForegroundColor Yellow
}
Write-Host "      [OK] Bibliografía procesada" -ForegroundColor Green

# Paso 3: Segunda compilación de pdflatex (integra bibliografía)
Write-Host "[3/5] Segunda pasada: pdflatex..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló la segunda compilación" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Segunda pasada completada" -ForegroundColor Green

# Paso 4: Tercera compilación de pdflatex (resuelve referencias cruzadas)
Write-Host "[4/5] Tercera pasada: pdflatex..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló la tercera compilación" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Tercera pasada completada" -ForegroundColor Green

# Paso 5: Limpieza de archivos temporales (opcional)
Write-Host "[5/5] Limpiando archivos temporales..." -ForegroundColor Yellow
Remove-Item -Path "*.aux", "*.log", "*.bbl", "*.blg", "*.toc", "*.out" -ErrorAction SilentlyContinue
Write-Host "      [OK] Limpieza completada" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  ✓ COMPILACIÓN EXITOSA" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Archivo generado: main.pdf" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver el PDF, ejecuta:" -ForegroundColor Yellow
Write-Host "  Start-Process main.pdf" -ForegroundColor White
Write-Host ""



