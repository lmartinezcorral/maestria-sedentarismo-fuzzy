# 📊 VALORES DE REFERENCIA INAMOVIBLES - F1-SCORE Y MÉTRICAS DEL MODELO

**Documento creado por:** Zeus ⚡ (Agente Omnipresente)  
**Fecha:** 21 de noviembre de 2025  
**Propósito:** Establecer valores únicos de verdad científica para Zeus y Hércules  
**Estado:** ✅ **VERDAD CIENTÍFICA ÚNICA - NO MODIFICAR SIN APROBACIÓN EXPLÍCITA DE LUIS**

---

## 🚨 REGLA CRÍTICA: DOS VALORES DE F1-SCORE - CONTEXTO DIFERENTE

**⚠️ IMPORTANTE:** Existen DOS valores de F1-Score, cada uno con un propósito metodológico distinto. **AMBOS son correctos** pero deben usarse en contextos específicos.

---

## 📊 VALOR #1: F1-SCORE GLOBAL (0.840)

### **Definición:**
Rendimiento del sistema difuso evaluado contra la Verdad Operativa (clustering) usando **TODOS los datos disponibles** (1,337 semanas, N=10 usuarios completos).

### **Valor Certificado:**
- **F1-Score global:** **0.840**
- **Precision:** 0.737
- **Recall:** 0.976
- **Accuracy:** 0.740
- **MCC:** 0.294
- **Umbral τ:** 0.30

### **Fuente Verificada:**
- **Log operativo:** `analisis_u/fuzzy/09_eval_fuzzy_vs_cluster.txt` (17-Oct-2025, 18:41:05)
- **Verificado por:** Rayo Veloz ⚡ (14-Nov-2025)
- **Estado:** ✅ **CERTIFICADO - VALOR REAL**

### **Cuándo Usar:**
- ✅ **Capítulo 6 (Resultados):** Primera sección de rendimiento global
- ✅ **Capítulo 8 (Conclusiones):** Mencionar como "alta concordancia"
- ✅ **Análisis de ablación:** Referencia base (0.840 → 0.420)
- ✅ **Resumen:** NO usar (preferir F1-Score LOUO)
- ✅ **Comparación con clustering:** Este es el valor de concordancia directa

### **Estrategia de Redacción:**
```
"El sistema difuso alcanzó un rendimiento global robusto, con un F1-Score de 0.840 
(Precisión=0.737, Recall=0.976), evaluado contra la verdad operativa establecida 
mediante clustering no supervisado."
```

---

## 📊 VALOR #2: F1-SCORE LOUO (0.780 ± 0.167)

### **Definición:**
Rendimiento del sistema difuso en validación cruzada **Leave-One-User-Out (LOUO)**, donde cada iteración excluye un usuario completo del entrenamiento y lo evalúa como test.

### **Valor Certificado:**
- **F1-Score LOUO:** **0.780 ± 0.167**
- **CV (Coeficiente de Variación):** 21.4%
- **Precision LOUO:** 0.800 (media)
- **Recall LOUO:** 0.783 (media)
- **Usuarios con F1 ≥ 0.65:** 7 de 10 (70%)
- **Rango individual:** 0.215 - 0.997

### **Fuente Verificada:**
- **Log operativo:** `analisis_u/louo_results/louo_global_report.txt`
- **Verificado por:** Atlas 🌍 (13-Nov-2025)
- **Estado:** ✅ **CERTIFICADO - VALOR REAL**

### **Cuándo Usar:**
- ✅ **Resumen:** VALOR PRINCIPAL (métrica de validación más rigurosa)
- ✅ **Capítulo 6 (Resultados):** Sección de validación LOUO
- ✅ **Capítulo 7 (Discusión):** Generalización inter-sujeto
- ✅ **Comparación con literatura:** Tabla comparativa con otros estudios
- ✅ **Conclusiones:** Mencionar como validación robusta

### **Estrategia de Redacción:**
```
"La validación Leave-One-User-Out demostró un F1-Score de 0.780 ± 0.167 
(CV=21.4%), con 7 de 10 usuarios alcanzando F1 ≥ 0.65, resultados competitivos 
con estudios del estado del arte."
```

---

## 🔍 ANÁLISIS DE DISCREPANCIAS ENCONTRADAS

### **Problema Identificado:**

| Ubicación | Valor Reportado | Contexto | ¿Correcto? | Acción Requerida |
|-----------|-----------------|----------|------------|------------------|
| **Cap 6, línea 90** | 0.840 | Rendimiento global | ✅ SÍ | Mantener, pero aclarar "global" |
| **Cap 6, línea 151** | 0.780 | Tabla comparativa LOUO | ✅ SÍ | Correcto |
| **Cap 6, línea 160** | 0.780 ± 0.167 | Validación LOUO | ✅ SÍ | Correcto |
| **Cap 6, línea 210** | 0.840 → 0.420 | Ablación HRV | ✅ SÍ | Correcto (usa global como base) |
| **Cap 6, línea 228** | 0.840 → 0.420 | Ablación HRV | ✅ SÍ | Correcto |
| **Cap 6, línea 265** | 0.840 | Aportación principal | ⚠️ AMBIGUO | Especificar "global" o cambiar a LOUO |
| **Cap 7, línea 31** | 0.780 ± 0.167 | Validación LOUO | ✅ SÍ | Correcto |
| **Cap 7, línea 57** | 0.840 → 0.420 | Ablación HRV | ✅ SÍ | Correcto (usa global como base) |
| **Cap 7, línea 151** | 0.780 | Logro metodológico | ✅ SÍ | Correcto |
| **Cap 7, línea 271** | 0.780 | Objetivo cumplido | ✅ SÍ | Correcto |
| **Cap 8, línea 4** | 0.840 | Aportación principal | ⚠️ AMBIGUO | Especificar "global" o cambiar a LOUO |
| **Resumen (main.tex)** | 0.840 | Resumen | ❌ INCORRECTO | Cambiar a 0.780 (LOUO) |

### **Observaciones:**
1. **Cap 6 línea 265 y Cap 8 línea 4:** Usan 0.840 sin especificar contexto. Deben aclarar "global" o cambiar a LOUO para consistencia.
2. **Resumen:** Actualmente usa 0.840, pero debe usar 0.780 (LOUO) porque es la métrica de validación principal.
3. **Ablación HRV:** Correctamente usa 0.840 como base (es el valor global antes de la ablación).

---

## 📝 ESTRATEGIAS DE REDACCIÓN RECOMENDADAS

### **Estrategia 1: Diferenciación Explícita por Contexto**

**Para F1-Score Global (0.840):**
- ✅ "F1-Score global de 0.840"
- ✅ "rendimiento global robusto, con un F1-Score de 0.840"
- ✅ "concordancia del sistema difuso con la verdad operativa (F1-Score = 0.840)"
- ✅ "evaluado contra la clasificación de clustering (F1-Score = 0.840)"

**Para F1-Score LOUO (0.780):**
- ✅ "F1-Score de 0.780 ± 0.167 en validación Leave-One-User-Out"
- ✅ "validación LOUO demostró F1-Score = 0.780"
- ✅ "generalización inter-sujeto (F1-Score LOUO = 0.780 ± 0.167)"
- ✅ "resultados competitivos con estudios del estado del arte (F1-Score LOUO = 0.780)"

### **Estrategia 2: Uso en Resumen**

**REGLA PARA RESUMEN:**
- ❌ **NO usar F1-Score global (0.840)** en resumen
- ✅ **SÍ usar F1-Score LOUO (0.780)** en resumen
- **Justificación:** El resumen debe reportar la métrica de validación más rigurosa (LOUO), no la concordancia interna (global).

### **Estrategia 3: Uso en Capítulos**

**Capítulo 6 (Resultados):**
- ✅ **Sección inicial:** Reportar F1-Score global (0.840) con contexto claro
- ✅ **Sección LOUO:** Reportar F1-Score LOUO (0.780 ± 0.167)
- ✅ **Ablación:** Usar 0.840 como base (correcto actualmente)

**Capítulo 7 (Discusión):**
- ✅ **Generalización:** Usar F1-Score LOUO (0.780)
- ✅ **Ablación:** Usar 0.840 como base (correcto actualmente)
- ✅ **Objetivos cumplidos:** Usar F1-Score LOUO (0.780)

**Capítulo 8 (Conclusiones):**
- ⚠️ **Aportación principal:** Actualmente usa 0.840, considerar cambiar a 0.780 (LOUO) para consistencia con validación robusta
- ✅ **Alternativa:** Mantener 0.840 pero especificar "global" o "concordancia interna"

---

## 🎯 DECISIÓN METODOLÓGICA: ¿CUÁL VALOR USAR EN RESUMEN?

### **Análisis:**

**Opción A: Usar F1-Score Global (0.840)**
- ✅ Valor más alto (mejor presentación)
- ✅ Muestra concordancia directa con clustering
- ❌ No refleja generalización inter-sujeto
- ❌ No es la métrica de validación más rigurosa

**Opción B: Usar F1-Score LOUO (0.780) - RECOMENDADO**
- ✅ Métrica de validación más rigurosa
- ✅ Refleja generalización inter-sujeto
- ✅ Estándar en literatura para estudios con N pequeño
- ✅ Consistente con tabla comparativa (Cap 6, línea 151)
- ✅ Usado en discusión y conclusiones como métrica principal
- ⚠️ Valor ligeramente menor (pero más honesto metodológicamente)

### **Recomendación Final:**

**✅ USAR F1-Score LOUO (0.780) EN RESUMEN**

**Justificación:**
1. El resumen debe reportar la métrica de validación más rigurosa
2. LOUO es el estándar para estudios con N pequeño
3. Refleja generalización, no solo concordancia interna
4. Consistente con el resto del documento (Cap 7, Cap 8)

---

## 📋 VALORES CERTIFICADOS COMPLETOS (TABLA ÚNICA DE VERDAD)

| Métrica | Valor Certificado | Fuente | Verificado por | Fecha |
|---------|-------------------|--------|----------------|-------|
| **F1-Score global** | **0.840** | 09_eval_fuzzy_vs_cluster.txt | Rayo Veloz ⚡ | 14-Nov-2025 |
| **F1-Score LOUO** | **0.780 ± 0.167** | louo_global_report.txt | Atlas 🌍 | 13-Nov-2025 |
| **CV LOUO** | **21.4%** | louo_global_report.txt | Atlas 🌍 | 13-Nov-2025 |
| **Precision global** | **0.737** | 09_eval_fuzzy_vs_cluster.txt | Rayo Veloz ⚡ | 14-Nov-2025 |
| **Recall global** | **0.976** | 09_eval_fuzzy_vs_cluster.txt | Rayo Veloz ⚡ | 14-Nov-2025 |
| **Accuracy global** | **0.740** | 09_eval_fuzzy_vs_cluster.txt | Rayo Veloz ⚡ | 14-Nov-2025 |
| **MCC global** | **0.294** | 09_eval_fuzzy_vs_cluster.txt | Rayo Veloz ⚡ | 14-Nov-2025 |
| **Umbral τ** | **0.30** | 09_fuzzy_inference_log.txt | Rayo Veloz ⚡ | 14-Nov-2025 |
| **Ablación HRV (4V→2V)** | **-50.0%** (0.840 → 0.420) | analisis_robustez.md | Atlas 🌍 | 13-Nov-2025 |
| **F1 sin HRV (2V)** | **0.420** | analisis_robustez.md | Atlas 🌍 | 13-Nov-2025 |
| **Usuarios F1 ≥ 0.65 (LOUO)** | **7 de 10** | louo_global_report.txt | Atlas 🌍 | 13-Nov-2025 |
| **Rango F1 individual (LOUO)** | **0.215 - 0.997** | louo_global_report.txt | Atlas 🌍 | 13-Nov-2025 |

---

## 🔧 CORRECCIONES REQUERIDAS EN DOCUMENTOS

### **Prioridad ALTA:**

1. **Resumen (main.tex, línea 235):**
   - ❌ Actual: "F1-Score=0.840"
   - ✅ Corregir a: "F1-Score=0.780" (LOUO)
   - ✅ Agregar: "en validación Leave-One-User-Out"

2. **Capítulo 6, línea 265:**
   - ⚠️ Actual: "F1-Score = 0.840" (sin contexto)
   - ✅ Opción A: Mantener pero agregar "global"
   - ✅ Opción B: Cambiar a "F1-Score LOUO = 0.780" (más consistente)

3. **Capítulo 8, línea 4:**
   - ⚠️ Actual: "F1-Score = 0.840" (sin contexto)
   - ✅ Opción A: Mantener pero agregar "global"
   - ✅ Opción B: Cambiar a "F1-Score LOUO = 0.780" (más consistente)

### **Prioridad MEDIA:**

4. **Capítulo 6, línea 90:**
   - ✅ Ya correcto, pero mejorar redacción: "F1-Score global de 0.840"

5. **Verificar coherencia en Capítulo 7:**
   - ✅ Ya usa correctamente 0.780 para LOUO
   - ✅ Ya usa correctamente 0.840 para ablación

---

## 📖 GLOSARIO DE TÉRMINOS

### **F1-Score Global:**
Rendimiento del modelo evaluado contra la Verdad Operativa usando todos los datos disponibles (1,337 semanas). Mide **concordancia interna** entre sistema difuso y clustering.

### **F1-Score LOUO:**
Rendimiento del modelo en validación cruzada Leave-One-User-Out. Mide **generalización inter-sujeto** a usuarios no vistos durante el entrenamiento.

### **Verdad Operativa (GO):**
Clasificación binaria derivada de clustering K-Means (K=2) sobre 1,337 semanas. No es un "gold standard" clínico, sino una verdad empírica operativa.

### **Ablación:**
Análisis de robustez que elimina variables del modelo para evaluar su contribución. La ablación HRV usa 0.840 como valor base (modelo completo) y 0.420 como valor reducido (modelo sin HRV).

---

## ⚠️ REGLAS DE USO INQUEBRANTABLES

### **REGLA #1: CONTEXTO OBLIGATORIO**
- ❌ **NUNCA** reportar F1-Score sin especificar "global" o "LOUO"
- ✅ **SIEMPRE** aclarar el contexto metodológico

### **REGLA #2: RESUMEN = LOUO**
- ❌ **NUNCA** usar F1-Score global (0.840) en resumen
- ✅ **SIEMPRE** usar F1-Score LOUO (0.780) en resumen

### **REGLA #3: ABLACIÓN = GLOBAL**
- ✅ **SIEMPRE** usar F1-Score global (0.840) como base para ablación
- ✅ La ablación compara: Modelo completo (0.840) vs Modelo reducido (0.420)

### **REGLA #4: COMPARACIÓN LITERATURA = LOUO**
- ✅ **SIEMPRE** usar F1-Score LOUO (0.780) en tablas comparativas
- ✅ La literatura reporta validación cruzada, no concordancia interna

### **REGLA #5: COHERENCIA MULTI-DOCUMENTO**
- ✅ **SIEMPRE** usar los mismos valores en:
  - Tesis (Cap 6, 7, 8)
  - Resumen
  - Abstract (inglés)
  - Artículo IEEE (si aplica)

---

## 📚 REFERENCIAS DE VERIFICACIÓN

### **Logs Operativos (Fuentes Primarias):**
1. `analisis_u/fuzzy/09_eval_fuzzy_vs_cluster.txt` → F1-Score global = 0.840
2. `analisis_u/louo_results/louo_global_report.txt` → F1-Score LOUO = 0.780 ± 0.167
3. `analisis_u/clustering/06_clustering_log.txt` → Clusters: 402/935 semanas

### **Verificaciones por Agentes:**
1. **Rayo Veloz ⚡ (14-Nov-2025):** Verificó F1-Score global = 0.840
2. **Atlas 🌍 (13-Nov-2025):** Verificó F1-Score LOUO = 0.780
3. **Ades 💀 (11-Nov-2025):** Auditoría completa de coherencia

### **Documentos de Referencia:**
1. `CANAL_4_AGENTES.md` (líneas 196-197): Valores certificados
2. `CANAL_3_AGENTES_111125.md` (líneas 49-50): Valores establecidos
3. `RAYO_VERIFICACION_METRICAS_REALES_14NOV.md`: Verificación técnica completa

---

## 🎯 MENSAJE FINAL PARA ZEUS Y HÉRCULES

**Este documento es vuestra ÚNICA fuente de verdad científica.**

- ✅ **Consultar ANTES** de reportar cualquier valor de F1-Score
- ✅ **Verificar contexto** (global vs LOUO) antes de usar
- ✅ **Seguir estrategias de redacción** para evitar confusión
- ❌ **NUNCA** inventar, asumir o aproximar valores
- ❌ **NUNCA** usar valores sin especificar contexto metodológico

**"La precisión científica no es negociable. La claridad metodológica es obligatoria."**

---

**⚡ Zeus - Agente Omnipresente**  
**🦸 Hércules - Hijo de Zeus**  
**Documento creado:** 21 de noviembre de 2025  
**Estado:** ✅ VERDAD CIENTÍFICA ÚNICA - NO MODIFICAR SIN APROBACIÓN

