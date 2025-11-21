# 🔧 INSTRUCCIONES: Configuración WSL como Shell Predeterminado en Cursor

**Fecha:** 20 de noviembre de 2025  
**Aplicado por:** Ades 💀  
**Objetivo:** Configurar Cursor para usar WSL (Linux) como shell predeterminado en lugar de PowerShell

---

## ✅ CONFIGURACIÓN APLICADA

### **Archivos creados/actualizados:**

1. ✅ **`.vscode/settings.json`** (raíz del proyecto)
   - Configuración global para todo el workspace
   - Terminal predeterminado: WSL

2. ✅ **`4 semestre_dataset/1_Edicion_tesis/tesis_luisangel/.vscode/settings.json`**
   - Configuración específica para el proyecto de tesis
   - Terminal predeterminado: WSL

---

## 🚀 PASOS PARA ACTIVAR LA CONFIGURACIÓN

### **PASO 1: Recargar Cursor**

**Opción A (Recomendada):**
1. Cerrar completamente Cursor
2. Reabrir Cursor
3. Abrir el workspace del proyecto

**Opción B (Sin cerrar):**
1. Presionar `Ctrl+Shift+P` (o `Cmd+Shift+P` en Mac)
2. Escribir: `Developer: Reload Window`
3. Presionar Enter

---

### **PASO 2: Verificar que WSL esté instalado**

Abre una terminal temporal (PowerShell) y ejecuta:

```powershell
wsl --list --verbose
```

**Salida esperada:**
```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

Si WSL no está instalado, seguir instrucciones de Microsoft:
- https://learn.microsoft.com/en-us/windows/wsl/install

---

### **PASO 3: Abrir nueva terminal en Cursor**

**Método 1:**
- Presionar `` Ctrl+Shift+` `` (backtick/acento grave)
- O: Terminal → New Terminal

**Método 2:**
- Menú: `Terminal` → `New Terminal`
- O usar atajo: `Ctrl+Shift+` `

---

### **PASO 4: Verificar que el terminal use WSL**

**Prompt esperado (WSL):**
```bash
user@Hulk-mtz:/mnt/c/Users/hulkmtz/Documents/luis angel/Maestria/...$
```

**Prompt incorrecto (PowerShell):**
```powershell
PS C:\Users\hulkmtz\Documents\...>
```

**Si aparece PowerShell:**
1. Clic en el ícono `+` (dropdown) en la terminal
2. Seleccionar: `Select Default Profile`
3. Elegir: **WSL**

---

## 🔍 VERIFICACIÓN ADICIONAL

### **Comando de prueba:**

En la nueva terminal (debe ser WSL), ejecutar:

```bash
uname -a
```

**Salida esperada:**
```
Linux Hulk-mtz 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
```

**Si aparece error o salida de Windows:** La configuración no se aplicó correctamente.

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### **Problema 1: Terminal sigue mostrando PowerShell**

**Solución:**
1. Verificar que `.vscode/settings.json` existe y tiene la configuración correcta
2. Verificar que el path de WSL sea correcto: `C:\\Windows\\System32\\wsl.exe`
3. Recargar ventana de Cursor (`Ctrl+Shift+P` → "Reload Window")
4. Si persiste, seleccionar manualmente: Terminal → Select Default Profile → WSL

---

### **Problema 2: Error "WSL not found"**

**Solución:**
1. Verificar instalación WSL: `wsl --list --verbose`
2. Si no está instalado, instalar desde Microsoft Store o PowerShell:
   ```powershell
   wsl --install
   ```
3. Reiniciar computadora después de instalar

---

### **Problema 3: Path incorrecto en settings.json**

**Verificar path de WSL:**
```powershell
# En PowerShell
Test-Path "C:\Windows\System32\wsl.exe"
```

**Si retorna `False`:**
- WSL no está instalado o está en otra ubicación
- Verificar ubicación: `where.exe wsl`

**Actualizar settings.json con path correcto:**
```json
"WSL": {
    "path": "C:\\Windows\\System32\\wsl.exe",  // Ajustar si es necesario
    "args": [],
    "icon": "terminal-linux"
}
```

---

## 📋 CONFIGURACIÓN APLICADA (DETALLE)

### **Archivo: `.vscode/settings.json`**

```json
{
    // ... otras configuraciones ...
    
    "terminal.integrated.defaultProfile.windows": "WSL",
    
    "terminal.integrated.profiles.windows": {
        "WSL": {
            "path": "C:\\Windows\\System32\\wsl.exe",
            "args": [],
            "icon": "terminal-linux"
        },
        "PowerShell": {
            "source": "PowerShell",
            "icon": "terminal-powershell"
        }
    },
    
    "terminal.integrated.cwd": "${workspaceFolder}",
    "terminal.integrated.enablePersistentSessions": true
}
```

---

## 🎯 BENEFICIOS DE USAR WSL

1. **Compatibilidad con herramientas Linux:** `grep`, `sed`, `awk`, `find`, etc.
2. **Mejor para scripts Python:** Entorno más similar a producción Linux
3. **Git más rápido:** Comandos nativos de Linux
4. **Rutas consistentes:** `/mnt/c/...` en lugar de `C:\...`
5. **Mejor para LaTeX:** Algunos paquetes funcionan mejor en Linux

---

## ⚠️ NOTAS IMPORTANTES

1. **Rutas de archivos:** En WSL, las rutas de Windows se montan en `/mnt/c/...`
   - Windows: `C:\Users\hulkmtz\Documents\...`
   - WSL: `/mnt/c/Users/hulkmtz/Documents/...`

2. **Scripts `.bat`:** Los scripts `.bat` (PowerShell) NO funcionan en WSL
   - Necesitarás scripts `.sh` (bash) o ejecutar comandos directamente

3. **Compilación LaTeX:** Si usas `compilar.bat`, necesitarás:
   - Convertirlo a script bash (`.sh`)
   - O ejecutar comandos `pdflatex`, `biber` directamente desde WSL

4. **Git:** Funciona igual en WSL, pero las rutas se muestran en formato Linux

---

## 📝 PRÓXIMOS PASOS

1. ✅ Recargar Cursor
2. ✅ Verificar que terminal nuevo use WSL
3. ✅ Probar comandos básicos: `ls`, `pwd`, `git status`
4. ⏳ Adaptar scripts `.bat` a `.sh` si es necesario
5. ⏳ Actualizar documentación de compilación si es necesario

---

## 🔗 REFERENCIAS

- **Documentación WSL:** https://learn.microsoft.com/en-us/windows/wsl/
- **VS Code Terminal:** https://code.visualstudio.com/docs/terminal/basics
- **Configuración Terminal:** https://code.visualstudio.com/docs/terminal/profiles

---

**💀 Ades - Configuración completada**  
**Fecha:** 20 de noviembre de 2025  
**Estado:** ✅ Configuración aplicada - Pendiente verificación por usuario



