# 📚 Verificador de Referencias Bibliográficas

Script automatizado para verificar la indexación de referencias bibliográficas en múltiples bases de datos académicas.

---

## 🎯 ¿Qué hace este script?

Este script verifica si las referencias de tu archivo `.bib` están indexadas en las siguientes bases de datos académicas:

- ✅ **ScienceDirect** (Elsevier)
- ✅ **PubMed** (NCBI - Ciencias biomédicas)
- ✅ **IEEE Xplore** (Ingeniería/Tecnología)
- ✅ **ACM Digital Library** (Ciencias de la computación)
- ✅ **Google Scholar** (Búsqueda general)
- ✅ **SpringerLink** (Editorial Springer)
- ✅ **Wiley Online Library** (Editorial Wiley)
- ✅ **Crossref** (Metadatos DOI)

---

## 📋 Requisitos Previos

### 1. Python 3.6 o superior

**Verificar si Python está instalado:**
```bash
python --version
```

**Si no está instalado:**
- Descarga Python desde: https://www.python.org/downloads/
- ⚠️ **IMPORTANTE:** Durante la instalación, marca la opción **"Add Python to PATH"**

### 2. Archivo `referencias.bib`

El archivo debe estar en la misma carpeta que el script.

---

## 🚀 Uso Rápido (Windows)

### Opción 1: Doble clic (Más fácil)

1. **Coloca tu archivo `referencias.bib`** en la misma carpeta que `verificar_referencias.bat`
2. **Haz doble clic** en `verificar_referencias.bat`
3. Espera a que termine (puede tardar varios minutos)
4. Abre el archivo `referencias_multiple_bases_datos.csv` con Excel

### Opción 2: Línea de comandos

```bash
# Abre PowerShell o CMD en la carpeta del proyecto
verificar_referencias.bat
```

---

## 🐍 Uso Manual (Windows/Mac/Linux)

### 1. Instalar dependencias

```bash
pip install requests
```

### 2. Ejecutar el script

```bash
python verificar_multiple_bases_datos.py
```

---

## 📊 Archivos Generados

Después de ejecutar el script, se generan dos archivos:

### 1. `referencias_multiple_bases_datos.csv`

Tabla con los siguientes campos:

| Columna | Descripción |
|---------|-------------|
| `key` | Clave de la referencia en el .bib |
| `title` | Título del artículo |
| `author` | Autores |
| `journal` | Revista |
| `year` | Año de publicación |
| `doi` | DOI (si existe) |
| `total_databases` | Número de bases de datos donde está indexada |
| `{database}_indexed` | `True`/`False` si está en esa base |
| `{database}_url` | URL de búsqueda o del artículo |
| `{database}_method` | Método usado (doi_search, title_search, etc.) |
| `crossref_publisher` | Editorial según Crossref |

### 2. `referencias_multiple_bases_datos.json`

Mismos datos en formato JSON (útil para procesamiento automatizado).

---

## 📈 Interpretación de Resultados

### Ejemplo de fila en el CSV:

```csv
key,title,doi,pubmed_indexed,pubmed_url,ieee_indexed,...
Bull2020,WHO Guidelines...,10.1136/bjsports-2020-102955,True,https://pubmed...,False,...
```

### Significado:

- **`pubmed_indexed = True`**: El artículo está indexado en PubMed
- **`pubmed_url`**: Enlace directo para ver el artículo en PubMed
- **`total_databases = 4`**: El artículo está en 4 de las 8 bases de datos verificadas

---

## ⏱️ Tiempo de Ejecución

- **~50 referencias**: 2-3 minutos
- **~100 referencias**: 5-7 minutos
- **~150 referencias**: 10-15 minutos

El tiempo depende de:
- Número de referencias
- Velocidad de tu conexión a internet
- Carga de los servidores de las bases de datos

---

## ❓ Preguntas Frecuentes (FAQ)

### ¿Por qué algunas referencias no aparecen en ninguna base de datos?

**Posibles razones:**
1. **No tienen DOI**: Las búsquedas por título son menos precisas
2. **Son documentos técnicos/informes**: No están en bases de datos académicas
3. **Son muy recientes**: Pueden no estar indexadas aún
4. **Son de editoriales pequeñas**: Pueden no estar en las bases verificadas

### ¿Por qué Google Scholar encuentra todo?

Google Scholar tiene una cobertura muy amplia (incluye preprints, tesis, etc.), pero no es una base de datos "oficial" como PubMed o ScienceDirect.

### ¿Qué hacer si una referencia no aparece?

1. **Verifica el DOI**: Usa https://doi.org/ para validar
2. **Busca manualmente**: En la base de datos más relevante para tu área
3. **Revisa el título**: Puede haber errores de tipeo en el .bib

### ¿Puedo verificar solo ScienceDirect?

Sí, usa el script alternativo:
```bash
python verificar_sciencedirect.py
```

---

## 🔧 Solución de Problemas

### Error: "Python no está instalado"

**Solución:**
1. Instala Python desde https://www.python.org/downloads/
2. Durante la instalación, marca **"Add Python to PATH"**
3. Reinicia la terminal/CMD

### Error: "No se encontró el archivo referencias.bib"

**Solución:**
- Asegúrate de que el archivo `referencias.bib` esté en la misma carpeta que el script
- Verifica que el nombre del archivo sea exactamente `referencias.bib` (sin espacios adicionales)

### Error: "No se pudo instalar requests"

**Solución manual:**
```bash
pip install requests
```

Si no funciona, prueba:
```bash
python -m pip install requests
```

### El script se detiene o da errores de conexión

**Posibles causas:**
- Conexión a internet lenta o intermitente
- Los servidores de las bases de datos están sobrecargados
- Firewall bloqueando las peticiones

**Solución:**
- Espera unos minutos y vuelve a ejecutar
- Verifica tu conexión a internet
- Ejecuta el script en un horario con menos tráfico

---

## 📝 Formato del Archivo .bib

El script espera un archivo BibTeX estándar. Ejemplo:

```bibtex
@article{Bull2020,
  author = {Bull, Fiona C. and Al-Ansari, Salih S.},
  title = {World Health Organization 2020 guidelines on physical activity},
  journal = {British Journal of Sports Medicine},
  year = {2020},
  doi = {10.1136/bjsports-2020-102955}
}
```

**Campos importantes:**
- `title`: Título del artículo
- `author`: Autores
- `doi`: DOI (muy recomendado para búsquedas precisas)
- `journal`: Nombre de la revista
- `year`: Año de publicación

---

## 📚 Bases de Datos Verificadas

### ScienceDirect
- **Enfoque**: Ciencias, medicina, ingeniería
- **Editorial**: Elsevier
- **Relevancia**: ⭐⭐⭐⭐

### PubMed
- **Enfoque**: Ciencias biomédicas
- **Editorial**: National Library of Medicine
- **Relevancia**: ⭐⭐⭐⭐⭐ (para salud pública)

### IEEE Xplore
- **Enfoque**: Ingeniería, tecnología
- **Editorial**: IEEE
- **Relevancia**: ⭐⭐⭐⭐ (para wearables, sensores)

### ACM Digital Library
- **Enfoque**: Ciencias de la computación
- **Editorial**: ACM
- **Relevancia**: ⭐⭐⭐ (para machine learning)

### Google Scholar
- **Enfoque**: General (todas las disciplinas)
- **Editorial**: Google
- **Relevancia**: ⭐⭐⭐⭐⭐ (búsqueda amplia)

### SpringerLink
- **Enfoque**: Ciencias, medicina, ingeniería
- **Editorial**: Springer Nature
- **Relevancia**: ⭐⭐⭐

### Wiley Online Library
- **Enfoque**: Ciencias, medicina
- **Editorial**: John Wiley & Sons
- **Relevancia**: ⭐⭐⭐

### Crossref
- **Enfoque**: Metadatos DOI
- **Editorial**: Crossref (sin fines de lucro)
- **Relevancia**: ⭐⭐⭐⭐⭐ (verificación de DOIs)

---

## 📊 Estadísticas Esperadas

Para un archivo típico con ~150 referencias:

- **Google Scholar**: ~100% (muy amplio)
- **SpringerLink**: ~70-80%
- **Crossref**: ~65-75%
- **PubMed**: ~40-50% (si es área de salud)
- **ScienceDirect**: ~10-15% (solo Elsevier)

---

## 🔄 Actualizaciones y Mejoras

### Versión Actual: 1.0

**Características:**
- ✅ Verificación en 8 bases de datos
- ✅ Exportación a CSV y JSON
- ✅ Estadísticas por base de datos
- ✅ Script .bat para Windows

### Mejoras Futuras:
- [ ] Verificación en Scopus (requiere API key)
- [ ] Verificación en Web of Science (requiere suscripción)
- [ ] Interfaz gráfica (GUI)
- [ ] Exportación a Excel con formato

---

## 👥 Compartir con Compañeros

### Para compartir este script:

1. **Copia toda la carpeta** con estos archivos:
   - `verificar_referencias.bat`
   - `verificar_multiple_bases_datos.py`
   - `referencias.bib` (tu archivo)
   - `README_VERIFICADOR_REFERENCIAS.md` (este archivo)

2. **O comparte solo estos archivos:**
   - `verificar_referencias.bat`
   - `verificar_multiple_bases_datos.py`
   - `README_VERIFICADOR_REFERENCIAS.md`

3. **Indica a tus compañeros:**
   - Que necesitan Python instalado
   - Que deben colocar su archivo `.bib` en la misma carpeta
   - Que ejecuten `verificar_referencias.bat`

---

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la sección **"Solución de Problemas"** arriba
2. Verifica que Python esté instalado correctamente
3. Asegúrate de que el archivo `.bib` tenga el formato correcto

---

## 📄 Licencia

Este script es de uso libre para fines académicos.

---

## 🙏 Créditos

- **Autor**: Luis Angel Martínez Corral
- **Proyecto**: Tesis de Maestría - Modelo de Evaluación del Comportamiento Sedentario
- **Fecha**: Noviembre 2025

---

**¡Buena suerte con tu verificación de referencias! 📚✨**

