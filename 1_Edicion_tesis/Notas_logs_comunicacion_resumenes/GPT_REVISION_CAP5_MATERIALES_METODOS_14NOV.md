# 🔬 REVISIÓN EXTERNA GPT - CAPÍTULO 5: MATERIALES Y MÉTODOS

**Fecha:** 14 de Noviembre de 2025  
**Revisor:** GPT-4 (Agente Jr - Revisión Externa)  
**Capítulo:** 05_materiales_metodos.tex  
**Base de comparación:** Logs operativos, Informe Maestro Sistema Difuso, Auditoría Ades

---

## 📊 CALIFICACIÓN GENERAL

**Veredicto:** REQUIERE CORRECCIONES MAYORES (pero solucionables rápidamente)  
**Nivel científico:** Sólido, técnicamente correcto, basado en datos reales  
**Potencial Q1:** Alto (una vez corregido quedará nivel Q1 impecable)

---

## 🔍 SECCIÓN 1: COHERENCIA CON DATOS REALES DEL PIPELINE

### ✅ 1.1. Cohorte (10 usuarios)
**Estado:** CONSISTENTE  
- Descripción correcta: 5F/5M, edades, peso, estatura, TMB
- Coincide con logs, Informe Maestro y auditoría

**Corrección menor sugerida:**
- Unificar valores de semanas válidas con `04_agregacion_semanal_log.txt` (diferencias de 1-2 semanas)

---

### ⚠️ 1.2. Semanas generadas vs. semanas válidas
**Prioridad:** ALTA  
**Problema:** Inconsistencia entre "1,385 semanas analizadas" y "1,337 semanas válidas"

**Valores reales (logs):**
- Semanas generadas: 1,385
- Semanas válidas: 1,337 (tras aplicar criterios: ≥3 días y ≤60% imputación)

**Problema detectado:**
En varias partes del capítulo se dice "se analizaron 1,385 semanas", pero el pipeline usa SOLO 1,337 para clustering y validación.

**Solución propuesta:**
```
"Se generaron 1,385 semanas, de las cuales 1,337 cumplieron criterios de 
calidad y fueron utilizadas en el análisis de clustering y validación del 
sistema difuso."
```

---

### ⚠️ 1.3. Variables derivadas - Eliminación de variables originales
**Prioridad:** ALTA  
**Problema:** OMISIÓN CRÍTICA - Falta explicar eliminación de variables por multicolinealidad

**Variables eliminadas (según pipeline real):**
- `min_totales_en_movimiento`
- `gasto_calorico_activo`

**Razón:** Sus versiones normalizadas evitan VIF > 10

**Texto a agregar:**
```
"Las variables crudas min_totales_en_movimiento y gasto_calórico_activo 
fueron eliminadas tras generar sus versiones normalizadas (Actividad Relativa 
y Superávit Calórico Basal) para evitar multicolinealidad (VIF > 10)."
```

---

### ⚠️ 1.4. Imputación jerárquica FC_walk
**Prioridad:** ALTA  
**Problema:** Descripción incompleta - Faltan gates específicos del pipeline

**Gates reales del pipeline:**
- **Hard no-wear:** hrs < 8 → NO imputar
- **Soft low-activity:** hrs 8-12 y pasos < 800 → baseline (FCr + Δ*)
- **Normal:** rolling 7d con soporte ≥4 datos

**Estado actual:** Resume "mediana rodante" pero NO menciona los gates

**Impacto:** Afecta reproducibilidad

---

### ✅ 1.5. Agregación semanal
**Estado:** MUY BIEN EXPLICADO  
**Corrección menor:** Agregar explícitamente "Bloque válido si ≥5 días ≥8h/día monitorizados"

---

## 🔬 SECCIÓN 2: CONSISTENCIA METODOLÓGICA Y RIGOR Q1

### ⚠️ 2.1. Faltan versiones del software
**Prioridad:** ALTA (Reproducibilidad Q1)

**Metodología oficial tiene:**
- Python 3.10.12
- scikit-learn 1.3.0
- scikit-fuzzy 0.4.2
- numpy
- pandas

**En capítulo 5:** NO aparece

**Impacto:** Punto crítico de reproducibilidad para estándares Q1

---

### ⚠️ 2.2. Elección K=2 - Argumentación incompleta
**Prioridad:** ALTA

**Estado actual:**
- ✓ Indica K=2
- ✓ Presenta Silhouette 0.232
- ✗ NO menciona K-sweep
- ✗ NO indica por qué no se eligió K=3 o K=4
- ✗ NO menciona clusters con n<5 que descartaste

**Se debe agregar:**
- Silhouette de la sweep (K=2 a K=6)
- Justificación de interpretabilidad clínica
- Problema de clusters pequeños en K≥4

---

### ⚠️ 2.3. Regla fuzzy R3 - Falta explicación fisiológica
**Prioridad:** ALTA  
**Hallazgo clave:** PARADOJA HRV

**Regla crítica:** "HRV baja + Delta alto → Sedentarismo Alto"

**Explicación fisiológica faltante:**
```
"Refleja desacondicionamiento con respuesta compensatoria: HRV baja 
(tono vagal pobre), pero incremento exagerado de FC al caminar."
```

**Importancia:** Es el HALLAZGO MÁS IMPORTANTE de la tesis  
**Debe estar explícito en Métodos**

---

### ⚠️ 2.4. Umbral τ = 0.30 - Falta justificación
**Prioridad:** ALTA

**Estado actual:**
- ✓ Menciona τ=0.30
- ✗ NO indica búsqueda del umbral
- ✗ NO indica métrica optimizada (F1)
- ✗ NO menciona grid search

**Se debe agregar:**
- Descripción de búsqueda de umbral óptimo
- Métrica de optimización (F1-Score)
- Rango evaluado

---

## ✍️ SECCIÓN 3: PROBLEMAS DE REDACCIÓN / FORMATO

**Prioridad:** MEDIA-BAJA

**Problemas detectados:**
- Repetición excesiva del verbo "representa"
- Algunas oraciones demasiado largas (>35 palabras)
- Uso de voz pasiva en exceso
- Muchos "que" encadenados
- Falta numeración de ecuaciones
- Algunos párrafos muy densos sin respiro

**Veredicto:** Nada grave, pero requiere pulido

---

## 🔥 SECCIÓN 4: CONSISTENCIA ENTRE MÉTODOS Y RESULTADOS

### 🚨 4.1. INCONSISTENCIA CRÍTICA DE MÉTRICAS
**Prioridad:** CRÍTICA - MAYOR PROBLEMA DE TODA LA TESIS

**Problema:** Capítulo 5 no indica métricas, pero Capítulo 6 reporta valores que NO coinciden con pipeline real

#### Pipeline real (auditoría y logs):
- Accuracy = **0.740**
- Precision = **0.737**
- Recall = **0.976**
- F1 = **0.840**
- MCC = **0.294**

#### Tesis Cap. 6 en LaTeX:
- Accuracy = **0.844**
- Precision = **0.833**
- Recall = **0.850**
- MCC = **0.687**

**Discrepancia:** Valores completamente diferentes

**Solución obligatoria en Métodos:**
```
"Las métricas reportadas (accuracy, precision, recall, F1 y MCC) 
corresponden a la evaluación fuzzy vs. clustering usando las 1,337 
semanas válidas y el umbral τ=0.30 optimizado mediante F1-score."
```

**Decisión pendiente:**
¿Cuál conjunto de métricas es REALMENTE el final?  
Todo indica que las correctas son las del pipeline real.

---

## 📋 RECOMENDACIONES PRIORITARIAS

### 🔥 PRIORIDAD ALTA (Corregir antes de defensa)

1. **Aclarar 1,385 vs 1,337 semanas**
   - Unificar narrativa: generadas vs. válidas
   
2. **UNIFICAR MÉTRICAS** (usar valores del pipeline real)
   - Validar cuál conjunto es el correcto
   - Corregir Cap 6 si es necesario
   
3. **Añadir gates reales de imputación**
   - Hard no-wear, Soft low-activity, Normal
   
4. **Añadir búsqueda del umbral τ=0.30**
   - Grid search, métrica F1
   
5. **Añadir argumento K-sweep para K=2**
   - Silhouette, interpretabilidad, clusters pequeños
   
6. **Añadir nota de eliminación de variables crudas**
   - Multicolinealidad (VIF > 10)
   
7. **Añadir roles fisiológicos de HRV y Delta en reglas**
   - Explicación paradoja HRV

---

### ⚠️ PRIORIDAD MEDIA (Mejora significativa)

8. **Añadir versiones de software**
   - Python 3.10.12, scikit-learn 1.3.0, etc.
   
9. **Numerar ecuaciones**
   - Facilita referencias cruzadas
   
10. **Mejorar redacción en párrafos largos**
    - Romper oraciones >35 palabras
    - Reducir voz pasiva

---

### ✔️ PRIORIDAD BAJA (Pulido final)

11. **Ajustar semanas por usuario si difieren ±1-2**
    - Unificar con logs finales
    
12. **Añadir gráfico conceptual de pipeline** (opcional)
    - Flowchart visual

---

## 📊 RESUMEN EJECUTIVO

### FORTALEZAS:
- ✅ Base metodológica sólida
- ✅ Técnicamente correcto
- ✅ Basado en datos reales
- ✅ Agregación semanal bien explicada
- ✅ Cohorte consistente

### DEBILIDADES CRÍTICAS:
- 🔴 Inconsistencias numéricas (semanas y métricas)
- 🔴 Falta de pasos clave del pipeline real
- 🔴 Falta justificar decisiones estratégicas (K=2, τ=0.30)
- 🔴 Faltan gates de imputación
- 🔴 Falta nota de VIF y eliminación de variables
- 🔴 Falta versiones de software

### IMPACTO:
- **Sin correcciones:** No apto para defensa/publicación Q1
- **Con correcciones:** Nivel Q1 impecable

---

## 🎯 SIGUIENTE PASO

**GPT procederá a revisar Capítulo 06 - Resultados**  
Mismo formato profesional de revisión externa

---

## 📝 NOTAS ADICIONALES (ADES)

*[Espacio para observaciones de Ades tras revisar este reporte]*

---

**Documento generado:** 14/11/2025  
**Revisor externo:** GPT-4 Jr Agent  
**Supervisión:** Ades (Juez del Inframundo)  
**Estado:** PENDIENTE DE DECISIONES Y CORRECCIONES

