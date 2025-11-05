# Normas APA 7ma Edición - Formato para LaTeX
**Referencia para implementación en plantilla de tesis MFIPS-UACH**

---

## 📄 **Configuración General**

### Tamaño de Papel
- **Formato:** Carta (21.59 cm × 27.94 cm / 8.5" × 11")
- **LaTeX:** `\geometry{letterpaper,...}`

### Fuente
- **Texto principal:** Times New Roman 12 pt
- **Figuras:** Sans-serif 8-14 pt
- **Código:** Lucida Console o Courier New 10 pt (monoespaciada)

### Márgenes
**APA 7 Oficial:** 2.54 cm (1 pulgada) en TODOS los lados
- Superior: 2.54 cm
- Inferior: 2.54 cm
- Izquierdo: 2.54 cm
- Derecho: 2.54 cm

### Interlineado
- **General:** 1.5 líneas (`\onehalfspacing`)
- **Tablas:** Puede ser sencillo, 1.5 o doble (según legibilidad)
- **Títulos:** Doble

---

## 📑 **Títulos y Subtítulos (5 Niveles)**

### Nivel 1: `\chapter{}` o `\section{}`
- **Formato:** Centrado, Negrita, Cada Palabra en Mayúscula
- **LaTeX:** 
  ```latex
  \begin{center}
  {\bfseries Título de Nivel 1}
  \end{center}
  ```
- **Texto:** Inicia en nuevo párrafo

### Nivel 2: `\section{}`
- **Formato:** Izquierda, Negrita, Cada Palabra en Mayúscula
- **LaTeX:** `\section{Título de Nivel 2}`
- **Texto:** Inicia en nuevo párrafo

### Nivel 3: `\subsection{}`
- **Formato:** Izquierda, Negrita, Cursiva, Cada Palabra en Mayúscula
- **LaTeX:** `\subsection{\textit{Título de Nivel 3}}`
- **Texto:** Inicia en nuevo párrafo

### Nivel 4: `\subsubsection{}`
- **Formato:** Izquierda, Negrita, Cada Palabra en Mayúscula, Sangría 1.27 cm, Punto final
- **LaTeX:** 
  ```latex
  \paragraph{Título de Nivel 4.} Texto continúa en la misma línea...
  ```
- **Texto:** Inicia en la misma línea

### Nivel 5: `\paragraph{}`
- **Formato:** Izquierda, Negrita, Cursiva, Cada Palabra en Mayúscula, Sangría 1.27 cm, Punto final
- **LaTeX:**
  ```latex
  \paragraph{\textit{Título de Nivel 5.}} Texto continúa en la misma línea...
  ```
- **Texto:** Inicia en la misma línea

---

## 📊 **Tablas (Formato APA)**

### Estructura
```
Tabla 1
Título de la Tabla en Cursiva

┌─────────────────────────────────┐
│ Encabezado 1 │ Encabezado 2    │ (centrados)
├─────────────────────────────────┤
│ Dato 1       │ Dato 2          │ (centrados o izq)
│ Dato 3       │ Dato 4          │
└─────────────────────────────────┘

Nota. Descripción adicional si es necesaria.
```

### Componentes LaTeX

```latex
\begin{table}[htbp]
    \centering
    \caption{Título de la Tabla en Cursiva}
    \label{tab:mi_tabla}
    \begin{tabular}{@{}lcc@{}}
        \toprule
        \textbf{Encabezado 1} & \textbf{Encabezado 2} & \textbf{Encabezado 3} \\
        \midrule
        Dato 1 & Dato 2 & Dato 3 \\
        Dato 4 & Dato 5 & Dato 6 \\
        \bottomrule
    \end{tabular}
    \\[5pt]
    \footnotesize{\textit{Nota.} Descripción adicional.}
\end{table}
```

### Reglas de Bordes
- ✅ Línea arriba de encabezados (`\toprule`)
- ✅ Línea debajo de encabezados (`\midrule`)
- ✅ Línea arriba de totales (si hay)
- ✅ Línea al final de tabla (`\bottomrule`)
- ❌ NO líneas verticales
- ❌ NO bordes alrededor de celdas

### Ubicación
- **Opción 1:** Incrustar después de primera mención
- **Opción 2:** Al final después de referencias

### Citar en Texto
```latex
Los resultados se muestran en la Tabla 3.
Como se observa en la \Cref{tab:mi_tabla}...
```

---

## 📈 **Figuras (Formato APA)**

### Estructura
```
Figura 1
Título de la Figura en Cursiva

[IMAGEN/GRÁFICO]

Nota. Descripción y atribución de derechos de autor.
```

### Componentes LaTeX

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.7\textwidth]{figuras/mi_figura.png}
    \caption{Título de la Figura en Cursiva}
    \label{fig:mi_figura}
    \\[5pt]
    \footnotesize{\textit{Nota.} Descripción adicional.}
\end{figure}
```

### Nota de Derechos de Autor

**Figura adaptada:**
```
Nota. Adaptado de "Título Original" (p. 120), por A. Apellido, 2014, Editorial.
```

**Figura propia:**
- No requiere nota de derechos de autor
- Si no hay `\cite{}`, se asume que es del autor

### Citar en Texto
```latex
Como se observa en la Figura 2...
La \Cref{fig:mi_figura} muestra...
```

---

## 📝 **Sangría de Párrafos**

### Regla General
- **Primera línea:** Sangría de 1.27 cm (½ pulgada)
- **LaTeX:** `\setlength{\parindent}{1.27cm}`

### Excepciones (SIN sangría)

```latex
% Después de títulos
\section{Título}
\noindent Primer párrafo sin sangría...

Segundo párrafo con sangría normal...

% Primer párrafo del resumen
\noindent El resumen debe...
```

---

## 📚 **Apéndices**

### Un Solo Apéndice
```latex
\chapter*{Apéndice}
\addcontentsline{toc}{chapter}{Apéndice}

Contenido del apéndice...
```

### Múltiples Apéndices
```latex
\chapter*{Apéndice A: Título del Apéndice A}
\addcontentsline{toc}{chapter}{Apéndice A: Título}

\chapter*{Apéndice B: Título del Apéndice B}
\addcontentsline{toc}{chapter}{Apéndice B: Título}
```

### Tablas en Apéndices
- **Con múltiples apéndices:** `Tabla A1`, `Tabla B2`
- **Un solo apéndice:** `Tabla A1`

### Ubicación
- Después de Referencias
- Cada apéndice en página nueva

---

## 🔢 **Numeración de Páginas**

### Trabajos Estudiantiles (Tu caso)
- **Solo número de página** en esquina superior derecha
- **LaTeX:**
  ```latex
  \fancyhead[R]{\thepage}
  \renewcommand{\headrulewidth}{0pt}
  ```

### Trabajos Profesionales
- Título corto (izquierda) + número (derecha)
- Máximo 50 caracteres en MAYÚSCULAS

---

## 📐 **Interlineado**

### General
- **Texto:** 1.5 líneas (`\onehalfspacing`)
- **Títulos:** Doble (`\doublespacing` localmente)
- **Tablas:** Flexible (sencillo, 1.5 o doble)

### Excepciones
- Citas en bloque: sencillo
- Referencias: sencillo o 1.5
- Notas de tablas/figuras: sencillo

---

## 🎯 **Implementación en LaTeX - Plantilla Actual**

### Ya Configurado ✅
```latex
\geometry{letterpaper,top=2.5cm,bottom=2.5cm,left=3.0cm,right=2.5cm}
\onehalfspacing
\setlength{\parindent}{1.2cm}  % Cercano a 1.27 cm
\fancyhead[R]{\thepage}
```

### Por Configurar
- Ajustar `\chapter`, `\section`, `\subsection` según niveles APA
- Implementar formato de tablas con `booktabs`
- Implementar formato de figuras con `caption`

---

*Documento de referencia - 30 de Octubre de 2025*


