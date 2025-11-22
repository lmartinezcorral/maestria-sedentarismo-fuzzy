# 📁 ESTRUCTURA DE DIRECTORIOS

## ¿Qué es cada carpeta?

### 📂 `/edicion_tesis/` (Raíz)
**Contiene:** Contenido actual de trabajo

**Uso:** Aquí desarrollamos y modificamos todo en tiempo real.

### 📂 `/plantilla_mfips/` 
**Contiene:** Plantilla EN BLANCO lista para compartir

**Propósito:** Esta es la versión que compartirás con tus compañeros de maestría.

**Características:**
- ✅ Toda la estructura correcta de la UACH
- ✅ Capítulos con plantillas y ejemplos
- ✅ Datos con placeholders `[REEMPLAZAR AQUÍ]`
- ✅ Logo de la universidad incluido
- ✅ Documentación completa
- ❌ NO contiene información personal

**Para compartir:**
1. Comprime esta carpeta en un `.zip`
2. Compártela con tus compañeros
3. Ellos descomprimen y personalizan con su información

### 📂 `/tesis_luisangel/`
**Contiene:** Tu versión personalizada con TUS datos

**Propósito:** Aquí trabajamos con tu información personal para generar TU tesis.

**Datos incluidos:**
- ✅ Tu nombre completo
- ✅ Tu matrícula y email
- ✅ Datos de la Facultad de Medicina y Ciencias Biomédicas
- ✅ Datos de tu Maestría (MFIPS)
- ✅ Logo de la UACH
- 🔄 Comité tutorial (faltan nombres)
- 🔄 Título de tesis (falta)

---

## 🔄 Flujo de Trabajo

```
┌─────────────────────────────────────┐
│   edicion_tesis/ (desarrollo)       │
│   ✅ Traba jo en tiempo real        │
│   ✅ Modificaciones rápidas          │
└─────────────────────────────────────┘
              ↓ Sincronizar
        (Cuando estés listo)
              ↓
    ┌─────────────────────────┐
    │   plantilla_mfips/      │
    │   📤 Para compartir     │
    │   (versión limpia)      │
    └─────────────────────────┘
              +
    ┌─────────────────────────┐
    │   tesis_luisangel/      │
    │   📝 Tu versión         │
    │   (con tus datos)       │
    └─────────────────────────┘
```

---

## 📋 Checklist de Uso

### Al Compartir con Compañeros:

- [ ] Comparte `/plantilla_mfips/` (NO `/tesis_luisangel/`)
- [ ] Asegúrate que no tenga información personal
- [ ] Incluye todos los archivos necesarios
- [ ] Incluye la documentación completa

### Al Trabajar en Tu Tesis:

- [ ] Trabaja en `/tesis_luisangel/`
- [ ] Edita `DATOS_PERSONALIZACION.json` primero
- [ ] Luego actualiza `plantilla_tesis.tex` con tus datos
- [ ] Mantén sincronizado `/edicion_tesis/` con tus cambios

---

## 📝 Diccionario de Datos

El archivo `DATOS_PERSONALIZACION.json` contiene:

- **universidad:** Datos de la UACH
- **facultad:** Datos de Medicina y Ciencias Biomédicas
- **programa:** Datos de la Maestría MFIPS
- **estudiante:** Tus datos personales
- **comite_tutorial:** Miembros de tu comité (completar)
- **tesis:** Configuración (LGAC, estilo de citas)

**Uso:** Edita este archivo JSON primero, luego copia los valores a los archivos `.tex`.

---

## 🚀 Próximos Pasos

1. ✅ Ya tienes la estructura creada
2. ⏭️ Continuamos trabajando en `/edicion_tesis/` (portada, firmas, etc.)
3. ⏭️ Cuando esté listo, sincronizamos a `/plantilla_mfips/` y `/tesis_luisangel/`

---

**Última actualización:** Octubre 29, 2025


