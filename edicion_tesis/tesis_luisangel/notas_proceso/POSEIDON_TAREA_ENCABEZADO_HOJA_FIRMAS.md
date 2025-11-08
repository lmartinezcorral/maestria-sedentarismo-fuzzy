# 🔱 TAREA PARA POSEIDÓN: Bug LaTeX - Encabezado Hoja de Firmas

**Fecha:** 08 de Noviembre de 2025, 18:05  
**Agente asignado:** Poseidón 🔱  
**Prioridad:** 🔥 ALTA  
**Archivo afectado:** `plantilla_tesis.tex` (líneas 252-261)

---

## 📋 **CONTEXTO**

Estamos diseñando la **Hoja de Firmas** (página 4) de la tesis con el nuevo formato de la Facultad de Medicina. El encabezado debe tener:

- **Logo UACH** (izquierda, altura 2.2cm)
- **3 títulos institucionales** (centro, 3 líneas verticales, fuente 12pt negrita)
- **Logo Facultad** (derecha, altura 2.2cm)

---

## 🎯 **DISEÑO ESPERADO**

```
┌───────────────┬──────────────────────────────────────────────────────┬───────────────┐
│               │  Universidad Autónoma de Chihuahua                   │               │
│  logo_uach    │  Facultad de Medicina y Ciencias Biomédicas         │ logo_medicina │
│  (2.2cm alto) │  Secretaría de Investigación y Posgrado             │  (2.2cm alto) │
└───────────────┴──────────────────────────────────────────────────────┴───────────────┘
```

**Los logos deben abarcar verticalmente la altura de las 3 líneas de títulos.**

---

## 🐛 **PROBLEMA ACTUAL**

Los títulos se están mostrando **en una sola línea continua** sin saltos:

```
Universidad Autónoma de ChihuahuaFacultad de Medicina y Ciencias BiomédicasSecretaría de Investigación y Posgrado
```

Incluso aparecen pegados sin espacios entre palabras.

---

## 📄 **CÓDIGO ACTUAL (NO FUNCIONA)**

```latex
% Encabezado: logos laterales (altura 3 líneas) + títulos centrados (3 líneas verticales)
\noindent
\begin{tabular}{@{}m{0.15\textwidth}m{0.65\textwidth}m{0.15\textwidth}@{}}
\includegraphics[height=2.2cm]{figuras/logo_uach_bn.png} &
\centering\arraybackslash{\fontsize{12}{14}\selectfont\bfseries 
Universidad Aut\'onoma de Chihuahua\newline
Facultad de Medicina y Ciencias Biom\'edicas\newline
Secretar\'ia de Investigaci\'on y Posgrado} &
\raggedleft\includegraphics[height=2.2cm]{\miLogoEncabezado} \\
\end{tabular}
```

**Problemas identificados:**
1. `\newline` no funciona dentro de `\centering\arraybackslash{...}`
2. Las llaves `{...}` crean un grupo que puede estar interfiriendo
3. `\arraybackslash` puede estar mal ubicado

---

## 🛠️ **INTENTOS PREVIOS (TODOS FALLARON)**

### Intento 1: Usar `\\` en lugar de `\newline`
```latex
\miUniversidad\\
\miFacultad\\
\miSecretaria
```
**Resultado:** Error de compilación o no hace saltos

### Intento 2: Usar `\newline` directamente
```latex
Universidad Aut\'onoma de Chihuahua\newline
Facultad de Medicina y Ciencias Biom\'edicas\newline
Secretar\'ia de Investigaci\'on y Posgrado
```
**Resultado:** No hace saltos, todo en una línea

### Intento 3: Agregar `\arraybackslash`
```latex
\centering\arraybackslash{\fontsize{12}{14}\selectfont\bfseries ...}
```
**Resultado:** No resuelve el problema

### Intento 4: Limpiar archivos auxiliares y recompilar
```powershell
Remove-Item *.aux, *.log, *.bcf, *.out, *.toc
.\compilar.bat
```
**Resultado:** No cambia nada en el PDF

---

## 💡 **ALTERNATIVAS SUGERIDAS PARA EXPLORAR**

### **OPCIÓN A: `minipage` dentro de la tabla (RECOMENDADA)**
```latex
\noindent
\begin{tabular}{@{}m{0.15\textwidth}m{0.65\textwidth}m{0.15\textwidth}@{}}
\includegraphics[height=2.2cm]{figuras/logo_uach_bn.png} &
\begin{minipage}[c]{0.65\textwidth}
    \centering
    {\fontsize{12}{14}\selectfont\bfseries
    Universidad Autónoma de Chihuahua\\
    Facultad de Medicina y Ciencias Biomédicas\\
    Secretaría de Investigación y Posgrado}
\end{minipage} &
\raggedleft\includegraphics[height=2.2cm]{\miLogoEncabezado} \\
\end{tabular}
```

### **OPCIÓN B: `\parbox` con altura explícita**
```latex
\noindent
\begin{tabular}{@{}m{0.15\textwidth}m{0.65\textwidth}m{0.15\textwidth}@{}}
\includegraphics[height=2.2cm]{figuras/logo_uach_bn.png} &
\parbox[c][2.2cm][c]{0.65\textwidth}{%
    \centering\fontsize{12}{14}\selectfont\bfseries
    Universidad Autónoma de Chihuahua\\
    Facultad de Medicina y Ciencias Biomédicas\\
    Secretaría de Investigación y Posgrado} &
\raggedleft\includegraphics[height=2.2cm]{\miLogoEncabezado} \\
\end{tabular}
```

### **OPCIÓN C: `\shortstack` (simple pero efectivo)**
```latex
\noindent
\begin{tabular}{@{}m{0.15\textwidth}m{0.65\textwidth}m{0.15\textwidth}@{}}
\includegraphics[height=2.2cm]{figuras/logo_uach_bn.png} &
\centering{\fontsize{12}{14}\selectfont\bfseries
\shortstack{Universidad Autónoma de Chihuahua\\
Facultad de Medicina y Ciencias Biomédicas\\
Secretaría de Investigación y Posgrado}} &
\raggedleft\includegraphics[height=2.2cm]{\miLogoEncabezado} \\
\end{tabular}
```

### **OPCIÓN D: Abandonar tabla, usar solo `minipage` con `\hfill`**
(Luis prefiere evitar esta opción porque ya la intentamos antes)

```latex
\noindent
\begin{minipage}[c]{0.15\textwidth}
    \includegraphics[height=2.2cm]{figuras/logo_uach_bn.png}
\end{minipage}%
\hfill
\begin{minipage}[c]{0.65\textwidth}
    \centering
    {\fontsize{12}{14}\selectfont\bfseries
    Universidad Autónoma de Chihuahua\\
    Facultad de Medicina y Ciencias Biomédicas\\
    Secretaría de Investigación y Posgrado}
\end{minipage}%
\hfill
\begin{minipage}[c]{0.15\textwidth}
    \raggedleft
    \includegraphics[height=2.2cm]{\miLogoEncabezado}
\end{minipage}
```

---

## 🎯 **TU MISIÓN, POSEIDÓN**

1. **Analizar** por qué `\newline` no funciona dentro de la tabla
2. **Probar** las alternativas sugeridas (A, B, C, o proponer la tuya)
3. **Implementar** la solución que funcione
4. **Compilar** y verificar visualmente el PDF (página 4)
5. **Documentar** la solución en comentarios del código
6. **Reportar** en `COMUNICACION_AGENTES.md` qué solución funcionó y por qué

---

## 📦 **ARCHIVOS RELEVANTES**

- **Plantilla principal:** `plantilla_tesis.tex` (líneas 252-261)
- **Variables LaTeX:** Líneas 98-100 (universidad, facultad, secretaría)
- **Figuras:**
  - `figuras/logo_uach_bn.png` (logo blanco y negro UACH)
  - `figuras/Logo_facultad_medicina.png` (logo facultad)
- **Script compilación:** `compilar.bat`

---

## 📊 **CRITERIOS DE ÉXITO**

✅ Los 3 títulos aparecen en **líneas separadas**  
✅ Los logos están **alineados verticalmente** con los títulos  
✅ Todo está **centrado horizontalmente**  
✅ **No hay warnings** de LaTeX relacionados con la tabla  
✅ El código es **limpio y mantenible**  

---

## 🔥 **NOTAS ADICIONALES**

- Luis está usando **Windows 10 + PowerShell + MiKTeX**
- El proyecto está versionado en **Git**
- Después de la solución, Luis hará un **checkpoint**
- Este encabezado se usa **solo en la Hoja de Firmas** (página 4, sin numeración)

---

## 📝 **PLANTILLA DE REPORTE**

Cuando termines, reporta en `COMUNICACION_AGENTES.md`:

```markdown
## ✅ REPORTE POSEIDÓN - Encabezado Hoja de Firmas RESUELTO

**Fecha:** [fecha]  
**Solución implementada:** OPCIÓN [A/B/C/D/otra]

### 🔍 Análisis del problema:
[Explicación de por qué no funcionaba]

### ✅ Solución:
[Código LaTeX que funcionó]

### 🧪 Prueba:
- ✅ Compilación exitosa
- ✅ PDF verificado visualmente
- ✅ No warnings

### 📚 Documentación:
[Comentarios agregados al código para futuros usuarios]

**Estado:** ✅ COMPLETADO
```

---

¡Adelante, Poseidón! Que las aguas del LaTeX fluyan a tu favor. 🌊🔱

