# 📋 Registro de Cambios - Plantilla MFIPS-UACH

---

## **v1.0** - 31 de Octubre de 2025

### ✨ **Nuevas Características**

#### **Estructura Completa de Tesis**
- ✅ 9 capítulos totalmente estructurados con instrucciones detalladas
- ✅ Portada oficial UACH-MFIPS
- ✅ Hoja de firmas del comité tutorial
- ✅ Resumen ejecutivo
- ✅ Página de información del documento
- ✅ Carta al Secretario de Investigación
- ✅ Dedicatoria y agradecimientos
- ✅ Índice de contenidos automático
- ✅ Sistema de bibliografía integrado

#### **Formato APA 7ma Edición**
- ✅ Márgenes oficiales (2.5/2.5/3.0/2.5 cm)
- ✅ Times New Roman 12 pt
- ✅ Interlineado 1.5 líneas
- ✅ Sangría de párrafos 1.2 cm
- ✅ Numeración en esquina superior derecha
- ✅ 5 niveles de títulos y subtítulos configurados
- ✅ Formato de tablas APA con `booktabs`
- ✅ Formato de figuras APA con `caption`

#### **Capítulos Incluidos**

1. **01_introduccion.tex** - Introducción completa con ejemplo real
2. **02_marco_teorico_antecedentes.tex** - Plantilla detallada con cuadro comparativo
3. **03_delimitacion.tex** - Delimitación del objeto de estudio
4. **04_justificacion.tex** - Justificación con diseño metodológico
5. **05_materiales_metodos.tex** - Metodología completa (diseño, población, instrumentos, análisis, ética)
6. **06_resultados.tex** - Resultados estructurados (validación, caracterización, análisis uni/bi/multivariado, tesis)
7. **07_discusion.tex** - Discusión con dos versiones (V1 general + V2 teórica detallada)
8. **08_conclusiones.tex** - Conclusiones, recomendaciones y futuras líneas
9. **09_anexos.tex** - Anexos (consentimiento informado, instrumentos)

#### **Sistema de Referencias BibTeX**
- ✅ `referencias.bib` con ejemplos de:
  - Artículos de revista
  - Conferencias
  - Libros
  - Capítulos de libro
  - Tesis y disertaciones
  - Reportes técnicos
  - Páginas web
  - Preprints (arXiv)
  - Estándares y normas
- ✅ 15+ referencias reales incluidas (WHO, Zadeh, Doherty, Escalante, etc.)
- ✅ Formato APA con `natbib` y estilo `apalike`

#### **Herramientas de Compilación**
- ✅ `compilar.bat` - Script automático de compilación (4 pasos)
- ✅ Limpieza automática de archivos temporales

#### **Documentación**
- ✅ `NORMAS_APA_FORMATO.md` - Guía completa de normas APA 7ma edición
- ✅ `README_PLANTILLA.md` - Manual de uso paso a paso
- ✅ Instrucciones dentro de cada capítulo (comentadas)

---

## 🔍 **Detalles Técnicos**

### **Paquetes LaTeX Incluidos**
```latex
\usepackage[utf8]{inputenc}          % Codificación UTF-8
\usepackage[T1]{fontenc}             % Codificación de fuentes
\usepackage[spanish,es-tabla]{babel} % Idioma español
\usepackage{times}                   % Times New Roman
\usepackage{graphicx}                % Imágenes
\usepackage{geometry}                % Márgenes
\usepackage{setspace}                % Interlineado
\usepackage{fancyhdr}                % Encabezados y pies
\usepackage{natbib}                  % Citas y bibliografía
\usepackage{hyperref}                % Enlaces (sin recuadros)
\usepackage{ragged2e}                % Justificación de texto
\usepackage{booktabs}                % Tablas profesionales
\usepackage{longtable}               % Tablas largas
\usepackage{caption}                 % Formato de títulos
\usepackage{cleveref}                % Referencias cruzadas inteligentes
```

### **Configuración de Geometría**
```latex
\geometry{
    letterpaper,
    top=2.5cm,
    bottom=2.5cm,
    left=3.0cm,
    right=2.5cm
}
```

---

## 🎯 **Próximas Mejoras (Sugerencias)**

### **Posibles Adiciones Futuras**
- [ ] Plantilla de lista de tablas automática
- [ ] Plantilla de lista de figuras automática
- [ ] Ejemplo de apéndice con tablas
- [ ] Glosario de términos
- [ ] Lista de abreviaturas
- [ ] Más ejemplos de figuras complejas

### **Solicitudes de Usuarios**
- Reporta errores o sugerencias a tu coordinador del programa

---

## ⚠️ **Notas Importantes**

1. **Imágenes Faltantes:** La plantilla incluye referencias a imágenes de ejemplo que no existen. Esto es normal. Reemplázalas con tus propias figuras.

2. **Referencias de Ejemplo:** Las citas `\cite{autor1}`, `\cite{autor2}`, etc., son placeholders. Reemplázalas con tus referencias reales del archivo `referencias.bib`.

3. **Labels Duplicados:** Si aparecen warnings de "multiply defined labels", es porque hay capítulos duplicados (ej: Metodología aparece en cap 4 y 5). Ajusta según tu estructura.

4. **Caracteres Especiales:** Asegúrate de escapar caracteres especiales en LaTeX:
   - `_` → `\_`
   - `%` → `\%`
   - `&` → `\&`

---

## 📖 **Cómo Usar Esta Plantilla**

### **Opción 1: Empezar desde Cero**
1. Copia toda la carpeta `plantilla_mfips/`
2. Renómbrala (ej: `tesis_tu_nombre/`)
3. Edita `plantilla_tesis.tex` con tus datos personales
4. Llena cada capítulo siguiendo las instrucciones

### **Opción 2: Adaptar tu Trabajo Existente**
1. Copia el contenido de tus capítulos a los archivos `.tex`
2. Ajusta el formato según las instrucciones comentadas
3. Agrega tus referencias a `referencias.bib`
4. Compila y verifica

---

**Última actualización:** 31 de Octubre de 2025  
**Versión de LaTeX:** Compatible con MiKTeX 24.1 y TeX Live 2024

