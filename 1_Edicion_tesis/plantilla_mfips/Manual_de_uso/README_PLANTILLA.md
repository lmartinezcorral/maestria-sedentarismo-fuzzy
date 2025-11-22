# 📝 Plantilla de Tesis MFIPS-UACH (v1.2)

**Universidad Autónoma de Chihuahua**  
**Facultad de Medicina y Ciencias Biomédicas**  
**Maestría en Formación e Innovación para Profesionales de la Salud (MFIPS)**

---

## 🎯 **Formato Perfeccionado (Noviembre 2025)**

Esta plantilla incluye ajustes milimétricos validados con requisitos institucionales UACH-MFIPS:
- ✅ Hoja de Firmas con alineación perfecta (-2.8\baselineskip)
- ✅ Índice con logo en todas las páginas (7-11)
- ✅ Espaciado óptimo para impresión (headsep 18pt)
- ✅ Numeración continua desde página 12
- ✅ Compilación automática con renombrado de PDF

---

## 📋 **Descripción**

Esta plantilla en LaTeX está diseñada específicamente para cumplir con los requisitos de formato de tesis del programa de Maestría en Formación e Innovación para Profesionales de la Salud (MFIPS) de la UACH.

### ✨ **Características Principales**

- ✅ **Formato oficial UACH-MFIPS** completo
- ✅ **Normas APA 7ma Edición** integradas
- ✅ **9 capítulos estructurados** con instrucciones detalladas
- ✅ **Plantillas de tablas y figuras** formato APA
- ✅ **Sistema de referencias** con `natbib` y BibTeX
- ✅ **Compilación automatizada** con `compilar.bat`
- ✅ **Guía de normas APA** incluida

---

## 🚀 **Inicio Rápido**

### 1. **Requisitos Previos**

Necesitas tener instalado:
- **MiKTeX** o **TeX Live** (distribución LaTeX para Windows)
- **Editor de LaTeX** recomendado: TeXstudio, Overleaf, o VS Code con LaTeX Workshop

### 2. **Compilar la Plantilla**

**Opción A: Usando el script automático (Windows)**
```batch
compilar.bat
```

**Opción B: Manual (4 pasos)**
```batch
pdflatex plantilla_tesis.tex
bibtex plantilla_tesis
pdflatex plantilla_tesis.tex
pdflatex plantilla_tesis.tex
```

---

## 📁 **Estructura de Archivos**

```
plantilla_mfips/
│
├── plantilla_tesis.tex          # Documento principal (EDITAR AQUÍ)
├── referencias.bib               # Tu bibliografía en formato BibTeX
├── compilar.bat                  # Script de compilación automática
│
├── LEEME_PRIMERO.txt             # Guía de inicio rápido
├── README.md                     # Descripción general
├── README_PLANTILLA.md           # Este archivo
├── README_USUARIO.md             # Manual completo (90+ páginas)
├── RESUMEN_EJECUTIVO.md          # Visión general del proyecto
├── NORMAS_APA_FORMATO.md         # Guía completa de formato APA
├── GUIA_OVERLEAF.md              # Guía para Overleaf
├── GUIA_RAPIDA_REFERENCIA.md     # Cheat sheet de comandos
│
├── capitulos/                    # Todos tus capítulos
│   ├── 01_introduccion.tex
│   ├── 02_marco_teorico_antecedentes.tex
│   ├── 03_delimitacion.tex
│   ├── 04_justificacion.tex
│   ├── 05_materiales_metodos.tex     ← CON EJEMPLOS completos
│   ├── 06_resultados.tex
│   ├── 07_discusion.tex
│   ├── 08_conclusiones.tex
│   └── 09_anexos.tex
│
├── figuras/                      # Coloca aquí tus imágenes
│   ├── logo_uach_portada.png
│   ├── logo_uach_bn.png
│   └── Logo_facultad_medicina.png
│
└── tablas/                       # (Opcional) Datos de tablas
```

---

## ✏️ **Cómo Personalizar**

### **Paso 1: Editar Datos Personales**

Abre `plantilla_tesis.tex` y modifica las líneas 35-51:

```latex
% --------------------- DATOS EDITABLES ----------------------
\newcommand{\miUniversidad}{Universidad Aut\'onoma de Chihuahua}
\newcommand{\miFacultad}{Facultad de Medicina y Ciencias Biom\'edicas}

\newcommand{\miTitulo}{TU TÍTULO DE TESIS AQUÍ}
\newcommand{\miAutor}{TU NOMBRE COMPLETO}

\newcommand{\miCiudad}{Chihuahua, Chih., M\'exico}
\newcommand{\miFecha}{DD de Mes de 2025}
```

### **Paso 2: Editar Comité Tutorial (Líneas 110-130)**

Actualiza los nombres de tu secretario, coordinador, director y asesores:

```latex
% --------------------- COMITÉ TUTORIAL ----------------------
% DATOS CONSTANTES (ya definidos - iguales para todos MFIPS):
\newcommand{\miSecretario}{Dr. Oscar Aguirre Barrera}
\newcommand{\miCoordinadora}{Dra. Haydeé Parra Acosta}

% DATOS VARIABLES (EDITA ESTOS con tu comité):
\newcommand{\miDirector}{Dr. [Nombre de tu Director]}
\newcommand{\miCodirector}{Dr. [Nombre de tu Codirector]}
\newcommand{\miAsesorUno}{Dr. [Nombre Asesor 1]}
\newcommand{\miAsesorDos}{Dr. [Nombre Asesor 2]}
```

**💡 Nota:** El Secretario y Coordinadora ya están definidos (constantes MFIPS). Solo edita Director, Codirector y Asesores con los nombres específicos de TU comité tutorial.

### **Paso 3: Escribir tu Contenido**

Edita cada archivo en la carpeta `capitulos/`:

#### **📖 Capítulos Obligatorios**

| Capítulo | Archivo | Descripción |
|----------|---------|-------------|
| Introducción | `01_introduccion.tex` | Contexto, problema, objetivos, hipótesis |
| Marco Teórico | `02_marco_teorico_antecedentes.tex` | Revisión de literatura y antecedentes |
| Delimitación | `03_delimitacion.tex` | Delimitación del objeto de estudio |
| Justificación | `04_justificacion.tex` | Importancia y relevancia |
| Materiales y Métodos | `05_materiales_metodos.tex` | Diseño, población, instrumentos, análisis |
| Resultados | `06_resultados.tex` | Presentación objetiva de hallazgos |
| Discusión | `07_discusion.tex` | Interpretación y comparación con literatura |
| Conclusiones | `08_conclusiones.tex` | Conclusiones concretas y recomendaciones |
| Anexos | `09_anexos.tex` | Material complementario |

**💡 Cada archivo `.tex` incluye:**
- ✅ Instrucciones detalladas comentadas
- ✅ Ejemplos de tablas y figuras
- ✅ Estructura sugerida por sección
- ✅ Recordatorios de requisitos de la facultad

---

## 📚 **Gestión de Referencias**

### **Agregar Referencias al Archivo `referencias.bib`**

#### **Ejemplo: Artículo de Revista**
```bibtex
@article{garcia2023,
    author  = {García, María and López, Carlos},
    title   = {Título del artículo},
    journal = {Nombre de la Revista},
    year    = {2023},
    volume  = {15},
    number  = {2},
    pages   = {45--67},
    doi     = {10.1234/ejemplo}
}
```

#### **Ejemplo: Libro**
```bibtex
@book{martinez2022,
    author    = {Martínez, Luis},
    title     = {Título del Libro},
    publisher = {Editorial},
    year      = {2022},
    address   = {Ciudad, País}
}
```

### **Citar en el Texto (Formato APA 7)**

```latex
% Cita narrativa (autor como parte del texto)
Según García et al. \cite{garcia2023}, el método propuesto...

% Cita entre paréntesis (al final del texto)
El método propuesto muestra resultados superiores \cite{garcia2023}.

% Múltiples citas
Diversos estudios \cite{garcia2023,WHO2020,Bull2020} coinciden en...

% Cita con página específica
Como menciona Smith \cite[p.~45]{smith2023}...
```

**🔍 Vista Previa del Resultado:**
- Narrativa: Según García et al. (2023), el método...
- Paréntesis: ...resultados superiores (García et al., 2023).
- Múltiples: ...diversos estudios (García et al., 2023; WHO, 2020; Bull et al., 2020)

---

## 🎨 **Tablas y Figuras (Formato APA)**

### **Tabla Básica**

```latex
\begin{table}[htbp]
    \centering
    \caption{Título descriptivo de la tabla}
    \label{tab:mi_tabla}
    \begin{tabular}{@{}lcc@{}}
        \toprule
        \textbf{Variable} & \textbf{Media} & \textbf{DE} \\
        \midrule
        Variable 1 & 25.3 & 4.2 \\
        Variable 2 & 30.1 & 5.8 \\
        \bottomrule
    \end{tabular}
    \\[5pt]
    \footnotesize{\textit{Nota:} DE = Desviación Estándar}
\end{table}
```

### **Figura Básica**

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.7\textwidth]{figuras/mi_grafica.png}
    \caption{Título descriptivo de la figura}
    \label{fig:mi_figura}
\end{figure}
```

**📌 Citar en texto:**
```latex
Como se observa en la Tabla 1...
La Figura 2 muestra que...
```

---

## 📐 **Formato APA Implementado**

### ✅ **Márgenes**
- Superior: 2.5 cm
- Inferior: 2.5 cm
- Izquierdo: 3.0 cm
- Derecho: 2.5 cm

### ✅ **Tipografía**
- Fuente: Times New Roman 12 pt
- Interlineado: 1.5 líneas
- Sangría primera línea: 1.2 cm

### ✅ **Numeración**
- Todas las páginas numeradas en esquina superior derecha
- Portada es página 1

### ✅ **Títulos (5 Niveles)**
1. **Nivel 1:** Centrado, Negrita, Cada Palabra en Mayúscula
2. **Nivel 2:** Izquierda, Negrita, Cada Palabra en Mayúscula
3. **Nivel 3:** Izquierda, Negrita, Cursiva, Cada Palabra en Mayúscula
4. **Nivel 4:** Sangría, Negrita, Primera palabra mayúscula, punto final.
5. **Nivel 5:** Sangría, Negrita, Cursiva, Primera palabra mayúscula, punto final.

📖 **Guía completa:** Ver `NORMAS_APA_FORMATO.md`

---

## 🔧 **Solución de Problemas**

### **Problema: "No compila / Errores de LaTeX"**

1. **Verifica que todos los paquetes estén instalados:**
   - Abre MiKTeX Console → Packages → Busca e instala: `natbib`, `booktabs`, `ragged2e`, `cleveref`

2. **Compila en el orden correcto:**
   - Usa `compilar.bat` o los 4 pasos manuales

3. **Revisa caracteres especiales:**
   - Escapa: `_`, `%`, `&`, `$`, `#`
   - Usa: `\_`, `\%`, `\&`, `\$`, `\#`

### **Problema: "Las citas aparecen como ??"**

- Asegúrate de correr **BibTeX** después del primer `pdflatex`
- Verifica que las claves en `\cite{}` coincidan con las de `referencias.bib`

### **Problema: "Imágenes no aparecen"**

- Coloca tus imágenes en la carpeta `figuras/`
- Usa rutas relativas: `figuras/mi_imagen.png`
- Formatos soportados: PNG, JPG, PDF

---

## 📞 **Soporte y Contacto**

### **Recursos Adicionales**

- 📘 **Manual de LaTeX:** [Overleaf Documentation](https://www.overleaf.com/learn)
- 📕 **Normas APA 7ma Ed.:** Ver `NORMAS_APA_FORMATO.md` incluido
- 📗 **Formato MFIPS:** Consulta con tu director de tesis

### **Comparte con tus Compañeros**

Esta plantilla fue desarrollada colaborativamente. Siéntete libre de compartirla con otros estudiantes del programa MFIPS-UACH.

---

## 📝 **Historial de Versiones**

| Versión | Fecha | Cambios |
|---------|-------|---------|
| v1.2 | Nov 2025 | Formato perfeccionado: ajustes milimétricos Hoja Firmas, Índice con logos, espaciado optimizado |
| v1.0 | Oct 2025 | Versión inicial con todos los capítulos y normas APA |

---

## 🎓 **Créditos**

**Desarrollado para:**  
Maestría en Formación e Innovación para Profesionales de la Salud (MFIPS)  
Facultad de Medicina y Ciencias Biomédicas  
Universidad Autónoma de Chihuahua

---

## 📄 **Licencia**

Esta plantilla es de uso libre para estudiantes del programa MFIPS-UACH.  
Se permite su distribución y modificación citando la fuente.

---

**¡Mucho éxito con tu tesis! 🎉**

*"MENTI DA LUCEM, MANIBUS ARTEM"*

