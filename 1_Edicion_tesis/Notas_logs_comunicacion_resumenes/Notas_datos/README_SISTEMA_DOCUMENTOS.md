# Sistema de Gestión de Documentos Académicos PDF

## 📋 Descripción

Sistema automatizado para procesar, analizar y catalogar documentos académicos en formato PDF, con almacenamiento en base de datos MySQL.

## ✨ Características

- ✅ Extracción automática de metadatos de PDFs
- ✅ Detección de fotocopias y documentos sin texto
- ✅ Almacenamiento en base de datos MySQL
- ✅ Extracción de: título, autor, colaboradores, año, tipo, abstract, editorial
- ✅ Generación automática de abstract cuando no existe
- ✅ Organización automática de archivos
- ✅ Sistema de consultas interactivo

## 🗄️ Estructura de la Base de Datos

**Base de datos:** `literatura_academica`

**Tabla:** `documentos`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT | Identificador único (auto-incremento) |
| nombre_archivo | VARCHAR(500) | Nombre del archivo PDF |
| titulo | VARCHAR(500) | Título del documento |
| autor_principal | VARCHAR(300) | Autor principal |
| colaboradores | TEXT | Colaboradores separados por comas |
| anio_publicacion | INT | Año de publicación |
| tipo_documento | VARCHAR(100) | Artículo, Libro, Tesis, etc. |
| abstract | TEXT | Resumen del documento |
| editorial | VARCHAR(300) | Editorial o publicador |
| ruta_archivo | VARCHAR(1000) | Ruta completa del archivo |
| fecha_registro | DATETIME | Fecha de registro en la BD |
| es_fotocopia | BOOLEAN | Indica si es fotocopia |

## 🚀 Instalación

### Requisitos previos

- Python 3.11+
- MySQL Server 8.0+
- Windows 10/11

### Librerías Python necesarias

```bash
python -m pip install pymupdf mysql-connector-python pdfplumber
```

## 📁 Configuración

### 1. Configurar MySQL

El sistema ya está configurado con:
- **Host:** localhost
- **Puerto:** 3306
- **Usuario:** root
- **Contraseña:** $Hulkmtz0312
- **Base de datos:** literatura_academica

### 2. Configurar directorios

Editar en `procesar_pdfs_academicos.py`:

```python
DIRECTORIO_PDFS = r"C:\Users\hulkmtz\Documents\luis angel\Maestria\Literatura de apoyo"
DIRECTORIO_FOTOCOPIAS = r"C:\Users\hulkmtz\Documents\luis angel\Maestria\Literatura de apoyo\fotocopias"
```

## 🎯 Uso

### Procesar documentos PDF

```bash
python procesar_pdfs_academicos.py
```

**Funcionalidades:**
1. Escanea **recursivamente** todos los PDFs en el directorio y subdirectorios
2. Extrae metadatos de cada documento  
3. Detecta fotocopias o documentos sin texto
4. Guarda información en MySQL
5. Mueve fotocopias a carpeta separada
6. **Exporta automáticamente a CSV** en el directorio actual

### Consultar documentos

```bash
python consultar_documentos.py
```

**Opciones de consulta:**
1. Ver todos los documentos
2. Buscar por autor
3. Buscar por año
4. Buscar por tipo de documento
5. Ver estadísticas
6. Ver documentos recientes
7. Buscar en título o abstract
8. Ver fotocopias detectadas

## 📊 Ejemplo de salida

```
======================================================================
  PROCESADOR DE DOCUMENTOS ACADÉMICOS PDF
======================================================================

📂 Directorio: C:\Users\hulkmtz\Documents\luis angel\Maestria\Literatura de apoyo
✓ Conectado a MySQL

📊 Encontrados 19 archivos PDF

📄 Procesando: Aspectos éticos.pdf
  📌 Título: REICE. Revista Iberoamericana sobre...
  👤 Autor: Autor desconocido
  📅 Año: 2011
  📚 Tipo: Artículo
  ✓ Guardado en base de datos (ID: 1)

======================================================================
  RESUMEN DEL PROCESAMIENTO
======================================================================
✓ Documentos procesados: 18
⚠ Fotocopias detectadas: 1
✗ Errores: 0
📊 Total: 19

✓ Proceso completado
```

## 🔍 Algoritmo de Detección de Fotocopias

El sistema detecta fotocopias mediante:

1. **Cantidad de texto extraído:** Si tiene menos de 200 caracteres legibles
2. **Ratio de caracteres ilegibles:** Si más del 30% son caracteres no imprimibles
3. **Calidad de extracción:** Comparación entre diferentes métodos de extracción

## 📝 Tipos de Documentos Reconocidos

- **Artículo:** Artículos de revistas científicas
- **Libro:** Libros completos
- **Tesis:** Tesis de grado o posgrado
- **Capítulo:** Capítulos de libros
- **Reporte:** Reportes técnicos
- **Conferencia:** Papers de conferencias
- **Documento:** Otros tipos

## 🛠️ Consultas SQL Útiles

### Ver todos los documentos

```sql
SELECT titulo, autor_principal, anio_publicacion, tipo_documento
FROM documentos
WHERE es_fotocopia = FALSE
ORDER BY anio_publicacion DESC;
```

### Buscar por autor

```sql
SELECT titulo, anio_publicacion, tipo_documento
FROM documentos
WHERE autor_principal LIKE '%nombre%'
   OR colaboradores LIKE '%nombre%';
```

### Estadísticas por tipo

```sql
SELECT tipo_documento, COUNT(*) as cantidad
FROM documentos
WHERE es_fotocopia = FALSE
GROUP BY tipo_documento;
```

### Documentos por año

```sql
SELECT anio_publicacion, COUNT(*) as cantidad
FROM documentos
WHERE es_fotocopia = FALSE AND anio_publicacion IS NOT NULL
GROUP BY anio_publicacion
ORDER BY anio_publicacion DESC;
```

## 📌 Notas Importantes

1. **Fotocopias:** Los documentos detectados como fotocopias se mueven automáticamente a la carpeta `/fotocopias`
2. **Duplicados:** El sistema no verifica duplicados automáticamente
3. **Extracción de texto:** La calidad depende del formato del PDF original
4. **Abstract:** Si no existe, se genera con las primeras 150 palabras del documento
5. **Encoding:** Todos los datos se guardan en UTF-8 para soportar caracteres especiales

## 🐛 Solución de Problemas

### Error de conexión a MySQL

```bash
# Verificar que el servicio esté corriendo
Get-Service MySQL80

# Iniciar servicio si está detenido
net start MySQL80
```

### Error al importar librerías

```bash
# Reinstalar librerías
python -m pip install --user --upgrade pymupdf mysql-connector-python pdfplumber
```

### No se extraen datos correctamente

- Verificar que el PDF no esté protegido
- Asegurar que el PDF contiene texto (no solo imágenes)
- Revisar que el PDF no esté corrupto

## 📈 Estadísticas del Sistema

**Resultados del procesamiento actual:**
- ✅ **552 archivos PDF procesados** (incluyendo subdirectorios)
- ✅ **543 documentos catalogados** exitosamente
- 📚 Tipos: 307 Artículos, 124 Documentos, 43 Libros, 41 Tesis, 21 Reportes, 7 Capítulos
- 📅 Rango temporal: 1984-2025 (41 años)
- 📁 **4 subdirectorios procesados** (Mates, Neurobiologia_ejercicio, sedentarismo_mineria_datos, Validacion instrumento)
- ⚠️ **9 fotocopias detectadas** y movidas
- 💾 **CSV exportado:** documentos_academicos.csv (163.73 KB)

## 🔐 Seguridad

- La contraseña de MySQL está hardcodeada en los scripts
- **Recomendación:** Usar variables de entorno para producción
- Los archivos se procesan localmente, no se envían a servicios externos

## 📞 Soporte

Para modificar la configuración o agregar funcionalidades, editar los scripts:
- `procesar_pdfs_academicos.py` - Procesamiento principal
- `consultar_documentos.py` - Sistema de consultas

## 🎓 Autor

Sistema automatizado para gestión de literatura académica  
Universidad: Maestría en Asesoría - Semestre 3  
Fecha: 28 de Octubre, 2025

---

**Nota:** Este sistema está diseñado específicamente para procesar documentos académicos en español e inglés.

