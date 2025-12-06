import re

text = """El comportamiento sedentario (gasto energético ≤1.5 METs) representa un factor de riesgo para enfermedades crónicas no transmisibles. Su medición en condiciones de vida libre permite capturar la variabilidad del comportamiento humano en entornos naturalísticos. Los cuestionarios de autoinforme adolecen de sesgos de memoria y deseabilidad social, mientras que las técnicas de referencia se restringen a laboratorio. Se desarrolló un sistema de clasificación del sedentarismo mediante lógica difusa que integra datos biométricos de dispositivos portátiles de consumo, aplicado bajo el paradigma Bring Your Own Device (BYOD) en condiciones de vida libre. La cohorte de adultos jóvenes se conformó por 10 participantes con seguimiento multianual (media: 133.7 semanas), acumulando 9,185 días de registro biométrico continuo mediante Apple Watch. Tras preprocesamiento (imputación jerárquica, normalización antropométrica), se generaron 1,337 semanas válidas. Se propusieron cuatro variables derivadas: Actividad relativa, Superávit calórico basal, Delta cardíaco y HRV-SDNN. Se utilizó clustering K-Means no supervisado (k=2) para establecer verdad operativa, seguido de un Sistema de Inferencia Difusa Mamdani con cinco reglas lingüísticas interpretables. El sistema se validó mediante Leave-One-User-Out, demostrando F1-Score=0.780±0.167 (Precisión=0.800, Sensibilidad=0.783), con variabilidad inter-sujeto (CV=21.4%), superando estudios comparables. Estos resultados respaldan que el sistema propuesto ofrece una clasificación fiable del comportamiento sedentario respecto a la verdad operativa, con reglas interpretables aplicables a monitorización continua en condiciones de vida libre en salud pública."""

words = re.findall(r'\b\w+\b', text)
sentences = [s.strip() for s in text.split('.') if s.strip()]

print('=== ANÁLISIS VERSIÓN MEJORADA ===')
print(f'Total palabras: {len(words)}')
print(f'Límite: 250 palabras')
exceso = len(words) - 250
if exceso <= 0:
    print(f'Estado: ✅ DENTRO DEL LÍMITE ({exceso} palabras)')
else:
    print(f'Estado: ❌ EXCEDE ({exceso} palabras)')
print(f'Total oraciones: {len(sentences)}')
print(f'Promedio palabras/oración: {len(words) / len(sentences):.1f}')

