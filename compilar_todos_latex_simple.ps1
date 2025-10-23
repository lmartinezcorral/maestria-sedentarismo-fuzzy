# ============================================================================
# SCRIPT MAESTRO: Compilar TODOS los documentos LaTeX
# Version simplificada (sin caracteres Unicode)
# ============================================================================

$ErrorActionPreference = "Continue"

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  COMPILACION MAESTRA DE TODOS LOS DOCUMENTOS LATEX" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que pdflatex esta instalado
try {
    $null = Get-Command pdflatex -ErrorAction Stop
    Write-Host "[OK] pdflatex encontrado" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] pdflatex no encontrado. Instala MiKTeX o TeX Live." -ForegroundColor Red
    Write-Host "        Descarga: https://miktex.org/download" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Directorio base
$BASE_DIR = Get-Location

# ============================================================================
# DOCUMENTO 1: INFORME ACADEMICO
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host "  [1/3] COMPILANDO DOCUMENTO ACADEMICO (main.tex)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location "INFORME_LATEX"

Write-Host "[1.1] Primera compilacion (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Fallo compilacion de main.tex. Ver main.log" -ForegroundColor Red
    Set-Location $BASE_DIR
    exit 1
}

Write-Host "[1.2] Procesando bibliografia (bibtex)..." -ForegroundColor Cyan
bibtex main 2>$null

Write-Host "[1.3] Segunda compilacion (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error main.tex >$null

Write-Host "[1.4] Tercera compilacion (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error main.tex >$null

Write-Host "[1.5] Limpiando archivos temporales..." -ForegroundColor Cyan
Remove-Item -Path "*.aux", "*.log", "*.bbl", "*.blg", "*.toc", "*.out" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "[OK] DOCUMENTO 1 COMPLETADO: main.pdf" -ForegroundColor Green
Write-Host ""

Set-Location $BASE_DIR

# ============================================================================
# DOCUMENTO 2: PRESENTACION BEAMER
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host "  [2/3] COMPILANDO PRESENTACION BEAMER (presentacion_beamer.tex)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location "BEAMER_LATEX"

Write-Host "[2.1] Primera compilacion (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error presentacion_beamer.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Fallo compilacion de presentacion_beamer.tex" -ForegroundColor Red
    Set-Location $BASE_DIR
    exit 1
}

Write-Host "[2.2] Segunda compilacion (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error presentacion_beamer.tex >$null

Write-Host "[2.3] Limpiando archivos temporales..." -ForegroundColor Cyan
Remove-Item -Path "*.aux", "*.log", "*.out", "*.toc", "*.nav", "*.snm" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "[OK] DOCUMENTO 2 COMPLETADO: presentacion_beamer.pdf" -ForegroundColor Green
Write-Host ""

Set-Location $BASE_DIR

# ============================================================================
# DOCUMENTO 3: POSTER ACADEMICO
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host "  [3/3] COMPILANDO POSTER ACADEMICO (poster_academico.tex)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location "POSTER_LATEX"

Write-Host "[3.1] Primera compilacion (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error poster_academico.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Fallo compilacion de poster_academico.tex" -ForegroundColor Red
    Set-Location $BASE_DIR
    exit 1
}

Write-Host "[3.2] Segunda compilacion (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error poster_academico.tex >$null

Write-Host "[3.3] Limpiando archivos temporales..." -ForegroundColor Cyan
Remove-Item -Path "*.aux", "*.log", "*.out", "*.toc" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "[OK] DOCUMENTO 3 COMPLETADO: poster_academico.pdf" -ForegroundColor Green
Write-Host ""

Set-Location $BASE_DIR

# ============================================================================
# RESUMEN FINAL
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "  COMPILACION MAESTRA COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "ARCHIVOS PDF GENERADOS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   [1] INFORME_LATEX\main.pdf" -ForegroundColor White
Write-Host "       - Documento academico completo (~40-50 paginas)" -ForegroundColor Gray
Write-Host "       - Uso: Manuscrito de tesis, publicacion cientifica" -ForegroundColor Gray
Write-Host ""
Write-Host "   [2] BEAMER_LATEX\presentacion_beamer.pdf" -ForegroundColor White
Write-Host "       - Presentacion academica (20 slides, 16:9)" -ForegroundColor Gray
Write-Host "       - Uso: Defensa de tesis, congresos" -ForegroundColor Gray
Write-Host ""
Write-Host "   [3] POSTER_LATEX\poster_academico.pdf" -ForegroundColor White
Write-Host "       - Poster cientifico (A0, 841x1189 mm)" -ForegroundColor Gray
Write-Host "       - Uso: Sesiones de poster, congresos" -ForegroundColor Gray
Write-Host ""

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  PARA ABRIR LOS PDFs:" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Start-Process 'INFORME_LATEX\main.pdf'" -ForegroundColor Yellow
Write-Host "  Start-Process 'BEAMER_LATEX\presentacion_beamer.pdf'" -ForegroundColor Yellow
Write-Host "  Start-Process 'POSTER_LATEX\poster_academico.pdf'" -ForegroundColor Yellow
Write-Host ""

Write-Host "============================================================================" -ForegroundColor Green
Write-Host "  TODOS LOS DOCUMENTOS LATEX COMPILADOS CON EXITO" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "   - Revisar cada PDF antes de usar" -ForegroundColor White
Write-Host "   - Verificar que todas las figuras se muestran correctamente" -ForegroundColor White
Write-Host "   - Imprimir poster en 300 dpi para congreso" -ForegroundColor White
Write-Host "   - Ensayar presentacion Beamer (timing: ~60 min)" -ForegroundColor White
Write-Host ""





