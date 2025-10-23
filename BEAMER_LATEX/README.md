# Presentación Beamer LaTeX - Sistema de Inferencia Difusa

Este directorio contiene una **presentación académica en Beamer** (el formato LaTeX estándar para presentaciones científicas), con 20+ slides.

---

## 📂 Archivos

```
BEAMER_LATEX/
├── presentacion_beamer.tex    # Documento principal
├── compilar.ps1               # Script de compilación (Windows)
├── compilar.sh                # Script de compilación (Linux/Mac)
└── README.md                  # Este archivo
```

**Nota:** La presentación hace referencia a las figuras en `../analisis_u/fuzzy/plots/`

---

## 🚀 Compilación Rápida

### Windows PowerShell
```powershell
cd "BEAMER_LATEX"
.\compilar.ps1
```

### Linux/Mac Terminal
```bash
cd BEAMER_LATEX
chmod +x compilar.sh
./compilar.sh
```

### Manual
```bash
pdflatex presentacion_beamer.tex
```

**Resultado:** `presentacion_beamer.pdf` (~20-25 slides, ~5-10 MB)

---

## 📋 Contenido de la Presentación (6 secciones)

### 1. Introducción y Objetivos (2 slides)
- Contexto y motivación
- Objetivo principal + 6 específicos

### 2. Datos y Metodología (4 slides)
- Datos y cohorte (tabla de 10 usuarios)
- Variables derivadas clave (1/2): Actividad_relativa, Superávit_calórico
- Variables derivadas clave (2/2): HRV_SDNN, Delta_cardiaco
- Pipeline metodológico (diagrama de 5 fases)

### 3. Clustering No Supervisado (1 slide)
- K-sweep (tabla K=2..6)
- Perfiles de K=2

### 4. Sistema de Inferencia Difusa (5 slides)
- Funciones de membresía: Actividad_relativa (figura)
- Funciones de membresía: Superávit_calórico (figura)
- Funciones de membresía: HRV_SDNN y Delta_cardiaco (2 figuras)
- Sistema difuso (5 reglas Mamdani)

### 5. Resultados y Validación (4 slides)
- Métricas de validación (F1=0.84, Recall=97.6%, matriz de confusión)
- Matriz de confusión visual (figura)
- Curva PR y distribución de scores (2 figuras)
- Concordancia por usuario (tabla + heterogeneidad)

### 6. Conclusiones y Próximos Pasos (2 slides)
- Conclusiones principales (5 puntos)
- Próximos pasos (corto, mediano, largo plazo)

### 7. Slide Final (1 slide)
- Agradecimientos y contacto

---

## 🎨 Tema y Formato

- **Tema:** `Madrid` (clásico, profesional)
- **Paleta de colores:** `whale` (azul profesional)
- **Formato:** 16:9 (widescreen, ideal para proyectores modernos)

### Cambiar Tema

Edita la línea 15:
```latex
\usetheme{Madrid}
% Opciones: Madrid, Berlin, Copenhagen, Darmstadt, Frankfurt, Hannover, Ilmenau, etc.
```

### Cambiar Colores

Edita la línea 16:
```latex
\usecolortheme{whale}
% Opciones: whale, dolphin, rose, orchid, lily, crane, beaver, default
```

### Cambiar Formato (4:3 en lugar de 16:9)

Edita la línea 7:
```latex
\documentclass[aspectratio=43]{beamer}
```

---

## 📐 Navegación y Estructura

### Tabla de Contenidos Automática

La presentación incluye una tabla de contenidos (slide 2) generada automáticamente a partir de las secciones.

### Numeración de Slides

Los slides están numerados automáticamente en el pie de página (esquina inferior derecha).

### Transiciones entre Secciones

Cada sección tiene una portada automática (puedes desactivarla comentando):
```latex
% \AtBeginSection{
%   \begin{frame}{Contenido}
%   \tableofcontents[currentsection]
%   \end{frame}
% }
```

---

## 🖼️ Figuras Necesarias

La presentación requiere **8 figuras PNG** en `../analisis_u/fuzzy/plots/`:

✅ `MF_Actividad_relativa_p50.png`  
✅ `MF_Superavit_calorico_basal_p50.png`  
✅ `MF_HRV_SDNN_p50.png`  
✅ `MF_Delta_cardiaco_p50.png`  
✅ `confusion_matrix.png`  
✅ `pr_curve.png`  
✅ `score_distribution_by_cluster.png`

---

## ⚙️ Requisitos de Software

### Instalación de LaTeX

**Windows:**
- Descargar e instalar [MiKTeX](https://miktex.org/download)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

**macOS:**
```bash
brew install mactex
```

### Paquetes LaTeX Necesarios

El documento usa:
- `beamer` (para presentaciones)
- `graphicx`, `booktabs`, `amsmath`, `tikz`

MiKTeX instala paquetes automáticamente.

---

## 🔧 Personalización

### Cambiar Título

Edita línea 28:
```latex
\title[Título Corto]{Título Largo de la Presentación}
```

### Cambiar Autor e Institución

Edita líneas 32-36:
```latex
\author[Iniciales]{Tu Nombre Completo}
\institute[Abrev.]{
    Tu Departamento\\
    Tu Universidad\\
    \texttt{tu.email@institution.edu}
}
```

### Cambiar Fecha

Edita línea 38:
```latex
\date{Nueva Fecha}
```

### Agregar Logo de Universidad

Agrega después de la línea 38:
```latex
\logo{\includegraphics[height=1cm]{logo_universidad.png}}
```

---

## 💡 Tips para Presentar

### Timing Recomendado (60 minutos)

| Sección | Slides | Tiempo |
|---------|--------|--------|
| Introducción | 2 | 5 min |
| Datos y Metodología | 4 | 12 min |
| Clustering | 1 | 5 min |
| Sistema Difuso | 5 | 15 min |
| Resultados | 4 | 15 min |
| Conclusiones | 2 | 6 min |
| Preguntas | 1 | 2 min |
| **Total** | **19** | **60 min** |

### Modo Presentación

Para navegar:
- **Siguiente slide:** Espacio, Flecha derecha, Enter
- **Slide anterior:** Flecha izquierda, Backspace
- **Ir a slide N:** Escribir número + Enter
- **Pantalla negra:** B
- **Pantalla blanca:** W
- **Salir:** Esc, Q

### Notas del Presentador (Opcional)

Para agregar notas visibles solo en tu pantalla:
```latex
\begin{frame}{Título}
Contenido visible...
\note{Notas solo para ti, no aparecen en proyector}
\end{frame}
```

Compilar con:
```bash
pdflatex -jobname=presentacion_beamer_notes "\def\shownotes{1}\input{presentacion_beamer.tex}"
```

---

## 📊 Exportar a Otros Formatos

### Exportar a PowerPoint

1. Abrir PDF en Acrobat Reader
2. Herramientas → Exportar PDF → Microsoft PowerPoint
3. Guardar como `.pptx`

### Exportar Slides como PNG

```bash
pdftoppm presentacion_beamer.pdf slide -png
```

Genera `slide-01.png`, `slide-02.png`, etc.

### Handouts (Folletos)

Para generar versión con 2/4/6 slides por página:
```latex
\documentclass[handout, aspectratio=169]{beamer}
\usepackage{pgfpages}
\pgfpagesuselayout{4 on 1}[a4paper,border shrink=5mm]
```

---

## ⚠️ Solución de Problemas

### Error: "beamer.cls not found"
**Solución:** Instalar `texlive-latex-recommended`:
```bash
sudo apt-get install texlive-latex-recommended
```

### Error: "Figuras no encontradas"
**Solución:** Verificar que las 8 PNG estén en `../analisis_u/fuzzy/plots/`

### Figuras demasiado grandes/pequeñas
**Solución:** Ajustar el ancho en cada `\includegraphics`:
```latex
\includegraphics[width=0.7\textwidth]{figura.png}  % 70% del ancho
```

### Texto desborda el slide
**Solución:** Reducir tamaño de fuente local:
```latex
{\small Texto más pequeño}
{\footnotesize Texto aún más pequeño}
```

---

## 🎓 Uso en Defensas de Tesis

### Checklist Pre-Defensa

- [ ] Compilar PDF sin errores
- [ ] Todas las figuras se muestran correctamente
- [ ] Texto legible en proyector (probar en sala si es posible)
- [ ] Timing ensayado (no exceder 60 min)
- [ ] Backup en USB + email + nube
- [ ] Versión PDF + versión PPTX (por si falla LaTeX en el proyector)
- [ ] Respuestas preparadas para preguntas anticipadas

### Preguntas Frecuentes Anticipadas

**P1: ¿Por qué K=2 y no K=3?**
- R: K=2 maximiza Silhouette (0.232) y ofrece interpretación clínica clara (Alto/Bajo). K>2 no mejora separabilidad.

**P2: ¿Por qué τ=0.30?**
- R: Búsqueda exhaustiva que maximiza F1 (0.84). Balance óptimo Precision-Recall.

**P3: ¿Cómo manejan los 325 FP?**
- R: Política conservadora para screening. Zona gris (0.40-0.60) requiere confirmación clínica.

**P4: ¿Generaliza a otras cohortes?**
- R: MF por percentiles → fácil recalibración. Estructura de reglas transferible. Validación externa necesaria.

**P5: ¿Por qué baja concordancia en u3/u8?**
- R: Alta variabilidad intra-semanal. Clustering agrupa por promedios; fuzzy captura extremos. Personalización de τ mejora.

---

## 📚 Recursos Adicionales

- **Documentación Beamer:** https://www.ctan.org/pkg/beamer
- **Galería de temas:** https://deic.uab.cat/~iblanes/beamer_gallery/
- **Overleaf Beamer Tutorial:** https://www.overleaf.com/learn/latex/Beamer

---

## ✅ Checklist Pre-Presentación

- [ ] PDF compilado sin errores
- [ ] Total de slides: 19-20
- [ ] Todas las figuras legibles
- [ ] Timing ensayado (≤60 min)
- [ ] Laptop cargada + cargador
- [ ] Adaptador HDMI/VGA para proyector
- [ ] Puntero láser (opcional)
- [ ] Agua para hidratarse durante preguntas
- [ ] Llegar 15 min antes para probar proyector

---

## 🎉 ¡Listo para Presentar!

Tu presentación Beamer está preparada para:
- ✅ Defensas de tesis (maestría/doctorado)
- ✅ Presentaciones en congresos
- ✅ Seminarios académicos
- ✅ Clases/tutoriales

**Tiempo estimado de compilación:** 20-40 segundos

---

**Última actualización:** 18 de octubre de 2025  
**Versión del template:** 1.0  
**Autor:** Luis Ángel Martínez





