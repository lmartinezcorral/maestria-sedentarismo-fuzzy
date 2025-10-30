# 📚 Herramienta de Bibliografía para LaTeX - UACH

## Descripción

Herramienta portable y simplificada para generar automáticamente referencias bibliográficas en formato BibTeX a partir de archivos PDF académicos.

## Características

- ✅ **Portable**: No requiere instalación compleja
- ✅ **Automática**: Usa IA (Gemini) para extraer metadatos
- ✅ **Gratis**: Usa plan gratuito de Google Gemini
- ✅ **Sin MySQL**: No requiere bases de datos
- ✅ **Plug & Play**: Solo necesitas tus PDFs

## Archivos Incluidos

- `GENERAR_REFERENCIAS.bat` - Archivo ejecutable principal
- `generar_referencias.py` - Script Python
- `INSTRUCCIONES.txt` - Manual de usuario
- `README.md` - Documentación técnica

## Requisitos

- Windows 10/11
- Python 3.9+ (el .bat lo verifica automáticamente)
- Conexión a internet
- Archivos PDF académicos

## Uso Rápido

1. Coloca tus PDFs en la misma carpeta que los archivos
2. Ejecuta `GENERAR_REFERENCIAS.bat`
3. Espera a que termine (2-5 min por PDF)
4. Usa los archivos generados en tu tesis

## Archivos Generados

- `referencias.csv` - Tabla con todas las referencias
- `referencias.bib` - Archivo BibTeX para LaTeX

## Integración con LaTeX

```latex
% En tu archivo .tex
\bibliography{referencias}

% Para citar
\cite{autor2024}
```

## Dependencias Automáticas

El script instala automáticamente:
- `google-generativeai` - Para usar Gemini AI
- `pymupdf` - Para extraer texto de PDFs

## API Key

La herramienta incluye una API key de Gemini ya configurada (gratis).

## Limitaciones

- Requiere conexión a internet
- Máximo 60 solicitudes por minuto (plan gratuito)
- Algunos PDFs pueden no procesarse correctamente

## Solución de Problemas

### Python no instalado
```
Error: Python no está instalado
Solución: Instalar desde https://www.python.org/downloads/
```

### Sin conexión a internet
```
Error: No hay conexión a internet
Solución: Verificar conexión a internet
```

### No se encuentran PDFs
```
Error: No se encontraron archivos PDF
Solución: Colocar PDFs en la misma carpeta
```

## Soporte

**Desarrollado por**: Luis Angel Martínez Corral  
**Email**: p261337@uach.mx  
**Teléfono**: +52 (614) 344-88-36

---

*Facultad de Medicina y Ciencias Biomédicas - UACH*  
*Octubre 2025*