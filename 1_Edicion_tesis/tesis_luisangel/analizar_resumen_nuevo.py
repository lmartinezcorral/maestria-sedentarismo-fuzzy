import re

text = """El comportamiento sedentario se define como cualquier actividad en vigilia con gasto energético ≤1.5 METs en posición sentada, reclinada o acostada, y representa un factor de riesgo para enfermedades crónicas no transmisibles. Su medición en condiciones de vida libre permite capturar la variabilidad del comportamiento humano en entornos naturalísticos reales. Los métodos tradicionales de evaluación (cuestionarios de autoinforme) adolecen de sesgos de memoria (incapacidad para recordar con precisión la actividad realizada) y deseabilidad social (tendencia a reportar comportamientos socialmente aceptables), mientras que las técnicas de referencia del estado del arte (calorimetría indirecta, actigrafía de investigación) se restringen a entornos de laboratorio que no capturan la complejidad del comportamiento en condiciones de vida libre. En este proyecto de tesis se desarrolló un sistema de clasificación del sedentarismo mediante lógica difusa que integra datos biométricos de dispositivos portátiles de consumo, aplicado bajo el paradigma Bring Your Own Device (BYOD) en condiciones de vida libre. La cohorte de adultos jóvenes se conformó por 10 participantes con seguimiento longitudinal retrospectivo multianual (media: 133.7 semanas; rango: 7-298 semanas), acumulando 9,185 días de registro biométrico continuo mediante Apple Watch. Tras preprocesamiento (imputación jerárquica, normalización antropométrica), se generaron 1,337 semanas válidas. Se analizaron las variables entregadas por el Apple Watch y se propusieron cuatro variables derivadas: Actividad relativa, Superávit calórico basal, Delta cardíaco y Variabilidad de frecuencia cardíaca (desviación estándar de intervalos NN). Tras este procesamiento, se utilizó un enfoque híbrido basado en clustering K-Means no supervisado (k=2) para establecer verdad operativa. Con base en la verdad operativa y las variables derivadas, se diseñó un Sistema de Inferencia Difusa Mamdani para determinar el tipo de sedentarismo mediante cinco reglas lingüísticas interpretables. El sistema se validó mediante Leave-One-User-Out, demostrando F1-Score=0.780±0.167 (Precisión=0.800, Sensibilidad=0.783), con variabilidad inter-sujeto (CV=21.4%), superando estudios del estado del arte de otros autores en cohortes comparables. Estos resultados respaldan que el sistema propuesto ofrece una clasificación fiable del comportamiento sedentario respecto a la verdad operativa derivada del clustering, y mantiene la interpretabilidad clínica mediante reglas transparentes aplicables a la monitorización continua en condiciones de vida libre en salud pública."""

words = re.findall(r'\b\w+\b', text)
sentences = [s.strip() for s in text.split('.') if s.strip()]

print('=== ANÁLISIS NUEVA VERSIÓN ===')
print(f'Total palabras: {len(words)}')
print(f'Límite: 250 palabras')
exceso = len(words) - 250
print(f'Exceso: {exceso} palabras ({exceso/250*100:.1f}% sobre límite)')
print(f'Total oraciones: {len(sentences)}')
print(f'Promedio palabras/oración: {len(words) / len(sentences):.1f}')

print('\n=== VERIFICACIÓN TÉRMINOS ===')
print(f'"ecológico" encontrado: {text.count("ecológico")} veces')
print(f'"condiciones de vida libre" encontrado: {text.count("condiciones de vida libre")} veces')
print(f'"vida libre" encontrado: {text.count("vida libre")} veces')

print('\n=== VERIFICACIÓN MÉTRICAS ===')
if 'F1-Score=0.780' in text:
    print('✅ F1-Score correcto: 0.780')
if '±0.167' in text:
    print('✅ Desviación estándar incluida: ±0.167')
if 'Precisión=0.800' in text:
    print('⚠️ Precisión: 0.800 (verificar valor correcto)')
if 'Sensibilidad=0.783' in text:
    print('⚠️ Sensibilidad: 0.783 (verificar si es Recall o Sensibilidad)')
if 'CV=21.4%' in text:
    print('⚠️ CV: 21.4% (verificar valor correcto)')

