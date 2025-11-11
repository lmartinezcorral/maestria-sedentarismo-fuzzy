# Plan de Integración DOCX → LaTeX
**Fecha:** 30 de Octubre de 2025  
**Estado:** Iniciando enfoque manual controlado

---

## ✅ Estado Actual

### Rama Master (Restaurada al commit 98a27c2)
- ✅ Portada, firmas, resumen, carta: **PERFECTOS, NO MODIFICAR**
- ✅ Dedicatoria y agradecimientos: **OK**
- ✅ Índice de contenidos: **OK**
- ✅ Introducción: **COMPLETA Y CORRECTA**
- ✅ Sistema de compilación: **FUNCIONANDO**
- ✅ Referencias bibliográficas: **INTEGRADAS (13 refs iniciales)**

### Rama de Respaldo (`respaldo_extraccion_docx`)
- Contiene extracción automática (con errores)
- Scripts de conversión disponibles para referencia
- Documento DOCX recuperado

---

## 📋 Estructura Correcta de Capítulos

| # | Capítulo | Archivo | Estado |
|---|----------|---------|--------|
| - | Introducción | `01_introduccion.tex` | ✅ **COMPLETO** |
| 2 | Marco Teórico y Antecedentes | `02_marco_teorico.tex` | ⚠️ Pendiente extraer del DOCX |
| 3 | Delimitación del Objeto de Estudio | `03_delimitacion.tex` | ❌ **FALTA CREAR** |
| 4 | Justificación | `04_justificacion.tex` | ❌ **FALTA CREAR** |
| 5 | Materiales y Métodos | `05_materiales_metodos.tex` | ⚠️ Pendiente extraer del DOCX |
| 6 | Resultados | `06_resultados.tex` | ⚠️ Pendiente extraer del DOCX |
| 7 | Discusión | `07_discusion.tex` | ⚠️ Pendiente extraer del DOCX |
| 8 | Conclusiones | `08_conclusiones.tex` | ⚠️ Pendiente extraer del DOCX |
| - | Referencias | `referencias.bib` | ⚠️ Añadir las 348 refs del DOCX |
| - | Anexos | `09_anexos.tex` | ❌ **FALTA CREAR** |

---

## 🔧 Problemas Identificados en Plantilla Vacía

### Archivos Duplicados/Incorrectos
```
❌ 03_estado_del_arte.tex      → Debe fusionarse con 02_marco_teorico.tex
❌ 04_metodologia.tex          → Es "Justificación", no metodología
❌ 05_materiales_metodos.tex   → Archivo correcto pero nombre confuso
❌ 05_resultados.tex           → Número duplicado con materiales
❌ 06_resultados.tex           → Duplicado de resultados
❌ 06_discusion.tex            → Número duplicado
❌ 07_discusion.tex            → Duplicado de discusión
❌ 07_conclusiones.tex         → Número duplicado
❌ 08_conclusiones.tex         → Duplicado de conclusiones
```

---

## 🎯 Estrategia de Trabajo

### Enfoque Manual Controlado (NO automático)

#### Fase 1: Corrección de Estructura de Plantillas ✅
1. ✅ Recuperar DOCX desde rama de respaldo
2. ⬜ Renombrar/reorganizar archivos de plantilla
3. ⬜ Actualizar `plantilla_tesis.tex` con estructura correcta

#### Fase 2: Extracción Manual del Contenido
**Método:** Leer secciones del DOCX y copiar/formatear manualmente

Para cada capítulo:
1. Leer sección correspondiente del DOCX
2. Identificar títulos, secciones, subsecciones
3. Copiar contenido con formato correcto
4. Escapar caracteres especiales LaTeX manualmente
5. Añadir `\cite{}` para referencias
6. Compilar y verificar

#### Fase 3: Referencias Bibliográficas
1. Extraer todas las referencias del DOCX
2. Convertir a formato BibTeX
3. Integrar con las 13 referencias ya existentes
4. Verificar formato APA

---

## 📝 Próximos Pasos Inmediatos

### 1. Reorganizar Estructura de Archivos

**Renombrar archivos en `tesis_luisangel/capitulos/`:**
```
02_marco_teorico.tex           → [MANTENER, expandir con DOCX]
03_estado_del_arte.tex         → [ELIMINAR, fusionar con cap 2]
04_metodologia.tex             → 04_justificacion.tex
05_materiales_metodos.tex      → 05_materiales_metodos.tex [OK]
05_resultados.tex              → [ELIMINAR, duplicado]
06_resultados.tex              → 06_resultados.tex
06_discusion.tex               → [ELIMINAR, duplicado]
07_discusion.tex               → 07_discusion.tex
07_conclusiones.tex            → [ELIMINAR, duplicado]
08_conclusiones.tex            → 08_conclusiones.tex

[CREAR NUEVOS]
03_delimitacion.tex            → Nuevo capítulo
09_anexos.tex                  → Nuevo capítulo
```

### 2. Actualizar `plantilla_tesis.tex`

```latex
\include{capitulos/01_introduccion}      % ✅ COMPLETO
\include{capitulos/02_marco_teorico}     % ⚠️ Expandir con DOCX
\include{capitulos/03_delimitacion}      % ❌ CREAR
\include{capitulos/04_justificacion}     % ❌ CREAR
\include{capitulos/05_materiales_metodos}% ⚠️ Extraer del DOCX
\include{capitulos/06_resultados}        % ⚠️ Extraer del DOCX
\include{capitulos/07_discusion}         % ⚠️ Extraer del DOCX
\include{capitulos/08_conclusiones}      % ⚠️ Extraer del DOCX
```

### 3. Método de Extracción

**Para cada capítulo del DOCX:**
1. Usar `python-docx` para leer párrafos
2. Identificar secciones por formato (negritas, tamaño)
3. Aplicar formato LaTeX correcto
4. Copiar a archivo `.tex` correspondiente
5. Compilar y verificar errores

---

## ⚠️ Lecciones Aprendidas

### Lo que NO funcionó:
- ❌ Extracción automática masiva genera errores difíciles de corregir
- ❌ Caracteres especiales no se escapan correctamente
- ❌ Estructura de secciones se pierde
- ❌ Referencias se extraen incompletas

### Lo que SÍ funciona:
- ✅ Enfoque manual controlado capítulo por capítulo
- ✅ Verificación de compilación después de cada capítulo
- ✅ Mantener estructura de archivos clara y simple
- ✅ No sobrescribir archivos que ya estaban correctos

---

## 📊 Progreso Esperado

**Tiempo estimado por capítulo:** 15-30 minutos
**Total capítulos pendientes:** 7
**Tiempo total estimado:** 2-4 horas

---

*Iniciado: 30 de Octubre de 2025, 19:00*

