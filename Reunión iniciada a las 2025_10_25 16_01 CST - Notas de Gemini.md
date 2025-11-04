# 📝 Notas

25 oct 2025

## Reunión del 25 oct 2025 a las 16:01 CST

Registros de la reunión [Transcripción](?tab=t.mjcc7am6fvg) 

### Resumen

Abimael Guzman Pando, luis martinez corral y David Ricardo Lopez Flores discutieron la normalización, gestión e imputación de datos, así como los principios de diseño de algoritmos, centrándose en el manejo de datos faltantes y la imputación jerárquica para variables cardiovasculares. luis martinez corral explicó la ingeniería de variables como el superávit calórico y la actividad relativa, y presentó un sistema de inferencia difuso con cuatro variables de entrada para clasificar el sedentarismo, el cual mostró un F1 score superior al 80% y buena generalización para usuarios no vistos. Se acordó que luis martinez corral se enfocará en documentar el trabajo actual en la tesis y en integrar la información del cuestionario SF36.

### Detalles

* **Normalización de datos** Abimael Guzman Pando y luis martinez corral discutieron el proceso de normalización de datos. Se debe dividir el conjunto de datos en nueve partes para entrenamiento y una para validación, aplicando la normalización solo a la parte de entrenamiento y luego aplicando el ajuste resultante a la parte de validación sin realizar un nuevo ajuste. Este proceso debe repetirse 10 veces, cambiando el usuario que se deja fuera cada vez ([00:00:00](#00:00:00)).

* **Gestión de datos faltantes** luis martinez corral explicó el mecanismo para identificar y manejar datos faltantes, especialmente los relacionados con las horas monitorizadas del Apple Watch ([00:01:02](#00:01:02)). Señaló que hay criterios de inclusión que pueden llevar a la pérdida de datos, como desechar una semana completa si ciertos días tienen menos de 10 horas monitorizadas. Para abordar esto, se realizó un análisis temporal de la pérdida de indicadores y se establecieron reglas de decisión para la inclusión de bloques de 7 días en el conjunto de datos ([00:02:23](#00:02:23)).

* **Imputación de datos** luis martinez corral describió la estrategia de imputación jerárquica utilizada, la cual avanza siempre hacia adelante y emplea medianas globales para completar los datos faltantes, siempre y cuando no se violen las reglas de decisión iniciales. Se mencionaron cinco métodos de imputación, incluyendo la media móvil de 7 días previos y la mediana del mismo día de la semana del último mes ([00:03:53](#00:03:53)). David Ricardo Lopez Flores y Abimael Guzman Pando resaltaron la importancia de esta estrategia híbrida de imputación ([00:06:05](#00:06:05)).

* **Principios de diseño de algoritmos** luis martinez corral enfatizó la importancia de respetar principios estadísticos, computacionales y fisiológicos en el diseño de algoritmos y manejo de datos. Subrayó la necesidad de trabajar dentro de los rangos clínicos fisiológicos del cuerpo humano para asegurar que el análisis de datos tenga sentido ([00:08:53](#00:08:53)). David Ricardo Lopez Flores señaló que esta es una rama de investigación válida ([00:10:20](#00:10:20)).

* **Pseudocódigo para imputación de variables cardiovasculares** luis martinez corral presentó el pseudocódigo para la imputación de variables cardiovasculares clave: frecuencia cardíaca al caminar, frecuencia en reposo y variabilidad de la frecuencia cardíaca ([00:10:20](#00:10:20)). Detalló tres métodos principales de imputación basados en la mediana móvil de los 7 días anteriores, la mediana del último mes y las medianas históricas del usuario ([00:11:46](#00:11:46)). También se mencionó la ecuación de Tanaca para la frecuencia cardíaca máxima, aunque su aplicación en el contexto de la frecuencia en reposo fue cuestionada y se aclaró que era para frecuencia cardíaca máxima ([00:13:16](#00:13:16)).

* **Análisis de pérdida e imputación de datos** luis martinez corral proporcionó datos sobre la pérdida de variables, indicando que la frecuencia cardíaca al caminar perdió el 7.6%, la frecuencia cardíaca en reposo el 4.2%, y la variabilidad de la frecuencia cardíaca fue la que más pérdida presentó ([00:16:31](#00:16:31)). Se explicó que se realizó un análisis de auditoría dual para no perder datos, manteniendo tablas de datos observados e imputados, y señalando el método de imputación utilizado ([00:18:13](#00:18:13)).

* **Rangos fisiológicos y mejora de la calidad de datos** luis martinez corral reafirmó que los valores utilizados para la frecuencia cardíaca y su variabilidad se basan en normas fisiológicas estándar y guías clínicas ([00:18:13](#00:18:13)). La estrategia jerárquica de imputación redujo la pérdida de la variabilidad cardíaca del 14.8% a 0%, lo que significa una mejora significativa en la calidad de los datos ([00:19:58](#00:19:58)).

* **Ingeniería de variables: Superávit calórico y actividad relativa** luis martinez corral explicó la ingeniería de variables para el superávit calórico y la actividad relativa, justificando su necesidad para una interpretación más precisa de los datos. El superávit calórico se define como el gasto energético por encima de la tasa metabólica basal, que depende de sexo, edad, peso y estatura, y se ajusta para reflejar que 500 calorías no representan lo mismo para personas de diferente peso ([00:21:06](#00:21:06)). La actividad relativa se calcula como pasos por hora de uso del dispositivo para normalizar el nivel de actividad ([00:24:40](#00:24:40)).

* **Análisis de variabilidad y correlación** Se presentó un análisis de variabilidad y correlación para las variables de actividad relativa, mostrando cómo esta variable reduce la varianza entre sujetos al homogeneizar las medianas de pasos, lo que permite un agrupamiento (clustering) más justo ([00:26:41](#00:26:41)). No obstante, Abimael Guzman Pando sugirió que esta homogeneización podría afectar negativamente la capacidad del clustering para discriminar entre grupos, ya que las variables con mayor varianza podrían ser más útiles para la separación de datos ([00:28:06](#00:28:06)).

* **Consideraciones para futuros análisis** Se acordó que luis martinez corral consideraría volver a realizar el análisis de clustering sin esta homogeneización para el futuro, especialmente para publicaciones JCR. David Ricardo Lopez Flores y Abimael Guzman Pando sugirieron que se anoten estas ideas para una futura implementación en publicaciones, ya que implicarían volver a correr los códigos ([00:30:53](#00:30:53)) ([00:39:27](#00:39:27)).

* **Clasificación del superávit calórico** luis martinez corral explicó una clasificación del superávit calórico basada en percentiles para categorizar la actividad física en sedentaria, moderada y vigorosa. La tasa metabólica basal se calcula usando la ecuación de Harris Benedict ([00:30:53](#00:30:53)).

* **Homogeneidad de las variables antropométricas** luis martinez corral mostró que los usuarios presentan heterogeneidad antropométrica, lo que justifica la normalización de las variables de actigrafía para ajustar el impacto de la actividad por cada usuario ([00:43:15](#00:43:15)). Se argumentó que el superávit calórico y la actividad relativa son variables cruciales para homogeneizar el grupo y permitir una clasificación precisa ([00:35:15](#00:35:15)).

* **Variables cardiovasculares en el modelo** luis martinez corral enfatizó la inclusión de variables cardiovasculares como la frecuencia del delta cardíaco (frecuencia al caminar menos frecuencia en reposo) y la variabilidad de la frecuencia cardíaca ([00:44:46](#00:44:46)). Estas variables proporcionan una visión importante del estado fisiológico del usuario, ya que la actividad física por sí sola (pasos, calorías) no captura completamente el sedentarismo desde una perspectiva fisiológica ([00:43:15](#00:43:15)). Una variabilidad de la frecuencia cardíaca baja puede indicar estrés o fatiga ([00:46:33](#00:46:33)).

* **Correlación de variables para clustering** Se presentó una matriz de correlación de Spearman que mostró que la variabilidad de la frecuencia cardíaca tiene correlaciones muy bajas con las variables de actividad, lo que valida que el tono vagal es un dominio ortogonal al volumen de movimiento. Estas cuatro variables (actividad relativa, superávit calórico, variabilidad de la frecuencia cardíaca y delta cardíaco) son las entradas al sistema difuso para clustering y modelado ([00:48:11](#00:48:11)).

* **Herramientas de codificación** luis martinez corral compartió que está utilizando Cursor, una herramienta similar a Visual Studio Code pero con inteligencia artificial integrada, para generar código, ejecutarlo en consola, generar logs y documentaciones ([00:51:29](#00:51:29)).

* **Reglas de inferencia del sistema difuso** Se mostró una tabla con reglas de inferencia para el sistema difuso, donde combinaciones de variables de entrada (actividad relativa, superávit calórico, variabilidad de la frecuencia cardíaca y delta cardíaco) se asocian con perfiles de usuario como "sedentario" y un puntaje de salida ([00:54:18](#00:54:18)). David Ricardo Lopez Flores solicitó una explicación más profunda sobre por qué estas cuatro variables específicas se seleccionaron como entradas para el modelo difuso ([00:55:43](#00:55:43)).

* **Adaptación de Variables al Movimiento Humano** luis martinez corral explicó que las variables utilizadas se adaptan mejor a los volúmenes de movimiento de una persona ([00:57:07](#00:57:07)). Abimael Guzman Pando señaló que algunas variables son derivadas, lo que las hace redundantes y justifica su eliminación. La eliminación de variables como "minutos de ejercicio" y "minutos de movimiento" ayuda a evitar la multicolinealidad, según luis martinez corral ([01:00:18](#01:00:18)).

* **Selección de Variables para Clustering** David Ricardo Lopez Flores expresó dudas sobre la justificación de las variables aceptadas para el clustering y el modelado difuso, solicitando una argumentación más convincente en la tesis ([01:00:18](#01:00:18)). luis martinez corral identificó cuatro variables cardíacas y de movimiento —actividad relativa, superávit calórico, variabilidad de la frecuencia cardíaca y delta cardíaco— como las elegidas para clasificar patrones de movimiento y función cardiovascular ([00:58:41](#00:58:41)).

* **Monitoreo Semanal y Sedentarismo** luis martinez corral propuso monitorear a las personas durante 7 días continuos, basándose en la recomendación de la OMS de 150 minutos de actividad física moderada a vigorosa por semana. Explicó que, si una persona cumple la meta semanal en un solo día, la medición por "outer" podría clasificarla incorrectamente como sedentaria a pesar de su alta actividad en un día específico ([01:01:29](#01:01:29)). David Ricardo Lopez Flores aclaró que cumplir con los 150 minutos semanales de actividad, independientemente de cómo se acumulen, significa no ser sedentario ([01:02:35](#01:02:35)).

* **Criterios de Validez y Completitud de Datos** Se estableció que el criterio de validez para el análisis requiere al menos 5 días con datos completos. luis martinez corral informó que se obtuvieron 1337 semanas válidas, con 16 características y cuatro variables destinadas al modelo de clustering y lógica difusa ([01:04:00](#01:04:00)). Se implementó un análisis de variabilidad dual para comparar datos crudos con datos imputados, aceptando la imputación si el coeficiente de variación del delta cardíaco es menor al 5% ([01:06:08](#01:06:08)).

* **Análisis de Correlación y Homogeneidad de Datos** luis martinez corral indicó que la matriz de correlación mostró que las variables relacionadas con el volumen de actividad física (actividad relativa y superávit calórico) presentaban una correlación moderada a fuerte. Sin embargo, las variables cardiovasculares (variabilidad de la frecuencia cardíaca y delta cardíaco) mostraron correlaciones más débiles, sugiriendo dominios fisiológicos distintos. Abimael Guzman Pando y David Ricardo Lopez Flores notaron que las matrices de correlación diarias y semanales eran similares, lo que llevó a la preocupación de que el comportamiento de los datos se estuviera homogeneizando y dificultando la separación de los clusters ([01:10:42](#01:10:42)) ([01:24:58](#01:24:58)).

* **Personalización del Comportamiento del Usuario** luis martinez corral enfatizó la necesidad de individualizar las características de cada usuario en lugar de generalizar los modelos, especialmente con la variable del superávit calórico. Se sugirió usar diagramas de dispersión y diagramas de caja para la defensa de la tesis, evitando detalles técnicos sobre el código ([01:15:29](#01:15:29)).

* **Confusión con las Variables de Entrada al Clustering** David Ricardo Lopez Flores expresó su confusión sobre las variables utilizadas para el clustering, ya que se mencionaron las cuatro variables principales inicialmente (actividad relativa, superávit calórico, HRB y delta cardíaco), pero luego se hizo referencia a ocho características que incluían percentiles y rangos intercuartílicos ([01:20:34](#01:20:34)) ([01:28:40](#01:28:40)). luis martinez corral aclaró que las cuatro variables originales fueron las que realmente entraron al clustering, mientras que el análisis de Componentes Principales (PCA) que mostraba ocho variables era erróneo ([01:30:08](#01:30:08)).

* **Resultados del Clustering y Definición de Grupos** El clustering resultó en dos grupos claramente distintos basados en el comportamiento de actividad y gasto calórico ([01:26:17](#01:26:17)). Se decidió renombrar los grupos como "sedentario" (alto sedentarismo) y "activo" (bajo sedentarismo) ([01:33:28](#01:33:28)). Se observó que la variabilidad de la frecuencia cardíaca no discriminaba eficazmente los clusters, planteando la pregunta de si era prescindible en el modelo difuso ([01:34:45](#01:34:45)).

* **Sistema de Inferencia Difuso** El objetivo del sistema difuso es construir un modelo interpretable que clasifique el nivel de sedentarismo semanal utilizando conocimiento experto y reglas fisiológicas. El sistema utiliza cuatro entradas continuas normalizadas, funciones de pertenencia triangulares, y cinco reglas basadas en conocimiento clínico ([01:35:54](#01:35:54)). La meta es lograr un F1 score de 0.70 contra la verdad operativa para validar el modelo ([01:37:19](#01:37:19)). Se aclaró que los percentiles se usan para definir los parámetros de las funciones de membresía, no como entradas directas al sistema difuso ([01:43:55](#01:43:55)).

* **Visualización del modelo** luis martinez corral presentó un modelo con visualizaciones, incluyendo una matriz de antecedentes, consecuentes y cobertura clínica ([01:53:39](#01:53:39)). El modelo difuso, con cuatro entradas y cinco reglas clínicas, ofrece una salida continua de 0 a 1 basada en percentiles empíricos, y está listo para validación. David Ricardo Lopez Flores consultó si el modelo fue desarrollado con inteligencia artificial, a lo que luis martinez corral confirmó que sí, y explicó que utilizó un chat para pasar artículos y generar matrices y análisis ([01:54:54](#01:54:54)).

* **Documentación del modelo** David Ricardo Lopez Flores enfatizó la importancia de asegurar que la documentación del modelo se alinee con el estado del arte para evitar inconsistencias y la invención de términos ([01:57:22](#01:57:22)). luis martinez corral indicó que utilizó una conexión entre Chat GPT y Cursor para la codificación y Gemini para la parte literaria del informe ([02:00:00](#02:00:00)).

* **Evaluación del sistema difuso** luis martinez corral presentó los resultados de la evaluación del sistema difuso, destacando una concordancia con el clustering y un F1 score superior al 80% ([02:00:00](#02:00:00)). Las métricas de desempeño incluyen precisión, sensibilidad y el F1 score, con una precisión del 74% y un recall del 97.6% para sedentarismo alto. Abimael Guzman Pando y David Ricardo Lopez Flores preguntaron sobre la verdad operativa y la aplicación de las métricas, aclarando luis martinez corral que se utilizó validación cruzada y el clustering como verdad operativa ([02:01:36](#02:01:36)).

* **Generalización del modelo y robustez** luis martinez corral afirmó que el modelo generaliza aceptablemente para usuarios no vistos, con un F1 score del 81% ([02:05:20](#02:05:20)). Esto sugiere que el sistema difuso captura patrones universales. Se realizó un análisis de robustez que mostró una disminución del rendimiento al 60% al utilizar dos variables en lugar de cuatro, indicando que las variables cardíacas, aunque no discriminatorias univariadamente, aportan valor en combinaciones multivariadas ([02:08:51](#02:08:51)).

* **Metodología de validación** David Ricardo Lopez Flores y luis martinez corral discutieron la metodología de validación, específicamente la aplicación del modelo con el método "one user out" (9-1), donde un usuario se utiliza para pruebas y los otros nueve para entrenamiento. Este método permite aplicar el modelo al comportamiento lineal completo de un usuario, a diferencia de una división aleatoria 80/20. luis martinez corral mencionó que la sugerencia del enfoque 9-1 provino de la inteligencia artificial ([02:04:11](#02:04:11)) ([02:11:24](#02:11:24)).

* **Ejemplos prácticos y funciones de pertenencia** luis martinez corral presentó ejemplos prácticos del sistema difuso, mostrando cómo se aplican las funciones de pertenencia y el proceso de inferencia ([02:12:52](#02:12:52)). Estos ejemplos ilustran la clasificación de diferentes escenarios de sedentarismo, incluyendo casos de baja actividad física con alta variabilidad cardíaca, lo cual el sistema reconoce como un estado compensatorio donde la persona está sedentaria pero se siente bien ([02:17:46](#02:17:46)).

* **Alineación con el estado del arte y contribuciones** David Ricardo Lopez Flores reiteró la importancia de alinear la documentación con el estado del arte, pidiendo a luis martinez corral que se asegure de que las secciones estén enlazadas y que los términos sean uniformes en toda la tesis ([02:22:02](#02:22:02)). David Ricardo Lopez Flores también alentó a luis martinez corral a identificar sus propias contribuciones, sugiriendo que responda a los "gaps" o vacíos en la literatura con sus hallazgos ([02:25:41](#02:25:41)).

* **Plan de trabajo para la tesis** Se acordó que luis martinez corral se concentrará en documentar el trabajo actual en la tesis, dejando cualquier implementación futura para una posible publicación en JCR ([02:26:58](#02:26:58)). El objetivo es que luis martinez corral envíe borradores de la tesis por secciones para revisión, comenzando con los resultados y la delimitación del objeto de estudio ([02:30:20](#02:30:20)). La discusión y las conclusiones se abordarán posteriormente, buscando una bibliografía sólida para respaldar los argumentos ([02:31:24](#02:31:24)).

* **Uso del cuestionario SF36** Se confirmó que el cuestionario de calidad de vida SF36 sí debe documentarse en la tesis, ya que se utilizó para validar el modelo difuso ([02:32:34](#02:32:34)). Aunque no se pudo hacer una validación completa con todos los usuarios debido a la baja participación, se explorará la correlación entre los resultados del sistema difuso y la percepción subjetiva de calidad de vida de cada usuario, posiblemente desde los diagramas descriptivos ([02:33:42](#02:33:42)).

### Pasos siguientes recomendados

- [ ] luis martinez corral considerará y volverá a hacer el análisis de clustering sin la homogeneización de la actividad relativa para ver si mejora la diferenciación de grupos.  
- [ ] luis martinez corral intentará pasar al algoritmo las calorías activas y la tasa metabólica basal como entrada en lugar del cálculo final del superavit calórico para ver si permite una mejor diferenciación de grupos.  
- [ ] luis martinez corral tomará nota de las consideraciones de Abimael Guzman Pando que implican correr de nuevo los códigos para el JCR.  
- [ ] luis martinez corral tendrá que ser más convincente al documentar en la tesis la justificación de por qué esas variables se aceptaron para cluster y modelado difuso.  
- [ ] luis martinez corral checará el razonamiento de la mediana por un patrón habitual de 7 días antes de concluir sobre la exclusión de ciertas personas en la categoría de sedentarios.  
- [ ] luis martinez corral manejará el diagrama de dispersión y los diagramas de cajas para la defensa de tesis.  
- [ ] luis martinez corral corregirá el gráfico de funciones de membresía de actividad relativa para que se vea igual que los demás y checará el script de PCA para las cuatro variables principales.  
- [ ] luis martinez corral incluirá la gráfica de clustering usando las cuatro variables con el TCA, PSA, y TSNE en la tesis.  
- [ ] luis martinez corral evitará que las confusiones creadas durante la discusión queden en la tesis, asegurando enlazar las secciones del documento y uniformizar los nombres de las variables.  
- [ ] luis martinez corral enviará el documento actualizado a los otros participantes para su revisión.  
- [ ] luis martinez corral documentará el cuestionario de calidad SF36 en la tesis y lo relacionará con los resultados de fusi, verificando las salidas de la consola y las matrices generadas.  
- [ ] luis martinez corral documentará los resultados y la delimitación del objeto de estudio en la plantilla de tesis para un vistazo general, y posteriormente trabajará en la discusión y conclusiones, buscando bibliografía para respaldar la argumentación.

*Revisa las notas de Gemini para asegurarte de que sean correctas. [Obtén consejos y descubre cómo toma notas Gemini](https://support.google.com/meet/answer/14754931)*

*Danos tu opinión sobre el uso de Gemini para tomar notas en una [breve encuesta.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=bdSVn8ZkWM2ivRnM2pVODxIOOAIIigIgABgBCA&detailid=unspecified)*

# 📖 Transcripción

25 oct 2025

## Reunión del 25 oct 2025 a las 16:01 CST \- Transcripción

### 00:00:00 {#00:00:00}

   
**Abimael Guzman Pando:** dividir primero nueve de entrenamiento y dejar el de validación fuera. Y sobre los nueve de entrenamiento, sobre esos aplicas ahora sí la normalización. Vas a hacer el ajuste de la normalización con esos y aplicas el ajuste que hiciste con el de validación, pero ya sin Ajá.  
**luis martinez corral:** O sea, con el usuario externo fuera, el que está por fuera.  
**Abimael Guzman Pando:** Pero ya ves que en la en la en las ¿cómo se llaman? las las funciones de Python, ¿no?  
**David Ricardo Lopez Flores:** Ok.  
**Abimael Guzman Pando:** Los program en el programa.  
**luis martinez corral:** Sí. Ajá.  
**Abimael Guzman Pando:** Para normalizar le puedes poner fit, que es ajuste. Entonces el fit, el escalador lo vas a hacer con el de training, pero ya sin el fit, o sea, ya con el ajuste que hiciste, con el mismo escalador, ese mismo escalador lo aplicas el de validación, que sería  
**luis martinez corral:** Okay.  
**Abimael Guzman Pando:** el que dejaste fuera. Y eso lo repites 10 veces cambiando el usuario que dejas fuera.  
**luis martinez corral:** Okay.  
**Abimael Guzman Pando:** Sí, así para grabar.  
**luis martinez corral:** Muy bien.  
   
 

### 00:01:02 {#00:01:02}

   
**luis martinez corral:** Sí, igual aquí, ¿cómo se dice? Ya activé el el transcriptor de Ajá. No sé si le sale ahí para para aceptar, para ir tomando nota.  
**Abimael Guzman Pando:** Okay. Entonces, no más eso, cuidar la fuga de datos. Primero dividir en el los 10 fals de dejando uno fuera y luego aplicar este la transformación en el escalador sobre el de entrenamiento, hacer el ajuste sobre esos y después aplicarlo al de validación sin ajuste. Así no más.  
**luis martinez corral:** Okay, muy bien. Okay, entonces ahora sí sigamos con aquí con la presentación de las de las diapositivas.  
**David Ricardo Lopez Flores:** Mm.  
**luis martinez corral:** Este, hicimos pues ahí un mecanismo, ¿cómo se dice?, de ver cuántos datos faltantes teníamos por por semana, eh, ya que como mencionamos hay días donde las horas  
**David Ricardo Lopez Flores:** ¿Qué?  
**luis martinez corral:** monitorizadas del del Apple Watch pues no nos daban, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Okay.  
**luis martinez corral:** Eh, ni las 10 horas. De hecho, no me acuerdo exactamente cómo ajusté el eh el criterio de admisión. No, no sé si a ocho o a 10, pero pues, ¿cómo se dice?  
   
 

### 00:02:23 {#00:02:23}

   
**luis martinez corral:** Ahí ahí tenemos otra fuga de datos al al ¿cómo se dice? al estandarizar a a una semana, porque también hay criterios de inclusión donde tenemos que Sí, porque estamos ya eligiendo 7 días, lunes a domingo, pero por decir si a lo mejor martes y jueves eh  
**Abimael Guzman Pando:** con todos los datos. Mhm.  
**luis martinez corral:** tuvieron menos de 10 horas monitorizadas, pues ya esa semana ya no la valeamos y desechamos todos esos esos datos eh en algunos en algunos momentos, ¿cómo se dice? Pues podemos arrastrar por por las medianas móviles, pero en otros no. Entonces, de ahí que, ¿cómo se dice? Hicimos todo este análisis temporal de de la pérdida de estos indicadores, que que fue una una una parte importante, ¿cómo se dice?  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Para entrar antes al al modelo de de ¿cómo se dice? de de clustering con el patrón temporal por por semana. Ah, aquí está usar imputación que ofrecer autocorrelación. Eh, si la pérdida es menor al 5% considera eliminación directa. Entonces, aquí tenemos ya las la la las reglas de decisión de de cuándo entraba un bloque de 7 días al al conjunto de datos y cuándo se quedaba por fuera.  
   
 

### 00:03:53 {#00:03:53}

   
**luis martinez corral:** Y al final tuvimos, ¿cómo se dice? eh 1300 semanas que que fueron válidas para el para el modelo. Hm. Y pues hicimos, a ver si ven aquí las figuras, aquí se mencionan Aquí, aquí viene, ¿cómo se dice otra vez? Eh, la imputación jerárquica que hicimos, ¿cómo se dice? siempre hacia el frente, eh aquí, ¿cómo se dice? lo que les decía que que utilizábamos las medianas globales para completar los los datos faltantes siempre y cuanto nos violaban las las reglas de decisión que que mencionamos al al principio. Aquí tenemos la la jerarquía de los cinco métodos, que es la media móvil de 7 días previos, eh la mediana del del mismo día de la semana del último mes, o sea, por ejemplo, martes con martes, eh la mediana histórica del usuario, eh palanca para la frecuencia cardíaca en reposo. ¿En qué casos hizo esta?  
**David Ricardo Lopez Flores:** Ah.  
**luis martinez corral:** Bueno, esta no hay para checarla. No me acuerdo esta regla de Sí.  
**Abimael Guzman Pando:** Es que no sé por qué a mí me aparece el 622 diferente. Luis, el 622 es el que estás viendo.  
   
 

### 00:06:05 {#00:06:05}

   
**Abimael Guzman Pando:** Ah, es que estás en el 62, pero todavía no llegas al Es que se usa se usan las cinco.  
**David Ricardo Lopez Flores:** dos, o sea, la idea de eso es ver cuáles de las cinco estrategias resultó mejor para imputación de datos.  
**luis martinez corral:** No, este se usan las cinco. Si si no entra en un en una en una en una regla de imputación, debe entrar en otra o en otra eh eh en cualquiera de las cinco reglas de imputación. y ya en el último recurso, ¿cómo se dice? Se se, ¿cómo se dice? Ya, ya no se acepta ni se pierde el bloque de 7 días, pero temporal No.  
**Abimael Guzman Pando:** Más adelante viene 622, viene un algoritmo descriptivo y sí se como que se entiende mejor.  
**David Ricardo Lopez Flores:** A ver. A ver, espérame, espérame, espérame. Es que eso, eso me parece importante. A ver, otra vez regrésate ahí. Podemos decir que podemos decir que que ningún trabajo del estado del arte utiliza una estrategia híbrida basada en Chin. Lo voy a poner de M1 a M a M5, ¿no?  
**Abimael Guzman Pando:** de imputación múltiple.  
   
 

### 00:07:33

   
**David Ricardo Lopez Flores:** Ajá. Para cómo sí una estrategia híbrida de imputación, ¿no?  
**Abimael Guzman Pando:** Ajá.  
**David Ricardo Lopez Flores:** De imputación de datos. Sí. Así lo voy a poner entre paréntesis de M1 a M5. Eso ya lo va a entender Luis, yo supongo, ¿no?  
**luis martinez corral:** Sí, que es lo de la sección dos. Igual yo aquí puse el esto para para completar los datos semanales porque de de los  
**David Ricardo Lopez Flores:** Y y para qué se hace eso eh para aumentar la para aumentar la calidad que que contribuye a la calidad  
**Abimael Guzman Pando:** completar datos.  
**luis martinez corral:** a los bloques a los bloques semanales.  
**David Ricardo Lopez Flores:** a la a la calidad del del a la calidad de los datos. Así. O sea, lo estoy poniendo es como un gap.  
**luis martinez corral:** Sí.  
**David Ricardo Lopez Flores:** Eso es un gap. O sea, yo estoy poniendo ese gap como que ningún trabajo del estado del arte utiliza una estrategia híbrida de imputación de datos entre paréntesis de M5 a M de M1 a M5 que contribuye a la calidad, la cual contribuye a la calidad de los datos. Estamos bien, ¿verdad?  
**luis martinez corral:** para la Sí. Okay.  
   
 

### 00:08:53 {#00:08:53}

   
**David Ricardo Lopez Flores:** Ahí está. Sigue, continúa. Yo estoy tratando de identificar esos gaps que al final de cuentas son los que te van a servir para reforzar tu tesis, ¿va? Y que pueden servir como para una publicación. Ok.  
**luis martinez corral:** Este aquí en los principios de de diseño, este, pues respetamos tanto la parte de estadística de análisis de datos computacional y fisiológica, que yo creo que esa es una de las de las, ¿cómo se dice?, de las cosas que de repente cuando está uno trabajando ahí en el código se se bueno, a mí me pasa que se me olvida mucho de repente a canijos, ¿cómo que estoy viendo frecuencias cardíacas de esto en tal comportamiento? Entonces aquí una norma que me puse yo de todos los procesos que estar haciendo es trabajar, como se dice, dentro de los rangos clínicos fisiológicos de de del cuerpo humano, porque si no si cómo se dice, si me  
**Abimael Guzman Pando:** ვერ  
**luis martinez corral:** pierdo de eso, pues ya muchas veces el el trabajo análisis de datos, ¿cómo se dice? pierde pierde sentido. Entonces, estos son los principios de diseños en los que en los que me basé, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Vale.  
**luis martinez corral:** para para llevar todo el todo el, ¿cómo se dice?  
   
 

### 00:10:20 {#00:10:20}

   
**luis martinez corral:** Pues toda la planeación y diseño de los algoritmos y y el manejo de los datos. Okay. Este es el que decías tú, este es el código.  
**Abimael Guzman Pando:** Aha.  
**David Ricardo Lopez Flores:** Abimaelimael pregunta pregunta. Existen solo JCRs donde donde el JCR solo se enfoca al tratamiento de la calidad de los datos, aumentar la calidad de los datos. O sea, en el sentido de que sí usa todo, no sé, por ejemplo, imagínate en tu área una red neuronal con de red profunda, pero que se usó para esto, pero la contribución principal fue en la calidad de los datos.  
**Abimael Guzman Pando:** Sí, creo que sí. También esa es una rama de investigación que existe.  
**David Ricardo Lopez Flores:** Okay. Ah, bueno, pues entonces sí, entonces sí está si está así algo así como que un Yo pienso que si es un gap ahí muy bueno también ese.  
**Abimael Guzman Pando:** Foca una cosa. Mm.  
**David Ricardo Lopez Flores:** Adelante, Luis.  
**luis martinez corral:** Okay. Entonces, pues aquí tenemos este eh pseudocódigo para la imputación de las variables eh cardiovasculares que que son tres principales, la frecuencia al caminar, la frecuencia en reposo y la variabilidad de la de la frecuencia cardíaca.  
   
 

### 00:11:46 {#00:11:46}

   
**luis martinez corral:** Yo sé que ya hemos sido, ¿cómo se dice? eh poco redundantes en esto y ya lo hemos mencionado tanto en sesiones pasadas como como ahorita en esta misma sesión de este día. Eh, pero ¿cómo se dice? Aquí tenemos ahora sí que la la las reglas, ¿cómo se dice?, para para cada una de las de las variables. Eh, el primer método de imputación pues es el la media móvil de los 7 días anteriores. Esto para el para el caso, ¿cómo se dice? De de cuando tenemos datos incompletos. Por decir, si tenemos día lunes, martes, miércoles, eh datos, pero el jueves ya no hay.  
**David Ricardo Lopez Flores:** Amén.  
**luis martinez corral:** Este y hay y hay días anteriores con, o sea, en los 7 días previos hay datos completos, imputamos por la mediana de esos siete de esos 7 días y con eso completamos el jueves. Este, la el segundo método es cuando, por ejemplo, eh tenemos uno o más días que nos falte, ¿cómo se dice? eh datos, por decir, en eh en un en un periodo, ¿cómo se dice?, de un mes, faltan más de dos días. Pues entonces la la media que arrastramos es la del último mes.  
   
 

### 00:13:16 {#00:13:16}

   
**luis martinez corral:** Y en el en el tercer caso, cuando haya haya más de 10 datos faltantes, pues los la las medianas, ¿cómo se dice?, históricas de del usuario, 6 meses, un año, 2 años, es es la que se imputa. Eh, aquí eh el método de estimación por ecuaciones de Tanaca. Eh, aquí nos dice, ¿cómo se dice? eh que la que la frecuencia cardíaca en reposo este menos la edad del usuario por punto s debería ser la frecuencia cardíaca de reposo estimada. Pero esta yo creo que si checamos cómo se dice, los logs de auditoría que hicimos, no creo que se haya utilizado, pero para vamos poniendo un caso práctico, eh, hago la mía.  
**Abimael Guzman Pando:** Creo que por ahí dice que se que se usó el 3%. % Luisa, sí se usó en el 3%.  
**luis martinez corral:** Si si se usó la Okay. Por por ejemplo, tú traes también son 220 también traes 32, ¿verdad?  
**Abimael Guzman Pando:** Sí.  
**luis martinez corral:** Igual 188 por07. Ah, no puse 007\. 20 \- 32 7 sería eso es frecuencia cardíaca máxima.  
   
 

### 00:15:18

   
**Abimael Guzman Pando:** Sí, de hecho acá me está diciendo que es para sacar la frecuencia cardíaca máxima de la ecuación de Tanaca.  
**luis martinez corral:** Así es. Frecuencia cardíaca máxima. Esa no. Sí, de hecho, por eso les decía que todo tiene que ser rangos fisiológicos. Entonces, ah, eh, es que hay un rango, por ejemplo, de hecho, de ahí sale la variable del delta cardíaco,  
**David Ricardo Lopez Flores:** Lo lo dejo.  
**Abimael Guzman Pando:** Pero por ejemplo ahí la máxima sí se concuerda con la de reposo.  
**David Ricardo Lopez Flores:** Pero E Gracias.  
**Abimael Guzman Pando:** Hace que no.  
**luis martinez corral:** delta cardíaco que es esa, que esa sí la vemos más más adelante. Por ejemplo, si tu frecuencia cardíaca en reposo es 55 latidos por minuto y tu frecuencia cardíaca, ah, ya sé para qué se utilizó. Si es justo para eso. Si tu frecuencia cardíaca máxima es 190 lat por minuto y tu frecuencia cardíaca mínima, tenemos un rango. Voy a volver a poner la calculadora aquí. son, dijimos, 220 \- 32 son 188\*7 es 131\. Entonces este sería el rango, ¿cómo se dice?  
   
 

### 00:16:31 {#00:16:31}

   
**David Ricardo Lopez Flores:** Oh.  
**luis martinez corral:** De frecuencia cardíaca máxima. Está muy bajito.  
**Abimael Guzman Pando:** H okay.  
**luis martinez corral:** Entonces, pero porque dice frecuencia cardíaca al reposo. Esta la pudiéramos estimar para frecuencia cardíaca el caminar. Necesitaría, necesito checar ese script.  
**Abimael Guzman Pando:** Sí, sí, porque también se me hizo raro eso.  
**luis martinez corral:** Sí, porque este debería ser frecuencia cardíaca, ¿cómo se dice? El caminar 131\. Sí, es un valor para frecuencia cardíaca. ¿Cómo se dice el caminar? Y la y la tanaca es frecuencia cardíaca máxima. Ah, okay.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Y pues el último método de imputación para para la frecuencia cardíaca al caminar, ¿cómo se dice? Es la la mediana global. Eh, aquí viene la pérdida. Entonces, aquí viene una mano.  
**David Ricardo Lopez Flores:** Ahí vienen los los valores de imputación por cada, o sea, el las pérdidas por cada modelo  
**luis martinez corral:** Sí. Okay. De la variable de frecuencia calcaminar se perdió el 7.6% de la frecuencia cardíaca en reposo el 4.2% de la que más hubo pérdida fue la variabilidad de la frecuencia cardíaca.  
   
 

### 00:18:13 {#00:18:13}

   
**David Ricardo Lopez Flores:** y la aportación por cada método.  
**luis martinez corral:** Y ajá, aquí viene la tasa de imputación por por variable y método y frecuencia cardíaca al reposo.  
**Abimael Guzman Pando:** 2% fue la que se usó en el cuatro.  
**luis martinez corral:** Tenemos método cuatro. Voy a checar de dónde de dónde salió esa.  
**David Ricardo Lopez Flores:** Hm.  
**luis martinez corral:** Igual de todos estos pues hicimos un análisis de cómo se dice, de auditoría dual, donde no perdemos los datos, sino tengo ahí una tabla donde están los datos observados y los datos imputados. Entonces ahí lo checo de forma de forma manual y también vienen, ¿cómo se dice? Señalados por qué método se se se, ¿cómo se dice? Se se imputa el resultado final y el cual se pasa la base de datos sobre la que trabajamos. Y aquí es lo que les decía ahorita de que se verificó que todos los por decir la la frecuencia cardíaco reposo fuera menor a 100 latidos por minuto y mayor a 40 latidos por minuto. frecuencia cardíaca al caminar que fuera mayor a 60 lativos por minutos y menor a 160 latidos por minuto y la variabilidad de la frecuencia cardíaca que no se bajara de 15 milisegundos ni subiera de 150 milisegundos porque si encontrábamos valores sobre todo por arriba de los 150 debajo de 15 no lo no los vi eh no pues son las normas estándar fisiológicas para para esos valores.  
   
 

### 00:19:58 {#00:19:58}

   
**David Ricardo Lopez Flores:** Esos valores que que es que impusiste los rangos tú los pusiste esos. Ah, bueno, bueno. Entonces, no se te olvide referenciarlo. Eso y es como cuando haces un análisis clínico, ¿no?  
**luis martinez corral:** Sí, no, esa esas son, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Que dice los mínimos y los máximos.  
**luis martinez corral:** Exactamente. Sí, justo eso es.  
**David Ricardo Lopez Flores:** Okay, okay.  
**luis martinez corral:** Sí. O sea, hay guías clínicas de que, ¿cómo se dice? la respaldan estos estos valores.  
**David Ricardo Lopez Flores:** Lo argumentarlo. Crito  
**luis martinez corral:** Okay. Ah, la estrategia jerárquica logró reducir el 14%.8 de de la pérdida de la variabilidad cardíaca a 0% con 90% valores imputados mediante métodos específicos del usuario del M1 al M3, garantizando la consistencia individual. Eh, y luego ya pues aquí la imputación jerárquica sin fuga temporal preserva la integridad de las series temporales para los análisis posteriores y la agregación semanal.  
**Abimael Guzman Pando:** Bueno,  
**luis martinez corral:** Entonces, ya con eso, ¿cómo se dice? Eh, tenemos un un  
   
 

### 00:21:06 {#00:21:06}

   
**David Ricardo Lopez Flores:** A ver, espérame, espérame tantito, espérame tantito, espérame, espérame. La calidad de los datos podría decirse que subió aún la que subió a un ¿Qué?  
**luis martinez corral:** después de lautación. Sí. más bien de de la de las pérdidas que teníamos al principio del del 14.8% este la recuperamos, la bajamos al al 0% por los mecanismos de de imputación, entonces ya no tenemos pérdidas de datos.  
**David Ricardo Lopez Flores:** Entonces, mejoró. ¿Cuánto?  
**luis martinez corral:** Pues el 14 sí porque porque ya ya no hay fuga de datos.  
**David Ricardo Lopez Flores:** Un 14\. 14\. Es una mejoría eso. Okay. Sí. No, sí, adelante.  
**Abimael Guzman Pando:** Pérdida de datos más bien fuga de datos es otra cosa.  
**luis martinez corral:** Okay, aquí pues tod me falta, ¿cómo se dice? Desarrollar los textos de estos de estos, ¿cómo se dice? De estos subtítulos. Pero bueno, ahora vamos con la con las variables, ¿cómo se dice? que le hicimos ingeniería, que fue la del la del superabit calórico. Eh, el superabit calórico que vamos en un principio que que es todo el gasto energético por encima de la tasa metabólica basal, que esta depende en función de del sexo, la edad, el peso y la estatura.  
   
 

### 00:23:05

   
**Abimael Guzman Pando:** Eu  
**luis martinez corral:** Este y y luego pues aquí me da, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Eso veces.  
**luis martinez corral:** El índice de masa corporal por medio de los usuarios y justifica, ¿cómo se dice? ¿Por qué debemos de de hacer, ¿cómo se dice, la la ingeniería de la variable del gasto calórico en activo? Porque, ¿cómo se dice? 500 calorías no representa lo mismo para una persona leviana que para una más pesada.  
**David Ricardo Lopez Flores:** Mhm.  
**Abimael Guzman Pando:** Hm.  
**luis martinez corral:** Okay. Entonces, igual lo los pasos diarios totales no reflejan el nivel de actividad, sino se se ajustan por el tiempo de uso del dispositivo. Un usuario con 10,000 pasos en 20 horas eh encendido eh en todo el día presenta, ¿cómo se dice? Menor densidad de actividad que uno que hizo 10,000 pasos en 10 horas. Entonces eh ahí, ¿cómo se dice? eh pues nos obliga a a crear la la ingeniería de variables que que quedamos, que era la actividad relativa por día. Por eso les decía ahorita que de repente me cómo se dice, me salen pasos atrasados y otros enfrente, pero ya ya iré corrigiendo cómo se dice eso en el el documento de tesis.  
   
 

### 00:24:40 {#00:24:40}

   
**luis martinez corral:** Entonces, aquí tenemos ya otra vez, ¿cómo se dice? la fórmula para calcular la actividad relativa, que es el el número de pasos, ¿cómo se dice? Sobre la hora que hay con datos, eh, por cómo se dice, por su porcentaje, por 1000\. Bueno,  
**Abimael Guzman Pando:** 100 pasos por mí.  
**luis martinez corral:** Okay, aquí viene la ¿cómo se dice? eh el análisis de variabilidad dual que hicimos, ¿cómo se dice? Sobre sobre sobre estas sobre estas variables. Aquí tenemos la la regla decisión. Si después de normalizar, ¿cómo se dice? Eh, esta estos futures o estas características, eh la el comportamiento de la variabilidad temporal, ¿cómo se dice? no se altera, eh, pues confirmamos, ¿cómo se dice? Eh, e el coeficiente variación. Igual si la correlación con los pasos brutos eh que recogemos es es mayor a al 80%, pues valeamos que que la esencia de la variable se se conserva y que y que hacer la ingeniería de características, ¿cómo se dice?, pues es es fructífero. Aquí tenemos por decir con con los pasos eh el el IMC, ¿cómo se dice?  
   
 

### 00:26:41 {#00:26:41}

   
**luis martinez corral:** De de tres usuarios aleatorios, la la media de cada uno, su desviación estándar y y cómo se dice, el coeficiente de variación.  
**David Ricardo Lopez Flores:** Alo.  
**luis martinez corral:** Aquí tenemos, ¿cómo se dice? Eh, todos los todas la todas las, ¿cómo se dice? Las todo el análisis de de variabilidad y correlación se hizo usuario por usuario y luego ya después en eh en conjunto. Entonces, para el usuario uno, por ejemplo, aquí el el coeficiente de variación fue de 45.9%, el usuario 5.8% y el 46.3% 3% de coeficiente de variación, pero tenemos, ¿cómo se dice? Eh, medias de de pasos muy muy distintas. Uno casi le anda pegando a los a los 10,000 pasos, otro apenas superó los 5000 y otro está en el medio de los tres. Entonces, eh, ¿cómo se dice? Pues los valores son totalmente distintos. Entonces aquí la decisión de la actividad relativa reduce la varianza entre el sujeto, atribuye a diferencias en tiempo de uso, coeficiente de variación similar, pero medianas más homogéneas, permitiendo el clúster más justo.  
**David Ricardo Lopez Flores:** Ha.  
   
 

### 00:28:06 {#00:28:06}

   
**luis martinez corral:** Entonces, ya con esto evitamos, ¿cómo se dice? Que que usuarios con menos horas de registro eh tengan, ¿cómo se dice? eh afecten la distribución de frecuencias de de los usuarios que, por decir, tienen más más, ¿cómo se dice?, más horas de registro. Entonces, ya con eso eh evitamos que que, ¿cómo se dice? Que que los datos sean, ¿cómo se dice? Dispares en en dependencia del tiempo de uso del del reloj. Eh, la variable actividad relativa kilopos por hora normaliza exitosamente porción al dispositivo manteniendo la variabilidad natural del comportamiento. Eh, coeficiente de variación interujeto preservado. Mientras homogeniza las medianas intersujeto, esta variable será un input crítico para las funciones de pertenencia difusas capítulas.  
**Abimael Guzman Pando:** Oye, Luis, por ejemplo, ahí estamos homogeneizando los valores de la varianza, ¿no? Que tanto varían entre sujetos, pero eso no.  
**luis martinez corral:** Sí.  
**Abimael Guzman Pando:** Bueno, más bien, hm, o sea, prácticamente estamos haciendo que todos estén dentro del mismo rango cuando antes estaban claramente estaban diferenciables, ¿no? Había uno de 8,000, otro de 5,000.  
   
 

### 00:29:30

   
**Abimael Guzman Pando:** Entonces, ¿no será mejor alimentar variables que tienen mayor varianza para poder hacer la discriminación ya en el clustering?  
**David Ricardo Lopez Flores:** Abajo.  
**Abimael Guzman Pando:** Porque si le quitas la varianza, pues prácticamente estás haciendo que todo sea homogéneo, ¿verdad? Y cuando quieras hacer el clustering, pues no va a haber forma de separar los datos. No sé si me explico.  
**luis martinez corral:** Okay. Sí, entonces.  
**Abimael Guzman Pando:** O sea, no sé si esto que hiciste aquí nos esté afectando a la hora de tratar de hacer el clustering, porque ya todo está homogéneo, ¿verdad?  
**luis martinez corral:** Ajá. Entonces, no no no es que no tengamos usuarios activos, sino que están todos, ¿cómo se dice? Homagionizados.  
**Abimael Guzman Pando:** Ajá. que ya hicimos esto y que como quien dice lo estamos estandarizando previamente para que todos estén más o menos en los mismos rangos y ya cuando queremos generar los los grupos separados, ah, caray, pues ya todo está igual. Entonces, para, o sea, para que lo vayas pensando, porque yo pienso que sí, se me hace que sí está metiendo ruido esto, porque si había una diferencia muy grande de 5000 a 8500 y luego de repente pasamos a una diferencia de punto 6 a5, pues prácticamente nada.  
   
 

### 00:30:53 {#00:30:53}

   
**luis martinez corral:** Okay, entonces lo considero y vuelvo a hacer el análisis ahí de de clustering, ¿cómo se dice? Sin sin esta homogeneización.  
**Abimael Guzman Pando:** Mm. Y no sé si eso aplica para las otras variables que hiciste nuevas, las que derivaste de las originales.  
**luis martinez corral:** Esa esa esta es la la primer variable, la la actividad relativa y la otra pues es el el superabit calórico basal.  
**David Ricardo Lopez Flores:** relativa. Hm.  
**luis martinez corral:** Dice, "¿Por qué ajustar la tasa metólica?" Aquí aquí aquí es donde entran las medidas antiopromáticas de de peso, estatura y demás.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Déjame, vamos viendo ahí la aquí viene la a la a la la ecuación de de Harris Benedict, que es la la que nos da la tasa metabólica basal para hombres y para mujeres.  
**David Ricardo Lopez Flores:** Uno.  
**luis martinez corral:** Si la tasa metabólica varía 20% intersujeto justifica normalización antiopromética heterogénea. Si superabáit calórico del percentil 50 es menor al 20% clasificar como sedentario. Si superait calórico del porcentil 50 está entre el 20 y 50% actividad moderada y si el superáit calórico es mayor al percent 50 es actividad vigorosa.  
   
 

### 00:32:15

   
**David Ricardo Lopez Flores:** Eso, ¿quién lo define? el mismo autor.  
**luis martinez corral:** Este no esto lo estamos, ¿cómo se dice? Haciendo una una clasificación nosotros. Eh, la tasa metabólica basal es es el gasto, ¿cómo se dice?, de Harry Benedict.  
**David Ricardo Lopez Flores:** Sí, esa sí la fórmula, ¿no? la la clasificación  
**luis martinez corral:** Ajá. Pero pero la clasificación esta la hicimos en base a los a los a los a los percentiles. Aquí en un principio sugerido el el factor de actividad física que era 1.1 1.2 este 1.3 eh 1.8 y hasta 2.0 de de la tasa metabólica basal para los cinco niveles. Aquí, aquí, ¿cómo se dice? Nos quedamos con con tres con tres ventanas, sedentario, actividad moderada y vigorosa. De hecho, entonces cuando el el gasto calórico es menor al 20%, pues es una persona sedentaria.  
**David Ricardo Lopez Flores:** M.  
**luis martinez corral:** Este, del 20 al 50% es con una actividad ligera maderada y mayor del 50% actividad vigorosa deportiva. Aquí aquí los resultados por decir aquí tenemos la la tasa metabólica basal de de de cuatro usuarios como ejemplo.  
   
 

### 00:33:54

   
**luis martinez corral:** Eh, por decir la el usuario requiere apenas 1498 kilocalorías. El usuario 3 requiere 1865\. Este, y cómo se dice, los tres pues andan en gastos calóricos muy muy similares. El más bajo es 28% y el más alto es el 34.2%. Eh, entonces pues aquí respecto a la tasa metabólica, eh están ordenados por orden alfabético,  
**David Ricardo Lopez Flores:** Y tú los acomodaste, o sea, porque veo que consiguen desde U1 hasta U10. ¿Tú los acomodaste desde un inicio así o o coincidió?  
**luis martinez corral:** no más para saber cómo se dice, eh, quién era quién.  
**David Ricardo Lopez Flores:** Ah, espérate, es que leí mal yo. Está bien. No sé. Síguele. Me leí mal la columna esa. La última. Pensé que estaban ordenados en los ascendentes, pero no. Síguelo.  
**luis martinez corral:** No, no, no es el el, ¿cómo se dice? El identificador de cada cada usuario.  
**David Ricardo Lopez Flores:** Sí.  
**luis martinez corral:** Entonces aquí pues sí vemos que sí son, ¿cómo se dice?  
   
 

### 00:35:15 {#00:35:15}

   
**luis martinez corral:** Eh, homogéneos. Eh, aquí hay, por ejemplo, en en los pasos eh habría que ver, ¿cómo se dice?  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Meitaría a lo mejor hacer un análisis de de de cómo se dice, de comparar, no sé, con con barras la las dos estas dos variables, ¿no?  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Se que en el de distribución sí los vimos, se comportaban iguales porque sí justificamos que teníamos no más dos grupos. ¿Por qué? Por ejemplo, esta persona trae el 1498 kilocalorías de gasto. Pero, ¿cómo se dice? Esta persona a lo mejor para quemar este 34% de de gasto calórico, necesita quemar las 8,000 kilocalorías. os digo dar los 8000 pesos al día, pero a lo mejor este que es más pesado el usuario 3, eh necesita, ¿cómo se dice?  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** dar 5,000 pasos para para quemar nada más esto. Entonces, eh esto es lo que nos homogeniza más que más que los pasos, porque el esfuerzo no es el mismo por las características antropométicas, pero porque alguien que pesa 80 kg eh, y camina 8,000 pesos, pues su gasto  
   
 

### 00:36:26

   
**Abimael Guzman Pando:** H Mhm.  
**David Ricardo Lopez Flores:** Ev.  
**luis martinez corral:** calórico es bajo. Pero alguien que está más pesado y que camina menos, su gasto calórico está más elevado.  
**David Ricardo Lopez Flores:** M.  
**luis martinez corral:** Entonces, te digo, no no no es tan no pienso yo que el la la la la variable de de actividad relativa homogeneice, sino más bien esta es la que nos homogeneiza al grupo, porque si te fijas aquí si ya no hay mucha mucha variación.  
**Abimael Guzman Pando:** Es que se hace que son las dos, ¿no? Oye, y por ejemplo, si no hacemos el cálculo, ¿no? Pero le pasamos lo que necesita para el cálculo, por ejemplo, en la actividad relativa, que le pasáramos al algoritmo como entrada, los pasos y las horas con datos.  
**luis martinez corral:** Aha.  
**Abimael Guzman Pando:** Este, ahí estamos asociando que cada uno de esos datos, o sea, tiene sus horas y tiene sus pasos, ¿no? Para cada dato tendríamos eso. No estamos diciéndole cuál es la actividad relativa porque ya ahí está se se homogeneecería el comportamiento, pero a lo mejor si le pasamos desde el inicio la entrada, los pasos, pues se encuentra más fácil un camino para diferenciar los dos grupos.  
   
 

### 00:38:04

   
**Abimael Guzman Pando:** Igual lo mismo aquí, que le pasemos lo que es lo que se utiliza para el cálculo, pero no el cálculo final.  
**David Ricardo Lopez Flores:** Ay,  
**Abimael Guzman Pando:** Por ejemplo, el superavit utiliza las calorías activas, ¿no?  
**luis martinez corral:** Okay.  
**Abimael Guzman Pando:** Y la tasa.  
**luis martinez corral:** Ajá.  
**Abimael Guzman Pando:** A pasarle esas dos variables como entrada para cada uno de los datos que estamos sacando.  
**luis martinez corral:** Para, por decir, la tasa metólica, pues sería, ¿cómo se dice? está fija en los Sí. Okay, lo puedo intentar.  
**Abimael Guzman Pando:** Ajá. O sea, dejarla fija para cada usuario, como quien dice, pero que sea un dato de entrada que que sí llega al modelo, a lo mejor así nos permite diferenciarlo mejor. No sé, estoy con la doc.  
**David Ricardo Lopez Flores:** Pues lo que veo es que, o sea, que si tomo esas anotaciones en cuestión a a qué puede mejorar, pero no sé, o sea, Ahora vámonos al punto del él va a escribir ahorita este de lo que estemos discutiendo, pero qué tal si lo que tiene que escribir implica que tenga que hacer más corrias de programas.  
**Abimael Guzman Pando:** A lo mejor no más que lo considere para JCR, ¿no?  
   
 

### 00:39:27 {#00:39:27}

   
**Abimael Guzman Pando:** cuando si lo vamos a publicar.  
**David Ricardo Lopez Flores:** Ándale, ándale. Entonces, sí, Luis, sí, este, eso es a lo que iba, porque ahorita están saliendo así como que muchos detallitos que implican que Luis vuelva a ejecutar.  
**Abimael Guzman Pando:** Hm.  
**David Ricardo Lopez Flores:** Sí. Y pues la verdad de las cosas en en esto de la ciencia pues es nosotros podemos voltear la tortilla muchas veces. Eso ya yo creo que más que nada pues Amal también lo debe y Luis ya lo debe de entender bien que que podemos darle la vuelta la tortilla muchas veces, pero pero pues ya yo creo que en este punto sí hay que considerar que Luis tome esas consideraciones por si por más después que que él ya esté documentando y que pues que vamos a estos pasar un JCR, a lo mejor ya se ahí sí valdría la pena, este hacer esos análisis y correr esos análisis, pero para que Luis ya concrete y avance, pues lo sigue dejando así, porque de hecho todo lo que le has dicho, yo estoy entendiendo o de que has le hemos  
**Abimael Guzman Pando:** Sí, que lo siga dejando así ahora.  
**David Ricardo Lopez Flores:** comentado es que él tendría que volver a correr análisis en en el código. Sí, Luis.  
**luis martinez corral:** Así es.  
**David Ricardo Lopez Flores:** Entonces, yo digo que mejor lo anote todo lo que le hemos estado diciendo y para lo del JCR.  
   
 

### 00:40:45

   
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** Entonces ahí sí tendría que volver a correr los análisis porque pues ahorita se trata de que ya Luis tome lo que sí puede implementar y que no implique correr todos los códigos de todo lo que le estamos diciendo,  
**luis martinez corral:** Okay.  
**Abimael Guzman Pando:** Sí.  
**David Ricardo Lopez Flores:** ¿verdad? Y que lo que implique mover códigos, pues ya lo dejemos como para un JCR. ¿Cómo laes?  
**luis martinez corral:** No, pues de hecho, ¿cómo se dice? Ya ya me paré de de, ¿cómo se dice? De correr ideas, porque ahora que hice todas estas ingenierías de características, eh fue algo que en su momento le le decía más de de que era más más factible por los tipos de datos, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Exacto.  
**luis martinez corral:** Hacer, no sé, un análisis con cadenas de Marcop. que con lógica difusa.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Fue algo que nunca me dejó muy muy, ¿cómo se dice? eh muy convencido, pero pues bueno, vamos aquí en el en el barco con la lógica difusa y y ¿cómo se dice?  
**David Ricardo Lopez Flores:** Sí, sí, sí, sí, no, no, pero pero no a bolear la tortilla y ya no así es.  
   
 

### 00:42:03

   
**luis martinez corral:** Entonces, hm pues hacer los cambios pues se puede, pero sí sí, ¿cómo se dice? Volvemos a a a cómo se dice, a Sí. Entonces, pues sí.  
**David Ricardo Lopez Flores:** No, pero pero fíjate bien, Luis, que todas estas discusiones y todas estas hallazgos que que el doctorel te está comentando ahorita, lo que o lo que yo he estado alcanzando a ver, no hubiera sido posible si no hacemos una radiografía de qué tienes, qué es lo que hemos, qué es lo que te hemos estado diciendo desde un inicio, es que cómo vamos a saber qué sí y qué no si no estamos si no se está analizando  
**Abimael Guzman Pando:** Hm. M.  
**David Ricardo Lopez Flores:** cuáles fueron los resultados. No, ese es el punto de en lo que también debes de poner atención de que no puedes voltear la tortilla de nuevo si no sabes por qué la vas a voltear y pues voltea la tortilla pues la puedes voltear un millón de veces, ¿no? Para mejorar digamos el la idea, ¿no? Entonces, ahorita yo creo que si nos vamos a quedar así en ese sentido de que de que si toma nota a lo que te está comentando y lo que y lo que hemos estado platicando.  
   
 

### 00:43:15 {#00:43:15}

   
**David Ricardo Lopez Flores:** Inclusive tú mismo has has concluido otras ideas que a lo mejor no las tenías en visualizadas y que a lo mejor ya para una publicación a lo mejor ya valdría la pena correr algunas de esas ideas. Okay, adelante.  
**Abimael Guzman Pando:** Hm.  
**David Ricardo Lopez Flores:** Continúa.  
**luis martinez corral:** Okay. Luego pues aquí vemos cómo se dice que el usuario de menor tasa metabólica basal es de 1498 kcalorías y el mayor de 2121, ¿cómo se dice? Kilocalorías. Confirmando nuevamente pues que sí hay heterogeneidad, ¿cómo se dice? Ah, antropra crítica entre usuarios. Eh, y que, ¿cómo se dice? pues la normalización se se hace necesaria por por ¿cómo se dice? para para que los los las variables, ¿cómo se dice? De actigrafía eh eh clasifiquen de manera, ¿cómo se dice? ajusta el ahora sí que el impacto que tiene la la actividad por por cada usuario. Ah, esa es la misma conclusión que acaba de plantear.  
**David Ricardo Lopez Flores:** No, no.  
**luis martinez corral:** Eh, dice, "¿Por qué incluir variables cardiovasculares? La actividad física, pasos, calorías, no captura completamente el sedentarismo desde una perspectiva fisiológica.  
   
 

### 00:44:46 {#00:44:46}

   
**luis martinez corral:** Un un usuario puede tener alto volumen de pasos, pero pobre adaptación cardiovascular, una variabilidad de la frecuencia cardíaca baja, reserva cardíaca limitada, indicando cómo se dice, un deseonamiento físico subyacente. Eh, entonces de ahí es que incorporamos la la frecuencia del delta cardíaco, que es como la respuesta de de cómo se comporta la frecuencia cardíaca. respecto al ejercicio y la variabilidad de la frecuencia cardíaca. Este, eh, entonces, ¿cómo se dice? eh la respuesta del comportamiento del de las variables cardiovasculares al ejercicio, pues nos dan ahora sí que una vista muy muy importante de de de cuál es el estado fisiológico de del usuario. Uno a lo mejor si sale ahorita y camina dos o 3 km puede que llegue hecho pomada porque no tiene condición física cardiovascular y otro que está entrenado no no le sirve ni de calentamiento.  
**David Ricardo Lopez Flores:** Gracias.  
**luis martinez corral:** Entonces, eh para eso no nos sirve monitorizar las las variables cardiovasculares y y que, ¿cómo se dice? Y que si no interpretamos adecuadamente, si no le hacemos las ingenierías de variables, pues van a pasar como como ruido nada más en el modelado de los datos que que tenemos. Entonces, aquí el el delta cardíaco lo calculamos por día. derivado de la frecuencia cardíaca al caminar menos la frecuencia cardíaca en reposo.  
   
 

### 00:46:33 {#00:46:33}

   
**luis martinez corral:** Entonces, si si cómo se dice, si uno tiene 90 lativos por minuto de de frecuencia al caminar y y 60 latidos por minuto en reposo, pues tenemos un un delta cardíaco de 30 latidos por minuto y a lo mejor alguien igual 60 lativos por minuto, frecuencia cardíaca en reposo, pero frecuencia del caminar de de 110, pues ya anda con un delta cardíaco de 50\. Entonces, entre más alto sea el delta cardíaco, eh menos óptimo es el estado de de la función cardiovascular respecto al ejercicio del usuario.  
**David Ricardo Lopez Flores:** Es quiere decir que quiere decir que es usuario no tiene condición o algo así.  
**luis martinez corral:** Eh, exactamente. Ajá. Y luego, ¿cómo capturamos? ¿Cómo se dice? Eh, la ahora sí que esta es la la respuesta. del sistema nervioso derivado, ¿cómo se dice? De de las variables cardiovasculares. Entre mayor variabilidad de la frecuencia cardíaca tengamos, quiere decir que el sistema nervioso está más relajado. Entre más bajo sea la variabilidad de la frecuencia cardíaca, el el ¿cómo se dice? Eh, el usuario tiene más pueden ser muchos los factores que dijimos que afectan la calidad de vida, pero puede ser fatiga, sobreentrenamiento, estrés crónico, este, o enfermedad o algún otro factor psicosocial.  
   
 

### 00:48:11 {#00:48:11}

   
**luis martinez corral:** Pero este nosotros, ¿cómo se dice?, lo vamos a a identificar con con valores más bajos y quedamos que el valor más bajo que admitimos era de 15 y el mayor de 150\.  
**David Ricardo Lopez Flores:** Ahora sí, ahora  
**luis martinez corral:** Aquí tenemos, ¿cómo se dice? Una una matriz de correlación de de Spirman de las variables, ¿cómo se dice? derivadas que son las cardiovasculares y las de actividad relativa contra la actividad relativa. Ah, y pues aquí vemos cómo se dice que que cómo se dice que que el volumen de de actividad relativa este sí, ¿cómo se dice? Sí, captura las los diferentes valores de las variables cardiovasculares. Dice, "E específicamente la variabilidad de la frecuencia cardíaca muestra correlaciones muy bajas menores a a al 20% con variables de actividad, validando que el tono vagal es un domino ortogonal al volumen de movimiento. acepta  
**Abimael Guzman Pando:** ¿Sabes qué hace falta Luis?  
**luis martinez corral:** el conjunto de cuatro variables para clustering y modelado difuso. Esto es lo que entra al a al sistema de difuso a estas cuatro variables.  
**David Ricardo Lopez Flores:** M.  
**luis martinez corral:** Eh, ¿qué?  
**Abimael Guzman Pando:** que graficaras esas cuatro como graficaste las otras con la de violín y todo eso.  
   
 

### 00:50:03

   
**David Ricardo Lopez Flores:** Aquí. Ahí está.  
**luis martinez corral:** Déjame ver. Sí, las dejé haciendo esa tarea antes de empezarla.  
**Abimael Guzman Pando:** Sí, las tienes.  
**luis martinez corral:** Deja ver si las hizo aquí el el script.  
**Abimael Guzman Pando:** Ah, sí, lo dejaste.  
**luis martinez corral:** No más no está compilado, pero ir a cuarto semestre dataset. ¿Me salgo o seguimos?  
**Abimael Guzman Pando:** Mm, que no es que no sé si sea bueno para verlas, o sea, antes de de meternos al sistema que entró  
**luis martinez corral:** Porque de hecho ahí en uno de los No, yo no te dijeron  
**David Ricardo Lopez Flores:** No, no sé. Es que sí, ya.  
**luis martinez corral:** ya valió. Aquí tengo la ruta. Si están a la vista las dejamos. Si no eh no lo seguimos.  
**Abimael Guzman Pando:** Sí, si no le seguimos.  
**luis martinez corral:** Es corto análisis.  
**David Ricardo Lopez Flores:** Bueno, yo ahorita sí quiero que me expliques bien, o sea, otra vez por qué esas cuatro van para el modelo difuso. Porque se correlacionaron, porque no se correlacionaron, lo que quiero.  
**Abimael Guzman Pando:** Oye, ¿cómo le estás haciendo para que la te genere todas esas cosas?  
   
 

### 00:51:29 {#00:51:29}

   
**David Ricardo Lopez Flores:** Pues con la clase que le dijo el profe, el profe es que le da puros.  
**luis martinez corral:** Pagando, pagando Este, estoy usando cursor.  
**Abimael Guzman Pando:** Ay, profesor.  
**luis martinez corral:** Eh, antes usaba chatt, pero eh cursor es como visual visual, ¿cómo se dice? Visual estudio code, pero con una inteligencia artificial integrada.  
**David Ricardo Lopez Flores:** Hm.  
**luis martinez corral:** Entonces, ay, gey, abri.  
**David Ricardo Lopez Flores:** te ayuda te ayuda a desarrollar código ahí mismo sin tener que estar copiando y pegando y te generé el código Mhm.  
**luis martinez corral:** Ah, aquí se los presento. Este es el Aquí, aquí va. ¿Cómo se dice? Le doy el cómo se dice, el la instrucción. Ah, aquí, ¿cómo se dice? me va generando el, ¿cómo se dice? El código. Lo lo ejecuta en consola. Eh, genera la Bueno, dependiendo ahí lo que le vaya pidiendo uno, pero yo le voy pidiendo loss y documentaciones y demás. Eh, verifica lo que hizo y luego ya me da las lo pasadísima de lanza, nada más.  
**Abimael Guzman Pando:** H Órale.  
**luis martinez corral:** La versión de capa gratuita está muy básica, no te alcanza ni para generar un un, ¿cómo se dice?  
   
 

### 00:53:01

   
**luis martinez corral:** Eh eh pues no no no te hace yo creo que ni una página web, pero no sé, se queda.  
**David Ricardo Lopez Flores:** te limita ciertas líneas de código.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** De hecho, con la versión de pago ya he pagado dos dos de estos dos veces 20 dolaritos, pero aquí le voy pidiendo, ¿cómo se dice? todo y no se le pierde nada, nada de contexto. Y luego pues aquí tiene las terminales a un lado nada más ahorita la tengo, ¿cómo se dice? Dormidita. Pero bueno, esto es lo que lo que hizo, ¿cómo se dice? De los grados de de pertenencia. Actividad, ¿cómo se dice? baja, moderada, actividad activa. Eh, estoy tratando de porque también para mí es la primera vez que la veo.  
**Abimael Guzman Pando:** Pero sí gráficas de violín de las variables no no es eso.  
**luis martinez corral:** Deja, deja ver, ¿qué más hay? Estas caso sedentario.  
**Abimael Guzman Pando:** A ver, esas pimeline completo también. Esas son las inferencias.  
**luis martinez corral:** Aquí está las cosas finales del sistema interrotación caso clínico activo real caso baja.  
   
 

### 00:54:18 {#00:54:18}

   
**Abimael Guzman Pando:** Ya no se me hace que no están porque son puras del sistema.  
**luis martinez corral:** Este, aquí pues por aquí en esta tablita yo creo que está más más, ¿cómo se dice? Eh, más de sí, actividad relativa, eh, superáit calórico, variabilidad de la frecuencia cardíaco, delta cardíaco y el este es el score, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Las columnas son las columnas son las entradas. Ahí, por ejemplo, interpreta una regla, dice, si actividad relativa es bajo, superar calórico es bajo y actividades relativas baja y delta es bajo.  
**luis martinez corral:** Y acá el el usuario es sedentario, perfil sedentario clásico.  
**David Ricardo Lopez Flores:** Entonces, y la y la salida es punto 8\. Okay, okay.  
**luis martinez corral:** Punto 8 acedentario. Ajá.  
**David Ricardo Lopez Flores:** Y eso score, o sea, a partir de cuándo decidiste cuándo es cada quien, de dónde salió.  
**luis martinez corral:** Ya nos vamos directo hasta ahí.  
**David Ricardo Lopez Flores:** No, no, no, no. Así déjalo, así déjalo. Bueno, después lo contestas, ¿no? Pero después ahora mejor nos No sé si mi madre quiere ver otra gráfica para No, sí que vamos a estar hasta la 1 de la mañana.  
   
 

### 00:55:43 {#00:55:43}

   
**Abimael Guzman Pando:** Sí, no vamos a regresarnos ya Oh.  
**luis martinez corral:** Sí, por sé porque aquí hay tres tres clas tres casos prácticos por decir si actividad relativa es alta eh superabit cardórico alto y variabilidad de la frecuencia cardíaca alta y delta cardíaco alto no es sedentario.  
**David Ricardo Lopez Flores:** No manches. O sea, qué mal.  
**luis martinez corral:** Aquí un caso, ¿cómo se dice? combinado, actividad relativa baja, superait calórico bajo, variabilidad de la frecuencia alta y y delta cardíaco medio, pues es, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Ajá.  
**luis martinez corral:** sedentario.  
**David Ricardo Lopez Flores:** Sí. Okay, entonces nos volvemos a a la pregunta esa que que te que te decía otra vez.  
**luis martinez corral:** Ah. Ah.  
**David Ricardo Lopez Flores:** Quiero que me expliques, porque estoy medio chonte, por qué esas cuatro variables representaron las entradas al sistema difuso. No.  
**luis martinez corral:** Eh, ¿por qué son las que se las que cómo se dice? De forma ortogonal. No sé cómo de de cómo se dice de famil con con ¿cómo se dice? Con ay es que es un proceso matemático que hay í en el curso de lógica difusa, eh, donde hacemos uno, o sea, hacemos una proyección entre matrices y cada una de estas cuatro variables son las que,  
   
 

### 00:57:07 {#00:57:07}

   
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** ¿cómo se dice? se se adaptan mejor al a los a los, ¿cómo se dice?, a los volúmenes del movimiento de la persona.  
**David Ricardo Lopez Flores:** No tuvo que ver con la matriz de correlación anterior.  
**luis martinez corral:** Sí. Okay.  
**David Ricardo Lopez Flores:** A ver, a ver, tratar de fundamentar en eso.  
**luis martinez corral:** Por decir, pues aquí tenemos, ¿cómo se dice? actividad relativa, todos esto pues es uno, pero la actividad relativa con el con el superabáit calórico tiene un un, ¿cómo se dice? Un 68% de correlación utilizando Spirman.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Variabilidad de la frecuencia cardíaca con actividad relativa. Casi no tiene cómo se relación en correlación, nada más tiene el punto 12\. Eh, la actividad relativa con el delta cardíaca igual tiene una correlación baja de de apenas el 24%.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Entonces aquí la el superabit calórico con la con la variabilidad de la frecuencia cardíaca este tiene muy muy poca correlación, apenas el punto09% y el delta cardíaco tiene una correlación mayor de del 30%. ¿Por qué? Pues delta cardíaco eh sí se deriva, ¿cómo se dice?  
   
 

### 00:58:41 {#00:58:41}

   
**luis martinez corral:** de de la frecuencia cardíaca al caminar, mientras que la variabilidad de la frecuencia cardíaca pues es totalmente eh autónomo a las a las variables de de movimiento. Estas estas dos variables son de movimiento y estas dos variables son cardíacas. Entonces, la variabilidad de la frecuencia cardíaca con el delta cardíaco sí se tiene igual una baja correlación, pero pues ahí existe, ¿cómo se dice? La la los los índices de de relación que hay entre estas eh variables tanto cardíacas como de movimiento. Por un lado, estamos mediendo la actividad relativa, que es, ¿cómo se dice? lo que se mueve la persona en el tiempo que lo observamos, eh el gasto que que esto le genera a la persona de eh por encima de su metabolismo sal y el comportamiento, ¿cómo se dice? Del corazón, de cómo cómo está funcionando a a nivel cardiovascular. Entonces, con estas cuatro variables es como como estamos, ¿cómo se dice? Eh, decidiendo, ¿cómo se dice? seguir para para clasificar sus patrones de de movimiento por una parte y de función cardiovascular por la otra.  
**David Ricardo Lopez Flores:** Lo busco. Sí.  
**Abimael Guzman Pando:** También ahí, acuérdate, Luis, que por ejemplo estás haciendo unas variables derivadas de otras, entonces como son derivadas van a tener una relación ya sea proporcional o inversa.  
   
 

### 01:00:18 {#01:00:18}

   
**Abimael Guzman Pando:** Por eso también eliminaste esas y tendrían redundancia, entonces ya no tiene caso que las  
**luis martinez corral:** Ajá. Sí, exactamente. Sí. Por eso borramos minutos de ejercicio, minutos de movimiento. Eh, pues la Ah, sí, sí.  
**David Ricardo Lopez Flores:** Ah, órale. Ahí ahí puede salir la justificación de porque eso les preguntaba de por qué las eliminaste.  
**luis martinez corral:** Y aquí aquí, ¿cómo se dice? Eh, eh, evitamos la la multicolinead, que es, ¿cómo se dice? pues el estar repitiendo los las características o los futures de las de las matrices.  
**David Ricardo Lopez Flores:** Bueno, a mí todavía me acabó duda eso de por qué esas variables se aceptaron para cluster y modelado de difuso. Entonces, vas a tener que ser más convincente para que quede claro esa sala cuando cuando lo documentes en la en la tesis.  
**luis martinez corral:** Okay, de acuerdo.  
**David Ricardo Lopez Flores:** Sí, porque si eso se documenta en un paper también te lo van a cuestionar, o sea, te van a decir, ¿por qué? ¿Por qué esas cuatro y por qué no otras? Entonces aquí el punto es tú toma nota y todo lo que sea implementable que no implica que desarrolles código, pues trátalo de abordar en la escritura de la tesis, ¿verdad?  
   
 

### 01:01:29 {#01:01:29}

   
**David Ricardo Lopez Flores:** Y lo que sabes que derives, que va a derivar en código, pues no, eso es dejarlo para un para una publicación tipo JCR.  
**luis martinez corral:** Okay, muy bien.  
**David Ricardo Lopez Flores:** Ok.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Este, y luego pues aquí hasta acá se me lanzó lo de la lo de la aguación semanal que les decía de de pues buscar, ¿cómo se dice? Monitorizar 7 días continuos. Aquí era lo que les decía de que nos justificamos por la parte que la OMS te sugiere. como mínimo 150 minutos de actividad física de moderado vigorosa a la semana. Eh, pero aquí a lo mejor este ahorita que me dijiste lo del la homogeneización ahí de las variables, a lo mejor si si una persona hace los 150 minutos en un día y el resto de la semana se  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** tira la lona, ¿cómo se dice? pues cumple con la meta del según la OMS, pero nosotros aquí sí lo sacamos, ¿cómo se dice? Por outer, entonces habría que checarlo porque si yo a lo mejor nada más corro los domingos, pero oye me aviento 100 km en bicicleta y el resto de la semana estoy en la oficina, pues pueda que sea activo  
   
 

### 01:02:35 {#01:02:35}

   
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** un día, pero extremadamente activo y ese compensa la semana.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Entonces, o sea, tiene comportamientos centarios de de lunes en sábado, pero puede que pero no tiene sedentarismo.  
**David Ricardo Lopez Flores:** O sea, si hago bici 4 horas al domingo soy soy no soy sedentario.  
**Abimael Guzman Pando:** No tiene sedentarismo. Ah.  
**David Ricardo Lopez Flores:** Ah, ya. Ok.  
**luis martinez corral:** Y y la OMS nos dice que por cualquier método de ya sea acumulativo, de que todos los días uno camine 6000 pasos, o o haga tres días de ejercicio de forma vigorosa la semana, eh siempre y cuando unoales 150 minutos de actividad física de moderada vigorosa en la semana, ya no ya no eres sedentario.  
**David Ricardo Lopez Flores:** Mhm.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Entonces aquí pues por decir a los a los runers, a los ciclistas o o a los que van al gimnasio dos o tres días por semana, a lo mejor puede que los los, ¿cómo se dice? Los los excluyamos de de esa categoría por por, ¿cómo se dice? Por detectar los layers debido a un día, porque aquí estamos, ¿cómo se dice?  
   
 

### 01:04:00 {#01:04:00}

   
**David Ricardo Lopez Flores:** Mhm.  
**Abimael Guzman Pando:** Aha.  
**luis martinez corral:** buscando la mediana por un patrón habitual de 7 días.  
**Abimael Guzman Pando:** Sí, la mediana pues va a eliminar todo lo que esté los extremos.  
**luis martinez corral:** Sí, voy a voy a voy a checar ese razonamiento antes de de de cómo se dice, de concluir, eh para ver cómo cómo se comporta, pero bueno, ahí está.  
**Abimael Guzman Pando:** M.  
**luis martinez corral:** Pues lo es lo que dijimos, mínimo. Aquí está el criterio de validez que les decía, tenemos que tener al menos 5 días con datos completos.  
**David Ricardo Lopez Flores:** Tres.  
**luis martinez corral:** El resultado, ¿cómo se dice? Tenemos 1337 eh semanas válidas. Tenemos 16 características y cuatro variables que se van al modelo de clustering y lógica difusa.  
**David Ricardo Lopez Flores:** por si  
**luis martinez corral:** Okay, aquí este ahorita les platiqué también que aquí vamos generando los logouts de salida donde guardábamos eh las los las, ¿cómo se dice?  
**David Ricardo Lopez Flores:** está dispo.  
**luis martinez corral:** Las salidas que se registran del reloj antes de imputarlas y después de de imputarlas. Y pues hicimos un análisis de de variabilidad dual, ¿cómo se dice? Entre entre la variabilidad observada de los datos cruos, ¿cómo se dice?  
   
 

### 01:06:08 {#01:06:08}

   
**luis martinez corral:** Sin imputar y con los datos, ¿cómo se dice? Operativos del modelo después de la de la imputación.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Eh, aquí pues la regla de decisiones si el delta si el coeficiente de variación del delta cardíaco es menor al 5% aceptamos la imputación. Si el del si si cómo se dice, si el 5% es mayor o igual al delta al coeficiente de variación del delta cardíaco y o entre ellos dice lo aceptarnos con precaución y si el coeficiente de variación es mayor al mayor o igual al 10% eh revisamos la estrategia de de cómo se dice, de imputación.  
**David Ricardo Lopez Flores:** Eh,  
**luis martinez corral:** Eh, los resultados, pues aquí los tenemos en la en esta tablita.  
**David Ricardo Lopez Flores:** para el  
**luis martinez corral:** El coeficiente de variación observado el 62%. Eh, el operativo, entonces el coeficiente de variación es del 2 menor al 2.%, 5%. Pues yo creo que todos quedaron menos del del 5% que que pusimos en la primera regla de decisión.  
**Abimael Guzman Pando:** del cinco.  
**David Ricardo Lopez Flores:** 5%.  
**Abimael Guzman Pando:** Ok.  
**David Ricardo Lopez Flores:** O sea,  
**luis martinez corral:** Aquí está la variabilidad operativa versus la variabilidad, ¿cómo se dice?  
   
 

### 01:07:42

   
**luis martinez corral:** Eh, observada. Ahí vemos cómo se dice, pues que no supera el 5%. Aquí está también por por usuario. La variable porable.  
**David Ricardo Lopez Flores:** Ay menos  
**luis martinez corral:** A ver, a ver si aquí reforzamos un poquito su duda, Doc, de de por qué, ¿cómo se dice? la agregación semanal van al va van, ¿cómo se dice? Al al clustering. Se espera que el dataset generado de 1337 semanas por las 16 características tenga una completitud del 100% con los rangos fisiológicos posibles y variabilidad suficiente del coeficiente de variación menor al 20% para identificar los patrones. el proceso de generación, partir de los datos diarios imputados, agrupar por usuario y luego después la ventana semanal de lunes a domingo. Luego calcular los percentiles de 50, 10, 90 ah para el rango intercuartílico de cada variable. Aplicar el filtro de de de más de 5 días válidos por semana. Eh, aquí la regla de decisión. Si completamos el 100% de los datos eh mayor a, o sea, si tenemos más de 1000 muestras, aceptamos para el clustering.  
   
 

### 01:09:11

   
**luis martinez corral:** Si las medianas están dentro de los rangos clínicos, aceptamos. Y si el coeficiente variación es menor a 10, eh, revisamos la la variable que que se que discrimina. Entonces, aquí toma. Esta es la base de datos con la que se trabajó para el para el análisis de datos. La mediana global de la actividad relativa está el punto 59%, el super calírico al 29.4, 4, la variabilidad de la frecuencia cardíaca 48, delante cardíaco 36\. Y cómo se dice, y pues con las tres reglas que pusimos de decisión, pues nos dice, ¿cómo se dice? Que que sí se cumplieron y se valían para el para el, ¿cómo se dice? Para el para el algoritmo de camins. Ajá. Laaciónal reduce efectivamente el ruido diario. El análisis dos de variabilidad confirma la amputación. No introduce artefactos severos. El dato semanal con cuatro variables por 50 y cuatro rangos interlicos. está listo para el matriz de correlación con las dice, "Se esperaba que las variables relacionadas con el volumen de actividad física,  
   
 

### 01:10:42 {#01:10:42}

   
**David Ricardo Lopez Flores:** Ah.  
**Abimael Guzman Pando:** H  
**luis martinez corral:** con el volumen de actividad, actividad relativa perceptil 50, superáid calórico por 50 presentaban correlación moderada a fuerte eh con un R mayor al 60%. Eh, mientras que las variables cardiovasculares de variabilidad de la frecuencia cardíaca al parcentil 50 y el delta cardíaco al parcentil 50 mostraban correlaciones más débiles con las primeras, indicando que la captura de los dominios fisiológicos son distintos. Eh, se calculó la matriz de correlación de las cuatro variables 50 semana se calculones de se parece a la matriz que vimos ahorita, ¿verdad?  
**Abimael Guzman Pando:** Es igual se me hace eso.  
**luis martinez corral:** Sí, cambian nada más que las otras era con con las con las con la mediana del porcentil 50, ¿no?  
**Abimael Guzman Pando:** Sí, nada más trae el cambio de Ah, no.  
**luis martinez corral:** O sea, los la otra matriz de correlación que vimos era con datos diarios y este es con datos semanales, pero la correlación no era ante actividad relat reflejan volumen de actividad y las correlaciones bajas entre vales de actividad  
**David Ricardo Lopez Flores:** semanales.  
**Abimael Guzman Pando:** A ver, sí, pues sale igual, es la misma.  
   
 

### 01:12:24

   
**luis martinez corral:** cardiovascular menores a 35 confirma dominios distintos. Sí. Entonces, ¿cómo se dice? Pues ya justificamos. Eh, dice, "Para valuar la teogenidad de lo de patrones de correlación entre participantes se calculaban matrices de correlación de priduales nivel diario de todas las variables dice algunos usuarios exigen correlaciones fuertes entre actividad y variables cardiovasculares. Otras  
**David Ricardo Lopez Flores:** Ok.  
**luis martinez corral:** muestran independencia relativa, ejemplo usuario 1, usuario 5, justificando el enfoque personalizado del sistema difuso. Valitad intersurjeto refuerza lación de usar medanas semanales en lugar de promedios globales. Aquí, ¿cómo se dice? Hay una matriz de dispersión de los datos de aquí tenemos pasos diarios. Así era como lo querías ver ahorita tú, ¿no?  
**Abimael Guzman Pando:** Está por usuario aquí, ¿verdad?  
**luis martinez corral:** Sí, cada usuario es un color.  
**David Ricardo Lopez Flores:** Es un color.  
**luis martinez corral:** Ah.  
**Abimael Guzman Pando:** Sí, sí, sí. Se ve que no no hay forma de separarlos así tan fácil. No más en la de mm la DAS RB. Se ve algo, alguna diferenciación entre esas dos gaucianas, pero es el seis, creo, el que hace una separación de los demás casi en la columna, ¿cómo se llama?  
   
 

### 01:13:52

   
**luis martinez corral:** Usuario nu. Mejor el el dejar quién es el seis.  
**Abimael Guzman Pando:** Fila dos, columna dos también. Ahí estoy viendo esa.  
**luis martinez corral:** Seis.  
**Abimael Guzman Pando:** Los demás sí se ven casi iguales todo. más esa es la que quién sabe si eso le afectó que se homogenizara todo el comportamiento.  
**David Ricardo Lopez Flores:** Ha. Ah.  
**luis martinez corral:** Tengo aquí la relación o se me da que s usuario seis. Ahí está. Ahí se visualizó. No, este güey es el más sedentario de todos.  
**Abimael Guzman Pando:** Entonces, ese es el que está dándote el inventario y el tres también por ahí anda, eh, más que no salió tan alto, como que no.  
**luis martinez corral:** Ese es el más y el que salió más bajo también en el cuestionario el SF 36\.  
**David Ricardo Lopez Flores:** Y el rojo, el rojo es el que salió la campana más a la izquierda. ¿Quién es?  
**Abimael Guzman Pando:** Ajá.  
**David Ricardo Lopez Flores:** El tres, el usuario tres parece,  
**Abimael Guzman Pando:** Sí, el tres.  
**luis martinez corral:** Sí, pues aquí está la dispersión por las variables, pero está está complicado, pero pero sí, pues pero sí, ¿cómo se dice?  
   
 

### 01:15:29 {#01:15:29}

   
**luis martinez corral:** Definitivamente cada cada, ¿cómo se dice? Hm. Cada usuario nos nos dice, ¿cómo se dice? Pues que si hay que buscar la la personalización o más bien la individualización de sus características y no tanto generalizar los modelos, sino de sí de hacer adaptativo.  
**David Ricardo Lopez Flores:** está conectado.  
**luis martinez corral:** Pero con la con, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Dale.  
**luis martinez corral:** La ingeniería variables aquí no tiene si con la del superabáit calórico, pues con esa sí se individualiza el el comportamiento, por decir aquí el el ¿cómo se dice? El usuario dos, yo creo que es el que se da más matriz de dispersión.  
**David Ricardo Lopez Flores:** ¿Qué pegó?  
**luis martinez corral:** Igual para la tesis, yo creo que podemos manejar los e eh este diagrama, ¿cómo se dice? de dispersión y el otro que hicimos con los diagramas de cajas para la defensa de tesis, ¿no? la presentación del el 5 de diciembre, no tenemos que meternos tanto en el eh pues en la parte técnica de código y de y está  
**Abimael Guzman Pando:** Mhm. No, no, sin meterse en código.  
**David Ricardo Lopez Flores:** No, no, de hecho en la defensa de tesis no ni menciones.  
   
 

### 01:17:13

   
**Abimael Guzman Pando:** Ajá.  
**David Ricardo Lopez Flores:** O sea, tú vas y vas a mostrar, qué método usaste y los resultados y cuáles fueron tus contribuciones principales.  
**luis martinez corral:** Sí, sí. y estos estos, ¿cómo se dice?  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Estos gráficos manos.  
**David Ricardo Lopez Flores:** Entonces, hay que hay que poner los que más convenzan, verad.  
**luis martinez corral:** Sí. Y luego, pues, aquí tenemos la matriz de correlación, ¿cómo se dice? Entre las 16 variables. El mapa de calor de correlación de Pon para las cuatro variables manuales P50. Se confirma la correlación entre actividad la T y calórico, mientras que las variables cardiovasculares delta cardíaco muestran correlaciones bajas con es lo mismo que vimos en la tablita.  
**David Ricardo Lopez Flores:** Sí.  
**Abimael Guzman Pando:** Y porque ahí, por ejemplo, aumentaron la otra vez a a ocho, eran cuatro y luego aumentaron a ocho. ¿Por qué usaste los percentiles 50 y Ah, pues eso fue lo que cambió, no más, ¿no? Que usaste el P50. Ah, y el rango intercartel.  
**luis martinez corral:** Intercorpelo.  
   
 

### 01:18:23

   
**David Ricardo Lopez Flores:** M.  
**luis martinez corral:** Ajá.  
**Abimael Guzman Pando:** ¿Por qué usaste esas ahora? ¿Por qué no te quedaste con las cuatro que ya tenía?  
**luis martinez corral:** Es que estoy viendo a ver cuáles, cómo se dice, encajaban más, pero Ajá.  
**Abimael Guzman Pando:** O sea, estas son las que estoy entendiendo ya por lo que dice ahí arribita, que estas son las que le entraron al cluster. ¿Y por qué no dejaste nada más así?  
**luis martinez corral:** Nada más que eh con esta yo creo que queríamos ah con esta discriminamos cuál valor era mejor de cómo se dice para entrar si el percentil 50 o el o el del rango intercartílico.  
**David Ricardo Lopez Flores:** Ui.  
**Abimael Guzman Pando:** Simplemente paso. Ah, no, sí, las cuatro que tenías antes, ¿no? Actividad relativa, HRB, Superavit. Y de hecho pasos diarios no la tenías. Era otra, ¿no? La actividad.  
**luis martinez corral:** No, pues esto no, el delta cardíaco.  
**Abimael Guzman Pando:** Ándale, delta cardíaco. ¿Por qué no dejaste esas cuatro para el cluster?  
   
 

### 01:19:23

   
**luis martinez corral:** Sí, con esto son las que entraron al cluster. Nada más te digo, como te digo, esto se lo di a la al, ¿cómo se dice? A la inteligencia artificial.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Le dije, todos los gráficos que hemos, ¿cómo se dice? Eh, hechos, este, inclúyelos en el documento y y genérales un un, ¿cómo se dice?, un un texto descriptivo abajo de la figura. Digo, pero esto ya lo habíamos pasado desde muy atrás, ¿no?  
**Abimael Guzman Pando:** Ah, entonces eso no le entró al cluster. Okay. Sí.  
**luis martinez corral:** No, por decir aquí está mostrando cómo se dice eh la comparación de dos mapas de calor entre el usuario uno y el usuario dos. Esto lo generó totalmente aleatorio. Usuarios 3 y cu e 5 y se te digo. Pero esa de arriba, ¿cómo se dice? Eh, ya, ¿cómo se dice?  
**Abimael Guzman Pando:** H.  
**luis martinez corral:** Pues son cosas que se quedan atrás porque ya después usamos, ¿cómo se dice?, los los valores de toda la de todos los usuarios y no y no por usuarios.  
   
 

### 01:20:34 {#01:20:34}

   
**luis martinez corral:** Por que de hecho estas matrices son las que hiciste tú, ¿no? Del primer código que hiciste tú.  
**Abimael Guzman Pando:** Sí, porque ahí se vienen las variables originales.  
**luis martinez corral:** Sí. No, yo creo nada más las sacó el, ¿cómo se dice? el repositorio y digo el directorio ahí que tenía indexado y y las copió y pegó y puso la descripción.  
**Abimael Guzman Pando:** les quiso dar ahí con una descripción.  
**luis martinez corral:** Ajá. Okay. Y luego aquí de análisis de multionale Este  
**Abimael Guzman Pando:** Porque creo que ahí abajo vienen otra vez las cuatro. Eso de percentil 50\. Entonces ahí sí ya estamos perdidos.  
**David Ricardo Lopez Flores:** Y es que es que la confusión más arriba dices que vas a usar esas para clustering y para fus y luego ya ahí aparecen otras. Y creo que esa es la confusión principal,  
**Abimael Guzman Pando:** Sí, las cuatro principales eran actividades relativas, superabit calórico, HRB y delta cardíaco, ¿verdad?  
**luis martinez corral:** Aha.  
**Abimael Guzman Pando:** Y los pues ya no ya no fueron.  
**David Ricardo Lopez Flores:** que no.  
**Abimael Guzman Pando:** O sí son, pero más bien con los percentiles. Pero, pero, ¿por qué?  
   
 

### 01:22:39

   
**luis martinez corral:** Aquí dice, "Reducir las ocho dimensiones a los componentes principales para visualizar la estructura de los datos en 2D. Identificar cuáles variables contribuyen más a la variancia. evaluar si los clusteres a describid son visualmente separables. Matriz de carianza, desconeción de valores propios, proyección de son vectores propios e aquí tenemos cuatro principales componentes.  
**Abimael Guzman Pando:** M.  
**luis martinez corral:** Variancia 42.321 32 un lado que otra vez no siguen manejando el P50.  
**Abimael Guzman Pando:** Sí, mira, ahí vuelven a aparecer los rangos intercuartílicos también. De hecho, se están reduciendo. Es, o sea, eso sí es lo que le entró al clustering, esas ocho ocho características. Entonces está medio raro ahí ya.  
**luis martinez corral:** 42.3  
**Abimael Guzman Pando:** Ese  
**luis martinez corral:** ¿Qué te dice aquí este este gráfico Se  
**Abimael Guzman Pando:** me dice que no hay muchos no hay mucha separabilidad entre los datos.  
**David Ricardo Lopez Flores:** que están todos remezclados ahí. que ni con los percentiles te puedes dar puedes dar una separación, ¿no? Pero fíjate, es que todo eso puede ser derivado de la de eso que no sabemos, verad, porque pues hay que evaluar y pues no, ahorita ya no te vas a poner a evaluar, pero es como decía Ismael que a lo mejor puede ser eso de que porque más arriba comentabas sobre que cómo era que decías que las homogeniz.  
   
 

### 01:24:58 {#01:24:58}

   
**Abimael Guzman Pando:** que está homogeneizando el comportamiento.  
**luis martinez corral:** Sí.  
**David Ricardo Lopez Flores:** Ajá. A lo mejor, a lo mejor eso te llevó a que todos quedaran los datos bien juntos.  
**Abimael Guzman Pando:** Da.  
**David Ricardo Lopez Flores:** Así es. Es correcto.  
**Abimael Guzman Pando:** Y luego, si te fijas, Luis, también hay los vectores de dirección, o sea, el superáit calórico, el rango intercuartílico y el P50 están apuntando casi la misma dirección de de la variabilidad.  
**luis martinez corral:** Aha. Aha.  
**Abimael Guzman Pando:** También te podrías quedar nada más con uno, o sea, no sé por qué se hizo eso de dividirlo en ocho características.  
**David Ricardo Lopez Flores:** No están los originales ahí, o sea, Mm.  
**Abimael Guzman Pando:** No, como que se dividieron en cada original se dividió en dos, en el rango intercartílico y el P50 y ahí están.  
**luis martinez corral:** H  
**Abimael Guzman Pando:** Y sí está raro eso porque como son derivadas, o sea, el rango y el P50 son derivadas de una sola variable, entonces por eso se ve que apuntan más o menos en la misma dirección.  
**David Ricardo Lopez Flores:** Acabo de acabo, o sea, 20 minutos  
   
 

### 01:26:17 {#01:26:17}

   
**Abimael Guzman Pando:** Y luego también otra cosa que puede hacer ahí es visualizarlo en 3D. también para que no te quedes con dos componentes. Puedes verlo en tres y a ver si en el tercer componente hay otra se puede ver más fácil la separación, pero pues así como se ve, pues no podemos generar clústers ahí.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** Y el crosser a qué se lo aplicaste a eso que se ve ahí.  
**Abimael Guzman Pando:** Sí. A ver cómo quedó.  
**luis martinez corral:** Ajá.  
**David Ricardo Lopez Flores:** ¿Y qué fue lo que resultó?  
**luis martinez corral:** En dos grupos.  
**David Ricardo Lopez Flores:** A ver cómo quedaron.  
**Abimael Guzman Pando:** A ver, los grupos del clúster. Aquí en mi documento no viene el los grupos en el clúster graficados.  
**David Ricardo Lopez Flores:** No más dice ahí bajo sedentarismo alto en caso cer y caso  
**luis martinez corral:** Aquí en el perfil del clúster activad relativa variable P50. 502 Sentario.  
**Abimael Guzman Pando:** Así que ese sí lo vamos a tener que correr de nuevo.  
**luis martinez corral:** M.  
**David Ricardo Lopez Flores:** Ah, mira, ahí es donde es lo que también me confundo, porque ahí, por ejemplo, ahí otra vez aparecen actividad relativa, superar el carólico, el delta cardíata, lo que lo que te ha estado diciendo el doctor imagen.  
   
 

### 01:28:40 {#01:28:40}

   
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** Ahora otra vez cambiaste ahí a esas a esas cuatro cuanto cuando el análisis anterior era de de los cuartiles de esas, ¿no? Perceptiles.  
**luis martinez corral:** Aquí están otra vez  
**David Ricardo Lopez Flores:** es que viene siendo.  
**Abimael Guzman Pando:** Este era análisis de variables por clúster, ¿no? ¿Cómo están?  
**luis martinez corral:** Sí. relativamente M.  
**David Ricardo Lopez Flores:** Entonces, sí hiciste para esas cuatro variables, pero no están los no están las gráficas ahí.  
**Abimael Guzman Pando:** De hecho, si estuvieran así, pues esa la de Superabit si es diferenciable. Ahí se ve que la media está más alta que el otro clúster y y la varianza ni siquiera llega a alcanzar a la otra casi. Si hay algo de traslape, pero no tanto.  
**David Ricardo Lopez Flores:** en las que en actividad relativa en las que están ahí casi juntas son las otras dos, el delta cardiato y el el HR.  
**Abimael Guzman Pando:** También acá en el actividad relativa.  
**luis martinez corral:** Eh Hm hm.  
**Abimael Guzman Pando:** Ajá. el delta cardíaca y el revés sí son poco diferenciables o discriminantes,  
**David Ricardo Lopez Flores:** Y es que ahí dices, mira, dice ahí dice cluster.  
   
 

### 01:30:08 {#01:30:08}

   
**David Ricardo Lopez Flores:** ¿Qué dice ahí? dice cluster cero, o sea, eso viene del análisis de clúster, esas gráficas estoy tratando de entender.  
**luis martinez corral:** Noá. Sí. Ajá.  
**David Ricardo Lopez Flores:** Entonces si le aplicaste clúster a esas cuatro variables, o sea, entonces hay que retirar lo otro, ¿no?  
**Abimael Guzman Pando:** Es que no sé si el clúster se aplicó con las ocho variables y luego después ya teniendo los grupos se vio los perfiles de los grupos con las variables originales o si los clústers se generaron con las variables originales. Esa es la duda.  
**David Ricardo Lopez Flores:** Con las 4\. Con las cuatro.  
**Abimael Guzman Pando:** Ajá.  
**David Ricardo Lopez Flores:** Pues yo entiendo, o sea, yo entiendo que así se hizo.  
**Abimael Guzman Pando:** las cuatro.  
**David Ricardo Lopez Flores:** Por eso le por eso le cuestioné más arriba que decía, "¿Por qué decidiste que esas cuatro van para Clútering y para fusi?" Sí, se acuerdan que le pregunté eso, ¿eh?  
**Abimael Guzman Pando:** Mm.  
**David Ricardo Lopez Flores:** Y dije, "Ah, pues esas son las que él va a usar para clustering." Y eso fue lo que yo entendí.  
**luis martinez corral:** Sí, estos son las que entraron al clustering.  
   
 

### 01:31:09

   
**luis martinez corral:** Aquí está. ¿Cómo?  
**Abimael Guzman Pando:** Entonces, si esas entraron, ¿por qué mostrar el PCA con las otras ocho, verdad?  
**David Ricardo Lopez Flores:** Es a lo que voy. O sea, pues más bien es más bien es que yo entendí que de ahí, o sea, de donde le pregunté yo eso de por qué esas cuatro es brincar ahí.  
**luis martinez corral:** Entonces, más bien el que está, ¿cómo se dice? Róneo es el el PCA, No.  
**Abimael Guzman Pando:** No sé si hay que chicar eso, Luis, porque si eso sí está. Ajá.  
**David Ricardo Lopez Flores:** Así entiendo yo, o sea, que la tesis no vayas a poner, por ejemplo, el análisis de los perceptiles de esas cuatro en clustering, porque pues está viendo que no hay una separación y donde sí se está viendo una separación es en al menos en estas cuatro, en dos de ellas bien marcadas.  
**Abimael Guzman Pando:** Aquí sí se ve, pero eso se debería haber reflejado también en el diagrama del PCA, o sea, con estas cuatro hace el PCA y deberíamos de ver alguna separación.  
**David Ricardo Lopez Flores:** Sí. O sea, que no lo que no se haga con los que no se hubiera hecho con los que los perceptiles de esas cuatro, ¿no?  
   
 

### 01:32:10

   
**luis martinez corral:** Entonces,  
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** Pero eso eso que le llevaría mucho tiempo a eso.  
**luis martinez corral:** más bien cómo se dice checar el script de de PCO y volver a aplicar Ajá.  
**Abimael Guzman Pando:** A ver si le entr lo que tenía que entrarle. Okay.  
**David Ricardo Lopez Flores:** Pero si tuviste que haber hecho clustering para ver por estas gráficas, ¿no?, que están ahí.  
**luis martinez corral:** Sí, o sea, el clustering sí está, pero el de el de PSA era más bien confirmatorio, No,  
**Abimael Guzman Pando:** Sí, el de PSA no más es para visualizar. Como tenemos cuatro características, no las podemos ver así en pues en tres dimensiones, pues no podríamos. Y el PCA lo que hace es reducir las dimensionalidad para poderlas ver, para poder visualizar los clusters.  
**luis martinez corral:** sí, porque, o sea, el clustering y el fusí están con estas cuatro nada más.  
**David Ricardo Lopez Flores:** Bueno, ahora entonces sí, pero entonces ojo, entonces loot otro no iría en tu tesis, o sea, sí iría el PSA, pero para estas cuatro variables, o sea, te toma, no te en eso, o sea, no  
**luis martinez corral:** No, el PSA.  
**Abimael Guzman Pando:** Ajá.  
   
 

### 01:33:28 {#01:33:28}

   
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** es a meter en la tesis porque, o sea, ve la confusión que que que nos generó a nosotros. Ah, sí, allá dijiste bien claro que ibas a usar esas cuatro y de repente usaste otras derivadas de esas cuatro, entonces pues ya ah caray, ya nos perdimos ahí. O sea, lo lógico era seguir con esas cuatro, pero pues seguramente a lo mejor algo se te está escapando y a lo mejor ahorita se fue de foco.  
**Abimael Guzman Pando:** H  
**luis martinez corral:** Mhm.  
**David Ricardo Lopez Flores:** Entonces yo digo que sí, mejor ya este continúa a partir de ahí. ¿Qué fue lo que que para qué te sirvió eso?  
**luis martinez corral:** De aquí pues nos nos sirvió para crear dos dos categorías que dijimos que vamos a modificar el el término lingüístico como sedentario y y activo nada más. Este, ¿no?  
**David Ricardo Lopez Flores:** A ver, ¿cómo? Como sedentario y sedentario activo.  
**luis martinez corral:** Eh, el que dice alto sedentarismo lo dejamos así nada más como sedentario y y el que dice bajo sedentarismo lo dejamos como activo.  
**David Ricardo Lopez Flores:** Ajá. Okay. Activo. Activo sedentario.  
**luis martinez corral:** Este no es que estos tienen el 41% del superabáit calórico, o sea, no son tan sedentarios.  
   
 

### 01:34:45 {#01:34:45}

   
**David Ricardo Lopez Flores:** Ah, okay. Son activos y los y el de abajo va a quedar como sedentario.  
**luis martinez corral:** son activos como sedentario.  
**David Ricardo Lopez Flores:** Okay. Ah.  
**luis martinez corral:** Camin se identifica dos perfiles de comportamiento claramente distintos de actividad y gasto calórico. Eh, la verdad operativa la la, ¿cómo se dice? Amos con mand. ¿Cómo se pronuncia este?  
**Abimael Guzman Pando:** with you.  
**luis martinez corral:** Ajá. Yo lo había leído al revés. En la clase de estadística lo utilizamos, ¿cómo se dice? Mand de Youne, la eh Sí, sí, estuvimos viendo ahí varios estadísticos, los ANO, ustedes studen y todos esos.  
**Abimael Guzman Pando:** Si lo ven es.  
**luis martinez corral:** Este, aquí dice la la variabilidad de la frecuencia cardíaca no discrimina clústers inevariadamente planteando la pregunta es prescindible en el modelo difuso.  
**David Ricardo Lopez Flores:** Ah, mira, ahí está. Pues ahí está. Mira, fue lo que vimos en las gráficas, ¿no?  
**luis martinez corral:** Ajá.  
**David Ricardo Lopez Flores:** Que que que el HRB no se veía muy no se veían muy diferenciables.  
   
 

### 01:35:54 {#01:35:54}

   
**luis martinez corral:** Pero sí, sí que que que no se para.  
**David Ricardo Lopez Flores:** Ajá.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Es, pero ahí hay una hay unaita que cuando eliminamos la la variable de las reglas ya no ya no clasifica adecuadamente. Eh, sistema de inferencia difuso mandami objetivo del sistema de construir un modelo interpretable que clasifique el nivel del centarismo semanal utilizando conocimiento experto, reglas fisiológicas en lugar de aprendizaje supervisado. La salida del sistema será liado contra la verdad operativa de de clustering. Hm. El componente cuatro entradas cuatro variables continuas normalizadas de 0 a uno. La fusificación funciones de pertenencias triangulares, tres por variable bases de regla cinco bases de reglas y entonces basadas en el conocimiento clínico. La inferencia es el método mandami utilizando eh el como agregación. Las especificaciones por el método del centroide y la salida es un score que tiene de 0 a un eh y con una finalización de umbral.  
**David Ricardo Lopez Flores:** Pausa, pausa, pausa. Entonces, podemos decir que todo lo anterior que hiciste y que fuiste y fuiste conduciendo era para determinar que esas cuatro variables en el paso uno son las que dijiste.  
**luis martinez corral:** Ajá.  
   
 

### 01:37:19 {#01:37:19}

   
**David Ricardo Lopez Flores:** Okay, continúa. Eso no se te olvide de reforzarlo cuando lo escribas porque si no va a parecer que Fusi está totalmente aislado de todo lo que hiciste con la anterioridad. Ok.  
**luis martinez corral:** Okay. Si el sistema difuso logra un un F1 score de de punto 70 versus el la verdad operativa, aceptamos el el modelo como como válido. Si el si el recall es eh mayor al 90% priorizamos la sensibilidad. Este si la precisión es menor al 60, pero el recable es mayor a 95, aceptamos los los falsos positivos eh tolerables, ¿cómo se dice? En el contexto de salud pública. Entonces, pues aquí tenemos nuestras reglas de decisión para ver cómo se comporta el el modelo. Aquí tenemos las entradas. X1 lo voy a hacer, ¿cómo se dice? El conjunto difuso de aquí está otra vez el P50.  
**David Ricardo Lopez Flores:** Híjole, ahí está el pers el que la canción. Sí, sí, tienes que arreglar eso, ¿eh? Y otra vez están los percentiles en lugar de los si tienes que Mm.  
**Abimael Guzman Pando:** Sí, sabe qué es lo que entró ahí.  
   
 

### 01:38:39

   
**luis martinez corral:** Pues vámonos a descansar y y corrijo esto. ¿Cómo ven? Y y esto retomamos la próxima semana o cómo o quieren que le le siga para ver qué más contiene.  
**David Ricardo Lopez Flores:** No, yo digo que continúes, o sea, para que te lleves todo lo que, o sea, lo que para que te lleves una línea de trabajo desde aquí que hay que hacer y qué sí es posible y qué no  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** es posible hacer.  
**Abimael Guzman Pando:** Si vas a moverle eso, pues ya también muévele a lo de que te dije del la fuga de datos Ahí la normalización de arriba.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** O sea, tú crees que sí puedes, o sea, porque tú crees que sí puedes hacerlo en esta semana.  
**luis martinez corral:** Esta semana dejé de ver muchos pacientes y me desvelé bastantito.  
**David Ricardo Lopez Flores:** Por eso te por es que ese es el punto, o sea, que cuándo debería tener cuándo deberías tener la tesis  
**luis martinez corral:** Este, o sea, sí, sí me quitó bastante tiempecito, pero igual ya encaminaba a lo mejor, ¿cómo se dice? Ya avanza más rápido.  
**David Ricardo Lopez Flores:** terminada escrita.  
**luis martinez corral:** Hó un perro allá el lunes.  
   
 

### 01:39:53

   
**David Ricardo Lopez Flores:** No manches. Pues, ¿cómo lo hacemos ahí a Porque, por ejemplo, otra vez ahí ya volvió a cambiar los percentiles, ya volviste a cambiar los percentiles? Ya no sé qué onda yo. O sea, primero dijiste que acá arriba, mira, vamos, vamos, vamos a confiar en que simplemente fue error de dedo y tú síguele.  
**luis martinez corral:** Voy a darle una una checada a cómo se dice a a Sí. O sea, vamos como a lo mejor como se dice nada más fue ahí algún documento que se quedó con este y así lo redactó el la  
**David Ricardo Lopez Flores:** Sí, sí, sí, exacto.  
**luis martinez corral:** inteligencia artificial.  
**David Ricardo Lopez Flores:** Eso es lo que voy. Por eso digo, mejor continúa eso, eso se le llama corrigiendo errores, loce.  
**luis martinez corral:** Entonces, bueno, pero sí, entonces aquí tenemos pues los cuatro conjuntos. Actividad relativa, superait calórico, variable de la frecuencia cardíaco delta cardíaco. Eh, todos están sobre todos pertenecen, ¿cómo se dice? Eh, a un score continuo sobre la sobre la recta de 0 a un donde los valores, ¿cómo se dice? que entre más cercas al uno indican un alto sedentarismo.  
   
 

### 01:41:06

   
**luis martinez corral:** Ah, interpretamente comprensibles. bajo medio alto procede la literatura el sistema de difuso mano funciones de pertenencias tres por variable cinco reglas clínica  
**David Ricardo Lopez Flores:** A ver, espérate, espérate. Dale poquito para arriba. Porque, ¿por qué pusiste esos dos? El ¿Por qué no? O sea, será necesario mencionarlo.  
**luis martinez corral:** pues no porque ya desde aquí no cómo se dice nos fuimos Ah.  
**David Ricardo Lopez Flores:** A ver, no quita eso porque vas a si no vas a tener por qué argumentar por qué no su gen y por qué no su camoto. Quitar lo mejor eso al caos.  
**luis martinez corral:** ¿Por qué funciones?  
**David Ricardo Lopez Flores:** Eso no creo que sea una variante para empezar. Yo no creo que haya un trabajo que aborde el mismo enfoque y concluya con un fusi. Entonces, ya desde ahí sería algo, digamos, que no tengas por qué preocuparte.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Dice, ¿por qué funciones triangulares basadas en percentiles? Las funciones de pertenencia deben capturar la distribución real de los datos. No asumir normalidad y permitir interpretabilidad clínica. Para usar percentiles del dataset, garantiza que las etiquetas baja, media, alta reflejen cuartiles reales de la población, nombrales arbitrarios.  
   
 

### 01:42:29

   
**luis martinez corral:** Hipótesis. Las las member functions basadas en percentiles y pimenta serán más robustas que las member functionéas opcionas con parámetros físicos, especialmente en datos no normales con un coeficiente de relación mayor a 50%. Ah, aquí viene. ¿Por qué utiliza el P50? No, aquí, ¿cómo se dice? de define la parametrización como para baja cuando entra en el percendil 10\. Eh, aquí el valor es cer, aquí es uno y aquí vuelve a a cero, ¿verdad? O sea, haría esto. Percentil 10, percentil 25, percentil 40 percentil medio, percentil 35, percentil 50, percentil 65\.  
**Abimael Guzman Pando:** Y ahí sí tiene lógica eso.  
**luis martinez corral:** Alta percentil 60\. Percentil 90\. Más bien utilizamos los percentiles para para definir la las funciones de membresía,  
**David Ricardo Lopez Flores:** Es que sí, es que yo Yo digo que por algo lo hiciste, pero a lo mejor ahorita se te escapó para definir las funciones de membresía. Es lo que estoy entendiendo, pero lo que entran no son los percentiles, son los Ah, Ok.  
   
 

### 01:43:55 {#01:43:55}

   
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** ¿no? Entonces, el conjunto es como se dice la o sea, todo el conjunto de de la variable pues son de, ¿cómo se dice? o pues todo lo que ocupa eh por decir en en el la variabilidad de la frecuencia cardíaca de de 15 a 150 es de de 0 a un, pero por bueno, aquí voy a a poner 15\.  
**David Ricardo Lopez Flores:** Sí, o sea, pero mi duda es no entran los percentiles, entran los valores de las cuatro variables que definiste. van a entrar al fusi.  
**luis martinez corral:** Ajá. Entonces, por decir, bueno, no, no, no, no.  
**David Ricardo Lopez Flores:** No entran los percentiles, ¿eh?  
**luis martinez corral:** Más bien los percentiles definen, ¿cómo se dice? los los parámetros para para las funciones.  
**Abimael Guzman Pando:** las funciones difusas.  
**David Ricardo Lopez Flores:** Ah, bueno, entonces no es que esté mal lo que pusiste ahí arriba, más bien es que más bien es que encuéntrale pies y cabeza a eso que quede bien claro en la tesis.  
**luis martinez corral:** Entonces, por decir, sí, porque por decir aquí voy a usar el bueno el Entonces, supongamos que esta es aquí 15 de HRV H RB.  
   
 

### 01:45:27

   
**luis martinez corral:** Y acá es 150\. Entonces el percentil 10 es este.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Aquí es el percentil 25, pero en sí toda la variable puede oscilar desde 15, que vendría a ser hasta 150, que sería vendría Ajá.  
**David Ricardo Lopez Flores:** Mhm. Sí. Y así va a entrar en la variable, va a entrar con esos valores.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Entonces, las las ¿cómo se dice?  
**David Ricardo Lopez Flores:** Okay.  
**luis martinez corral:** La parametrización la hacemos en base a los percentiles, pero en sí toda la variable queda como variabilidad la frecuencia cardíaco, delta cardíaco, eh perfil de actividad.  
**David Ricardo Lopez Flores:** Ah, entonces eso es lo que tienes que aclarar nada más en el escrito. O sea, no es que estaba mal lo anterior, es que tienes que aclarar para que no cree esa confusión que que nos que nos creó a nosotros ahorita. Okay, adelante.  
**luis martinez corral:** Sí, sí. Pero entonces entonces aquí ya pues, ¿cómo se dice?  
**David Ricardo Lopez Flores:** No.  
**luis martinez corral:** Entonces tenemos la la, ¿cómo se dice? La la parametrización de las de los conjuntos difusos donde va por por los percepctiles y y están en en tres en tres funciones, ¿cómo se dice?  
   
 

### 01:46:37

   
**luis martinez corral:** Baja, media, alta para cada una de las cuatro variables. Cada cada cada variable tiene sus sus, ¿cómo se dice? sus parámetros definidos en estos en estos tres bajo, medio alto.  
**David Ricardo Lopez Flores:** Mhm.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Entonces, la la las reglas de decisión si la entre etiquetas es mayor al 10% rechazar la transición es demasiado abrupta, no difusa. Si el overlap es mayor al 30% rechazar amigad excesiva, perde discriminación si percentiles extremos pedidantas captura el 80% de los datos aceptar cobertura. Aquí tenemos las las funciones triangulares donde A, B, C son los parámetros del triángulo izquierda, pico derecha. Okay. Ah, okay. Aquí está de nuevo actividad relativa, superabit calórico. Aquí no, aquí no nos dice cómo se dice lo del lo del percentil, pero nos da las etiquetas baja, media, alta, el delta cardíaco y y nos da, ¿cómo se dice? Su su valor difuso por cada por cada nivel. Entonces, aquí tenemos laama tres.  
**David Ricardo Lopez Flores:** Si tienes que sí tienes que aclarar bien eso, eh, porque ahí otra vez pusiste las variables y no en percentiles y volviste a dar este coordenadas de las funciones de membresía.  
   
 

### 01:47:58

   
**luis martinez corral:** Entonces, nada más hay que hay que documentar bien esta parte, pero son cuatro variables las que aquí, aquí está.  
**David Ricardo Lopez Flores:** Ajá. Sí, que no. Ajá. Que no vaya a confundir eso de que Bueno, entonces, ¿qué tomaste? Percentiles o esto si tomaste percentiles, ¿para qué los usaste bien? Eso nada más.  
**luis martinez corral:** Aquí se dice actividad relativa. Aquí no dice con el P50.  
**David Ricardo Lopez Flores:** Mm.  
**luis martinez corral:** Este, y aquí están dibujadas las funciones de membresía.  
**David Ricardo Lopez Flores:** las funciones de membresía que se supone que están en función a los perceptes. lo que estamos entendiendo.  
**luis martinez corral:** Ajá.  
**David Ricardo Lopez Flores:** Mm.  
**Abimael Guzman Pando:** Y esa, ¿por qué se ve tan fea, Luis? La primerita, tan comprimida.  
**David Ricardo Lopez Flores:** por yo creo que por el universo de discurso, o sea, por lo que puede variar S.  
**luis martinez corral:** Se agarró el universo. Discurso.  
**Abimael Guzman Pando:** O sea, el percentil, a ver, que primero se usa el percentil. Ah, es que no lo tengo aquí en el documento.  
   
 

### 01:48:52

   
**Abimael Guzman Pando:** Ah, el percentil 10\. Entonces, a lo mejor hubo un valor del percentil cero muy muy abajo y otro muy arriba en el percentil 100 y esa no sería conveniente mejor en lugar de usar triangulares o a lo mejor  
**luis martinez corral:** Sí, sí. Y yo pues de hecho esta es la que más nos ha dado a lo largo de todo el a una abierta.  
**Abimael Guzman Pando:** una triangular en el centro y trapezoidalla así para que agarre todos los valores. Ya. Ajá. O sea, que que corte hasta donde donde empieza y otra que corte hasta donde termina.  
**David Ricardo Lopez Flores:** solo dos funciones.  
**luis martinez corral:** Ah, pues ahí ahí. ¿Cómo se dice? Ahí hago el el ajuste al ca. Eso sí no es no es mucho.  
**Abimael Guzman Pando:** Así como trapezoidales, no sé si Ajá.  
**luis martinez corral:** Sí. O sea, que queda abierta a la izquierda y abierta a la derecha.  
**David Ricardo Lopez Flores:** Sí, para que no se vean la discontinuidad en los en los extremos.  
**luis martinez corral:** Y Aquí.  
**David Ricardo Lopez Flores:** Pero bueno, pero eso le va a afectar en la en la aportación. Eh, porque no sí déjalo mueva ya.  
   
 

### 01:49:51

   
**Abimael Guzman Pando:** Bueno, ya queremos que no que no haga cambio. Ya. Así.  
**David Ricardo Lopez Flores:** Ni modos. O sea, es que sí es que te digo es que no estos son todo lo que te estamos cuestionando, multiplícalo por 1000\. La revisión por panel,  
**Abimael Guzman Pando:** Bueno, es que para la tesis ya no, Luis, porque ya la tesis la tenemos encima, pero sí pensar todo esto que te estamos diciendo para los JCR, porque ese sí lo revisan por pares así y es Mhm.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** no sé.  
**luis martinez corral:** Así. Entonces ahí ahí ahí ahí corrijo este este grafiquito para que sea igual que los demás, eh, pero aquí pues vemos que el modelo funciona. Una de las principales cosas es que, ¿cómo se dice? Que no hay grupos donde donde, ¿cómo se dice? O sea, utilizar los percentiles no nos no se sobreponen una sobre otra porque me tocó al principio probar con unos modelos que por decir, ¿cómo se dice?  
**Abimael Guzman Pando:** M.  
**luis martinez corral:** pues un valor un valor podía entrar en una u otra perfectamente.  
**David Ricardo Lopez Flores:** Todas están sobre Todas están sobre, pero ojo, el usar los perceptives para el diseño de las funciones de membresía.  
   
 

### 01:51:01

   
**luis martinez corral:** Entonces ahorita pues el utilizar los percentiles pues nos da el la posibilidad de de sí, ¿cómo se dice?  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Categorizm.  
**David Ricardo Lopez Flores:** Ok.  
**luis martinez corral:** Okay. Entonces va a ser aquí una por qué cinco reglas y no más. Las reglas difusas deben ser paraosas, interpretables por clínicos, precompletas, cubrir casos relevantes más de reglas quean sobrecarga cognitiva. Menos de tres omiten casos clínicos importantes. cinco reglas basados de conocimiento experto combinado actividad física y biomercadores capturan los patrones clar de centarino versus actividad lograr un score mayor a 70 versus la verdad operativa.  
**David Ricardo Lopez Flores:** Oye, ahí es donde tienes que conectar y introducir pues que todo lo que está atrás, o sea, porque ahí se ve aislado de lo que está atrás todo es, o sea, dale para arriba donde estabas diciendo el porqué de las cinco reglas. Eso ahí también debes de conectar con todo lo que está atrás, Luis, porque si así como está suena de que se está aislado con todo lo demás, o sea, de o sea, debes de mencionar frases que involucren el  
**luis martinez corral:** Aha. Okay.  
**David Ricardo Lopez Flores:** por qué llegaste hasta la conclusión incluso a las esas cinco variables, ¿no?  
   
 

### 01:52:24

   
**David Ricardo Lopez Flores:** No, cuatro, no.  
**luis martinez corral:** Cuatro variables.  
**David Ricardo Lopez Flores:** cuatro.  
**luis martinez corral:** Son cinco reglas.  
**David Ricardo Lopez Flores:** Sí, o sea, Ajá. Porque las variables que se eligieron con la metodología de no sé qué y la experiencia combinada con el experto. No sé si me da entender el punto, porque si lo presentas así se ve como que a lado de todo lo que está atrás.  
**luis martinez corral:** Sí. Okay, de acuerdo.  
**David Ricardo Lopez Flores:** Okay, adelante.  
**luis martinez corral:** Entonces, método de construcción de reglas, inspección de centroides, clústers, identificar variables, discrimin más, conocimiento clínico, análisis de correlaciones, evitar redundancia entre los antecedentes. Mm, aquí vienen las cinco reglas. Las desmenuzamos de una por una o así las observamos n más.  
**David Ricardo Lopez Flores:** Pues yo creo que aquí vamos a tener que confiar en ti. Porque pues tú eres el experto ahí, o sea, ¿cómo vamos a decirte que estás mal ahí en lo que tú sabes?  
**luis martinez corral:** Okay, entonces, okay, si actividad relativa es baja y superabit calórico es bajo, eh, entonces el sedentarismo es alto, si actividad relativa es baja.  
**David Ricardo Lopez Flores:** O sea, mm.  
**luis martinez corral:** ¿Qué qué es lo que vimos ahorita?  
   
 

### 01:53:39 {#01:53:39}

   
**luis martinez corral:** De hecho, al final le pedí, ¿cómo se dice? Quisiera, ¿cómo se dice?  
**Abimael Guzman Pando:** Hm.  
**luis martinez corral:** Unas cosas más visuales. Ahí están las últimas cinco paginitas. Aquí aquí está igual la matriz de de antecedentes.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Eh, luego tenemos los los consecuentes. Aquí tenemos la cobertura clánica. ¿Cómo se dice? Que hay casos muy extremos y también casos intermedios. Eh, las cinco reglas sonizables y habitables por espectos clínicos. O sea, acá cualquier, ¿cómo se dice? eh conjunto de semanal que que agarremos y lo haga eh y lo pasemos, ¿cómo se dice? Por por el modelo, pues nos nos va a dar, ¿cómo se dice?  
**David Ricardo Lopez Flores:** por el modelo.  
**luis martinez corral:** una una interpretación, una salida ajustada a lo que estamos diciendo aquí en estas en este proceso de inferencia difusa.  
**David Ricardo Lopez Flores:** Mm.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Este, aquí usted es el bueno, doc, yo me trabo con las mates, pero aquí están los lo los pasos del del modelo.  
**David Ricardo Lopez Flores:** Mhm.  
   
 

### 01:54:54 {#01:54:54}

   
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** La conclusión, el sistema difuso mandami con cuatro entradas, cinco correr reglas clínicas y salida continua de 0 a un funciones de pertenencias basadas en percentiles empíricos. Data más experto. Reglas justificadas fisiológicamente integradas con actividad y salud cardiovascular. El umbral óptimo es de T30 determinada por la clasificación minaria y el sistema está listo para una validación contra la verdad operativa.  
**David Ricardo Lopez Flores:** Oye, Luis, ese modelo como está escrito, ¿te lo escribió la IA?  
**luis martinez corral:** Eh, sí. ¿Cómo se dice? Estoy usando una idea desde pues todo el semestre. He tenido un chat abierto donde le paso puros artículos de de ¿cómo se dice?  
**David Ricardo Lopez Flores:** Es que eso es a lo que eso es a lo que iba.  
**luis martinez corral:** de de Fusy.  
**David Ricardo Lopez Flores:** Lo has visto documentado en Fusia. Así el modelo.  
**luis martinez corral:** Sí, de hecho aquí en en chat GPT esto ahora ni lo tenía abierto todo el yo voy a cargar, yo creo que a lo largo de todo el de todo el ¿cómo se dice? Toda la maestría ha tenido este chat abierto por este talento en cargarse.  
   
 

### 01:56:16

   
**luis martinez corral:** Está bien pesadote.  
**David Ricardo Lopez Flores:** Sí, pasé.  
**luis martinez corral:** Pero artículo artículo, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Se se pone más lento.  
**luis martinez corral:** Que que cargaba artículo que le que le pasaba y dame todas las todas las matrices, ¿eh? Hazme todo el acá está la por decir aquí desarrollo un sistema. domótico con controlador y lo anális y lo le, ¿cómo se dice? Eres un experto analista de data driver, explícame qué hicieron. Este, desmenuza el pipeline, ¿cómo se dice? De de de su modelo de lógica difusa. Explícamelo. Propónme modelos prácticos. ¿Cómo se dice?  
**David Ricardo Lopez Flores:** He.  
**luis martinez corral:** Entrégame las las matrices. Y luego aquí semorfismo, teoría de conjunt. Ah, esa es otra que estuve siempre buscando con el cuando agarro un artículo que me explica el isomorfismo desde teoría de conjuntos, este, lógica proporcional, este, la la, ¿cómo se dice? la parte computacional y la parte matemática, por decir, aquí es este artículo era de de cómo se dice, para un ventilador que decía, si la temperatura va de los los 40 gr, este va a ser así, si la  
   
 

### 01:57:22 {#01:57:22}

   
**David Ricardo Lopez Flores:** No. ¿Dónde?  
**Abimael Guzman Pando:** H  
**luis martinez corral:** humedad está del 0 al 100% el ventilador debe ir a tantos de estos enfactora esto y lo las etiquetas muy frío, frío, templado, caliente, caliente, muy caliente. Y ahí, ¿cómo se dice? Pues e ellos ellos, ¿cómo se dice? Bueno, aquí es aquí es un ejemplo de cómo se ve e en teoría de conjuntos en lógica ah proposicional, este en código.  
**David Ricardo Lopez Flores:** No, dale ahí para arriba, para arriba. Si ves ahí las si ves ahí los este los operadores que usan, o sea, sí te acuerdas que algo vimos de eso por alguna vez.  
**luis martinez corral:** Ajá. Sí, sí.  
**David Ricardo Lopez Flores:** Entonces, entonces a lo que a lo que voy es hay que asegurarte que lo que vayas a documentar pues esté de acuerdo al estado del arte nada más porque sí hay muchas formas de documentar el modelo y una  
**luis martinez corral:** Ah.  
**David Ricardo Lopez Flores:** de ellas es como lo vimos uy hace tiempo ya te acuerdas.  
**luis martinez corral:** Sí. Entonces siente.  
**David Ricardo Lopez Flores:** Entonces, nada, nada más hay que tener cuidado con eso, o sea, que no vayamos no vayamos a inventar una forma que no existe de cómo documentar un modelo.  
   
 

### 01:58:53

   
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** Eso es lo que hay hay que tener cuidado nada más.  
**luis martinez corral:** Sí. Okay.  
**David Ricardo Lopez Flores:** Si tú ya si tú ya entiendes como está ahorita y está documentado en el estado del arte, no hay problema. Pero si no está en estado del arte y fue algo que que está es algo que está difiriendo en estado del arte, eso verás cómo molesta los a los revisiones por pares que uno invente términos, ¿eh?  
**luis martinez corral:** Aha.  
**David Ricardo Lopez Flores:** No, no te imaginas, ¿no? Si por eso no más te van para atrás a la primera.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** Es es este hay que tener mucho cuidado con eso, inclusive desde la desde el manejo de términos que de repente se te ocurre a ti un por eso te preguntaba de los términos y eso así se maneja en el estado del arte porque a veces tan solo eso de introducir un término que no es común dentro de ese temática, ah, cómo molesta eso a los que revisan más allá. O sea, aquí pues estamos en confianza, pero más allá. Me refiero ya en revisiones por pares. Hay que tener cuidado con eso. Sí, sí. Adelante.  
**luis martinez corral:** Okay.  
   
 

### 02:00:00 {#02:00:00}

   
**David Ricardo Lopez Flores:** Continúa, continúa con lo con lo otro.  
**luis martinez corral:** Entonces, pues de aquí he sacado, ¿cómo se dice? Y aquí de este chat yo le pedía que le decían un PR maestro, pídele tal matriz, pídele tal explicación matemática, eh, y dile a cursor que lo haga.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Entonces, prácticamente establecí una línea de conexión entre chat GPT y y cursor, porque cursor es el que ha hecho ahora sí que que el código y la parte de revisión, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Mhm. Mhm.  
**luis martinez corral:** eh pues más, ¿cómo se dice? más más literaria la ha hecho con con Gemini, pero entonces por y y este informe pues ahora sí que es un un conglomerado de de todas las partes.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Aquí está lo de la evaluación por por cómo se dice, de concordancia entre el fus y el clustering. las medidas de desempeño del sistema difuso diseñado con el conocimiento por concordancia altamente con un F1 mayor a al 80% con una operativa verdad operativa derivada empíricamente del clustering ha demostrado que ambos métodos independientes capturan la misma estructura subyacente del centarismo. Métrica seleccionada, precisión, sensibilidad, este el F1 score y este, ¿cuál es la sila del MSCSC?  
   
 

### 02:01:36 {#02:01:36}

   
**Abimael Guzman Pando:** Miss classification es  
**luis martinez corral:** Sí, pero bueno, le le aplicamos las las cuatro métricas al modelo.  
**David Ricardo Lopez Flores:** de fusi y a eso te refieres a haber utilizado un set como organizado  
**luis martinez corral:** Ajá.  
**Abimael Guzman Pando:** A ver.  
**luis martinez corral:** eh un set de validación cruzada y análisis de rast test.  
**Abimael Guzman Pando:** Ah, no es el coeficiente de correlación de Matius ese.  
**luis martinez corral:** Bueno, pues aplicamos ahí los los cuatro, ¿cómo se dice? los cuatro los cuatro medidas de desempeño.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Este, aquí tenemos nuestras reglas de decisión, la matriz de de coinfusión métricas. Entonces, el accuracy eh tiene un 74% de de clasificaciones correctas. en predición tiene un 73% de predicciones de alto sedentarismo. Eh, el recal, el 97.6 de los casos está con alto sedentarismo detectado, el F1 score o el punto 84%, ¿cómo se dice? de con un balance colete  
**Abimael Guzman Pando:** Yeah. Estamos hablando de que es el promedio de las 10 corridas.  
**David Ricardo Lopez Flores:** Es lo que es mi duda, o sea, es de que, o sea, o son ocho ocho corridas con ocho, o sea, ocho usuarios y dos de prueba.  
   
 

### 02:03:10

   
**David Ricardo Lopez Flores:** Es lo que no no me yo no estoy entendiendo ahí.  
**luis martinez corral:** H Ok.  
**Abimael Guzman Pando:** Porque si es así, hay que poner también las lavón estándar y y ver qué tanto variaron, ¿verdad?  
**David Ricardo Lopez Flores:** O sea, o sea, y y por ejemplo, ¿contra quién?  
**Abimael Guzman Pando:** entre corriendo.  
**David Ricardo Lopez Flores:** ¿Contra quién tú dijiste esto sí es cierto? Esto no es cierto. Esto sí es cierto. Esto no es cierto.  
**Abimael Guzman Pando:** El clúster lo usó como si fuera el gran Ajá.  
**David Ricardo Lopez Flores:** La verdad operativa.  
**luis martinez corral:** Ajá. Sí. Cruzada.  
**David Ricardo Lopez Flores:** Ah, okay, okay. Sí, es que ahí me perdí. Ahí me perdí. Sorry.  
**Abimael Guzman Pando:** ¿Quién sabe?  
**David Ricardo Lopez Flores:** El clúster. El el clúster. ¿Pero sobre qué? ¿Sobre los perceptiles o sobre las cuatro variables? Entonces hay que hay que aclarar eso, ¿no? Hay que aclarar eso, ¿no? Ahí dice, dice, "No, no, pero eso es otra cosa."  
   
 

### 02:04:11 {#02:04:11}

   
**David Ricardo Lopez Flores:** Ya, no.  
**luis martinez corral:** Esto es porque no se paré en 80 20 y usamos el el one user alternativa.  
**David Ricardo Lopez Flores:** Alo.  
**Abimael Guzman Pando:** de Aha.  
**David Ricardo Lopez Flores:** No, pues más bien lo, o sea, más bien la duda anterior era, ¿cuál era la verdad operativa? para clustering, ¿no?  
**luis martinez corral:** Ajá.  
**David Ricardo Lopez Flores:** Sí, pero clustering hay que hay tienes que definir bien si cuál si fueron las cuatro variables o los o eso de que estábamos discutiendo, ¿no?  
**luis martinez corral:** Sí, el el cluster. Ajá.  
**David Ricardo Lopez Flores:** Hay que tener cuidado porque porque sí se va a malinterpretar eso.  
**luis martinez corral:** Ah, aquí.  
**David Ricardo Lopez Flores:** Y contra quién decidiste todas esas métricas que era verdad o mentira. Ok.  
**luis martinez corral:** Ajá.  
**Abimael Guzman Pando:** Sí, mira, ahí procedimiento.  
**luis martinez corral:** Aquí. Aquí vienen nuevos usuarios restantes, el test del usuario eh recalcular entrada presentes para los numberad operativa organización aplicar el sistema entrenado test de valor métricas para repetir para 10 usuarios.  
**Abimael Guzman Pando:** Ah, mira, viene métricas finales media más desviación estándar. Esa es la que estoy necesitando, pero no viene acá más menos deción estándar.  
   
 

### 02:05:20 {#02:05:20}

   
**Abimael Guzman Pando:** Ándale. Entonces esa sobre las 10\. Eso via hasta mero abajo. ¿Dónde viene?  
**luis martinez corral:** Eso yo creo que no lo tienes. A lo mejor en la porque toda estuve ayer trabajando un rato y esto lo y con lo que estaba batallando era con las, ¿cómo se dice? con las tablitas porque salían mucho de la ventana y y se me hace que ya las ajusté al final, pero ahí les paso esta versión ahorita.  
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** Mhm.  
**Abimael Guzman Pando:** Ok.  
**luis martinez corral:** El modelo generaliza aceptablemente a usuarios no vistos con un F1 del 81% aliado un sistema difuso.  
**David Ricardo Lopez Flores:** Ah.  
**luis martinez corral:** Captura patrones universales no específicos para la muestra completa.  
**Abimael Guzman Pando:** Y acuérdate de hacer para el paper eso, el de la normalización después de que haces la división.  
**luis martinez corral:** Okay. cambios de Ah, aquí probamos con  
**Abimael Guzman Pando:** Pues eso se ve. Eso, ¿qué era? Modelo contra qué?  
**David Ricardo Lopez Flores:** Ludo.  
**Abimael Guzman Pando:** A contra dos.  
**David Ricardo Lopez Flores:** El U. Bueno, en el U, ¿qué valstate?  
   
 

### 02:06:34

   
**luis martinez corral:** Sí, aquí utilizamos, ¿cómo se dice? Eh, ajá, pero ahí en vez de usar cuatro cuatro variables, utilizamos después dos dos reglas y y y es eh  
**David Ricardo Lopez Flores:** El fusil, ¿no? Eh, espérate, espérate, espérame, espérame, espérame. No, no te me adelantes. El Lúo, el Lúo, el Lúo. Analizaste el modelo con cuatro entradas.  
**luis martinez corral:** sí, con cuatro entradas y y volvimos a repetir este, pero después, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Ah, okay. Y ahí fue de uno contra nueve y luego brincaste al siguiente contra otros nueve.  
**luis martinez corral:** Desactivamos eh dos variables y y dos reglas.  
**Abimael Guzman Pando:** Desactivaste las dos variables que que se sobrelapaban.  
**luis martinez corral:** Este aquí procedimiento recalcular dos variables excluir regla 3 y cu optimizar independiente comparar métricas cuatro cuatro variables versus dos variables.  
**David Ricardo Lopez Flores:** Pero, ¿cuáles fueron las que quitaste?  
**Abimael Guzman Pando:** A ver, dale para Ah, okay.  
**luis martinez corral:** Eh, la la las cardíacas.  
**David Ricardo Lopez Flores:** Ah, las que las que no se miraban separabilidad.  
**luis martinez corral:** Ajá.  
   
 

### 02:07:46

   
**David Ricardo Lopez Flores:** Ándale. Pues es que todo eso, todo eso tienes que entrelazarlo, Luis.  
**luis martinez corral:** Ho. Ah.  
**David Ricardo Lopez Flores:** Es cuando te digo, es que cuando es que a veces presentas, estás en una cosa y que lo que para ti es a lo mejor ya entendible, para nosotros no.  
**Abimael Guzman Pando:** Mm.  
**David Ricardo Lopez Flores:** Tú debes de entrelazar siempre debes de mantener la conexión y no que lo que estés analizando se vea ah digamos este separado de lo demás. Por ejemplo, ahí pudiste haber dicho como como te preguntamos ahorita, se eliminaron dos porque de acuerdo a la gráfica que estaba allá mostraban poca separabilidad.  
**luis martinez corral:** Mhm.  
**David Ricardo Lopez Flores:** Entonces todo eso es lo que no se te olvide manejar en el escrito de tu tesis. Y cuando presentes tu defensa, pues todo es algo que tú lo tienes que entrenar y lo tienes que ensayar más de una vez.  
**luis martinez corral:** Okay. Okay. Sí. Y y ya, ¿cómo se dice? Y y pues ya aquí la bajó el desempeño, ¿cómo existe?  
**Abimael Guzman Pando:** Se vio que sí bajó el desempeño.  
**luis martinez corral:** Hasta el 60% de del 80%.  
   
 

### 02:08:51 {#02:08:51}

   
**luis martinez corral:** Entonces, ¿cómo se dice? Eh, ajá.  
**David Ricardo Lopez Flores:** No era lo que esperabas que tuviera el desempeño,  
**luis martinez corral:** Entonces, no sabemos por qué si no discrimina, ¿cómo se dice? Las el delta cardíaco y la variabilidad de la frecuencia cardíaca. Al quitarlos de del modelo de de cuatro reglas se pierde. ¿Cómo se dice?  
**David Ricardo Lopez Flores:** Bueno, eso que no sabemos se queda con se escribe.  
**luis martinez corral:** Eh, es  
**David Ricardo Lopez Flores:** Por lo tanto, a trabajo futuro se va a hacer un análisis.  
**Abimael Guzman Pando:** Es eso se eso se puede analizar con análisis multivariado usando un este un random forest, por ejemplo, y ya checas la contribución que tuvo cada una de las variables de entrada, pero eso pues ya para el JCRA, ¿no?  
**luis martinez corral:** okay. Sí, sí.  
**Abimael Guzman Pando:** Para lais ya.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Y aquí viene, ¿cómo se dice? eh el análisis de de robustez y vemos cómo cómo cae el el 50%, ¿cómo se dice? de de rendimiento de cuatro variables versus dos variables.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Ah, dice reglas dos 3 cu capturan estados compensatorios baja actividad con alta variabilidad de la frecuencia cardíaca que el análisis variado no detecta.  
   
 

### 02:10:09

   
**luis martinez corral:** El sistema difuso explota interacciones no lineales entre variables and las variables débiles univariadamente aportan valor en combinaciones multivariadas.  
**David Ricardo Lopez Flores:** Oh.  
**luis martinez corral:** Es lo que dices del random forest.  
**Abimael Guzman Pando:** Ajá. Si es que combinadas, algunas variables combinadas aportan más discriminación. Por eso sí son necesarias también.  
**luis martinez corral:** Okay, entonces este pues es porque no elegimos, ¿cómo se dice? el el 2030, que yo creo que eso ya pues está de más porque sí nos funcionó el el proceso de 9 y1 y y ya nada más, ¿cómo se dice?  
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** A ver, A ver, a ver, ya si yo me perdí.  
**luis martinez corral:** Eh, eh, el 2030 eh agarra, ¿cómo se dice?, datos aleatorios de los de los usuarios y y ya no los podemos, ¿cómo se dice?  
**David Ricardo Lopez Flores:** ¿Por qué el 2030? Yo sé que más o menos sí lo leí. ¿Por qué no el 2030?  
**luis martinez corral:** Eh eh clusterizar o o agrupar.  
**David Ricardo Lopez Flores:** Okay. Y el nu y el 91 es de la metodología del UO.  
   
 

### 02:11:24 {#02:11:24}

   
**luis martinez corral:** Entonces, eh sí, entonces en vez de utilizar un split 80 de forma aleatorio para las 13 semanas, dejamos nada más un usuario, entonces ya podemos aplicarle el modelo sobre todo el comportamiento  
**David Ricardo Lopez Flores:** Ah, okay. Sí. No, no aplica aquí. No aplica.  
**luis martinez corral:** lineal de un usuario versus los nueve.  
**David Ricardo Lopez Flores:** Y el y el dúo de 91 lo has visto en otros en otros trabajos.  
**luis martinez corral:** Entonces, no, de hecho ese ese sí no lo no lo comentado. Fue, ¿cómo se dice? Sugerencia de la inteligencia artificial. Mir, aquí esta gráfica también se me se me sale del margen, pero pero igual ahí les paso este documento que está más completo que que la última versión.  
**David Ricardo Lopez Flores:** Lo.  
**luis martinez corral:** Ah, y luego pues aquí, ¿cómo se dice? Luego como alternativa robusta, ventaja preservate paraidad dentro de cada usuario sin fuga o la generación entre el sujeto interacciones, ¿no? Una aprovecha todos los datos. Cada usuario sirve como un test métricas con noan. Aquí está. ¿Cómo se dice? Esto fue lo último que hice. Tampoco lo no lo he revisado.  
   
 

### 02:12:52 {#02:12:52}

   
**luis martinez corral:** Lo hice ahí mientras los esperé ahorita para la conexión. Eh, vamos viendo a ver qué tiene aquí. Parámetros de funciones de pertenencia de la tabla 11.2. actividad relativa eh superit calórico porcentaje eh variabilidad de la frecuencia cardíaca en milisegundos y delta cardíaco en lativas por minuto. Aquí están las funciones de pertenencias bajo, medio, alto para cada una de las cuatro variables de niveles de de descificación 2 5 y 08 por abajo medio alto. Caso estos son los del centroide, ¿verdad? Son las entradidas para cada uno.  
**Abimael Guzman Pando:** Mm. Nivel de fifica.  
**David Ricardo Lopez Flores:** Ni idea.  
**Abimael Guzman Pando:** No sé, no dice ahí.  
**David Ricardo Lopez Flores:** Es que no dice niveles de descu Yo creo que son los niveles e del salida del fusi que tú que tú lo interpretarías como bajo, punto C medio y punto 8 como alto.  
**Abimael Guzman Pando:** Sí, ya los umbrales no.  
**luis martinez corral:** Ah\! Ah\! Sí\! Ah\! Sí, sí, sí, sí, sí, sí. Entrada en la caso, una semana sedentaria típica.  
   
 

### 02:14:08

   
**luis martinez corral:** Entrada X tenemos 35 15.2 35.1 28.4. Entonces actividad relativa en el en el conjunto, ¿cuál era el B?  
**Abimael Guzman Pando:** Hm.  
**luis martinez corral:** Ah, es bajo, medio, alto. Entonces, aquí en el eh en la en el no es el conjunto, pero la variable B pertenece al A ver, a leer esto.  
**David Ricardo Lopez Flores:** No, mira, espérame. Es que mira, es ahí te va, ahí te ve. Es es la entrada la entrada. Por ejemplo, si tengo actividad relativa pun 35, la fusificación de B es punto 50 de M0 y A0.  
**luis martinez corral:** Ajá.  
**David Ricardo Lopez Flores:** O sea, nada más está portando bajo. Sí. Y los superávidólicos y la entrada son 15.2, la fusificación es punto 48 en el conjunto bajo, en el medio 00 en el medio y el alto cero.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** O sea, que no más está activando la función bajo y va a y para las demás de manera similar.  
**luis martinez corral:** Sí. Aha.  
**Abimael Guzman Pando:** H  
**David Ricardo Lopez Flores:** Entonces esas justificaciones ya entran al proceso de inferencia, o sea, la activación de las reglas.  
   
 

### 02:15:29

   
**luis martinez corral:** Sí. Y este es para el caso uno. Entonces, por decir para un caso dos.  
**David Ricardo Lopez Flores:** Es un ejemplo, sí, es un ejemplo de cómo corre el algoritmo y los valores cómo los va dando nada más. Y ya el la fusificación punto 80, entonces sedentarismo punto entonces sedentarismo. Sí. O sea, que es sedentaria.  
**luis martinez corral:** Mm. Es aquí en el paso de activación de las reglas tenemos las Sí. Ajá.  
**David Ricardo Lopez Flores:** Y si es y según y según el formulario eso se encuadra con el formulario de esa persona. Sí, va. Okay.  
**luis martinez corral:** Sí. Este son tres tres ejemplos al azar que agarramos ahí.  
**David Ricardo Lopez Flores:** y si cuadran con el con lo que te rojó el formulario y eso eso sí lo tienes contemplado este como una comparativa, o sea, como como como decir esto fue lo que me evalué los usuarios tales con el  
**luis martinez corral:** Sí, pues esto.  
**David Ricardo Lopez Flores:** modelo difuso y toda la metodología y estos fueron los resultados y esto es con el formulario.  
**luis martinez corral:** Ajá. Sí, estos ya estos ya son, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Okay. No más.  
**luis martinez corral:** ejemplos prácticos.  
   
 

### 02:16:44

   
**David Ricardo Lopez Flores:** Sí, son ejemplos. Sí, son ejemplos.  
**luis martinez corral:** O sea, si agarramos cualquier caso al azar puede caer a lo mejor eh Sí. Ah ah ah.  
**David Ricardo Lopez Flores:** Mm.  
**Abimael Guzman Pando:** El operador de agregación fue el min, ¿verdad? También o max.  
**David Ricardo Lopez Flores:** Es fue Max. Max, no, Max. Pues fue un mandami el mandami creo que es Max me. M. No, no, pero ya para qué le muevo ahorita.  
**luis martinez corral:** Agregación.  
**Abimael Guzman Pando:** Este también se puede usar con el de producto punto.  
**luis martinez corral:** Acá lo y aquí está el caso tres.  
**Abimael Guzman Pando:** No, no, pero no más quiero saber cuál se usó.  
**David Ricardo Lopez Flores:** No, no. Bueno, que no más. Pero pero igual, o sea, no sé si eso lo No, ahí está, ahí está.  
**luis martinez corral:** Acá tenemos otra matriz de comparación de los de los tres casos.  
**David Ricardo Lopez Flores:** Pinga su máquina estuvo bueno.  
**luis martinez corral:** Pues ahí quedó.  
**Abimael Guzman Pando:** A ver, ese de compensación es intermedio o qué?  
**David Ricardo Lopez Flores:** Ah.  
**luis martinez corral:** ¿Cómo?  
   
 

### 02:17:46 {#02:17:46}

   
**Abimael Guzman Pando:** El de tres, el compensación. A ver, es alta baja porque según clustering era alto y bajo, ¿no?  
**luis martinez corral:** Sí. Compensación.  
**Abimael Guzman Pando:** Y ese compensación que es, o sea, entonces al final el sistema difuso da tres tres salidas.  
**David Ricardo Lopez Flores:** No, pues no.  
**luis martinez corral:** Ah. Ah. Ah. Es que aquí es baja actividad física, pero alta variabilidad cardíaca. O sea, no eh es es que hay, ¿cómo se dice?  
**David Ricardo Lopez Flores:** cambió eso.  
**luis martinez corral:** Eh, sí. No, no, no. Aquí aquí por decir aquí la salida de este regla uno, sentario alto, regentario. Ah, justificación.  
**David Ricardo Lopez Flores:** No, es que eso no es la salida.  
**luis martinez corral:** Ah, no, no es sedentario, pero tiene una variabilidad de la frecuencia alta y variabilidad de la frecuencia alta es positivo porque quiere decir que está relajado, que está, o sea, sigue estando sedentario, pero se siente bien.  
**Abimael Guzman Pando:** Mm. Entonces acá en las tres últimas que muestras, a ver, dale otra vez a donde decía compensación en clase.  
   
 

### 02:18:46

   
**luis martinez corral:** Eso. Entonces te digo, y y es que ese es el el problema con la variable de la frecuencia cardíaca, que a lo mejor tú puedes estar dando hueva, no no estar haciendo nada, pero sentirte bien.  
**Abimael Guzman Pando:** Ca. M.  
**luis martinez corral:** ¿Sí me explico? Porque eh la variabilidad de la frecuencia cardíaca, quedamos que entre más alto era la variabilidad de la frecuencia cardíaca, eh el eh el estrés fisiológico de tu cuerpo es que estaba estaba mejor, o sea, entre más alta la variabilidad de la frecuencia cardíaca, tu estado de salud es más óptimo. Y nosotros tenemos casos donde tenemos una persona sedentaria, pero que goza de buena salud, o sea, eh eh Ajá.  
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** Y eso consideras como alto asterisco.  
**luis martinez corral:** Sí. Entonces, eh tiene es sedentaria la persona, pero está sana.  
**Abimael Guzman Pando:** O sea, en este caso entonces nos está diciendo que pero en este caso específico fue sedentarismo, o sea, caso uno fue sedentario.  
**luis martinez corral:** Hay personas enas con buena salud.  
**David Ricardo Lopez Flores:** Y eso no fue con Ya.  
**luis martinez corral:** ¿Cómo? O sea, el caso uno es una persona sedentaria que tiene mala calidad de vida.  
   
 

### 02:20:07

   
**luis martinez corral:** El caso dos es una persona activa y pues con buena calidad de vida. Ahí a lo mejor debería haber un tercer caso donde tenemos una persona activa y tiene variabilidad de la frecuencia cardíaca baja.  
**Abimael Guzman Pando:** Okay, okay, ya te entendí. O sea, la clase que predijo acá el modelo difuso fue alto, que sería que sedentarismo, pero se siente bien.  
**David Ricardo Lopez Flores:** Ah.  
**luis martinez corral:** Sí. O sea, eh el es este el número tres tiene actividad, o sea, todas las la Ah, estoy acá con el dedo.  
**David Ricardo Lopez Flores:** Sí, sí.  
**Abimael Guzman Pando:** Ajá.  
**luis martinez corral:** Actividad y actividad. Estas son, ¿cómo se dice?  
**David Ricardo Lopez Flores:** ¿Y qué pasó  
**luis martinez corral:** Métricas de movimiento. Son bajas, pero la de la de salud, la la cardiovascular es alta.  
**Abimael Guzman Pando:** Está bien. Okay.  
**luis martinez corral:** Entonces, el vato el vato este, o sea, o la el caso, ejemplo, este es de una persona que a lo mejor tiró flojera, que estuvo, ¿cómo se dice?, más sedentaria lo normal, pero se sentía bien.  
**David Ricardo Lopez Flores:** con la cuarta entrada ahí?  
**luis martinez corral:** Entonces aquí debería otro ejemplo que este es alta, alta, pero se siente mal, ¿no?  
   
 

### 02:21:11

   
**Abimael Guzman Pando:** Sí, cierto. Y la cuarta entrada aquí.  
**David Ricardo Lopez Flores:** Y la cuarta entrada que Luisa, no usaste la otra entrada.  
**luis martinez corral:** Pero es este es un, ¿cómo se dice? Fue un ejemplo que hice ahorita al final.  
**Abimael Guzman Pando:** Ah, es que en ese ejemplo no se esta entrada, yo creo, pero no genera.  
**David Ricardo Lopez Flores:** No, si está ahí, mírala. Ahí está.  
**luis martinez corral:** No, sí. Delta, Delta.  
**David Ricardo Lopez Flores:** ¿Dónde está la otra?  
**Abimael Guzman Pando:** Ah, no, sí, sí está.  
**David Ricardo Lopez Flores:** No, no, no. Es que está bien, o sea, si entendemos que intentaste poner un ejemplo numérico, pero ten cuidado con eso porque pues ahí no se ve la cuarta entrada, o sea, no está la cuarta entrada ahí, ¿no?  
**luis martinez corral:** Ah, aquí, aquí de aquí dice C. Es que este este ejemplo lo hice ahorita con con Pero es de hecho por eso lo hice aquí como apéndice y no como el capítulo nada más para Ok.  
**David Ricardo Lopez Flores:** Ya tú sí, sí, ya es que ya estás en corto. Ya estás en corto circuito. Ya estás, eh.  
   
 

### 02:22:02 {#02:22:02}

   
**David Ricardo Lopez Flores:** No, está bien. Mira, yo creo que yo creo que ahora hay que recapitular qué va a documentar Luis Aimar, porque ya, o sea, ya él tiene que irse ahorita con una línea de trabajo y y centrarse en esa línea de trabajo,  
**Abimael Guzman Pando:** Sí, sí, pues yo pienso que así como lo tiene está bien que lo documenta así en la tesis, nada más que sí incluya la gráfica de clustering usando las cuatro variables con el TCA.  
**David Ricardo Lopez Flores:** ¿no? Sí, Luis, si es alcanzable, ¿no? N más es poner una gráfica, ¿no?  
**luis martinez corral:** Muy bien. Sí. Entonces, okay.  
**David Ricardo Lopez Flores:** Okay. Y recuerda con las confusiones que nos creaste, que no queden en la tesis, ¿eh?  
**Abimael Guzman Pando:** Ah, Luis, si la vas a hacer también hazla con PSA y con TSNE para ver si es este TU- SN.  
**luis martinez corral:** ¿Cuál es el otro? T. T.  
**Abimael Guzman Pando:** Una es para datos cuando tienen relación lineal y otra cuando no. O también puede ser debes can cualquiera de las que tú quieras de esas dos que sean para datos no lineales. M.  
   
 

### 02:23:07

   
**David Ricardo Lopez Flores:** Y luego recuerda mucho, Luis, no secciones, o sea, cuando hables de de una sección tienes que enlazar con la anterior o con lo que tú quieras de lo anterior y de anterior.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** El chiste es que no se desarticule el documento, que no aparezca una sección como que ah esta sección que tiene que ver con las anteriores. Okay.  
**luis martinez corral:** Mm. Okay.  
**David Ricardo Lopez Flores:** Y luego evita este que evita también por ahí te puse mucho de que si la variable se llama a A se va a llamar en todo el documento. Okay.  
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** No cambies ni a cortes, ni extiendas, ni a sumas, que todos vamos a entender que que modelo A es lo mismo que model A. ¿Sí? Entonces, hay que uniformizarlo de variables y que sobre todo esa confusión grande que tuvimos con los perceptiles, que al final de cuentas sirvieron para lo declarar las funciones de membresía, que quede bien claro eso y que solo se usaron para eso y que al final de cuentas por clustering te diste cuenta que esas cuatro variables pues dos de ellas sí presentan alta diferenciación, mientras las otras no. Sin embargo, así deo mejores resultados el el modelo con considerando las cuatro entradas.  
   
 

### 02:24:26

   
**luis martinez corral:** Okay, muy  
**David Ricardo Lopez Flores:** Luego ahí no sé este, ¿qué más quieres agregar? Entonces te quedas con esa línea de trabajo ya, o sea, ya a documentar en tesis esto así lo de redes neuronales y eso pues te va a  
**Abimael Guzman Pando:** Sí, yo creo que sí nos quedamos con esto y recuerda no comentar ya para nada lo de Hm. Ándale, eso lo de las redes normales.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** ayudar a que acabes más rápido también. Sí. Oye, Luis, ¿estás manejando en tu tesis cuáles son tus contribuciones?  
**luis martinez corral:** Entonces, igual nada más por si las dudas aquí les voy a mandar, ¿cómo se dice? El el documento actualizado, si les llegara, ¿cómo se dice?  
**Abimael Guzman Pando:** Sí, mandanos.  
**luis martinez corral:** Eh, ¿cómo que? O sea, ¿cuáles son?  
**Abimael Guzman Pando:** Es que por lo regular no se usa en las tesis. Ah, no más en el resumen se llega a poner algo, pero para que vaya pensando en el JCR.  
**David Ricardo Lopez Flores:** Bueno, yo decía como para que lo alineara. Así es. O sea, por ejemplo, mira, abre el el documento ese que te envié ahí por el chat, el que dice gaps.  
   
 

### 02:25:41 {#02:25:41}

   
**Abimael Guzman Pando:** Gaps.  
**David Ricardo Lopez Flores:** Ajá.  
**luis martinez corral:** Ahí va.  
**David Ricardo Lopez Flores:** O sea, yo detecté esas esas contribuciones, ¿no? Pero pues igual me puedo estar equivocando, ¿no? No están completadas unas, pero pues es la idea centrar. ¿Qué se propone? Pues se propone el título de tu tesis. Sí. Y o sea, y con base aquí está el modelo y todo lo que propones.  
**luis martinez corral:** Mhm.  
**David Ricardo Lopez Flores:** Y luego los gaps es lo que tú ves que no está en la literatura, que no existe y luego tus contribuciones es la respuesta de esos gaps. Por ejemplo, ahí dice un método de imputación híbrido basado en M1-5 que mejora la calidad de los datos.  
**luis martinez corral:** Ok.  
**David Ricardo Lopez Flores:** Y en la literatura ningún trabajo del estado del arte utiliza una estrategia híbrida de imputación de datos.  
**luis martinez corral:** Ok.  
**David Ricardo Lopez Flores:** O sea, yo sé que a lo mejor no sé cuál es el modelo de escritura de la tesis de el formato de ellos ahí mal, pero pues sí serviría que fuera pensando en en este en Ajá.  
**Abimael Guzman Pando:** Eso.  
**David Ricardo Lopez Flores:** en que porque pues al final de cuentas él tiene que argumentar, bueno, ¿qué propuso y qué cont?  
   
 

### 02:26:58 {#02:26:58}

   
**David Ricardo Lopez Flores:** O sea, qué contribuciones derivaron de lo que propuso, ¿no? Eso es pues básicamente la respuesta a los gaps.  
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** Entonces, no sé, Luis, no si te confundes, no lo hagas. Simple, simplemente hazlo como lo estás haciendo ya. Okay.  
**luis martinez corral:** Okay, igual ahí me ve cómo se dice ahora sí que el tiempo ir reflexionando un poquito más, leyendo yo, ¿cómo se dice? Parte por parte, sin, ¿cómo se dice? Ya sin correr tanto, ¿eh?  
**David Ricardo Lopez Flores:** Código. Sí, ya no, ya no. Sí, ya no. Si es si es algo que de plano es corre mucho código. No, ya ya no es porque si no no va a sacar documental.  
**Abimael Guzman Pando:** No vas a acabar.  
**David Ricardo Lopez Flores:** Okay.  
**luis martinez corral:** Ok.  
**David Ricardo Lopez Flores:** Okay. Este, tú vas a tú vas a de todo lo que te dijimos, solo con solo haz lo que sí es alcanzable. Lo demás queda queda así como que en pauta para pues para una publicación tipo JCR. Ahí sí se tendría que implementar.  
   
 

### 02:27:59

   
**David Ricardo Lopez Flores:** Okay, sale.  
**luis martinez corral:** Okay, de acuerdo.  
**David Ricardo Lopez Flores:** Pero eso ya está fuera fuera de lo que tienes que entregar ahorita. Primero hay que concentrarte en esto que es el escrito de la tesis de de lo que está escrito ahí.  
**luis martinez corral:** Okay, muy bien.  
**David Ricardo Lopez Flores:** ¿Sí está bien identificado? ¿Consideras que está bien identificado o no? Esos gaps y pueda y pueda que haya más, pero que yo no los detecte.  
**luis martinez corral:** H, sí.  
**David Ricardo Lopez Flores:** Entonces, pero ve cómo están estructurados.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** Okay. Nada más para que lo vayas teniendo en mente, pues al final de cuentas eso es lo que tú estás aportando a esta área. Okay. Y sabes por qué, por qué, sobre todo, porque pues me otra vez me llamó mucho la atención que tú mismo te estás cancelando. Dijiste, "Es que yo no voy a lograr ningún cambio." Pero ve lo que está escrito ahí y eso pues es algo que es de tu trabajo. Entonces, pues primero hay que creértela que sí se puede, ¿no? Y ya el eso de el hecho de que te digan que sí o no, tu trabajo vale la pena.  
   
 

### 02:29:06

   
**David Ricardo Lopez Flores:** Vamos a dejárselo a gente que es externa a este tema, pero pues nosotros hay que creer que sí se puede. Okay.  
**Abimael Guzman Pando:** M. No, pues yo yo pienso que hasta aquí está Mhm.  
**luis martinez corral:** Okay, de acuerdo.  
**David Ricardo Lopez Flores:** Bueno, pues no sé qué otra cosa más, doctoral, puedas podamos ver. Pues yo creo que ya hasta aquí está bien. Yo creo que no nos veríamos hasta cuándo, Luis.  
**luis martinez corral:** Eh, okay.  
**David Ricardo Lopez Flores:** O sea, porque ya porque ya, o sea, ya es que te pongas a escribir, Luis, ya no es que nos demuestres más metodología.  
**luis martinez corral:** Entonces, ya nada más trabajaría sobre los documentos y y se los pasaría para revisión.  
**David Ricardo Lopez Flores:** Yo creo que sí, ¿no?  
**Abimael Guzman Pando:** Pasando tus avances.  
**David Ricardo Lopez Flores:** Bueno, pero, o sea, que vaya pasando conforme vaya avanzando, mejor que tenga un borrador final.  
**luis martinez corral:** Okay, muy bien, perfecto.  
**Abimael Guzman Pando:** Mes se hace que el no sé ahí cómo cómo estaría mejor trabajar porque cómo te sientes más presionado.  
**David Ricardo Lopez Flores:** Pues es que lo que no sé es que nos diga Luis porque es que a mí se me hace que va a ser más estresante que nos lo esté pasando por pedazo y nosotros hundiéndole por pedazo.  
   
 

### 02:30:20 {#02:30:20}

   
**Abimael Guzman Pando:** Sí, también.  
**David Ricardo Lopez Flores:** O sea, no se me hace muy se me hace muy Mira, es que yo mira yo yo es que mira lo que yo pienso que ya todo lo que te pudimos haber dicho ya te lo dijimos, Luis.  
**Abimael Guzman Pando:** Pero sí, ya tienes  
**luis martinez corral:** No. Creo que lo podemos este crear en tres bloques, ¿no? Eh, Yeah.  
**David Ricardo Lopez Flores:** Yo creo que esta revisión de tesis va a ser nada más en cuestión a que esté bien escrita, que esté en formato y si vemos algo que no se que no se aclaró, pues te lo hacemos saber. O sea, yo pienso que debería ser un que debería, o sea, con esto con este ejercicio que acabamos de hacer, yo pienso que la revisión debería ser más rápido, o sea, ya no de que sea un borrador final.  
**Abimael Guzman Pando:** Ya, el borrador final.  
**David Ricardo Lopez Flores:** Exactamente, porque ya porque ya yo pienso con esto que hicimos ahorita es que Luis ya entendió qué es lo que tiene que hacer, porque si Luis hubiera escrito la el borrador sin haber tenido esta sesión, pues es lo que le hubiéramos dicho en esa revisión.  
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** Entonces, tenemos que confiar en que Luis va a hacerlo tal y como lo hemos estado platicando ahorita para que ya sean mínimas las revisiones con Luis.  
   
 

### 02:31:24 {#02:31:24}

   
**David Ricardo Lopez Flores:** Eso es lo que se espera, ¿no? Es la hipótesis.  
**luis martinez corral:** Este, yo digo que les puedo pasar por por partes. por ejemplo, eh, pues okay.  
**David Ricardo Lopez Flores:** Bueno, es como tú te sientas, como tú te sientas. Ahí nos vas marcando la pauta. Mejor ahorita no digas nada y como tú te sientas nos dices, ahí les va la parte esta. Órale, puedes.  
**luis martinez corral:** Sí, yo creo que eh por sí ahorita resultados y de limitación del objeto de estudio ya es esto.  
**David Ricardo Lopez Flores:** Pero pues perdón. Sí. Así es.  
**luis martinez corral:** Eh, esto ya nada más documento, este, lo paso al al ¿cómo se dice? La plantilla del de la tesis y ya se los puedo nada más para que, ¿cómo se dice? Le den el vistazo general de de, ¿cómo se dice? De puntos, comas, eh saltos de página, además.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Y y ya posteriormente nada más las sacamos, ¿cómo se dice?, la la discusión y conclusiones y esa la podemos debatir. Ahora sí que, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Mhm.  
   
 

### 02:32:34 {#02:32:34}

   
**luis martinez corral:** Para ver si sí capturamos la idea de los de los gaps principales y y sobre todo, ¿cómo se dice? Buscar una bibliografía para para respaldar, ¿cómo se dice? Todo lo que vamos a discutir y argumentar.  
**David Ricardo Lopez Flores:** Sí. O sea, sido lo que yo opino es que lo que lo más fuerte que hubiera salido de la revisión fue lo que ya te dijimos ahorita y ya te dijimos que que vas a abordar lo que sí  
**Abimael Guzman Pando:** Mhm.  
**David Ricardo Lopez Flores:** es alcanzable y lo que no queda pendiente para una publicación tipo JCR y ya.  
**luis martinez corral:** Muy bien.  
**David Ricardo Lopez Flores:** Okay.  
**luis martinez corral:** Este, nada más una duda antes ya de terminar, eh, lo del A no lo vamos a documentar, pero lo del cuestionario de calidad, ¿sí o no?  
**Abimael Guzman Pando:** Sì.  
**luis martinez corral:** Lo del SF36, eso sí.  
**David Ricardo Lopez Flores:** No, eso sí o no. O yo no sé. Pues yo considero que sí. No sé.  
**Abimael Guzman Pando:** Ahí este se usó el para validar que no era posible hacerlo del cuestionario o algo así entendí que hiciste.  
**luis martinez corral:** Eh, ah, no, no nos, o sea, pues tuvimos una baja participación de de usuarios.  
   
 

### 02:33:42 {#02:33:42}

   
**luis martinez corral:** Este, intentamos est lo y no sí, sí fue.  
**David Ricardo Lopez Flores:** Pero el formulario, o sea, pero el formulario sí se usó para variar fusi también, ¿no?  
**Abimael Guzman Pando:** Ajá. No, ese sí lo ese sí documéntalo, Luis.  
**David Ricardo Lopez Flores:** No, ese no lo se puede quitar. O sea, pues es que eso fue un trabajar que no eso no eso no puede quedar.  
**luis martinez corral:** Pues de hecho hicimos hasta lo del juicio expertos y todo ese rol.  
**Abimael Guzman Pando:** Hm.  
**David Ricardo Lopez Flores:** Lo que sí podría quedar fuera es lo de, o sea, queda claro que no usaste ANN porque no encontraste una relación lineal, pero eso no cancela, eso no cancela el cuestionario.  
**Abimael Guzman Pando:** Eso no, pero el cuestionario, por ejemplo, al final sí lo usamos para validar algo y ni tampoco hacemos la relación de del fusi con el cuestionario.  
**luis martinez corral:** Okay.  
**David Ricardo Lopez Flores:** Es lo que yo le pregunté. me dijo que lo usó para fusi y no  
**luis martinez corral:** No, de esto último ya no varamos nada con el cuestionario. Pues lo que pudiéramos hacer, ¿cómo se dice? es eh en base a los resultados de cada individuo, según es el el modelo de clasificación de Fusi, eh ver cómo se comparar compararlo con el cuestionario, pues me faltaría, ¿cómo se dice?  
   
 

### 02:34:44

   
**David Ricardo Lopez Flores:** compararlo con con el cuestionario y esos resultados ya los tienes, No. Bueno, este,  
**luis martinez corral:** Correr, o sea, sacar métricas individuales ya al final de las salidas del fusil. Pero, pero, ¿cómo se dice? Se puede documentado.  
**Abimael Guzman Pando:** Se me hace que sí para que quede Bieno.  
**David Ricardo Lopez Flores:** pues es que pues sí, porque pues si no se va a perder, se va a perder todo lo del cuestionario. Se me hace se me hace una lástima.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** Okay, muy bien.  
**David Ricardo Lopez Flores:** Bueno, este, pero, o sea, no puedes simplemente relacionarlo con lo que te con lo que te di resultado, si es sedentario o no sedentario el cuestionario con lo que te de fusi si es sedentario o no sedentario, sin sacar tantas métricas, no puedes hacer esa correlación.  
**luis martinez corral:** Pues a lo mejor desde allí en los descriptivos donde vimos las los diagramas de de caja o los de violín Ahí, ahí todavía, ¿cómo se dice?  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** Tenemos identificados a los usuarios uno a uno. Podemos, ¿cómo se dice? Hacer como que pues una impresión eh global de cómo se encuentra cada usuario y su calidad de vida y su percepción de calidad de vida subjetiva y ya después mandarlos al al sistema, porque en el sistema el las  
   
 

### 02:35:54

   
**Abimael Guzman Pando:** Bien.  
**David Ricardo Lopez Flores:** Mhm.  
**luis martinez corral:** variables de de ¿cómo se dice? de del cuestionario. Eso no lo no las no las incluimos.  
**Abimael Guzman Pando:** Pero ya lo tienes, me hace Luis, porque acuérdate que hiciste 10 fs, un fold para cada usuario y dejaste uno fuera que era el que usaste para validar. Entonces, el usuario que acá está afuera no más relación con su cuestionario.  
**luis martinez corral:** Ah, entonces no más. Ah, okay. Entonces ahí checo las las salidas del de la consola y las y las matrices que me generó.  
**David Ricardo Lopez Flores:** Bueno, bueno, ahí sí, ahí sí ya me perdí mucho, pero la idea ahí está, o sea, de que de que sí sería relacionar ese cuestionario con los resultados de fusil.  
**Abimael Guzman Pando:** Mhm.  
**luis martinez corral:** sale pues.  
**David Ricardo Lopez Flores:** A ver qué queda. Bueno, pues entonces así quedamos bajo ese contexto.  
**luis martinez corral:** Mhm.  
**David Ricardo Lopez Flores:** Ya no nos vamos a juntar. Básicamente sería nada más para que que Luis estuviéramos al pendiente con Luis de que nos pasara lo como él considere los avances y y revisarlos, ¿no?  
**luis martinez corral:** Muy bien, de acuerdo.  
**David Ricardo Lopez Flores:** Okay. Bueno, pues entonces ahí estamos. Hijo de su máquina todo mareado.  
**luis martinez corral:** Mucho, muchísimas gracias.  
**Abimael Guzman Pando:** Tam.  
**David Ricardo Lopez Flores:** Bueno, a ver, no pues sí, antes sí se notó la diferencia.  
**luis martinez corral:** yo no tomé café ahora porque dije no para relax y poder dormir.  
**Abimael Guzman Pando:** Sí,  
**luis martinez corral:** Pero  
   
 

### La transcripción finalizó después de 02:37:30

*Esta transcripción editable se ha generado por ordenador y puede contener errores. Los usuarios también pueden cambiar el texto después de que se haya generado.*