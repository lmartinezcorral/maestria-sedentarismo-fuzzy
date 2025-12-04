# PIPELINE BIOESTADÍSTICO COMPLETO - VERSIÓN ACTUALIZADA V2
## Análisis Cronológico de Datos Biométricos para Clasificación de Sedentarismo

**Proyecto:** Tesis MFIPS - Modelo de Evaluación del Comportamiento Sedentario  
**Universidad:** Universidad Autónoma de Chihuahua (UACH)  
**Facultad:** Medicina y Ciencias Biomédicas  
**Autor:** Luis Ángel Martínez Corral  
**Director:** Dr. Abimael Guzmán Pando  
**Codirector:** Dr. David Ricardo López Flores  
**Asesora:** Dra. Celia María Quiñonez

**Registro Interno:** CI-088-24  
**Primer Dictamen:** 17 febrero 2025, Oficio SIP/116/25  
**Aprobación Ética:** 21 agosto 2025, Registro CI-088-24  
**Convocatoria Lanzada:** 21 agosto 2025

---

## NOTA IMPORTANTE: ORGANIZACIÓN DE CAPÍTULOS

```
MATERIALES Y MÉTODOS (Capítulo 5):
├── Diseño del estudio hasta Sistema Difuso (diseño metodológico)
└── NO incluye resultados numéricos finales

RESULTADOS (Capítulo 6):
├── Desempeño del Sistema Difuso Mamdani
└── Validación LOUO con métricas
```

---

## PSEUDOCÓDIGO DEL PIPELINE COMPLETO

```pseudocode
================================================================================
FASE 1: PLANTEAMIENTO Y DISEÑO DEL ESTUDIO
================================================================================

PROCEDIMIENTO Planteamiento_Inicial()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 1 y 2: Planteamiento del Problema y Diseño Metodológico
    // ═══════════════════════════════════════════════════════════════════════
    
    // ────────────────────────────────────────────────────────────────────
    // HIPÓTESIS INICIAL (Pre-pivote)
    // ────────────────────────────────────────────────────────────────────
    HIPÓTESIS_H0 ← "Existe relación inversa y medible entre Comportamiento Sedentario 
                    objetivo (CS_obj) cuantificado por wearables y Calidad de Vida 
                    (CVRS) evaluada por SF-36, modelable mediante ANN"
    
    OBJETIVO_PRIMARIO_INICIAL ← "Predecir CVRS (SF-36) desde datos biométricos con ANN"
    
    // ────────────────────────────────────────────────────────────────────
    // TIPO DE INVESTIGACIÓN Y ENFOQUE
    // ────────────────────────────────────────────────────────────────────
    DISEÑO_ESTUDIO ← {
        enfoque: "Cuantitativo",
        tipo: "Exploratorio-correlacional",
        temporalidad: "Longitudinal retrospectivo multianual",
        diseño: "Observacional de un solo corte",
        grupo_control: FALSE,
        paradigma: "BYOD (Bring Your Own Device)",
        
        componentes: {
            exploratorio: "Descubrimiento de patrones en vida libre",
            correlacional: "Validación concordancia Modelo Difuso ↔ Clustering",
            paradoja_HRV: "Interacción multivariada de biomarcadores no capturada univariadamente"
        },
        
        características: [
            "No experimental",
            "Sin intervención en condiciones de los participantes",
            "Sin grupo control",
            "Recolección de datos en un momento específico (retrospectivo)",
            "Análisis de relaciones sin manipulación intencional"
        ]
    }
    
    // ────────────────────────────────────────────────────────────────────
    // APROBACIONES ÉTICAS Y ADMINISTRATIVAS
    // ────────────────────────────────────────────────────────────────────
    APROBACIONES ← {
        comité_investigación: {
            fecha: "17 febrero 2025",
            oficio: "SIP/116/25",
            registro: "CI-088-24",
            estatus: "APROBADO"
        },
        
        comité_ética: {
            fecha_aprobación: "21 agosto 2025",
            registro: "CI-088-24",
            estatus: "APROBADO"
        },
        
        convocatoria: {
            fecha_lanzamiento: "21 agosto 2025",
            canales: ["Redes sociales facultad", "Correo institucional", "Contacto directo"]
        }
    }
    
    // ────────────────────────────────────────────────────────────────────
    // SELECCIÓN DEL DISPOSITIVO WEARABLE
    // ────────────────────────────────────────────────────────────────────
    // COMPARACIÓN INICIAL: Características generales de wearables
    COMPARACIÓN_CARACTERÍSTICAS ← Evaluar_Características_Wearables([
        Sensores: [Acelerómetro_3_ejes, PPG, GPS, Giroscopio],
        Precisión: [Validación_científica, Concordancia_gold_standard],
        Plataforma: [API_disponible, SDK_disponible, Exportación_datos],
        Uso: [Batería, Resistencia_agua, Comodidad]
    ])
    
    // COMPARACIÓN ESPECÍFICA: Marcas de mercado
    MATRIZ_DECISIÓN ← Evaluar_Wearables_Marcas({
        candidatos: [AppleWatch, Fitbit, Garmin, MiBand],
        
        criterios_ponderados: {
            validez_científica: {peso: 35%, subcriteria: [
                "Publicaciones Q1/Q2 validando sensores",
                "Concordancia con gold-standard (>90% FC, pasos)",
                "Consistencia inter-versión hardware"
            ]},
            
            exportabilidad_datos: {peso: 30%, subcriteria: [
                "API robusta para investigación",
                "SDK nativo disponible",
                "Formato datos estructurado (XML/JSON)",
                "Acceso a datos históricos completos"
            ]},
            
            consistencia_hardware: {peso: 20%, subcriteria: [
                "Uniformidad sensores entre versiones",
                "Estabilidad temporal de mediciones",
                "Ecosistema cerrado vs abierto"
            ]},
            
            penetración_mercado: {peso: 15%, subcriteria: [
                "Disponibilidad en México",
                "Costo promedio",
                "Facilita reclutamiento BYOD"
            ]}
        },
        
        resultados: {
            AppleWatch: {
                score: 9.2/10,
                validez: 10,  // Múltiples estudios Q1 (Stahl 2016, Shcherbina 2017)
                exportabilidad: 10,  // HealthKit XML completo
                consistencia: 9,  // Ecosistema cerrado Apple
                penetración: 8,  // Alta en población urbana
                seleccionado: TRUE
            },
            Fitbit: {score: 7.5/10, seleccionado: FALSE},
            Garmin: {score: 7.8/10, seleccionado: FALSE},
            MiBand: {score: 5.1/10, seleccionado: FALSE}
        }
    })
    
    DISPOSITIVO_SELECCIONADO ← AppleWatch
    
    JUSTIFICACIÓN_APPLE ← {
        a_favor: [
            "Ecosistema cerrado → Mayor consistencia entre Series 3-9",
            "HealthKit SDK robusto para investigación (Swift disponible)",
            "Exportación manual de datos históricos completos (export.zip)",
            "Validación científica extensa (>50 papers Q1/Q2)",
            "Concordancia >90% con gold-standard para FC, pasos",
            "Alta penetración en población objetivo (estudiantes/profesores facultad)",
            "Uniformidad y calidad de sensores mantenida en todas las versiones"
        ],
        
        limitaciones_reconocidas: [
            "SESGO: Solo usuarios Apple Watch (excluye Android/otros wearables)",
            "Barrera económica: Costo $300-800 USD limita representatividad poblacional",
            "Método manual de extracción (no app nativa en Swift por limitaciones técnicas)",
            "Prototipo fuera del lenguaje nativo de Apple (Python vs Swift)",
            "Heterogeneidad entre versiones en métricas avanzadas:",
            "  - Sueño: Series 3-5 (estimación básica) vs Series 6+ (fases detalladas)",
            "  - HRV: Series 4+ (sensor óptico mejorado) vs Series 3 (limitado)",
            "  - EKG: Solo Series 4+",
            "  - VO2max: Series 3+ pero algoritmos mejorados en Series 6+",
            "  - Physical Effort: Solo watchOS 9+ (Series 4+)"
        ],
        
        decisión_final: "A pesar de limitaciones, Apple Watch seleccionado por balance 
                         óptimo entre validez científica, exportabilidad y disponibilidad"
    }
    
    // ────────────────────────────────────────────────────────────────────
    // DISEÑO DE LA COHORTE Y TAMAÑO MUESTRAL
    // ────────────────────────────────────────────────────────────────────
    
    // Justificación paradigma de muestras densamente monitoreadas
    PARADIGMA_LONGITUDINAL ← "Intensive Longitudinal Designs (Bolger & Laurenceau, 2013)"
    
    // Fórmula de poder estadístico
    FUNCIÓN Calcular_Poder_Estadístico(N, n_obs_promedio)
        // En diseños longitudinales densos, el poder NO proviene de N sujetos,
        // sino del número TOTAL de observaciones temporales
        Poder ∝ N × n̄_obs/sujeto
        
        n_total ← N × n_obs_promedio
        
        SI n_total >= 500 ENTONCES
            RETORNAR "Suficiente para clustering estable y validación LOUO"
        SINO SI n_total >= 1000 ENTONCES
            RETORNAR "Excelente para modelado multivariado robusto"
        SINO
            RETORNAR "Insuficiente - Considerar extender seguimiento o N"
        FIN_SI
    FIN_FUNCIÓN
    
    N_OBJETIVO ← Calcular_Tamaño_Muestral_Justificado(
        paradigma: "Intensive Longitudinal Design",
        n_total_objetivo: 1000,  // Mínimo para clustering + validación LOUO
        T_seguimiento_esperado: 130,  // semanas promedio estimadas
        N_mínimo: TECHO(1000 / 130) = 8,  // Redondeo hacia arriba
        N_seleccionado: 10  // Por encima del mínimo para robustez
    )
    
    RESULTADO_TAMAÑO_MUESTRAL ← {
        N_participantes: 10,
        justificación_estadística: {
            fórmula: "Poder ∝ N × n̄_obs/sujeto",
            N: 10,
            n_obs_promedio: 133.7,  // semanas por usuario (real final)
            n_total: 1337,  // semanas válidas totales
            mínimo_requerido: 500,  // Para clustering estable
            mínimo_ideal: 1000,  // Para validación LOUO robusta
            cumple_criterio: TRUE,
            referencia: "Bolger & Laurenceau (2013), Alin et al. (2020)"
        },
        
        características_finales: {
            sexo: "5M / 5F (balanceado)",
            edad: "34.2 ± 6.7 años (rango 25-45)",
            IMC: "24.8 ± 3.2 kg/m²",
            seguimiento_mediana: 131,  // semanas
            seguimiento_rango: "7-298 semanas",
            días_totales: 9185,
            semanas_generadas: 1385,
            semanas_válidas: 1337  // Criterio ≥5 días/semana
        }
    }
    
    // ────────────────────────────────────────────────────────────────────
    // CRITERIOS DE SELECCIÓN
    // ────────────────────────────────────────────────────────────────────
    POBLACIÓN_OBJETIVO ← {
        tipo: "Conveniencia (no probabilística)",
        universo: "Alumnos y personal de la Facultad de Medicina y Ciencias Biomédicas, UACH",
        rango_edad: "18-65 años",
        ambos_sexos: TRUE
    }
    
    CRITERIOS_INCLUSIÓN ← [
        "Propiedad de Apple Watch Series 3 o superior",
        "Uso continuo del dispositivo por ≥6 meses previos",
        "Capacidad ambulatoria sin limitaciones severas",
        "Disponibilidad para exportar datos históricos desde su dispositivo",
        "Firma de consentimiento informado de manera digital",
        "Edad 18-65 años"
    ]
    
    CRITERIOS_EXCLUSIÓN ← [
        "Edad <18 o >65 años",
        "Sin dispositivo Apple Watch o Series <3",
        "Uso del dispositivo <6 meses (sesgo de adaptación)",
        "Limitaciones severas de movilidad",
        "Negativa o retiro de consentimiento",
        "Datos exportables con <80% adherencia/completitud"
    ]
    
    RETORNAR {
        DISEÑO_ESTUDIO,
        APROBACIONES,
        DISPOSITIVO_SELECCIONADO,
        JUSTIFICACIÓN_APPLE,
        N_OBJETIVO,
        RESULTADO_TAMAÑO_MUESTRAL,
        POBLACIÓN_OBJETIVO,
        CRITERIOS_INCLUSIÓN,
        CRITERIOS_EXCLUSIÓN
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 2: CONVOCATORIA Y RECOLECCIÓN DE DATOS
================================================================================

PROCEDIMIENTO Convocatoria_y_Recoleccion()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 3: Protocolo de Convocatoria y Recepción de Datos
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  INICIO DE CONVOCATORIA - 21 AGOSTO 2025"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    CANDIDATOS_CONVOCADOS ← 0
    PARTICIPANTES_INCLUIDOS ← []
    
    PARA cada candidato EN Convocatoria_Abierta():
        CANDIDATOS_CONVOCADOS ← CANDIDATOS_CONVOCADOS + 1
        
        // ────────────────────────────────────────────────────────────────
        // PASO 1: VERIFICAR CRITERIOS DE INCLUSIÓN/EXCLUSIÓN
        // ────────────────────────────────────────────────────────────────
        cumple_criterios ← Verificar_Criterios_Inclusión(candidato)
        
        SI NO cumple_criterios ENTONCES
            REGISTRAR_EXCLUSIÓN(candidato, motivo_exclusión)
            CONTINUAR  // Pasar al siguiente candidato
        FIN_SI
        
        // ────────────────────────────────────────────────────────────────
        // PASO 2: SESIÓN PRESENCIAL INFORMATIVA
        // ────────────────────────────────────────────────────────────────
        AGENDAR_SESIÓN_PRESENCIAL(candidato)
        
        EN_SESIÓN_PRESENCIAL:
            // Explicar el proyecto
            PRESENTAR_Información_Proyecto(candidato)
            PRESENTAR_Hoja_Información(candidato)
            
            // Explicar riesgos y beneficios
            EXPLICAR_Privacidad_Y_Anonimización()
            EXPLICAR_Uso_De_Datos()
            
            // Entregar instructivo de exportación
            ENTREGAR_Instructivo_Exportación_AppleHealth()
            
            // Solicitar consentimiento informado
            CONSENTIMIENTO ← Solicitar_Consentimiento_Informado_Digital(candidato)
            
            SI CONSENTIMIENTO == FALSE ENTONCES
                REGISTRAR "Candidato rechazó participar"
                EXCLUIR candidato
                CONTINUAR
            FIN_SI
        FIN_EN_SESIÓN
        
        // ────────────────────────────────────────────────────────────────
        // PASO 3: EXPORTACIÓN DE DATOS POR PARTE DEL PARTICIPANTE
        // ────────────────────────────────────────────────────────────────
        INSTRUCCIONES_EXPORTACIÓN ← {
            paso_1: "Abrir app 'Salud' en iPhone",
            paso_2: "Tocar foto de perfil (esquina superior derecha)",
            paso_3: "Desplazarse hasta 'Exportar datos de salud'",
            paso_4: "Tocar 'Exportar' → Se genera export.zip",
            paso_5: "Compartir archivo via:",
            opciones: ["Correo encriptado institucional", "USB físico", "AirDrop seguro"],
            tamaño_esperado: "50 MB - 2 GB (dependiendo de historial)"
        }
        
        ESPERANDO_EXPORTACIÓN:
            ARCHIVO_ZIP ← Esperar_Recepción_Export_Zip(candidato)
            
            // Validar integridad del archivo
            SI NOT Validar_Integridad_ZIP(ARCHIVO_ZIP) ENTONCES
                SOLICITAR_Reenvío(candidato, "Archivo corrupto o incompleto")
                CONTINUAR_ESPERANDO
            FIN_SI
            
            // Verificar tamaño y contenido
            SI Tamaño(ARCHIVO_ZIP) < 10_MB ENTONCES
                ADVERTIR "Archivo sospechosamente pequeño - Verificar historial"
                SOLICITAR_Confirmación_Historial(candidato)
            FIN_SI
        FIN_ESPERANDO
        
        // ────────────────────────────────────────────────────────────────
        // PASO 4: APLICACIÓN DEL CUESTIONARIO SF-36
        // ────────────────────────────────────────────────────────────────
        SF36_DATA ← Aplicar_Cuestionario_SF36(
            candidato,
            modalidad: "Presencial o Google Forms",
            versión: "Versión mexicana validada",
            dimensiones: [FF, RF, DC, SG, VT, FS, RE, SM]
        )
        
        SI SF36_DATA == INCOMPLETO ENTONCES
            REGISTRAR "Cuestionario SF-36 incompleto"
            EXCLUIR candidato
            CONTINUAR
        FIN_SI
        
        // ────────────────────────────────────────────────────────────────
        // PASO 5: CAPTURA DE DATOS ANTROPOMÉTRICOS
        // ────────────────────────────────────────────────────────────────
        DATOS_ANTROPOMÉTRICOS ← Capturar_Formulario_Digital({
            edad: candidato.edad,
            sexo_biológico: candidato.sexo,
            peso_kg: candidato.peso,
            estatura_cm: candidato.estatura,
            // Calcular IMC
            IMC: candidato.peso / (candidato.estatura/100)^2
        })
        
        // ────────────────────────────────────────────────────────────────
        // PASO 6: ANONIMIZACIÓN Y ALMACENAMIENTO SEGURO
        // ────────────────────────────────────────────────────────────────
        CODIGO_ANONIMO ← Asignar_Codigo_Usuario(candidato)
        // Formato: u1, u2, u3, ..., u10
        
        PROTOCOLO_PRIVACIDAD ← {
            anonimización: "Código usuario único (u1-u10)",
            almacenamiento: "Servidor institucional UACH",
            encriptación: "AES-256",
            acceso_restringido: "Solo equipo investigación",
            respaldo: "Backup semanal encriptado",
            retención: "5 años post-publicación (reglamento UACH)"
        }
        
        ALMACENAR_SEGURO(
            archivo_zip: ARCHIVO_ZIP,
            sf36: SF36_DATA,
            antropometría: DATOS_ANTROPOMÉTRICOS,
            código: CODIGO_ANONIMO,
            protocolo: PROTOCOLO_PRIVACIDAD
        )
        
        // Agregar a lista de participantes válidos
        PARTICIPANTES_INCLUIDOS.append({
            código: CODIGO_ANONIMO,
            fecha_inclusión: FECHA_ACTUAL,
            archivo_zip: RUTA_SEGURA
        })
    FIN_PARA
    
    // ────────────────────────────────────────────────────────────────────
    // MÉTRICAS FINALES DE CONVOCATORIA
    // ────────────────────────────────────────────────────────────────────
    RESULTADO_CONVOCATORIA ← {
        candidatos_convocados: 15,
        cumplieron_criterios: 12,
        completaron_protocolo: 10,
        
        tasa_cumplimiento_criterios: (12/15) * 100 = 80.0%,
        tasa_retención_final: (10/15) * 100 = 66.7%,
        
        motivos_exclusión: {
            sin_SF36_completo: 1,
            abandonos_voluntarios: 2,
            datos_insuficientes_<6meses: 2
        },
        
        distribución_final: {
            sexo: "5M / 5F (balanceado)",
            edad_promedio: "34.2 ± 6.7 años",
            IMC_promedio: "24.8 ± 3.2 kg/m²"
        },
        
        cumple_N_objetivo: TRUE  // N=10 alcanzado
    }
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  CONVOCATORIA COMPLETADA: N=10 PARTICIPANTES"
    IMPRIMIR "  Tasa retención: 66.7% (aceptable para BYOD)"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        PARTICIPANTES_INCLUIDOS,
        RESULTADO_CONVOCATORIA
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 3: PREPROCESAMIENTO XML → CSV (EXTRACCIÓN Y LIMPIEZA)
================================================================================

PROCEDIMIENTO Preprocesamiento_XML_a_CSV()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 3: Conversión de Datos Crudos Apple Health
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  INICIO PREPROCESAMIENTO XML → CSV"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    // ────────────────────────────────────────────────────────────────────
    // ESTRUCTURA TÍPICA DEL EXPORT.ZIP DE APPLE HEALTH
    // ────────────────────────────────────────────────────────────────────
    ESTRUCTURA_EXPORT_ZIP ← {
        archivo_principal: "export.xml",  // Contiene TODOS los datos HealthKit
        tamaño_típico: "50 MB - 2 GB (no comprimido hasta 10 GB)",
        
        estructura_XML: {
            raíz: "<HealthData locale='es_MX'>",
            elementos_principales: [
                "<Record>",  // Datos de cantidad/eventos
                "<Workout>",  // Entrenamientos
                "<ActivitySummary>",  // Resumen actividad diaria
                "<ClinicalRecord>",  // Registros clínicos (opcional)
                "<Audiogram>",  // Audiogramas (opcional)
            ],
            
            atributos_Record: {
                type: "Tipo de métrica HealthKit",
                sourceName: "Dispositivo/app que generó el dato",
                sourceVersion: "Versión del software",
                device: "Modelo específico del dispositivo",
                unit: "Unidad de medida",
                creationDate: "Fecha de creación del registro",
                startDate: "Fecha/hora inicio del evento",
                endDate: "Fecha/hora fin del evento",
                value: "Valor numérico de la métrica"
            }
        },
        
        ejemplo_estructura_XML: '
        <HealthData locale="es_MX">
          <Record type="HKQuantityTypeIdentifierStepCount"
                  sourceName="Apple Watch de Luis"
                  sourceVersion="9.6.1"
                  device="<<HKDevice: 0x..., name:Apple Watch, ...>>"
                  unit="count"
                  creationDate="2023-10-22 08:16:00 -0600"
                  startDate="2023-10-22 08:15:00 -0600"
                  endDate="2023-10-22 08:16:00 -0600"
                  value="45"/>
          <Record type="HKQuantityTypeIdentifierHeartRate"
                  sourceName="Apple Watch de Luis"
                  ...
                  value="72"
                  unit="count/min"/>
          ...
        </HealthData>
        '
    }
    
    // ────────────────────────────────────────────────────────────────────
    // SCRIPT DE TRANSFORMACIÓN: apple-health-data-parser.py
    // ────────────────────────────────────────────────────────────────────
    SCRIPT_PARSER ← {
        fuente: "https://github.com/vinayakgaur/Apple-Health-Data-Analysis",
        archivo: "apple-health-data-parser.py",
        adaptaciones: "Personalizado para métricas específicas del estudio",
        
        funcionalidad: [
            "Parse XML usando ElementTree (Python)",
            "Filtrar por sourceName (solo Apple Watch, excluir iPhone/apps)",
            "Convertir timestamps a zona horaria local (UTC-6 Chihuahua)",
            "Agregar métricas a nivel diario",
            "Exportar a CSV individual por tipo de métrica"
        ]
    }
    
    // ────────────────────────────────────────────────────────────────────
    // ARCHIVOS CSV GENERADOS POR EL SCRIPT (LISTA COMPLETA)
    // ────────────────────────────────────────────────────────────────────
    ARCHIVOS_CSV_GENERADOS ← [
        // ═══ MÉTRICAS DE ACTIVIDAD FÍSICA (USADAS) ═══
        "ActiveEnergyBurned.csv",           // ✅ USADA → Gasto calórico activo
        "AppleExerciseTime.csv",            // ⚠️ REVISADA (no usada final)
        "AppleStandHour.csv",               // ⚠️ REVISADA (no usada final)
        "AppleStandTime.csv",               // ⚠️ REVISADA (no usada final)
        "DistanceWalkingRunning.csv",       // ⚠️ REVISADA (no usada final)
        "FlightsClimbed.csv",               // ⚠️ REVISADA (no usada final)
        "StepCount.csv",                    // ✅ USADA → Pasos diarios
        
        // ═══ MÉTRICAS CARDIOVASCULARES (USADAS) ═══
        "HeartRate.csv",                    // ✅ USADA → Frecuencia cardíaca general
        "RestingHeartRate.csv",             // ✅ USADA → FC en reposo
        "WalkingHeartRateAverage.csv",      // ✅ USADA → FC al caminar
        "HeartRateVariabilitySDNN.csv",     // ✅ USADA → HRV_SDNN (variabilidad cardíaca)
        
        // ═══ OTRAS MÉTRICAS DISPONIBLES (NO USADAS) ═══
        "AppleWalkingSteadiness.csv",
        "AudioExposureEvent.csv",
        "BasalEnergyBurned.csv",            // ⚠️ Calculada manualmente con Harris-Benedict
        "BloodPressureDiastolic.csv",
        "BloodPressureSystolic.csv",
        "BodyMass.csv",
        "DistanceSwimming.csv",
        "HeadphoneAudioExposure.csv",
        "HeartRateRecoveryOneMinute.csv",
        "Height.csv",
        "HighHeartRateEvent.csv",
        "LowHeartRateEvent.csv",
        "MindfulSession.csv",
        "NikeFuel.csv",
        "PhysicalEffort.csv",               // Solo watchOS 9+ (Series 4+)
        "RespiratoryRate.csv",
        "RunningSpeed.csv",
        "SixMinuteWalkTestDistance.csv",
        "SleepAnalysis.csv",
        "SwimmingStrokeCount.csv",
        "VO2Max.csv",                        // Algoritmos diferentes entre Series 3-6+
        "WalkingAsymmetryPercentage.csv",
        "WalkingDoubleSupportPercentage.csv",
        "WalkingSpeed.csv",
        "WalkingStepLength.csv",
        "Workout.csv"
    ]
    
    // ────────────────────────────────────────────────────────────────────
    // VARIABLES ORIGINALES SELECCIONADAS PARA EL ESTUDIO
    // ────────────────────────────────────────────────────────────────────
    VARIABLES_ORIGINALES_SELECCIONADAS ← {
        // De archivos CSV directos
        pasos_diarios: "StepCount.csv → Suma diaria",
        gasto_calórico_activo: "ActiveEnergyBurned.csv → Suma diaria (kcal)",
        FC_reposo: "RestingHeartRate.csv → Mínimo diario en ventana 02:00-05:00 (lpm)",
        FC_caminar: "WalkingHeartRateAverage.csv → Media diaria (lpm)",
        HRV_SDNN: "HeartRateVariabilitySDNN.csv → Media diaria (ms)",
        
        // Variables derivadas/calculadas
        horas_monitoreadas: "Calculada → Rango temporal con registros activos por día",
        TMB: "Calculada → Harris-Benedict (sexo, edad, peso, estatura)",
        
        // Nota: AppleStandHour/AppleStandTime NO usadas finalmente
        // (alta variabilidad, baja completitud, reemplazadas por Actividad_relativa)
    }
    
    // ────────────────────────────────────────────────────────────────────
    // PROCESO DE PARSING Y CONVERSIÓN
    // ────────────────────────────────────────────────────────────────────
    PARA cada usuario EN [u1, u2, u3, ..., u10]:
        IMPRIMIR f"Procesando usuario {usuario}..."
        
        // ═══ PASO 1: DESCOMPRESIÓN Y VALIDACIÓN ═══
        ARCHIVO_ZIP ← Cargar_Export_Zip_Seguro(usuario)
        
        INTENTAR:
            XML_FILE ← Descomprimir_Y_Extraer(ARCHIVO_ZIP, "export.xml")
        CAPTURAR Error_Descompresión:
            REGISTRAR_ERROR(usuario, "Archivo ZIP corrupto - Datos incompletos")
            SOLICITAR_Reenvío(usuario)
            CONTINUAR
        FIN_INTENTAR
        
        // ═══ PASO 2: PARSING XML CON VALIDACIÓN DE INTEGRIDAD ═══
        INTENTAR:
            ARBOL ← Parse_XML_Con_Validación(XML_FILE)
            REGISTROS ← ARBOL.findall("Record")
            TOTAL_REGISTROS ← COUNT(REGISTROS)
            
            IMPRIMIR f"  Total registros XML: {TOTAL_REGISTROS:,}"
            
        CAPTURAR Error_XML_Malformado:
            // Problema común: XML roto por volumen excesivo
            REGISTRAR_ERROR(usuario, tipo="XML_INCOMPLETO", detalle={
                problema: "Falta delimitador de cierre (</HealthData> o </Record>)",
                causa: "Corrupción por gran volumen de datos (>2 GB XML)",
                solución_aplicada: "Reparación manual o solicitar re-exportación"
            })
            
            APLICAR_Reparación_XML_Si_Posible(XML_FILE)
            O_BIEN
            SOLICITAR_Reenvío(usuario)
            CONTINUAR
        FIN_CAPTURAR
        
        // ═══ PASO 3: FILTRADO POR FUENTE (SOLO APPLE WATCH) ═══
        DF_DIARIO ← DataFrame_Vacio()
        registros_apple_watch ← 0
        registros_descartados ← 0
        
        PARA cada REGISTRO EN REGISTROS:
            source_name ← REGISTRO.get("sourceName", "")
            
            // Filtro crítico: Solo datos del Apple Watch del participante
            SI source_name CONTIENE "Apple Watch" ENTONCES
                TIPO ← REGISTRO.type  // ej: HKQuantityTypeIdentifierStepCount
                VALOR ← REGISTRO.value
                FECHA_UTC ← REGISTRO.startDate
                HORA_UTC ← EXTRAER_HORA(FECHA_UTC)
                UNIDAD ← REGISTRO.unit
                
                // Ajustar zona horaria a local (Chihuahua, México)
                FECHA_LOCAL ← Convertir_UTC_to_Local(
                    FECHA_UTC,
                    HORA_UTC,
                    zona_horaria="America/Chihuahua"  // UTC-6
                )
                
                DF_DIARIO.append([FECHA_LOCAL, TIPO, VALOR, UNIDAD])
                registros_apple_watch ← registros_apple_watch + 1
            SINO
                // Descartar datos de iPhone, apps terceras, etc.
                registros_descartados ← registros_descartados + 1
            FIN_SI
        FIN_PARA
        
        IMPRIMIR f"  Registros Apple Watch: {registros_apple_watch:,}"
        IMPRIMIR f"  Registros descartados: {registros_descartados:,}"
        IMPRIMIR f"  Porcentaje Apple Watch: {(registros_apple_watch/TOTAL_REGISTROS)*100:.1f}%"
        
        // ═══ PASO 4: LIMPIEZA DE DATOS ERRÓNEOS ═══
        // Problema común: Registros con errores temporales o valores imposibles
        ERRORES_DETECTADOS ← {
            fechas_futuras: 0,
            fc_imposibles: 0,
            valores_negativos: 0
        }
        
        PARA cada fila EN DF_DIARIO:
            // Error 1: Fechas futuras (ej: registros en 2028 cuando estamos en 2025)
            SI fila.fecha > FECHA_ACTUAL ENTONCES
                MARCAR_PARA_ELIMINAR(fila)
                ERRORES_DETECTADOS.fechas_futuras += 1
            FIN_SI
            
            // Error 2: Frecuencias cardíacas imposibles
            SI fila.tipo == "HeartRate" Y (fila.valor < 30 O fila.valor > 220) ENTONCES
                MARCAR_PARA_ELIMINAR(fila)
                ERRORES_DETECTADOS.fc_imposibles += 1
            FIN_SI
            
            // Error 3: Valores negativos
            SI fila.valor < 0 ENTONCES
                MARCAR_PARA_ELIMINAR(fila)
                ERRORES_DETECTADOS.valores_negativos += 1
            FIN_SI
        FIN_PARA
        
        DF_DIARIO ← ELIMINAR_Filas_Marcadas(DF_DIARIO)
        
        SI SUM(ERRORES_DETECTADOS.values()) > 0 ENTONCES
            REGISTRAR_LOG_LIMPIEZA(usuario, ERRORES_DETECTADOS)
            IMPRIMIR f"  ⚠️ Errores corregidos: {SUM(ERRORES_DETECTADOS.values())}"
        FIN_SI
        
        // ═══ PASO 5: AGREGACIÓN DIARIA POR TIPO DE MÉTRICA ═══
        // Diferentes métricas requieren diferentes funciones de agregación
        FUNCIONES_AGREGACIÓN ← {
            StepCount: SUMA,
            ActiveEnergyBurned: SUMA,
            HeartRate: MEDIA,
            RestingHeartRate: MÍNIMO,  // FC reposo = mínima del día
            HRV_SDNN: MEDIA,
            WalkingHeartRateAverage: MEDIA,
            DistanceWalkingRunning: SUMA
        }
        
        DF_PIVOTE ← DF_DIARIO.pivot_table(
            index = "fecha",
            columns = "tipo",
            values = "valor",
            aggfunc = FUNCIONES_AGREGACIÓN
        )
        
        // Renombrar columnas a nombres legibles
        DF_PIVOTE.rename(columns={
            "HKQuantityTypeIdentifierStepCount": "Pasos_diarios",
            "HKQuantityTypeIdentifierActiveEnergyBurned": "Calorías_activas",
            "HKQuantityTypeIdentifierHeartRate": "FC_promedio",
            "HKQuantityTypeIdentifierRestingHeartRate": "FCr_promedio_diario",
            "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "HRV_SDNN_promedio_diario",
            "HKQuantityTypeIdentifierWalkingHeartRateAverage": "FC_caminar_promedio_diario"
        })
        
        // ═══ PASO 6: CALCULAR VARIABLE "HORAS MONITOREADAS" ═══
        // Variable crítica para normalización posterior
        PARA cada fecha EN DF_PIVOTE.index:
            registros_fecha ← FILTRAR DF_DIARIO DONDE fecha == fecha
            hora_primer_registro ← MIN(registros_fecha.hora)
            hora_último_registro ← MAX(registros_fecha.hora)
            
            horas_monitoreadas ← (hora_último_registro - hora_primer_registro).hours
            
            DF_PIVOTE.loc[fecha, "Hrs_monitoreadas"] ← horas_monitoreadas
        FIN_PARA
        
        // ═══ PASO 7: EXPORTAR CSV INDIVIDUAL ═══
        GUARDAR_CSV(DF_PIVOTE, ruta=f"DB_u{usuario}.csv")
        
        IMPRIMIR f"  ✅ Archivo generado: DB_u{usuario}.csv"
        IMPRIMIR f"  Días con datos: {LEN(DF_PIVOTE)}"
        IMPRIMIR ""
    FIN_PARA
    
    // ────────────────────────────────────────────────────────────────────
    // MÉTRICAS DE COMPLETITUD POST-PROCESAMIENTO
    // ────────────────────────────────────────────────────────────────────
    MÉTRICAS_COMPLETITUD ← []
    
    PARA cada archivo_csv EN Listar_Archivos("DB_u*.csv"):
        usuario ← EXTRAER_ID_Usuario(archivo_csv)
        DF ← CARGAR_CSV(archivo_csv)
        
        días_totales ← LEN(DF)
        días_válidos ← COUNT(DF DONDE Todas_Variables_Clave_Presentes)
        completitud_porcentaje ← (días_válidos / días_totales) * 100
        
        missingness_por_variable ← {}
        PARA cada variable EN [Pasos, Calorías, FCr, FC_caminar, HRV]:
            missing ← COUNT(DF DONDE variable ES NULO)
            missingness_porcentaje ← (missing / días_totales) * 100
            missingness_por_variable[variable] ← missingness_porcentaje
        FIN_PARA
        
        MÉTRICAS_COMPLETITUD.append({
            usuario: usuario,
            días_totales: días_totales,
            días_válidos: días_válidos,
            completitud: completitud_porcentaje,
            missingness: missingness_por_variable
        })
    FIN_PARA
    
    // Calcular promedios globales
    RESULTADO_FINAL ← {
        archivos_generados: 10,
        días_totales_todos_usuarios: 9185,
        completitud_promedio: MEDIA([m.completitud PARA m EN MÉTRICAS_COMPLETITUD]) = 94.7%,
        
        missingness_promedio_por_variable: {
            Pasos: 2.3%,
            Calorías: 2.8%,
            FCr: 4.2%,
            FC_caminar: 7.6%,  // Mayor missingness (sensor óptico)
            HRV_SDNN: 14.8%    // Mayor missingness (quitarse reloj en sueño)
        },
        
        observaciones: [
            "Completitud >90% cumple criterio de calidad",
            "Variables cardiovasculares tienen mayor missingness esperado",
            "Mecanismo: Reloj quitado durante sueño/carga",
            "Requiere estrategia de imputación robusta (Fase 5)"
        ]
    }
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR f"  ✅ PREPROCESAMIENTO COMPLETADO"
    IMPRIMIR f"  Archivos CSV: {RESULTADO_FINAL.archivos_generados}"
    IMPRIMIR f"  Días totales: {RESULTADO_FINAL.días_totales:,}"
    IMPRIMIR f"  Completitud: {RESULTADO_FINAL.completitud_promedio:.1f}%"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR RESULTADO_FINAL, MÉTRICAS_COMPLETITUD
FIN_PROCEDIMIENTO


================================================================================
FASE 4: ANÁLISIS EXPLORATORIO INICIAL (EDA) Y VALIDACIÓN SF-36
================================================================================

PROCEDIMIENTO EDA_Inicial_y_Validación_SF36()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 4 (Informe Técnico) / Sección 5.4 (Tesis)
    // Análisis Exploratorio de Datos Pre-Pivote
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  FASE 4: ANÁLISIS EXPLORATORIO INICIAL"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    DB_CONSOLIDADA ← Consolidar_Todos_Usuarios()  // 9,185 días × 10 usuarios
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 1: ESTADÍSTICOS DESCRIPTIVOS ROBUSTOS
    // ────────────────────────────────────────────────────────────────────
    VARIABLES_CLAVE ← [
        "Pasos_diarios",
        "Calorías_activas",
        "FCr_promedio_diario",
        "FC_caminar_promedio_diario",
        "HRV_SDNN_promedio_diario",
        "Hrs_monitoreadas"
    ]
    
    ESTADÍSTICOS_DESCRIPTIVOS ← {}
    
    PARA cada variable EN VARIABLES_CLAVE:
        // Estadísticos de tendencia central
        media ← MEDIA(DB_CONSOLIDADA[variable])
        mediana ← PERCENTIL(DB_CONSOLIDADA[variable], 50)
        
        // Estadísticos de dispersión
        desv_est ← DESV_EST(DB_CONSOLIDADA[variable])
        CV ← (desv_est / media) * 100  // Coeficiente de Variación
        
        Q1 ← PERCENTIL(DB_CONSOLIDADA[variable], 25)
        Q3 ← PERCENTIL(DB_CONSOLIDADA[variable], 75)
        IQR ← Q3 - Q1
        
        // Rango
        mínimo ← MIN(DB_CONSOLIDADA[variable])
        máximo ← MAX(DB_CONSOLIDADA[variable])
        
        // Almacenar
        ESTADÍSTICOS_DESCRIPTIVOS[variable] ← {
            n: COUNT(DB_CONSOLIDADA[variable].no_nulos),
            media: media,
            desv_est: desv_est,
            CV_porcentaje: CV,
            mediana: mediana,
            Q1: Q1,
            Q3: Q3,
            IQR: IQR,
            mínimo: mínimo,
            máximo: máximo
        }
    FIN_PARA
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 2: PRUEBAS DE NORMALIDAD
    // ────────────────────────────────────────────────────────────────────
    RESULTADOS_NORMALIDAD ← {}
    
    PARA cada variable EN VARIABLES_CLAVE:
        n ← COUNT(DB_CONSOLIDADA[variable].no_nulos)
        
        // Seleccionar test apropiado según tamaño muestral
        SI n < 5000 ENTONCES
            test_nombre ← "Shapiro-Wilk"
            W_statistic, p_valor ← Test_Shapiro_Wilk(DB_CONSOLIDADA[variable])
        SINO
            test_nombre ← "Kolmogorov-Smirnov"
            KS_statistic, p_valor ← Test_Kolmogorov_Smirnov(DB_CONSOLIDADA[variable])
        FIN_SI
        
        // Decisión estadística
        SI p_valor < 0.05 ENTONCES
            decisión ← "RECHAZAR normalidad"
            implicación ← "Usar métodos no paramétricos"
        SINO
            decisión ← "NO RECHAZAR normalidad"
            implicación ← "Métodos paramétricos válidos"
        FIN_SI
        
        RESULTADOS_NORMALIDAD[variable] ← {
            test: test_nombre,
            p_valor: p_valor,
            decisión: decisión,
            implicación: implicación
        }
    FIN_PARA
    
    // Resultado esperado: TODAS las variables rechazan normalidad (p<0.001)
    CONCLUSIÓN_NORMALIDAD ← "Distribuciones NO normales → Métodos no paramétricos obligatorios"
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 3: VISUALIZACIONES EXPLORATORIAS
    // ────────────────────────────────────────────────────────────────────
    GENERAR_VISUALIZACIONES({
        histogramas_con_KDE: {
            variables: VARIABLES_CLAVE,
            bins: 50,
            kernel: "gaussian",
            archivo: "histogramas_con_kde.png",
            observación: "Alta variabilidad (CV >50%) y asimetría positiva"
        },
        
        boxplots_comparativos: {
            por_usuario: TRUE,
            detectar_outliers: TRUE,
            método_outliers: "IQR × 1.5",
            archivo: "boxplots_comparativos.png",
            observación: "Heterogeneidad inter-sujeto marcada"
        },
        
        violin_plots: {
            mostrar_densidad: TRUE,
            mostrar_cuartiles: TRUE,
            archivo: "violin_plots_por_usuario.png"
        },
        
        heatmap_patrón_semanal: {
            variable: "Pasos_diarios",
            agregación: "mediana por día de semana",
            archivo: "heatmap_patron_semanal.png",
            observación: "Reducción actividad en fines de semana"
        }
    })
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 4: VALIDACIÓN PSICOMÉTRICA DEL SF-36
    // ────────────────────────────────────────────────────────────────────
    SF36_DIMENSIONES ← [
        "Función_Física_FF",
        "Rol_Físico_RF",
        "Dolor_Corporal_DC",
        "Salud_General_SG",
        "Vitalidad_VT",
        "Función_Social_FS",
        "Rol_Emocional_RE",
        "Salud_Mental_SM"
    ]
    
    VALIDACIÓN_SF36 ← {}
    
    PARA cada dimensión EN SF36_DIMENSIONES:
        ítems ← EXTRAER_Ítems_Dimensión(dimensión)
        
        // Calcular Alfa de Cronbach
        FUNCIÓN Calcular_Alpha_Cronbach(ítems)
            K ← LEN(ítems)  // Número de ítems
            varianza_ítems ← SUM([VAR(ítem) PARA ítem EN ítems])
            varianza_total ← VAR(SUM(ítems))
            
            alpha ← (K / (K - 1)) * (1 - (varianza_ítems / varianza_total))
            RETORNAR alpha
        FIN_FUNCIÓN
        
        alpha ← Calcular_Alpha_Cronbach(ítems)
        varianza ← VAR(SUM(ítems))
        
        // Criterio de aceptación
        SI alpha >= 0.70 Y varianza > 0 ENTONCES
            decisión ← "Aceptable"
        SINO SI varianza == 0 ENTONCES
            decisión ← "Rechazada (efecto techo/suelo)"
        SINO
            decisión ← "Marginal/Rechazada"
        FIN_SI
        
        VALIDACIÓN_SF36[dimensión] ← {
            alpha_cronbach: alpha,
            varianza: varianza,
            decisión: decisión
        }
    FIN_PARA
    
    // Resultado real del estudio
    RESULTADOS_SF36_REALES ← {
        dimensiones_aceptables: 7,
        dimensiones_rechazadas: 1,  // Rol_Físico (varianza=0)
        
        problemas_detectados: {
            Rol_Físico: "Varianza nula - Efecto techo (todos reportaron mismo valor)",
            Vitalidad: "Alpha=0.64 < 0.70 - Consistencia interna insuficiente"
        },
        
        implicación_metodológica: "SF-36 presenta limitaciones psicométricas en esta 
                                   cohorte específica (N=10, adultos jóvenes sanos). 
                                   No sensible a variaciones diarias/semanales capturadas 
                                   por wearable."
    }
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  ✅ EDA COMPLETADO"
    IMPRIMIR "  Variables NO normales: 6/6"
    IMPRIMIR "  SF-36 dimensiones válidas: 7/8"
    IMPRIMIR "  Conclusión: Alta variabilidad diaria (CV>50%)"
    IMPRIMIR "              → Justifica agregación semanal"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        ESTADÍSTICOS_DESCRIPTIVOS,
        RESULTADOS_NORMALIDAD,
        VALIDACIÓN_SF36,
        RESULTADOS_SF36_REALES
    }
FIN_PROCEDIMIENTO

================================================================================
FASE 5: PIVOTE METODOLÓGICO (H0 → H2) - CRÍTICO
================================================================================

PROCEDIMIENTO Pivote_Metodológico_Crítico()
    // ═══════════════════════════════════════════════════════════════════════
    // Capítulo 5 (Informe Técnico) / Sección 5.5 (Tesis)
    // Decisión de rechazar hipótesis inicial y reformular enfoque
    // ═══════════════════════════════════════════════════════════════════════
    
    IMPRIMIR "═══════════════════════════════════════════════════════"
    IMPRIMIR "  🔄 FASE 5: PIVOTE METODOLÓGICO (CRÍTICO)"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 1: ANÁLISIS DE CORRELACIÓN SF-36 vs BIOMÉTRICOS
    // ────────────────────────────────────────────────────────────────────
    BIOMÉTRICOS_AGREGADOS ← {
        // Promedio de 4 semanas por usuario
        Pasos_prom: MEDIA_4_SEMANAS(Pasos_diarios),
        Calorías_prom: MEDIA_4_SEMANAS(Calorías_activas),
        FCr_prom: MEDIA_4_SEMANAS(FCr_promedio_diario),
        FC_caminar_prom: MEDIA_4_SEMANAS(FC_caminar_promedio_diario),
        HRV_prom: MEDIA_4_SEMANAS(HRV_SDNN_promedio_diario)
    }
    
    SF36_DIMS_VÁLIDAS ← [FF, DC, SG, VT, FS, RE, SM]  // Excluir RF
    
    MATRIZ_CORRELACIONES ← DataFrame_Vacio(
        filas=LEN(BIOMÉTRICOS_AGREGADOS),
        columnas=LEN(SF36_DIMS_VÁLIDAS)
    )
    
    PARA cada bio_var EN BIOMÉTRICOS_AGREGADOS:
        PARA cada sf36_dim EN SF36_DIMS_VÁLIDAS:
            // Correlación de Spearman (datos no normales)
            rho, p_valor ← Correlación_Spearman(bio_var, sf36_dim)
            
            // Corrección Bonferroni para comparaciones múltiples
            n_comparaciones ← LEN(BIOMÉTRICOS_AGREGADOS) × LEN(SF36_DIMS_VÁLIDAS)
            alpha_ajustado ← 0.05 / n_comparaciones = 0.0016
            
            p_valor_ajustado ← MIN(p_valor × n_comparaciones, 1.0)
            
            MATRIZ_CORRELACIONES[bio_var, sf36_dim] ← {
                rho: rho,
                p_valor: p_valor,
                p_ajustado: p_valor_ajustado
            }
        FIN_PARA
    FIN_PARA
    
    // Resultado real del estudio
    RESULTADO_CORRELACIONES ← {
        correlación_máxima: 0.45,  // Calorías_prom vs Salud_General
        correlación_mínima: -0.21,  // FCr_prom vs Función_Física
        
        ninguna_significativa_bonferroni: TRUE,  // Todas p_ajustado > 0.0016
        
        conclusión: "Correlaciones débiles a moderadas (0.09 ≤ |r| ≤ 0.45), 
                     ninguna sobrevive corrección Bonferroni. Insuficiente 
                     para modelo predictivo supervisado."
    }
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 2: MODELADO CON RED NEURONAL ARTIFICIAL (ANN) - PRUEBA DEFINITIVA
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  Probando ANN como prueba definitiva..."
    
    // Preparar datos
    X ← MATRIZ(N=10, features=16)  // 16 features biométricos agregados
    y ← MATRIZ(N=10, dimensiones=7)  // 7 dimensiones SF-36 válidas
    
    // Arquitectura ANN explorada
    ARQUITECTURA_ANN ← {
        capas: [
            Dense(32, activation="relu", input_dim=16),
            Dense(16, activation="relu"),
            Dense(7, activation="linear")  // Salida: 7 dimensiones SF-36
        ],
        
        optimizador: Adam(learning_rate=0.001),
        loss: "mean_squared_error",
        métricas: ["mae", "mse"],
        
        validación: "5-fold Cross-Validation",
        epochs: 500,
        early_stopping: {patience: 50, monitor: "val_loss"}
    }
    
    // Entrenamiento (20 configuraciones probadas)
    RESULTADO_ANN ← {
        R2_train: 0.92,   // Sobreajuste evidente
        R2_val: -0.18,    // NEGATIVO → Peor que predecir la media
        R2_test: -0.34,   // NEGATIVO
        
        MAE_test: 21.3,   // Error inaceptable (>20 puntos SF-36)
        RMSE_test: 27.9,
        
        diagnóstico: "Sobreajuste severo. R² negativo indica que el modelo 
                      es PEOR que simplemente predecir la media. Evidencia de:
                      1) N=10 insuficiente para ANN (regla: N ≥ 10 × params)
                      2) Relación CS-CVRS multifactorial confundida
                      3) SF-36 no sensible a variaciones wearable"
    }
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 3: DECISIÓN METODOLÓGICA - RECHAZAR H0
    // ────────────────────────────────────────────────────────────────────
    EVIDENCIA_RECHAZO_H0 ← {
        correlaciones_débiles: TRUE,  // |r| < 0.60
        p_valores_no_significativos: TRUE,  // p > 0.0016 (Bonferroni)
        ANN_R2_negativo: TRUE,  // Modelo inútil
        
        causas_identificadas: [
            "N=10 insuficiente para modelado supervisado ANN",
            "Relación CS-CVRS multifactorial, confundida por variables psicosociales",
            "SF-36 carece de sensibilidad a variaciones diarias/semanales en población joven-adulta sana",
            "Datos biométricos de vida libre muy ruidosos (CV>50%)"
        ]
    }
    
    DECISIÓN_ESTADÍSTICA ← "RECHAZAR HIPÓTESIS H0"
    
    IMPRIMIR "  ❌ HIPÓTESIS H0 RECHAZADA"
    IMPRIMIR "     Correlaciones débiles: r<0.60"
    IMPRIMIR "     ANN R²: -0.34 (negativo)"
    IMPRIMIR "     Conclusión: Enfoque supervisado NO viable"
    IMPRIMIR ""
    
    // ────────────────────────────────────────────────────────────────────
    // PASO 4: REFORMULACIÓN - NUEVA HIPÓTESIS H2 (DATA-DRIVEN)
    // ────────────────────────────────────────────────────────────────────
    IMPRIMIR "  🔄 REFORMULANDO ENFOQUE..."
    
    HIPÓTESIS_H2 ← "Los datos biométricos contienen patrones latentes que permiten 
                    clasificar objetivamente semanas como 'ACTIVO' vs 'SEDENTARIO', 
                    independientemente de la percepción subjetiva de CVRS (SF-36)"
    
    NUEVO_ENFOQUE_DUAL ← {
        método_1: {
            nombre: "Clustering No Supervisado (K-Means)",
            propósito: "Descubrimiento empírico de patrones → Ground Truth Operativa",
            ventaja: "Data-driven, sin etiquetas externas",
            salida: "Etiquetas binarias: ACTIVO / SEDENTARIO"
        },
        
        método_2: {
            nombre: "Sistema de Inferencia Difusa (Mamdani)",
            propósito: "Modelo experto interpretable basado en conocimiento fisiológico",
            ventaja: "Reglas clínicas transparentes, lógica proposicional",
            salida: "Score continuo [0,1] + clasificación binaria"
        },
        
        validación: {
            tipo: "Concordancia entre métodos independientes",
            métrica_principal: "F1-Score ≥ 0.80",
            umbral_aceptación: "Alta concordancia Fuzzy ↔ Clustering valida ambos"
        }
    }
    
    MÉTRICAS_ÉXITO_REFORMULADAS ← {
        F1_Score: "≥ 0.80 (balance precisión-recall)",
        Recall: "≥ 0.90 (sensibilidad para screening sedentarismo)",
        MCC: "≥ 0.30 (correlación ajustada por desbalanceo)",
        interpretabilidad: "Reglas difusas clínicamente comprensibles"
    }
    
    JUSTIFICACIÓN_PIVOTE ← {
        evidencia_empírica: "Correlaciones débiles + ANN fallida",
        teórica: "Enfoque data-driven apropiado para descubrimiento en vida libre",
        respaldo_comité: "Validación interna (concordancia) aceptable para estudio piloto"
    }
    
    IMPRIMIR "  ✅ NUEVO ENFOQUE DATA-DRIVEN ADOPTADO"
    IMPRIMIR "     H2: Clasificación objetiva ACTIVO/SEDENTARIO"
    IMPRIMIR "     Método 1: Clustering K-Means → Ground Truth"
    IMPRIMIR "     Método 2: Sistema Difuso → Modelo Interpretable"
    IMPRIMIR "     Validación: Concordancia F1≥0.80"
    IMPRIMIR "═══════════════════════════════════════════════════════"
    
    RETORNAR {
        HIPÓTESIS_H0_RECHAZADA: TRUE,
        EVIDENCIA_RECHAZO: EVIDENCIA_RECHAZO_H0,
        HIPÓTESIS_H2: HIPÓTESIS_H2,
        NUEVO_ENFOQUE: NUEVO_ENFOQUE_DUAL,
        MÉTRICAS_ÉXITO: MÉTRICAS_ÉXITO_REFORMULADAS
    }
FIN_PROCEDIMIENTO


// ═══════════════════════════════════════════════════════════════════════════
// CONTINUACIÓN EN SIGUIENTE MENSAJE (FASES 6-12)
// Debido a límite de longitud, las fases restantes se incluyen a continuación
// ═══════════════════════════════════════════════════════════════════════════

```

---

## RESUMEN DE CAMBIOS APLICADOS (V2)

### ✅ 1. **Tipo de Investigación Actualizado**
- Cuantitativo, exploratorio-correlacional
- Longitudinal retrospectivo multianual
- Observacional de un solo corte, sin grupo control
- Paradigma BYOD

### ✅ 2. **Fechas y Aprobaciones Agregadas**
- Primer dictamen: 17 febrero 2025 (SIP/116/25)
- Registro: CI-088-24
- Aprobación ética: 21 agosto 2025
- Convocatoria: 21 agosto 2025

### ✅ 3. **Justificación Tamaño Muestral con Fórmula**
```
Poder ∝ N × n̄_obs/sujeto
N=10 × 133.7 semanas = 1,337 observaciones
Cumple criterio: ntotal > 1,000 ✅
Referencia: Bolger & Laurenceau (2013)
```

### ✅ 4. **Archivos CSV Específicos Detallados**
**USADOS:**
- `ActiveEnergyBurned.csv` → Gasto calórico activo
- `StepCount.csv` → Pasos diarios
- `HeartRate.csv` → FC general
- `RestingHeartRate.csv` → FC reposo
- `WalkingHeartRateAverage.csv` → FC caminar
- `HeartRateVariabilitySDNN.csv` → HRV_SDNN

**NO USADOS (pero generados):**
- AppleStandHour/AppleStandTime (baja completitud)
- VO2Max, PhysicalEffort (heterogeneidad entre versiones)
- 20+ archivos adicionales disponibles pero no relevantes

### ✅ 5. **Cambio de Nomenclatura**
```
ANTES:
- Cluster 0: Bajo Sedentarismo
- Cluster 1: Alto Sedentarismo

DESPUÉS:
- Cluster 0: ACTIVO
- Cluster 1: SEDENTARIO

Justificación: Mejor storytelling clínico,
usuarios no patológicos
```

### ✅ 6. **Consideraciones y Limitaciones Reconocidas**
- Sesgo: Solo usuarios Apple Watch
- Método manual de extracción (no Swift nativo)
- Heterogeneidad entre Series 3-9 en métricas avanzadas
- Errores comunes en XML (fechas futuras, FC imposibles)
- Problemas de corrupción en archivos >2GB

---

**Fecha de Generación:** Diciembre 3, 2024  
**Versión:** 2.0 - Pipeline Actualizado con Correcciones  
**Estado:** REVISADO - Listo para Restructuración Capítulos 5-6

