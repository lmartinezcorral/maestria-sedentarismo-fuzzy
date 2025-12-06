# 📊 COMPARACIÓN DE PAQUETES PARA ALGORITMOS Y CÓDIGO

## 1. DIFERENCIAS ENTRE PAQUETES

### **`algorithmic` + `algorithm` (ACTUAL)**
**Ventajas:**
- ✅ Diseñado específicamente para pseudocódigo estructurado
- ✅ Sintaxis matemática integrada (`$\gets$`, `$\leq$`, etc.)
- ✅ Estructuras de control claras (`\For`, `\If`, `\Procedure`)
- ✅ Numeración automática de líneas
- ✅ Ideal para algoritmos matemáticos/científicos

**Desventajas:**
- ❌ No tiene resaltado de sintaxis de lenguajes reales
- ❌ Fuente predeterminada (Times New Roman, no monospace)
- ❌ No permite fondo de color fácilmente
- ❌ Limitado para código fuente real

**Uso recomendado:** Pseudocódigo, algoritmos matemáticos, procedimientos estructurados

---

### **`algorithm2e`**
**Ventajas:**
- ✅ Sintaxis más compacta y moderna
- ✅ Mejor control visual (cajas, colores, líneas)
- ✅ Soporte para múltiples estilos de caja
- ✅ Más flexible en diseño

**Desventajas:**
- ❌ Sintaxis diferente (requiere reescribir)
- ❌ Menos común en literatura científica
- ❌ No tiene resaltado de sintaxis

**Uso recomendado:** Algoritmos con diseño visual más elaborado

---

### **`listings` (RECOMENDADO PARA CÓDIGO)**
**Ventajas:**
- ✅ **Resaltado de sintaxis** (Python, R, etc.)
- ✅ **Fuente monospace** (Courier New, Consolas)
- ✅ **Fondo de color** fácilmente configurable
- ✅ **Estilo IDE/VSCode** con colores
- ✅ Numeración de líneas personalizable
- ✅ Bordes y marcos configurables
- ✅ Ideal para fragmentos de código real

**Desventajas:**
- ❌ No tiene estructuras de control matemáticas (`\For`, `\If`)
- ❌ Requiere escribir código más literalmente
- ❌ Menos ideal para pseudocódigo matemático

**Uso recomendado:** Código fuente real, fragmentos de implementación, scripts

---

## 2. RECOMENDACIÓN SEGÚN CONTEXTO

| Tipo de Contenido | Paquete Recomendado | Razón |
|-------------------|---------------------|-------|
| **Pseudocódigo matemático** | `algorithmic` | Estructuras claras, notación matemática |
| **Algoritmo con diseño visual** | `algorithm2e` | Más control de formato |
| **Código Python/R real** | `listings` | Resaltado de sintaxis, estilo IDE |
| **Fragmentos de código cortos** | `listings` | Fondo, fuente monospace |
| **Algoritmo en tabla (APA 7)** | `algorithmic` + tabla | Ya implementado, funciona bien |

---

## 3. CONFIGURACIÓN `listings` ESTILO IDE/VSCode

### Configuración en `estilos_apa7.sty`:

```latex
% ============================================================================
% CONFIGURACIÓN DE LISTINGS PARA CÓDIGO (ESTILO IDE/VSCode)
% ============================================================================
\RequirePackage{listings}
\RequirePackage{xcolor}

% Paleta de colores estilo VSCode Dark+
\definecolor{codebackground}{RGB}{30,30,30}      % Fondo oscuro
\definecolor{codeforeground}{RGB}{212,212,212}   % Texto claro
\definecolor{codekeyword}{RGB}{86,156,214}       % Azul (keywords)
\definecolor{codestring}{RGB}{206,145,120}       % Naranja (strings)
\definecolor{codecomment}{RGB}{106,153,85}       % Verde (comentarios)
\definecolor{codefunction}{RGB}{220,220,170}    % Amarillo (funciones)
\definecolor{codeborder}{RGB}{100,100,100}       % Borde gris

% Estilo para código Python
\lstdefinestyle{pythoncode}{
    language=Python,
    basicstyle=\ttfamily\fontsize{10}{12}\selectfont\color{codeforeground},
    backgroundcolor=\color{codebackground},
    frame=single,
    frameround=tttt,
    rulecolor=\color{codeborder},
    linewidth=0.8pt,
    keywordstyle=\color{codekeyword}\bfseries,
    commentstyle=\color{codecomment}\itshape,
    stringstyle=\color{codestring},
    functionstyle=\color{codefunction},
    numbers=left,
    numberstyle=\tiny\color{codeforeground},
    stepnumber=1,
    numbersep=8pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=4,
    breaklines=true,
    breakatwhitespace=false,
    captionpos=b,
    xleftmargin=12pt,
    xrightmargin=12pt,
    framexleftmargin=8pt,
    framexrightmargin=8pt,
    aboveskip=6pt,
    belowskip=6pt
}

% Estilo para pseudocódigo (sin resaltado de sintaxis)
\lstdefinestyle{pseudocode}{
    basicstyle=\ttfamily\fontsize{10}{12}\selectfont\color{codeforeground},
    backgroundcolor=\color{codebackground},
    frame=single,
    frameround=tttt,
    rulecolor=\color{codeborder},
    linewidth=0.8pt,
    numbers=left,
    numberstyle=\tiny\color{codeforeground},
    stepnumber=1,
    numbersep=8pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=4,
    breaklines=true,
    breakatwhitespace=false,
    captionpos=b,
    xleftmargin=12pt,
    xrightmargin=12pt,
    framexleftmargin=8pt,
    framexrightmargin=8pt,
    aboveskip=6pt,
    belowskip=6pt
}

% Estilo claro (para impresión en blanco y negro)
\lstdefinestyle{pythoncode-light}{
    language=Python,
    basicstyle=\ttfamily\fontsize{10}{12}\selectfont,
    backgroundcolor=\color{gray!10},
    frame=single,
    frameround=tttt,
    rulecolor=\color{black!30},
    linewidth=0.8pt,
    keywordstyle=\bfseries,
    commentstyle=\itshape\color{gray!60},
    stringstyle=\color{black!80},
    numbers=left,
    numberstyle=\tiny\color{gray!50},
    stepnumber=1,
    numbersep=8pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=4,
    breaklines=true,
    breakatwhitespace=false,
    captionpos=b,
    xleftmargin=12pt,
    xrightmargin=12pt,
    framexleftmargin=8pt,
    framexrightmargin=8pt,
    aboveskip=6pt,
    belowskip=6pt
}

% Estilo predeterminado
\lstset{style=pythoncode-light}  % Usar estilo claro por defecto
```

---

## 4. EJEMPLO DE USO CON `listings` EN TABLA

```latex
\begin{table}[htbp]
    \centering
    \caption{Preprocesamiento XML $\rightarrow$ CSV diario}
    \label{alg:xml_csv}
    \begin{tabularx}{\textwidth}{@{}X@{}}
        \toprule
        \textbf{Algoritmo 1.} \textit{Preprocesamiento XML $\rightarrow$ CSV diario} \\
        \midrule
        \begin{lstlisting}[style=pseudocode]
Entrada: archivo export.zip por participante
Salida: DB_u{id}.csv con columnas [fecha, pasos, calorías, FC_reposo, HRV_SDNN, ...]

procedure PARSEXML(xml_file, user_id):
    tree <- parse(xml_file)
    records <- tree.findall("Record")
    df <- empty_dataframe()
    for record in records do:
        if record.sourceName contains "Apple Watch" then:
            type <- record.type
            value <- record.value
            date <- record.startDate.date()
            df.append([date, type, value])
        end if
    end for
    df_pivot <- df.pivot(index=date, columns=type, values=value)
    df_pivot.to_csv(f"DB_u{user_id}.csv")
end procedure
        \end{lstlisting} \\
        \bottomrule
    \end{tabularx}
\end{table}
```

---

## 5. FIGURAS VS TABLAS SEGÚN APA 7 Y TU MANUAL

### **Según APA 7 (Oficial):**
- **Tablas:** Datos cuantitativos organizados en filas y columnas
- **Figuras:** Ilustraciones, gráficos, diagramas, fotografías
- **Código/Fórmulas:** NO se clasifican como tablas ni figuras
  - Código: Se presenta como bloque de texto con formato especial
  - Fórmulas: Se presentan como ecuaciones numeradas

### **Según tu Manual (Regla Local):**
> "Todo lo que no sea una tabla será considerado una figura"

**Implicaciones:**
- ✅ **Algoritmos/Pseudocódigo:** Si está en tabla → **Tabla**
- ✅ **Algoritmos/Pseudocódigo:** Si está fuera de tabla → **Figura**
- ✅ **Fórmulas matemáticas:** Generalmente se presentan como ecuaciones numeradas (no tabla ni figura)
- ✅ **Fragmentos de código:** Si está en tabla → **Tabla**; si está fuera → **Figura**

### **Recomendación para tu Tesis:**

**Opción 1: Algoritmo en Tabla (ACTUAL - RECOMENDADO)**
```latex
\begin{table}[htbp]
    \caption{Algoritmo 1. Preprocesamiento...}
    \begin{tabularx}{\textwidth}{@{}X@{}}
        \toprule
        \textbf{Algoritmo 1.} \textit{...} \\
        \midrule
        [contenido del algoritmo] \\
        \bottomrule
    \end{tabularx}
\end{table}
```
✅ **Ventaja:** Formato consistente con tablas APA 7, numeración como tabla

**Opción 2: Algoritmo como Figura**
```latex
\begin{figure}[htbp]
    \caption{Algoritmo 1. Preprocesamiento...}
    \begin{lstlisting}[style=pseudocode]
    [código aquí]
    \end{lstlisting}
\end{figure}
```
✅ **Ventaja:** Más flexible visualmente, puede usar `listings` con fondo

**Opción 3: Fórmulas como Ecuaciones (NO tabla ni figura)**
```latex
\begin{equation}
    \text{Actividad\_relativa} = \frac{\text{min\_movimiento}}{60 \times \text{hrs\_monitoreadas}}
    \label{eq:actividad_relativa}
\end{equation}
```
✅ **Ventaja:** Formato estándar para fórmulas matemáticas

---

## 6. RECOMENDACIÓN FINAL

### **Para Algoritmos:**
- ✅ **Mantener formato de tabla** (como está ahora)
- ✅ **Agregar configuración `listings`** para estilo de código si quieres fondo/colores
- ✅ **Usar `algorithmic` dentro de tabla** para mantener estructura matemática

### **Para Fragmentos de Código Cortos:**
- ✅ **Usar `listings` con estilo claro** (fondo gris claro, fuente Courier)
- ✅ **Presentar como figura** si está fuera de tabla
- ✅ **Presentar como tabla** si quieres formato APA 7 estricto

### **Para Fórmulas:**
- ✅ **Usar `equation` o `align`** (no tabla ni figura)
- ✅ **Numerar con `\label`** para referencias

---

## 7. IMPLEMENTACIÓN SUGERIDA

**Paso 1:** Agregar configuración `listings` a `estilos_apa7.sty`

**Paso 2:** Mantener algoritmo actual en tabla con `algorithmic`

**Paso 3:** Para fragmentos de código adicionales, usar `listings` en figura

**Paso 4:** Para fórmulas, usar entornos `equation`/`align`

---

**¿Quieres que implemente alguna de estas configuraciones?**

