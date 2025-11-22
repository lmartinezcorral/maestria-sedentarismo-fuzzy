# 🔄 CONFIGURAR MENDELEY - SINCRONIZACIÓN AUTOMÁTICA CON LaTeX

**Para:** Luis Angel Martínez Corral  
**Autor:** Poseidón 🔱  
**Fecha:** 4 de Noviembre de 2025  
**Tiempo estimado:** 10 minutos

---

## 🎯 **OBJETIVO**

Configurar Mendeley Desktop para que **automáticamente exporte** tus referencias a un archivo `.bib` cada vez que hagas cambios, eliminando la necesidad de exportación manual.

---

## ✅ **MÉTODO RECOMENDADO: Auto-Sync BibTeX**

### **PASO 1: Crear Carpeta Específica en Mendeley para la Tesis** ⏱️ 2 min

1. Abre **Mendeley Desktop**
2. En el panel izquierdo, click derecho en "**My Library**"
3. Selecciona "**Create Folder...**"
4. Nombre: `TESIS_MAESTRIA_SEDENTARISMO`
5. Arrastra las referencias relevantes a esta carpeta (solo las que usarás en la tesis)

**¿Por qué esto?**
- Tu `mendely_library.bib` tiene **4,337 líneas** (toda tu biblioteca)
- Solo necesitas ~80 referencias para la tesis
- Mantener bibliotecas separadas evita confusión

---

### **PASO 2: Habilitar BibTeX Syncing** ⏱️ 3 min

1. En Mendeley Desktop: **Tools → Options** (o `Ctrl+,`)
2. Ve a la pestaña "**BibTeX**"
3. ✅ Marca la casilla **"Enable BibTeX syncing"**
4. Click en "**Browse...**" para seleccionar carpeta de destino:
   ```
   C:\Users\hulkmtz\Documents\luis angel\Maestria\Asesoria\Semestre 3\Convocatoria\Datos\4 semestre_dataset\edicion_tesis\tesis_luisangel\
   ```
5. (Opcional) ✅ Marca **"Escape LaTeX special characters"**
6. (Opcional) ✅ Marca **"Create one BibTeX file per collection"**
   - Esto creará un archivo `.bib` específico para tu carpeta "TESIS_MAESTRIA_SEDENTARISMO"
7. Click "**OK**"

**RESULTADO:**
- Mendeley creará automáticamente: `TESIS_MAESTRIA_SEDENTARISMO.bib`
- Cada vez que agregues/modifiques referencias, el archivo se actualiza automáticamente

---

### **PASO 3: Configurar LaTeX para Usar el Archivo Auto-Sync** ⏱️ 2 min

En `plantilla_tesis.tex`, actualiza esta línea:

```latex
% ANTES:
\addbibresource{referencias.bib}

% DESPUÉS:
\addbibresource{TESIS_MAESTRIA_SEDENTARISMO.bib}
```

**¿Prefieres mantener `referencias.bib` como nombre?**
- Renombra el archivo auto-generado:
  ```bash
  # En la carpeta de tesis, ejecuta cada vez que Mendeley actualice:
  copy TESIS_MAESTRIA_SEDENTARISMO.bib referencias.bib
  ```
- O usa un symbolic link (Windows):
  ```bash
  mklink referencias.bib TESIS_MAESTRIA_SEDENTARISMO.bib
  ```

---

### **PASO 4: Probar la Sincronización** ⏱️ 3 min

1. En Mendeley, agrega una referencia de prueba a la carpeta "TESIS_MAESTRIA_SEDENTARISMO"
2. Espera 5 segundos
3. Ve a la carpeta de tu tesis y abre `TESIS_MAESTRIA_SEDENTARISMO.bib`
4. Verifica que la nueva referencia aparezca al final
5. ✅ Si aparece: **¡Sincronización funciona!**
6. ❌ Si NO aparece: Revisa que "Enable BibTeX syncing" esté marcado

---

## 🔄 **FLUJO DE TRABAJO COMPLETO (Futuro)**

```
1. Encuentro paper interesante (PDF)
   ↓
2. Arrastro PDF a Mendeley Desktop
   ↓
3. Mendeley extrae metadatos automáticamente
   ↓
4. Añado paper a carpeta "TESIS_MAESTRIA_SEDENTARISMO"
   ↓
5. Mendeley auto-exporta a .bib (instantáneo)
   ↓
6. En LaTeX, cito con \cite{clave}
   ↓
7. Compilo: pdflatex → biber → pdflatex → pdflatex
   ↓
8. ¡PDF con referencias actualizadas! ✅
```

---

## ⚙️ **CONFIGURACIÓN AVANZADA (Opcional)**

### **Personalizar Claves de Citación (Citation Keys)**

Por defecto, Mendeley genera claves como: `Apellido2024a`

**Para personalizar:**
1. `Tools → Options → BibTeX`
2. En "Citation key format" selecciona:
   - **Simple:** `[auth][year]` → `Martinez2024`
   - **Con título:** `[auth][year][shorttitle]` → `Martinez2024Fuzzy`
   - **Personalizado:** `[auth:lower][year]` → `martinez2024`

**MI RECOMENDACIÓN:**
- Usar: `[auth][year]` (simple y limpio)

---

### **Actualización Automática vs Manual**

**Modo Automático (Recomendado):**
- ✅ Mendeley actualiza `.bib` cada vez que modificas algo
- ✅ No necesitas recordar exportar
- ⚠️ Archivo .bib puede cambiar mientras compilas LaTeX (raramente causa problemas)

**Modo Manual (Más Control):**
1. Desmarca "Enable BibTeX syncing"
2. Cuando necesites actualizar:
   - Selecciona carpeta "TESIS_MAESTRIA_SEDENTARISMO"
   - `File → Export...`
   - Formato: BibTeX
   - Guardar como `referencias.bib`

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Problema 1: Mendeley no exporta automáticamente**

**Causa:** BibTeX syncing no habilitado

**Solución:**
1. `Tools → Options → BibTeX`
2. ✅ Marcar "Enable BibTeX syncing"
3. Reiniciar Mendeley Desktop

---

### **Problema 2: Archivo .bib vacío o con pocas referencias**

**Causa:** Carpeta incorrecta seleccionada para sync

**Solución:**
1. Verifica en `Options → BibTeX` que la carpeta de destino sea correcta
2. Asegúrate de que las referencias estén en la carpeta correcta de Mendeley

---

### **Problema 3: Caracteres especiales mal codificados**

**Causa:** Configuración de encoding

**Solución:**
1. En Mendeley: `Options → BibTeX`
2. ✅ Marcar "Escape LaTeX special characters"
3. En LaTeX, asegúrate de tener: `\usepackage[utf8]{inputenc}`

---

### **Problema 4: Claves de citación duplicadas**

**Causa:** Mendeley genera claves idénticas (ej: Martinez2024a, Martinez2024b)

**Solución:**
1. En Mendeley, edita la referencia
2. Click en "Citation Key" (abajo a la derecha)
3. Personaliza manualmente: `Martinez2024Fuzzy`, `Martinez2024Tesis`, etc.

---

## 🎯 **ALTERNATIVA: Usar Zotero (Si prefieres)**

Zotero tiene mejor integración con LaTeX que Mendeley:

**Ventajas de Zotero:**
- ✅ Better BibTeX plugin (más potente)
- ✅ Auto-sync más estable
- ✅ Mejor manejo de caracteres especiales
- ✅ Gratis y open-source

**Instalación Zotero + Better BibTeX:**
1. Instala Zotero: https://www.zotero.org/
2. Instala plugin Better BibTeX: https://retorque.re/zotero-better-bibtex/
3. Configura auto-export en `Preferences → Better BibTeX → Automatic Export`

**NOTA:** Si ya invertiste tiempo en Mendeley, **quédate con Mendeley**. El cambio no vale la pena a menos que tengas problemas graves.

---

## ✅ **CHECKLIST DE CONFIGURACIÓN**

Marca al completar:

- [ ] Mendeley Desktop instalado y funcionando
- [ ] Carpeta "TESIS_MAESTRIA_SEDENTARISMO" creada
- [ ] Referencias relevantes movidas a la carpeta
- [ ] BibTeX syncing habilitado en Options
- [ ] Carpeta de destino configurada correctamente
- [ ] Archivo `.bib` auto-generado aparece en carpeta tesis
- [ ] LaTeX usa `\addbibresource{NOMBRE_ARCHIVO.bib}`
- [ ] Compilación de prueba exitosa
- [ ] Referencias aparecen correctamente en PDF

---

## 📚 **RECURSOS ADICIONALES**

### **Documentación Oficial:**
- **Mendeley + BibTeX:** https://www.mendeley.com/guides/using-citation-plugins/
- **biblatex-apa:** https://ctan.org/pkg/biblatex-apa
- **APA 7 Manual:** https://apastyle.apa.org/

### **Tutoriales en Video:**
- "Mendeley and LaTeX integration" (YouTube)
- "How to use Mendeley with LaTeX" (Overleaf Learn)

### **Foros de Ayuda:**
- Mendeley Support: https://www.mendeley.com/support
- TeX Stack Exchange: https://tex.stackexchange.com/
- Overleaf Learn: https://www.overleaf.com/learn

---

## 💬 **PREGUNTAS FRECUENTES**

### **Q1: ¿Puedo usar Mendeley Web en lugar de Desktop?**
**A:** No. BibTeX syncing solo funciona en **Mendeley Desktop** (versión de escritorio). La versión web no tiene esta función.

---

### **Q2: ¿Qué pasa si cambio una referencia en Mendeley?**
**A:** El archivo `.bib` se actualiza automáticamente. La próxima vez que compiles LaTeX, verás los cambios.

---

### **Q3: ¿Puedo tener múltiples carpetas sincronizadas?**
**A:** Con configuración estándar, solo una carpeta. Pero si marcas "Create one BibTeX file per collection", cada carpeta genera su propio `.bib`.

---

### **Q4: ¿Debo hacer commit del archivo auto-generado en Git?**
**A:** **NO.** Agrega a `.gitignore`:
```
# .gitignore
TESIS_MAESTRIA_SEDENTARISMO.bib
*.bib  # Si prefieres, ignora todos los .bib auto-generados
```

**Mejor práctica:** Haz commit del `.bib` manualmente solo cuando esté estable (previo a envío de tesis).

---

### **Q5: ¿Funciona en Overleaf?**
**A:** **Parcialmente.** 
- Mendeley auto-sync **NO funciona** en Overleaf (es local)
- **Alternativa:** Exporta manualmente de Mendeley → Sube `.bib` a Overleaf

**Para Overleaf:** Mejor usar el plugin de Zotero o gestión manual.

---

## 🚀 **PRÓXIMA ACCIÓN (Después de Configurar)**

Una vez configurado Mendeley:

1. **Limpia tu biblioteca:**
   - Revisa que solo references relevantes estén en carpeta "TESIS_MAESTRIA_SEDENTARISMO"
   - Elimina duplicados
   - Completa metadatos faltantes (DOIs, páginas, etc.)

2. **Verifica el archivo exportado:**
   - Abre `TESIS_MAESTRIA_SEDENTARISMO.bib` con editor de texto
   - Verifica que las claves sean correctas (ej: `Martinez2024`, no `@#$%2024`)
   - Asegúrate de que caracteres especiales (á, é, í, ñ) estén correctos

3. **Prueba una citación:**
   - En tu capítulo, agrega `\cite{clave_referencia}`
   - Compila: pdflatex → biber → pdflatex
   - Verifica que aparezca correctamente en Referencias

---

## 📝 **RESUMEN (30 SEGUNDOS)**

```
1. Mendeley Desktop → Tools → Options → BibTeX
2. ✅ Enable BibTeX syncing
3. Seleccionar carpeta: [ruta de tesis_luisangel]
4. Crear carpeta "TESIS_MAESTRIA_SEDENTARISMO" en Mendeley
5. Mover referencias relevantes a esa carpeta
6. Mendeley auto-genera .bib
7. En LaTeX: \addbibresource{TESIS_MAESTRIA_SEDENTARISMO.bib}
8. Compilar y ¡listo!
```

---

**¿Problemas o dudas?** Consulta la sección "Solución de Problemas" arriba.

**FIN DEL DOCUMENTO**


