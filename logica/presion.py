def evaluar_presion_arterial(sistolica, diastolica):
    """
    Evalúa los niveles de presión arterial según los estándares de salud comunes.
    Sistólica (máxima) y Diastólica (mínima).
    """
    try:
        # Clasificación lógica
        if sistolica < 120 and diastolica < 80:
            resultado = "Normal"
            estado = "Óptimo"
        elif 120 <= sistolica <= 129 and diastolica < 80:
            resultado = "Elevada"
            estado = "Precaución"
        elif 130 <= sistolica <= 139 or 80 <= diastolica <= 89:
            resultado = "Hipertensión Nivel 1"
            estado = "Riesgo Moderado"
        elif sistolica >= 140 or diastolica >= 90:
            resultado = "Hipertensión Nivel 2"
            estado = "Riesgo Alto"
        else:
            # En caso de crisis hipertensiva (S > 180 o D > 120)
            if sistolica > 180 or diastolica > 120:
                resultado = "CRISIS HIPERTENSIVA"
                estado = "URGENCIA MÉDICA"
            else:
                resultado = "Valores inconsistentes"
                estado = "Revisar medición"

        return resultado, estado

    except Exception as e:
        return "Error", f"Detalle: {str(e)}"