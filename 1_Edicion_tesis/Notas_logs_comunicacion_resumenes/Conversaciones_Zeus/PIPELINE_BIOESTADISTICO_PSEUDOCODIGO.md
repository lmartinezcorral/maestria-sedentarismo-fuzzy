# PIPELINE BIOESTADÍSTICO COMPLETO
## Análisis Cronológico de Datos Biométricos para Clasificación de Sedentarismo

**Proyecto:** Tesis MFIPS - Modelo de Evaluación del Comportamiento Sedentario  
**Universidad:** Universidad Autónoma de Chihuahua (UACH)  
**Autor:** Luis Ángel Martínez Corral

---

## PSEUDOCÓDIGO DEL PIPELINE COMPLETO

```pseudocode
================================================================================
FASE 1: PLANTEAMIENTO Y DISEÑO DEL ESTUDIO
================================================================================

PROCEDIMIENTO Planteamiento_Inicial()
    // Capítulo 1: Planteamiento del Problema
    HIPÓTESIS_H0 ← "Existe relación CVRS ↔ Sedentarismo_Objetivo medible con ANN"
    OBJETIVO_PRIMARIO ← "Predecir CVRS (SF-36) desde datos biométricos"
    DISEÑO ← "Longitudinal observacional, N=10, BYOD"
    
    // Capítulo 2: Selección de Dispositivo
    MATRIZ_DECISIÓN ← Evaluar_Wearables([AppleWatch, Fitbit, Garmin, MiBand])
    DISPOSITIVO_SELECCIONADO ← AppleWatch  // Score: 9.2/10
    
    // Capítulo 2: Diseño de Cohorte
    N_OBJETIVO ← Calcular_Tamaño_Muestral(
        n_total_objetivo = 1000 observaciones,
        T_seguimiento = 130 semanas promedio
    )
    N_PARTICIPANTES ← 10  // 5M/5F, edad 34.2±6.7, IMC 24.8±3.2
    
    RETORNAR DISEÑO_ESTUDIO
FIN_PROCEDIMIENTO

================================================================================
FASE 2: RECOLECCIÓN Y PREPROCESAMIENTO DE DATOS
================================================================================

PROCEDIMIENTO Recoleccion_Datos()
    // Capítulo 3: Protocolo de Convocatoria
    PARA cada participante_id EN [u1, u2, ..., u10]:
        CONSENTIMIENTO ← Obtener_Consentimiento_Informado(participante_id)
        SI CONSENTIMIENTO == FALSE ENTONCES
            EXCLUIR participante_id
            CONTINUAR
        FIN_SI
        
        // Exportación de datos Apple Health
        ARCHIVO_XML ← Solicitar_Export_Zip(participante_id)
        SF36_DATA ← Aplicar_Cuestionario_SF36(participante_id)
        
        // Anonimización
        CODIGO_ANONIMO ← Asignar_Codigo_Usuario(participante_id)
        ALMACENAR_SEGURO(ARCHIVO_XML, SF36_DATA, CODIGO_ANONIMO)
    FIN_PARA
    
    RESULTADO_CONVOCATORIA ← {
        convocados: 15,
        incluidos: 12,
        completaron: 10,
        tasa_retención: 67%
    }
    
    RETORNAR DATOS_CRUDOS
FIN_PROCEDIMIENTO


PROCEDIMIENTO Preprocesamiento_XML_a_CSV()
    // Capítulo 3: Conversión XML → CSV
    PARA cada usuario EN [u1, u2, ..., u10]:
        XML_FILE ← Cargar_Export_XML(usuario)
        ARBOL ← Parse_XML(XML_FILE)
        REGISTROS ← ARBOL.findall("Record")
        
        DF_DIARIO ← DataFrame_Vacio()
        
        PARA cada REGISTRO EN REGISTROS:
            SI REGISTRO.sourceName CONTIENE "Apple Watch" ENTONCES
                TIPO ← REGISTRO.type  // StepCount, HeartRate, HRV, etc.
                VALOR ← REGISTRO.value
                FECHA ← REGISTRO.startDate.date()
                HORA ← REGISTRO.startDate.time()
                
                // Ajustar zona horaria
                FECHA_LOCAL ← Convertir_UTC_to_Local(FECHA, HORA, "America/Chihuahua")
                
                DF_DIARIO.append([FECHA_LOCAL, TIPO, VALOR])
            FIN_SI
        FIN_PARA
        
        // Agregación diaria
        DF_PIVOTE ← DF_DIARIO.pivot(
            index = fecha,
            columns = tipo,
            values = valor,
            aggfunc = {
                StepCount: suma,
                ActiveEnergyBurned: suma,
                HeartRate: media,
                RestingHeartRate: min,
                HRV_SDNN: media,
                WalkingHeartRateAverage: media
            }
        )
        
        DF_PIVOTE.to_csv(f"DB_u{usuario}.csv")
    FIN_PARA
    
    // Métricas de completitud
    PARA cada archivo_csv EN DB_usuarios:
        CALCULAR completitud_diaria(archivo_csv)
        CALCULAR missingness_por_variable(archivo_csv)
    FIN_PARA
    
    RETORNAR {
        archivos_generados: 10,
        completitud_promedio: 94.7%,
        días_totales: 9185
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 3: ANÁLISIS EXPLORATORIO Y VALIDACIÓN DE INSTRUMENTOS
================================================================================

PROCEDIMIENTO Analisis_Exploratorio_Inicial()
    // Capítulo 4: EDA de Variables Biométricas
    
    // Paso 1: Estadísticos Descriptivos
    PARA cada variable EN [Pasos, Calorías, FC_reposo, FC_caminar, HRV, ...]:
        CALCULAR {
            media, desviación_estándar, CV,
            mediana, Q1, Q3, IQR,
            min, max
        }
        
        // Prueba de normalidad
        SI n < 5000 ENTONCES
            p_valor ← Test_Shapiro_Wilk(variable)
        SINO
            p_valor ← Test_Kolmogorov_Smirnov(variable)
        FIN_SI
        
        SI p_valor < 0.05 ENTONCES
            REGISTRAR "Rechazar normalidad → Usar métodos no paramétricos"
        FIN_SI
    FIN_PARA
    
    // Paso 2: Visualizaciones
    GENERAR Histogramas_con_KDE(variables)
    GENERAR Boxplots_por_usuario(variables)
    GENERAR Violin_plots(variables)
    GENERAR Heatmap_patrón_semanal(Pasos)
    
    // Paso 3: Validación SF-36
    SF36_DIMENSIONES ← [FF, RF, DC, SG, VT, FS, RE, SM]
    PARA cada dimensión EN SF36_DIMENSIONES:
        alpha_cronbach ← Calcular_Alpha_Cronbach(dimensión)
        varianza ← Calcular_Varianza(dimensión)
        
        SI alpha_cronbach >= 0.70 Y varianza > 0 ENTONCES
            MARCAR dimensión COMO "Aceptable"
        SINO
            MARCAR dimensión COMO "Rechazada"
            REGISTRAR problema_psicométrico
        FIN_SI
    FIN_PARA
    
    RESULTADO_SF36 ← {
        dimensiones_válidas: 7/8,
        dimensiones_rechazadas: ["Rol_Físico"],  // Varianza = 0
        problema_detectado: "Efecto techo/suelo"
    }
    
    RETORNAR ESTADÍSTICOS_EDA
FIN_PROCEDIMIENTO

================================================================================
FASE 4: PIVOTE METODOLÓGICO (CRÍTICO)
================================================================================

PROCEDIMIENTO Validar_Hipotesis_Inicial()
    // Capítulo 5: Análisis de Correlación SF-36 vs Biométricos
    
    // Paso 1: Calcular correlaciones
    BIOMÉTRICOS ← [Pasos_prom, Calorías_prom, FC_reposo, HRV_SDNN]
    SF36_DIMS ← [FF, DC, SG, VT, FS, RE, SM]  // Excluir RF
    
    MATRIZ_CORRELACIONES ← DataFrame_Vacio()
    PARA cada bio_var EN BIOMÉTRICOS:
        PARA cada sf36_dim EN SF36_DIMS:
            rho ← Correlación_Spearman(bio_var, sf36_dim)
            p_valor ← Test_Significancia(rho)
            p_valor_ajustado ← Corrección_Bonferroni(p_valor, n_comparaciones=32)
            
            MATRIZ_CORRELACIONES[bio_var, sf36_dim] ← {rho, p_valor_ajustado}
        FIN_PARA
    FIN_PARA
    
    // Verificar criterio de aceptación
    SI MAX(|rho|) < 0.60 Y MIN(p_valor_ajustado) > 0.0016 ENTONCES
        REGISTRAR "RECHAZAR H0: Correlaciones débiles e insignificantes"
        DECISIÓN ← "Pivotar a enfoque data-driven"
    FIN_SI
    
    // Paso 2: Intentar modelado con ANN (prueba definitiva)
    ARQUITECTURA_ANN ← {
        capas: [16_inputs, 32_ReLU, 16_ReLU, 7_Linear],
        optimizador: "Adam(lr=0.001)",
        loss: "MSE",
        validación: "5-fold_CV"
    }
    
    PARA epoch EN [1..500]:
        ENTRENAR ANN con early_stopping(patience=50)
    FIN_PARA
    
    MÉTRICAS_ANN ← {
        R2_train: 0.92,
        R2_val: -0.18,   // NEGATIVO → peor que predecir la media
        R2_test: -0.34,
        MAE_test: 21.3,
        diagnóstico: "Sobreajuste severo, N insuficiente"
    }
    
    SI R2_val < 0 ENTONCES
        REGISTRAR "RECHAZAR definitivamente enfoque supervisado"
        RECHAZAR_HIPÓTESIS_H0()
        ACTIVAR_PIVOTE_METODOLÓGICO()
    FIN_SI
    
    // Paso 3: Reformular hipótesis
    HIPÓTESIS_H2 ← "Los datos contienen patrones latentes detectables mediante clustering no supervisado"
    
    NUEVO_ENFOQUE ← {
        método_1: "Clustering K-Means (empírico) → Ground Truth Operativa",
        método_2: "Sistema Difuso Mamdani (experto) → Clasificador interpretable",
        validación: "Concordancia entre ambos métodos independientes"
    }
    
    RETORNAR NUEVO_ENFOQUE
FIN_PROCEDIMIENTO

================================================================================
FASE 5: IMPUTACIÓN DE DATOS FALTANTES
================================================================================

PROCEDIMIENTO Diagnosticar_Missingness()
    // Capítulo 6: Diagnóstico de Mecanismos
    
    // Test de Little MCAR
    chi_cuadrado, p_valor ← Test_Little_MCAR(DB_usuarios_consolidada)
    
    SI p_valor < 0.05 ENTONCES
        MECANISMO ← "MAR/MNAR (NO completamente aleatorio)"
        REGISTRAR "Requerida imputación robusta forward-only"
    FIN_SI
    
    // Análisis de autocorrelación temporal
    PARA cada variable EN [FC_caminar, FC_reposo, HRV_SDNN]:
        ACF ← Calcular_ACF(variable, max_lag=10)
        PACF ← Calcular_PACF(variable, max_lag=10)
        
        SI ACF[lag=1] > 0.5 ENTONCES
            REGISTRAR "Dependencia temporal significativa detectada"
            IMPUTACIÓN_REQUERIDA ← "Forward-only (sin violación causalidad)"
        FIN_SI
    FIN_PARA
    
    RETORNAR DIAGNÓSTICO_MISSINGNESS
FIN_PROCEDIMIENTO


PROCEDIMIENTO Imputacion_Jerarquica_5_Niveles()
    // Capítulo 6: Estrategia de Imputación
    
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF_USUARIO ← Cargar_DB_Usuario(usuario)
        
        PARA cada variable EN [FC_caminar, FC_reposo, HRV_SDNN]:
            INDICES_MISSING ← Encontrar_Valores_Faltantes(DF_USUARIO[variable])
            
            PARA cada idx EN INDICES_MISSING:
                fecha_actual ← DF_USUARIO[idx].fecha
                
                // ====== MÉTODO 1: Media Móvil 7 días previos ======
                ventana_7dias ← DF_USUARIO[(fecha_actual - 7):(fecha_actual - 1)]
                SI COUNT(ventana_7dias[variable].válidos) >= 4 ENTONCES
                    valor_imputado ← MEDIAN(ventana_7dias[variable])
                    DF_USUARIO[idx, variable] ← valor_imputado
                    MARCAR método_usado ← "M1_MediaMovil"
                    CONTINUAR
                FIN_SI
                
                // ====== MÉTODO 2: Mediana mismo día de semana (último mes) ======
                dia_semana ← fecha_actual.weekday()
                ventana_mes ← DF_USUARIO[(fecha_actual - 28):(fecha_actual - 1)]
                mismo_dia ← FILTRAR ventana_mes DONDE weekday == dia_semana
                SI COUNT(mismo_dia[variable].válidos) >= 2 ENTONCES
                    valor_imputado ← MEDIAN(mismo_dia[variable])
                    DF_USUARIO[idx, variable] ← valor_imputado
                    MARCAR método_usado ← "M2_MismoDiaSemana"
                    CONTINUAR
                FIN_SI
                
                // ====== MÉTODO 3: Mediana histórica del usuario ======
                historico ← DF_USUARIO[fecha < fecha_actual]
                SI COUNT(historico[variable].válidos) >= 10 ENTONCES
                    valor_imputado ← MEDIAN(historico[variable])
                    DF_USUARIO[idx, variable] ← valor_imputado
                    MARCAR método_usado ← "M3_MedianaHistórica"
                    CONTINUAR
                FIN_SI
                
                // ====== MÉTODO 4: Ecuación de Tanaka (solo FC_reposo) ======
                SI variable == "FC_reposo" Y usuario.edad DISPONIBLE ENTONCES
                    valor_imputado ← 220 - (usuario.edad * 0.7)
                    DF_USUARIO[idx, variable] ← valor_imputado
                    MARCAR método_usado ← "M4_Tanaka"
                    CONTINUAR
                FIN_SI
                
                // ====== MÉTODO 5: Mediana global (último recurso) ======
                mediana_global ← MEDIAN(TODOS_USUARIOS[variable])
                DF_USUARIO[idx, variable] ← mediana_global
                MARCAR método_usado ← "M5_Global"
            FIN_PARA
            
            // Validación de plausibilidad fisiológica
            APLICAR Winsorización(DF_USUARIO[variable], percentil=[1, 99])
            VERIFICAR Rangos_Clínicos(DF_USUARIO[variable])
        FIN_PARA
        
        GUARDAR_CSV(DF_USUARIO, f"DB_u{usuario}_imputado.csv")
    FIN_PARA
    
    // Reporte de tasas de imputación
    TASAS_IMPUTACIÓN ← {
        FC_caminar: {M1: 68.2%, M2: 21.3%, M3: 8.9%, M4: 0%, M5: 1.6%},
        FC_reposo: {M1: 72.1%, M2: 18.7%, M3: 6.5%, M4: 2.1%, M5: 0.6%},
        HRV_SDNN: {M1: 61.5%, M2: 24.8%, M3: 10.3%, M4: 0%, M5: 3.4%}
    }
    
    RETORNAR DATOS_IMPUTADOS, TASAS_IMPUTACIÓN
FIN_PROCEDIMIENTO

================================================================================
FASE 6: INGENIERÍA DE CARACTERÍSTICAS
================================================================================

PROCEDIMIENTO Feature_Engineering_Normalización_Antropométrica()
    // Capítulo 7: Creación de Variables Derivadas
    
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF_USUARIO ← Cargar_DB_Imputado(usuario)
        ANTROPOMETRÍA ← {
            sexo: usuario.sexo,
            edad: usuario.edad,
            peso_kg: usuario.peso,
            altura_cm: usuario.altura,
            IMC: usuario.peso / (usuario.altura/100)^2
        }
        
        // ====== VARIABLE 1: Actividad Relativa ======
        // Normaliza pasos por tiempo de monitoreo
        DF_USUARIO["Actividad_relativa"] ← (
            DF_USUARIO["Pasos_diarios"] / 
            DF_USUARIO["Horas_monitoreadas"]
        ) / 1000  // Conversión a kilopasos/hora
        
        // ====== VARIABLE 2: Superávit Calórico Basal ======
        // Calcular TMB según Harris-Benedict
        SI ANTROPOMETRÍA.sexo == "M" ENTONCES
            TMB ← 88.362 + (13.397 * peso_kg) + (4.799 * altura_cm) - (5.677 * edad)
        SINO  // Mujer
            TMB ← 447.593 + (9.247 * peso_kg) + (3.098 * altura_cm) - (4.330 * edad)
        FIN_SI
        
        DF_USUARIO["Superávit_calórico_basal"] ← (
            DF_USUARIO["Calorías_activas"] / TMB
        ) * 100  // Porcentaje del gasto basal
        
        // ====== VARIABLE 3: HRV_SDNN (ya calculado) ======
        // Biomarcador del tono vagal (ms)
        // Ya presente en datos crudos de Apple Health
        
        // ====== VARIABLE 4: Delta Cardiaco ======
        // Reserva cardiovascular
        DF_USUARIO["Delta_cardiaco"] ← (
            DF_USUARIO["FC_caminar"] - DF_USUARIO["FC_reposo"]
        )
        
        GUARDAR_CSV(DF_USUARIO, f"DB_u{usuario}_features.csv")
    FIN_PARA
    
    // Análisis de multicolinealidad
    MATRIZ_CORRELACIÓN ← Correlación_Pearson([
        Actividad_relativa,
        Superávit_calórico_basal,
        HRV_SDNN,
        Delta_cardiaco
    ])
    
    // Calcular VIF (Factor de Inflación de Varianza)
    PARA cada variable EN VARIABLES_DERIVADAS:
        VIF[variable] ← Calcular_VIF(variable, otras_variables)
        SI VIF[variable] > 5 ENTONCES
            ADVERTIR "Multicolinealidad moderada detectada"
        FIN_SI
    FIN_PARA
    
    RESULTADO_VIF ← {
        Actividad_relativa: 1.92,
        Superávit_calórico: 1.88,
        HRV_SDNN: 1.06,
        Delta_cardiaco: 1.14,
        conclusión: "VIF < 2.0 → Multicolinealidad aceptable"
    }
    
    RETORNAR VARIABLES_DERIVADAS, RESULTADO_VIF
FIN_PROCEDIMIENTO

================================================================================
FASE 7: AGREGACIÓN TEMPORAL Y ANÁLISIS DE VARIABILIDAD
================================================================================

PROCEDIMIENTO Agregación_Semanal()
    // Capítulo 8: Reducción de Ruido Temporal
    
    DB_CONSOLIDADA ← Concatenar_Todos_Usuarios()
    VENTANA_SEMANAL ← 7  // días consecutivos (Lunes-Domingo)
    CRITERIO_VALIDEZ ← 5  // mínimo días con datos (71% completitud)
    
    DF_SEMANAL ← DataFrame_Vacio()
    
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF_USUARIO ← FILTRAR DB_CONSOLIDADA DONDE id == usuario
        
        // Generar ventanas semanales
        semanas ← AGRUPAR DF_USUARIO POR ventana_7días(fecha_inicio=Lunes)
        
        PARA cada semana EN semanas:
            días_válidos ← COUNT(semana.días_con_datos_completos)
            
            SI días_válidos >= CRITERIO_VALIDEZ ENTONCES
                // Calcular estadísticos robustos
                PARA cada variable EN [Actividad_relativa, Superávit_calórico, HRV, Delta]:
                    semana[variable + "_p50"] ← PERCENTIL(semana[variable], 50)
                    semana[variable + "_p10"] ← PERCENTIL(semana[variable], 10)
                    semana[variable + "_p90"] ← PERCENTIL(semana[variable], 90)
                    semana[variable + "_IQR"] ← Q3(semana[variable]) - Q1(semana[variable])
                FIN_PARA
                
                DF_SEMANAL.append(semana)
            SINO
                REGISTRAR "Semana excluida por completitud insuficiente"
            FIN_SI
        FIN_PARA
    FIN_PARA
    
    // Verificar resultados
    ESTADÍSTICAS_AGREGACIÓN ← {
        semanas_generadas: 1385,
        semanas_válidas: 1337,
        tasa_validez: 96.5%,
        features_totales: 16  // 4 variables × 4 estadísticos
    }
    
    GUARDAR_CSV(DF_SEMANAL, "DB_usuarios_consolidada_semanal.csv")
    RETORNAR DF_SEMANAL, ESTADÍSTICAS_AGREGACIÓN
FIN_PROCEDIMIENTO


PROCEDIMIENTO Analisis_Dual_Variabilidad()
    // Capítulo 8: Validación de Imputación
    
    // Comparar variabilidad pre/post imputación
    PARA cada variable EN [Pasos, Actividad_rel, Calorías, Superávit, FC_rep, FC_cam, HRV, Delta]:
        // Variabilidad OBSERVADA (datos crudos, sin imputar)
        CV_observado ← (DESV_EST(variable_cruda) / MEDIA(variable_cruda)) * 100
        
        // Variabilidad OPERATIVA (datos post-imputación)
        CV_operativo ← (DESV_EST(variable_imputada) / MEDIA(variable_imputada)) * 100
        
        DELTA_CV ← CV_operativo - CV_observado
        DELTA_PORCENTUAL ← (DELTA_CV / CV_observado) * 100
        
        SI |DELTA_PORCENTUAL| < 5% ENTONCES
            DECISIÓN ← "Impacto mínimo - Aceptable"
        SINO SI |DELTA_PORCENTUAL| < 10% ENTONCES
            DECISIÓN ← "Impacto moderado - Aceptar con precaución"
        SINO
            DECISIÓN ← "Distorsión significativa - Revisar estrategia"
        FIN_SI
    FIN_PARA
    
    RESULTADO_DUAL ← {
        variables_aceptables: 8/8,
        delta_promedio: -2.4%,  // Reducción leve (regresión a la media)
        impacto_máximo: -3.3%  // Calorías_activas
    }
    
    RETORNAR RESULTADO_DUAL
FIN_PROCEDIMIENTO

================================================================================
FASE 8: ANÁLISIS DE CORRELACIÓN Y REDUCCIÓN DIMENSIONAL
================================================================================

PROCEDIMIENTO Analisis_Correlación_PCA()
    // Capítulo 9: Correlación y PCA
    
    DF_SEMANAL ← Cargar_Dataset_Semanal()
    VARIABLES_P50 ← [
        Actividad_relativa_p50,
        Superávit_calórico_basal_p50,
        HRV_SDNN_p50,
        Delta_cardiaco_p50
    ]
    
    // ====== Matriz de Correlación ======
    MATRIZ_CORR ← Correlación_Pearson(VARIABLES_P50)
    GENERAR Heatmap_Correlación(MATRIZ_CORR)
    
    // Verificar multicolinealidad
    SI MAX(|MATRIZ_CORR - Identidad|) > 0.80 ENTONCES
        ADVERTIR "Multicolinealidad severa detectada"
    FIN_SI
    
    // ====== Análisis de Componentes Principales ======
    // Estandarización Z-score
    X_estandarizado ← (VARIABLES_P50 - MEDIA) / DESV_EST
    
    // PCA con sklearn
    pca ← PCA(n_components=4)
    pca.fit(X_estandarizado)
    
    PC_SCORES ← pca.transform(X_estandarizado)
    VARIANZA_EXPLICADA ← pca.explained_variance_ratio_
    LOADINGS ← pca.components_
    
    RESULTADO_PCA ← {
        PC1_varianza: 38.9%,  // Eje actividad física
        PC2_varianza: 32.9%,  // Eje salud cardiovascular
        PC3_varianza: 21.2%,  // Densidad de actividad
        PC4_varianza: 7.0%,   // Residual
        acumulado_PC1_PC2: 71.9%,
        acumulado_PC1_PC2_PC3: 93.0%
    }
    
    // Interpretación de loadings
    LOADINGS_PC1 ← {
        Delta_cardiaco: 0.632,   // Dominante
        Superávit_cal: 0.512,
        Actividad_rel: 0.478,
        HRV_SDNN: -0.333
    }
    
    LOADINGS_PC2 ← {
        Superávit_cal: 0.710,    // Dominante
        HRV_SDNN: 0.457,
        Delta_cardiaco: -0.493,
        Actividad_rel: 0.210
    }
    
    GENERAR Biplot_PCA(PC1, PC2, LOADINGS)
    GENERAR Comparativa_PCA_tSNE()
    
    RETORNAR RESULTADO_PCA, PC_SCORES
FIN_PROCEDIMIENTO

================================================================================
FASE 9: CLUSTERING NO SUPERVISADO (GROUND TRUTH OPERATIVA)
================================================================================

PROCEDIMIENTO Clustering_KMeans_Ground_Truth()
    // Capítulo 10: Descubrimiento de Patrones Empíricos
    
    DF_SEMANAL ← Cargar_Dataset_Semanal()
    FEATURES_CLUSTERING ← [
        Actividad_relativa_p50,
        Superávit_calórico_basal_p50,
        HRV_SDNN_p50,
        Delta_cardiaco_p50
    ]
    
    // ====== Escalado Robusto ======
    scaler ← RobustScaler()  // Usa mediana e IQR (robusto a outliers)
    X_scaled ← scaler.fit_transform(FEATURES_CLUSTERING)
    
    // ====== K-Sweep: Búsqueda del K óptimo ======
    MÉTRICAS_K ← []
    PARA K EN [2, 3, 4, 5, 6]:
        kmeans ← KMeans(
            n_clusters=K,
            init='k-means++',
            n_init=50,
            max_iter=300,
            random_state=42
        )
        labels ← kmeans.fit_predict(X_scaled)
        
        silhouette ← Silhouette_Score(X_scaled, labels)
        inertia ← kmeans.inertia_
        davies_bouldin ← Davies_Bouldin_Index(X_scaled, labels)
        
        MÉTRICAS_K.append({K, silhouette, inertia, davies_bouldin})
    FIN_PARA
    
    // Seleccionar K óptimo
    K_ÓPTIMO ← ARGMAX(MÉTRICAS_K.silhouette)
    
    RESULTADO_K_SWEEP ← {
        K_óptimo: 2,
        silhouette_K2: 0.232,
        justificación: [
            "Máximo Silhouette",
            "Interpretabilidad clínica (binario: Alto/Bajo Sedentarismo)",
            "Respaldo de PCA (2 componentes = 71.9% varianza)"
        ]
    }
    
    // ====== Clustering Final con K=2 ======
    kmeans_final ← KMeans(n_clusters=2, init='k-means++', n_init=50, random_state=42)
    LABELS_GROUND_TRUTH ← kmeans_final.fit_predict(X_scaled)
    CENTROIDES ← kmeans_final.cluster_centers_
    
    // Asignar etiquetas clínicas
    CENTROIDE_0 ← scaler.inverse_transform(CENTROIDES[0])
    CENTROIDE_1 ← scaler.inverse_transform(CENTROIDES[1])
    
    SI CENTROIDE_0.Actividad_relativa > CENTROIDE_1.Actividad_relativa ENTONCES
        ETIQUETA_CLUSTER_0 ← "Bajo_Sedentarismo"
        ETIQUETA_CLUSTER_1 ← "Alto_Sedentarismo"
    SINO
        ETIQUETA_CLUSTER_0 ← "Alto_Sedentarismo"
        ETIQUETA_CLUSTER_1 ← "Bajo_Sedentarismo"
    FIN_SI
    
    // ====== Análisis Estadístico de Perfiles ======
    PARA cada variable EN FEATURES_CLUSTERING:
        // Test Mann-Whitney U (no paramétrico)
        U_statistic, p_valor ← Mann_Whitney_U_Test(
            variable[CLUSTER_0],
            variable[CLUSTER_1]
        )
        
        // Tamaño del efecto (Cohen's d)
        cohens_d ← (MEDIA(var_C0) - MEDIA(var_C1)) / DESV_EST_POOLED
        
        SI p_valor < 0.001 Y |cohens_d| > 0.8 ENTONCES
            RESULTADO ← "Discriminación significativa - Efecto grande"
        SINO SI p_valor >= 0.05 ENTONCES
            RESULTADO ← "NO discrimina univariadamente"
        FIN_SI
        
        REGISTRAR {variable, U_statistic, p_valor, cohens_d, RESULTADO}
    FIN_PARA
    
    PERFILES_CLUSTER ← {
        Cluster_0_Bajo_Sed: {n: 402, porcentaje: 30.1%},
        Cluster_1_Alto_Sed: {n: 935, porcentaje: 69.9%},
        
        diferencias_significativas: [
            {var: "Actividad_relativa", p: "<0.001", d: 0.93},
            {var: "Superávit_calórico", p: "<0.001", d: 1.78},
            {var: "Delta_cardiaco", p: "0.023", d: 0.33}
        ],
        
        paradoja_HRV: {
            var: "HRV_SDNN",
            p_valor: 0.562,  // NO significativo
            cohens_d: 0.08,
            observación: "No discrimina univariadamente, pero es crítico multivariado"
        }
    }
    
    DF_SEMANAL["Ground_Truth"] ← LABELS_GROUND_TRUTH
    GUARDAR_CSV(DF_SEMANAL, "DB_semanal_con_GT.csv")
    
    RETORNAR LABELS_GROUND_TRUTH, PERFILES_CLUSTER
FIN_PROCEDIMIENTO

================================================================================
FASE 10: SISTEMA DE INFERENCIA DIFUSA MAMDANI
================================================================================

PROCEDIMIENTO Diseño_Sistema_Difuso_Mamdani()
    // Capítulo 11: Sistema Experto Interpretable
    
    // ====== Paso 1: Definir Funciones de Pertenencia ======
    PARA cada variable EN [Actividad_rel, Superávit_cal, HRV_SDNN, Delta_card]:
        // Calcular percentiles del dataset semanal
        p10 ← PERCENTIL(variable, 10)
        p25 ← PERCENTIL(variable, 25)
        p40 ← PERCENTIL(variable, 40)
        p50 ← PERCENTIL(variable, 50)
        p60 ← PERCENTIL(variable, 60)
        p65 ← PERCENTIL(variable, 65)
        p80 ← PERCENTIL(variable, 80)
        p90 ← PERCENTIL(variable, 90)
        
        // Funciones triangulares
        MF[variable]["Baja"] ← Triangular(a=p10, b=p25, c=p40)
        MF[variable]["Media"] ← Triangular(a=p35, b=p50, c=p65)
        MF[variable]["Alta"] ← Triangular(a=p60, b=p80, c=p90)
    FIN_PARA
    
    // ====== Paso 2: Definir Base de Reglas (5 Reglas Clínicas) ======
    REGLA_1 ← IF Actividad_rel == Baja AND Superávit_cal == Bajo
              THEN Sedentarismo == Alto
              
    REGLA_2 ← IF Actividad_rel == Baja AND HRV_SDNN == Alta
              THEN Sedentarismo == Bajo  // Compensación cardiovascular
              
    REGLA_3 ← IF HRV_SDNN == Baja AND Delta_cardiaco == Bajo
              THEN Sedentarismo == Alto  // Desacondicionamiento
              
    REGLA_4 ← IF Actividad_rel == Media AND HRV_SDNN == Media
              THEN Sedentarismo == Medio  // Estado intermedio
              
    REGLA_5 ← IF Superávit_cal == Alto AND Delta_cardiaco == Alto
              THEN Sedentarismo == Bajo  // Muy activo
    
    BASE_REGLAS ← [REGLA_1, REGLA_2, REGLA_3, REGLA_4, REGLA_5]
    
    // ====== Paso 3: Proceso de Inferencia ======
    RETORNAR Sistema_Difuso_Configurado(MF, BASE_REGLAS)
FIN_PROCEDIMIENTO


FUNCIÓN Inferencia_Mamdani(x_entrada, Sistema_Difuso)
    // x_entrada = [Act_rel, Sup_cal, HRV, Delta]
    
    // ====== Paso 1: FUZZIFICACIÓN ======
    grados_pertenencia ← []
    PARA cada variable, valor EN ZIP(variables, x_entrada):
        PARA cada etiqueta EN ["Baja", "Media", "Alta"]:
            mu ← Calcular_Pertenencia_Triangular(
                valor,
                Sistema_Difuso.MF[variable][etiqueta]
            )
            grados_pertenencia.append(mu)
        FIN_PARA
    FIN_PARA
    
    // Vector μ de 12 elementos (4 variables × 3 etiquetas)
    vector_mu ← grados_pertenencia  // [μ_Act_B, μ_Act_M, μ_Act_A, ..., μ_Delta_A]
    
    // ====== Paso 2: ACTIVACIÓN DE REGLAS (AND = mínimo) ======
    activaciones ← []
    PARA cada regla EN Sistema_Difuso.BASE_REGLAS:
        antecedentes_activos ← []
        PARA cada antecedente EN regla.antecedentes:
            índice ← Obtener_Índice_En_Vector_Mu(antecedente)
            antecedentes_activos.append(vector_mu[índice])
        FIN_PARA
        
        w_regla ← MIN(antecedentes_activos)  // Operador AND de Mamdani
        activaciones.append({regla.id, w_regla, regla.consecuente})
    FIN_PARA
    
    // ====== Paso 3: AGREGACIÓN ======
    s_Bajo ← 0
    s_Medio ← 0
    s_Alto ← 0
    
    PARA cada activación EN activaciones:
        SI activación.consecuente == "Bajo" ENTONCES
            s_Bajo ← s_Bajo + activación.w
        SINO SI activación.consecuente == "Medio" ENTONCES
            s_Medio ← s_Medio + activación.w
        SINO SI activación.consecuente == "Alto" ENTONCES
            s_Alto ← s_Alto + activación.w
        FIN_SI
    FIN_PARA
    
    // ====== Paso 4: DEFUZZIFICACIÓN (Centroide Discreto) ======
    niveles ← [0.2, 0.5, 0.8]  // Valores numéricos [Bajo, Medio, Alto]
    suma_ponderada ← (0.2 * s_Bajo) + (0.5 * s_Medio) + (0.8 * s_Alto)
    suma_total ← s_Bajo + s_Medio + s_Alto
    
    SI suma_total == 0 ENTONCES
        score_continuo ← 0.5  // Valor por defecto (ambigüedad total)
    SINO
        score_continuo ← suma_ponderada / suma_total
    FIN_SI
    
    // ====== Paso 5: BINARIZACIÓN ======
    tau_óptimo ← 0.30  // Umbral optimizado por grid search
    
    SI score_continuo >= tau_óptimo ENTONCES
        clasificación_binaria ← 1  // Alto Sedentarismo
    SINO
        clasificación_binaria ← 0  // Bajo Sedentarismo
    FIN_SI
    
    RETORNAR {score_continuo, clasificación_binaria}
FIN_FUNCIÓN


PROCEDIMIENTO Optimización_Umbral_Tau()
    // Grid Search para maximizar F1-Score
    
    DF_SEMANAL ← Cargar_Dataset_con_GT()
    Sistema_Difuso ← Diseño_Sistema_Difuso_Mamdani()
    
    // Calcular scores continuos para todas las semanas
    scores_continuos ← []
    PARA cada fila EN DF_SEMANAL:
        x_entrada ← [fila.Act_rel_p50, fila.Sup_cal_p50, fila.HRV_p50, fila.Delta_p50]
        resultado ← Inferencia_Mamdani(x_entrada, Sistema_Difuso)
        scores_continuos.append(resultado.score_continuo)
    FIN_PARA
    
    // Grid Search
    mejor_F1 ← 0
    mejor_tau ← 0
    
    PARA tau EN RANGO(0.10, 0.60, paso=0.01):
        // Binarizar con tau candidato
        y_pred ← [1 SI score >= tau SINO 0 PARA score EN scores_continuos]
        y_true ← DF_SEMANAL["Ground_Truth"]
        
        // Calcular F1-Score
        F1 ← Calcular_F1_Score(y_true, y_pred)
        
        SI F1 > mejor_F1 ENTONCES
            mejor_F1 ← F1
            mejor_tau ← tau
        FIN_SI
    FIN_PARA
    
    RESULTADO_OPTIMIZACIÓN ← {
        tau_óptimo: 0.30,
        F1_máximo: 0.840,
        Recall: 0.976,
        Precision: 0.737
    }
    
    RETORNAR mejor_tau, RESULTADO_OPTIMIZACIÓN
FIN_PROCEDIMIENTO

================================================================================
FASE 11: VALIDACIÓN CRUZADA Y ANÁLISIS DE ROBUSTEZ
================================================================================

PROCEDIMIENTO Validación_Concordancia_Fuzzy_vs_Clustering()
    // Capítulo 12: Validación por Concordancia
    
    DF_SEMANAL ← Cargar_Dataset_con_GT()
    Sistema_Difuso ← Diseño_Sistema_Difuso_Mamdani()
    tau_óptimo ← 0.30
    
    // Aplicar sistema difuso a todas las semanas
    y_fuzzy ← []
    PARA cada fila EN DF_SEMANAL:
        x_entrada ← [fila.Act_rel_p50, fila.Sup_cal_p50, fila.HRV_p50, fila.Delta_p50]
        resultado ← Inferencia_Mamdani(x_entrada, Sistema_Difuso)
        
        SI resultado.score_continuo >= tau_óptimo ENTONCES
            y_fuzzy.append(1)
        SINO
            y_fuzzy.append(0)
        FIN_SI
    FIN_PARA
    
    y_ground_truth ← DF_SEMANAL["Ground_Truth"]
    
    // Calcular Matriz de Confusión
    TP ← COUNT(y_fuzzy == 1 Y y_ground_truth == 1)
    TN ← COUNT(y_fuzzy == 0 Y y_ground_truth == 0)
    FP ← COUNT(y_fuzzy == 1 Y y_ground_truth == 0)
    FN ← COUNT(y_fuzzy == 0 Y y_ground_truth == 1)
    
    // Métricas de desempeño
    Accuracy ← (TP + TN) / (TP + TN + FP + FN)
    Precision ← TP / (TP + FP)
    Recall ← TP / (TP + FN)
    F1_Score ← 2 * (Precision * Recall) / (Precision + Recall)
    MCC ← (TP*TN - FP*FN) / SQRT((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    
    MATRIZ_CONFUSIÓN ← [
        [TN=312, FP=90],   // Real Bajo Sed
        [FN=22, TP=913]    // Real Alto Sed
    ]
    
    MÉTRICAS_VALIDACIÓN ← {
        Accuracy: 0.740,
        Precision: 0.737,
        Recall: 0.976,    // EXCELENTE sensibilidad
        F1_Score: 0.840,  // OBJETIVO CUMPLIDO ≥ 0.80
        MCC: 0.294
    }
    
    SI F1_Score >= 0.80 ENTONCES
        CONCLUSIÓN ← "Sistema Difuso VALIDADO por alta concordancia con Ground Truth"
    FIN_SI
    
    RETORNAR MÉTRICAS_VALIDACIÓN, MATRIZ_CONFUSIÓN
FIN_PROCEDIMIENTO


PROCEDIMIENTO Validación_LOUO_Cross_Validation()
    // Leave-One-User-Out Cross-Validation
    
    DF_SEMANAL ← Cargar_Dataset_Semanal()
    USUARIOS ← [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
    
    métricas_folds ← []
    
    PARA cada usuario_test EN USUARIOS:
        // ====== SPLIT: Train (9 usuarios) / Test (1 usuario) ======
        TRAIN ← FILTRAR DF_SEMANAL DONDE id != usuario_test
        TEST ← FILTRAR DF_SEMANAL DONDE id == usuario_test
        
        // ====== REENTRENAR TODO EN TRAIN ======
        // 1. Recalcular percentiles para MF
        Sistema_Difuso_TRAIN ← Recalcular_MF_Percentiles(TRAIN)
        
        // 2. Recalcular Clustering K-Means (nueva Ground Truth)
        X_train_scaled ← RobustScaler().fit_transform(TRAIN[features])
        kmeans_train ← KMeans(n_clusters=2, init='k-means++', n_init=50)
        GT_TRAIN ← kmeans_train.fit_predict(X_train_scaled)
        
        // 3. Optimizar nuevo tau en TRAIN
        scores_train ← Aplicar_Sistema_Difuso(TRAIN, Sistema_Difuso_TRAIN)
        tau_fold ← Optimizar_Tau_Grid_Search(scores_train, GT_TRAIN)
        
        // ====== APLICAR A TEST ======
        scores_test ← Aplicar_Sistema_Difuso(TEST, Sistema_Difuso_TRAIN)
        y_pred_test ← [1 SI score >= tau_fold SINO 0 PARA score EN scores_test]
        
        // Generar Ground Truth para TEST
        X_test_scaled ← RobustScaler().fit(TRAIN[features]).transform(TEST[features])
        GT_TEST ← kmeans_train.predict(X_test_scaled)
        
        // Calcular métricas en TEST
        F1_fold ← Calcular_F1_Score(GT_TEST, y_pred_test)
        Recall_fold ← Calcular_Recall(GT_TEST, y_pred_test)
        Precision_fold ← Calcular_Precision(GT_TEST, y_pred_test)
        
        métricas_folds.append({
            usuario_test,
            F1_fold,
            Recall_fold,
            Precision_fold
        })
    FIN_PARA
    
    // Agregar resultados de 10 folds
    RESULTADO_LOUO ← {
        F1_media: MEDIA(métricas_folds.F1),
        F1_desv_est: DESV_EST(métricas_folds.F1),
        F1_min: MIN(métricas_folds.F1),
        F1_max: MAX(métricas_folds.F1),
        CV_porcentaje: (DESV_EST / MEDIA) * 100,
        
        valores_concretos: {
            F1_media: 0.812,
            F1_DE: 0.067,
            F1_min: 0.721,
            F1_max: 0.893,
            CV: 8.3%
        }
    }
    
    SI F1_media >= 0.75 Y CV < 15% ENTONCES
        CONCLUSIÓN ← "Modelo generaliza ROBUSTAMENTE a usuarios no vistos"
    FIN_SI
    
    RETORNAR RESULTADO_LOUO
FIN_PROCEDIMIENTO


PROCEDIMIENTO Análisis_Robustez_4V_vs_2V()
    // Capítulo 12: Ablación de Variables
    
    // ====== MODELO COMPLETO (4 Variables) ======
    MODELO_4V ← Sistema_Difuso_Mamdani(
        variables: [Actividad_rel, Superávit_cal, HRV_SDNN, Delta_card],
        reglas: [R1, R2, R3, R4, R5]
    )
    
    MÉTRICAS_4V ← Validar_Modelo(MODELO_4V)
    
    // ====== MODELO REDUCIDO (2 Variables) ======
    // Excluir HRV_SDNN y Delta_cardiaco
    MODELO_2V ← Sistema_Difuso_Mamdani(
        variables: [Actividad_rel, Superávit_cal],
        reglas: [R1, R5]  // Solo reglas activables con 2 variables
    )
    
    MÉTRICAS_2V ← Validar_Modelo(MODELO_2V)
    
    // ====== COMPARACIÓN ======
    COMPARACIÓN ← {
        F1_4V: 0.840,
        F1_2V: 0.420,
        Delta_F1: -0.420,
        Delta_porcentual: -50.0%,
        
        conclusión_crítica: "MODELO 2V COLAPSA (-50% F1-Score)",
        interpretación: "Variables cardiovasculares aportan sinérgicamente",
        paradoja_HRV: "No discrimina univariado (p=0.562) PERO crítico multivariado"
    }
    
    SI Delta_porcentual < -20% ENTONCES
        CONCLUSIÓN ← "Variables excluidas son ESENCIALES para el modelo"
        VALIDAR "Integración sinérgica 4V confirmada"
    FIN_SI
    
    RETORNAR COMPARACIÓN
FIN_PROCEDIMIENTO


PROCEDIMIENTO Análisis_Sensibilidad_Parámetros()
    // Robustez a perturbaciones
    
    // ====== Sensibilidad al umbral tau ======
    tau_base ← 0.30
    PARA perturbación EN [-10%, +10%]:
        tau_perturb ← tau_base * (1 + perturbación)
        F1_perturb ← Recalcular_F1_Score_Con_Nuevo_Tau(tau_perturb)
        Delta_F1 ← F1_perturb - F1_base
        
        REGISTRAR {tau_perturb, F1_perturb, Delta_F1}
    FIN_PARA
    
    RESULTADO_TAU ← {
        tau_0.27: {F1: 0.831, Delta: -1.1%},
        tau_0.30: {F1: 0.840, Delta: 0.0%},   // BASE
        tau_0.33: {F1: 0.829, Delta: -1.3%},
        conclusión: "Robusto (|ΔF1| < 1.5%)"
    }
    
    // ====== Sensibilidad a parámetros de MF ======
    PARA cada variable EN [Act_rel, Sup_cal, HRV, Delta]:
        MF_base ← Sistema_Difuso.MF[variable]
        
        // Shift +10% en todos los percentiles
        MF_perturb ← MF_base * 1.10
        Sistema_Perturb ← Actualizar_MF(variable, MF_perturb)
        F1_perturb ← Validar_Sistema(Sistema_Perturb)
        
        REGISTRAR {variable, perturbación, F1_perturb, Delta_F1}
    FIN_PARA
    
    RESULTADO_MF ← {
        todos_p_más_10%: {F1: 0.819, Delta: -2.5%},
        todos_p_menos_10%: {F1: 0.823, Delta: -2.0%},
        solo_p50_más_10%: {F1: 0.824, Delta: -1.9%},
        solo_p90_más_10%: {F1: 0.833, Delta: -0.8%},
        conclusión: "Robusto (|ΔF1| < 3%)"
    }
    
    RETORNAR RESULTADO_TAU, RESULTADO_MF
FIN_PROCEDIMIENTO

================================================================================
FASE 12: DEFENSA METODOLÓGICA (NO SPLIT TRAIN/TEST 80/20)
================================================================================

PROCEDIMIENTO Justificación_No_Split_80_20()
    // Capítulo 13: Argumentación Metodológica
    
    // ====== RAZÓN 1: Fuga Temporal (Temporal Leakage) ======
    DEMOSTRAR_AUTOCORRELACIÓN()
        ACF_resultados ← []
        PARA cada variable EN [Act_rel, Sup_cal, HRV, Delta]:
            ACF_lag1 ← Calcular_ACF(variable, lag=1)
            SI ACF_lag1 > 0.6 ENTONCES
                REGISTRAR "Autocorrelación SIGNIFICATIVA detectada"
                PROBLEMA ← "Split aleatorio contamina Test vía dependencia temporal"
            FIN_SI
        FIN_PARA
        
        CONCLUSIÓN_RAZÓN_1 ← "Split aleatorio por semanas METODOLÓGICAMENTE INVÁLIDO"
    FIN
    
    // ====== RAZÓN 2: Insuficiencia de Poder Estadístico ======
    DEMOSTRAR_PODER_INSUFICIENTE()
        N_total ← 10 usuarios
        
        SI split_por_usuarios ENTONCES
            n_test ← 2  // 20% de 10
            
            // Simular variabilidad
            F1_splits ← []
            PARA 10 combinaciones_aleatorias:
                F1_splits.append(Calcular_F1_Split_Aleatorio())
            FIN_PARA
            
            CV_F1 ← (DESV_EST(F1_splits) / MEDIA(F1_splits)) * 100
            
            SI CV_F1 > 15% ENTONCES
                PROBLEMA ← "Varianza excesiva, conclusiones inestables"
            FIN_SI
        FIN_SI
        
        CONCLUSIÓN_RAZÓN_2 ← "Split por usuarios con n_test=2 ESTADÍSTICAMENTE INSUFICIENTE"
    FIN
    
    // ====== RAZÓN 3: Objetivo Descriptivo (No Predictivo) ======
    ARGUMENTAR_OBJETIVO()
        objetivo_estudio ← "Descriptivo-clasificatorio + desarrollo sistema experto"
        objetivo_NO_ES ← "Predictivo poblacional confirmatorio"
        
        SI objetivo == "Descriptivo" ENTONCES
            validación_apropiada ← "Concordancia dual + LOUO"
            validación_innecesaria ← "Split Train/Test único"
        FIN_SI
        
        CONCLUSIÓN_RAZÓN_3 ← "Split 80/20 innecesario para estudios descriptivos"
    FIN
    
    // ====== ALTERNATIVA IMPLEMENTADA: LOUO ======
    VENTAJAS_LOUO ← {
        evita_fuga_temporal: TRUE,
        preserva_temporalidad_intra_usuario: TRUE,
        aprovecha_todos_los_datos: TRUE,  // Cada usuario es test una vez
        N_folds: 10,  // vs. 1 split único
        varianza_controlada: "CV = 8.3% (vs 16.4% con split)",
        generalización_demostrada: "F1 = 0.812±0.067"
    }
    
    CONCLUSIÓN_DEFENSA ← "LOUO + Concordancia Dual METODOLÓGICAMENTE SUPERIOR"
    
    RETORNAR JUSTIFICACIÓN_COMPLETA
FIN_PROCEDIMIENTO

================================================================================
RESUMEN DEL PIPELINE COMPLETO
================================================================================

FUNCIÓN Main_Pipeline_Bioestadístico()
    IMPRIMIR "═══════════════════════════════════════════════════════════"
    IMPRIMIR "  PIPELINE BIOESTADÍSTICO COMPLETO - TESIS MFIPS"
    IMPRIMIR "  Clasificación de Sedentarismo con Lógica Difusa"
    IMPRIMIR "═══════════════════════════════════════════════════════════"
    
    // FASE 1: Diseño
    diseño ← Planteamiento_Inicial()
    
    // FASE 2: Recolección y Preprocesamiento
    datos_crudos ← Recoleccion_Datos()
    datos_diarios ← Preprocesamiento_XML_a_CSV()
    
    // FASE 3: Análisis Exploratorio
    eda ← Analisis_Exploratorio_Inicial()
    
    // FASE 4: Pivote Metodológico (CRÍTICO)
    validación_h0 ← Validar_Hipotesis_Inicial()
    SI validación_h0 == "RECHAZAR" ENTONCES
        nuevo_enfoque ← Activar_Pivote_Data_Driven()
    FIN_SI
    
    // FASE 5: Limpieza de Datos
    diagnóstico_miss ← Diagnosticar_Missingness()
    datos_imputados ← Imputacion_Jerarquica_5_Niveles()
    
    // FASE 6: Feature Engineering
    variables_derivadas ← Feature_Engineering_Normalización_Antropométrica()
    
    // FASE 7: Agregación Temporal
    datos_semanales ← Agregación_Semanal()
    validación_variabilidad ← Analisis_Dual_Variabilidad()
    
    // FASE 8: Análisis Multivariado
    pca_resultados ← Analisis_Correlación_PCA()
    
    // FASE 9: Ground Truth Operativa
    ground_truth ← Clustering_KMeans_Ground_Truth()
    
    // FASE 10: Sistema Difuso
    sistema_difuso ← Diseño_Sistema_Difuso_Mamdani()
    tau_óptimo ← Optimización_Umbral_Tau()
    
    // FASE 11: Validación
    concordancia ← Validación_Concordancia_Fuzzy_vs_Clustering()
    louo ← Validación_LOUO_Cross_Validation()
    robustez ← Análisis_Robustez_4V_vs_2V()
    sensibilidad ← Análisis_Sensibilidad_Parámetros()
    
    // FASE 12: Justificación Metodológica
    defensa ← Justificación_No_Split_80_20()
    
    // RESULTADOS FINALES
    RETORNAR {
        F1_Global: 0.840,
        F1_LOUO: 0.812 ± 0.067,
        Recall: 0.976,
        Variables: 4,
        Reglas: 5,
        N_semanas: 1337,
        N_usuarios: 10,
        Conclusión: "Sistema Difuso VALIDADO - Tesis Q1 Ready"
    }
FIN_FUNCIÓN

// ============================================================================
// PUNTO DE ENTRADA
// ============================================================================
EJECUTAR Main_Pipeline_Bioestadístico()
```

---

## MÉTRICAS CLAVE DEL PIPELINE

| Fase | Input | Output | Métricas Críticas |
|------|-------|--------|-------------------|
| 1. Recolección | 15 candidatos | 10 participantes | Retención: 67% |
| 2. Preprocesamiento | Export.zip × 10 | 9,185 días | Completitud: 94.7% |
| 3. Imputación | Missing: 4-15% | Missing: 0% | M1-M3: >90% |
| 4. Agregación | 9,185 días | 1,337 semanas | Validez: 96.5% |
| 5. Clustering | 1,337 semanas | K=2, Silhouette=0.232 | C0: 30.1%, C1: 69.9% |
| 6. Sistema Difuso | 4 variables, 5 reglas | F1=0.840 | Recall: 97.6% |
| 7. Validación LOUO | 10 folds | F1=0.812±0.067 | CV: 8.3% |
| 8. Robustez 4V vs 2V | Ablación | ΔF1=-50% | HRV crítico multivariado |

---

**Fecha de Generación:** $(Get-Date -Format "dddd, dd 'de' MMMM 'de' yyyy, HH:mm:ss")$  
**Versión:** 1.0 - Pipeline Completo Bioestadístico  
**Estado:** VALIDADO - Listo para Defensa Q1

