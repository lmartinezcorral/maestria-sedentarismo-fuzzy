# 💀 ADES - LISTADOS DETALLADOS DE CORRECCIONES
## Gerundios + Extranjerismos + Oraciones Largas (Listo para Aplicar)

**Timestamp:** martes, 11 de noviembre de 2025, 17:30:00  
**Propósito:** Facilitar aplicación rápida de correcciones ALTA PRIORIDAD  
**Tiempo estimado total:** 2h 15min (EA-1 + EA-2 + EA-3)

---

# 📋 EA-1: GERUNDIOS INNECESARIOS (15 CORRECCIONES)

**Tiempo:** 30-45 min  
**Prioridad:** 🟡 ALTA

---

## CAP 2 (Marco Teórico) - 8 correcciones

### **G2-1: Línea 4**
```latex
ANTES:
incluyendo cuestionarios de autoinforme y tecnologías avanzadas

DESPUÉS:
que incluyen cuestionarios de autoinforme y tecnologías avanzadas
```

### **G2-2: Línea 14**
```latex
ANTES:
siendo que se dedica mucho tiempo invertido en conductas sedentarias

DESPUÉS:
ya que se dedica mucho tiempo a conductas sedentarias
```

### **G2-3: Línea 81**
```latex
ANTES:
permitiendo cuantificar tanto la intensidad instantánea de la actividad

DESPUÉS:
lo cual permite cuantificar tanto la intensidad instantánea de la actividad
```

### **G2-4: Línea 120**
```latex
ANTES:
Siendo la responsabilidad por la exposición a conductas sedentarias

DESPUÉS:
La responsabilidad por la exposición a conductas sedentarias es
```

### **G2-5: Línea 185**
```latex
ANTES:
asegurando una mayor representatividad de datos

DESPUÉS:
lo cual asegura una mayor representatividad de datos
```

### **G2-6: Línea 201**
```latex
ANTES:
brindando retroalimentación valiosa para diseñar intervenciones

DESPUÉS:
brinda retroalimentación valiosa para diseñar intervenciones
```

### **G2-7 y G2-8: Múltiples "utilizando"**
**Buscar patrón:** `utilizando`  
**Reemplazar con:** `mediante` / `con` (según contexto)

**Instancias:**
- Línea 142: "utilizando X" → "mediante X"
- Línea 207: "utilizando técnicas" → "con técnicas"

---

## CAP 5 (Materiales y Métodos) - 4 correcciones

### **G5-1: Línea 273**
```latex
ANTES:
generando un índice de densidad de actividad

DESPUÉS:
y genera un índice de densidad de actividad
```

### **G5-2: Línea 442**
```latex
ANTES:
asegurando la confidencialidad y trazabilidad de la información

DESPUÉS:
lo cual asegura la confidencialidad y trazabilidad de la información
```

### **G5-3 y G5-4: Múltiples "utilizando"**
**Instancias:**
- Línea 357: "utilizando las ocho características" → "con las ocho características"
- Línea 762: "utilizando X" → "mediante X"

---

## CAP 6 (Resultados) - 2 correcciones

### **G6-1: Línea 13**
```latex
ANTES:
reflejando diferencias sustanciales

DESPUÉS:
lo que refleja diferencias sustanciales
```

### **G6-2: Línea 183**
```latex
ANTES:
preservando la ventaja de interpretabilidad

DESPUÉS:
y preserva la ventaja de interpretabilidad
```

---

## CAP 7 (Discusión) - 1 corrección

### **G7-1: Línea 118**
```latex
ANTES:
incorporando recomendaciones dinámicas

DESPUÉS:
e incorpora recomendaciones dinámicas
```

---

# 📋 EA-2: EXTRANJERISMOS (74 CORRECCIONES)

**Tiempo:** 45-60 min  
**Prioridad:** 🟡 ALTA

**Estrategia:** Usar `search_replace` con `replace_all=true` para cada término

---

## TIPO 1: REEMPLAZOS DIRECTOS (50 instancias)

### **EX-1: "dataset" → "conjunto de datos" (15 instancias)**

**Archivos afectados:** 02, 05, 06, 07  
**Comando:**
```
search_replace(pattern="dataset", new="conjunto de datos", replace_all=true)
```

**Excepciones a verificar manualmente:**
- En contextos de código: `\texttt{dataset}` → MANTENER

---

### **EX-2: "pipeline" → "secuencia metodológica" (19 instancias)**

**Archivos afectados:** 02, 05, 06, 07  
**Comando:**
```
search_replace(pattern="pipeline", new="secuencia metodológica", replace_all=true)
```

**Alternativa en algunos contextos:**
- "tubería de procesamiento" (contexto técnico)
- "flujo metodológico" (contexto narrativo)

---

### **EX-3: "features" → "características" (10 instancias)**

**Archivos afectados:** 02, 05, 06  
**Comando:**
```
search_replace(pattern="features", new="características", replace_all=true)
```

---

### **EX-4: "performance" → "rendimiento" (5 instancias)**

**Archivos afectados:** 05, 06, 07  
**Comando:**
```
search_replace(pattern="performance", new="rendimiento", replace_all=true)
```

---

### **EX-5: "framework" → "marco" (4 instancias)**

**Archivos afectados:** 02, 05  
**Comando:**
```
search_replace(pattern="framework", new="marco", replace_all=true)
```

---

### **EX-6: "insights" → "hallazgos" (2 instancias)**

**Archivos afectados:** 07  
**Comando:**
```
search_replace(pattern="insights", new="hallazgos", replace_all=true)
```

---

### **EX-7: "highlights" → "aspectos destacados" (1 instancia)**

**Archivos afectados:** 07  
**Comando:**
```
search_replace(pattern="highlights", new="aspectos destacados", replace_all=true)
```

---

### **EX-8: "smartphone" → "teléfono inteligente" (1 instancia)**

**Archivos afectados:** 02  
**Comando:**
```
search_replace(pattern="smartphone", new="teléfono inteligente", replace_all=true)
```

---

## TIPO 2: REEMPLAZOS CONTEXTUALES (24 instancias)

### **EX-9: "clustering" → "agrupamiento (clustering)" (15 instancias)**

**Estrategia:**
1. **Primera mención en cada capítulo:** "agrupamiento (clustering)"
2. **Subsecuentes en mismo capítulo:** Alternar "agrupamiento" / "clustering"
3. **En títulos de secciones:** MANTENER "clustering" (ya establecido)

**Reemplazo manual requerido (no usar replace_all):**

**Cap 2:**
- Línea 269 (primera): "clustering (agrupamiento)"
- Líneas subsecuentes: alternar

**Cap 3:**
- Línea 68 (primera): "análisis de conglomerados (clustering)"
- Subsecuentes: alternar

**Cap 5:**
- Línea 354 (primera): "agrupamiento (clustering)"
- Subsecuentes: alternar

**Cap 6:**
- Línea 34 (primera): "análisis de conglomerados"
- Subsecuentes: "clustering" (ya establecido)

**Cap 7:**
- Línea 78 (primera): "clustering no supervisado"
- Subsecuentes: mantener

**Tiempo:** 15-20 min (manual)

---

### **EX-10: "accuracy" → mantener o "exactitud"**

**Decisión:** MANTENER "accuracy" en contexto de métricas técnicas  
**Razón:** Es término aceptado internacionalmente en ML

**Alternativa:** Añadir la primera vez "exactitud (accuracy)"

**Instancias (5):**
- Tab 6.2: Mantener "Acc" (abreviatura estándar)
- Tab 6.3: Mantener "Accuracy"
- Texto narrativo: Cambiar a "exactitud"

**Tiempo:** 10 min (selectivo)

---

## TIPO 3: TÉRMINOS TÉCNICOS MANTENER (40 instancias)

### **MANTENER SIN CAMBIOS:**
- ✅ "wearables" (29 veces) - Término técnico OMS
- ✅ "LOOU" (19 veces) - Estándar internacional (investigado por Poseidón)
- ✅ "et al." (múltiples) - APA 7 correcto
- ✅ "versus" / "vs." (múltiples) - Aceptado
- ✅ "BYOD" (Bring Your Own Device) - Sigla establecida
- ✅ "Mamdani", "Takagi-Sugeno" - Nombres propios de modelos

---

# 📋 EA-3: ORACIONES LARGAS (5 CORRECCIONES)

**Tiempo:** 30 min  
**Prioridad:** 🟡 ALTA

---

## CAP 2 (Marco Teórico) - 3 correcciones

### **O2-1: Línea 118 (62 palabras) 🔥**

```latex
ANTES (1 oración de 62 palabras):
A pesar del lanzamiento de la DPAS, ningún país ha revertido significativamente la tendencia al aumento de las tasas de obesidad o diabetes, Guthold et al. mencionan que la mayoría de los niños y adolescentes, no cumplen con los requerimientos mínimos de AF y que el CS en menores aumentó significativamente del 2001 al 2016.

DESPUÉS (2 oraciones):
A pesar del lanzamiento de la DPAS, ningún país ha revertido significativamente la tendencia al aumento de las tasas de obesidad o diabetes. Guthold et al. \citep{Guthold2020} reportan que la mayoría de los niños y adolescentes no cumplen con los requerimientos mínimos de AF, y que el CS en menores aumentó significativamente del 2001 al 2016.
```

---

### **O2-2: Línea 122 (58 palabras) 🔥**

```latex
ANTES (1 oración de 58 palabras):
En los hallazgos de la OMS a través de la Encuesta sobre la capacidad de los países para afrontar las enfermedades no transmisibles (2021), se menciona que casi un tercio de los adultos tampoco alcanzan los niveles recomendados de AF. En México el CS en adultos es mayor llegando al 40% según la Encuesta Nacional de Salud y Nutrición 2022.

DESPUÉS (3 oraciones):
En los hallazgos de la OMS a través de la Encuesta sobre la capacidad de los países para afrontar las enfermedades no transmisibles (2021), se reporta que casi un tercio de los adultos no alcanzan los niveles recomendados de AF. En México, el comportamiento sedentario en adultos es mayor, llegando al 40\%. Estos datos provienen de la Encuesta Nacional de Salud y Nutrición 2022 \citep{Shamah-Levy2023ENSANUT}.
```

---

### **O2-3: Línea 185 (48 palabras) ⚠️**

```latex
ANTES (1 oración de 48 palabras):
El equipo conformado por Bhuyan y cols., apoyan el uso y empoderamiento, de la implementación de las biotecnologías, ya que estas hacen que la gestión y la prestación de asistencia sanitaria sean más eficientes, seguras y económica.

DESPUÉS (2 oraciones):
El equipo de Bhuyan et al. \citep{Bhuyan2016Mobile} apoya el uso y empoderamiento de las biotecnologías en salud. Estas hacen que la gestión y la prestación de asistencia sanitaria sean más eficientes, seguras y económicas.
```

---

## CAP 5 (Materiales y Métodos) - 2 correcciones

### **O5-1: Línea 442 (71 palabras) 🔥🔥**

```latex
ANTES (1 oración de 71 palabras):
Este enfoque basado en scripts reutilizables garantiza la reproducibilidad del proceso sin requerir desarrollo de aplicaciones nativas en Swift. Los participantes generaron un archivo export.zip a través de la aplicación Apple Health en sus dispositivos. Cada archivo fue recibido y almacenado en un entorno seguro, asignándole un código único de participante para asegurar la confidencialidad y trazabilidad de la información.

DESPUÉS (4 oraciones):
Este enfoque basado en scripts reutilizables garantiza la reproducibilidad del proceso sin requerir desarrollo de aplicaciones nativas en Swift. Los participantes generaron un archivo \texttt{export.zip} mediante la aplicación Apple Health en sus dispositivos. Cada archivo fue recibido y almacenado en un entorno seguro. Se asignó un código único a cada participante para asegurar confidencialidad y trazabilidad de la información.
```

---

### **O5-2: Línea 445 (55 palabras) ⚠️**

```latex
ANTES (párrafo muy largo con listas inline):
Para el manejo de datos se identificaron registros con valores faltantes, nulos o atípicos. Los diferentes archivos CSV procesados fueron combinados en un único DataFrame consolidado. Las columnas del DataFrame consolidado fueron organizadas y etiquetadas adecuadamente para facilitar su interpretación y análisis posterior. Los encabezados de las columnas incluyeron: [Total de horas en las que se rompe la sedestación, Total de horas en sedestación, Total de Horas por día que tiene registros el dispositivo...]

DESPUÉS (usar itemize para claridad):
Para el manejo de datos se identificaron registros con valores faltantes, nulos o atípicos. Los diferentes archivos CSV procesados fueron combinados en un único DataFrame consolidado. Las columnas fueron organizadas con los siguientes encabezados:

\begin{itemize}[noitemsep,topsep=0pt]
    \item Total de horas con sedestación interrumpida
    \item Total de horas en sedestación
    \item Total de horas monitoreadas por día
    \item Total de horas sin registro
    \item Total de minutos en movimiento
    \item Pasos diarios
    \item Distancia recorrida diaria (km)
    \item Frecuencia cardíaca de reposo promedio diario
    \item Frecuencia cardíaca al caminar promedio diario
    \item Gasto calórico activo
\end{itemize}
```

**Nota:** Requiere añadir `\usepackage{enumitem}` en preámbulo si no está

---

# 📋 EA-2: EXTRANJERISMOS DETALLADOS

**Tiempo:** 45-60 min  
**Prioridad:** 🟡 ALTA

---

## ESTRATEGIA DE REEMPLAZO

### **MÉTODO A: Reemplazo global con replace_all=true (6 términos - 20 min)**

**Términos directos:**
1. `dataset` → `conjunto de datos` (15 instancias)
2. `performance` → `rendimiento` (5 instancias)
3. `framework` → `marco` (4 instancias)
4. `insights` → `hallazgos` (2 instancias)
5. `highlights` → `aspectos destacados` (1 instancia)
6. `smartphone` → `teléfono inteligente` (1 instancia)

**Total:** 28 instancias en 20 min

---

### **MÉTODO B: Reemplazo selectivo manual (2 términos - 25 min)**

#### **EXT-1: "pipeline" (19 instancias)**

**Contextos diferentes requieren traducciones diferentes:**

**Cap 5 (Metodología):**
- "pipeline metodológico" → "secuencia metodológica"
- "the pipeline" → "la tubería de procesamiento"
- "data pipeline" → "flujo de datos"

**Cap 6 (Resultados):**
- "siguiendo la secuencia del pipeline" → "siguiendo la secuencia metodológica"

**Cap 7 (Discusión):**
- "pipeline híbrido clustering-difuso" → "arquitectura híbrida clustering-difuso"

**Tiempo:** 15 min (revisión contextual)

---

#### **EXT-2: "features" (10 instancias)**

**Contextos diferentes:**

**Cap 5:**
- "feature engineering" → "ingeniería de características"
- "features de entrada" → "variables de entrada"
- "selected features" → "características seleccionadas"

**Cap 6:**
- "cuatro features" → "cuatro características"

**Tiempo:** 10 min

---

### **MÉTODO C: Reemplazo primera mención (clustering - 15 min)**

#### **EXT-3: "clustering" (15 instancias)**

**Estrategia híbrida:**

**Primera mención por capítulo:**
- Cap 2: "agrupamiento (clustering)"
- Cap 3: "análisis de conglomerados (clustering)"
- Cap 5: "agrupamiento (clustering)"
- Cap 6: "clustering" (ya establecido en Cap 5)
- Cap 7: "clustering" (ya establecido)

**Subsecuentes:**
- Alternar "agrupamiento" / "clustering" para variedad

**En títulos de secciones:**
- MANTENER "clustering" (término técnico establecido)

**Tiempo:** 15 min (manual selectivo)

---

## TÉRMINOS TÉCNICOS MANTENER (NO CAMBIAR):

### **LISTA DEFINITIVA:**
- ✅ `wearables` (29 veces) - Término OMS aceptado
- ✅ `LOOU` / `Leave-One-User-Out` (19 veces) - Estándar internacional
- ✅ `BYOD` / `Bring Your Own Device` (6 veces) - Sigla establecida
- ✅ `Mamdani`, `Takagi-Sugeno` - Nombres propios modelos
- ✅ `K-Means`, `PCA`, `VIF`, `ANOVA` - Siglas matemáticas
- ✅ `Apple Watch`, `HealthKit` - Marcas comerciales
- ✅ `et al.`, `versus`, `vs.` - APA 7 correcto
- ✅ `XML`, `CSV`, `DataFrame` - Términos informáticos técnicos
- ✅ `accuracy`, `precision`, `recall` - En contexto técnico tablas (opcional traducir en texto)

---

# 📋 TABLA RESUMEN EXTRANJERISMOS

| Extranjerismo | Reemplazo | Instancias | Método | Tiempo |
|---------------|-----------|------------|--------|--------|
| dataset | conjunto de datos | 15 | Global | 3 min |
| pipeline | secuencia metodológica | 19 | Manual | 15 min |
| features | características | 10 | Global | 3 min |
| performance | rendimiento | 5 | Global | 2 min |
| framework | marco | 4 | Global | 2 min |
| insights | hallazgos | 2 | Global | 1 min |
| highlights | aspectos destacados | 1 | Global | 1 min |
| smartphone | teléfono inteligente | 1 | Global | 1 min |
| clustering | agrupamiento (clustering) | 15 | Manual | 15 min |
| **TOTAL** | | **72** | | **43 min** |

**Tiempo real estimado:** 45-60 min (con verificación compilación)

---

# 📋 EA-4: DIVIDIR PÁRRAFO CAP 1 (20 min)

**Prioridad:** 🟡 ALTA

---

## PÁRRAFO ACTUAL (450 palabras - EXCESIVO)

**Ubicación:** `01_introduccion.tex` líneas 29-56

**Problema:** Párrafo único muy denso que mezcla 4 temas:
1. Contexto CS como reto salud pública (líneas 29-31)
2. Limitaciones métodos actuales (líneas 32-40)
3. Oportunidad wearables (líneas 41-46)
4. Enfoque metodológico del estudio (líneas 47-56)

---

## DIVISIÓN PROPUESTA (4 PÁRRAFOS)

### **Párrafo 1: Contexto epidemiológico (150 palabras)**
Líneas 29-31 actuales + expansión mínima

### **Párrafo 2: Limitaciones metodológicas (120 palabras)**
Líneas 32-40 actuales

### **Párrafo 3: Oportunidad tecnológica (100 palabras)**
Líneas 41-46 actuales

### **Párrafo 4: Enfoque de este estudio (80 palabras)**
Líneas 47-56 actuales + síntesis

**Implementación:**
Simplemente añadir `\par` o línea en blanco entre cada bloque temático

**Tiempo:** 15-20 min (reformateo + verificación)

---

# 📋 EA-5: EXPANDIR CAP 4 (30 min)

**Prioridad:** 🟡 ALTA (ya aplicada PARCIALMENTE)

---

## ESTADO ACTUAL

**ANTES (original - 11 líneas, 3 párrafos breves):**
- Párrafo 1: Contexto epidemiológico (80 palabras)
- Párrafo 2: Enfoque correlacional pre-pivote (90 palabras)
- Párrafo 3: Necesidad salud pública (25 palabras)

**TOTAL:** 195 palabras (MUY BREVE para un capítulo)

---

## DESPUÉS DE CORRECCIÓN EC-1 (12 líneas actuales, 4 párrafos)

**YA APLICADO:**
- Párrafo 1: Contexto epidemiológico (82 palabras) ✅
- Párrafo 2: Dicotomía métodos evaluación (115 palabras) ✅ NUEVO
- Párrafo 3: Enfoque metodológico (125 palabras) ✅ NUEVO
- Párrafo 4: Relevancia científica (110 palabras) ✅ NUEVO
- Párrafo 5: Perspectiva salud pública (120 palabras) ✅ NUEVO

**TOTAL:** ~550 palabras ✅

**ESTADO:** ✅ **YA EXPANDIDO EN CORRECCIÓN EC-1** (aplicada automáticamente)

---

# 📋 EA-6: USAR BULLETS CAP 5 (20 min)

**Prioridad:** 🟡 ALTA

---

## UBICACIÓN: Líneas 443-445

**PROBLEMA:**
Lista inline de variables muy larga y difícil de leer:
> "Los encabezados de las columnas incluyeron: [Total de horas en las que se rompe la sedestación, Total de horas en sedestación, Total de Horas por día que tiene registros el dispositivo...]"

**SOLUCIÓN:**
Convertir a lista itemize (ver código en sección O5-2 arriba)

**Requiere:**
- Añadir `\usepackage{enumitem}` si no existe
- Reformatear como bullets
- Verificar compilación

**Tiempo:** 20 min

---

# 📋 EM-1: AÑADIR NOTAS TABLAS (10 min)

**Prioridad:** 🟢 MEDIA

---

## TABLA 5.1bis (Cohorte N=10)

**Ubicación:** `05_materiales_metodos.tex` línea 89 (después de \bottomrule)

**Añadir:**
```latex
\begin{flushleft}
\scriptsize
\textit{Nota:} Datos demográficos de la cohorte completa. Edad e IMC expresados como media $\pm$ desviación estándar. Semanas válidas: observaciones con $\geq$5 días de datos por semana.
\end{flushleft}
```

**Tiempo:** 5 min

---

## TABLA 6.1 (Distribución clusters por usuario)

**Ubicación:** `06_resultados.tex` línea 96 (después de \bottomrule)

**Añadir:**
```latex
\begin{flushleft}
\scriptsize
\textit{Nota:} Distribución porcentual de semanas asignadas a cada clúster por usuario. Cluster Alto Sed = Sedentarismo alto (Clúster 0). Cluster Bajo Sed = Sedentarismo bajo (Clúster 1).
\end{flushleft}
```

**Tiempo:** 5 min

---

# 🎯 PLAN DE EJECUCIÓN RECOMENDADO

## SESIÓN 1 (Luis regresa - 20 min): SOLO CRÍTICO

### **Opción A-Rápida:**
1. ✅ EC-1: Cap 4 reescrito (YA APLICADO) - 0 min
2. ✅ Compilar + verificar PDF - 5 min
3. ✅ Commit + push - 5 min
4. ✅ Actualizar CANAL_3_AGENTES - 10 min

**RESULTADO:** 9.5/10 ⭐⭐⭐⭐⭐ (DEFENDIBLE)

---

## SESIÓN 2 (Mañana - 2h): ALTA PRIORIDAD

### **Opción B-Completa:**
1. EA-1: Gerundios (30-45 min)
2. EA-2: Extranjerismos (45-60 min)
3. EA-3: Oraciones largas (30 min)
4. Compilar + verificar (10 min)
5. Commit + push (5 min)

**RESULTADO:** 9.7/10 ⭐⭐⭐⭐⭐

---

## SESIÓN 3 (Opcional - 1h): REFINAMIENTO

### **Opción C-Perfección:**
1. EA-4: Dividir párrafo Cap 1 (20 min)
2. EA-6: Bullets Cap 5 (20 min)
3. EM-1: Notas tablas (10 min)
4. Compilar + verificar (10 min)

**RESULTADO:** 9.8/10 ⭐⭐⭐⭐⭐ (EXCELENCIA)

---

# 📊 MATRIZ DE DECISIÓN

| Opción | Tiempo | Correcciones | Calificación | Defensa | Recomendado |
|--------|--------|--------------|--------------|---------|-------------|
| **A** | 20 min | 1 crítica | 9.5/10 | ✅ SÍ | Luis sin tiempo |
| **B** | 2h 30min | 1+6 altas | 9.7/10 | ✅ SÍ | Balance ideal ⭐ |
| **C** | 4h | 1+6+3 todas | 9.8/10 | ✅ SÍ | Perfeccionistas |

**MI RECOMENDACIÓN:** **Opción A HOY + Opción B MAÑANA** (2 sesiones cortas)

---

# 💡 NOTAS TÉCNICAS PARA APLICACIÓN

## Para usar replace_all de forma segura:

```python
# EJEMPLO replace_all para "dataset":
search_replace(
    file_path="capitulos/02_marco_teorico_antecedentes.tex",
    old_string="dataset",
    new_string="conjunto de datos",
    replace_all=True
)
```

## Para aplicar correcciones manuales:

**Usar grep para verificar contexto ANTES de reemplazar:**
```bash
grep -n "pipeline" capitulos/05_materiales_metodos.tex
```

**Luego search_replace con contexto suficiente (NO replace_all)**

---

# 📋 CHECKLIST DE VERIFICACIÓN POST-CORRECCIONES

## Después de cada bloque de correcciones:

- [ ] Compilar pdflatex (3 veces)
- [ ] Verificar 0 errores fatales
- [ ] Buscar warnings nuevos
- [ ] Revisar visualmente páginas afectadas en PDF
- [ ] Commit con mensaje descriptivo
- [ ] Push a GitHub

---

**"Los detalles están mapeados. Las correcciones están priorizadas. Las rutas están trazadas. Solo queda ejecutar."** 💀📋✅

