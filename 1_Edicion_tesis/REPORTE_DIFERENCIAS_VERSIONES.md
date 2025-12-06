# REPORTE DE DIFERENCIAS ENTRE VERSIONES
## Versión Revisada (15/11/2025) vs Versión Actual

**Fecha del Reporte:** 27 de noviembre de 2025  
**Commit Revisado:** `d3219eb` (15/11/2025 - "docs: actualiza README y formato cap 5")  
**Archivos Comparados:**
- `main.tex` vs `main_revisado.tex`
- `01_introduccion.tex` vs `01_introduccion_revisado.tex`
- `02_marco_teorico_antecedentes.tex` vs `02_marco_teorico_antecedentes_revisado.tex`

---

## 1. DIFERENCIAS EN `main.tex`

### 1.1. Configuración de Bibliografía

**Versión Revisada (15/11/2025):**
```latex
\usepackage[style=apa,backend=biber,natbib]{biblatex}
```

**Versión Actual:**
```latex
\usepackage{estilos_apa7}
```

**Cambio:** Centralización de configuración de biblatex en archivo de estilos personalizado (`estilos_apa7.sty`). Esto permite mantener consistencia y facilitar mantenimiento.

### 1.2. Paquetes Adicionales

**Versión Actual incluye:**
- `\usepackage{xltabular}` - Para tablas largas que se ajustan automáticamente al ancho

**Justificación:** Necesario para optimizar formato de tablas (especialmente Tabla 2.2 del Capítulo 2).

### 1.3. Fecha del Documento

**Versión Revisada:**
```latex
\newcommand{\miFecha}{27 de Octubre de 2025}
```

**Versión Actual:**
```latex
\newcommand{\miFecha}{9 de Diciembre de 2025}
```

**Cambio:** Actualización de fecha según progreso del documento.

### 1.4. Resumen (Abstract)

**Versión Revisada:**
- Resumen más detallado con métricas específicas (F1-Score=0.840, CV=4.8%)
- Menciona validación convergente con SF-36
- Incluye análisis de ablación de HRV

**Versión Actual:**
- Resumen más conciso
- F1-Score = 0.780 ± 0.167 (CV=21.4%)
- Enfoque en validación LOUO y contribución a ODS

**Cambio:** Revisión y actualización de métricas según resultados finales del análisis.

### 1.5. Dedicatoria y Agradecimientos

**Versión Revisada:**
- Plantilla vacía con placeholders (`\underline{\hspace{3cm}}`)

**Versión Actual:**
- Contenido completo y personalizado
- Dedicatoria a Dios, padres y prometida
- Agradecimientos detallados a comité tutorial, docentes y colaboradores

**Cambio:** Completado según observaciones del comité.

---

## 2. DIFERENCIAS EN `01_introduccion.tex`

### 2.1. Primera Oración - Tono y Enfoque

**Versión Revisada:**
```latex
El comportamiento sedentario (CS) se ha consolidado como uno de los principales retos de salud pública...
```

**Versión Actual:**
```latex
El Comportamiento Sedentario (CS) representa actualmente uno de los desafíos más críticos de salud pública...
```

**Cambios:**
- Capitalización: "Comportamiento Sedentario" (mayúscula inicial) vs "comportamiento sedentario"
- Tono: "representa actualmente" vs "se ha consolidado"
- Intensidad: "desafíos más críticos" vs "principales retos"

### 2.2. Citas y Referencias

**Versión Revisada:**
```latex
Este panorama, descrito por la Organización Mundial de la Salud (OMS), refleja...
\cite{WHO2020,Bull2020,Guthold2020}
```

**Versión Actual:**
```latex
Este panorama, descrito por \cite{WHO2020}, refleja...
```

**Cambios:**
- Eliminada redundancia "OMS" (ya está en la cita)
- Citas agrupadas vs individuales según observaciones del comité

### 2.3. Formato de Anglicismos

**Versión Revisada:**
```latex
como el GPAQ o el SF-36
```

**Versión Actual:**
```latex
como el Cuestionario Mundial sobre Actividad Física (\textit{GPAQ}, por sus siglas en inglés) o el Cuestionario Internacional de Actividad Física (\textit{IPAQ}, por sus siglas en inglés)
```

**Cambios:**
- Añadidas cursivas a anglicismos (`\textit{GPAQ}`, `\textit{IPAQ}`)
- Definiciones completas con siglas en inglés
- Cambio de SF-36 a IPAQ (más relevante para el contexto)

### 2.4. Eliminación de Texto Entre Paréntesis

**Versión Revisada:**
```latex
permite representar razonamientos humanos en términos lingüísticos ("actividad alta", "HRV baja", "riesgo moderado")
```

**Versión Actual:**
```latex
permite representar razonamientos humanos en términos lingüísticos
```

**Cambio:** Eliminado texto entre paréntesis según observaciones del comité.

### 2.5. Corrección de Mayúsculas

**Versión Revisada:**
```latex
calidad de vida relacionada con la salud (CVRS)
Enfermedades Crónicas No Transmisibles (ENT)
```

**Versión Actual:**
```latex
Calidad de Vida Relacionada con la Salud (CVRS)
Enfermedades Crónicas No Transmisibles (ENT)
```

**Cambio:** Corrección de mayúsculas en términos técnicos según normas académicas.

### 2.6. Eliminación de Redundancias

**Versión Revisada:**
```latex
la Organización Mundial de la Salud (OMS)
```

**Versión Actual:**
```latex
\cite{WHO2020}
```

**Cambio:** Eliminada redundancia, la cita ya contiene la información.

### 2.7. Reestructuración de Párrafo Final

**Versión Revisada:**
```latex
En suma, este proyecto articula tres dimensiones convergentes...
```

**Versión Actual:**
```latex
La urgencia de abordar el CS se evidencia en datos globales alarmantes...
Este proyecto articula tres dimensiones convergentes...
```

**Cambio:** Añadido párrafo con datos epidemiológicos específicos (muertes, costos, prevalencia en México) antes de la conclusión, mejorando el contexto y justificación.

### 2.8. Corrección de Siglas y Referencias

**Versión Revisada:**
```latex
validación cruzada Leave-One-User-Out (LOOU)
```

**Versión Actual:**
```latex
validación cruzada \textit{Leave-One-User-Out} (\textit{LOUO})
```

**Cambios:**
- Corrección: LOOU → LOUO
- Añadidas cursivas a anglicismos
- Formato consistente con otras siglas

### 2.9. Eliminación de Frases AI-Típicas

**Versión Revisada:**
```latex
En suma, este proyecto articula...
```

**Versión Actual:**
```latex
Este proyecto articula...
```

**Cambio:** Eliminada frase de cierre típica de IA ("En suma") según observaciones del Dr. David.

---

## 3. DIFERENCIAS EN `02_marco_teorico_antecedentes.tex`

### 3.1. Reorganización Estructural Mayor

**Cambios Principales:**
- **Unificación de secciones fragmentadas** sobre Comportamiento Sedentario
- **Movimiento de contenido** de "Antecedentes" a "Marco Teórico" (validación wearables, IA/ML, Lógica Difusa, Clustering, LOUO)
- **Eliminación de secciones** que contenían resultados (no apropiadas para Antecedentes)

### 3.2. Eliminación de Subtítulos Redundantes

**Versión Revisada tenía:**
- Múltiples `\subsubsection` que fragmentaban la narrativa

**Versión Actual:**
- Subtítulos eliminados, narrativa fluida en prosa
- Ejemplo: Sección "Agrupamiento No Supervisado y el Vacío Metodológico" sin subtítulos internos

### 3.3. Mejora de Narrativa - Enfoque "Why Before What"

**Versión Revisada:**
- Explicaba "qué" son los dispositivos antes de "por qué" se necesitan

**Versión Actual:**
- Reestructurado siguiendo enfoque Simon Sinek
- Primero se explica la necesidad (por qué), luego la solución (qué)

### 3.4. Añadido de Citas Faltantes

**Versión Actual incluye nuevas citas:**
- `\cite{Escalante2023}` para definición de IA
- `\cite{Vellido2020Importance}` para definición de ML
- `\cite{Zadeh1965}` para fundamento de Lógica Difusa
- `\cite{Damoun2024HRV}` para actualización de estándares HRV

**Justificación:** Cada definición técnica requiere referencia académica según normas APA 7.

### 3.5. Corrección de Términos Técnicos

**Versión Revisada:**
```latex
triaxiales
```

**Versión Actual:**
```latex
triaxales
```

**Cambio:** Corrección de término técnico.

### 3.6. Definiciones Completas de Acrónimos

**Versión Actual añade:**
- Definición completa de IEC: "Comisión Electrotécnica Internacional (IEC, por sus siglas en inglés: International Electrotechnical Commission)"
- Definición completa de PPG: "fotopletismografía óptica (PPG, por sus siglas en inglés: Photoplethysmography)"
- Definición completa de ODS: "Objetivos de Desarrollo Sostenible (ODS)"

### 3.7. Eliminación de Sección "Síntesis del Análisis Comparativo"

**Versión Revisada tenía:**
- `\subsection{Síntesis del Análisis Comparativo}` (línea ~305)

**Versión Actual:**
- Sección eliminada completamente

**Justificación:** Redundante y no aportaba valor según observaciones del comité.

### 3.8. Eliminación de Sección "Aportación Diferencial de la Investigación Actual"

**Versión Revisada tenía:**
- Sección completa con resultados y contribuciones

**Versión Actual:**
- Sección eliminada completamente

**Justificación:** Contenía resultados que pertenecen a "Discusión" o "Conclusiones", no a "Antecedentes".

### 3.9. Mejora de Sección sobre Validación LOUO

**Versión Revisada:**
- Mencionaba estudios específicos (Ricotti, Crozat, Kaveh, Lu) que pertenecen a Antecedentes

**Versión Actual:**
- Explica conceptos teóricos: split 80/20, temporal leakage, identity leakage
- Justifica por qué LOUO es estándar para datos longitudinales
- Añadidas citas: `\cite{Pedregosa2011sklearn}`, `\cite{Bassani2025DLHAR}`, `\cite{Rehman2024LOSO}`, `\cite{Mathew2024LOSO}`, `\cite{Ji2023Scratch}`, `\cite{Bolger2013}`

### 3.10. Añadido de Cursivas a Anglicismos

**Versión Actual añade cursivas consistentemente:**
- `\textit{wearables}`, `\textit{deep learning}`, `\textit{Machine Learning}`, `\textit{Random Forest}`, `\textit{Support Vector Machines}`, `\textit{Fitbit}`, `\textit{LOUO}`, `\textit{BYOD}`, `\textit{CNNs}`, `\textit{LSTM}`, `\textit{HAR}`, `\textit{gold standard}`, `\textit{MAPE}`, etc.

**Justificación:** Consistencia con normas académicas para extranjerismos.

### 3.11. Eliminación de Frases AI-Típicas

**Versión Revisada tenía:**
```latex
En síntesis, ...
```

**Versión Actual:**
- Eliminada completamente

**Justificación:** Según observaciones del Dr. David sobre estilo de redacción.

### 3.12. Corrección de Citas Duplicadas

**Versión Revisada tenía:**
- Cita duplicada para Razjouyan et al.

**Versión Actual:**
- Cita corregida y unificada

### 3.13. Renombramiento de Secciones

**Versión Revisada:**
```latex
\subsection{Clustering No Supervisado para Establecimiento de Ground Truth}
\subsection{Validación Leave-One-User-Out en Wearables}
```

**Versión Actual:**
```latex
\subsection{Agrupamiento No Supervisado y el Vacío Metodológico en Clasificación de Sedentarismo}
\subsection{Mecanismos de Validación en Estudios con Dispositivos Portátiles}
```

**Cambios:**
- Eliminados anglicismos de títulos
- Títulos más descriptivos y en español
- Enfoque en conceptos metodológicos generales

### 3.14. Actualización de Referencias HRV

**Versión Revisada:**
```latex
\cite{TaskForce1996}
```

**Versión Actual:**
```latex
\cite{Damoun2024HRV,TaskForce1996}
```

**Justificación:** Añadida referencia actualizada (2024) manteniendo la histórica (1996) para contexto.

---

## 4. RESUMEN DE CAMBIOS POR CATEGORÍA

### 4.1. Cambios de Formato y Estilo
- ✅ Unificación de citas (solo `\cite`)
- ✅ Añadido cursivas a anglicismos
- ✅ Corrección de mayúsculas/minúsculas
- ✅ Eliminación de redundancias
- ✅ Definiciones completas de acrónimos

### 4.2. Cambios Estructurales
- ✅ Reorganización Marco Teórico vs Antecedentes
- ✅ Eliminación de subtítulos redundantes
- ✅ Unificación de secciones relacionadas
- ✅ Eliminación de secciones con resultados en Antecedentes

### 4.3. Cambios de Contenido
- ✅ Añadido de citas faltantes
- ✅ Actualización de referencias (HRV 2024)
- ✅ Corrección de términos técnicos
- ✅ Mejora de narrativa (enfoque "why before what")
- ✅ Eliminación de frases AI-típicas

### 4.4. Cambios Técnicos
- ✅ Centralización de configuración biblatex
- ✅ Añadido paquete xltabular
- ✅ Actualización de fecha
- ✅ Completado dedicatoria y agradecimientos

---

## 5. IMPACTO DE LOS CAMBIOS

### 5.1. Mejoras en Formato
- Formato APA 7 más consistente
- Citas unificadas y correctamente formateadas
- Anglicismos con cursivas consistentes

### 5.2. Mejoras en Contenido
- Marco Teórico mejor estructurado y coherente
- Antecedentes enfocados exclusivamente en investigaciones previas
- Definiciones y citas completas
- Referencias actualizadas

### 5.3. Mejoras en Legibilidad
- Narrativa más fluida y lógica
- Eliminación de redundancias
- Mejor conexión entre ideas

---

## 6. ARCHIVOS PARA COMPARACIÓN

Todos los archivos revisados están disponibles en:
```
tesis_luisangel/
├── main_revisado.tex
└── capitulos/
    ├── 01_introduccion_revisado.tex
    ├── 02_marco_teorico_antecedentes_revisado.tex
    ├── 03_delimitacion_revisado.tex
    ├── 04_justificacion_revisado.tex
    ├── 05_materiales_metodos_revisado.tex
    ├── 06_resultados_revisado.tex
    ├── 07_discusion_revisado.tex
    ├── 08_conclusiones_revisado.tex
    └── 09_anexos_revisado.tex
```

---

**Nota:** Este reporte documenta las diferencias más significativas identificadas. Para una comparación línea por línea, se recomienda usar herramientas de diff (como `git diff` o comparadores visuales) entre los archivos `_revisado.tex` y los archivos actuales.

---

**Fecha del Reporte:** 27 de noviembre de 2025  
**Elaborado por:** Zeus - Agente Omnipresente  
**Estado:** ✅ Reporte completo

