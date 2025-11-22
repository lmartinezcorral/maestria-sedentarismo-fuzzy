# 📝 ANGLICISMOS Y EXTRANJERISMOS APLICADOS CON CURSIVA EN LA TESIS

**Fecha de aplicación:** 2025-11-22  
**Total de cambios aplicados:** 533 correcciones  
**Archivos procesados:** 11 archivos LaTeX

---

## ✅ RESUMEN DE CORRECCIONES APLICADAS

Se aplicó formato de cursiva (`\textit{}`) a los siguientes anglicismos y extranjerismos en todos los archivos LaTeX de la tesis:

### Dispositivos y Tecnologías
- **Apple Watch** → `\textit{Apple Watch}`
- **HealthKit** → `\textit{HealthKit}`
- **wearables / wearable** → `\textit{wearables}` / `\textit{wearable}`
- **BYOD** → `\textit{BYOD}`
- **GPS** → `\textit{GPS}`
- **PPG** → `\textit{PPG}`
- **LED** → `\textit{LED}`
- **SDK** → `\textit{SDK}`
- **API** → `\textit{API}`

### Métricas y Siglas Técnicas
- **HRV-SDNN / HRV_SDNN** → `\textit{HRV-SDNN}`
- **HRV** → `\textit{HRV}`
- **SDNN** → `\textit{SDNN}`
- **LOUO** → `\textit{LOUO}`
- **LOOU** → `\textit{LOOU}`
- **F1-Score / F1 Score** → `\textit{F1-Score}`
- **Recall** → `\textit{Recall}`
- **Precision** → `\textit{Precision}`
- **Accuracy** → `\textit{Accuracy}`
- **MCC** → `\textit{MCC}`
- **IQR** → `\textit{IQR}`
- **MET** → `\textit{MET}`
- **SpO2** → `\textit{SpO\textsubscript{2}}`
- **VO2** → `\textit{VO\textsubscript{2}}`
- **FCmax** → `\textit{FC\textsubscript{max}}`
- **FCmáx** → `\textit{FC\textsubscript{máx}}`

### Métodos y Algoritmos
- **K-Means / K Means** → `\textit{K-Means}`
- **clustering** → `\textit{clustering}`
- **fuzzy** → `\textit{fuzzy}`
- **Mamdani** → `\textit{Mamdani}`
- **Big data** → `\textit{Big data}`
- **World Wide Web** → `\textit{World Wide Web}`
- **internet** → `\textit{internet}`

### Lenguajes y Herramientas de Programación
- **Python** → `\textit{Python}`
- **Swift** → `\textit{Swift}`
- **pandas** → `\textit{pandas}`
- **numpy** → `\textit{numpy}`
- **pytz** → `\textit{pytz}`
- **GitHub** → `\textit{GitHub}`
- **DataFrame** → `\textit{DataFrame}`
- **CSV** → `\textit{CSV}`
- **XML** → `\textit{XML}`

### Términos Generales
- **et al.** → `\textit{et al.}`
- **output** → `\textit{output}`
- **input** → `\textit{input}`
- **feedback** → `\textit{feedback}`
- **baseline** → `\textit{baseline}`
- **software** → `\textit{software}`
- **hardware** → `\textit{hardware}`
- **dataset** → `\textit{dataset}`

---

## 📊 DISTRIBUCIÓN DE CAMBIOS POR ARCHIVO

| Archivo | Cambios Aplicados |
|---------|-------------------|
| `01_introduccion.tex` | 10 |
| `02_marco_teorico_antecedentes.tex` | 135 |
| `03_delimitacion.tex` | 29 |
| `04_justificacion.tex` | 10 |
| `05_materiales_metodos.tex` | 110 |
| `06_resultados.tex` | 48 |
| `07_discusion.tex` | 92 |
| `08_conclusiones.tex` | 2 |
| `09_anexos.tex` | 65 |
| `seccion_5_8_CORREGIDA_TRIANGULARES.tex` | 4 |
| `main.tex` | 28 |
| **TOTAL** | **533** |

---

## ⚠️ NOTAS IMPORTANTES

### Excepciones Aplicadas

Los siguientes contextos **NO** fueron modificados (correctamente):

1. **Comandos LaTeX**: Anglicismos dentro de `\cite{}`, `\citep{}`, `\citet{}`, `\path{}`, `\texttt{}`, etc.
2. **Ya en cursiva**: Términos que ya estaban dentro de `\textit{}` o `\textit{}` previo.
3. **Comentarios**: Líneas que comienzan con `%`.
4. **Etiquetas y referencias**: Dentro de `\label{}`, `\ref{}`, `\Cref{}`, etc.

### Caso Especial: "et al." en Citas

**Pregunta:** ¿Cómo aplicar cursiva a "et al." en las citas cuando se usa sistema de referencias LaTeX?

**Respuesta:**

En LaTeX, cuando usas `\cite{}`, el sistema de referencias (BibTeX/Biblatex) maneja automáticamente "et al." según el estilo de citación configurado (por ejemplo, APA 7). **No necesitas aplicar cursiva manualmente** dentro de `\cite{}` porque el estilo lo controla.

Sin embargo, si "et al." aparece **en el texto del párrafo** (no dentro de `\cite{}`), sí debe ir en cursiva:

- ✅ **Correcto en cita automática:**
  ```latex
  Según Smith et al. \cite{Smith2020}, el método...
  ```
  (LaTeX manejará "et al." según el estilo)

- ✅ **Correcto en texto:**
  ```latex
  Varios autores (\textit{et al.}, 2020) han reportado...
  ```

- ✅ **Correcto en tablas/anexos (manual):**
  ```latex
  Smith \textit{et al.} (2020) \cite{Smith2020}
  ```

En el archivo `09_anexos.tex`, las citas ya tienen `\textit{et al.}` aplicado manualmente, lo cual es correcto para tablas donde se muestra el formato de citación explícitamente.

---

## 🔍 VERIFICACIÓN POST-APLICACIÓN

Después de aplicar las correcciones, se realizó una segunda búsqueda que identificó:
- **835 ocurrencias restantes** (muchas son falsos positivos del script de búsqueda, como "ent" dentro de "presente", "met" dentro de "método", etc.)
- **67 tipos únicos** de posibles anglicismos adicionales

**Recomendación:** Revisar manualmente los casos específicos que puedan requerir atención adicional, especialmente:
- Siglas que pueden ser anglicismos o acrónimos en español
- Términos técnicos que pueden tener traducción al español
- Nombres propios de marcas o productos

---

## 📝 METODOLOGÍA APLICADA

1. **Primera pasada**: Script automatizado aplicó cursiva a 533 ocurrencias de anglicismos identificados.
2. **Corrección**: Se corrigieron las dobles barras invertidas (`\\textit{}` → `\textit{}`).
3. **Verificación**: Segunda búsqueda para identificar posibles casos faltantes.

---

**Generado por:** Script `aplicar_cursiva_mejorado.py` y `corregir_dobles_barras.py`  
**Fecha:** 2025-11-22

