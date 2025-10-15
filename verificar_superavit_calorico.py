import pandas as pd
import numpy as np

# Leer el archivo actualizado
df = pd.read_csv('DB_usuarios_consolidada_con_actividad_relativa.csv')

print("="*100)
print("VERIFICACIÓN DE LA VARIABLE 'SUPERAVIT_CALORICO_BASAL'")
print("="*100)

# Información de usuarios
usuarios_info = {
    'Usuario_1': 'ale (Mujer, 68kg, 170cm, 34 años)',
    'Usuario_2': 'brenda (Mujer, 76kg, 169cm, 37 años)',
    'Usuario_3': 'christina (Mujer, 77kg, 164cm, 39 años)',
    'Usuario_4': 'edson (Hombre, 100kg, 180cm, 25 años)',
    'Usuario_5': 'esmeralda (Mujer, 64kg, 160cm, 28 años)',
    'Usuario_6': 'fidel (Hombre, 100kg, 180cm, 34 años)',
    'Usuario_7': 'kevin (Hombre, 92kg, 156cm, 32 años)',
    'Usuario_8': 'legarda (Hombre, 92kg, 181cm, 29 años)',
    'Usuario_9': 'lmartinez (Hombre, 124kg, 185cm, 32 años)',
    'Usuario_10': 'vane (Mujer, 58kg, 164cm, 28 años)'
}

print("\n1. INFORMACIÓN GENERAL DEL ARCHIVO")
print("-"*100)
print(f"Total de registros: {len(df)}")
print(f"Total de columnas: {len(df.columns)}")
print(f"Columnas: {', '.join(df.columns.tolist())}")

print("\n2. ESTADÍSTICAS DESCRIPTIVAS POR USUARIO")
print("-"*100)

# Crear resumen estadístico por usuario
resumen = []

for usuario_id in sorted(usuarios_info.keys()):
    mask = df['Usuario'] == usuario_id
    if mask.any():
        datos = df.loc[mask]

        info = {
            'Usuario': usuario_id,
            'Nombre': usuarios_info[usuario_id],
            'N_Registros': len(datos),
            'TMB': datos['TMB'].iloc[0],
            'Gasto_Activo_Media': datos['Gasto_calorico_activo'].mean(),
            'Gasto_Activo_Min': datos['Gasto_calorico_activo'].min(),
            'Gasto_Activo_Max': datos['Gasto_calorico_activo'].max(),
            'Superavit_Media': datos['Superavit_calorico_basal'].mean(),
            'Superavit_Mediana': datos['Superavit_calorico_basal'].median(),
            'Superavit_Min': datos['Superavit_calorico_basal'].min(),
            'Superavit_Max': datos['Superavit_calorico_basal'].max(),
            'Superavit_Std': datos['Superavit_calorico_basal'].std()
        }
        resumen.append(info)

df_resumen = pd.DataFrame(resumen)

# Mostrar el resumen
for idx, row in df_resumen.iterrows():
    print(f"\n{row['Usuario']}: {row['Nombre']}")
    print(f"  Registros: {int(row['N_Registros'])}")
    print(f"  TMB: {row['TMB']:.2f} kcal/día")
    print(
        f"  Gasto Calórico Activo: Media={row['Gasto_Activo_Media']:.2f}, Min={row['Gasto_Activo_Min']:.2f}, Max={row['Gasto_Activo_Max']:.2f}")
    print(
        f"  Superávit Calórico Basal (%): Media={row['Superavit_Media']:.2f}, Mediana={row['Superavit_Mediana']:.2f}")
    print(
        f"                                 Min={row['Superavit_Min']:.2f}, Max={row['Superavit_Max']:.2f}, Std={row['Superavit_Std']:.2f}")

print("\n3. COMPARACIÓN ENTRE HOMBRES Y MUJERES")
print("-"*100)

# Separar por sexo
usuarios_hombres = ['Usuario_4', 'Usuario_6',
                    'Usuario_7', 'Usuario_8', 'Usuario_9']
usuarios_mujeres = ['Usuario_1', 'Usuario_2',
                    'Usuario_3', 'Usuario_5', 'Usuario_10']

hombres_data = df[df['Usuario'].isin(usuarios_hombres)]
mujeres_data = df[df['Usuario'].isin(usuarios_mujeres)]

print(
    f"\nHOMBRES (n={len(usuarios_hombres)} usuarios, {len(hombres_data)} registros):")
print(f"  TMB Media: {hombres_data['TMB'].mean():.2f} kcal/día")
print(
    f"  Gasto Calórico Activo Media: {hombres_data['Gasto_calorico_activo'].mean():.2f} kcal")
print(
    f"  Superávit Calórico Basal Media: {hombres_data['Superavit_calorico_basal'].mean():.2f}%")
print(
    f"  Superávit Calórico Basal Mediana: {hombres_data['Superavit_calorico_basal'].median():.2f}%")

print(
    f"\nMUJERES (n={len(usuarios_mujeres)} usuarios, {len(mujeres_data)} registros):")
print(f"  TMB Media: {mujeres_data['TMB'].mean():.2f} kcal/día")
print(
    f"  Gasto Calórico Activo Media: {mujeres_data['Gasto_calorico_activo'].mean():.2f} kcal")
print(
    f"  Superávit Calórico Basal Media: {mujeres_data['Superavit_calorico_basal'].mean():.2f}%")
print(
    f"  Superávit Calórico Basal Mediana: {mujeres_data['Superavit_calorico_basal'].median():.2f}%")

print("\n4. DISTRIBUCIÓN DEL SUPERÁVIT CALÓRICO BASAL (TODOS LOS USUARIOS)")
print("-"*100)

# Crear rangos de superávit calórico
rangos = [0, 10, 20, 30, 40, 50, 100, float('inf')]
etiquetas = ['0-10%', '10-20%', '20-30%',
             '30-40%', '40-50%', '50-100%', '>100%']

df['Rango_Superavit'] = pd.cut(
    df['Superavit_calorico_basal'], bins=rangos, labels=etiquetas, include_lowest=True)
distribucion = df['Rango_Superavit'].value_counts().sort_index()

print("\nDistribución de registros por rango de Superávit Calórico Basal:")
for rango, count in distribucion.items():
    porcentaje = (count / len(df)) * 100
    print(f"  {rango}: {count:4d} registros ({porcentaje:5.2f}%)")

print("\n5. EJEMPLOS DE REGISTROS")
print("-"*100)

# Mostrar algunos ejemplos
print("\nPrimeros 5 registros con mayor Superávit Calórico Basal:")
top5 = df.nlargest(5, 'Superavit_calorico_basal')[
    ['Fecha', 'Usuario', 'Gasto_calorico_activo', 'TMB', 'Superavit_calorico_basal']]
for idx, row in top5.iterrows():
    print(f"  {row['Fecha']} - {row['Usuario']}: Gasto={row['Gasto_calorico_activo']:.2f} kcal, TMB={row['TMB']:.2f} kcal, Superávit={row['Superavit_calorico_basal']:.2f}%")

print("\n6. GUARDAR RESUMEN EN ARCHIVO CSV")
print("-"*100)

df_resumen.to_csv('resumen_superavit_calorico_basal.csv', index=False)
print("Archivo 'resumen_superavit_calorico_basal.csv' guardado exitosamente")

print("\n" + "="*100)
print("VERIFICACIÓN COMPLETADA")
print("="*100)

