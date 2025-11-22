# ============================================================================
# Script de Compilación LaTeX POSTER (Windows PowerShell)
# ============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  COMPILACIÓN DE POSTER ACADÉMICO A PDF" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
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
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO COMPILACIÓN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Compilar poster
Write-Host "[1/2] Compilando poster..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode -halt-on-error poster_academico.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló la compilación. Revisa errores en poster_academico.log" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Primera pasada completada" -ForegroundColor Green

# Segunda pasada (para resolver referencias)
Write-Host "[2/2] Segunda pasada..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode -halt-on-error poster_academico.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Falló la segunda compilación" -ForegroundColor Red
    exit 1
}
Write-Host "      [OK] Segunda pasada completada" -ForegroundColor Green

# Limpieza de archivos temporales
Write-Host "[3/3] Limpiando archivos temporales..." -ForegroundColor Yellow
Remove-Item -Path "*.aux", "*.log", "*.out", "*.toc" -ErrorAction SilentlyContinue
Write-Host "      [OK] Limpieza completada" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  ✓ COMPILACIÓN EXITOSA" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Archivo generado: poster_academico.pdf (A0, 841×1189 mm)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver el PDF, ejecuta:" -ForegroundColor Yellow
Write-Host "  Start-Process poster_academico.pdf" -ForegroundColor White
Write-Host ""
Write-Host "💡 RECOMENDACIONES PARA IMPRESIÓN:" -ForegroundColor Cyan
Write-Host "   • Imprimir en papel mate o glossy" -ForegroundColor White
Write-Host "   • Resolución 300 dpi" -ForegroundColor White
Write-Host "   • Montar en foam board (5-7 mm)" -ForegroundColor White
Write-Host ""





