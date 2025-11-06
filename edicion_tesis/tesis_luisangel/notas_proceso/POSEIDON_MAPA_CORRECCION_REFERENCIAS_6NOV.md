# 🔱 POSEIDÓN: Mapa de Corrección de Referencias BibTeX
**Fecha:** 6 de noviembre de 2025  
**Tarea:** ADES_R1 - Resolver 32 referencias undefined  
**Status:** En progreso

---

## 📊 RESUMEN EJECUTIVO

- **Total referencias citadas:** 108
- **Referencias undefined:** 32
- **Causa raíz:** Desalineación entre claves en `.tex` vs `.bib`
- **Solución:** Corrección sistemática de claves

---

## 🔍 MAPA DE CORRECCIONES (32 referencias)

### ✅ EXISTENTES - Solo requieren cambiar clave en `.tex`

| Clave citada (INCORRECTA)              | Clave en .bib (CORRECTA)        | Acción                    |
|-----------------------------------------|---------------------------------|---------------------------|
| `Riebe2018`                             | `Riebe2018ACSM`                 | ✅ YA CORREGIDO           |
| `Guthold2020GlobalTrends`               | `Guthold2020`                   | Reemplazar en .tex        |
| `DiPietro2020PhysicalActivity`          | `DiPietro2020Advancing`         | Reemplazar en .tex        |
| `Murray2020GlobalBurden`                | `Murray2020GBD`                 | Reemplazar en .tex        |
| `Okunogbe2021EconomicImpact`            | `Okunogbe2021Economic`          | Reemplazar en .tex        |
| `WHO2022AsambleaMundial`                | `WHO2022InformeActividad`       | Reemplazar en .tex        |
| `Chaves2017CapacidadAerobica`           | `Chaves2017Asociacion`          | Reemplazar en .tex        |
| `Rothney2008ValidityAccelerometers`     | `Rothney2008Validity`           | Reemplazar en .tex        |
| `Henriksen2018UsingSmartphone`          | `Henriksen2018`                 | Reemplazar en .tex        |
| `Bhuyan2016WearableDevices`             | `Bhuyan2016Mobile`              | Reemplazar en .tex        |
| `Tajammul2023WearablesMarket`           | `Tajammul2023Statistics`        | Reemplazar en .tex        |
| `Wright2017ValidityWearables`           | `Wright2017ConsumerMonitors`    | Reemplazar en .tex        |
| `Dinesh2014ValidityActiGraph`           | `Dinesh2014ActiGraph`           | Reemplazar en .tex        |
| `Redenius2019ValidityFitbit`            | `Redenius2019Fitbit`            | Reemplazar en .tex        |
| `White2019BiosensorsPhysicalActivity`   | `White2019`                     | Reemplazar en .tex        |
| `Strain2020WristAccelerometry`          | `Strain2020`                    | Reemplazar en .tex        |
| `Amit2001FeatureExtraction`             | `Amit2001Computational`         | Reemplazar en .tex        |
| `Levitz1979Incompatibility`             | `Levitz1979Logic`               | Reemplazar en .tex        |
| `Strefezza2009FuzzyLogic`               | `Strefezza2009Logica`           | Reemplazar en .tex        |
| `Katzmarzyk2023Sedentary`               | `Katzmarzyk2023Impact`          | Reemplazar en .tex        |
| `Santos2023Sedentary`                   | `Santos2023CostInaction`        | Reemplazar en .tex        |
| `Healy2024ValiditySedentary`            | `Healy2024`                     | Reemplazar en .tex        |
| `Migueles2022AccelerometerData`         | `Migueles2022GRANADA`           | Reemplazar en .tex        |
| `Deka2023MachineLearning`               | `Deka2023Nonlinear`             | Reemplazar en .tex        |
| `Vellido2020ExplainableAI`              | `Vellido2020Importance`         | Reemplazar en .tex        |
| `Meusel2006StrategiaGlobal`             | `Meusel2006Framework`           | Reemplazar en .tex        |

**Subtotal:** 26 referencias existentes

---

### ❌ FALTANTES - Requieren añadir entrada en `.bib`

| Clave citada                      | Status                                |
|-----------------------------------|---------------------------------------|
| `Torres2023Fotopletismografia`    | ❌ NO EXISTE - Añadir entrada BibTeX  |
| `Rodriguez2021MonitoresFitness`   | ❌ NO EXISTE - Añadir entrada BibTeX  |
| `GPAQ2012AnalysisGuide`           | ❌ NO EXISTE - Añadir entrada BibTeX  |
| `Tsoukalas1997FuzzyControl`       | ❌ NO EXISTE - Añadir entrada BibTeX  |
| `Lu2022MeasurementSedentary`      | ❌ NO EXISTE - Añadir entrada BibTeX  |
| `Aubert2022HeartRate`             | ❌ NO EXISTE - Añadir entrada BibTeX  |

**Subtotal:** 6 referencias faltantes

---

## 📋 PLAN DE ACCIÓN

### FASE 1: Corrección de claves en `.tex` (26 reemplazos) - 20 min
- Buscar y reemplazar cada clave incorrecta por la correcta
- Prioridad: Capítulos 1, 2, 4, 5, 6, 7

### FASE 2: Añadir 6 referencias faltantes en `.bib` - 30 min
- Buscar DOI/información completa
- Crear entradas BibTeX válidas
- Insertar en `referencias.bib`

### FASE 3: Recompilación y verificación - 10 min
- Ejecutar `compilar.bat`
- Verificar 0 warnings de Biber
- Confirmar PDF con referencias completas

**TIEMPO TOTAL ESTIMADO:** 1h 0min

---

## 🔧 SIGUIENTE PASO

Iniciar FASE 1 con reemplazos sistemáticos.

---

**Poseidón - Curador Científico Senior** 🔱

