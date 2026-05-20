def calcular_dosis_pediatrica(peso, dosis_mg_kg, concentracion_mg, volumen_ml):
    """
    Fórmula: (Peso * Dosis requerida * Volumen presentación) / Concentración presentación
    Ej: Un niño de 10kg, dosis 15mg/kg, presentación de 120mg en 5ml.
    """
    if concentracion_mg <= 0:
        return 0

    mg_totales = peso * dosis_mg_kg
    ml_a_dar = round((mg_totales * volumen_ml) / concentracion_mg, 2)

    return ml_a_dar, mg_totales