# 📊 DOCUMENTO PARA CLASE DE BIOESTADÍSTICA

**Unidad Formativa:** Bioestadística  
**Asesor:** Dr. José López Loya  
**Programa:** Maestría en Formación e Innovación para Profesionales de la Salud  
**Estudiante:** LMH. Luis Angel Martínez Corral  
**Fecha:** 3 de Diciembre de 2025

---

## 📁 CONTENIDO

Este directorio contiene un documento LaTeX específico para presentación en la clase de Bioestadística, que incluye únicamente los capítulos de **Metodología** y **Resultados** de la tesis principal.

**Capítulos incluidos:**
- Capítulo 5: Materiales y Métodos
- Capítulo 6: Resultados

---

## 🔧 CÓMO COMPILAR

### **Opción 1: Usando el script de compilación (RECOMENDADO)**

```batch
cd bioestadistica
compilar.bat
```

Esto generará automáticamente el PDF con nombre:
```
bioestadistica_LAMC_DDMMYY.pdf
```

### **Opción 2: Compilación manual**

```batch
cd bioestadistica
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

---

## 📂 ESTRUCTURA DE ARCHIVOS

```
bioestadistica/
├── main.tex              # Documento principal
├── compilar.bat          # Script de compilación automática
├── README.md             # Este archivo
└── bioestadistica_LAMC_DDMMYY.pdf  # PDF generado (después de compilar)
```

**IMPORTANTE:** Los capítulos y figuras se referencian desde el directorio padre (`../capitulos/` y `../figuras/`), por lo que este documento DEBE permanecer dentro del directorio `tesis_luisangel/bioestadistica/`.

---

## ⚠️ NOTAS IMPORTANTES

1. **Referencias bibliográficas:** Se utiliza el archivo `../referencias.bib` del directorio padre
2. **Estilos:** Se utiliza `../estilos_apa7.sty` del directorio padre
3. **Figuras:** Todas las figuras se cargan desde `../figuras/`
4. **Formato:** Sigue estrictamente formato APA 7ma edición

---

## 📝 DIFERENCIAS CON DOCUMENTO PRINCIPAL

Este documento simplificado:
- ✅ Incluye SOLO Capítulos 5 y 6 (Metodología y Resultados)
- ✅ Portada adaptada para clase de Bioestadística
- ✅ Sin capítulos introductorios (1-4)
- ✅ Sin capítulos de cierre (7-8)
- ✅ Sin anexos

---

**Última actualización:** 3 de Diciembre de 2025

