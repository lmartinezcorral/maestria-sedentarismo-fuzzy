# ============================================================================
# Script de Compilación LaTeX BEAMER (Windows PowerShell)
# ============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  COMPILACIÓN DE PRESENTACIÓN BEAMER A PDF" -ForegroundColor Cyan
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

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO COMPILACIÓN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Compilar presentación
Write-Host "[1/2] Compilando presentación..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode -halt-on-error presentacion_beamer.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló la compilación. Revisa errores en presentacion_beamer.log" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Primera pasada completada" -ForegroundColor Green

# Segunda pasada (para resolver referencias y tabla de contenidos)
Write-Host "[2/2] Segunda pasada..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode -halt-on-error presentacion_beamer.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló la segunda compilación" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Segunda pasada completada" -ForegroundColor Green

# Limpieza de archivos temporales
Write-Host "[3/3] Limpiando archivos temporales..." -ForegroundColor Yellow
Remove-Item -Path "*.aux", "*.log", "*.out", "*.toc", "*.nav", "*.snm" -ErrorAction SilentlyContinue
Write-Host "      [OK] Limpieza completada" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  ✓ COMPILACIÓN EXITOSA" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Archivo generado: presentacion_beamer.pdf (~20 slides, 16:9)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver el PDF, ejecuta:" -ForegroundColor Yellow
Write-Host "  Start-Process presentacion_beamer.pdf" -ForegroundColor White
Write-Host ""
Write-Host "💡 TIPS PARA PRESENTAR:" -ForegroundColor Cyan
Write-Host "   • Ensayar timing (~60 min total)" -ForegroundColor White
Write-Host "   • Llevar backup en USB + email" -ForegroundColor White
Write-Host "   • Probar proyector 15 min antes" -ForegroundColor White
Write-Host ""





