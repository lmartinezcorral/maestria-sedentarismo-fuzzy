# 📚 Bases de Datos Académicas para Verificación de Referencias

Este documento describe las principales bases de datos académicas donde puedes verificar la indexación de artículos científicos.

---

## 🎯 Bases de Datos Verificadas por el Script

### 1. **ScienceDirect** (Elsevier)
- **URL:** https://www.sciencedirect.com/
- **Enfoque:** Ciencias, medicina, ingeniería, ciencias sociales
- **Editorial:** Elsevier
- **Cobertura:** ~2,500 revistas, 40,000 libros
- **Relevancia para tu proyecto:** ⭐⭐⭐⭐ (Lancet, Applied Physiology, etc.)

### 2. **PubMed** (NCBI/NLM)
- **URL:** https://pubmed.ncbi.nlm.nih.gov/
- **Enfoque:** Ciencias biomédicas y de la vida
- **Editorial:** National Library of Medicine (EE.UU.)
- **Cobertura:** MEDLINE + otras fuentes (más de 34 millones de citas)
- **Relevancia para tu proyecto:** ⭐⭐⭐⭐⭐ (Salud pública, actividad física, HRV)

### 3. **IEEE Xplore**
- **URL:** https://ieeexplore.ieee.org/
- **Enfoque:** Ingeniería, tecnología, ciencias de la computación
- **Editorial:** IEEE (Institute of Electrical and Electronics Engineers)
- **Cobertura:** ~5 millones de documentos
- **Relevancia para tu proyecto:** ⭐⭐⭐⭐ (Wearables, sensores, procesamiento de señales)

### 4. **ACM Digital Library**
- **URL:** https://dl.acm.org/
- **Enfoque:** Ciencias de la computación, inteligencia artificial
- **Editorial:** ACM (Association for Computing Machinery)
- **Cobertura:** ~2.5 millones de documentos
- **Relevancia para tu proyecto:** ⭐⭐⭐ (Machine learning, procesamiento de datos)

### 5. **Google Scholar**
- **URL:** https://scholar.google.com/
- **Enfoque:** General (todas las disciplinas)
- **Editorial:** Google
- **Cobertura:** Muy amplia (artículos, tesis, libros, preprints)
- **Relevancia para tu proyecto:** ⭐⭐⭐⭐⭐ (Búsqueda general, citas)

### 6. **SpringerLink**
- **URL:** https://link.springer.com/
- **Enfoque:** Ciencias, medicina, ingeniería, humanidades
- **Editorial:** Springer Nature
- **Cobertura:** ~3,000 revistas, 300,000 libros
- **Relevancia para tu proyecto:** ⭐⭐⭐ (Revistas de salud, ingeniería)

### 7. **Wiley Online Library**
- **URL:** https://onlinelibrary.wiley.com/
- **Enfoque:** Ciencias, medicina, ingeniería, ciencias sociales
- **Editorial:** John Wiley & Sons
- **Cobertura:** ~1,600 revistas, 20,000 libros
- **Relevancia para tu proyecto:** ⭐⭐⭐ (Revistas médicas, ingeniería)

### 8. **Crossref**
- **URL:** https://www.crossref.org/
- **Enfoque:** Metadatos DOI (no es una base de datos de contenido)
- **Editorial:** Crossref (organización sin fines de lucro)
- **Cobertura:** Metadatos de ~140 millones de documentos
- **Relevancia para tu proyecto:** ⭐⭐⭐⭐⭐ (Verificación de DOIs, publisher info)

---

## 📊 Otras Bases de Datos Importantes (No incluidas en el script)

### **Scopus**
- **URL:** https://www.scopus.com/
- **Enfoque:** Multidisciplinario
- **Editorial:** Elsevier
- **Cobertura:** ~25,000 revistas
- **Acceso:** Requiere suscripción institucional
- **Relevancia:** ⭐⭐⭐⭐⭐ (Índices de citas, métricas)

### **Web of Science (WoS)**
- **URL:** https://www.webofscience.com/
- **Enfoque:** Multidisciplinario
- **Editorial:** Clarivate Analytics
- **Cobertura:** ~21,000 revistas
- **Acceso:** Requiere suscripción institucional
- **Relevancia:** ⭐⭐⭐⭐⭐ (Índices de citas, impacto)

### **arXiv**
- **URL:** https://arxiv.org/
- **Enfoque:** Preprints (física, matemáticas, ciencias de la computación)
- **Editorial:** Cornell University
- **Cobertura:** Preprints (no revisados por pares)
- **Acceso:** Gratuito
- **Relevancia:** ⭐⭐ (Preprints, no artículos publicados)

### **ResearchGate**
- **URL:** https://www.researchgate.net/
- **Enfoque:** Red social académica
- **Editorial:** ResearchGate GmbH
- **Cobertura:** Perfiles de investigadores, publicaciones
- **Acceso:** Gratuito (requiere registro)
- **Relevancia:** ⭐⭐⭐ (Red social, no base de datos oficial)

### **Semantic Scholar**
- **URL:** https://www.semanticscholar.org/
- **Enfoque:** IA para búsqueda académica
- **Editorial:** Allen Institute for AI
- **Cobertura:** ~200 millones de artículos
- **Acceso:** Gratuito
- **Relevancia:** ⭐⭐⭐⭐ (Búsqueda inteligente, gráficos de citas)

---

## 🚀 Uso del Script de Verificación

### Script Simple (Solo ScienceDirect)
```bash
python verificar_sciencedirect.py
```

### Script Completo (Múltiples Bases de Datos)
```bash
python verificar_multiple_bases_datos.py
```

### Archivos Generados

1. **`referencias_sciencedirect.csv`** - Resultados solo de ScienceDirect
2. **`referencias_multiple_bases_datos.csv`** - Resultados de todas las bases de datos
3. **Archivos JSON** - Mismos datos en formato JSON

---

## 📈 Interpretación de Resultados

### Columnas en el CSV

- `key`: Clave de la referencia en el .bib
- `title`, `author`, `journal`, `year`, `doi`: Información básica
- `{database}_indexed`: `True`/`False` si está indexada
- `{database}_url`: URL de búsqueda o del artículo
- `{database}_method`: Método usado para encontrarla (doi_search, title_search, etc.)
- `total_databases`: Número total de bases de datos donde está indexada
- `crossref_publisher`: Editorial según Crossref

### Ejemplo de Resultado

```csv
key,title,doi,pubmed_indexed,pubmed_url,ieee_indexed,ieee_url,...
Bull2020,WHO Guidelines...,10.1136/bjsports-2020-102955,True,https://pubmed...,False,...
```

---

## 💡 Recomendaciones por Tipo de Referencia

### **Ciencias de la Salud / Medicina**
- ✅ **PubMed** (prioridad)
- ✅ **ScienceDirect** (Elsevier)
- ✅ **Google Scholar**

### **Ingeniería / Tecnología**
- ✅ **IEEE Xplore** (prioridad)
- ✅ **ACM Digital Library**
- ✅ **SpringerLink**

### **Ciencias Generales**
- ✅ **Google Scholar** (prioridad)
- ✅ **Crossref** (verificar DOI)
- ✅ **ScienceDirect** o **SpringerLink** según editorial

### **Referencias sin DOI**
- ✅ **Google Scholar** (búsqueda por título)
- ✅ **PubMed** (si es de salud)
- ⚠️ Otras bases de datos pueden no encontrarlas

---

## ⚠️ Limitaciones

1. **Búsquedas automatizadas:** Algunas bases de datos pueden bloquear requests automatizados
2. **Tiempo de ejecución:** Verificar 150+ referencias puede tardar 10-20 minutos
3. **Precisión:** Las búsquedas por título pueden dar falsos positivos
4. **Acceso:** Algunas bases de datos requieren suscripción para ver contenido completo

---

## 🔧 Mejoras Futuras

- [ ] Agregar verificación en Scopus (si hay acceso)
- [ ] Agregar verificación en Web of Science (si hay acceso)
- [ ] Mejorar detección de falsos positivos
- [ ] Agregar verificación en Semantic Scholar
- [ ] Exportar estadísticas más detalladas

---

## 📚 Referencias

- [Lista de bases de datos académicas](https://en.wikipedia.org/wiki/List_of_academic_databases_and_search_engines)
- [Guía de acceso a bases de datos](https://www.recursoscientificos.fecyt.es/)

---

**Última actualización:** Noviembre 2025

