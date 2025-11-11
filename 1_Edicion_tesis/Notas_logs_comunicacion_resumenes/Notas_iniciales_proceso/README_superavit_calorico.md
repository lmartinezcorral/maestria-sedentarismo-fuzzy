# Variable: Superávit Calórico Basal

## Descripción

Se ha creado una nueva variable llamada **`Superavit_calorico_basal`** que captura el impacto fisiológico del gasto calórico activo ajustado por las características físicas de cada usuario (sexo, peso, estatura y edad).

## Justificación

El gasto calórico activo absoluto (en kcal) no refleja el mismo impacto fisiológico para diferentes individuos. Por ejemplo:
- 400 kcal gastadas tienen un impacto diferente en una mujer de 58 kg comparado con un hombre de 124 kg
- El mismo gasto calórico representa un esfuerzo relativo distinto según el sexo, edad, peso y estatura del individuo

## Fórmula de Cálculo

### Superávit Calórico Basal
```
Superavit_calorico_basal = (Gasto_calorico_activo × 100) / TMB
```

Donde TMB es la Tasa Metabólica Basal calculada según el sexo:

### TMB para Hombres (Fórmula de Mifflin-St Jeor)
```
TMB = (10 × peso en kg) + (6.25 × estatura en cm) - (5 × edad en años) + 5
```

### TMB para Mujeres (Fórmula de Mifflin-St Jeor)
```
TMB = (10 × peso en kg) + (6.25 × estatura en cm) - (5 × edad en años) - 161
```

## Datos de Usuarios

| Usuario | Nombre | Sexo | Estatura (cm) | Peso (kg) | Edad (años) | TMB (kcal/día) |
|---------|--------|------|---------------|-----------|-------------|----------------|
| Usuario_1 | ale | Mujer | 170 | 68 | 34 | 1411.50 |
| Usuario_2 | brenda | Mujer | 169 | 76 | 37 | 1470.25 |
| Usuario_3 | christina | Mujer | 164 | 77 | 39 | 1439.00 |
| Usuario_4 | edson | Hombre | 180 | 100 | 25 | 2005.00 |
| Usuario_5 | esmeralda | Mujer | 160 | 64 | 28 | 1339.00 |
| Usuario_6 | fidel | Hombre | 180 | 100 | 34 | 1960.00 |
| Usuario_7 | kevin | Hombre | 156 | 92 | 32 | 1740.00 |
| Usuario_8 | legarda | Hombre | 181 | 92 | 29 | 1911.25 |
| Usuario_9 | lmartinez | Hombre | 185 | 124 | 32 | 2241.25 |
| Usuario_10 | vane | Mujer | 164 | 58 | 28 | 1304.00 |

## Resultados Principales

### Estadísticas Generales
- **Total de registros procesados:** 9,185
- **Nuevas columnas agregadas:** 2 (TMB, Superavit_calorico_basal)
- **Columnas totales en el archivo:** 17

### Comparación por Sexo

#### Hombres (5 usuarios, 6,158 registros)
- TMB Media: 2,016.15 kcal/día
- Gasto Calórico Activo Media: 667.39 kcal
- Superávit Calórico Basal Media: **32.84%**
- Superávit Calórico Basal Mediana: **28.83%**

#### Mujeres (5 usuarios, 3,027 registros)
- TMB Media: 1,388.78 kcal/día
- Gasto Calórico Activo Media: 450.35 kcal
- Superávit Calórico Basal Media: **32.22%**
- Superávit Calórico Basal Mediana: **25.60%**

### Distribución del Superávit Calórico Basal

| Rango | Registros | Porcentaje |
|-------|-----------|------------|
| 0-10% | 707 | 7.70% |
| 10-20% | 1,631 | 17.76% |
| 20-30% | 2,751 | 29.95% |
| 30-40% | 1,705 | 18.56% |
| 40-50% | 979 | 10.66% |
| 50-100% | 1,300 | 14.15% |
| >100% | 112 | 1.22% |

## Interpretación

El **Superávit Calórico Basal** se expresa como un **porcentaje** que indica qué proporción del metabolismo basal representa el gasto calórico activo:

- **0-20%**: Actividad física baja relativa a la TMB
- **20-40%**: Actividad física moderada relativa a la TMB
- **40-60%**: Actividad física alta relativa a la TMB
- **>60%**: Actividad física muy alta relativa a la TMB

### Observaciones Clave

1. **Normalización por características individuales**: La variable ajusta el gasto calórico por las diferencias fisiológicas entre usuarios.

2. **Comparabilidad mejorada**: Permite comparar niveles de actividad física entre usuarios con diferentes características antropométricas.

3. **Valores extremos**: Algunos registros presentan valores muy altos (>100%) que corresponden a días con actividad física excepcional.

4. **Distribución**: La mayoría de los registros (76.27%) se encuentran en el rango de 10-50% de superávit calórico basal.

## Archivos Generados

1. **DB_usuarios_consolidada_con_actividad_relativa.csv** (actualizado)
   - Archivo principal con las nuevas columnas TMB y Superavit_calorico_basal

2. **resumen_superavit_calorico_basal.csv**
   - Resumen estadístico por usuario

3. **crear_superavit_calorico.py**
   - Script Python para calcular y agregar las nuevas variables

4. **verificar_superavit_calorico.py**
   - Script Python para verificar y generar estadísticas de la nueva variable

## Uso Futuro

Esta variable permite:
- Comparar la intensidad de actividad física entre usuarios de manera normalizada
- Identificar patrones de actividad ajustados por características individuales
- Realizar análisis de sedentarismo considerando el impacto fisiológico real del gasto energético
- Utilizar como input para modelos de lógica difusa o machine learning que requieran variables normalizadas

---

**Fecha de creación:** 15 de octubre de 2025  
**Archivo base:** DB_usuarios_consolidada_con_actividad_relativa.csv  
**Método de cálculo TMB:** Fórmula de Mifflin-St Jeor


