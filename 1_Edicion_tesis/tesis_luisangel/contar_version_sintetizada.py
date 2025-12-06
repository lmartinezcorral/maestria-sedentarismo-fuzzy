import re

text = """El comportamiento sedentario (CS), definido como actividad en vigilia con gasto energético ≤1.5 METs, constituye el cuarto factor de riesgo de mortalidad según la OMS. Su medición objetiva en condiciones de vida libre representa un vacío metodológico, pues los cuestionarios de autoinforme (ej. IPAQ) presentan sesgo de memoria, mientras que las técnicas de laboratorio (calorimetría indirecta, actigrafía) no capturan la complejidad del comportamiento humano. Este estudio desarrolló un modelo de clasificación del sedentarismo mediante lógica difusa que integra datos biométricos de dispositivos wearables, aplicado bajo el paradigma Bring Your Own Device (BYOD) en condiciones de vida libre. La cohorte se conformó por 10 adultos jóvenes con seguimiento multianual mediante Apple Watch. Se propusieron cuatro variables derivadas: actividad relativa, superávit calórico basal, delta cardíaco y variabilidad de la frecuencia cardíaca (HRV). La metodología empleó clustering K-Means no supervisado para establecer verdad operativa, seguido de un Sistema de Inferencia Difusa Mamdani con cinco reglas lingüísticas interpretables. El sistema se validó mediante Leave-One-User-Out, demostrando F1-Score=0.780±0.167 (CV=21.4%), resultados que validan una herramienta fiable y transparente para el diseño de intervenciones de salud personalizadas, contribuyendo a la mitigación de este riesgo sanitario mediante la promoción de estilos de vida activos."""

words = re.findall(r'\b\w+\b', text)
sentences = [s.strip() for s in text.split('.') if s.strip()]

print('=== ANÁLISIS VERSIÓN SINTETIZADA ===')
print(f'Total palabras: {len(words)}')
print(f'Límite: 250 palabras')
exceso = len(words) - 250
if exceso <= 0:
    print(f'Estado: ✅ DENTRO DEL LÍMITE ({abs(exceso)} palabras bajo el límite)')
else:
    print(f'Estado: ❌ EXCEDE ({exceso} palabras)')
print(f'Total oraciones: {len(sentences)}')
print(f'Promedio palabras/oración: {len(words) / len(sentences):.1f}')


