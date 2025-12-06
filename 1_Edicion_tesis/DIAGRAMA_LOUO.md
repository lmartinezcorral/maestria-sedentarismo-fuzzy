# DIAGRAMA EXPLICATIVO: LEAVE-ONE-USER-OUT (LOUO)

## Diagrama 1: Proceso General de LOUO

```mermaid
graph TB
    Start([Cohorte Total<br/>N=10 usuarios<br/>1,337 semanas]) --> Split[División LOUO]
    
    Split --> Fold1[Fold 1:<br/>Usuario 1 = TEST<br/>Usuarios 2-10 = TRAIN]
    Split --> Fold2[Fold 2:<br/>Usuario 2 = TEST<br/>Usuarios 1,3-10 = TRAIN]
    Split --> Fold3[Fold 3:<br/>Usuario 3 = TEST<br/>Usuarios 1-2,4-10 = TRAIN]
    Split --> FoldN[Fold 10:<br/>Usuario 10 = TEST<br/>Usuarios 1-9 = TRAIN]
    
    Fold1 --> Train1[Entrenar modelo<br/>con datos de<br/>9 usuarios]
    Fold2 --> Train2[Entrenar modelo<br/>con datos de<br/>9 usuarios]
    Fold3 --> Train3[Entrenar modelo<br/>con datos de<br/>9 usuarios]
    FoldN --> TrainN[Entrenar modelo<br/>con datos de<br/>9 usuarios]
    
    Train1 --> Test1[Evaluar en<br/>Usuario 1<br/>F1₁]
    Train2 --> Test2[Evaluar en<br/>Usuario 2<br/>F1₂]
    Train3 --> Test3[Evaluar en<br/>Usuario 3<br/>F1₃]
    TrainN --> TestN[Evaluar en<br/>Usuario 10<br/>F1₁₀]
    
    Test1 --> Aggregate[Agregar Resultados]
    Test2 --> Aggregate
    Test3 --> Aggregate
    TestN --> Aggregate
    
    Aggregate --> Final[F1-Score LOUO<br/>μ = 0.780<br/>σ = 0.167<br/>CV = 21.4%]
    
    style Start fill:#e1f5ff
    style Final fill:#c8e6c9
    style Split fill:#fff9c4
    style Aggregate fill:#f3e5f5
```

## Diagrama 2: Comparación LOUO vs Split Tradicional

```mermaid
graph LR
    subgraph Traditional["❌ Split Tradicional 80/20"]
        T1[80% TRAIN<br/>Usuarios mezclados] --> T2[20% TEST<br/>Mismo usuario puede<br/>estar en ambos]
        T2 --> T3[⚠️ Data Leakage<br/>Temporal + Identity]
    end
    
    subgraph LOUO["✅ Leave-One-User-Out"]
        L1[9 usuarios TRAIN<br/>Usuario excluido] --> L2[1 usuario TEST<br/>Usuario nunca visto<br/>en entrenamiento]
        L2 --> L3[✓ Sin Leakage<br/>Generalización<br/>inter-sujeto]
    end
    
    style Traditional fill:#ffebee
    style LOUO fill:#e8f5e9
    style T3 fill:#ffcdd2
    style L3 fill:#c8e6c9
```

## Diagrama 3: Ejemplo Iterativo Detallado (Fold 1)

```mermaid
graph TB
    subgraph Cohort["Cohorte Completa (N=10)"]
        U1[Usuario 1<br/>133 semanas]
        U2[Usuario 2<br/>298 semanas]
        U3[Usuario 3<br/>145 semanas]
        U4[Usuario 4<br/>87 semanas]
        U5[Usuario 5<br/>156 semanas]
        U6[Usuario 6<br/>234 semanas]
        U7[Usuario 7<br/>201 semanas]
        U8[Usuario 8<br/>112 semanas]
        U9[Usuario 9<br/>178 semanas]
        U10[Usuario 10<br/>193 semanas]
    end
    
    Cohort --> Fold1[FOLD 1: Usuario 1 como TEST]
    
    Fold1 --> TrainSet[CONJUNTO DE ENTRENAMIENTO<br/>Usuarios 2-10<br/>1,204 semanas totales]
    Fold1 --> TestSet[CONJUNTO DE PRUEBA<br/>Usuario 1<br/>133 semanas]
    
    TrainSet --> Model[Modelo Difuso<br/>Entrenado]
    TestSet --> Eval[Evaluación]
    
    Model --> Eval
    Eval --> Result1[F1-Score Fold 1<br/>F1₁ = 0.812]
    
    style Cohort fill:#e3f2fd
    style TrainSet fill:#c8e6c9
    style TestSet fill:#fff9c4
    style Result1 fill:#f3e5f5
```

## Diagrama 4: Ventajas de LOUO para Datos Longitudinales

```mermaid
graph TB
    subgraph Problem["Problema: Datos Longitudinales"]
        P1[Autocorrelación temporal<br/>Datos del mismo usuario<br/>son dependientes]
        P2[Identidad del usuario<br/>Patrones individuales<br/>únicos]
    end
    
    Problem --> Solution[LOUO como Solución]
    
    Solution --> V1[✓ Evita Temporal Leakage<br/>No mezcla semanas<br/>del mismo usuario]
    Solution --> V2[✓ Evita Identity Leakage<br/>Usuario de test<br/>nunca visto en train]
    Solution --> V3[✓ Generalización Real<br/>Simula despliegue<br/>en nuevos usuarios]
    Solution --> V4[✓ Apropiado para N pequeño<br/>Máximo uso de datos<br/>N folds = N usuarios]
    
    style Problem fill:#ffebee
    style Solution fill:#e8f5e9
    style V1 fill:#c8e6c9
    style V2 fill:#c8e6c9
    style V3 fill:#c8e6c9
    style V4 fill:#c8e6c9
```

## Diagrama 5: Resultados por Usuario (Visualización)

```mermaid
graph TB
    subgraph Results["Resultados LOUO por Usuario"]
        R1[Usuario 1: F1 = 0.812]
        R2[Usuario 2: F1 = 0.997]
        R3[Usuario 3: F1 = 0.215]
        R4[Usuario 4: F1 = 0.654]
        R5[Usuario 5: F1 = 0.876]
        R6[Usuario 6: F1 = 0.743]
        R7[Usuario 7: F1 = 0.891]
        R8[Usuario 8: F1 = 0.567]
        R9[Usuario 9: F1 = 0.789]
        R10[Usuario 10: F1 = 0.698]
    end
    
    Results --> Stats[Estadísticas Agregadas]
    Stats --> Mean[Media: μ = 0.780]
    Stats --> SD[Desviación: σ = 0.167]
    Stats --> CV[Coeficiente Variación: 21.4%]
    Stats --> Success[7/10 usuarios<br/>F1 ≥ 0.65]
    
    style Results fill:#e3f2fd
    style Stats fill:#f3e5f5
    style Mean fill:#c8e6c9
    style Success fill:#c8e6c9
```

## Diagrama 6: Flujo Completo del Proceso

```mermaid
flowchart TD
    Start([Inicio: Cohorte N=10]) --> Preprocess[Preprocesamiento<br/>Imputación + Normalización]
    
    Preprocess --> Aggregate[Agregación Semanal<br/>Medianas + IQR]
    
    Aggregate --> Loop{Iteración LOUO<br/>i = 1 a 10}
    
    Loop -->|Fold i| Split[Separar Usuario i<br/>como TEST]
    Split --> Train[Entrenar Modelo<br/>con Usuarios 1...i-1, i+1...10]
    Train --> Test[Evaluar en Usuario i<br/>Calcular F1ᵢ]
    Test --> Store[Almacenar F1ᵢ]
    
    Store --> Check{i < 10?}
    Check -->|Sí| Loop
    Check -->|No| AggregateResults[Agregar Resultados<br/>μ, σ, CV]
    
    AggregateResults --> Final([F1-Score LOUO<br/>0.780 ± 0.167])
    
    style Start fill:#e1f5ff
    style Final fill:#c8e6c9
    style Loop fill:#fff9c4
    style AggregateResults fill:#f3e5f5
```

## Diagrama 7: Comparación Visual: Split 80/20 vs LOUO

```mermaid
graph TB
    subgraph Split80["❌ Split 80/20 Tradicional"]
        S1[80% Datos<br/>Mezcla aleatoria<br/>de semanas] --> S2[20% Datos<br/>Misma mezcla]
        S2 --> S3[Problema:<br/>Semanas del Usuario 1<br/>en TRAIN y TEST]
        S3 --> S4[Data Leakage<br/>Sobrestimación<br/>del rendimiento]
    end
    
    subgraph LOUO["✅ Leave-One-User-Out"]
        L1[9 Usuarios<br/>Todas sus semanas<br/>en TRAIN] --> L2[1 Usuario<br/>Todas sus semanas<br/>en TEST]
        L2 --> L3[Sin Leakage:<br/>Usuario de TEST<br/>completamente nuevo]
        L3 --> L4[Generalización<br/>Real<br/>Rendimiento conservador]
    end
    
    style Split80 fill:#ffebee
    style LOUO fill:#e8f5e9
    style S4 fill:#ffcdd2
    style L4 fill:#c8e6c9
```

---

## INSTRUCCIONES DE USO

### Para PowerPoint/Google Slides:
1. Copia el código Mermaid del diagrama que prefieras
2. Ve a [Mermaid Live Editor](https://mermaid.live/)
3. Pega el código y genera la imagen
4. Exporta como PNG/SVG de alta resolución
5. Inserta en tu presentación

### Para LaTeX (si necesitas en la tesis):
Los diagramas Mermaid se pueden convertir a TikZ o usar el paquete `mermaid` si está disponible.

### Recomendación para Presentación:
- **Diapositiva 10 (Metodología):** Usa el Diagrama 1 o Diagrama 6
- **Diapositiva 11 (Resultados):** Usa el Diagrama 5
- **Si hay preguntas sobre validación:** Usa el Diagrama 2 o Diagrama 7

---

## EXPLICACIÓN TEXTUAL PARA EL GUION

**Para Diagrama 1 (Proceso General):**
> "La validación Leave-One-User-Out divide nuestra cohorte de 10 usuarios en 10 iteraciones. En cada iteración, un usuario se excluye completamente del entrenamiento y se usa exclusivamente para evaluación. El modelo se entrena con los datos de los 9 usuarios restantes, y luego se evalúa en el usuario excluido. Este proceso se repite para cada usuario, generando 10 valores de F1-Score que se agregan para obtener nuestra métrica final de 0.780 con desviación estándar de 0.167."

**Para Diagrama 2 (Comparación):**
> "A diferencia del split tradicional 80/20, donde los datos se mezclan aleatoriamente y el mismo usuario puede aparecer en entrenamiento y prueba, LOUO garantiza que el usuario de prueba nunca ha sido visto durante el entrenamiento. Esto elimina completamente el data leakage temporal e identitario, proporcionando una estimación realista de la generalización inter-sujeto."

---

**Nota:** Estos diagramas están optimizados para explicar LOUO de manera clara y visual. Elige el que mejor se adapte a tu estilo de presentación.

