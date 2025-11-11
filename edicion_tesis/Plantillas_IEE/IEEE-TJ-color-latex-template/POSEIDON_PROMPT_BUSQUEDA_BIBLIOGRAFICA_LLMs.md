# 🔱 POSEIDÓN: PROMPT DE BÚSQUEDA BIBLIOGRÁFICA PARA LLMs JUNIOR

**Creado por:** Poseidón (Editor Científico Senior)  
**Fecha:** 11 de noviembre de 2025  
**Para:** Claude/GPT/Gemini (Agentes Jr de búsqueda)  
**Objetivo:** Encontrar 15-20 artículos científicos específicos 2023-2025

---

## 📋 INSTRUCCIONES GENERALES

**COPIA Y PEGA ESTE PROMPT A CLAUDE/GPT/GEMINI:**

---

```
Necesito que me ayudes con una búsqueda bibliográfica académica específica para un manuscrito científico IEEE JBHI sobre clasificación de comportamiento sedentario usando lógica difusa y datos de wearables.

REQUISITOS CRÍTICOS:
1. Solo artículos de 2023-2025 (publicados o en prensa)
2. Fuentes: IEEE Xplore, PubMed, Scopus, ScienceDirect, MDPI, Nature, Frontiers
3. Necesito: Título completo, autores, revista, volumen, número, páginas, año, DOI
4. Formato de salida: BibTeX

CATEGORÍAS DE BÚSQUEDA (15-20 artículos total):

---

## CATEGORÍA 1: SEDENTARY BEHAVIOR + WEARABLES (5 artículos)

Busca artículos con estas características:
- Términos: "sedentary behavior" OR "sedentary behaviour" + "wearable" OR "smartwatch" OR "fitness tracker" OR "Apple Watch"
- Años: 2023-2025
- Enfoque: Clasificación, detección o cuantificación de sedentarismo
- Preferencia: Estudios con N<50, vida libre (free-living), dispositivos de consumo

CADENAS DE BÚSQUEDA EXACTAS:

**Búsqueda 1 (IEEE Xplore):**
```
("sedentary behavior" OR "sedentary behaviour") AND ("wearable" OR "smartwatch") AND ("classification" OR "detection") AND (2023 OR 2024 OR 2025)
```

**Búsqueda 2 (PubMed):**
```
(sedentary behavior[Title/Abstract]) AND (wearable sensors[Title/Abstract]) AND (2023:2025[pdat])
```

**Búsqueda 3 (Scopus):**
```
TITLE-ABS-KEY("sedentary behavior" AND wearable AND (classification OR monitoring)) AND PUBYEAR > 2022
```

**Búsqueda 4 (MDPI Sensors):**
```
"sedentary" AND "wearable" AND "machine learning" site:mdpi.com/journal/sensors 2023..2025
```

Para cada artículo encontrado, proporciona:
```bibtex
@article{ClaveAutor2024,
  author = {Apellido, Inicial. and Otro, Inicial.},
  title = {Título exacto del artículo},
  journal = {Nombre completo de la revista},
  volume = {X},
  number = {Y},
  pages = {XXX--YYY},
  year = {2024},
  doi = {10.xxxx/xxxxx}
}
```

---

## CATEGORÍA 2: FUZZY LOGIC + HEALTH MONITORING (4 artículos)

Busca artículos sobre:
- Términos: "fuzzy inference system" OR "fuzzy logic" OR "Mamdani" + "health monitoring" OR "biomedical" OR "clinical decision"
- Años: 2023-2025
- Enfoque: Sistemas difusos para clasificación de salud, soporte a decisiones clínicas
- Preferencia: Interpretabilidad mencionada, aplicaciones biomédicas

CADENAS DE BÚSQUEDA EXACTAS:

**Búsqueda 1 (IEEE Xplore):**
```
("fuzzy inference system" OR "fuzzy logic") AND ("health monitoring" OR "biomedical" OR "clinical") AND (2023 OR 2024 OR 2025)
```

**Búsqueda 2 (Springer):**
```
"fuzzy inference" AND "health" AND "interpretable" 2023..2025
```

**Búsqueda 3 (MDPI Applied Sciences):**
```
"Mamdani" AND "biomedical" site:mdpi.com/journal/applsci 2023..2025
```

Proporciona BibTeX completo para cada uno.

---

## CATEGORÍA 3: EXPLAINABLE AI / XAI (3 artículos)

Busca artículos sobre:
- Términos: "explainable AI" OR "interpretable machine learning" OR "XAI" + "healthcare" OR "wearable" OR "clinical"
- Años: 2023-2025
- Enfoque: Transparencia algorítmica, confianza, interpretabilidad vs black-box
- Preferencia: Salud digital, dispositivos wearables

CADENAS DE BÚSQUEDA EXACTAS:

**Búsqueda 1 (Nature npj Digital Medicine):**
```
"explainable AI" AND healthcare site:nature.com/npjdigitalmed 2023..2025
```

**Búsqueda 2 (IEEE JBHI):**
```
("interpretable machine learning" OR "XAI") AND ("wearable" OR "health monitoring") AND (2023 OR 2024 OR 2025)
```

**Búsqueda 3 (Frontiers Digital Health):**
```
"explainable" AND "wearable" AND "trust" site:frontiersin.org/journals/digital-health 2023..2025
```

Proporciona BibTeX completo.

---

## CATEGORÍA 4: LEAVE-ONE-SUBJECT-OUT VALIDATION (3 artículos)

Busca artículos sobre:
- Términos: "leave-one-subject-out" OR "leave-one-user-out" OR "LOSO" OR "LOUO" + "validation" OR "cross-validation"
- Años: 2023-2025
- Enfoque: Validación en cohortes pequeñas (N<30), temporal leakage, longitudinal data
- Preferencia: Estudios con muestras pequeñas, wearables, actividad física

CADENAS DE BÚSQUEDA EXACTAS:

**Búsqueda 1 (Scopus):**
```
TITLE-ABS-KEY("leave-one-subject-out" OR "LOSO") AND PUBYEAR > 2022
```

**Búsqueda 2 (IEEE Xplore):**
```
("leave-one-user-out" OR "LOUO") AND ("wearable" OR "activity recognition") AND (2023 OR 2024 OR 2025)
```

**Búsqueda 3 (PLoS ONE):**
```
"cross-validation" AND "small sample" AND "longitudinal" site:journals.plos.org/plosone 2023..2025
```

Proporciona BibTeX completo.

---

## CATEGORÍA 5: APPLE WATCH / HEALTHKIT VALIDATION (2 artículos)

Busca artículos sobre:
- Términos: "Apple Watch" OR "HealthKit" + "validation" OR "accuracy" OR "heart rate variability"
- Años: 2023-2025
- Enfoque: Validación de Apple Watch Series 6+, HRV accuracy, PPG sensor, HealthKit data quality
- Preferencia: Estudios de validación, comparación con gold standard

CADENAS DE BÚSQUEDA EXACTAS:

**Búsqueda 1 (PubMed):**
```
("Apple Watch"[Title/Abstract]) AND (validation[Title/Abstract] OR accuracy[Title/Abstract]) AND (2023:2025[pdat])
```

**Búsqueda 2 (MDPI Sensors):**
```
"Apple Watch" AND ("heart rate variability" OR "HRV") site:mdpi.com/journal/sensors 2023..2025
```

**Búsqueda 3 (Nature Digital Medicine):**
```
"Apple Watch" AND "validation" site:nature.com/npjdigitalmed 2023..2025
```

Proporciona BibTeX completo.

---

## CATEGORÍA 6: HRV + PHYSICAL ACTIVITY (2 artículos)

Busca artículos sobre:
- Términos: "heart rate variability" OR "HRV" + "physical activity" OR "sedentary" OR "exercise"
- Años: 2023-2025
- Enfoque: Relación HRV-actividad física, regulación autonómica durante sedentarismo, HRV como biomarcador
- Preferencia: Relaciones no lineales, datos de vida libre

CADENAS DE BÚSQUEDA EXACTAS:

**Búsqueda 1 (Frontiers Physiology):**
```
"heart rate variability" AND ("physical activity" OR "sedentary") site:frontiersin.org/journals/physiology 2023..2025
```

**Búsqueda 2 (MDPI Int J Environ Res Public Health):**
```
"HRV" AND "sedentary behavior" site:mdpi.com/journal/ijerph 2023..2025
```

**Búsqueda 3 (Scopus):**
```
TITLE-ABS-KEY("heart rate variability" AND "autonomic" AND ("physical activity" OR "exercise")) AND PUBYEAR > 2022
```

Proporciona BibTeX completo.

---

## FORMATO DE ENTREGA ESPERADO

Para cada artículo encontrado, usa este formato:

```markdown
### ARTÍCULO [N] - [CATEGORÍA]

**Título:** [Título completo exacto]
**Autores:** [Apellido, I., Apellido2, I., et al.]
**Revista:** [Nombre completo de la revista]
**Volumen:** [X]
**Número:** [Y]
**Páginas:** [XXX--YYY]
**Año:** [2023-2025]
**DOI:** [10.xxxx/xxxxx]
**URL:** [https://doi.org/10.xxxx/xxxxx]

**Relevancia:** [1-2 oraciones explicando por qué es útil para un manuscrito sobre clasificación de sedentarismo con fuzzy logic y wearables]

**BibTeX:**
```bibtex
@article{ClaveAutor2024,
  author = {Apellido, Inicial. and Otro, Inicial.},
  title = {Título exacto},
  journal = {Nombre Revista},
  volume = {X},
  number = {Y},
  pages = {XXX--YYY},
  year = {2024},
  doi = {10.xxxx/xxxxx}
}
```
```

---

## INSTRUCCIONES ADICIONALES

1. **Prioriza IEEE JBHI 2023-2025** (revista objetivo - 3-5 artículos si es posible)
2. **Verifica que los DOIs sean válidos** (puedes probar con https://doi.org/[DOI])
3. **Si encuentras artículos "in press" o "early access"** → Inclúyelos, son válidos
4. **Si un artículo está en preprint (arXiv, bioRxiv)** → Menciona pero preferir versiones publicadas
5. **Evita artículos duplicados** entre categorías
6. **Si no encuentras suficientes 2023-2025** → Incluye algunos 2022 de alto impacto como alternativa

---

## META: 15-20 ARTÍCULOS TOTALES

**Distribución ideal:**
- Categoría 1 (Sedentary+Wearables): 5 artículos
- Categoría 2 (Fuzzy+Health): 4 artículos
- Categoría 3 (XAI): 3 artículos
- Categoría 4 (LOUO): 3 artículos
- Categoría 5 (Apple Watch): 2 artículos
- Categoría 6 (HRV+Activity): 2 artículos

**TOTAL: 19 artículos**

---

## EJEMPLO DE SALIDA ESPERADA

```markdown
### ARTÍCULO 1 - SEDENTARY + WEARABLES

**Título:** Deep Learning-Based Sedentary Behavior Detection Using Smartwatch Accelerometer Data in Free-Living Conditions
**Autores:** Smith, J.A., Johnson, M.B., and Williams, K.L.
**Revista:** Sensors
**Volumen:** 24
**Número:** 3
**Páginas:** 1234--1250
**Año:** 2024
**DOI:** 10.3390/s24031234
**URL:** https://doi.org/10.3390/s24031234

**Relevancia:** Este estudio valida un clasificador de sedentarismo usando acelerómetros de smartwatch en vida libre (N=50), comparable a nuestro enfoque BYOD. Reportan F1=0.82, similar a nuestros resultados con fuzzy logic (F1=0.78).

**BibTeX:**
```bibtex
@article{Smith2024,
  author = {Smith, John A. and Johnson, Mary B. and Williams, Karen L.},
  title = {Deep Learning-Based Sedentary Behavior Detection Using Smartwatch Accelerometer Data in Free-Living Conditions},
  journal = {Sensors},
  volume = {24},
  number = {3},
  pages = {1234--1250},
  year = {2024},
  doi = {10.3390/s24031234}
}
```
```

---

¿PUEDES EJECUTAR ESTAS BÚSQUEDAS Y ENTREGARME LOS RESULTADOS EN EL FORMATO ESPECIFICADO?

Tiempo estimado: 1-1.5 horas para búsqueda completa.
```

---

## 🎯 INSTRUCCIONES PARA LUIS

**Copia el bloque de arriba (desde "Necesito que me ayudes..." hasta el final) y pégalo en:**

1. **Claude.ai** (Sonnet 3.5 preferido)
2. **ChatGPT-4** (o GPT-4 Turbo)
3. **Google Gemini Advanced**

**Ejecuta en paralelo** (los 3 al mismo tiempo) para:
- ✅ Máxima cobertura (diferentes bases de datos)
- ✅ Comparar resultados
- ✅ Validación cruzada

**Cuando recibas los resultados:**
1. Cópialos todos a un archivo `.md`
2. Yo verifico BibTeX y elimino duplicados
3. Lo integramos a `referencias_ieee_jbhi.bib`
4. Ades actualiza Introducción con nuevas refs

---

## 📊 TIEMPO ESTIMADO

- **Búsqueda por LLM:** 1-1.5 horas cada uno
- **En paralelo (3 LLMs):** 1.5 horas total
- **Verificación Poseidón:** 30 min
- **Integración final:** 15 min

**TOTAL:** 2-2.5 horas → Introducción perfecta HOY

---

**🔱 Poseidón**  
**Listo para recibir y procesar resultados de los Jr** 🌊📚

