# ESTRUCTURA DE PRESENTACIÓN: DEFENSA PREVIA DE TESIS
## Duración: 15 minutos (~1 minuto por diapositiva)

**Título:** Modelo de Evaluación del Comportamiento Sedentario mediante Lógica Difusa y Datos Biométricos  
**Investigador:** Luis Angel Martínez Corral  
**Programa:** Maestría en Formación e Innovación para Profesionales de la Salud (MFIPS)  
**Universidad:** Universidad Autónoma de Chihuahua (UACH)

---

## DIAPOSITIVA 1: PORTADA ✅ (Ya tienes)
**Tiempo:** 10 segundos
- Título completo
- Tu nombre
- Programa y Universidad
- Fecha

---

## DIAPOSITIVA 2: TABLA DE CONTENIDO ✅ (Ya tienes)
**Tiempo:** 30 segundos
- Introducción
- Marco Teórico
- Planteamiento del Problema
- Objetivos
- Diseño del Estudio
- Técnicas y Procedimientos
- Resultados
- Discusión
- Conclusiones

---

## DIAPOSITIVA 3: CONTEXTO Y JUSTIFICACIÓN
**Tiempo:** 1 minuto 15 segundos

**Contenido:**
- **Problema de salud pública:** Comportamiento Sedentario (CS) como factor de riesgo independiente
- **Magnitud:** 40% de adultos mexicanos (ENSANUT 2022)
- **Costo global:** >300,000 millones USD anuales
- **Limitación metodológica actual:**
  - Cuestionarios: sesgos de memoria, deseabilidad social
  - Técnicas objetivas: restringidas a laboratorio
- **Oportunidad:** Dispositivos portátiles de consumo masivo (Apple Watch) + IA interpretable

**Guion:**
> "El comportamiento sedentario representa uno de los desafíos más críticos de salud pública del siglo XXI. En México, el 40% de los adultos presenta comportamiento sedentario, generando costos superiores a 300 mil millones de dólares anuales a nivel global. Los métodos tradicionales de evaluación presentan limitaciones: los cuestionarios adolecen de sesgos subjetivos, mientras que las técnicas objetivas se restringen a entornos de laboratorio. La ubicuidad de dispositivos portátiles como el Apple Watch, combinada con inteligencia artificial interpretable, ofrece una oportunidad sin precedentes para la evaluación objetiva en condiciones de vida libre."

---

## DIAPOSITIVA 4: PROBLEMA DE INVESTIGACIÓN
**Tiempo:** 1 minuto

**Contenido:**
- **Vacío metodológico:** Ausencia de sistemas que integren múltiples biomarcadores de vida libre
- **Dilema actual:**
  - Modelos de caja negra (deep learning): alta precisión pero sin interpretabilidad
  - Análisis univariados: insuficientes para capturar interacciones no lineales
- **Necesidad:** Sistema robusto, validado, interpretable y con validez ecológica

**Guion:**
> "El problema central radica en la ausencia de un sistema que integre de forma sinérgica múltiples biomarcadores de vida libre en una clasificación del sedentarismo que sea robusta, empíricamente validada e interpretable. Los modelos de deep learning alcanzan alta precisión pero operan como cajas negras, dificultando su adopción clínica. Los análisis estadísticos univariados resultan insuficientes para capturar las complejas interacciones no lineales entre actividad física, función autonómica y respuesta metabólica."

---

## DIAPOSITIVA 5: PREGUNTA DE INVESTIGACIÓN
**Tiempo:** 30 segundos

**Contenido:**
- Pregunta central en pantalla completa
- Formato destacado

**Guion:**
> "La pregunta que guía esta investigación es: ¿De qué manera un modelo basado en lógica difusa puede clasificar el comportamiento sedentario a partir de datos biométricos recopilados en condiciones de vida libre por dispositivos wearables?"

---

## DIAPOSITIVA 6: HIPÓTESIS
**Tiempo:** 45 segundos

**Contenido:**
- **Hipótesis Conceptual (HC):** La clasificación del sistema difuso exhibe alta concordancia con clasificación objetiva mediante clustering no supervisado
- **Hipótesis Nula (H₀):** No existe concordancia estadísticamente significativa

**Guion:**
> "Planteamos que la clasificación del comportamiento sedentario generada por el sistema de inferencia difusa, basado en reglas que integran biomarcadores de actividad y función cardiovascular, exhibe una alta concordancia con la clasificación objetiva obtenida mediante análisis de conglomerados no supervisado sobre los mismos datos."

---

## DIAPOSITIVA 7: OBJETIVO GENERAL
**Tiempo:** 30 segundos

**Contenido:**
- Objetivo general destacado

**Guion:**
> "El objetivo general es construir y validar un modelo interpretable, basado en lógica difusa, para la clasificación del comportamiento sedentario a partir de datos biométricos de wearables recopilados en condiciones de vida libre."

---

## DIAPOSITIVA 8: OBJETIVOS ESPECÍFICOS (Resumen)
**Tiempo:** 1 minuto

**Contenido:**
- 5 objetivos específicos en formato de viñetas concisas:
  1. Analizar datos biométricos longitudinales para derivar variables semanales
  2. Identificar perfiles mediante clustering no supervisado (ground truth)
  3. Diseñar sistema de inferencia difusa con reglas lingüísticas
  4. Evaluar desempeño mediante concordancia con clustering
  5. Examinar contribución de componentes mediante análisis de sensibilidad

**Guion:**
> "Los objetivos específicos incluyen: primero, analizar datos biométricos longitudinales para derivar variables semanales representativas; segundo, identificar perfiles de comportamiento mediante clustering no supervisado para establecer una clasificación de referencia empírica; tercero, diseñar un sistema de inferencia difusa con reglas lingüísticas fundamentadas fisiológicamente; cuarto, evaluar el desempeño mediante concordancia con los perfiles identificados; y quinto, examinar la contribución de cada componente mediante análisis de sensibilidad."

---

## DIAPOSITIVA 9: DISEÑO DEL ESTUDIO
**Tiempo:** 1 minuto 15 segundos

**Contenido:**
- **Paradigma:** Bring-Your-Own-Device (BYOD)
- **Cohorte:** N=10 (5F/5M), edad 34.2±6.7 años
- **Seguimiento:** Media 133.7 semanas (rango 7-298 semanas)
- **Datos totales:** 9,185 días, 1,337 semanas válidas
- **Dispositivo:** Apple Watch (PPG + acelerómetro)
- **Variables:** 4 variables normalizadas antropométricamente
  - Actividad_relativa
  - Superávit_calórico_basal
  - HRV_SDNN
  - Delta_cardiaco

**Guion:**
> "El estudio empleó un diseño longitudinal bajo el paradigma Bring-Your-Own-Device con una cohorte de 10 participantes adultos, con seguimiento medio de 133.7 semanas, acumulando 9,185 días de datos. Utilizamos Apple Watch para capturar datos de fotopletismografía y acelerometría. El modelo integra 4 variables normalizadas antropométricamente: actividad relativa, superávit calórico basal, variabilidad de frecuencia cardíaca y delta cardíaco."

---

## DIAPOSITIVA 10: METODOLOGÍA (Pipeline)
**Tiempo:** 1 minuto 30 segundos

**Contenido:**
- **Pipeline metodológico:**
  1. Preprocesamiento: imputación jerárquica, normalización
  2. Agregación semanal: medianas e IQR
  3. Clustering K-Means (K=2): Ground Truth operativa
  4. Sistema Difuso Mamdani: 4 variables, 5 reglas, funciones triangulares
  5. Validación LOUO: Leave-One-User-Out (10-fold)

**Guion:**
> "El pipeline metodológico incluye: preprocesamiento con imputación jerárquica y normalización antropométrica; agregación semanal mediante estadísticos robustos; establecimiento de verdad operativa mediante clustering K-Means con K=2; diseño de sistema difuso Mamdani con 4 variables de entrada, 5 reglas lingüísticas y funciones de membresía triangulares; y validación rigurosa mediante Leave-One-User-Out para evaluar generalización inter-sujeto."

---

## DIAPOSITIVA 11: RESULTADOS PRINCIPALES
**Tiempo:** 1 minuto 30 segundos

**Contenido:**
- **Rendimiento Global:**
  - F1-Score: 0.840
  - Accuracy: 0.740
  - Precision: 0.737
  - Recall: 0.976
  - MCC: 0.294
- **Validación LOUO:**
  - F1-Score: 0.780 ± 0.167 (CV=21.4%)
  - 7 de 10 usuarios con F1 ≥ 0.65
- **Comparación con literatura:** Competitivo con estudios de mayor N

**Guion:**
> "El sistema alcanzó un F1-Score global de 0.840 con alta sensibilidad de 0.976. La validación Leave-One-User-Out, que simula el despliegue real en nuevos usuarios, produjo un F1-Score de 0.780 con coeficiente de variación del 21.4%. Siete de diez usuarios alcanzaron F1-Score superior a 0.65, demostrando capacidad de generalización inter-sujeto robusta. Estos resultados son competitivos con estudios que emplean cohortes significativamente mayores."

---

## DIAPOSITIVA 12: HALLAZGO CLAVE: PARADOJA HRV
**Tiempo:** 1 minuto 15 segundos

**Contenido:**
- **Paradoja HRV:**
  - No significativo univariado: p=0.562, Cohen's d=0.051
  - Crítico multivariado: Ablación HRV → -50% F1-Score (0.840 → 0.420)
- **Interpretación:** Contribución sinérgica en contexto multivariado no lineal
- **Implicación:** Validación del diseño integral del modelo

**Guion:**
> "Un hallazgo contraintuitivo y fundamental emergió del análisis de robustez: la variabilidad de frecuencia cardíaca no mostró diferencia significativa entre grupos en análisis univariado, con p-valor de 0.562 y tamaño del efecto prácticamente nulo. Sin embargo, su eliminación del modelo provocó un colapso del 50% en el F1-Score, de 0.840 a 0.420. Esta paradoja demuestra que la HRV contribuye de forma sinérgica en el contexto multivariado no lineal, validando el diseño integral del modelo y el poder del enfoque basado en reglas para capturar relaciones fisiológicas complejas."

---

## DIAPOSITIVA 13: DISCUSIÓN E INTERPRETACIÓN
**Tiempo:** 1 minuto 30 segundos

**Contenido:**
- **Contribuciones metodológicas:**
  - Primer sistema híbrido clustering-difuso validado con LOUO
  - HRV como variable fisiológica para clasificación de sedentarismo
  - Interpretabilidad 100% mediante reglas lingüísticas
  - Validación con datos de vida libre multi-anual (BYOD)
  - Metodología validada para cohorte pequeña (N=10)
- **Limitaciones:**
  - Tamaño muestral (mitigado por densidad longitudinal)
  - Verdad operativa circular (clustering, no gold-standard clínico)
  - Dispositivo específico (Apple Watch)

**Guion:**
> "Esta investigación aporta cinco contribuciones metodológicas: es el primer sistema híbrido clustering-difuso validado con Leave-One-User-Out; incorpora HRV como variable fisiológica para clasificación de sedentarismo; ofrece interpretabilidad total mediante reglas lingüísticas auditables; valida con datos de vida libre multi-anual bajo paradigma BYOD; y demuestra metodología viable para cohortes pequeñas. Las limitaciones incluyen el tamaño muestral, mitigado por la densidad longitudinal, y la verdad operativa derivada de clustering en lugar de gold-standard clínico."

---

## DIAPOSITIVA 14: CONCLUSIONES
**Tiempo:** 1 minuto 15 segundos

**Contenido:**
- **Conclusión principal:** Sistema difuso validado con generalización inter-sujeto aceptable
- **Cumplimiento de objetivos:** Todos los objetivos específicos alcanzados
- **Cumplimiento de hipótesis:** Hipótesis conceptual aceptada (alta concordancia demostrada)
- **Relevancia:** Contribución al campo de IA explicable en salud digital
- **Aplicabilidad:** Base para intervenciones digitales personalizadas

**Guion:**
> "Concluimos que el sistema de inferencia difusa desarrollado logra clasificar el comportamiento sedentario con generalización inter-sujeto aceptable, cumpliendo todos los objetivos específicos y validando la hipótesis conceptual. Esta investigación contribuye al campo emergente de inteligencia artificial explicable aplicada a salud digital, proporcionando una base metodológica para el diseño de intervenciones digitales personalizadas y programas de monitoreo comunitario escalables."

---

## DIAPOSITIVA 15: CONTRIBUCIONES Y PROYECCIONES
**Tiempo:** 1 minuto

**Contenido:**
- **Contribuciones científicas:**
  - Metodología reproducible para estudios piloto (N<30)
  - Demostración de valor multivariado de HRV
  - Pipeline BYOD validado para investigación en salud
- **Proyecciones futuras:**
  - Escalabilidad a cohortes mayores
  - Integración con intervenciones digitales
  - Validación con gold-standard clínico

**Guion:**
> "Las contribuciones incluyen una metodología reproducible para estudios piloto con cohortes pequeñas, la demostración del valor multivariado de HRV en clasificación de sedentarismo, y un pipeline BYOD validado para investigación en salud. Las proyecciones futuras contemplan la escalabilidad a cohortes mayores, la integración con intervenciones digitales personalizadas, y la validación con gold-standard clínico para fortalecer la evidencia."

---

## DIAPOSITIVA 16: AGRADECIMIENTOS Y PREGUNTAS
**Tiempo:** 30 segundos

**Contenido:**
- Agradecimientos breves
- "¿Preguntas?"
- Información de contacto (opcional)

**Guion:**
> "Agradezco a mi comité tutorial, a los participantes del estudio, y a todas las personas que contribuyeron a este trabajo. Estoy abierto a sus preguntas y comentarios."

---

## DISTRIBUCIÓN DE TIEMPO TOTAL

| Sección | Tiempo | Acumulado |
|---------|--------|-----------|
| Portada | 0:10 | 0:10 |
| Tabla de Contenido | 0:30 | 0:40 |
| Contexto y Justificación | 1:15 | 2:00 |
| Problema de Investigación | 1:00 | 3:00 |
| Pregunta de Investigación | 0:30 | 3:30 |
| Hipótesis | 0:45 | 4:15 |
| Objetivo General | 0:30 | 4:45 |
| Objetivos Específicos | 1:00 | 5:45 |
| Diseño del Estudio | 1:15 | 7:00 |
| Metodología (Pipeline) | 1:30 | 8:30 |
| Resultados Principales | 1:30 | 10:00 |
| Hallazgo Clave (Paradoja HRV) | 1:15 | 11:15 |
| Discusión e Interpretación | 1:30 | 12:45 |
| Conclusiones | 1:15 | 14:00 |
| Contribuciones y Proyecciones | 1:00 | 15:00 |
| Agradecimientos | 0:30 | 15:30 |

**Total:** ~15 minutos 30 segundos (con margen para transiciones)

---

## RECOMENDACIONES PARA EL SINODAL

### Elementos que un sinodal espera ver:

1. **Problema de investigación claro** ✅ (Diapositiva 4)
2. **Justificación sólida** ✅ (Diapositiva 3)
3. **Pregunta de investigación explícita** ✅ (Diapositiva 5)
4. **Hipótesis formuladas** ✅ (Diapositiva 6)
5. **Objetivos alcanzables y medibles** ✅ (Diapositivas 7-8)
6. **Metodología rigurosa y reproducible** ✅ (Diapositivas 9-10)
7. **Resultados con métricas claras** ✅ (Diapositiva 11)
8. **Hallazgos significativos** ✅ (Diapositiva 12)
9. **Discusión crítica** ✅ (Diapositiva 13)
10. **Conclusiones fundamentadas** ✅ (Diapositiva 14)
11. **Contribuciones identificadas** ✅ (Diapositiva 15)

### Aspectos adicionales importantes:

- **Pivote metodológico:** Mencionar brevemente en Metodología (cambio de ANN supervisado a sistema difuso con clustering)
- **Tamaño de muestra:** Justificar N=10 en Diseño del Estudio (densidad longitudinal compensa)
- **Validación rigurosa:** Enfatizar LOUO como estándar para generalización inter-sujeto
- **Interpretabilidad:** Destacar como ventaja competitiva vs. modelos de caja negra

---

## CONSEJOS PARA LA PRESENTACIÓN

1. **Ritmo:** Mantener ~1 minuto por diapositiva, ajustar según complejidad
2. **Visualización:** Usar gráficos clave (PCA, perfiles clusters, análisis robustez)
3. **Números clave:** Memorizar: F1=0.780, N=10, 133.7 semanas, -50% ablación HRV
4. **Transiciones:** Conectar cada diapositiva con la siguiente ("Esto nos llevó a...", "Para abordar esto...")
5. **Énfasis:** Destacar interpretabilidad, validación LOUO, y paradoja HRV
6. **Preparación para preguntas:**
   - ¿Por qué N=10? → Densidad longitudinal, metodología validada
   - ¿Por qué clustering como ground truth? → Ausencia de gold-standard, enfoque data-driven
   - ¿Comparación con deep learning? → Interpretabilidad vs. precisión, aplicabilidad clínica
   - ¿Limitaciones? → Tamaño muestral, verdad operativa circular, dispositivo específico

---

## ELEMENTOS VISUALES RECOMENDADOS

- **Diapositiva 9:** Diagrama del diseño BYOD
- **Diapositiva 10:** Diagrama del pipeline metodológico
- **Diapositiva 11:** Tabla de resultados LOUO (resumida)
- **Diapositiva 12:** Gráfico de análisis de robustez (4V vs 2V)
- **Diapositiva 13:** Comparación con literatura (tabla resumida)

---

**¡Éxito en tu presentación, Luis!** 🎓⚡

