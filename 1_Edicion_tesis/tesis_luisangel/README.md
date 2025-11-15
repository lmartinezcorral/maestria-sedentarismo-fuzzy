# 📚 PLANTILLA DE TESIS LATEX - UACH

## Facultad de Medicina y Ciencias Biomédicas · Maestría en Formación e Innovación para Profesionales de la Salud (MFIPS)

---

## 🎯 ¿Qué es esto?

Esta es una **plantilla completa de tesis en LaTeX** diseñada específicamente para estudiantes de posgrado de la UACH. 

**¡NO necesitas experiencia previa en LaTeX!** Todo está explicado paso a paso.

---

## 🚀 INICIO RÁPIDO

### 📖 Lee Primero:

1. **`RESUMEN_EJECUTIVO.md`** ← Visión general del proyecto (5 min)
2. **`README_USUARIO.md`** ← Manual completo paso a paso (30 min)
3. **`GUIA_OVERLEAF.md`** ← Si usarás Overleaf (online)

### ⚡ Para Impacientes:

**Opción A: Overleaf (Sin instalar nada)**
1. Ve a https://www.overleaf.com
2. Crea cuenta gratis
3. Sube esta carpeta completa como ZIP
4. Edita `plantilla_tesis.tex` (datos personales)
5. Clic en "Recompile"
6. ¡Listo! 🎉

**Opción B: Local en Windows**
1. Instala MiKTeX: https://miktex.org/download
2. Doble clic en `compilar.bat`
3. ¡Listo! 🎉

---

## 📁 Estructura del Proyecto

```
edicion_tesis/
│
├── 📄 plantilla_tesis.tex          ← ARCHIVO PRINCIPAL (empieza aquí)
├── 📚 referencias.bib               ← Tus referencias bibliográficas
├── ⚙️ compilar.bat                 ← Script de compilación automática
│
├── 📖 README.md                     ← Este archivo
├── 📋 RESUMEN_EJECUTIVO.md          ← Visión general (lee primero)
├── 📗 README_USUARIO.md             ← Manual completo (90+ páginas)
├── 🌐 GUIA_OVERLEAF.md              ← Guía para usar Overleaf
├── ⚡ GUIA_RAPIDA_REFERENCIA.md     ← Cheat sheet (copiar/pegar código)
│
├── 📁 capitulos/                    ← Tus capítulos (7 archivos .tex)
│   ├── 01_introduccion.tex
│   ├── 02_marco_teorico.tex         ← Con EJEMPLOS de figuras/tablas
│   ├── 03_estado_del_arte.tex
│   ├── 04_metodologia.tex
│   ├── 05_resultados.tex
│   ├── 06_discusion.tex
│   └── 07_conclusiones.tex
│
├── 📁 figuras/                      ← Guarda aquí tus imágenes
│   └── README.txt
│
└── 📁 tablas/                       ← (Opcional) Datos de tablas
```

---

## ✨ Características

### ✅ Para Principiantes
- 📚 **90+ páginas de documentación** en español
- 💡 **Ejemplos completos** en cada capítulo
- 🎓 **Sin experiencia requerida** en LaTeX
- 🌐 **Compatible con Overleaf** (online, gratis)

### ✅ Cumple Normas UACH
- ✔️ Márgenes oficiales (Izq 3cm, Der 2.5cm, etc.)
- ✔️ Interlineado 1.5
- ✔️ Portada y hoja de firmas
- ✔️ Páginas preliminares completas

### ✅ Funcionalidades Avanzadas
- 🔢 **Numeración automática** (capítulos, figuras, tablas, ecuaciones)
- 📚 **Gestión de bibliografía** (BibTeX)
- 🔗 **Referencias cruzadas** inteligentes
- 📊 **Tablas e imágenes** profesionales
- 🧮 **Ecuaciones matemáticas** completas

---

## 📖 Documentación Incluida

| Archivo                          | Contenido                           | Tiempo |
|----------------------------------|-------------------------------------|--------|
| `RESUMEN_EJECUTIVO.md`           | Visión general del proyecto         | 5 min  |
| `README_USUARIO.md`              | Manual completo paso a paso         | 30 min |
| `GUIA_OVERLEAF.md`               | Cómo usar Overleaf (online)         | 20 min |
| `GUIA_RAPIDA_REFERENCIA.md`      | Cheat sheet de comandos LaTeX       | 10 min |

**Total:** 90+ páginas de documentación 📚

---

## 🎓 ¿Para Quién?

### ✅ Ideal Para:
- Estudiantes de **Maestría** (cualquier área de Ingeniería)
- Estudiantes de **Doctorado**
- Tesis con **muchas ecuaciones matemáticas**
- Tesis con **50+ referencias bibliográficas**
- Personas que **odian los problemas de formato en Word**
- Colaboración con **asesor en tiempo real** (Overleaf)

### ⚠️ Considera Alternativas Si:
- Tu tesis es solo texto plano sin ecuaciones (Word puede ser suficiente)
- Necesitas entregar **mañana** (LaTeX tiene curva de aprendizaje de 2-3 días)
- Tu institución utiliza normas distintas a APA 7 y no deseas editarlas manualmente

---

## 💡 Ejemplos Incluidos

El archivo `capitulos/02_marco_teorico.tex` contiene ejemplos completos de:

- ✅ Cómo insertar figuras
- ✅ Cómo crear tablas profesionales
- ✅ Cómo escribir ecuaciones matemáticas
- ✅ Cómo citar referencias bibliográficas
- ✅ Cómo hacer listas (numeradas y con viñetas)
- ✅ Cómo usar referencias cruzadas

**¡Copia y adapta estos ejemplos a tu tesis!**

---

## 🔧 Requisitos

### Para Overleaf (Recomendado):
- ✅ Navegador web
- ✅ Conexión a Internet
- ❌ **NO necesitas instalar nada**

### Para Instalación Local:
- ✅ Windows 7/8/10/11
- ✅ MiKTeX (~3 GB)
- ✅ Editor LaTeX (TeXstudio recomendado)
- ✅ 4 GB RAM mínimo

---

## 🎯 Primeros Pasos (3 minutos)

1. **Elige tu método:**
   - 🌐 Overleaf (online, sin instalar) → Lee `GUIA_OVERLEAF.md`
   - 💻 Local (en tu PC) → Lee `README_USUARIO.md`

2. **Edita tus datos:**
   - Abre `plantilla_tesis.tex`
   - Busca "DATOS DEL AUTOR" (línea ~110)
   - Reemplaza `[TU NOMBRE]`, `[TÍTULO]`, etc.

3. **Escribe tu contenido:**
   - Edita archivos en `capitulos/`
   - Reemplaza texto entre `[corchetes]`

4. **Compila:**
   - Overleaf: Clic en "Recompile"
   - Local: Doble clic en `compilar.bat`

5. **¡Listo!** 🎉

---

## 📊 Comparación: Esta Plantilla vs. Empezar de Cero

| Aspecto                    | Con Esta Plantilla ✅ | Desde Cero ❌     |
|----------------------------|----------------------|-------------------|
| Tiempo de setup inicial    | 15 minutos           | 2-3 días          |
| Documentación en español   | 90+ páginas          | 0 (solo inglés)   |
| Ejemplos de código         | 7 capítulos          | 0                 |
| Formato de la facultad     | ✅ Ya incluido       | Buscar + configurar|
| Soporte                    | ✅ Contacto directo  | Solo foros        |

**Tiempo ahorrado:** 10-15 horas ⏰

---

## 🆘 ¿Necesitas Ayuda?

### Recursos Incluidos:
1. Lee `README_USUARIO.md` → Sección "Problemas Comunes"
2. Revisa `GUIA_RAPIDA_REFERENCIA.md` → Cheat sheet

### Recursos Online:
- **Overleaf Learn:** https://www.overleaf.com/learn
- **LaTeX Wikibook (ES):** https://es.wikibooks.org/wiki/Manual_de_LaTeX
- **Stack Exchange:** https://tex.stackexchange.com/
- **Detexify (buscar símbolos):** http://detexify.kirelabs.org/

### Contacto:
- **Autor:** Luis Ángel Martínez Corral
- **Email:** lmartinezcorral@uach.mx
- **Facultad:** Medicina y Ciencias Biomédicas - UACH (Programa MFIPS)

---

## 🎁 Licencia

- ✅ **Uso libre** para fines académicos
- ✅ **Modificar y compartir** libremente (mantén los créditos)
- ✅ **Sin restricciones** para estudiantes UACH
- ❌ **NO vender** (es un recurso abierto para la comunidad)

### Créditos:
Si te fue útil, agradécelo en tu tesis:

> *"Agradezco a Luis Ángel Martínez Corral por compartir la plantilla LaTeX que facilitó la escritura de este documento."*

---

## 📈 Estadísticas

- **Archivos:** 15+ (LaTeX + documentación)
- **Documentación:** 90+ páginas
- **Ejemplos:** 7 capítulos completos
- **Referencias:** 20+ entradas de ejemplo
- **Tiempo de aprendizaje:** 2-3 días para dominar lo básico
- **Tiempo ahorrado:** 10-15 horas vs. empezar de cero

---

## ✅ Checklist de Inicio

Antes de empezar a escribir:

- [ ] Leí `RESUMEN_EJECUTIVO.md` (visión general)
- [ ] Leí `README_USUARIO.md` (manual completo)
- [ ] Elegí: Overleaf o instalación local
- [ ] Configuré mi entorno (Overleaf o MiKTeX)
- [ ] Compilé la plantilla con éxito (veo el PDF)
- [ ] Edité mis datos personales
- [ ] Probé insertar una figura
- [ ] Probé crear una tabla
- [ ] Probé agregar una referencia
- [ ] Guardé respaldo (USB + nube)

---

## 🏆 Testimonios (Esperados)

> *"Esta plantilla me ahorró semanas de trabajo. Pude enfocarme en mi investigación en lugar de pelear con el formato."*  
> — Futuro estudiante de Maestría 🎓

---

## 🚀 ¡Empieza Ya!

**3 opciones según tu urgencia:**

### 🔴 **URGENTE** (1 hora disponible):
1. Lee `RESUMEN_EJECUTIVO.md` (5 min)
2. Sube a Overleaf (5 min)
3. Edita datos personales (5 min)
4. Empieza a escribir (45 min)

### 🟡 **NORMAL** (Medio día disponible):
1. Lee `README_USUARIO.md` completo (30 min)
2. Lee `GUIA_OVERLEAF.md` (20 min)
3. Configura tu entorno (30 min)
4. Practica con ejemplos (1 hora)
5. Empieza tu tesis (resto del día)

### 🟢 **ÓPTIMO** (Fin de semana completo):
1. Lee toda la documentación (2 horas)
2. Configura e instala local (1 hora)
3. Practica cada tipo de contenido (3 horas)
4. Escribe 1-2 capítulos completos (resto del tiempo)

---

## 💪 ¡Mucho Éxito con Tu Tesis!

**Recuerda:** Los primeros 2-3 días con LaTeX son los más difíciles. Después se vuelve **más rápido y fácil que Word**.

**No te rindas.** Tienes 90+ páginas de documentación para ayudarte. 📚

---

**📅 Última actualización:** Noviembre 2025  
**🔢 Versión:** 1.1  
**👤 Autor:** Luis Ángel Martínez Corral  
**🏫 Institución:** Universidad Autónoma de Chihuahua  - Facultad de Medicina y Ciencias Biomédicas
**🎓 Programa:** Maestría en Formación e Innovación para Profesionales de la Salud (MFIPS)  
**💻 Repositorio:** [maestria-sedentarismo-fuzzy](https://github.com/lmartinezcorral/maestria-sedentarismo-fuzzy)

---

**¿Listo para comenzar? → Lee `RESUMEN_EJECUTIVO.md` primero** ⏭️

