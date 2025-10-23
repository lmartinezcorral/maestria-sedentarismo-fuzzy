# Instrucciones para Generar Presentación PowerPoint

## 🚀 Opción 1: Usando el Script Python (Recomendada)

Ya tienes el script `generar_presentacion_pptx.py` creado. Para ejecutarlo:

### Paso 1: Instalar python-pptx

```powershell
pip install --user python-pptx
```

**Esperado:** Instalación exitosa de `python-pptx`, `lxml`, `XlsxWriter`, `typing-extensions`

### Paso 2: Ejecutar el script

```powershell
# Ya estás en: 4 semestre_dataset
python generar_presentacion_pptx.py
```

**Resultado:** Se generará `PRESENTACION_SISTEMA_DIFUSO_SEDENTARISMO.pptx` (18 slides)

### Paso 3: Abrir la presentación

```powershell
Start-Process PRESENTACION_SISTEMA_DIFUSO_SEDENTARISMO.pptx
```

---

## 🌐 Opción 2: Usar Google Slides (Si python-pptx falla)

Si tienes problemas con la instalación, usa esta alternativa:

### Paso 1: Crear presentación en Google Slides

1. Ir a https://slides.google.com
2. Crear presentación nueva
3. Usar los contenidos del archivo `CONTENIDO_SLIDES.md` (generado a continuación)

### Paso 2: Insertar figuras manualmente

Todas las figuras están en: `analisis_u/fuzzy/plots/`

- `MF_Actividad_relativa_p50.png`
- `MF_Superavit_calorico_basal_p50.png`
- `MF_HRV_SDNN_p50.png`
- `MF_Delta_cardiaco_p50.png`
- `confusion_matrix.png`
- `pr_curve.png`
- `score_distribution_by_cluster.png`
- `sedentarismo_score_histogram.png`

---

## 📊 Opción 3: Usar PowerPoint Desktop Manualmente

Si prefieres crear la presentación directamente en PowerPoint:

### Plantilla de 18 Slides:

1. **Título:** Sistema de Inferencia Difusa para Evaluación del Comportamiento Sedentario
2. **Objetivos:** Objetivo principal + 6 específicos
3. **Datos y Cohorte:** Tabla de 10 usuarios con características
4. **Variables Clave:** 4 variables derivadas (Actividad_relativa, Superávit, HRV, Delta)
5. **Pipeline:** 5 fases metodológicas
6. **Clustering:** K=2, tabla de K-sweep
7. **MF 1:** Actividad_relativa (figura PNG)
8. **MF 2:** Superávit_calórico (figura PNG)
9. **MF 3:** HRV_SDNN (figura PNG)
10. **MF 4:** Delta_cardiaco (figura PNG)
11. **Sistema Difuso:** 5 reglas Mamdani
12. **Métricas Globales:** F1=0.84, Recall=97.6%, Accuracy=74.0%
13. **Matriz de Confusión:** Figura PNG + tabla TN/FP/FN/TP
14. **Curvas:** PR curve + distribución de scores (2 figuras lado a lado)
15. **Concordancia:** Tabla por usuario (27.7%-99.3%)
16. **Conclusiones:** 5 puntos clave
17. **Próximos Pasos:** Corto, mediano, largo plazo
18. **Agradecimientos:** Contacto

---

## ⚠️ Solución de Problemas

### Error: "Permission denied" al instalar python-pptx

**Solución 1:** Usar `--user`
```powershell
pip install --user python-pptx
```

**Solución 2:** Ejecutar PowerShell como Administrador

**Solución 3:** Usar Opción 2 o 3 (Google Slides o PowerPoint manual)

### Error: "No such file or directory"

**Causa:** Ruta incorrecta. 

**Solución:** Asegúrate de estar en el directorio correcto:
```powershell
cd "C:\Users\hulkmtz\Documents\luis angel\Maestria\Asesoria\Semestre 3\Convocatoria\Datos\4 semestre_dataset"
python generar_presentacion_pptx.py
```

### Error: "ModuleNotFoundError: No module named 'pptx'"

**Causa:** python-pptx no está instalado.

**Solución:** Ejecutar `pip install --user python-pptx` primero.

---

## 📋 Checklist de Ejecución

- [ ] Instalé python-pptx con `pip install --user python-pptx`
- [ ] Estoy en el directorio `4 semestre_dataset`
- [ ] Ejecuté `python generar_presentacion_pptx.py`
- [ ] Se generó el archivo `PRESENTACION_SISTEMA_DIFUSO_SEDENTARISMO.pptx`
- [ ] Abrí la presentación con PowerPoint
- [ ] Revisé los 18 slides
- [ ] Todas las figuras se muestran correctamente

---

## 🎨 Personalizar la Presentación

Si deseas cambiar colores, fuentes o layout, edita las siguientes líneas en `generar_presentacion_pptx.py`:

```python
# Líneas 18-21: Colores del tema
COLOR_TITULO = RGBColor(0, 51, 102)      # Azul oscuro
COLOR_SUBTITULO = RGBColor(51, 102, 153) # Azul medio
COLOR_TEXTO = RGBColor(64, 64, 64)       # Gris oscuro
COLOR_ACENTO = RGBColor(0, 176, 80)      # Verde para highlights
```

Luego vuelve a ejecutar el script.

---

## 💡 Tips para la Presentación

### Timing Recomendado (60 minutos total)

- Slides 1-2 (Título + Objetivos): 3 min
- Slides 3-5 (Datos + Variables + Pipeline): 8 min
- Slide 6 (Clustering): 5 min
- Slides 7-10 (Funciones de Membresía): 10 min (2.5 min c/u)
- Slide 11 (Sistema Difuso): 5 min
- Slides 12-14 (Métricas + Visualizaciones): 10 min
- Slide 15 (Concordancia por usuario): 5 min
- Slides 16-17 (Conclusiones + Próximos pasos): 10 min
- Slide 18 (Agradecimientos + Preguntas): 4 min

### Preguntas Anticipadas

**P1: "¿Por qué K=2 y no K=3 o K=4?"**
- R: K=2 maximiza Silhouette (0.232) y ofrece interpretación clínica clara (Alto/Bajo Sedentarismo). K>2 introduce complejidad sin ganancia de separabilidad.

**P2: "¿Por qué τ=0.30 y no otro valor?"**
- R: Búsqueda exhaustiva de umbral que maximiza F1-score (0.84). Balance óptimo entre Precision (73.7%) y Recall (97.6%).

**P3: "¿Cómo manejan los 325 falsos positivos?"**
- R: Política conservadora para screening: preferible alertar de más (con confirmación clínica) que pasar por alto casos de riesgo. Zona gris (0.40-0.60) requiere evaluación adicional.

**P4: "¿Generaliza a otras cohortes?"**
- R: Funciones de membresía por percentiles → fácil recalibración. Estructura de reglas transferible. Validación externa necesaria antes de despliegue clínico.

**P5: "¿Por qué baja concordancia en u3 y u8?"**
- R: Alta variabilidad intra-semanal (IQR alto). Clustering agrupa por promedios; fuzzy captura extremos. Personalización de τ por usuario puede mejorar concordancia.

---

## 📧 Exportar a PDF

Si necesitas PDF en lugar de PPTX:

### Desde PowerPoint
1. Abrir `PRESENTACION_SISTEMA_DIFUSO_SEDENTARISMO.pptx`
2. Archivo → Guardar como → PDF
3. Opciones: Incluir notas del orador (opcional)

### Desde Google Slides
1. Subir PPTX a Google Drive
2. Abrir con Google Slides
3. Archivo → Descargar → PDF

---

## ✅ Resultado Final

**Archivo:** `PRESENTACION_SISTEMA_DIFUSO_SEDENTARISMO.pptx`

**Contenido:**
- 18 slides profesionales
- 8 figuras PNG insertadas (300 dpi)
- 4 tablas con datos de cohorte, métricas, concordancia
- Colores coherentes (azul/verde)
- Fuentes legibles (Calibri/Arial)
- Layout limpio y profesional

**Tamaño:** ~5-10 MB (dependiendo de las figuras)

---

**¡Listo para presentar al comité tutorial!** 🎉




