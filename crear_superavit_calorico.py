import os
import pandas as pd
import numpy as np

# Definir los datos de cada usuario
usuarios_info = {
    'Usuario_1': {'nombre': 'ale', 'sexo': 'Mujer', 'estatura': 170, 'peso': 68, 'edad': 34},
    'Usuario_2': {'nombre': 'brenda', 'sexo': 'Mujer', 'estatura': 169, 'peso': 76, 'edad': 37},
    'Usuario_3': {'nombre': 'christina', 'sexo': 'Mujer', 'estatura': 164, 'peso': 77, 'edad': 39},
    'Usuario_4': {'nombre': 'edson', 'sexo': 'Hombre', 'estatura': 180, 'peso': 100, 'edad': 25},
    'Usuario_5': {'nombre': 'esmeralda', 'sexo': 'Mujer', 'estatura': 160, 'peso': 64, 'edad': 28},
    'Usuario_6': {'nombre': 'fidel', 'sexo': 'Hombre', 'estatura': 180, 'peso': 100, 'edad': 34},
    'Usuario_7': {'nombre': 'kevin', 'sexo': 'Hombre', 'estatura': 156, 'peso': 92, 'edad': 32},
    'Usuario_8': {'nombre': 'legarda', 'sexo': 'Hombre', 'estatura': 181, 'peso': 92, 'edad': 29},
    'Usuario_9': {'nombre': 'lmartinez', 'sexo': 'Hombre', 'estatura': 185, 'peso': 124, 'edad': 32},
    'Usuario_10': {'nombre': 'vane', 'sexo': 'Mujer', 'estatura': 164, 'peso': 58, 'edad': 28}
}


def calcular_tmb(sexo, peso, estatura, edad):
    """
    Calcula la Tasa Metabólica Basal según la fórmula de Mifflin-St Jeor

    Hombres: TMB = (10 * peso) + (6.25 * estatura) - (5 * edad) + 5
    Mujeres: TMB = (10 * peso) + (6.25 * estatura) - (5 * edad) - 161

    Args:
        sexo: 'Hombre' o 'Mujer'
        peso: peso en kg
        estatura: estatura en cm
        edad: edad en años

    Returns:
        TMB en kcal/día
    """
    tmb_base = (10 * peso) + (6.25 * estatura) - (5 * edad)

    if sexo == 'Hombre':
        tmb = tmb_base + 5
    else:  # Mujer
        tmb = tmb_base - 161

    return tmb


def calcular_superavit_calorico(gasto_activo, tmb):
    """
    Calcula el superávit calórico sobre el basal

    Formula: (gasto_calorico_activo * 100) / TMB

    Args:
        gasto_activo: Gasto calórico activo en kcal
        tmb: Tasa Metabólica Basal en kcal/día

    Returns:
        Porcentaje del superávit calórico respecto al TMB
    """
    return (gasto_activo * 100) / tmb


# Leer el archivo CSV
print("Leyendo archivo CSV...")
print(f"Directorio actual: {os.getcwd()}")
df = pd.read_csv('DB_usuarios_consolidada_con_actividad_relativa.csv')

print(f"Archivo leído. Dimensiones: {df.shape}")
print(f"Columnas: {df.columns.tolist()}")

# Crear columnas para TMB y Superávit Calórico Basal
df['TMB'] = 0.0
df['Superavit_calorico_basal'] = 0.0

# Calcular TMB y Superávit Calórico para cada usuario
print("\nCalculando TMB y Superávit Calórico Basal para cada usuario...")

for usuario_id, info in usuarios_info.items():
    print(f"\n{usuario_id} ({info['nombre']}):")
    print(
        f"  Sexo: {info['sexo']}, Peso: {info['peso']} kg, Estatura: {info['estatura']} cm, Edad: {info['edad']} años")

    # Calcular TMB
    tmb = calcular_tmb(info['sexo'], info['peso'],
                       info['estatura'], info['edad'])
    print(f"  TMB calculada: {tmb:.2f} kcal/día")

    # Filtrar filas del usuario
    mask = df['Usuario'] == usuario_id
    num_registros = mask.sum()
    print(f"  Registros encontrados: {num_registros}")

    # Asignar TMB a todas las filas del usuario
    df.loc[mask, 'TMB'] = tmb

    # Calcular Superávit Calórico Basal
    df.loc[mask, 'Superavit_calorico_basal'] = (
        df.loc[mask, 'Gasto_calorico_activo'] * 100) / tmb

# Verificar los resultados
print("\n" + "="*80)
print("RESUMEN DE RESULTADOS")
print("="*80)

for usuario_id in usuarios_info.keys():
    mask = df['Usuario'] == usuario_id
    if mask.any():
        tmb_usuario = df.loc[mask, 'TMB'].iloc[0]
        superavit_mean = df.loc[mask, 'Superavit_calorico_basal'].mean()
        superavit_min = df.loc[mask, 'Superavit_calorico_basal'].min()
        superavit_max = df.loc[mask, 'Superavit_calorico_basal'].max()

        print(f"\n{usuario_id}:")
        print(f"  TMB: {tmb_usuario:.2f} kcal/día")
        print(f"  Superávit Calórico Basal - Media: {superavit_mean:.2f}%")
        print(f"  Superávit Calórico Basal - Mín: {superavit_min:.2f}%")
        print(f"  Superávit Calórico Basal - Máx: {superavit_max:.2f}%")

# Guardar el archivo actualizado
output_file = 'DB_usuarios_consolidada_con_actividad_relativa.csv'
print(f"\n{'='*80}")
print(f"Guardando archivo actualizado: {output_file}")
df.to_csv(output_file, index=False)
print("¡Archivo guardado exitosamente!")

# Mostrar las primeras filas
print("\n" + "="*80)
print("PRIMERAS 5 FILAS DEL ARCHIVO ACTUALIZADO:")
print("="*80)
print(df[['Fecha', 'Usuario', 'Gasto_calorico_activo',
      'TMB', 'Superavit_calorico_basal']].head())

print("\n" + "="*80)
print("PROCESO COMPLETADO")
print("="*80)
print(f"Total de registros procesados: {len(df)}")
print(f"Columnas en el archivo final: {len(df.columns)}")
print(f"Nueva variable 'Superavit_calorico_basal' agregada exitosamente")
