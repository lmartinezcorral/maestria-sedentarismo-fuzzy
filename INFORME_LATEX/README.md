# Informe LaTeX: Sistema de Inferencia Difusa para Evaluación de Sedentarismo

Este directorio contiene el documento LaTeX completo del proyecto de tesis, listo para compilar a PDF en formato académico.

---

## 📂 Archivos del Proyecto

```
INFORME_LATEX/
├── main.tex              # Documento principal LaTeX
├── referencias.bib       # Bibliografía en formato BibTeX
├── compilar.ps1          # Script de compilación (Windows PowerShell)
├── README.md             # Este archivo (instrucciones)
└── (main.pdf)            # PDF generado tras compilación
```

**Nota:** El documento hace referencia a las figuras en:
```
../analisis_u/fuzzy/plots/
├── MF_Actividad_relativa_p50.png
├── MF_Superavit_calorico_basal_p50.png
├── MF_HRV_SDNN_p50.png
├── MF_Delta_cardiaco_p50.png
├── confusion_matrix.png
├── pr_curve.png
├── score_distribution_by_cluster.png
└── sedentarismo_score_histogram.png
```

---

## 🚀 OPCIÓN 1: Compilación Automática con Script (Recomendada)

### Windows (PowerShell)

1. **Abrir PowerShell en el directorio `INFORME_LATEX`:**
   ```powershell
   cd "4 semestre_dataset\INFORME_LATEX"
   ```

2. **Permitir ejecución de scripts (solo la primera vez):**
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

3. **Ejecutar script de compilación:**
   ```powershell
   .\compilar.ps1
   ```

4. **El PDF `main.pdf` se generará automáticamente.**

**El script realiza automáticamente:**
- Compilación 1: `pdflatex main.tex` (genera archivos auxiliares)
- Compilación 2: `bibtex main` (procesa bibliografía)
- Compilación 3: `pdflatex main.tex` (integra bibliografía)
- Compilación 4: `pdflatex main.tex` (resuelve referencias cruzadas)
- Limpieza de archivos temporales (.aux, .log, .bbl, .blg, .toc, .out)

---

## 🔧 OPCIÓN 2: Compilación Manual

Si prefieres compilar manualmente o estás en Linux/Mac:

### 1. Instalar LaTeX (si no lo tienes)

**Windows:**
- Descarga e instala [MiKTeX](https://miktex.org/download)
- O [TeX Live](https://tug.org/texlive/)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

**macOS:**
```bash
brew install mactex
```

### 2. Compilar con comandos

```bash
# Primera pasada: genera archivos auxiliares
pdflatex main.tex

# Procesar bibliografía
bibtex main

# Segunda pasada: integra bibliografía
pdflatex main.tex

# Tercera pasada: resuelve referencias cruzadas
pdflatex main.tex
```

**Resultado:** Se genera `main.pdf` en el mismo directorio.

---

## 📖 OPCIÓN 3: Usar Overleaf (Online, sin instalar nada)

1. **Crear cuenta en [Overleaf](https://www.overleaf.com)** (gratis).

2. **Crear nuevo proyecto:**
   - Click en "New Project" → "Blank Project"
   - Nombrar: "Sistema_Difuso_Sedentarismo"

3. **Subir archivos:**
   - Subir `main.tex` (arrastra y suelta en la columna izquierda)
   - Subir `referencias.bib`
   - Crear carpeta `analisis_u/fuzzy/plots/` y subir las 8 figuras PNG

4. **Compilar:**
   - Click en el botón verde "Recompile"
   - El PDF se generará automáticamente en el panel derecho

5. **Descargar:**
   - Click en "Download PDF" para guardar localmente

**Ventajas de Overleaf:**
- No requiere instalación local
- Compilación automática
- Control de versiones integrado
- Colaboración en tiempo real

---

## 📄 Contenido del Documento

El documento LaTeX incluye:

### Secciones Principales
1. **Resumen / Abstract** — Objetivos, métodos, resultados, conclusiones
2. **Introducción** — Contexto, justificación de variables (Actividad_relativa, Superávit_calórico_basal, HRV, Delta_cardiaco)
3. **Datos y Cohorte** — Tabla con 10 usuarios, características antropométricas, TMB
4. **Pipeline Metodológico** — 5 fases (preprocesamiento, variables derivadas, agregación semanal, clustering, fuzzy)
5. **Resultados** — Métricas globales (F1=0.84, Recall=97.6%), matriz de confusión, análisis por usuario
6. **Discusión** — Validez clínica, heterogeneidad inter-sujeto, comparación con clustering
7. **Fortalezas y Limitaciones** — Trade-offs metodológicos, FP, cohorte pequeña
8. **Conclusiones** — 5 puntos clave
9. **Próximos Pasos** — Corto, mediano y largo plazo
10. **Apéndices** — Pseudocódigo del sistema fuzzy, reproducibilidad

### Figuras (8 PNG, 300 dpi)
- 4 figuras de funciones de membresía (MF)
- Matriz de confusión
- Curva Precision-Recall
- Distribución de scores por cluster
- Histograma del score fuzzy

### Tablas
- Características de la cohorte (N=10)
- K-sweep para clustering (K=2..6)
- Métricas de validación globales
- Matriz de confusión (TN, FP, FN, TP)
- Concordancia por usuario

### Ecuaciones
- Actividad_relativa
- TMB (Mifflin-St Jeor, por sexo)
- Superávit_calórico_basal
- Delta_cardiaco
- Funciones de membresía triangulares

---

## ⚠️ Solución de Problemas

### Error: "pdflatex: command not found"
**Causa:** LaTeX no está instalado o no está en el PATH.
**Solución:** Instala MiKTeX/TeX Live (ver sección "Instalar LaTeX").

### Error: "File 'XYZ.sty' not found"
**Causa:** Faltan paquetes LaTeX.
**Solución (MiKTeX):** Los paquetes se instalan automáticamente la primera vez.
**Solución (TeX Live):** Reinstala con `texlive-full` o instala paquetes específicos con `tlmgr`.

### Error: "Figuras no encontradas"
**Causa:** Las rutas relativas a las figuras están incorrectas.
**Solución:**
1. Asegúrate de que las 8 figuras PNG estén en:
   ```
   4 semestre_dataset/analisis_u/fuzzy/plots/
   ```
2. Si compilas desde Overleaf, crea la misma estructura de carpetas y sube las figuras.

### Error: "Undefined control sequence"
**Causa:** Comandos personalizados o paquetes no cargados.
**Solución:** Revisa que todos los paquetes estén en el preámbulo de `main.tex`.

### Error en bibtex: "I couldn't open file name 'referencias.bib'"
**Causa:** El archivo `referencias.bib` no está en el mismo directorio que `main.tex`.
**Solución:** Copia `referencias.bib` al directorio `INFORME_LATEX/`.

---

## 📝 Personalización del Documento

### Cambiar Autor, Institución o Fecha

Edita las líneas en `main.tex`:

```latex
\author{
    Tu Nombre\\
    \small Tu Institución\\
    \small \texttt{tu.email@institution.edu}
}

\date{Fecha actual}
```

### Ajustar Márgenes

En el preámbulo, modifica:

```latex
\usepackage[left=3cm,right=3cm,top=3cm,bottom=3cm]{geometry}
```

### Cambiar Interlineado

```latex
\onehalfspacing   % Interlineado 1.5
% \doublespacing  % Interlineado 2.0
% \singlespacing  % Interlineado simple
```

### Agregar/Quitar Figuras

Busca las secciones `\begin{figure}...\end{figure}` y comenta/descomenta según necesites:

```latex
% \begin{figure}[h]
% \centering
% \includegraphics[width=0.8\textwidth]{ruta/figura.png}
% \caption{Descripción}
% \label{fig:etiqueta}
% \end{figure}
```

### Agregar Referencias Bibliográficas

Edita `referencias.bib` y agrega entradas en formato BibTeX:

```bibtex
@article{Apellido2025,
  title={Título del artículo},
  author={Apellido, Nombre and Otro, Autor},
  journal={Nombre de la revista},
  volume={10},
  number={1},
  pages={1--10},
  year={2025},
  doi={10.xxxx/xxxx}
}
```

Luego cita en el texto con `\citep{Apellido2025}` o `\citet{Apellido2025}`.

---

## 📊 Formato del Documento

- **Tipo de documento:** `article` (12pt, a4paper, twoside)
- **Idioma:** Español (con babel)
- **Fuente:** Latin Modern (lmodern)
- **Interlineado:** 1.5 (`\onehalfspacing`)
- **Márgenes:** 2.5 cm en todos los lados
- **Bibliografía:** Estilo `plain` con numeración
- **Algoritmos:** En español (configurados con `algpseudocode`)

---

## ✅ Checklist de Compilación Exitosa

Después de compilar, verifica que `main.pdf` contiene:

- [ ] Página de título con autor, fecha, título
- [ ] Resumen (Abstract) en la primera página
- [ ] Tabla de contenidos (Table of Contents)
- [ ] 10 secciones principales
- [ ] 8 figuras insertadas correctamente
- [ ] 6 tablas con datos de la cohorte, métricas, etc.
- [ ] Ecuaciones numeradas y formateadas
- [ ] Bibliografía al final (referencias citadas en el texto)
- [ ] Apéndices con pseudocódigo y reproducibilidad
- [ ] Sin errores de referencias cruzadas (no aparece "??")

---

## 🎓 Recomendaciones para Tesis

### Antes de Entregar

1. **Revisar ortografía y redacción** (herramientas: LanguageTool, Grammarly para español)
2. **Verificar todas las figuras** (resolución 300 dpi, legibles al imprimir)
3. **Comprobar referencias cruzadas** (Figura~X, Tabla~Y, Ecuación~Z)
4. **Revisar bibliografía** (formato consistente, DOIs válidos)
5. **Imprimir borrador** (revisar paginación, márgenes)

### Formato para Comité

Si tu institución requiere formato específico (IEEE, APA, etc.), consulta:
- [Overleaf Templates](https://www.overleaf.com/latex/templates)
- [LaTeX Templates for Thesis](http://www.latextemplates.com/cat/theses)

---

## 🆘 Soporte

Si tienes problemas:

1. **Revisa los logs:** `main.log` contiene detalles del error
2. **Busca el error específico:** Copia el mensaje de error y busca en [TeX StackExchange](https://tex.stackexchange.com/)
3. **Simplifica:** Comenta secciones del documento para identificar dónde falla
4. **Usa Overleaf:** Si la compilación local falla, prueba en Overleaf (detecta y soluciona errores automáticamente)

---

## 📚 Recursos Adicionales

- [Documentación LaTeX (español)](https://www.latex-project.org/help/documentation/)
- [Beamer para presentaciones](https://www.overleaf.com/learn/latex/Beamer)
- [TikZ para diagramas](https://www.overleaf.com/learn/latex/TikZ_package)
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)

---

## 🎉 ¡Todo Listo!

Tu documento LaTeX está preparado para compilar. Sigue las instrucciones de la **Opción 1** (script automático) para obtener el PDF en menos de 1 minuto.

**¡Mucho éxito con tu tesis!** 🚀

---

**Última actualización:** 18 de octubre de 2025  
**Versión del documento:** 1.0  
**Autor del template:** Luis Ángel Martínez



