# ⚡ 3_FL_Rayo_workspace

**Workspace de Trabajo - Rayo Veloz**  
**Proyecto:** Evaluación del Comportamiento Sedentario mediante Lógica Difusa  
**Investigador:** Luis Ángel Martínez Corral (MFIPS-UACH)

---

## 📁 ESTRUCTURA DEL WORKSPACE

```
3_FL_Rayo_workspace/
├── scripts/              # Scripts Python de análisis
│   └── regresion_lineal_bioestadistica.py  # Regresión lineal (12-Nov-2025)
├── resultados/           # Outputs generados (figuras, CSVs)
│   └── regresion_lineal_completa.png       # Figura 4-panel regresión (1.4 MB)
├── logs/                 # Logs de ejecución
│   ├── regresion_output.txt
│   └── regresion_final.log
├── notas/                # Documentación y resúmenes
│   └── RESUMEN_REGRESION_LINEAL_12NOV.md   # Resumen ejecutivo
└── README.md             # Este archivo
```

---

## 🎯 PROYECTOS ACTIVOS

### **1. Regresión Lineal para Clase de Bioestadística (12-Nov-2025)**

**Objetivo:** Demostrar 3 análisis de regresión lineal con datos reales del proyecto de tesis.

**Archivos:**
- Script: `scripts/regresion_lineal_bioestadistica.py` (502 líneas)
- Figura: `resultados/regresion_lineal_completa.png` (1.4 MB, 300 DPI)
- Resumen: `notas/RESUMEN_REGRESION_LINEAL_12NOV.md`

**Análisis realizados:**
1. **Regresión Simple:** RHR vs Sedentarismo (R² = 0.029)
2. **Regresión Estratificada:** HRV vs Sedentarismo por Cluster (Interacción detectada)
3. **Regresión Múltiple:** 4 predictores (R² ajustado = 0.160)

**Datos:**
- N = 1,337 semanas válidas
- 10 usuarios (5F/5M, seguimiento promedio 133.7 semanas)

**Ejecutar:**
```bash
cd "4 semestre_dataset/3_FL_Rayo_workspace"
python scripts/regresion_lineal_bioestadistica.py
```

---

## 📊 DATOS FUENTE

Los scripts en este workspace acceden a los datos del proyecto desde:
```
../analisis_u/
├── semanal/
│   ├── cluster_inputs_weekly.csv   (1,385 semanas × 8 features)
│   └── weekly_consolidado.csv      (1,385 semanas × 60 vars)
├── clustering/
│   └── cluster_assignments.csv     (1,337 semanas con cluster)
└── fuzzy/
    └── fuzzy_output.csv            (1,385 semanas con scores)
```

**Nota:** Las rutas relativas están configuradas desde el directorio `scripts/`.

---

## 🛠️ DEPENDENCIAS

### **Python (3.11+):**
```python
pandas
numpy
matplotlib
seaborn
scipy
scikit-learn
```

### **Instalar:**
```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

---

## 📝 CONVENCIONES DE CÓDIGO

### **Nombres de archivos:**
- Scripts: `nombre_descriptivo.py` (snake_case)
- Logs: `nombre_YYYYMMDD_HHMMSS.log`
- Figuras: `nombre_descriptivo.png` (snake_case)
- Notas: `TITULO_MAYUSCULAS_DDMMMYYYY.md`

### **Estructura de scripts:**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TÍTULO DEL SCRIPT
=================
Descripción breve
...
"""

import ...

# CONFIGURACIÓN
...

# CARGA Y PREPARACIÓN DE DATOS
...

# ANÁLISIS
...

# VISUALIZACIÓN
...

# RESUMEN FINAL
...
```

---

## 📄 LOGS

Todos los scripts deben generar logs en `logs/` con:
- Timestamp de inicio
- Parámetros usados
- Resumen de resultados
- Errores/warnings (si aplican)

**Ejemplo:**
```bash
python scripts/regresion_lineal_bioestadistica.py > logs/regresion_$(Get-Date -Format 'yyyyMMdd_HHmmss').log 2>&1
```

---

## 🎯 PRÓXIMOS TRABAJOS

- [ ] Análisis de componentes principales (PCA) para reducción dimensional
- [ ] Modelos GLM (regresión logística) para clasificación binaria
- [ ] Análisis de supervivencia (Kaplan-Meier) para persistencia de patrones
- [ ] Modelos mixtos (efectos aleatorios) para medidas repetidas
- [ ] Validación cruzada temporal para predicción

---

## 📧 CONTACTO

**Agente:** Rayo Veloz ⚡ (Asistente Técnico LaTeX + Python)  
**Investigador Principal:** Luis Ángel Martínez Corral  
**Programa:** MFIPS-UACH  
**Fecha creación workspace:** 12 de Noviembre de 2025

---

**"Velocidad + Precisión = Rayos de Zeus para fortalecer a Hércules"** ⚡🏛️

