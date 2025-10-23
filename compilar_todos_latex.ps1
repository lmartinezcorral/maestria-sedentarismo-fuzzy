# ============================================================================
# SCRIPT MAESTRO: Compilar TODOS los documentos LaTeX
# ============================================================================
# 
# Este script compila en orden:
# 1. Documento académico (main.tex) → ~40-50 páginas
# 2. Presentación Beamer (presentacion_beamer.tex) → 20 slides
# 3. Poster académico (poster_academico.tex) → A0
#
# ============================================================================

$ErrorActionPreference = "Continue"

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  COMPILACIÓN MAESTRA DE TODOS LOS DOCUMENTOS LATEX" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que pdflatex está instalado
try {
    $null = Get-Command pdflatex -ErrorAction Stop
    Write-Host "[OK] pdflatex encontrado" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] pdflatex no encontrado. Instala MiKTeX o TeX Live." -ForegroundColor Red
    Write-Host "        Descarga: https://miktex.org/download" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Directorio base
$BASE_DIR = Get-Location

# ============================================================================
# DOCUMENTO 1: INFORME ACADÉMICO
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host "  [1/3] COMPILANDO DOCUMENTO ACADÉMICO (main.tex)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location "INFORME_LATEX"

Write-Host "[1.1] Primera compilación (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló compilación de main.tex. Ver main.log" -ForegroundColor Red
    Set-Location $BASE_DIR
    exit 1
}

Write-Host "[1.2] Procesando bibliografía (bibtex)..." -ForegroundColor Cyan
bibtex main 2>$null

Write-Host "[1.3] Segunda compilación (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error main.tex >$null

Write-Host "[1.4] Tercera compilación (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error main.tex >$null

Write-Host "[1.5] Limpiando archivos temporales..." -ForegroundColor Cyan
Remove-Item -Path "*.aux", "*.log", "*.bbl", "*.blg", "*.toc", "*.out" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "[OK] DOCUMENTO 1 COMPLETADO: main.pdf (~40-50 paginas)" -ForegroundColor Green
Write-Host ""

Set-Location $BASE_DIR

# ============================================================================
# DOCUMENTO 2: PRESENTACIÓN BEAMER
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host "  [2/3] COMPILANDO PRESENTACIÓN BEAMER (presentacion_beamer.tex)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location "BEAMER_LATEX"

Write-Host "[2.1] Primera compilación (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error presentacion_beamer.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló compilación de presentacion_beamer.tex. Ver presentacion_beamer.log" -ForegroundColor Red
    Set-Location $BASE_DIR
    exit 1
}

Write-Host "[2.2] Segunda compilación (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error presentacion_beamer.tex >$null

Write-Host "[2.3] Limpiando archivos temporales..." -ForegroundColor Cyan
Remove-Item -Path "*.aux", "*.log", "*.out", "*.toc", "*.nav", "*.snm" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "✅ DOCUMENTO 2 COMPLETADO: presentacion_beamer.pdf (20 slides, 16:9)" -ForegroundColor Green
Write-Host ""

Set-Location $BASE_DIR

# ============================================================================
# DOCUMENTO 3: POSTER ACADÉMICO
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host "  [3/3] COMPILANDO POSTER ACADÉMICO (poster_academico.tex)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location "POSTER_LATEX"

Write-Host "[3.1] Primera compilación (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error poster_academico.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló compilación de poster_academico.tex. Ver poster_academico.log" -ForegroundColor Red
    Set-Location $BASE_DIR
    exit 1
}

Write-Host "[3.2] Segunda compilación (pdflatex)..." -ForegroundColor Cyan
pdflatex -interaction=nonstopmode -halt-on-error poster_academico.tex >$null

Write-Host "[3.3] Limpiando archivos temporales..." -ForegroundColor Cyan
Remove-Item -Path "*.aux", "*.log", "*.out", "*.toc" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "✅ DOCUMENTO 3 COMPLETADO: poster_academico.pdf (A0, 841×1189 mm)" -ForegroundColor Green
Write-Host ""

Set-Location $BASE_DIR

# ============================================================================
# RESUMEN FINAL
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "  ✅✅✅ COMPILACIÓN MAESTRA COMPLETADA EXITOSAMENTE ✅✅✅" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "📁 ARCHIVOS PDF GENERADOS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   [1] INFORME_LATEX\main.pdf" -ForegroundColor White
Write-Host "       → Documento académico completo (~40-50 páginas)" -ForegroundColor Gray
Write-Host "       → Uso: Manuscrito de tesis, publicación científica" -ForegroundColor Gray
Write-Host ""
Write-Host "   [2] BEAMER_LATEX\presentacion_beamer.pdf" -ForegroundColor White
Write-Host "       → Presentación académica (20 slides, 16:9)" -ForegroundColor Gray
Write-Host "       → Uso: Defensa de tesis, congresos" -ForegroundColor Gray
Write-Host ""
Write-Host "   [3] POSTER_LATEX\poster_academico.pdf" -ForegroundColor White
Write-Host "       → Poster científico (A0, 841×1189 mm)" -ForegroundColor Gray
Write-Host "       → Uso: Sesiones de poster, congresos" -ForegroundColor Gray
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
Write-Host "  🎉 ¡TODOS LOS DOCUMENTOS LATEX COMPILADOS CON ÉXITO!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "💡 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "   • Revisar cada PDF antes de usar" -ForegroundColor White
Write-Host "   • Verificar que todas las figuras se muestran correctamente" -ForegroundColor White
Write-Host "   • Imprimir poster en 300 dpi para congreso" -ForegroundColor White
Write-Host "   • Ensayar presentación Beamer (timing: ~60 min)" -ForegroundColor White
Write-Host ""

