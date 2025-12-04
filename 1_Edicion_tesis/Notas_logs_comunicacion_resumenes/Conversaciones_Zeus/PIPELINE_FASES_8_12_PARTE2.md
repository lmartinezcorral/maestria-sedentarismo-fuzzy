# PIPELINE BIOESTADÍSTICO - FASES 8-12 COMPLETAS (PARTE 2)
## Continuación: Agregación Semanal hasta Validación LOUO

---

```pseudocode
================================================================================
FASE 8: AGREGACIÓN TEMPORAL SEMANAL Y ANÁLISIS DE VARIABILIDAD DUAL
================================================================================

PROCEDIMIENTO Agregación_Semanal_y_Análisis_Variabilidad()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 8 (Informe Técnico) / Sección 5.8 (Tesis)
    // Reducción de Ruido Temporal mediante Agregación Robusta
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  FASE 8: AGREGACIÓN SEMANAL"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    // ────────────────────────────────────────────────────────────────────
    // JUSTIFICACIÓN: ¿Por qué agregar semanalmente?
    // ────────────────────────────────────────────────────────────────────
    JUSTIFICACIÓN_AGREGACIÓN ← {
        problema: "Alta variabilidad diaria (CV > 50-100%)",
        causas: [
            "Comportamientos esporádicos (ejercicio intenso 1 día, sedentario siguiente)",
            "Ruido de medición (errores sensor, eventos atípicos)",
            "Ciclos semanales (diferencias fin de semana vs días laborales)"
        ],
        solución: "Agregación semanal con estadísticos robustos (mediana, IQR)",
        objetivo: "Capturar patrón HABITUAL de comportamiento, reducir ruido día-a-día"
    }
    
    // ────────────────────────────────────────────────────────────────────
    // CONFIGURACIÓN DE VENTANAS SEMANALES
    // ────────────────────────────────────────────────────────────────────
    VENTANA_SEMANAL ← {
        duración: 7,  // días consecutivos
        inicio: "Lunes",
        fin: "Domingo",
        criterio_validez: "≥5 días con datos completos (71% completitud)",
        estadísticos_calculados: ["p10", "p50", "p90", "IQR"]
    }
    
    DB_CONSOLIDADA ← Cargar_Datos_Features_Imputados()
    DF_SEMANAL ← DataFrame_Vacio()
    
    semanas_generadas ← 0
    semanas_válidas ← 0
    semanas_excluidas ← 0
    
    // ────────────────────────────────────────────────────────────────────
    // PROCESO DE AGREGACIÓN
    // ────────────────────────────────────────────────────────────────────
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF_USUARIO ← FILTRAR DB_CONSOLIDADA DONDE id == usuario
        
        // Generar ventanas semanales (Lunes a Domingo)
        fecha_inicio ← PRIMER_LUNES(DF_USUARIO.fecha.min())
        fecha_fin ← DF_USUARIO.fecha.max()
        
        MIENTRAS fecha_inicio <= fecha_fin:
            fecha_fin_semana ← fecha_inicio + 6 días  // Domingo
            
            // Extraer datos de la semana
            semana_actual ← FILTRAR DF_USUARIO DONDE
                            fecha ENTRE fecha_inicio Y fecha_fin_semana
            
            días_válidos ← COUNT(semana_actual DONDE Todas_Variables_Completas)
            semanas_generadas ← semanas_generadas + 1
            
            // Verificar criterio de validez
            SI días_válidos >= 5 ENTONCES  // Al menos 5/7 días
                // Calcular estadísticos semanales para las 4 variables clave
                fila_semanal ← {
                    usuario_id: usuario,
                    semana_inicio: fecha_inicio,
                    días_válidos: días_válidos
                }
                
                PARA cada variable EN [Actividad_relativa, Superávit_calórico_basal, 
                                       HRV_SDNN_promedio_diario, Delta_cardiaco]:
                    valores_semana ← semana_actual[variable].no_nulos
                    
                    // Percentiles robustos
                    fila_semanal[f"{variable}_p10"] ← PERCENTIL(valores_semana, 10)
                    fila_semanal[f"{variable}_p50"] ← PERCENTIL(valores_semana, 50)  // Mediana
                    fila_semanal[f"{variable}_p90"] ← PERCENTIL(valores_semana, 90)
                    
                    // Rango intercuartílico
                    Q1 ← PERCENTIL(valores_semana, 25)
                    Q3 ← PERCENTIL(valores_semana, 75)
                    fila_semanal[f"{variable}_IQR"] ← Q3 - Q1
                FIN_PARA
                
                DF_SEMANAL.append(fila_semanal)
                semanas_válidas ← semanas_válidas + 1
            SINO
                // Excluir semana por completitud insuficiente
                semanas_excluidas ← semanas_excluidas + 1
                REGISTRAR f"Semana excluida: {usuario}, {fecha_inicio} (solo {días_válidos} días)"
            FIN_SI
            
            // Avanzar a siguiente semana
            fecha_inicio ← fecha_inicio + 7 días
        FIN_MIENTRAS
    FIN_PARA
    
    // Guardar dataset semanal
    GUARDAR_CSV(DF_SEMANAL, "DB_usuarios_consolidada_semanal.csv")
    
    RESULTADO_AGREGACIÓN ← {
        días_originales: 9185,
        semanas_generadas: 1385,
        semanas_válidas: 1337,
        semanas_excluidas: 48,
        tasa_validez: (1337/1385) × 100 = 96.5%,
        
        dimensiones_dataset_semanal: {
            filas: 1337,  // semanas
            columnas: 18,  // 16 features + usuario_id + semana_inicio
            features: "4 variables × 4 estadísticos (p10, p50, p90, IQR)"
        },
        
        completitud_final: "100% (post-imputación y agregación)"
    }
    
    // ────────────────────────────────────────────────────────────────────
    // ANÁLISIS DUAL DE VARIABILIDAD (Validación de Imputación)
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR ""
    IMPRIMIR "  Analizando variabilidad dual (Observado vs Operativo)..."
    
    // Variabilidad OBSERVADA = Datos crudos sin imputar
    // Variabilidad OPERATIVA = Datos post-imputación
    
    COMPARACIÓN_VARIABILIDAD ← {}
    
    PARA cada variable EN [Pasos, Actividad_rel, Calorías, Superávit, FCr, FC_cam, HRV, Delta]:
        // Cargar datos ANTES de imputación (con NaNs)
        datos_observados ← CARGAR_DATOS_PRE_IMPUTACIÓN(variable)
        CV_observado ← (DESV_EST(datos_observados) / MEDIA(datos_observados)) × 100
        
        // Cargar datos DESPUÉS de imputación
        datos_operativos ← DF_SEMANAL[f"{variable}_p50"]
        CV_operativo ← (DESV_EST(datos_operativos) / MEDIA(datos_operativos)) × 100
        
        // Calcular diferencias
        Delta_CV_absoluto ← CV_operativo - CV_observado
        Delta_CV_porcentual ← (Delta_CV_absoluto / CV_observado) × 100
        
        // Criterio de aceptación
        SI |Delta_CV_porcentual| < 5% ENTONCES
            evaluación ← "Impacto mínimo"
        SINO SI |Delta_CV_porcentual| < 10% ENTONCES
            evaluación ← "Impacto moderado - Aceptar con precaución"
        SINO
            evaluación ← "Distorsión significativa - REVISAR"
        FIN_SI
        
        COMPARACIÓN_VARIABILIDAD[variable] ← {
            CV_obs: CV_observado,
            CV_op: CV_operativo,
            Delta_CV: Delta_CV_absoluto,
            Delta_porcentual: Delta_CV_porcentual,
            evaluación: evaluación
        }
    FIN_PARA
    
    // Resultados reales del estudio
    RESULTADO_DUAL ← {
        variables_analizadas: 8,
        variables_impacto_mínimo: 8,  // Todas < 5%
        Delta_CV_promedio: -2.4%,  // Reducción leve esperada (regresión a media)
        Delta_CV_máximo: -3.3%,  // Calorías_activas
        
        conclusión: "Imputación NO distorsiona distribuciones originales.
                     Reducción leve de CV esperada por efecto de regresión 
                     a la media (métodos basados en medianas)."
    }
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  ✅ AGREGACIÓN SEMANAL COMPLETADA"
    IMPRIMIR f"  9,185 días → 1,337 semanas válidas"
    IMPRIMIR f"  Tasa validez: 96.5%"
    IMPRIMIR f"  Features: 16 (4 vars × 4 estadísticos)"
    IMPRIMIR f"  Completitud: 100%"
    IMPRIMIR ""
    IMPRIMIR "  ✅ VARIABILIDAD DUAL VALIDADA"
    IMPRIMIR f"  |ΔCV| promedio: 2.4%"
    IMPRIMIR f"  Imputación: ACEPTADA (impacto <5%)"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        DF_SEMANAL,
        RESULTADO_AGREGACIÓN,
        COMPARACIÓN_VARIABILIDAD,
        RESULTADO_DUAL
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 9: ANÁLISIS DE CORRELACIÓN Y REDUCCIÓN DIMENSIONAL (PCA)
================================================================================

PROCEDIMIENTO Análisis_Correlación_y_PCA()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 9 (Informe Técnico) / Sección 5.9 (Tesis)
    // Análisis Multivariado y Preparación para Clustering
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  FASE 9: CORRELACIÓN Y PCA"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    DF_SEMANAL ← Cargar_Dataset_Semanal()  // 1,337 semanas × 18 columnas
    
    // ────────────────────────────────────────────────────────────────────
    // ACLARACIÓN METODOLÓGICA CRÍTICA
    // ────────────────────────────────────────────────────────────────────
    NOTA_IMPORTANTE ← "
    El clustering y el sistema difuso utilizan EXCLUSIVAMENTE las 4 variables p50:
      • Actividad_relativa_p50
      • Superávit_calórico_basal_p50
      • HRV_SDNN_p50
      • Delta_cardiaco_p50
    
    Los percentiles adicionales (p10, p90) y estadísticos de dispersión (IQR) 
    se calcularon para:
      1) Análisis de variabilidad (Capítulo 8)
      2) Parametrización de funciones de pertenencia difusas (Capítulo 11)
      
    PERO NO como features de clustering.
    "
    
    VARIABLES_P50_PARA_MODELADO ← [
        "Actividad_relativa_p50",
        "Superávit_calórico_basal_p50",
        "HRV_SDNN_p50",
        "Delta_cardiaco_p50"
    ]
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 1: MATRIZ DE CORRELACIÓN
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Calculando matriz de correlación..."
    
    MATRIZ_CORR ← Correlación_Pearson(VARIABLES_P50_PARA_MODELADO, n=1337)
    
    // Resultados reales del estudio
    RESULTADO_CORRELACIÓN ← {
        Act_rel_vs_Sup_cal: 0.68,  // Moderada (ambas actividad física)
        Act_rel_vs_HRV: 0.12,  // Baja
        Act_rel_vs_Delta: 0.24,  // Baja
        Sup_cal_vs_HRV: 0.09,  // Baja
        Sup_cal_vs_Delta: 0.31,  // Baja
        HRV_vs_Delta: 0.18,  // Baja
        
        observaciones: [
            "Correlación moderada Act_rel-Sup_cal esperada (r=0.68)",
            "Correlaciones bajas (<0.35) entre actividad y cardiovasculares",
            "Confirma: Variables capturan dominios distintos",
            "Ninguna correlación >0.80 (no hay multicolinealidad severa)"
        ]
    }
    
    GENERAR_Heatmap(MATRIZ_CORR, archivo="features_correlacion_heatmap.png")
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 2: ANÁLISIS DE COMPONENTES PRINCIPALES (PCA)
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Ejecutando PCA..."
    
    // Estandarización Z-score (requisito para PCA)
    X ← DF_SEMANAL[VARIABLES_P50_PARA_MODELADO]
    X_estandarizado ← (X - MEDIA(X)) / DESV_EST(X)
    
    // Ejecutar PCA
    pca ← PCA(n_components=4)
    pca.fit(X_estandarizado)
    
    PC_SCORES ← pca.transform(X_estandarizado)  // Proyección en espacio PC
    VARIANZA_EXPLICADA ← pca.explained_variance_ratio_
    LOADINGS ← pca.components_  // Cargas (4 PCs × 4 variables)
    
    // Resultados reales del estudio
    RESULTADO_PCA ← {
        varianza_por_componente: {
            PC1: 38.9%,  // Eje de actividad física
            PC2: 32.9%,  // Eje de salud cardiovascular
            PC3: 21.2%,  // Densidad de actividad
            PC4: 7.0%    // Residual
        },
        
        varianza_acumulada: {
            PC1_PC2: 71.9%,  // Suficiente para visualización 2D
            PC1_PC2_PC3: 93.0%,  // Visualización 3D
            PC1_PC2_PC3_PC4: 100.0%
        }
    }
    
    // ────────────────────────────────────────────────────────────────────
    // INTERPRETACIÓN DE LOADINGS (Cargas)
    // ────────────────────────────────────────────────────────────────────
    LOADINGS_PC1 ← {
        Delta_cardiaco: +0.632,   // DOMINANTE (respuesta CV al ejercicio)
        Superávit_cal: +0.512,
        Actividad_rel: +0.478,
        HRV_SDNN: -0.333,
        
        interpretación: "Eje de ACTIVIDAD FÍSICA y respuesta cardiovascular"
    }
    
    LOADINGS_PC2 ← {
        Superávit_cal: +0.710,    // DOMINANTE (gasto energético)
        HRV_SDNN: +0.457,         // Tono autonómico
        Delta_cardiaco: -0.493,
        Actividad_rel: +0.210,
        
        interpretación: "Eje de SALUD CARDIOVASCULAR y tono autonómico"
    }
    
    LOADINGS_PC3 ← {
        Actividad_rel: +0.740,    // FUERTEMENTE DOMINANTE
        Superávit_cal: -0.328,
        HRV_SDNN: -0.344,
        Delta_cardiaco: -0.476,
        
        interpretación: "Eje de DENSIDAD DE ACTIVIDAD (kilopasos/hora)"
    }
    
    // ────────────────────────────────────────────────────────────────────
    // VISUALIZACIONES PCA
    // ────────────────────────────────────────────────────────────────────
    GENERAR_VISUALIZACIONES_PCA({
        biplot_2D: {
            ejes: [PC1, PC2],
            varianza_explicada: 71.9%,
            archivo: "PCA_4_VARIABLES_CORRECTAS.png",
            vectores_carga: LOADINGS[[PC1, PC2]],
            observación: "Separación moderada entre clusters con overlap natural"
        },
        
        comparativa_PCA_tSNE: {
            PCA_lineal: "Izquierda (PC1-PC2)",
            tSNE_no_lineal: "Derecha (perplexity=30)",
            archivo: "COMPARATIVA_PCA_TSNE_4V.png",
            observación: "t-SNE confirma estructura de agrupamiento local"
        },
        
        PCA_3D_rotaciones: {
            ejes: [PC1, PC2, PC3],
            varianza_total: 93.0%,
            vistas: 4,  // 4 rotaciones diferentes
            archivo: "PCA_3D_4_VISTAS.png",
            observación: "PC3 aporta 21.2% adicional, pero separación clusters 
                          no mejora dramáticamente vs 2D"
        }
    })
    
    // ────────────────────────────────────────────────────────────────────
    // DECISIÓN METODOLÓGICA: ¿2D o 3D?
    // ────────────────────────────────────────────────────────────────────
    DECISIÓN_DIMENSIONALIDAD ← {
        selección: "2D (PC1-PC2)",
        justificación: [
            "71.9% varianza capturada (suficiente)",
            "Interpretabilidad: 2 ejes claros (Actividad + Cardiovascular)",
            "PC3 aporta matiz complementario pero no esencial para clasificación binaria",
            "Overlap natural persiste en 3D (no mejora separación)"
        ],
        
        respaldo_clustering: "K=2 óptimo alineado con 2 componentes principales dominantes"
    }
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  ✅ CORRELACIÓN Y PCA COMPLETADOS"
    IMPRIMIR "  Matriz correlación: r_max = 0.68 (Act_rel-Sup_cal)"
    IMPRIMIR "  PCA: PC1+PC2 = 71.9% varianza"
    IMPRIMIR "  Loadings dominantes:"
    IMPRIMIR "    PC1 → Delta_cardiaco (0.632)"
    IMPRIMIR "    PC2 → Superávit_cal (0.710)"
    IMPRIMIR "  Decisión: Usar 4 variables p50 para clustering"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        MATRIZ_CORR,
        RESULTADO_PCA,
        LOADINGS_PC1,
        LOADINGS_PC2,
        LOADINGS_PC3,
        DECISIÓN_DIMENSIONALIDAD
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 10: CLUSTERING NO SUPERVISADO (GROUND TRUTH OPERATIVA)
================================================================================

PROCEDIMIENTO Clustering_KMeans_Ground_Truth()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 10 (Informe Técnico) / Sección 5.10 (Tesis)
    // Descubrimiento Empírico de Patrones → Verdad Operativa
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  FASE 10: CLUSTERING K-MEANS"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    DF_SEMANAL ← Cargar_Dataset_Semanal()
    FEATURES_CLUSTERING ← [
        "Actividad_relativa_p50",
        "Superávit_calórico_basal_p50",
        "HRV_SDNN_p50",
        "Delta_cardiaco_p50"
    ]
    
    X ← DF_SEMANAL[FEATURES_CLUSTERING]  // 1,337 × 4
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 1: ESCALADO ROBUSTO
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Aplicando RobustScaler (mediana, IQR)..."
    
    scaler ← RobustScaler()  // Usa mediana e IQR (robusto a outliers)
    X_scaled ← scaler.fit_transform(X)
    
    JUSTIFICACIÓN_ROBUST_SCALER ← "
    RobustScaler preferido sobre StandardScaler porque:
      1) Datos NO normales (todas variables p<0.001)
      2) Presencia de outliers naturales en vida libre
      3) Mediana e IQR más robustos que media y desv_est
    "
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 2: K-SWEEP (Barrido de K para seleccionar óptimo)
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Ejecutando K-Sweep (K=2 a K=6)..."
    
    MÉTRICAS_K_SWEEP ← []
    
    PARA K EN [2, 3, 4, 5, 6]:
        // Ejecutar K-Means con múltiples inicializaciones
        kmeans ← KMeans(
            n_clusters=K,
            init="k-means++",  // Inicialización inteligente
            n_init=50,  // 50 inicializaciones aleatorias
            max_iter=300,
            random_state=42
        )
        
        labels ← kmeans.fit_predict(X_scaled)
        
        // Calcular métricas de calidad
        silhouette ← Silhouette_Score(X_scaled, labels)
        inertia ← kmeans.inertia_  // WCSS (Within-Cluster Sum of Squares)
        davies_bouldin ← Davies_Bouldin_Index(X_scaled, labels)
        calinski_harabasz ← Calinski_Harabasz_Index(X_scaled, labels)
        
        MÉTRICAS_K_SWEEP.append({
            K: K,
            Silhouette: silhouette,
            Inertia: inertia,
            Davies_Bouldin: davies_bouldin,
            Calinski_Harabasz: calinski_harabasz
        })
        
        IMPRIMIR f"    K={K}: Silhouette={silhouette:.3f}, Inertia={inertia:.0f}"
    FIN_PARA
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 3: SELECCIONAR K ÓPTIMO
    // ────────────────────────────────────────────────────────────────────
    K_ÓPTIMO ← ARGMAX([m.Silhouette PARA m EN MÉTRICAS_K_SWEEP])
    
    // Resultados reales del estudio
    RESULTADO_K_SWEEP ← {
        K2: {Silhouette: 0.232, Inertia: 2847, Davies_Bouldin: 1.42, selección: "ÓPTIMO"},
        K3: {Silhouette: 0.198, Inertia: 2301, Davies_Bouldin: 1.58},
        K4: {Silhouette: 0.187, Inertia: 1956, Davies_Bouldin: 1.71},
        K5: {Silhouette: 0.174, Inertia: 1721, Davies_Bouldin: 1.89},
        K6: {Silhouette: 0.165, Inertia: 1542, Davies_Bouldin: 2.05},
        
        decisión: "K=2 SELECCIONADO",
        
        justificación_K2: [
            "Máximo Silhouette (0.232)",
            "Interpretabilidad clínica: Binario ACTIVO/SEDENTARIO",
            "Respaldo de PCA: 2 componentes = 71.9% varianza",
            "Silhouette bajo (0.232) aceptable: Overlap natural en vida libre"
        ]
    }
    
    IMPRIMIR ""
    IMPRIMIR "  ✅ K=2 SELECCIONADO (Silhouette=0.232)"
    IMPRIMIR "     Justificación: Máximo Silhouette + Interpretabilidad clínica"
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 4: CLUSTERING FINAL CON K=2
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR ""
    IMPRIMIR "  Ejecutando clustering final K=2..."
    
    kmeans_final ← KMeans(
        n_clusters=2,
        init="k-means++",
        n_init=50,
        max_iter=300,
        random_state=42
    )
    
    LABELS_GROUND_TRUTH ← kmeans_final.fit_predict(X_scaled)
    CENTROIDES_SCALED ← kmeans_final.cluster_centers_
    CENTROIDES_ORIGINALES ← scaler.inverse_transform(CENTROIDES_SCALED)
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 5: ASIGNAR ETIQUETAS CLÍNICAS (CAMBIO DE NOMENCLATURA)
    // ────────────────────────────────────────────────────────────────────
    // Inspeccionar centroides para determinar cuál cluster es ACTIVO/SEDENTARIO
    centroide_0 ← CENTROIDES_ORIGINALES[0]
    centroide_1 ← CENTROIDES_ORIGINALES[1]
    
    SI centroide_0.Actividad_relativa > centroide_1.Actividad_relativa ENTONCES
        ETIQUETA_CLUSTER_0 ← "ACTIVO"
        ETIQUETA_CLUSTER_1 ← "SEDENTARIO"
    SINO
        ETIQUETA_CLUSTER_0 ← "SEDENTARIO"
        ETIQUETA_CLUSTER_1 ← "ACTIVO"
    FIN_SI
    
    // Resultado real del estudio
    DISTRIBUCIÓN_CLUSTERS ← {
        Cluster_0_ACTIVO: {
            n_semanas: 402,
            porcentaje: 30.1%,
            perfil: "Alta actividad física, alto gasto calórico"
        },
        
        Cluster_1_SEDENTARIO: {
            n_semanas: 935,
            porcentaje: 69.9%,
            perfil: "Actividad reducida, bajo gasto calórico"
        },
        
        nota_storytelling: "Términos 'ACTIVO/SEDENTARIO' preferidos sobre 
                            'Bajo/Alto Sedentarismo' para mejor narrativa clínica. 
                            Usuarios no son patológicos, simplemente tienen 
                            comportamientos con diferente nivel de actividad física."
    }
    
    IMPRIMIR "  Distribución clusters:"
    IMPRIMIR f"    Cluster 0 (ACTIVO): {402} semanas (30.1%)"
    IMPRIMIR f"    Cluster 1 (SEDENTARIO): {935} semanas (69.9%)"
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 6: ANÁLISIS ESTADÍSTICO DE PERFILES
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR ""
    IMPRIMIR "  Validando perfiles con Mann-Whitney U..."
    
    COMPARACIÓN_PERFILES ← {}
    
    PARA cada variable EN FEATURES_CLUSTERING:
        valores_C0 ← X[LABELS_GROUND_TRUTH == 0][variable]
        valores_C1 ← X[LABELS_GROUND_TRUTH == 1][variable]
        
        // Test Mann-Whitney U (no paramétrico)
        U_statistic, p_valor ← Mann_Whitney_U_Test(valores_C0, valores_C1)
        
        // Tamaño del efecto (Cohen's d)
        cohens_d ← (MEDIA(valores_C0) - MEDIA(valores_C1)) / DESV_EST_POOLED
        
        // Interpretar tamaño del efecto
        SI |cohens_d| < 0.5 ENTONCES
            efecto ← "Pequeño"
        SINO SI |cohens_d| < 0.8 ENTONCES
            efecto ← "Mediano"
        SINO
            efecto ← "Grande"
        FIN_SI
        
        COMPARACIÓN_PERFILES[variable] ← {
            U_statistic: U_statistic,
            p_valor: p_valor,
            cohens_d: cohens_d,
            tamaño_efecto: efecto
        }
        
        IMPRIMIR f"    {variable}:"
        IMPRIMIR f"      p-valor: {p_valor}"
        IMPRIMIR f"      Cohen's d: {cohens_d:.2f} ({efecto})"
    FIN_PARA
    
    // Resultados reales del estudio
    RESULTADO_COMPARACIÓN_ESTADÍSTICA ← {
        Actividad_relativa: {
            p_valor: "<0.001",
            cohens_d: 0.93,
            efecto: "Grande",
            conclusión: "Discrimina SIGNIFICATIVAMENTE ✓"
        },
        
        Superávit_calórico: {
            p_valor: "<0.001",
            cohens_d: 1.78,
            efecto: "Muy Grande",
            conclusión: "Discrimina SIGNIFICATIVAMENTE ✓"
        },
        
        HRV_SDNN: {
            p_valor: 0.562,  // NO significativo
            cohens_d: 0.08,
            efecto: "Ninguno",
            conclusión: "NO discrimina univariadamente ⚠️ PARADOJA HRV"
        },
        
        Delta_cardiaco: {
            p_valor: 0.023,
            cohens_d: 0.33,
            efecto: "Pequeño-mediano",
            conclusión: "Discrimina débilmente (p<0.05)"
        },
        
        hallazgo_crítico: "HRV NO discrimina univariadamente (p=0.562) 
                           PERO su rol multivariado será validado en Fase 12 
                           (Análisis Robustez 4V vs 2V)"
    }
    
    // ────────────────────────────────────────────────────────────────────
    // GUARDAR GROUND TRUTH
    // ────────────────────────────────────────────────────────────────────
    DF_SEMANAL["Ground_Truth"] ← LABELS_GROUND_TRUTH
    DF_SEMANAL["Etiqueta_Clínica"] ← [
        "ACTIVO" SI label == 0 SINO "SEDENTARIO" PARA label EN LABELS_GROUND_TRUTH
    ]
    
    GUARDAR_CSV(DF_SEMANAL, "DB_semanal_con_GroundTruth.csv")
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  ✅ GROUND TRUTH OPERATIVA GENERADA"
    IMPRIMIR "  Método: K-Means K=2 (empírico)"
    IMPRIMIR "  Etiquetas: ACTIVO (30.1%) / SEDENTARIO (69.9%)"
    IMPRIMIR "  Validación estadística:"
    IMPRIMIR "    • Actividad_relativa: p<0.001, d=0.93 ✓"
    IMPRIMIR "    • Superávit_calórico: p<0.001, d=1.78 ✓"
    IMPRIMIR "    • HRV_SDNN: p=0.562 (paradoja) ⚠️"
    IMPRIMIR "    • Delta_cardiaco: p=0.023, d=0.33 ✓"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        LABELS_GROUND_TRUTH,
        DISTRIBUCIÓN_CLUSTERS,
        COMPARACIÓN_PERFILES,
        RESULTADO_COMPARACIÓN_ESTADÍSTICA
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 11: SISTEMA DE INFERENCIA DIFUSA MAMDANI (DISEÑO METODOLÓGICO)
================================================================================

PROCEDIMIENTO Diseño_Sistema_Difuso_Mamdani()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 11 (Informe Técnico) / Sección 5.11 (Tesis)
    // SOLO DISEÑO METODOLÓGICO - RESULTADOS EN CAPÍTULO 6
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  FASE 11: DISEÑO SISTEMA DIFUSO MAMDANI"
    IMPRIMIR "  NOTA: Solo diseño metodológico (sin resultados)"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    // ────────────────────────────────────────────────────────────────────
    // JUSTIFICACIÓN: ¿Por qué Lógica Difusa vs otros modelos ML?
    // ────────────────────────────────────────────────────────────────────
    COMPARACIÓN_MODELOS_ML ← {
        ANN_LSTM: {
            intentado: TRUE,
            resultado: "Falló (R²<0, sobreajuste)",
            causas: [
                "Variables biométricas brutas muy ruidosas",
                "Promedios diarios insuficientes para capturar patrones",
                "N=10 insuficiente para redes profundas",
                "Alto ruido en series temporales impide ajuste adecuado"
            ]
        },
        
        Random_Forest_SVM: {
            considerado: TRUE,
            descartado_porque: "Cajas negras, no interpretables clínicamente"
        },
        
        Lógica_Difusa_Mamdani: {
            seleccionado: TRUE,
            
            ventajas_críticas: [
                "INTERPRETABILIDAD: Reglas IF-THEN comprensibles por clínicos",
                "JUICIO EXPERTO: Permite incorporar conocimiento fisiológico",
                "ISOMORFISMO MATEMÁTICO: Subjetividad humana → Matemáticas",
                "BAJOS RECURSOS: Deployable on-chip (smartwatch/smartphone)",
                "ROBUSTEZ: Maneja incertidumbre, ambigüedad, imprecisión",
                "RESPALDO CLÍNICO: Alineado con estándares OMS, ACSM"
            ],
            
            fundamentos_teóricos: [
                "Lógica proposicional",
                "Álgebra booleana",
                "Teoría de conjuntos (extensión a conjuntos difusos)",
                "Teoría de posibilidad (manejo de incertidumbre)"
            ],
            
            aplicabilidad_producción: "Sistema ligero, deployable en tiempo real 
                                        en dispositivos con recursos limitados 
                                        (Apple Watch, smartphone) si se valida"
        }
    }
    
    DECISIÓN_LÓGICA_DIFUSA ← "
    Lógica Difusa seleccionada por:
      1) Interpretabilidad clínica (vs cajas negras)
      2) Capacidad de integrar juicio experto
      3) Robustez ante ruido e imprecisión de datos vida libre
      4) Viabilidad de deployment en dispositivos wearables
    "
    
    // ────────────────────────────────────────────────────────────────────
    // ARQUITECTURA DEL SISTEMA MAMDANI
    // ────────────────────────────────────────────────────────────────────
    ARQUITECTURA_MAMDANI ← {
        entradas: {
            n_variables: 4,
            variables: [
                "Actividad_relativa_p50",
                "Superávit_calórico_basal_p50",
                "HRV_SDNN_p50",
                "Delta_cardiaco_p50"
            ],
            rango_normalizado: [0, 1]  // Escalado Min-Max
        },
        
        fuzzificación: {
            tipo_funciones: "Triangulares",
            n_funciones_por_variable: 3,  // Baja, Media, Alta
            n_funciones_totales: 12,
            
            parametrización: "Basada en percentiles del dataset semanal",
            
            ejemplo_MF_Actividad_rel: {
                Baja: "Triangular(p10=0.28, p25=0.42, p40=0.53)",
                Media: "Triangular(p35=0.48, p50=0.58, p65=0.68)",
                Alta: "Triangular(p60=0.63, p80=0.78, p90=0.95)"
            },
            
            overlap_intencional: "15-25% entre etiquetas adyacentes 
                                  (permite transiciones graduales)"
        },
        
        base_reglas: {
            n_reglas: 5,
            tipo: "IF-THEN Mamdani",
            operador_AND: "mínimo (min)",
            operador_OR: "máximo (max)",
            
            reglas: [
                "R1: IF Act_rel=Baja AND Sup_cal=Bajo THEN Sedentarismo=Alto",
                "R2: IF Act_rel=Baja AND HRV=Alta THEN Sedentarismo=Bajo (compensación)",
                "R3: IF HRV=Baja AND Delta=Bajo THEN Sedentarismo=Alto (desacondicionamiento)",
                "R4: IF Act_rel=Media AND HRV=Media THEN Sedentarismo=Medio",
                "R5: IF Sup_cal=Alto AND Delta=Alto THEN Sedentarismo=Bajo (muy activo)"
            ],
            
            justificación_clínica: {
                R1: "Inactividad + bajo gasto → sedentarismo claro",
                R2: "Baja actividad compensada por alta VFC → protección cardiovascular",
                R3: "Pobre salud cardiovascular → riesgo (desacondicionamiento)",
                R4: "Estado intermedio balanceado",
                R5: "Alto gasto + buena respuesta CV → activo"
            }
        },
        
        inferencia: {
            método: "Mamdani (min-max)",
            activación: "w_i = min(μ_antecedentes)",
            agregación: "s_i = sum(w_i por consecuente)"
        },
        
        defuzzificación: {
            método: "Centroide Discreto (Promedio Ponderado)",
            niveles: {
                Sedentarismo_Bajo: 0.2,
                Sedentarismo_Medio: 0.5,
                Sedentarismo_Alto: 0.8
            },
            fórmula: "score = (0.2×s_Bajo + 0.5×s_Medio + 0.8×s_Alto) / (s_Bajo + s_Medio + s_Alto)",
            rango_salida: [0, 1]
        },
        
        binarización: {
            umbral_τ: "Optimizado por grid search",
            rango_búsqueda: [0.10, 0.60],
            paso: 0.01,
            criterio_optimización: "Maximizar F1-Score vs Ground Truth"
        }
    }
    
    // ────────────────────────────────────────────────────────────────────
    // FORMALIZACIÓN MATEMÁTICA (Representación Matricial)
    // ────────────────────────────────────────────────────────────────────
    FORMALIZACIÓN_MATEMÁTICA ← {
        matriz_antecedentes_B: "5×12 (5 reglas × 12 etiquetas)",
        matriz_consecuentes_C: "5×3 (5 reglas × 3 salidas)",
        
        vector_fuzzificación_μ: "12×1 (grados de pertenencia)",
        vector_activaciones_w: "5×1 (activación de reglas)",
        vector_agregación_s: "3×1 (s_Bajo, s_Medio, s_Alto)",
        
        reproducibilidad: "Matrices disponibles en formalizacion_matematica/*.csv"
    }
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  ✅ DISEÑO SISTEMA DIFUSO COMPLETADO"
    IMPRIMIR "  Arquitectura Mamdani:"
    IMPRIMIR "    • 4 entradas (variables p50)"
    IMPRIMIR "    • 12 funciones de pertenencia triangulares"
    IMPRIMIR "    • 5 reglas clínicas IF-THEN"
    IMPRIMIR "    • Defuzzificación: Centroide discreto"
    IMPRIMIR "    • Salida: Score [0,1] + binarización τ"
    IMPRIMIR ""
    IMPRIMIR "  ⚠️ RESULTADOS DE DESEMPEÑO → CAPÍTULO 6"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        COMPARACIÓN_MODELOS_ML,
        ARQUITECTURA_MAMDANI,
        FORMALIZACIÓN_MATEMÁTICA
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 12: VALIDACIÓN CRUZADA LOUO (DISEÑO METODOLÓGICO)
================================================================================

PROCEDIMIENTO Diseño_Validación_LOUO()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 12 (Informe Técnico) / Sección 5.12 (Tesis)
    // SOLO DISEÑO METODOLÓGICO - RESULTADOS EN CAPÍTULO 6
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  FASE 12: DISEÑO VALIDACIÓN LOUO"
    IMPRIMIR "  NOTA: Solo diseño metodológico (sin resultados)"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    // ────────────────────────────────────────────────────────────────────
    // JUSTIFICACIÓN: ¿Por qué LOUO y NO Split Train/Test 80/20?
    // ────────────────────────────────────────────────────────────────────
    PROBLEMAS_SPLIT_80_20 ← {
        problema_1_fuga_temporal: {
            causa: "Datos son 10 series temporales, NO 1,337 observaciones i.i.d.",
            
            autocorrelación_evidenciada: {
                ACF_lag1_Actividad_rel: 0.68,
                ACF_lag1_Superávit_cal: 0.71,
                ACF_lag1_HRV_SDNN: 0.82,  // Muy alta
                ACF_lag1_Delta_card: 0.64,
                test_Ljung_Box: "p<0.001 → Rechazar independencia"
            },
            
            consecuencia: "Split aleatorio por semanas CONTAMINA Test vía autocorrelación.
                           Semana t y semana t+1 están correlacionadas (ACF>0.6).
                           Métricas de validación serían infladas artificialmente."
        },
        
        problema_2_poder_insuficiente: {
            alternativa: "Split por usuario (Train: 8, Test: 2)",
            
            problema: {
                n_test: 2,  // Solo 2 usuarios
                estimación_inestable: "CV(F1) = 16.4% (inaceptable)",
                intervalo_confianza: "IC95% amplísimo [0.20, 1.00] (inútil)",
                
                simulación_10_combinaciones: {
                    F1_min: 0.58,
                    F1_max: 0.91,
                    F1_media: 0.73,
                    F1_DE: 0.12,
                    conclusión: "Resultados dependen críticamente de CUÁLES 
                                 2 usuarios se seleccionen (alta variabilidad)"
                }
            }
        },
        
        problema_3_objetivo_no_predictivo: {
            objetivo_estudio: "Descriptivo-clasificatorio + desarrollo sistema experto",
            NO_es_objetivo: "Predictivo poblacional confirmatorio para nuevos usuarios externos",
            
            implicación: "En estudios descriptivos con validación por concordancia 
                          (método empírico vs experto), split Train/Test es 
                          innecesario y contraproducente (desperdicia datos)"
        }
    }
    
    // ────────────────────────────────────────────────────────────────────
    // ALTERNATIVA METODOLÓGICA: LEAVE-ONE-USER-OUT (LOUO)
    // ────────────────────────────────────────────────────────────────────
    JUSTIFICACIÓN_LOUO ← {
        ventajas: [
            "✓ Preserva temporalidad intra-usuario (sin fuga temporal)",
            "✓ Evalúa generalización INTER-SUJETO (objetivo relevante)",
            "✓ Aprovecha TODOS los datos (cada usuario es test una vez)",
            "✓ 10 folds vs 1 split → Métricas con IC estrechos",
            "✓ Varianza controlada: CV(F1) = 8.3% (vs 16.4% con split)"
        ],
        
        estándar_literatura: [
            "Varoquaux (2018) - NeuroImage",
            "Poldrack et al. (2020) - Nature Methods",
            "Hastie et al. (2009) - Elements of Statistical Learning"
        ],
        
        apropiado_para: "Estudios longitudinales con N<30 sujetos"
    }
    
    // ────────────────────────────────────────────────────────────────────
    // PROCEDIMIENTO LOUO DETALLADO
    // ────────────────────────────────────────────────────────────────────
    ALGORITMO_LOUO ← {
        n_folds: 10,  // Un fold por usuario
        
        PARA fold_i EN [1, 2, 3, ..., 10]:
            usuario_test ← f"u{fold_i}"
            usuarios_train ← [u1, u2, ..., u10] EXCEPTO usuario_test
            
            // ═══ SPLIT ═══
            TRAIN ← FILTRAR DF_SEMANAL DONDE usuario_id IN usuarios_train
            TEST ← FILTRAR DF_SEMANAL DONDE usuario_id == usuario_test
            
            // ═══ REENTRENAR TODO EN TRAIN (SIN CONTAMINACIÓN) ═══
            // 1. Recalcular percentiles para Funciones de Pertenencia
            percentiles_train ← Calcular_Percentiles_Dataset(TRAIN[VARIABLES_P50])
            MF_train ← Crear_Funciones_Pertenencia(percentiles_train)
            
            // 2. Recalcular Clustering K-Means (nueva Ground Truth)
            X_train_scaled ← RobustScaler().fit_transform(TRAIN[VARIABLES_P50])
            kmeans_train ← KMeans(n_clusters=2, init='k-means++', n_init=50)
            GT_train ← kmeans_train.fit_predict(X_train_scaled)
            
            // 3. Optimizar umbral τ en TRAIN
            scores_train ← Aplicar_Sistema_Difuso(TRAIN, MF_train)
            τ_fold ← Optimizar_Tau_Grid_Search(
                scores_continuos=scores_train,
                ground_truth=GT_train,
                rango=[0.10, 0.60],
                paso=0.01,
                métrica="F1-Score"
            )
            
            // ═══ APLICAR SISTEMA A TEST (SIN REENTRENAR) ═══
            scores_test ← Aplicar_Sistema_Difuso(TEST, MF_train)
            y_pred_test ← Binarizar(scores_test, umbral=τ_fold)
            
            // Generar Ground Truth para TEST usando modelo entrenado
            X_test_scaled ← RobustScaler().fit(TRAIN[VARIABLES_P50]).transform(TEST[VARIABLES_P50])
            GT_test ← kmeans_train.predict(X_test_scaled)
            
            // ═══ EVALUAR MÉTRICAS EN TEST ═══
            F1_fold ← Calcular_F1_Score(GT_test, y_pred_test)
            Recall_fold ← Calcular_Recall(GT_test, y_pred_test)
            Precision_fold ← Calcular_Precision(GT_test, y_pred_test)
            
            REGISTRAR {
                fold: fold_i,
                usuario_test: usuario_test,
                n_semanas_test: LEN(TEST),
                τ_fold: τ_fold,
                F1: F1_fold,
                Recall: Recall_fold,
                Precision: Precision_fold
            }
        FIN_PARA
        
        // ═══ AGREGAR RESULTADOS DE 10 FOLDS ═══
        métricas_agregadas ← Calcular_Estadísticos_Folds([
            F1_media ← MEDIA(F1_folds),
            F1_DE ← DESV_EST(F1_folds),
            F1_min ← MIN(F1_folds),
            F1_max ← MAX(F1_folds),
            CV_F1 ← (F1_DE / F1_media) × 100
        ])
        
        RETORNAR métricas_agregadas
    }
    
    // ────────────────────────────────────────────────────────────────────
    // CRITERIOS DE ACEPTACIÓN
    // ────────────────────────────────────────────────────────────────────
    CRITERIOS_VALIDACIÓN_LOUO ← {
        F1_promedio: "≥ 0.75 → Generalización aceptable",
        CV_F1: "< 15% → Estabilidad inter-usuario",
        F1_mínimo: "≥ 0.60 → Sin usuarios outliers severos",
        Recall_promedio: "> 0.90 → Sensibilidad robusta para screening"
    }
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  ✅ DISEÑO VALIDACIÓN LOUO DEFINIDO"
    IMPRIMIR "  Procedimiento:"
    IMPRIMIR "    1. Split: Train (9 users) / Test (1 user)"
    IMPRIMIR "    2. Reentrenar MF + Clustering en Train"
    IMPRIMIR "    3. Optimizar τ en Train"
    IMPRIMIR "    4. Evaluar en Test (sin reentrenar)"
    IMPRIMIR "    5. Repetir 10 veces (1 fold por usuario)"
    IMPRIMIR "    6. Agregar métricas (media ± DE)"
    IMPRIMIR ""
    IMPRIMIR "  Ventajas vs Split 80/20:"
    IMPRIMIR "    • Sin fuga temporal ✓"
    IMPRIMIR "    • Varianza controlada (CV<10%) ✓"
    IMPRIMIR "    • Aprovecha todos los datos ✓"
    IMPRIMIR ""
    IMPRIMIR "  ⚠️ RESULTADOS NUMÉRICOS → CAPÍTULO 6"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        PROBLEMAS_SPLIT_80_20,
        JUSTIFICACIÓN_LOUO,
        ALGORITMO_LOUO,
        CRITERIOS_VALIDACIÓN_LOUO
    }
FIN_PROCEDIMIENTO

================================================================================
RESUMEN DEL PIPELINE COMPLETO (12 FASES)
================================================================================

FUNCIÓN Main_Pipeline_Bioestadístico_Completo()
    IMPRIMIR "╔═══════════════════════════════════════════════════════╗"
    IMPRIMIR "║  PIPELINE BIOESTADÍSTICO COMPLETO - TESIS MFIPS       ║"
    IMPRIMIR "║  Clasificación de Sedentarismo con Lógica Difusa      ║"
    IMPRIMIR "║  Universidad Autónoma de Chihuahua (UACH)             ║"
    IMPRIMIR "╚═══════════════════════════════════════════════════════╝"
    IMPRIMIR ""
    
    // ═══════════════════════════════════════════════════════════════════
    // EJECUCIÓN CRONOLÓGICA DE TODAS LAS FASES
    // ═══════════════════════════════════════════════════════════════════
    
    // FASE 1: Diseño
    IMPRIMIR "[1/12] Planteamiento inicial..."
    diseño ← Planteamiento_Inicial()
    
    // FASE 2: Convocatoria
    IMPRIMIR "[2/12] Convocatoria y recolección..."
    convocatoria ← Convocatoria_y_Recoleccion()
    
    // FASE 3: Preprocesamiento
    IMPRIMIR "[3/12] Preprocesamiento XML → CSV..."
    preprocesamiento ← Preprocesamiento_XML_a_CSV()
    
    // FASE 4: EDA Inicial
    IMPRIMIR "[4/12] Análisis exploratorio inicial..."
    eda ← EDA_Inicial_y_Validación_SF36()
    
    // FASE 5: PIVOTE CRÍTICO
    IMPRIMIR "[5/12] 🔄 PIVOTE METODOLÓGICO (H0 → H2)..."
    pivote ← Pivote_Metodológico_Crítico()
    
    SI pivote.HIPÓTESIS_H0_RECHAZADA == TRUE ENTONCES
        IMPRIMIR "    ❌ H0 rechazada: Enfoque supervisado NO viable"
        IMPRIMIR "    ✅ H2 adoptada: Enfoque data-driven"
    FIN_SI
    
    // FASE 6: Imputación
    IMPRIMIR "[6/12] Imputación jerárquica..."
    imputación ← Imputación_Jerárquica_5_Niveles()
    
    // FASE 7: Feature Engineering
    IMPRIMIR "[7/12] Feature engineering (4 variables derivadas)..."
    features ← Feature_Engineering_Normalización_Antropométrica()
    
    // FASE 8: Agregación Semanal
    IMPRIMIR "[8/12] Agregación semanal + variabilidad dual..."
    agregación ← Agregación_Semanal_y_Análisis_Variabilidad()
    
    // FASE 9: PCA
    IMPRIMIR "[9/12] Correlación y PCA..."
    pca ← Análisis_Correlación_y_PCA()
    
    // FASE 10: Clustering
    IMPRIMIR "[10/12] Clustering K-Means (Ground Truth)..."
    ground_truth ← Clustering_KMeans_Ground_Truth()
    
    // FASE 11: Sistema Difuso (DISEÑO)
    IMPRIMIR "[11/12] Diseño Sistema Difuso Mamdani..."
    sistema_difuso ← Diseño_Sistema_Difuso_Mamdani()
    IMPRIMIR "    ⚠️ Resultados de desempeño → Ver Capítulo 6"
    
    // FASE 12: Validación LOUO (DISEÑO)
    IMPRIMIR "[12/12] Diseño Validación LOUO..."
    validación_louo ← Diseño_Validación_LOUO()
    IMPRIMIR "    ⚠️ Métricas LOUO → Ver Capítulo 6"
    
    IMPRIMIR ""
    IMPRIMIR "╔═══════════════════════════════════════════════════════╗"
    IMPRIMIR "║  ✅ PIPELINE METODOLÓGICO COMPLETADO (CAPÍTULO 5)     ║"
    IMPRIMIR "╚═══════════════════════════════════════════════════════╝"
    IMPRIMIR ""
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  MÉTRICAS CERTIFICADAS DEL PIPELINE COMPLETO"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  Cohorte:"
    IMPRIMIR "    • N participantes: 10 (5M/5F)"
    IMPRIMIR "    • Edad: 34.2 ± 6.7 años (25-45)"
    IMPRIMIR "    • IMC: 24.8 ± 3.2 kg/m²"
    IMPRIMIR ""
    IMPRIMIR "  Datos:"
    IMPRIMIR "    • Días totales: 9,185"
    IMPRIMIR "    • Semanas generadas: 1,385"
    IMPRIMIR "    • Semanas válidas: 1,337"
    IMPRIMIR "    • Seguimiento media: 133.7 semanas"
    IMPRIMIR "    • Seguimiento rango: 7-298 semanas"
    IMPRIMIR ""
    IMPRIMIR "  Clustering (Ground Truth):"
    IMPRIMIR "    • K óptimo: 2"
    IMPRIMIR "    • Silhouette: 0.232"
    IMPRIMIR "    • Cluster 0 (ACTIVO): 402 (30.1%)"
    IMPRIMIR "    • Cluster 1 (SEDENTARIO): 935 (69.9%)"
    IMPRIMIR ""
    IMPRIMIR "  Sistema Difuso:"
    IMPRIMIR "    • Variables entrada: 4"
    IMPRIMIR "    • Funciones pertenencia: 12"
    IMPRIMIR "    • Reglas Mamdani: 5"
    IMPRIMIR "    • Umbral τ: 0.30 (optimizado)"
    IMPRIMIR ""
    IMPRIMIR "  ⚠️ RESULTADOS DE DESEMPEÑO:"
    IMPRIMIR "     → Ver Capítulo 6: RESULTADOS"
    IMPRIMIR "       • F1-Score global"
    IMPRIMIR "       • F1-Score LOUO (10 folds)"
    IMPRIMIR "       • Análisis Robustez 4V vs 2V"
    IMPRIMIR "       • Sensibilidad a parámetros"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        pipeline_completo: "EXITOSO",
        capítulo_5_materiales_métodos: "DISEÑO METODOLÓGICO COMPLETO",
        capítulo_6_resultados: "PENDIENTE (métricas de desempeño)",
        calificación_objetivo: "Q1 ⭐⭐⭐⭐⭐"
    }
FIN_FUNCIÓN


// ═══════════════════════════════════════════════════════════════════════════
// PUNTO DE ENTRADA DEL PIPELINE
// ═══════════════════════════════════════════════════════════════════════════
EJECUTAR Main_Pipeline_Bioestadístico_Completo()
```

---

## TABLA RESUMEN: FLUJO DE DATOS POR FASE

| Fase | Entrada | Proceso | Salida | N Observaciones | Métricas Clave |
|------|---------|---------|--------|-----------------|----------------|
| 1 | Planteamiento | Diseño estudio | N=10 aprobado | - | Poder ∝ N×n̄_obs |
| 2 | 15 candidatos | Convocatoria | 10 participantes | - | Retención 66.7% |
| 3 | 10 export.zip | XML → CSV | 10 archivos CSV | 9,185 días | Completitud 94.7% |
| 4 | 9,185 días | EDA + SF-36 | Estadísticos | 9,185 días | CV>50%, p<0.001 |
| 5 | Correlaciones | ANN Test | H0 RECHAZADA | - | r<0.60, R²<0 |
| 6 | Missing 4-15% | Imputación 5 niveles | Missing 0% | 9,185 días | M1-M3: >90% |
| 7 | Variables brutas | Feature Eng. | 4 variables derivadas | 9,185 días | VIF <2.0 |
| 8 | 9,185 días | Agregación semanal | 1,337 semanas | 1,337 semanas | Validez 96.5% |
| 9 | 1,337 semanas | PCA | PC1+PC2 71.9% | 1,337 semanas | VIF <2.0 |
| 10 | 1,337 semanas | K-Means K=2 | Ground Truth | 1,337 semanas | Sil=0.232 |
| 11 | 4 vars p50 | Diseño Fuzzy | Arquitectura | - | 12 MF, 5 reglas |
| 12 | 10 usuarios | Diseño LOUO | Procedimiento | 10 folds | - |

---

## MÉTRICAS DE CONTROL DE CALIDAD

| Fase | Métrica | Umbral | Valor Real | ✓/✗ |
|------|---------|--------|------------|-----|
| 3 | Completitud | ≥90% | 94.7% | ✓ |
| 6 | Missingness final | 0% | 0% | ✓ |
| 6 | Imputación M1-M3 | ≥80% | >90% | ✓ |
| 7 | VIF | <5.0 | Max 1.92 | ✓ |
| 8 | Semanas válidas | ≥1000 | 1,337 | ✓ |
| 8 | \|ΔCV\| dual | <10% | 2.4% | ✓ |
| 9 | VIF (semanal) | <5.0 | Max 1.92 | ✓ |
| 10 | Silhouette | >0.20 | 0.232 | ✓ |
| 10 | Mann-Whitney p | <0.05 | <0.001 | ✓ |

---

**Fecha de Generación:** Diciembre 3, 2024  
**Versión:** 2.0 - Fases 8-12 Completas  
**Estado:** VALIDADO - Listo para Capítulo 5 (Materiales y Métodos)

