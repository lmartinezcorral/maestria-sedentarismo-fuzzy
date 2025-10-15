# Análisis de Datos Biométricos - 4to Semestre

## Descripción del Proyecto

Este repositorio contiene el análisis de datos biométricos obtenidos del Apple Watch para el estudio de patrones de actividad física y comportamiento sedentario. El objetivo principal es encontrar una forma de categorizar los niveles de actividad física y comportamiento sedentario con los datos biométricos obtenidos, considerando la variabilidad de la frecuencia cardíaca como variable de control o referencia del estado fisiológico.

## Estado Inicial del Repositorio

**Commit Inicial**: Estado original de las bases de datos sin transformación de variables.

### Archivos de Datos Originales

Los siguientes archivos CSV contienen los datos originales de cada participante del estudio:

- `DB_final_v3_u1.csv` - Datos del Usuario 1 (1,050 registros)
- `DB_final_v3_u2.csv` - Datos del Usuario 2
- `DB_final_v3_u3.csv` - Datos del Usuario 3
- `DB_final_v3_u4.csv` - Datos del Usuario 4
- `DB_final_v3_u5.csv` - Datos del Usuario 5
- `DB_final_v3_u6.csv` - Datos del Usuario 6
- `DB_final_v3_u7.csv` - Datos del Usuario 7
- `DB_final_v3_u8.csv` - Datos del Usuario 8
- `DB_final_v3_u9.csv` - Datos del Usuario 9
- `DB_final_v3_u10.csv` - Datos del Usuario 10 (855 registros)

### Estructura de Datos

Cada archivo CSV contiene las siguientes columnas:

- `Fecha` - Fecha del registro
- `Numero_horas_con_deambulacion` - Horas con movimiento
- `Numero_horas_estacionarias` - Horas estacionarias
- `Total_hrs_monitorizadas` - Total de horas monitoreadas por día
- `Hrs_sin_registro` - Horas sin registro
- `min_totales_en_movimiento` - Minutos totales en movimiento
- `Total_min_de_ejercicio_diario` - Minutos de ejercicio diario
- `distancia_caminada_en_km` - Distancia caminada en kilómetros
- `Numero_pasos_por_dia` - Número de pasos por día
- `FCr_promedio_diario` - Frecuencia cardíaca promedio diaria
- `Gasto_calorico_activo` - Gasto calórico activo
- `HRV_SDNN` - Variabilidad de la frecuencia cardíaca (SDNN)
- `FC_al_caminar_promedio_diario` - Frecuencia cardíaca al caminar promedio diaria

### Características del Dataset

- **Total de participantes**: 10 usuarios
- **Período de recolección**: Febrero 2022 - Marzo 2025
- **Promedio de horas monitoreadas**: ~15 horas por día
- **Variables biométricas**: Frecuencia cardíaca, HRV, pasos, distancia, gasto calórico
- **Variables de actividad**: Tiempo en movimiento, ejercicio, comportamiento sedentario

## Objetivos del Proyecto

1. **Categorización de Actividad Física**: Desarrollar un sistema de clasificación de niveles de actividad física basado en datos biométricos del Apple Watch.

2. **Análisis de Comportamiento Sedentario**: Identificar patrones de comportamiento sedentario y su relación con variables biométricas.

3. **Modelado con Lógica Difusa**: Implementar un sistema de lógica difusa para la clasificación de comportamientos de actividad física.

4. **Variable de Control**: Utilizar la variabilidad de la frecuencia cardíaca (HRV) como variable de referencia del estado fisiológico.

## Metodología

### Ingeniería de Variables

Se planea implementar variables derivadas para mejorar la representatividad de los datos:

- **Actividad Relativa**: Ratio de tiempo en movimiento vs tiempo total monitoreado
- **Intensidad de Actividad**: Combinación de variables de movimiento y frecuencia cardíaca
- **Patrones Temporales**: Análisis de variabilidad diaria y semanal

### Análisis Previsto

1. **Análisis Exploratorio**: Estadísticas descriptivas y visualizaciones
2. **Análisis de Correlaciones**: Relaciones entre variables biométricas y de actividad
3. **Clustering**: Identificación de patrones de comportamiento
4. **Modelado Predictivo**: Clasificación de niveles de actividad
5. **Sistema de Lógica Difusa**: Implementación de reglas de clasificación

## Estructura del Repositorio

```
4 semestre_dataset/
├── README.md                 # Este archivo
├── .gitignore               # Archivos a ignorar por Git
├── DB_final_v3_u1.csv      # Datos originales Usuario 1
├── DB_final_v3_u2.csv      # Datos originales Usuario 2
├── ...
├── DB_final_v3_u10.csv     # Datos originales Usuario 10
└── scripts/                 # Scripts de análisis (futuro)
```

## Notas Importantes

- **Estado Actual**: Datos originales sin transformaciones
- **Próximos Pasos**: Implementación de ingeniería de variables
- **Control de Versiones**: Cada transformación será documentada en commits separados
- **Reproducibilidad**: Todos los scripts de análisis serán versionados

## Contacto

Proyecto de investigación para el 4to semestre de la Maestría en Ciencias de la Computación.

---

**Fecha de Creación**: $(date)  
**Versión**: 1.0.0 - Estado Inicial  
**Última Actualización**: Commit inicial con datos originales


