# 🔍 REFERENCIAS INCOMPLETAS - BÚSQUEDA DE DOIs FALTANTES

**Para:** Luis Angel Martínez Corral  
**De:** Poseidón 🔱  
**Fecha:** 4 de Noviembre de 2025  
**Propósito:** Completar metadatos bibliográficos para cumplir APA 7

---

## 📊 **RESUMEN EJECUTIVO**

**Total de referencias en archivo:** 80+  
**Referencias con datos completos:** 60 (75%)  
**Referencias incompletas:** 20 (25%)  

**Categorías de incompletitud:**
- ❌ Sin DOI: 12 referencias
- ⚠️ Sin número de páginas: 5 referencias
- ⚠️ Sin volumen/número de revista: 3 referencias
- ⚠️ Datos de autor incompletos: 4 referencias
- ⚠️ Sin año de publicación: 2 referencias

---

## 🔴 **PRIORIDAD CRÍTICA - BUSCAR DOIs URGENTE (10 referencias)**

Estas referencias **requieren DOI obligatoriamente** según APA 7:

### 1. **FuzzyExpertSystems**
```bibtex
@misc{FuzzyExpertSystems,
  title = {Fuzzy Expert Systems and Fuzzy Reasoning},
  author = {{LinG Team}},
  note = {Live, Informative, Non-cost and Genuine resource}
}
```

**PROBLEMAS:**
- ❌ Sin autor específico
- ❌ Sin año de publicación
- ❌ Sin URL o DOI

**ACCIÓN:** 
- **Opción A:** Buscar libro/recurso original con título completo
- **Opción B:** Eliminar (parece referencia muy genérica)

**BÚSQUEDA SUGERIDA:**
```
Google Scholar: "Fuzzy Expert Systems and Fuzzy Reasoning" LinG
```

---

### 2. **Matic_SedentaryHRV**
```bibtex
@misc{Matic_SedentaryHRV,
  author = {Matic, Aleksandar and Cipresso, Pietro and Osmani, Venet and ...},
  title = {Sedentary Work Style and Heart Rate Variability: a Short Term Analysis}
}
```

**PROBLEMAS:**
- ❌ Sin año de publicación
- ❌ Sin revista/conferencia
- ❌ Sin DOI

**ACCIÓN:** Buscar en:
```
Google Scholar: Matic Cipresso "Sedentary Work Style" HRV
PubMed: Matic sedentary heart rate variability
```

**DOI ESPERADO:** Probablemente es un conference paper (IEEE o ACM)

---

### 3. **VanoliHRV**
```bibtex
@misc{VanoliHRV,
  title = {Heart rate variability during specific sleep stages}
}
```

**PROBLEMAS:**
- ❌ Sin autores
- ❌ Sin año
- ❌ Sin revista
- ❌ Sin DOI

**ACCIÓN:** Buscar:
```
Google Scholar: Vanoli "heart rate variability" sleep stages
```

**NOTA:** Probablemente es: *E. Vanoli et al., "Heart rate variability during specific sleep stages: a comparison of healthy subjects with patients after myocardial infarction"*

---

### 4. **HypertensionHRV**
```bibtex
@misc{HypertensionHRV,
  title = {The Role of Heart Rate Variability (HRV) in Different Hypertensive Syndromes},
  journal = {Diagnostics},
  year = {2023},
  doi = {10.3390/diagnostics}
}
```

**PROBLEMAS:**
- ❌ Sin autores
- ❌ DOI incompleto (falta número de artículo)

**ACCIÓN:** Buscar en Diagnostics 2023:
```
https://www.mdpi.com/journal/diagnostics
Buscar: "Heart Rate Variability" "Hypertensive Syndromes" 2023
```

**DOI CORRECTO ESPERADO:** `10.3390/diagnostics13XXXXXX`

---

### 5. **Tsoukalas_Uhrig_Fuzzy**
```bibtex
@book{Tsoukalas_Uhrig_Fuzzy,
  author = {Tsoukalas, Lefteri H. and Uhrig, Robert E.},
  title = {Fuzzy and Neural Approaches in Engineering},
  publisher = {Wiley-Interscience}
}
```

**PROBLEMAS:**
- ❌ Sin año de publicación
- ❌ Sin ISBN
- ❌ Sin DOI

**ACCIÓN:** Buscar en WorldCat o Amazon:
```
Google: Tsoukalas Uhrig "Fuzzy and Neural Approaches in Engineering" Wiley
WorldCat: http://www.worldcat.org/
```

**DATO ESPERADO:** Año 1997, ISBN: 978-0471160038

---

### 6. **BIOMEDICAS2023**
```bibtex
@phdthesis{BIOMEDICAS2023,
  author = {{Robinson Alberto Torres Villa}},
  title = {Aplicativo de Asistencia Deportiva a Partir del Procesamiento de Señales Fisiológicas},
  school = {Universidad [Nombre Universidad]},
  year = {2023},
  type = {Trabajo de grado},
  note = {Modalidad: Exploratorio. Autores: Lucero Karina Guevara Yandar, Andrea Casas Ramírez}
}
```

**PROBLEMAS:**
- ❌ Nombre de universidad faltante
- ❌ Sin URL o repositorio institucional

**ACCIÓN:** Buscar en:
```
Google: Robinson Torres Villa "Asistencia Deportiva" "Señales Fisiológicas" 2023
Repositorios colombianos (probable): 
  - https://repositorio.unal.edu.co/
  - https://repository.javeriana.edu.co/
```

---

### 7. **RodriguezOntiveros2021**
```bibtex
@misc{RodriguezOntiveros2021,
  author = {Rodríguez Ontiveros, Víctor Hugo and García Plaza, Víctor and {Sanz}, María Inmaculada},
  title = {Aplicaciones de sensores vestibles y teléfonos inteligentes...},
  year = {2021},
  school = {Universidad de Zaragoza},
  url = {http://zaguan.unizar.es}
}
```

**PROBLEMAS:**
- ⚠️ URL incompleta (falta el handle específico)
- ❌ Sin DOI

**ACCIÓN:** Buscar en repositorio ZAGUAN:
```
https://zaguan.unizar.es/
Buscar: Rodríguez Ontiveros 2021 sensores vestibles
```

**URL COMPLETA ESPERADA:** `http://zaguan.unizar.es/record/XXXXX`

---

### 8. **Levitz1979Logic**
```bibtex
@book{Levitz1979Logic,
  author = {Levitz, Kathleen and Levitz, Hilbert},
  title = {Logic and Boolean Algebra},
  publisher = {Barron's Educational Series},
  year = {1979}
}
```

**PROBLEMAS:**
- ❌ Sin ISBN
- ❌ Sin DOI (libros antiguos generalmente no tienen)

**ACCIÓN:**
- Buscar ISBN en WorldCat o Library of Congress
- **OPCIONAL:** Considerar reemplazar con referencia más reciente sobre álgebra booleana

---

### 9. **GlobalPAQ**
```bibtex
@misc{GlobalPAQ,
  title = {Global Physical Activity Questionnaire Analysis Guide (GPAQ)},
  howpublished = {\url{http://www.who.int/chp/steps/GPAQ/en/index.html}},
  note = {World Health Organization}
}
```

**PROBLEMAS:**
- ❌ Sin año
- ❌ Sin autores formales
- ⚠️ URL posiblemente desactualizada (WHO cambió estructura web)

**ACCIÓN:** Verificar URL actual en:
```
https://www.who.int/ → Buscar "GPAQ"
Actualizar a URL correcta de 2024
```

---

### 10. **Meusel2006Framework**
```bibtex
@misc{Meusel2006Framework,
  author = {Meusel, D and Höger, C and {Pérez-Rodrigo}, C and Aranceta, J and Cavill, N},
  title = {Global Strategy on Diet, Physical Activity and Health: A framework to monitor and evaluate implementation},
  year = {2006}
}
```

**PROBLEMAS:**
- ❌ Sin revista o tipo de documento
- ❌ Sin URL o DOI
- ⚠️ ¿Es un report de WHO? ¿O artículo?

**ACCIÓN:** Buscar en:
```
Google Scholar: Meusel Höger "Global Strategy" WHO 2006
WHO Document Repository: https://apps.who.int/iris/
```

---

## 🟡 **PRIORIDAD MEDIA - COMPLETAR METADATOS (8 referencias)**

### 11. **Amit2001Computational**
```bibtex
@book{Amit2001Computational,
  author = {{Amit Kumar}, M. and {Shruti}, J. M. S. and {Sudip}, P.},
  title = {Computational Intelligence in Healthcare},
  publisher = {Springer Nature Switzerland AG},
  year = {2001},
  url = {http://www.springer.com/series/11944}
}
```

**PROBLEMAS:**
- ⚠️ Año inconsistente (2001 pero editorial es "Springer Nature Switzerland AG" que no existía en 2001)
- ❌ Sin ISBN
- ⚠️ URL parece ser de una serie, no del libro específico

**ACCIÓN:** Verificar año correcto (probablemente 2019-2021)

---

### 12. **Strefezza2009Logica**
```bibtex
@article{Strefezza2009Logica,
  author = {Strefezza, M.},
  title = {Lógica difusa, un punto de vista},
  journal = {Revista Ciencia e Ingeniería},
  volume = {30},
  number = {3},
  year = {2009}
}
```

**PROBLEMAS:**
- ❌ Sin páginas
- ❌ Sin DOI

**ACCIÓN:** Buscar en:
```
Google Scholar: Strefezza "Lógica difusa" 2009 Venezuela
```
**NOTA:** Revista venezolana, probablemente no tiene DOI (antiguo)

---

### 13. **Gonzalez2018Analisis**
```bibtex
@article{Gonzalez2018Analisis,
  author = {González, Guillermo and Ortega, Zurisaday and ...},
  title = {Análisis de la capacidad aeróbica como cualidad esencial...},
  journal = {Retos},
  year = {2018},
  url = {www.retos.org}
}
```

**PROBLEMAS:**
- ❌ Sin volumen/número
- ❌ Sin páginas
- ❌ Sin DOI
- ⚠️ URL incompleta

**ACCIÓN:** Buscar en:
```
https://recyt.fecyt.es/index.php/retos
Buscar: González capacidad aeróbica 2018
```

---

### 14. **Pulopulos2018Association**
```bibtex
@article{Pulopulos2018Association,
  author = {Pulopulos, Matias M. and ...},
  title = {Association between changes in heart rate variability...},
  journal = {Psychoneuroendocrinology}
}
```

**PROBLEMAS:**
- ❌ Sin volumen
- ❌ Sin páginas
- ❌ Sin DOI

**ACCIÓN:** Buscar en PubMed:
```
PubMed: Pulopulos 2018 heart rate variability cortisol
```

**DOI ESPERADO:** Probablemente `10.1016/j.psyneuen.2018.05.004`

---

### 15-20. **Referencias Placeholder de Ejemplos (NO urgentes)**

Estas son placeholders de los capítulos con contenido de ejemplo:
- `autor2023`, `autor_original`, `autor1`, `autor2` (Cap. 2 - Marco Teórico)
- `autor_mexico`, `autor_metodologia`, `autor_diseños` (Cap. 4-5)
- `referencia`, `referencia_metodologica` (Cap. 5)
- `helsinki`, `belmont` (Cap. 5 - Ética)

**ACCIÓN:** 
- **NO buscar DOIs** (son placeholders)
- **Reemplazar cuando escribas contenido real** de cada capítulo

---

## ✅ **REFERENCIAS QUE SÍ TIENEN DATOS COMPLETOS (Ejemplos)**

Para comparación, estas son referencias BIEN formateadas:

```bibtex
@article{Bull2020,  ✅ COMPLETO
  author = {Bull, Fiona C. and Al-Ansari, Salih S. and ...},
  title = {World Health Organization 2020 guidelines...},
  journal = {British Journal of Sports Medicine},
  volume = {54},
  number = {24},
  pages = {1451--1462},
  year = {2020},
  doi = {10.1136/bjsports-2020-102955}  ← DOI presente
}

@article{Henriksen2018,  ✅ COMPLETO
  author = {Henriksen, Andreas and Mikalsen, Martin Haugen and ...},
  title = {Using fitness trackers and smartwatches...},
  journal = {Journal of Medical Internet Research},
  volume = {20},
  number = {3},
  pages = {e110},
  year = {2018},
  doi = {10.2196/jmir.9157}  ← DOI presente
}
```

---

## 🔧 **CÓMO BUSCAR DOIs FALTANTES**

### **Método 1: CrossRef (Más Rápido)**
1. Ve a: https://www.crossref.org/
2. Click en "Metadata Search"
3. Ingresa: **Título del artículo**
4. Copia el DOI encontrado

### **Método 2: Google Scholar**
1. Busca el título completo entre comillas
2. Si aparece, click en "Cite"
3. A veces incluye DOI en la citación

### **Método 3: Búsqueda Directa en PubMed**
1. Ve a: https://pubmed.ncbi.nlm.nih.gov/
2. Busca: `Apellido [Año] palabras clave`
3. El DOI aparece en la página del artículo

### **Método 4: DOI Resolver**
Si tienes el nombre de la revista:
```
https://doi.org/ → Ingresar posible DOI
Ejemplo: 10.1016/j.psyneuen.2018.05.004
```

---

## 📋 **CHECKLIST DE BÚSQUEDA**

Copia y marca al completar:

### **CRÍTICAS (Requieren DOI):**
- [ ] FuzzyExpertSystems → Buscar en Google Scholar
- [ ] Matic_SedentaryHRV → Buscar en IEEE Xplore / Google Scholar
- [ ] VanoliHRV → Buscar "Vanoli HRV sleep stages"
- [ ] HypertensionHRV → Buscar en MDPI Diagnostics 2023
- [ ] Pulopulos2018 → Buscar en PubMed
- [ ] GlobalPAQ → Actualizar URL de WHO
- [ ] Meusel2006Framework → Buscar en WHO IRIS

### **MEDIAS (Completar metadatos):**
- [ ] Tsoukalas_Uhrig → Verificar año e ISBN
- [ ] Amit2001Computational → Corregir año
- [ ] Strefezza2009 → Buscar páginas
- [ ] Gonzalez2018 → Buscar volumen/número/páginas
- [ ] BIOMEDICAS2023 → Buscar universidad y repositorio
- [ ] RodriguezOntiveros2021 → Completar URL ZAGUAN

---

## 🎯 **PRIORIDAD RECOMENDADA (Orden de Búsqueda)**

**DÍA 1 (Hoy/Mañana):**
1. Matic_SedentaryHRV (relevante para HRV)
2. Pulopulos2018 (relevante para HRV)
3. HypertensionHRV (actualizar DOI)

**DÍA 2:**
4. VanoliHRV (completar datos)
5. Tsoukalas_Uhrig (verificar año)
6. BIOMEDICAS2023 (completar universidad)

**DÍA 3:**
7. GlobalPAQ (actualizar URL)
8. Meusel2006 (verificar tipo documento)
9. Gonzalez2018 (completar metadatos)

**OPCIONAL (No urgente):**
10. FuzzyExpertSystems (considerar eliminar si no se encuentra)
11. Amit2001Computational (verificar año)
12. Strefezza2009 (búsqueda opcional)

---

## 📝 **FORMATO PARA REPORTAR HALLAZGOS**

Cuando encuentres un DOI, repórtalo así:

```
ENCONTRADO:
- Referencia: Matic_SedentaryHRV
- DOI: 10.1109/EMBC.2014.6943571
- Datos completos:
  * Autores: Matic, A., Cipresso, P., ...
  * Título: Sedentary Work Style and Heart Rate Variability
  * Conferencia: IEEE EMBC 2014
  * Páginas: 123-126
  * Año: 2014
```

---

## 💡 **TIPS DE BÚSQUEDA**

### **Si no encuentras el DOI:**
1. ✅ Verifica que el título sea exacto (copia del PDF original)
2. ✅ Intenta con variaciones del título (con/sin subtítulo)
3. ✅ Busca primero autor + año clave
4. ✅ Si es paper antiguo (<2000), probablemente no tiene DOI
5. ✅ Si es literatura gris, busca repositorio institucional

### **Alternativas sin DOI:**
- **Libros antiguos:** Usar ISBN en lugar de DOI
- **Reportes de gobierno:** Usar URL oficial
- **Literatura gris:** Usar repositorio institucional

---

## 🚀 **PRÓXIMA ACCIÓN**

**RECOMENDACIÓN:**
1. **Empieza con las 10 referencias críticas** (lista roja arriba)
2. **Dedica 30 min por referencia** (búsqueda + verificación)
3. **Total tiempo estimado:** 5 horas (distribuir en 2-3 días)
4. **Reporta avances** al completar cada 3 referencias

**¿Necesitas ayuda con alguna búsqueda específica?** Puedo asistir con estrategias de búsqueda avanzada.

---

**FIN DEL DOCUMENTO**


