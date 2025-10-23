# Guía Rápida de Compilación LaTeX

## ⚡ Compilación Express (3 pasos)

### Windows PowerShell
```powershell
cd "4 semestre_dataset\INFORME_LATEX"
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\compilar.ps1
```

### Linux/Mac Terminal
```bash
cd "4 semestre_dataset/INFORME_LATEX"
chmod +x compilar.sh
./compilar.sh
```

### Overleaf (Sin instalar nada)
1. Ir a https://www.overleaf.com
2. Crear proyecto → Subir `main.tex` y `referencias.bib`
3. Subir las 8 figuras PNG en carpeta `analisis_u/fuzzy/plots/`
4. Click en "Recompile" → Descargar PDF

---

## 📋 Comandos Manuales

Si el script falla, ejecuta manualmente:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 🔍 Verificar Instalación de LaTeX

### Windows
```powershell
pdflatex --version
```
Si falla: Instalar [MiKTeX](https://miktex.org/download)

### Linux (Ubuntu/Debian)
```bash
pdflatex --version
# Si falla:
sudo apt-get update
sudo apt-get install texlive-full
```

### macOS
```bash
pdflatex --version
# Si falla:
brew install mactex
```

---

## 📁 Estructura de Archivos Necesaria

```
4 semestre_dataset/
├── INFORME_LATEX/
│   ├── main.tex                 # ← Documento principal
│   ├── referencias.bib          # ← Bibliografía
│   ├── compilar.ps1             # ← Script Windows
│   ├── compilar.sh              # ← Script Linux/Mac
│   └── (main.pdf)               # ← Se genera aquí
└── analisis_u/
    └── fuzzy/
        └── plots/
            ├── MF_Actividad_relativa_p50.png
            ├── MF_Superavit_calorico_basal_p50.png
            ├── MF_HRV_SDNN_p50.png
            ├── MF_Delta_cardiaco_p50.png
            ├── confusion_matrix.png
            ├── pr_curve.png
            ├── score_distribution_by_cluster.png
            └── sedentarismo_score_histogram.png
```

**IMPORTANTE:** Las 8 figuras PNG deben existir en `../analisis_u/fuzzy/plots/` para que el LaTeX las encuentre.

---

## ⚠️ Errores Comunes y Soluciones

### Error: "pdflatex: command not found"
**Solución:** Instalar MiKTeX (Windows) o TeX Live (Linux/Mac).

### Error: "File 'booktabs.sty' not found"
**Solución (MiKTeX):** Los paquetes se instalan automáticamente la primera vez.  
**Solución (TeX Live):** `sudo apt-get install texlive-latex-extra`

### Error: "Figuras no encontradas"
**Solución:** Verificar que las 8 figuras PNG existan en `../analisis_u/fuzzy/plots/`.

### Compilación lenta (>30 segundos)
**Causa:** Primera compilación descarga paquetes (MiKTeX).  
**Solución:** Esperar; las compilaciones siguientes serán rápidas.

---

## 🎨 Personalización Rápida

### Cambiar Título
Edita en `main.tex` línea ~130:
```latex
\title{
    \textbf{Tu Título Aquí}\\
    ...
}
```

### Cambiar Autor
Edita línea ~137:
```latex
\author{
    Tu Nombre\\
    \small Tu Institución\\
    \small \texttt{tu.email@institution.edu}
}
```

### Cambiar Márgenes
Edita línea ~36:
```latex
\usepackage[left=3cm,right=3cm,top=3cm,bottom=3cm]{geometry}
```

### Quitar Figuras
Comenta las secciones `\begin{figure}...\end{figure}` en `main.tex`.

---

## 📊 Contenido del PDF Final

- **Páginas:** ~40-50 (con figuras y tablas)
- **Secciones:** 10 (Introducción → Conclusiones → Apéndices)
- **Figuras:** 8 (4 MF + 4 evaluación)
- **Tablas:** 6 (cohorte, K-sweep, métricas, confusión, por usuario)
- **Ecuaciones:** 10+ (con numeración automática)
- **Bibliografía:** 7 referencias

---

## 🚀 Flujo de Trabajo Recomendado

1. **Compilar borrador:** `.\compilar.ps1`
2. **Revisar PDF:** Buscar errores, figuras faltantes, referencias "??"
3. **Editar `main.tex`:** Corregir contenido
4. **Recompilar:** `.\compilar.ps1`
5. **Repetir hasta completar**
6. **Entregar `main.pdf`** a tu comité/asesor

---

## 📞 Soporte

- **LaTeX StackExchange:** https://tex.stackexchange.com/
- **Overleaf Tutorials:** https://www.overleaf.com/learn
- **Manual de LaTeX (español):** https://es.wikibooks.org/wiki/Manual_de_LaTeX

---

**Tiempo estimado de compilación:** 30-90 segundos (primera vez), 10-20 segundos (siguientes).

**Última actualización:** 18 de octubre de 2025




