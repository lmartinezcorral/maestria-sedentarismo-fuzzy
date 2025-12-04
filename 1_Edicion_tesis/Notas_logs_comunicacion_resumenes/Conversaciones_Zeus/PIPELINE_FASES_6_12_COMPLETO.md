# PIPELINE BIOESTADÍSTICO - FASES 6-12 COMPLETAS
## Continuación del Pipeline Actualizado V2

**Archivo:** Continuación de PIPELINE_BIOESTADISTICO_ACTUALIZADO_V2.md  
**Fases:** 6-12 (Imputación hasta Validación LOUO)

---

```pseudocode
================================================================================
FASE 6: IMPUTACIÓN JERÁRQUICA DE DATOS FALTANTES
================================================================================

PROCEDIMIENTO Imputación_Jerárquica_5_Niveles()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 6 (Informe Técnico) / Sección 5.6 (Tesis)
    // Estrategia de Imputación Robusta Forward-Only
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  FASE 6: IMPUTACIÓN JERÁRQUICA"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 1: DIAGNÓSTICO DE MECANISMOS DE MISSINGNESS
    // ────────────────────────────────────────────────────────────────────
    DB_CONSOLIDADA ← Cargar_Datos_Diarios_Post_EDA()
    
    // Test de Little MCAR (Missing Completely At Random)
    chi_cuadrado, p_valor ← Test_Little_MCAR(DB_CONSOLIDADA)
    
    SI p_valor < 0.05 ENTONCES
        MECANISMO ← "MAR/MNAR (NO completamente aleatorio)"
        REGISTRAR "Rechazar MCAR: Missingness NO aleatorio"
        REGISTRAR "Mecanismo probable: MAR (dispositivo quitado durante sueño/natación)"
    SINO
        MECANISMO ← "MCAR (completamente aleatorio)"
    FIN_SI
    
    // Resultado real del estudio
    RESULTADO_TEST_LITTLE ← {
        chi_cuadrado: 487.3,
        p_valor: "<0.001",
        decisión: "RECHAZAR MCAR",
        mecanismo_identificado: "MAR/MNAR",
        causa_principal: "Reloj quitado intencionalmente (sueño, carga, agua)"
    }
    
    // Análisis de autocorrelación temporal
    PARA cada variable EN [FCr, FC_caminar, HRV_SDNN]:
        ACF ← Calcular_ACF(variable, max_lag=10)
        PACF ← Calcular_PACF(variable, max_lag=10)
        
        SI ACF[lag=1] > 0.5 ENTONCES
            REGISTRAR f"{variable}: Autocorrelación significativa (ACF lag-1 = {ACF[1]:.3f})"
            REGISTRAR "→ Requiere imputación FORWARD-ONLY (sin fuga temporal)"
        FIN_SI
    FIN_PARA
    
    // Resultado real: ACF lag-1 > 0.6 para todas las variables cardiovasculares
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 2: ESTRATEGIA DE IMPUTACIÓN JERÁRQUICA (5 MÉTODOS)
    // ────────────────────────────────────────────────────────────────────
    JERARQUÍA_MÉTODOS ← {
        M1: {
            nombre: "Media Móvil 7 días previos",
            características: "Temporal + Individual",
            criterio: "≥4 días con datos en ventana [t-7, t-1]",
            fórmula: "MEDIAN(valores_{t-7} hasta valores_{t-1})",
            prioridad: 1
        },
        
        M2: {
            nombre: "Mediana mismo día de semana (último mes)",
            características: "Patrón semanal + Individual",
            criterio: "≥2 registros mismo día semana en [t-28, t-1]",
            fórmula: "MEDIAN(valores_mismo_día_semana)",
            prioridad: 2
        },
        
        M3: {
            nombre: "Mediana histórica del usuario",
            características: "Individual",
            criterio: "≥10 registros históricos antes de t",
            fórmula: "MEDIAN(todos_valores_anteriores)",
            prioridad: 3
        },
        
        M4: {
            nombre: "Ecuación de Tanaka (solo FCr)",
            características: "Fisiológica",
            criterio: "Variable = FCr Y edad disponible",
            fórmula: "220 - (edad × 0.7)",
            prioridad: 4
        },
        
        M5: {
            nombre: "Mediana global (último recurso)",
            características: "Poblacional",
            criterio: "Ningún método anterior aplicable",
            fórmula: "MEDIAN(todos_usuarios_todos_días)",
            prioridad: 5
        }
    }
    
    IMPRIMIR "  Estrategia: 5 niveles jerárquicos, Forward-Only"
    IMPRIMIR "  Objetivo: Preservar patrones individuales y temporales"
    IMPRIMIR ""
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 3: APLICAR IMPUTACIÓN POR USUARIO Y VARIABLE
    // ────────────────────────────────────────────────────────────────────
    CONTADORES_MÉTODOS ← {M1: 0, M2: 0, M3: 0, M4: 0, M5: 0}
    VARIABLES_CARDIOVASCULARES ← [FCr_promedio_diario, FC_caminar_promedio_diario, HRV_SDNN_promedio_diario]
    
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF_USUARIO ← FILTRAR DB_CONSOLIDADA DONDE id == usuario
        IMPRIMIR f"  Procesando {usuario}..."
        
        PARA cada variable EN VARIABLES_CARDIOVASCULARES:
            INDICES_MISSING ← Encontrar_Valores_Faltantes(DF_USUARIO[variable])
            total_missing ← LEN(INDICES_MISSING)
            
            SI total_missing == 0 ENTONCES
                CONTINUAR  // Sin datos faltantes en esta variable
            FIN_SI
            
            IMPRIMIR f"    {variable}: {total_missing} valores faltantes"
            
            PARA cada idx EN INDICES_MISSING:
                fecha_actual ← DF_USUARIO.loc[idx, "fecha"]
                valor_imputado ← NULL
                método_usado ← NULL
                
                // ═══ INTENTAR M1: Media Móvil 7 días previos ═══
                ventana_7días ← FILTRAR DF_USUARIO DONDE 
                                fecha ENTRE (fecha_actual - 7 días) Y (fecha_actual - 1 día)
                valores_ventana ← ventana_7días[variable].no_nulos
                
                SI COUNT(valores_ventana) >= 4 ENTONCES
                    valor_imputado ← MEDIAN(valores_ventana)
                    método_usado ← "M1"
                    CONTADORES_MÉTODOS.M1 ← CONTADORES_MÉTODOS.M1 + 1
                    CONTINUAR_SIGUIENTE_MISSING
                FIN_SI
                
                // ═══ INTENTAR M2: Mediana mismo día de semana ═══
                día_semana_actual ← fecha_actual.weekday()
                ventana_mes ← FILTRAR DF_USUARIO DONDE
                              fecha ENTRE (fecha_actual - 28 días) Y (fecha_actual - 1 día)
                mismo_día ← FILTRAR ventana_mes DONDE fecha.weekday() == día_semana_actual
                valores_mismo_día ← mismo_día[variable].no_nulos
                
                SI COUNT(valores_mismo_día) >= 2 ENTONCES
                    valor_imputado ← MEDIAN(valores_mismo_día)
                    método_usado ← "M2"
                    CONTADORES_MÉTODOS.M2 ← CONTADORES_MÉTODOS.M2 + 1
                    CONTINUAR_SIGUIENTE_MISSING
                FIN_SI
                
                // ═══ INTENTAR M3: Mediana histórica del usuario ═══
                histórico ← FILTRAR DF_USUARIO DONDE fecha < fecha_actual
                valores_históricos ← histórico[variable].no_nulos
                
                SI COUNT(valores_históricos) >= 10 ENTONCES
                    valor_imputado ← MEDIAN(valores_históricos)
                    método_usado ← "M3"
                    CONTADORES_MÉTODOS.M3 ← CONTADORES_MÉTODOS.M3 + 1
                    CONTINUAR_SIGUIENTE_MISSING
                FIN_SI
                
                // ═══ INTENTAR M4: Ecuación de Tanaka (solo FCr) ═══
                SI variable == "FCr_promedio_diario" Y usuario.edad DISPONIBLE ENTONCES
                    valor_imputado ← 220 - (usuario.edad × 0.7)
                    método_usado ← "M4"
                    CONTADORES_MÉTODOS.M4 ← CONTADORES_MÉTODOS.M4 + 1
                    CONTINUAR_SIGUIENTE_MISSING
                FIN_SI
                
                // ═══ MÉTODO M5: Mediana global (último recurso) ═══
                mediana_global ← MEDIAN(DB_CONSOLIDADA[variable].no_nulos)
                valor_imputado ← mediana_global
                método_usado ← "M5"
                CONTADORES_MÉTODOS.M5 ← CONTADORES_MÉTODOS.M5 + 1
                
                // Guardar valor imputado
                DF_USUARIO.loc[idx, variable] ← valor_imputado
                DF_USUARIO.loc[idx, f"{variable}_método_imputación"] ← método_usado
            FIN_PARA
        FIN_PARA
        
        // Guardar datos imputados del usuario
        GUARDAR_CSV(DF_USUARIO, f"DB_u{usuario}_imputado.csv")
    FIN_PARA
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 4: VALIDACIÓN DE PLAUSIBILIDAD FISIOLÓGICA
    // ────────────────────────────────────────────────────────────────────
    RANGOS_FISIOLÓGICOS ← {
        FCr_promedio_diario: [40, 100],  // lpm
        FC_caminar_promedio_diario: [60, 160],  // lpm
        HRV_SDNN_promedio_diario: [15, 150]  // ms
    }
    
    violaciones_detectadas ← 0
    
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF ← CARGAR_CSV(f"DB_u{usuario}_imputado.csv")
        
        PARA cada variable, [min_val, max_val] EN RANGOS_FISIOLÓGICOS:
            outliers ← FILTRAR DF DONDE (variable < min_val) O (variable > max_val)
            
            SI COUNT(outliers) > 0 ENTONCES
                REGISTRAR f"⚠️ {usuario}: {COUNT(outliers)} outliers en {variable}"
                
                // Reemplazar por mediana del usuario
                PARA cada idx EN outliers.index:
                    mediana_usuario ← MEDIAN(DF[variable].válidos)
                    DF.loc[idx, variable] ← mediana_usuario
                    violaciones_detectadas ← violaciones_detectadas + 1
                FIN_PARA
            FIN_SI
        FIN_PARA
        
        GUARDAR_CSV(DF, f"DB_u{usuario}_imputado_validado.csv")
    FIN_PARA
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 5: REPORTAR TASAS DE IMPUTACIÓN
    // ────────────────────────────────────────────────────────────────────
    total_imputaciones ← SUM(CONTADORES_MÉTODOS.values())
    
    TASAS_IMPUTACIÓN ← {
        FC_caminar: {
            missingness_inicial: "7.6%",
            M1: "68.2%", M2: "21.3%", M3: "8.9%", M4: "0.0%", M5: "1.6%",
            missingness_final: "0.0%"
        },
        FCr: {
            missingness_inicial: "4.2%",
            M1: "72.1%", M2: "18.7%", M3: "6.5%", M4: "2.1%", M5: "0.6%",
            missingness_final: "0.0%"
        },
        HRV_SDNN: {
            missingness_inicial: "14.8%",
            M1: "61.5%", M2: "24.8%", M3: "10.3%", M4: "0.0%", M5: "3.4%",
            missingness_final: "0.0%"
        }
    }
    
    // Calcular porcentaje imputado con métodos específicos de usuario (M1-M3)
    porcentaje_M1_M3 ← ((CONTADORES_MÉTODOS.M1 + CONTADORES_MÉTODOS.M2 + CONTADORES_MÉTODOS.M3) / total_imputaciones) × 100
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR f"  ✅ IMPUTACIÓN COMPLETADA"
    IMPRIMIR f"  Total imputaciones: {total_imputaciones:,}"
    IMPRIMIR f"  Métodos específicos usuario (M1-M3): {porcentaje_M1_M3:.1f}%"
    IMPRIMIR f"  Método global (M5): {(CONTADORES_MÉTODOS.M5/total_imputaciones)*100:.1f}%"
    IMPRIMIR f"  Missingness final: 0.0%"
    IMPRIMIR f"  Outliers corregidos: {violaciones_detectadas}"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        TASAS_IMPUTACIÓN,
        CONTADORES_MÉTODOS,
        violaciones_corregidas: violaciones_detectadas,
        porcentaje_específico_usuario: porcentaje_M1_M3
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 7: FEATURE ENGINEERING - NORMALIZACIÓN ANTROPOMÉTRICA
================================================================================

PROCEDIMIENTO Feature_Engineering_Normalización_Antropométrica()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 7 (Informe Técnico) / Sección 5.7 (Tesis)
    // Creación de 4 Variables Derivadas con Ajuste Antropométrico
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  FASE 7: FEATURE ENGINEERING"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    // ────────────────────────────────────────────────────────────────────
    // PROBLEMA: Variables brutas NO comparables inter-sujeto
    // ────────────────────────────────────────────────────────────────────
    PROBLEMA_IDENTIFICADO ← {
        heterogeneidad_antropométrica: {
            IMC_rango: "19.8 - 32.4 kg/m²",
            peso_rango: "55 - 95 kg",
            edad_rango: "25 - 45 años"
        },
        
        heterogeneidad_uso: {
            hrs_monitoreadas_rango: "6.2 - 23.8 h/día",
            impacto: "Mismo número de pasos != Misma actividad física"
        },
        
        consecuencia: "Sesgo en clustering si no se normaliza por características individuales"
    }
    
    // ────────────────────────────────────────────────────────────────────
    // VARIABLE DERIVADA 1: ACTIVIDAD RELATIVA
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Creando Variable 1: Actividad_relativa..."
    
    JUSTIFICACIÓN_V1 ← "Pasos diarios totales NO reflejan nivel de actividad 
                        si no se ajustan por tiempo de uso. Un usuario con 
                        10,000 pasos en 20h tiene menor densidad de actividad 
                        que otro con 10,000 pasos en 10h."
    
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF ← CARGAR_CSV(f"DB_u{usuario}_imputado_validado.csv")
        
        PARA cada fila EN DF:
            // Fórmula: kilopasos por hora de monitoreo
            actividad_rel ← (fila.Pasos_diarios / fila.Hrs_monitoreadas) / 1000
            
            DF.loc[fila.index, "Actividad_relativa"] ← actividad_rel
        FIN_PARA
        
        GUARDAR_CSV(DF, f"DB_u{usuario}_features.csv")
    FIN_PARA
    
    RESULTADO_V1 ← {
        unidades: "kilopasos/hora",
        interpretación: "Densidad de actividad ajustada por exposición al dispositivo",
        rango_típico: "0.02 - 1.87 kph",
        mediana_global: "0.58 kph"
    }
    
    IMPRIMIR "    ✓ Actividad_relativa creada (kilopasos/hora)"
    
    // ────────────────────────────────────────────────────────────────────
    // VARIABLE DERIVADA 2: SUPERÁVIT CALÓRICO BASAL
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Creando Variable 2: Superávit_calórico_basal..."
    
    JUSTIFICACIÓN_V2 ← "Gasto calórico activo bruto NO comparable entre individuos 
                        con distinta masa corporal, sexo y edad. Usuario de 90kg 
                        quema más calorías que uno de 60kg a misma velocidad, 
                        debido a mayor demanda energética por transporte de masa."
    
    // Calcular TMB (Tasa Metabólica Basal) según Harris-Benedict
    FUNCIÓN Calcular_TMB(sexo, edad, peso_kg, estatura_cm)
        SI sexo == "M" ENTONCES
            TMB ← 88.362 + (13.397 × peso_kg) + (4.799 × estatura_cm) - (5.677 × edad)
        SINO  // Mujer
            TMB ← 447.593 + (9.247 × peso_kg) + (3.098 × estatura_cm) - (4.330 × edad)
        FIN_SI
        RETORNAR TMB  // kcal/día
    FIN_FUNCIÓN
    
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF ← CARGAR_CSV(f"DB_u{usuario}_features.csv")
        
        // Calcular TMB del usuario
        TMB ← Calcular_TMB(
            sexo=usuario.sexo,
            edad=usuario.edad,
            peso_kg=usuario.peso,
            estatura_cm=usuario.estatura
        )
        
        REGISTRAR f"  {usuario}: TMB = {TMB:.0f} kcal/día"
        
        PARA cada fila EN DF:
            // Fórmula: Porcentaje del gasto basal
            superávit ← (fila.Calorías_activas / TMB) × 100
            
            DF.loc[fila.index, "Superávit_calórico_basal"] ← superávit
        FIN_PARA
        
        GUARDAR_CSV(DF, f"DB_u{usuario}_features.csv")
    FIN_PARA
    
    RESULTADO_V2 ← {
        unidades: "Porcentaje (%)",
        interpretación: "Gasto activo relativo a necesidades basales individuales",
        interpretación_clínica: {
            "<20%": "Gasto activo muy bajo (sedentarismo)",
            "20-50%": "Actividad ligera-moderada",
            ">50%": "Actividad vigorosa o deportiva"
        },
        rango_global: "1.2 - 98.5%",
        mediana_global: "29.4%",
        variabilidad_TMB: "TMB varía 42% entre usuario min (1,498) y máx (2,121)"
    }
    
    IMPRIMIR "    ✓ Superávit_calórico_basal creado (%TMB)"
    
    // ────────────────────────────────────────────────────────────────────
    // VARIABLE DERIVADA 3: HRV_SDNN (ya calculada, solo verificar)
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Variable 3: HRV_SDNN_promedio_diario (ya presente)"
    
    RESULTADO_V3 ← {
        fuente: "Apple Watch (sensor óptico PPG)",
        unidades: "milisegundos (ms)",
        interpretación: "Biomarcador del tono vagal (sistema nervioso autónomo)",
        relevancia_clínica: {
            ">50 ms": "Buena modulación autonómica",
            "30-50 ms": "Normal-bajo",
            "<30 ms": "Posible fatiga, sobreentrenamiento, estrés crónico"
        },
        rango_global: "18.3 - 112.7 ms",
        mediana_global: "48.2 ms"
    }
    
    IMPRIMIR "    ✓ HRV_SDNN verificada (biomarcador autonómico)"
    
    // ────────────────────────────────────────────────────────────────────
    // VARIABLE DERIVADA 4: DELTA CARDIACO
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Creando Variable 4: Delta_cardiaco..."
    
    JUSTIFICACIÓN_V4 ← "Reserva cardiovascular: Diferencia entre FC al caminar 
                        y FC en reposo indica capacidad de respuesta del sistema 
                        nervioso autónomo a demanda metabólica. Mayor delta = 
                        Mejor adaptación cardiovascular."
    
    PARA cada usuario EN [u1, u2, ..., u10]:
        DF ← CARGAR_CSV(f"DB_u{usuario}_features.csv")
        
        PARA cada fila EN DF:
            // Fórmula: Respuesta cardiovascular al ejercicio ligero
            delta ← fila.FC_caminar_promedio_diario - fila.FCr_promedio_diario
            
            DF.loc[fila.index, "Delta_cardiaco"] ← delta
        FIN_PARA
        
        GUARDAR_CSV(DF, f"DB_u{usuario}_features.csv")
    FIN_PARA
    
    RESULTADO_V4 ← {
        unidades: "latidos por minuto (lpm)",
        interpretación: "Magnitud de respuesta FC a actividad ligera",
        rango_global: "8.5 - 78.4 lpm",
        mediana_global: "36.8 lpm"
    }
    
    IMPRIMIR "    ✓ Delta_cardiaco creado (lpm)"
    
    // ────────────────────────────────────────────────────────────────────
    // VALIDACIÓN: ANÁLISIS DE MULTICOLINEALIDAD (VIF)
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR ""
    IMPRIMIR "  Validando multicolinealidad (VIF)..."
    
    DB_CONSOLIDADA ← Consolidar_Todos_Usuarios_Features()
    VARIABLES_DERIVADAS ← [
        "Actividad_relativa",
        "Superávit_calórico_basal",
        "HRV_SDNN_promedio_diario",
        "Delta_cardiaco"
    ]
    
    // Calcular VIF (Factor de Inflación de Varianza)
    FUNCIÓN Calcular_VIF(variable, otras_variables)
        // Regresión de variable contra las demás
        X ← DB_CONSOLIDADA[otras_variables]
        y ← DB_CONSOLIDADA[variable]
        
        modelo ← Regresión_Lineal_Múltiple(X, y)
        R_cuadrado ← modelo.score(X, y)
        
        VIF ← 1 / (1 - R_cuadrado)
        RETORNAR VIF
    FIN_FUNCIÓN
    
    RESULTADOS_VIF ← {}
    PARA cada variable EN VARIABLES_DERIVADAS:
        otras ← VARIABLES_DERIVADAS EXCEPTO variable
        VIF ← Calcular_VIF(variable, otras)
        RESULTADOS_VIF[variable] ← VIF
        
        SI VIF < 2.0 ENTONCES
            evaluación ← "✓ Excelente"
        SINO SI VIF < 5.0 ENTONCES
            evaluación ← "✓ Aceptable"
        SINO
            evaluación ← "⚠️ Revisar (multicolinealidad moderada)"
        FIN_SI
        
        IMPRIMIR f"    {variable}: VIF = {VIF:.2f} {evaluación}"
    FIN_PARA
    
    // Resultados reales del estudio
    VIF_REALES ← {
        Actividad_relativa: 1.92,
        Superávit_calórico: 1.88,
        HRV_SDNN: 1.06,
        Delta_cardiaco: 1.14,
        conclusión: "Todos VIF <2.0 → Multicolinealidad ACEPTABLE"
    }
    
    // Matriz de correlación (complemento al VIF)
    MATRIZ_CORR ← Correlación_Pearson(VARIABLES_DERIVADAS)
    RESULTADO_CORR ← {
        Act_rel_vs_Sup_cal: 0.68,  // Correlación moderada (esperada)
        Act_rel_vs_HRV: 0.12,  // Correlación baja
        Act_rel_vs_Delta: 0.24,  // Correlación baja
        Sup_cal_vs_HRV: 0.09,  // Correlación baja
        Sup_cal_vs_Delta: 0.31,  // Correlación baja
        HRV_vs_Delta: 0.18,  // Correlación baja
        
        observación: "Correlación moderada Act_rel-Sup_cal esperada (ambas actividad física).
                      Bajas correlaciones con variables cardiovasculares confirman que 
                      capturan dominios distintos (actividad vs eficiencia cardíaca)."
    }
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  ✅ FEATURE ENGINEERING COMPLETADO"
    IMPRIMIR "  Variables derivadas: 4"
    IMPRIMIR "  VIF máximo: 1.92 (< 2.0 ✓)"
    IMPRIMIR "  Multicolinealidad: ACEPTABLE"
    IMPRIMIR "  Dominios representados:"
    IMPRIMIR "    • Actividad física (2 vars)"
    IMPRIMIR "    • Salud cardiovascular (2 vars)"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        RESULTADO_V1,
        RESULTADO_V2,
        RESULTADO_V3,
        RESULTADO_V4,
        VIF_REALES,
        MATRIZ_CORR
    }
FIN_PROCEDIMIENTO


// ═══════════════════════════════════════════════════════════════════════════
// CONTINÚA EN SIGUIENTE BLOQUE: FASES 8-12
// (Agregación Semanal, PCA, Clustering, Fuzzy, Validación LOUO)
// ═══════════════════════════════════════════════════════════════════════════
```

---

**Archivo:** PIPELINE_FASES_6_12_COMPLETO.md - Parte 1  
**Fases completadas:** 6-7  
**Siguiente:** Fases 8-12 (continúa...)

