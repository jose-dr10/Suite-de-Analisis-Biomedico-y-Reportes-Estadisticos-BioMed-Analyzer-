def calcular_goteo(volumen_ml, tiempo_horas):
    """
    Calcula la velocidad de infusión en diferentes unidades.
    Factores estándar:
    - 1 ml = 20 gotas (Normogoteo)
    - 1 ml = 60 microgotas (Microgoteo)
    """
    if tiempo_horas <= 0:
        return None

    # Cálculo de ml/hora
    ml_hora = round(volumen_ml / tiempo_horas, 2)

    # Cálculo de gotas por minuto (Factor 3: constante para 20 gotas/ml)
    # Fórmula: (Volumen / (Tiempo_h * 3))
    gotas_min = round(volumen_ml / (tiempo_horas * 3), 1)

    # Cálculo de microgotas por minuto (Equivale a ml/hora)
    microgotas_min = round(ml_hora, 1)

    return {
        "ml_hora": ml_hora,
        "gotas_min": gotas_min,
        "microgotas_min": microgotas_min
    }


def estimar_duracion(volumen_ml, gotas_min):
    """
    Calcula cuánto durará un suero si ya conocemos el goteo.
    """
    if gotas_min <= 0:
        return None

    tiempo_horas = volumen_ml / (gotas_min * 3)
    return round(tiempo_horas, 2)