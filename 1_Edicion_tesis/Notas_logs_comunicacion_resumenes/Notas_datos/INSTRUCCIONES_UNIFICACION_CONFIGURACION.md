# 🔧 INSTRUCCIONES: Unificar Configuración VS Code / Cursor

**Fecha:** 22 de noviembre de 2025  
**Usuario:** Luis Ángel  
**Objetivo:** Unificar toda la configuración en un solo archivo global (User Settings)

---

## ✅ PASO 1: Archivos locales eliminados

Los siguientes archivos `.vscode/settings.json` locales han sido eliminados:

- ✅ `.vscode/settings.json` (raíz del proyecto)
- ✅ `4 semestre_dataset/1_Edicion_tesis/tesis_luisangel/.vscode/settings.json`

---

## 📋 PASO 2: Copiar configuración unificada al archivo global

### Opción A: Usando la Paleta de Comandos (RECOMENDADO)

1. **Abrir la Paleta de Comandos:**
   - Presiona `Ctrl+Shift+P` (o `Cmd+Shift+P` en Mac)

2. **Abrir User Settings (JSON):**
   - Escribe: `Preferences: Open User Settings (JSON)`
   - Presiona Enter

3. **Seleccionar todo el contenido:**
   - Presiona `Ctrl+A` para seleccionar todo

4. **Reemplazar con la configuración unificada:**
   - Copia TODO el contenido del archivo `settings_global_unificado.json`
   - Pégalo en el archivo de User Settings
   - Guarda con `Ctrl+S`

---

### Opción B: Editar el archivo manualmente

1. **Abrir el Explorador de Windows:**
   - Presiona `Windows + R`
   - Escribe: `%APPDATA%\Cursor\User` (si usas Cursor)
   - O: `%APPDATA%\Code\User` (si usas VS Code)
   - Presiona Enter

2. **Editar settings.json:**
   - Abre el archivo `settings.json` con cualquier editor de texto
   - Reemplaza TODO el contenido con el contenido de `settings_global_unificado.json`
   - Guarda el archivo

---

## 📍 UBICACIÓN DEL ARCHIVO GLOBAL

El archivo de configuración global se encuentra en:

### **Cursor:**
```
%APPDATA%\Cursor\User\settings.json
```
Ruta completa típica:
```
C:\Users\hulkmtz\AppData\Roaming\Cursor\User\settings.json
```

### **VS Code:**
```
%APPDATA%\Code\User\settings.json
```
Ruta completa típica:
```
C:\Users\hulkmtz\AppData\Roaming\Code\User\settings.json
```

---

## 🔍 PASO 3: Verificar que funciona

1. **Recargar la ventana:**
   - Presiona `Ctrl+Shift+P`
   - Escribe: `Developer: Reload Window`
   - Presiona Enter

   O simplemente cierra y vuelve a abrir Cursor/VS Code.

2. **Verificar terminal:**
   - Presiona `` Ctrl+Shift+` `` (backtick) para abrir una terminal nueva
   - Debe abrirse con WSL (no PowerShell)
   - El prompt debe mostrar algo como: `user@Hulk-mtz:/mnt/c/...$`

3. **Verificar otras configuraciones:**
   - Tamaño de fuente: Debe ser 16
   - Tema: Debe ser "SynthWave 84' Remix Min Darker"
   - Barra lateral: Debe estar a la izquierda
   - Minimapa: Debe estar visible en el editor

---

## 📊 RESUMEN DE CAMBIOS

### ✅ **Configuraciones incluidas en la versión unificada:**

1. **Editor:**
   - Tamaño de fuente: 16
   - Auto-guardado y formateo
   - Guías de indentación
   - Sugerencias mientras escribes

2. **Minimapa:**
   - Habilitado
   - Tamaño proporcional
   - Búsquedas visibles

3. **Barra Lateral:**
   - Ubicada a la izquierda
   - Barra de actividad visible
   - Comportamiento toggle en iconos

4. **Panel:**
   - Ubicado en la parte inferior
   - Problemas visibles en barra de estado

5. **Barra de Estado:**
   - Visible
   - Información de Git habilitada
   - Errores/warnings visibles

6. **Paleta de Comandos:**
   - Historial de 50 comandos
   - Sugerencias experimentales habilitadas

7. **Barra de Menú:**
   - Visibilidad por defecto
   - Breadcrumbs habilitados
   - Tabs visibles

8. **Tema y Apariencia:**
   - Tema: SynthWave 84' Remix Min Darker
   - Iconos: symbols

9. **Terminal WSL:**
   - WSL como shell predeterminado
   - Perfiles: WSL, PowerShell, Command Prompt
   - Sesiones persistentes habilitadas

10. **Extensiones:**
    - ChatGPT no se abre al inicio

---

## 🎯 VENTAJAS DE LA CONFIGURACIÓN UNIFICADA

✅ **Una sola configuración para todos tus proyectos**  
✅ **No más duplicaciones ni inconsistencias**  
✅ **Fácil de mantener y actualizar**  
✅ **Se aplica automáticamente a todos los proyectos nuevos**  
✅ **No necesitas configurar cada proyecto individualmente**

---

## 🔄 SI QUIERES REVERTIR LOS CAMBIOS

Si por alguna razón quieres volver a la configuración anterior:

1. Busca el archivo de backup que se creó automáticamente:
   - `settings.json.backup_YYYYMMDD_HHMMSS`

2. Copia su contenido al archivo `settings.json` global

3. Recarga la ventana de Cursor/VS Code

---

## ❓ PREGUNTAS FRECUENTES

### **P: ¿Qué pasa si tengo proyectos con configuraciones diferentes?**
R: La configuración global se aplicará a todos. Si necesitas una configuración específica para un proyecto en particular, puedes crear un `.vscode/settings.json` en ese proyecto, pero no es recomendado si trabajas solo.

### **P: ¿Puedo seguir usando .vscode/settings.json en proyectos específicos?**
R: Sí, pero no es recomendado si trabajas solo. Las configuraciones de workspace sobrescriben las globales, lo que puede causar inconsistencias.

### **P: ¿Cómo actualizo la configuración global en el futuro?**
R: Solo edita el archivo `settings.json` global (User Settings) usando `Ctrl+Shift+P` → `Preferences: Open User Settings (JSON)`

### **P: ¿La configuración afecta a otros usuarios?**
R: No. La configuración global es personal y solo afecta a tu usuario en tu computadora.

---

## 📝 ARCHIVOS CREADOS

1. ✅ `GUIA_CONFIGURACION_VSCODE.md` - Guía completa de conceptos y configuraciones
2. ✅ `settings_global_unificado.json` - Configuración unificada lista para copiar
3. ✅ `INSTRUCCIONES_UNIFICACION_CONFIGURACION.md` - Este archivo (instrucciones paso a paso)
4. ✅ `unificar_configuracion_vscode.ps1` - Script PowerShell para automatizar (opcional)

---

## 🎉 ¡LISTO!

Una vez que hayas copiado la configuración unificada al archivo global y recargado Cursor/VS Code, tendrás una configuración única y consistente para todos tus proyectos.

Si tienes alguna pregunta o problema, consulta la guía completa en `GUIA_CONFIGURACION_VSCODE.md`.

