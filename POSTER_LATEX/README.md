# Poster Académico LaTeX - Sistema de Inferencia Difusa

Este directorio contiene un **poster académico en formato LaTeX** tamaño A0 (841 × 1189 mm), ideal para congresos y presentaciones.

---

## 📂 Archivos

```
POSTER_LATEX/
├── poster_academico.tex    # Documento principal del poster
├── compilar.ps1            # Script de compilación (Windows)
├── compilar.sh             # Script de compilación (Linux/Mac)
└── README.md               # Este archivo
```

**Nota:** El poster hace referencia a las figuras en `../analisis_u/fuzzy/plots/`

---

## 🚀 Compilación Rápida

### Windows PowerShell
```powershell
cd "POSTER_LATEX"
.\compilar.ps1
```

### Linux/Mac Terminal
```bash
cd POSTER_LATEX
chmod +x compilar.sh
./compilar.sh
```

### Manual
```bash
pdflatex poster_academico.tex
```

**Resultado:** `poster_academico.pdf` (tamaño A0, ~10-15 MB)

---

## 📋 Contenido del Poster (3 columnas)

### Columna Izquierda (33%)
1. **Introducción y Objetivos**
   - Contexto clínico
   - Desafío (normalización)
   - Objetivo principal

2. **Datos y Cohorte**
   - Tabla de 10 usuarios
   - Rango de TMB (1,304-2,241 kcal/d)

3. **Variables Derivadas Clave**
   - Actividad_relativa (fórmula)
   - Superávit_calórico_basal (fórmula + TMB)
   - HRV_SDNN
   - Delta_cardiaco

### Columna Central (34%)
4. **Pipeline Metodológico**
   - Diagrama de 5 fases

5. **Clustering K=2**
   - Tabla K-sweep
   - Perfiles de clusters

6. **Funciones de Membresía**
   - 4 figuras PNG (2×2 grid)

7. **Sistema Difuso**
   - 5 reglas Mamdani
   - Defuzzificación y binarización (τ=0.30)

### Columna Derecha (33%)
8. **Métricas de Validación**
   - F1=0.840, Recall=97.6%, Accuracy=74.0%
   - Matriz de confusión (tabla + figura)

9. **Curvas y Distribución**
   - Curva PR + distribución de scores (2 figuras)

10. **Concordancia por Usuario**
    - Tabla de 6 usuarios
    - Heterogeneidad (27.7%-99.3%)

11. **Conclusiones y Próximos Pasos**
    - 5 conclusiones
    - 3 niveles de próximos pasos

12. **Referencias y Contacto**
    - 4 referencias clave
    - Email y repositorio

---

## 🎨 Tema y Colores

- **Tema:** `Autumn` (cálido, profesional)
- **Paleta de colores:** `BrownBlueOrange` (Germany)
- **Tamaño de fuente:** 25pt (legible a distancia)

Para cambiar el tema, edita la línea 16 de `poster_academico.tex`:
```latex
\usetheme{Autumn}
% Opciones: Default, Rays, Basic, Simple, Envelope, Wave, Board, Autumn, Desert
```

Para cambiar la paleta de colores, edita la línea 19:
```latex
\usecolorstyle[colorPalette=BrownBlueOrange]{Germany}
% Opciones: Default, Australia, Britain, Sweden, Spain, Russia, Denmark, Germany
```

---

## 📐 Formato y Tamaño

- **Tamaño:** A0 (841 × 1189 mm)
- **Orientación:** Vertical (portrait)
- **Layout:** 3 columnas (33%-34%-33%)
- **Resolución recomendada para impresión:** 300 dpi

### Cambiar a Tamaño A1

Edita la línea 7:
```latex
\documentclass[25pt, a1paper, portrait]{tikzposter}
```

### Cambiar a Orientación Horizontal

Edita la línea 7:
```latex
\documentclass[25pt, a0paper, landscape]{tikzposter}
```

---

## 🖼️ Figuras Necesarias

El poster requiere **8 figuras PNG** en `../analisis_u/fuzzy/plots/`:

✅ `MF_Actividad_relativa_p50.png`  
✅ `MF_Superavit_calorico_basal_p50.png`  
✅ `MF_HRV_SDNN_p50.png`  
✅ `MF_Delta_cardiaco_p50.png`  
✅ `confusion_matrix.png`  
✅ `pr_curve.png`  
✅ `score_distribution_by_cluster.png`

Opcional:  
⚠️ `logo_universidad.png` (añadir en este directorio para incluir logo)

Si el logo no existe, comenta la línea 30:
```latex
% \titlegraphic{\includegraphics[width=0.08\textwidth]{logo_universidad.png}}
```

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
- `tikzposter` (para el layout del poster)
- `graphicx`, `booktabs`, `amsmath`, `multirow`, `tabularx`

MiKTeX instala paquetes automáticamente la primera vez.

---

## 🔧 Personalización

### Cambiar Título
Edita línea 24:
```latex
\title{Tu Nuevo Título del Poster}
```

### Cambiar Autor e Institución
Edita líneas 26-28:
```latex
\author{Tu Nombre}
\institute{Tu Institución \\ Departamento \\ email@institution.edu}
```

### Ajustar Tamaño de Bloques

Los bloques se crean con:
```latex
\block{Título del Bloque}{
    Contenido...
}
```

Para bloques más altos/bajos, ajusta el contenido o usa `\vspace{Xcm}` para espaciado.

### Cambiar Ancho de Columnas

Edita las líneas `\column{0.33}` (actualmente 33%, 34%, 33%):
```latex
\column{0.25}  % 25%
\column{0.50}  % 50%
\column{0.25}  % 25%
```

---

## 📊 Uso en Congresos

### Impresión

1. **Compilar a PDF:** `pdflatex poster_academico.tex`
2. **Verificar tamaño:** Abrir PDF y comprobar propiedades (841 × 1189 mm)
3. **Enviar a imprenta:** Solicitar impresión en papel mate o glossy, 300 dpi
4. **Montar en foam board** (5-7 mm de grosor) para fácil transporte

### Presentación Digital

Si el congreso permite presentación digital:
- Convertir PDF a imagen PNG de alta resolución
- Usar en pantalla o proyector

### Tips de Diseño

✅ **Usar tamaño de fuente grande** (25pt mínimo para lecibilidad a 2 metros)  
✅ **Colores contrastantes** (fondos claros, texto oscuro)  
✅ **Menos texto, más figuras** (regla 40-60: 40% texto, 60% visual)  
✅ **Jerarquía clara** (títulos grandes, subtítulos medianos, cuerpo pequeño)  
⚠️ **Evitar exceso de información** (prioriza mensajes clave)

---

## ⚠️ Solución de Problemas

### Error: "tikzposter.cls not found"
**Solución:** Instalar `texlive-latex-extra`:
```bash
sudo apt-get install texlive-latex-extra
```

### Error: "Figuras no encontradas"
**Solución:** Verificar que las 8 PNG estén en `../analisis_u/fuzzy/plots/`

### Compilación muy lenta (>5 minutos)
**Causa:** Primera compilación descarga paquetes.  
**Solución:** Esperar; las siguientes serán rápidas.

### Poster se ve pixelado en PDF
**Causa:** Figuras PNG de baja resolución.  
**Solución:** Regenerar figuras con DPI=300 o superior.

---

## 📚 Recursos Adicionales

- **Documentación tikzposter:** https://www.ctan.org/pkg/tikzposter
- **Galería de temas:** https://bitbucket.org/surmann/tikzposter/wiki/Home
- **LaTeX Beamer & Posters:** https://www.overleaf.com/learn/latex/Posters

---

## ✅ Checklist Pre-Impresión

- [ ] Compilar PDF sin errores
- [ ] Verificar tamaño A0 (841 × 1189 mm) en propiedades del PDF
- [ ] Todas las figuras se muestran correctamente
- [ ] Texto legible a 2 metros de distancia (probar imprimiendo A4 y alejándose)
- [ ] Colores apropiados (evitar rojo/verde para daltónicos)
- [ ] Referencias y contacto actualizados
- [ ] Logo de universidad (si aplica)
- [ ] Sin errores de ortografía/redacción

---

## 🎉 ¡Listo para Imprimir!

Tu poster académico está preparado para:
- ✅ Congresos nacionales e internacionales
- ✅ Sesiones de poster en universidades
- ✅ Exposiciones de tesis
- ✅ Ferias de ciencia

**Tiempo estimado de compilación:** 30-60 segundos

---

**Última actualización:** 18 de octubre de 2025  
**Versión del template:** 1.0  
**Autor:** Luis Ángel Martínez





