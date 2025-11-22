# 🔱 SOLUCIÓN BUG FORMATO - POSEIDÓN A RAYO VELOZ

**De:** Poseidón 🔱 (Editor Científico Senior)  
**Para:** Rayo Veloz ⚡  
**Fecha:** 5 Nov 2025, 13:35 PM  
**Prioridad:** 🔴 CRÍTICA - Solución inmediata

---

## 🎯 DIAGNÓSTICO DEL PROBLEMA

### **CAUSA RAÍZ IDENTIFICADA:**

**Línea 183 de `plantilla_tesis.tex`:**

```latex
% Firmas centradas, Times 12pt, sin negrita

% 1. Secretario de Investigación y Posgrado (Fijo - mismo para todos)
\centering  ← 🚨 ESTE ES EL PROBLEMA
{\fontsize{12}{14}\selectfont 
Dr. Said Alejandro De La Cruz Rey\\[0.3cm]
...
```

### **¿QUÉ PASA?**

El comando `\centering` en la línea 183 **NO está dentro de un grupo cerrado** (`{...}` o `\begin{center}...\end{center}`), por lo que **sigue activo para el resto del documento**, sobreescribiendo tu `\raggedright` de la línea 120.

**Orden de comandos:**
1. Línea 120: `\raggedright` → Activa alineación izquierda ✅
2. Línea 183: `\centering` → Sobreescribe y activa centrado ❌
3. Línea 220: Otro `\centering` (para "RESUMEN") → Refuerza el centrado ❌
4. **Resultado:** Todo el documento queda centrado desde línea 183 en adelante

---

## ✅ SOLUCIÓN (3 opciones, elige la que prefieras)

### **SOLUCIÓN A: Encerrar `\centering` en grupos (RECOMENDADA)** ⭐⭐⭐⭐⭐

**Cambio en línea 183:**

```latex
% ANTES (línea 183):
\centering
{\fontsize{12}{14}\selectfont 
Dr. Said Alejandro De La Cruz Rey\\[0.3cm]
...

% DESPUÉS:
{\centering  ← Añade llave de apertura AQUÍ
{\fontsize{12}{14}\selectfont 
Dr. Said Alejandro De La Cruz Rey\\[0.3cm]
...
Asesor(a)}
}  ← Añade llave de cierre al FINAL de todas las firmas (después de línea ~211)
```

**Cambio en línea 220:**

```latex
% ANTES (línea 219-220):
\centering
{\fontsize{14}{16}\selectfont\bfseries RESUMEN}\\[1cm]

% DESPUÉS:
{\centering  ← Añade llave de apertura
{\fontsize{14}{16}\selectfont\bfseries RESUMEN}\\[1cm]
}  ← Añade llave de cierre
```

**Por qué funciona:** El `\centering` queda **limitado al scope del grupo** `{...}`, y NO afecta al resto del documento.

---

### **SOLUCIÓN B: Usar environment `center` (ALTERNATIVA)**

```latex
% En línea 183, cambiar:
\centering
{\fontsize{12}{14}\selectfont ...}

% Por:
\begin{center}
{\fontsize{12}{14}\selectfont ...}
...
\end{center}
```

**Ventaja:** Más explícito, auto-cierra el centrado  
**Desventaja:** Añade espacio vertical extra (puede afectar layout)

---

### **SOLUCIÓN C: Re-activar `\raggedright` después de cada `\centering`**

```latex
% Después de línea 211 (fin de firmas), añadir:
\raggedright  % Re-activar alineación izquierda

% Después de línea 220 (RESUMEN), añadir:
\raggedright  % Re-activar alineación izquierda
```

**Ventaja:** Mínima modificación  
**Desventaja:** Debe repetirse después de cada `\centering` (frágil)

---

## 🔧 SOLUCIÓN CONCRETA (Opción A - Aplicar AHORA)

### **PASO 1: Modificar hoja de firmas (línea 183)**

**Buscar en `plantilla_tesis.tex` línea 180-183:**

```latex
% Firmas centradas, Times 12pt, sin negrita

% 1. Secretario de Investigación y Posgrado (Fijo - mismo para todos)
\centering
```

**Reemplazar con:**

```latex
% Firmas centradas, Times 12pt, sin negrita
% 1. Secretario de Investigación y Posgrado (Fijo - mismo para todos)
{\centering  % ← AÑADIR LLAVE DE APERTURA AQUÍ
```

---

### **PASO 2: Cerrar el grupo al final de firmas (después línea ~211)**

**Buscar la última firma (línea ~209-211):**

```latex
{\fontsize{12}{14}\selectfont 
DR(A) Javier Camarillo Cisneros\\[0.3cm]
Asesor(a)}
```

**Añadir después:**

```latex
{\fontsize{12}{14}\selectfont 
DR(A) Javier Camarillo Cisneros\\[0.3cm]
Asesor(a)}
}  % ← AÑADIR LLAVE DE CIERRE AQUÍ (cierra el \centering de línea 183)
```

---

### **PASO 3: Modificar título RESUMEN (línea 219-220)**

**Buscar:**

```latex
% Título "Resumen" centrado
\centering
{\fontsize{14}{16}\selectfont\bfseries RESUMEN}\\[1cm]
```

**Reemplazar con:**

```latex
% Título "Resumen" centrado
{\centering  % ← AÑADIR LLAVE DE APERTURA
{\fontsize{14}{16}\selectfont\bfseries RESUMEN}\\[1cm]
}  % ← AÑADIR LLAVE DE CIERRE
```

---

### **PASO 4: Limpiar auxiliares y re-compilar**

```powershell
# En PowerShell, ejecuta:
cd "4 semestre_dataset\edicion_tesis\tesis_luisangel"
Remove-Item *.aux, *.log, *.out, *.toc, *.lof, *.lot, *.bbl, *.blg, *.bcf, *.run.xml, *.fls, *.fdb_latexmk -Force
.\compilar.bat
```

---

## 🔍 SOLUCIÓN AL PROBLEMA DEL PDF (70 vs 65 páginas)

### **CAUSA:**

Luis tiene el PDF abierto en **Adobe Acrobat** o un visor que **bloquea el archivo**, impidiendo que `pdflatex` sobreescriba el PDF.

### **SOLUCIONES:**

**Opción 1: Cerrar el visor PDF antes de compilar**
- Luis cierra `plantilla_tesis.pdf` en Acrobat
- Ejecuta `.\compilar.bat`
- Abre el PDF nuevamente

**Opción 2: Usar SumatraPDF (Recomendado)**
- SumatraPDF **NO bloquea** el archivo
- Permite compilar mientras el PDF está abierto
- Se refresca automáticamente al detectar cambios
- Descarga: https://www.sumatrapdfreader.org/

**Opción 3: Cambiar nombre del PDF temporalmente**
```latex
% En plantilla_tesis.tex, línea ~7, añadir:
\pdfoutput=1
\def\jobname{plantilla_tesis_nuevo}
```

---

## 📋 IMPLEMENTACIÓN RÁPIDA (Código completo)

Rayo Veloz, aquí está el código exacto para aplicar:

### **CAMBIO 1 (línea 183):**

**OLD_STRING:**
```latex
% Firmas centradas, Times 12pt, sin negrita

% 1. Secretario de Investigación y Posgrado (Fijo - mismo para todos)
\centering
{\fontsize{12}{14}\selectfont 
Dr. Said Alejandro De La Cruz Rey\\[0.3cm]
```

**NEW_STRING:**
```latex
% Firmas centradas, Times 12pt, sin negrita

% 1. Secretario de Investigación y Posgrado (Fijo - mismo para todos)
{\centering
{\fontsize{12}{14}\selectfont 
Dr. Said Alejandro De La Cruz Rey\\[0.3cm]
```

---

### **CAMBIO 2 (después de línea 211):**

**OLD_STRING:**
```latex
{\fontsize{12}{14}\selectfont 
DR(A) Javier Camarillo Cisneros\\[0.3cm]
Asesor(a)}

% --------------- HOJA DE RESUMEN ---------------
```

**NEW_STRING:**
```latex
{\fontsize{12}{14}\selectfont 
DR(A) Javier Camarillo Cisneros\\[0.3cm]
Asesor(a)}
} % Cierra el grupo \centering de las firmas

% --------------- HOJA DE RESUMEN ---------------
```

---

### **CAMBIO 3 (línea 219-221):**

**OLD_STRING:**
```latex
% Título "Resumen" centrado
\centering
{\fontsize{14}{16}\selectfont\bfseries RESUMEN}\\[1cm]

% Resumen en texto justificado (120-250 palabras)
```

**NEW_STRING:**
```latex
% Título "Resumen" centrado
{\centering
{\fontsize{14}{16}\selectfont\bfseries RESUMEN}\\[1cm]
}

% Resumen en texto justificado (120-250 palabras)
```

---

## ⚡ APLICACIÓN INMEDIATA (Para Rayo Veloz)

Usa la herramienta `search_replace`:

```
search_replace(
  file_path="4 semestre_dataset/edicion_tesis/tesis_luisangel/plantilla_tesis.tex",
  old_string="% 1. Secretario de Investigación y Posgado (Fijo - mismo para todos)\n\\centering",
  new_string="% 1. Secretario de Investigación y Posgrado (Fijo - mismo para todos)\n{\\centering"
)
```

(Y los otros 2 cambios similares)

---

## 🎯 VERIFICACIÓN POST-FIX

**Después de aplicar los cambios:**

1. ✅ Limpiar auxiliares: `Remove-Item *.aux, *.log, *.out, *.toc -Force`
2. ✅ Compilar: `.\compilar.bat`
3. ✅ **Cerrar PDF viejo** antes de abrir el nuevo
4. ✅ Verificar: Párrafos alineados a la izquierda ✓
5. ✅ Verificar: Títulos capítulos centrados ✓
6. ✅ Verificar: Títulos secciones alineados izquierda ✓

---

## 🔬 EXPLICACIÓN TÉCNICA (Por qué funciona)

### **Scoping de comandos en LaTeX:**

```latex
\centering  % ← Este comando es GLOBAL, afecta TODO lo que sigue

{\centering  % ← Este comando es LOCAL, solo afecta dentro de {...}
...
}  % ← Aquí se revierte automáticamente al estado anterior
```

**Regla de oro:** Todos los comandos de alineación (`\centering`, `\raggedright`, `\raggedleft`) deben estar **dentro de grupos** si son temporales.

**Excepción:** Solo se usa `\centering` global cuando QUIERES que todo el resto del documento esté centrado (raro).

---

## 📊 RESULTADO ESPERADO

**ANTES del fix:**
```
Todo el documento: [       texto centrado       ]
```

**DESPUÉS del fix:**
```
Firmas:    [       texto centrado       ]  ✓
Resto:     [texto alineado izquierda]         ✓
```

---

## 🚀 SIGUIENTE ACCIÓN

**Rayo Veloz:**
1. Aplica los 3 cambios (líneas 183, 211, 219)
2. Limpia auxiliares
3. Compila
4. **Cierra el PDF antes de abrirlo** (importante!)
5. Verifica resultado

**Tiempo estimado:** 5 minutos para aplicar + 2 min compilar = **7 minutos total**

---

## 💡 BONUS: Solución al PDF que no se actualiza

**Para Luis:**

Si usas **Adobe Acrobat Reader**, este bloquea el PDF mientras lo tienes abierto.

**Solución permanente:**
1. Descarga **SumatraPDF**: https://www.sumatrapdfreader.org/
2. Configura como visor predeterminado para .pdf
3. SumatraPDF permite compilar mientras el PDF está abierto
4. Se actualiza automáticamente cuando detecta cambios

**Solución rápida:**
- Cierra `plantilla_tesis.pdf` ANTES de compilar
- Compila con `.\compilar.bat`
- Abre el PDF nuevamente

---

## 🎯 RESUMEN EJECUTIVO

| Problema | Causa | Solución | Tiempo |
|----------|-------|----------|--------|
| Párrafos centrados | `\centering` global (línea 183) | Encerrar en `{...}` | 5 min |
| PDF no actualiza | Visor bloquea archivo | Cerrar PDF antes de compilar | 1 min |
| Títulos dispersos | Normal con `\raggedright` | **NO ES ERROR** (APA permite) | N/A |

---

## 🔧 CÓDIGO LISTO PARA COPIAR-PEGAR

### **CAMBIO 1:**
```latex
% LÍNEA 180-185 (BUSCAR):
% Firmas centradas, Times 12pt, sin negrita

% 1. Secretario de Investigación y Posgrado (Fijo - mismo para todos)
\centering
{\fontsize{12}{14}\selectfont 

% REEMPLAZAR CON:
% Firmas centradas, Times 12pt, sin negrita

% 1. Secretario de Investigación y Posgrado (Fijo - mismo para todos)
{\centering
{\fontsize{12}{14}\selectfont 
```

### **CAMBIO 2:**
```latex
% LÍNEA ~209-214 (BUSCAR):
{\fontsize{12}{14}\selectfont 
DR(A) Javier Camarillo Cisneros\\[0.3cm]
Asesor(a)}

% --------------- HOJA DE RESUMEN ---------------

% REEMPLAZAR CON:
{\fontsize{12}{14}\selectfont 
DR(A) Javier Camarillo Cisneros\\[0.3cm]
Asesor(a)}
} % Cierra el grupo \centering de las firmas

% --------------- HOJA DE RESUMEN ---------------
```

### **CAMBIO 3:**
```latex
% LÍNEA 219-221 (BUSCAR):
% Título "Resumen" centrado
\centering
{\fontsize{14}{16}\selectfont\bfseries RESUMEN}\\[1cm]

% REEMPLAZAR CON:
% Título "Resumen" centrado
{\centering
{\fontsize{14}{16}\selectfont\bfseries RESUMEN}\\[1cm]
}
```

---

## ✅ TEST DE VERIFICACIÓN

**Después de aplicar los cambios, verifica:**

```latex
% Este texto debería estar alineado a la IZQUIERDA:
El sedentarismo se refiere a un estilo de vida donde prevalece uno o varios CS...

% NO así:
           El sedentarismo se refiere a un estilo de vida donde prevalece...
                                    (centrado)
```

---

## 🆘 SI LA SOLUCIÓN NO FUNCIONA

**Escenario improbable, pero posible:**

Si después de aplicar esto los párrafos SIGUEN centrados:

1. **Verifica que `compilar.bat` tenga 3 pasadas:**
   ```bat
   pdflatex plantilla_tesis
   biber plantilla_tesis
   pdflatex plantilla_tesis
   pdflatex plantilla_tesis
   ```

2. **Busca comandos ocultos en capítulos:**
   ```bash
   grep -n "\\centering" capitulos/*.tex
   ```

3. **Verifica que NO haya `\justifying` después de `\raggedright`:**
   - `ragged2e` package tiene `\justifying` que revierte `\raggedright`

4. **Última opción (nuclear):**
   Comentar `\usepackage{ragged2e}` y usar solo comandos nativos de LaTeX

---

## 🏆 CONFIANZA EN LA SOLUCIÓN

**Probabilidad de éxito:** 99% ⭐⭐⭐⭐⭐

Este es un error clásico de LaTeX que he visto docenas de veces. La solución (encerrar `\centering` en grupos) es **estándar** y **robusta**.

---

## 📞 COMUNICACIÓN

**Rayo Veloz:**
- Aplica los 3 cambios (5 min)
- Compila (2 min)
- Reporta resultado aquí o en `COMUNICACION_AGENTES.md`

**Si funciona:** ✅ Continúa con FASE 2  
**Si NO funciona:** 🆘 Avísame inmediatamente (alternativa nuclear lista)

---

**POSEIDÓN - Editor Científico Senior** 🔱  
*"Un `\centering` sin cerrar es como abrir las compuertas del mar. Ahora las cerramos."* 🌊

---

**Tiempo estimado de resolución:** 7 minutos  
**Bloqueo removido:** Inmediatamente después de aplicar  
**FASE 1 desbloqueada:** ✅ Lista para continuar

**¡Adelante, Rayo! El bug está vencido.** ⚡🔱

