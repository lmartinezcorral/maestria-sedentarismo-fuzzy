@echo off
REM ============================================================================
REM Compilation Script for IEEE JBHI Article (ENGLISH VERSION)
REM Project: Fuzzy Inference System for Sedentary Behavior Classification
REM ============================================================================
REM Created by: Ades - adapted from compilar.bat by Rayo Veloz
REM Date: November 10, 2025
REM ============================================================================

echo ============================================================
echo    IEEE ARTICLE COMPILATION - main.tex (ENGLISH)
echo ============================================================
echo.

REM Define main file
set PROYECTO=main

echo [1/5] Initial LaTeX compilation...
pdflatex -interaction=nonstopmode %PROYECTO%.tex
if errorlevel 1 (
    echo ERROR: First LaTeX compilation failed
    pause
    exit /b 1
)

echo.
echo [2/5] Processing bibliography with BibTeX...
bibtex %PROYECTO%
if errorlevel 1 (
    echo WARNING: BibTeX reported errors (may be normal)
)

echo.
echo [3/5] Second LaTeX compilation (integrating bibliography)...
pdflatex -interaction=nonstopmode %PROYECTO%.tex
if errorlevel 1 (
    echo ERROR: Second LaTeX compilation failed
    pause
    exit /b 1
)

echo.
echo [4/5] Third LaTeX compilation (cross-references)...
pdflatex -interaction=nonstopmode %PROYECTO%.tex
if errorlevel 1 (
    echo ERROR: Third LaTeX compilation failed
    pause
    exit /b 1
)

echo.
echo [5/5] Cleaning auxiliary files...
REM IMPORTANT: DO NOT delete .bbl (processed bibliography)
del %PROYECTO%.aux 2>nul
del %PROYECTO%.log 2>nul
del %PROYECTO%.out 2>nul
del %PROYECTO%.toc 2>nul
del %PROYECTO%.blg 2>nul
REM .bbl is PRESERVED (contains formatted bibliography)

echo.
echo ============================================================
echo    COMPILATION SUCCESSFULLY COMPLETED
echo    PDF generated: %PROYECTO%.pdf
echo ============================================================
echo.

REM Open PDF automatically
echo Opening PDF...
start %PROYECTO%.pdf

echo.
echo Press any key to close...
pause >nul

