def calcular_kirby(pao2, fio2_pct):
    """
    Calcula el índice PaO2/FiO2 (Kirby).
    fio2_pct: Fracción inspirada de oxígeno (ej: 21 para aire ambiente, 50 para máscara).
    """
    # Convertir porcentaje a decimal (ej: 21 -> 0.21)
    fio2_dec = fio2_pct / 100

    indice = round(pao2 / fio2_dec, 0)

    if indice > 300:
        estado = "Normal / Sin distrés"
        color = "verde"
    elif indice > 200:
        estado = "SDRA Leve"
        color = "amarillo"
    elif indice > 100:
        estado = "SDRA Moderado"
        color = "naranja"
    else:
        estado = "SDRA Severo"
        color = "rojo"

    return indice, estado.upper()