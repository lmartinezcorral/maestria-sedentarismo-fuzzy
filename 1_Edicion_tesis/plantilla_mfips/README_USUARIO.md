# 📖 MANUAL DE USUARIO: Plantilla de Tesis LaTeX

**Versión:** 1.2 (Formato Perfeccionado)  
**Fecha:** Noviembre 2025  
**Autor:** Luis Ángel Martínez Corral  
**Facultad:** Medicina y Ciencias Biomédicas - UACH  
**Programa:** Maestría en Formación e Innovación para Profesionales de la Salud (MFIPS)

---

## 🎯 ¿Para Quién es Esta Plantilla?

Esta plantilla está diseñada para estudiantes de la **Maestría en Formación e Innovación para Profesionales de la Salud (MFIPS)** y otros **posgrados en Ciencias de la Salud de la UACH** que necesitan escribir su tesis, especialmente aquellos **SIN experiencia previa en LaTeX**. 

### ✅ Ventajas de Usar LaTeX:

- ✨ **Formato profesional** automático (no más dolores de cabeza con Word)
- 📚 **Gestión de referencias** automática (adiós copiar-pegar)
- 🔢 **Numeración automática** de capítulos, figuras, tablas y ecuaciones
- 🎨 **Consistencia garantizada** en todo el documento
- 📄 **Sin errores de formato** al imprimir o convertir a PDF
- 🚀 **Acepta documentos largos** (100+ páginas) sin problemas

---

## 📁 Estructura de Archivos

```
edicion_tesis/
│
├── plantilla_tesis.tex          ← Archivo PRINCIPAL (aquí está todo conectado)
│
├── capitulos/                   ← Carpeta con tus capítulos (9 archivos)
│   ├── 01_introduccion.tex
│   ├── 02_marco_teorico_antecedentes.tex
│   ├── 03_delimitacion.tex
│   ├── 04_justificacion.tex
│   ├── 05_materiales_metodos.tex
│   ├── 06_resultados.tex
│   ├── 07_discusion.tex
│   ├── 08_conclusiones.tex
│   └── 09_anexos.tex
│
├── figuras/                     ← Guarda aquí tus imágenes (.png, .jpg, .pdf)
│   └── ejemplo.png
│
├── tablas/                      ← (Opcional) Para datos de tablas
│
├── referencias.bib              ← Archivo de referencias bibliográficas
│
├── README_USUARIO.md            ← Este archivo (manual)
├── GUIA_OVERLEAF.md             ← Guía para usar Overleaf (online)
└── compilar.bat                 ← Script para compilar en Windows
```

---

## 🚀 INICIO RÁPIDO (3 Pasos)

### PASO 1: Edita Tus Datos Personales

Abre `plantilla_tesis.tex` y busca la sección "DATOS DEL AUTOR" (líneas 110-130 aproximadamente).

Reemplaza TODO lo que está entre `[corchetes]`:

```latex
\newcommand{\miNombre}{[TU NOMBRE COMPLETO]}
\newcommand{\miTitulo}{[TÍTULO DE TU TESIS]}
\newcommand{\miPrograma}{Maestría en Ciencias de la Computación}
...
```

**Ejemplo real:**
```latex
\newcommand{\miNombre}{María Elena González Pérez}
\newcommand{\miTitulo}{Sistema de Recomendación Basado en Aprendizaje Profundo}
\newcommand{\miPrograma}{Maestría en Ciencias de la Computación}
\newcommand{\miDirector}{Dr. Juan Carlos Rodríguez}
\newcommand{\miMes}{Junio}
\newcommand{\miAño}{2025}
```

### PASO 2: Escribe Tu Contenido

Edita los archivos en la carpeta `capitulos/`. Cada archivo es un capítulo completo.

**Consejos:**
- Usa los archivos de ejemplo como guía
- Todo el texto entre `[corchetes]` debe reemplazarse
- Lee los comentarios (líneas que empiezan con `%`) para ayuda

### PASO 3: Compila Tu Documento

**Opción A: Usando Overleaf (RECOMENDADO para principiantes)**
- Lee la guía `GUIA_OVERLEAF.md`
- No necesitas instalar nada

**Opción B: En tu computadora (Windows)**
1. Instala MiKTeX (ver sección de instalación abajo)
2. Doble clic en `compilar.bat`
3. Espera unos segundos
4. ¡Listo! Tu PDF estará en la misma carpeta

---

## 💻 Instalación Local (Opcional)

### Para Windows:

1. **Descarga MiKTeX:**
   - Ve a: https://miktex.org/download
   - Descarga el instalador (300 MB aprox.)
   - Instala con opciones por defecto

2. **Editor de texto (elige uno):**
   - **TeXstudio** (recomendado): https://www.texstudio.org/
   - **TeXworks** (viene con MiKTeX)
   - **Visual Studio Code** con extensión "LaTeX Workshop"

3. **Compilar:**
   - Abre `plantilla_tesis.tex` en el editor
   - Presiona F5 (o busca botón "Build" / "Compilar")
   - Espera 1-2 minutos
   - Se abrirá el PDF automáticamente

---

## ✏️ Cómo Editar Tu Tesis

### 1. Escribir Texto Normal

Simplemente escribe. Los párrafos se separan con una línea en blanco:

```latex
Este es el primer párrafo. Puede tener varias líneas
sin problema.

Este es el segundo párrafo. Nota la línea en blanco arriba.
```

### 2. Formato de Texto

```latex
\textbf{Texto en negrita}
\textit{Texto en cursiva}
\underline{Texto subrayado}
```

### 3. Listas

**Lista con viñetas:**
```latex
\begin{itemize}
    \item Primer elemento
    \item Segundo elemento
    \item Tercer elemento
\end{itemize}
```

**Lista numerada:**
```latex
\begin{enumerate}
    \item Primer paso
    \item Segundo paso
    \item Tercer paso
\end{enumerate}
```

### 4. Citas y Referencias

**Para citar un trabajo:**

```latex
Según Smith y Doe \cite{smith2023}, el método propuesto...
```

La clave `smith2023` debe existir en tu archivo `referencias.bib`.

**Múltiples citas:**
```latex
Diversos estudios \cite{smith2023,garcia2022,jones2021} han demostrado...
```

---

## 📊 Cómo Insertar Figuras

### Paso 1: Guarda tu imagen

Copia tu imagen (`.png`, `.jpg`, o `.pdf`) a la carpeta `figuras/`.

**Ejemplo:** `figuras/mi_grafica.png`

### Paso 2: Inserta en el texto

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.7\textwidth]{figuras/mi_grafica.png}
    \caption{Descripción de mi gráfica. Explica qué se muestra.}
    \label{fig:mi_grafica}
\end{figure}
```

**Explicación:**
- `[htbp]`: Posición (here, top, bottom, page)
- `width=0.7\textwidth`: Tamaño (70% del ancho de página)
- `\caption{...}`: Texto que aparece debajo de la figura
- `\label{fig:...}`: Etiqueta para referenciar (ver siguiente sección)

### Paso 3: Referenciar la figura en el texto

```latex
Como se observa en la \Cref{fig:mi_grafica}, los resultados muestran...
```

LaTeX automáticamente pondrá: "Como se observa en la **Figura 4.2**, los resultados..."

---

## 📈 Cómo Crear Tablas

### Tabla Simple:

```latex
\begin{table}[htbp]
    \centering
    \caption{Resultados del experimento}
    \label{tab:resultados}
    \begin{tabular}{@{}lcc@{}}
        \toprule
        \textbf{Método} & \textbf{Precisión} & \textbf{Recall} \\
        \midrule
        Método A        & 0.85               & 0.82 \\
        Método B        & 0.88               & 0.86 \\
        Método C        & 0.92               & 0.90 \\
        \bottomrule
    \end{tabular}
\end{table}
```

**Explicación:**
- `{lcc}`: l=izquierda, c=centrado, r=derecha
- `&` separa columnas
- `\\` termina una fila
- `\toprule`, `\midrule`, `\bottomrule`: líneas profesionales

**Referenciar la tabla:**
```latex
Los resultados en la \Cref{tab:resultados} muestran que...
```

**Herramienta útil:** Si Excel es más fácil, usa https://www.tablesgenerator.com/
- Pega tus datos desde Excel
- Clic en "Generate"
- Copia el código LaTeX

---

## 🔢 Ecuaciones Matemáticas

### Ecuación en línea (dentro del texto):

```latex
La fórmula es $E = mc^2$ donde $m$ es la masa.
```

### Ecuación destacada (en su propia línea):

```latex
\begin{equation}
    f(x) = \frac{a}{b} + \sqrt{x}
    \label{eq:mi_ecuacion}
\end{equation}
```

**Símbolos comunes:**
- Fracción: `\frac{arriba}{abajo}`
- Raíz: `\sqrt{x}`
- Potencia: `x^2`
- Subíndice: `x_i`
- Sumatoria: `\sum_{i=1}^{n}`
- Integral: `\int_{a}^{b}`

**Referenciar ecuación:**
```latex
Aplicando la \Cref{eq:mi_ecuacion}, obtenemos...
```

---

## 📚 Cómo Agregar Referencias (Bibliografía)

### Método 1: Editar manualmente `referencias.bib`

Abre `referencias.bib` y agrega entradas como esta:

```bibtex
@article{smith2023,
    author  = {Smith, John and Doe, Jane},
    title   = {Título del artículo},
    journal = {Nombre de la revista},
    year    = {2023},
    volume  = {45},
    pages   = {123--145}
}
```

### Método 2: Usar Google Scholar (¡MÁS FÁCIL!)

1. Busca el artículo en Google Scholar
2. Clic en las comillas `" ` (Citar)
3. Clic en "BibTeX" al final
4. Copia TODO el texto
5. Pega en tu archivo `referencias.bib`

### Método 3: Usar un gestor (Mendeley, Zotero)

- Mendeley: https://www.mendeley.com/
- Zotero: https://www.zotero.org/

Ambos pueden exportar directamente a formato `.bib`.

---

## 🔧 Problemas Comunes y Soluciones

### ❌ "No compila / Error desconocido"

**Solución:**
1. Lee el mensaje de error (suele decir la línea)
2. Busca llaves sin cerrar: `{` debe tener su `}`
3. Busca caracteres especiales: `&`, `%`, `_`, `#` → usa `\&`, `\%`, `\_`, `\#`
4. Verifica que TODAS las figuras existan en la carpeta

### ❌ "La figura no aparece"

**Solución:**
1. Verifica que el archivo existe en `figuras/`
2. Verifica el nombre (con extensión: `.png`, `.jpg`)
3. No uses espacios en nombres de archivo
4. Usa rutas relativas: `figuras/nombre.png`

### ❌ "Las referencias no aparecen"

**Solución:**
Debes compilar **TRES veces** en este orden:
1. pdflatex
2. bibtex
3. pdflatex
4. pdflatex

En Overleaf esto es automático. En local, usa el script `compilar.bat`.

### ❌ "Caracteres raros en español (á, é, í, ñ)"

**Solución:**
Asegúrate de que tu archivo tenga codificación UTF-8:
- En TeXstudio: Menú → Archivo → Guardar con codificación → UTF-8
- La plantilla ya tiene `\usepackage[utf8]{inputenc}`

---

## 🎓 Consejos para Escribir Tu Tesis

### ✅ HAZLO:

- **Escribe en bloques:** Completa una sección antes de pasar a otra
- **Compila frecuentemente:** Cada 15-20 minutos, compila para detectar errores temprano
- **Usa comentarios:** Las líneas con `%` son ignoradas (úsalas para notas personales)
- **Guarda versiones:** Crea respaldos cada semana (ej: `tesis_v1.zip`, `tesis_v2.zip`)
- **Imprime borradores:** Revisar en papel ayuda a encontrar errores

### ❌ NO HAGAS:

- **NO copies código de internet sin entender:** Puede romper todo
- **NO edites el preámbulo** (líneas 1-100 de `plantilla_tesis.tex`) a menos que sepas qué haces
- **NO uses Word para tablas complejas:** Usa Excel + tablesgenerator.com
- **NO dejes la bibliografía para el final:** Agrega referencias conforme avanzas

---

## 📞 ¿Necesitas Ayuda?

### Recursos Online:

1. **Overleaf Learn:**  
   https://www.overleaf.com/learn
   - Tutoriales paso a paso
   - Videos explicativos

2. **LaTeX Wikibook (en español):**  
   https://es.wikibooks.org/wiki/Manual_de_LaTeX
   - Guía completa y detallada

3. **Stack Exchange (TeX):**  
   https://tex.stackexchange.com/
   - Foro de preguntas y respuestas (¡muy activo!)

4. **TeXstudio Manual:**  
   https://www.texstudio.org/
   - Para el editor

### Contacto con el Autor:

- **Email:** [tu_email@uach.mx]
- **GitHub:** [tu_usuario_github]

---

## 📋 Checklist Final (Antes de Imprimir)

Antes de entregar tu tesis, verifica:

- [ ] Todos los datos personales están correctos (nombre, fecha, director)
- [ ] NO hay texto entre `[corchetes]` (eso significa que falta completar)
- [ ] Todas las figuras se ven bien y están referenciadas en el texto
- [ ] Todas las tablas tienen caption y están referenciadas
- [ ] La bibliografía está completa (todas las citas tienen entrada en `.bib`)
- [ ] Los números de página están correctos
- [ ] El índice (tabla de contenido) está actualizado
- [ ] Revisión ortográfica completa
- [ ] Alguien más (colega, familiar) leyó y dio feedback
- [ ] Respaldo guardado en al menos 2 lugares (USB + nube)

---

## 🎁 Créditos y Licencia

Esta plantilla fue creada por **Luis Ángel Martínez Corral** como regalo para los estudiantes de posgrado de la UACH.

**Licencia:** Uso libre para fines académicos. Se permite modificar y redistribuir.

**Agradecimientos:**
- A mis compañeros de maestría por la inspiración
- A mi comité tutorial por su apoyo
- A la comunidad LaTeX por crear herramientas increíbles

---

## 🚀 ¡Listo para Empezar!

No te asustes si al principio parece complicado. **LaTeX tiene una curva de aprendizaje**, pero después de 2-3 días editando, te volverás muy rápido. Los primeros 1-2 capítulos son los más difíciles, ¡luego es pura repetición!

**Recuerda:** Cada error es una oportunidad de aprender. ¡Ánimo con tu tesis! 💪

---

**Última actualización:** Octubre 2025  
**Versión del documento:** 1.0


