def calcular_puntos_edad(edad, sexo):
    if sexo == "hombre":
        if edad < 35: return 0
        if edad < 40: return 3
        if edad < 45: return 6
        if edad < 50: return 9
        if edad < 55: return 12
        if edad < 60: return 15
        if edad < 65: return 18
        if edad < 70: return 21
        return 24
    else:  # mujer
        if edad < 35: return 0
        if edad < 40: return 2
        if edad < 45: return 4
        if edad < 50: return 6
        if edad < 55: return 8
        if edad < 60: return 10
        if edad < 65: return 12
        if edad < 70: return 14
        return 16


def calcular_puntos_colesterol(col_total, sexo):
    # Basado en niveles mg/dL
    if col_total < 160: return 0
    if col_total < 200: return 1
    if col_total < 240: return 2
    if col_total < 280: return 3
    return 4


def calcular_puntos_presion(sis, dia, sexo):
    # Se toma el valor más alto entre sistólica o diastólica
    if sis < 120 and dia < 80: return 0
    if sis < 130 or dia < 85: return 1
    if sis < 140 or dia < 90: return 2
    if sis < 160 or dia < 100: return 3
    return 4


def evaluar_riesgo_framingham(sexo, edad, col_total, hdl, fumador, presion_sis, presion_dia):
    """
    Calcula el riesgo coronario a 10 años.
    fumador: booleano (True/False)
    """
    puntos = 0

    # 1. Edad
    puntos += calcular_puntos_edad(edad, sexo)

    # 2. Colesterol Total
    puntos += calcular_puntos_colesterol(col_total, sexo)

    # 3. HDL (A mayor HDL, menos puntos/riesgo)
    if hdl < 35:
        puntos += 2
    elif hdl < 45:
        puntos += 1
    elif hdl < 50:
        puntos += 0
    elif hdl < 60:
        puntos -= 1
    else:
        puntos -= 2

    # 4. Presión Arterial
    puntos += calcular_puntos_presion(presion_sis, presion_dia, sexo)

    # 5. Tabaquismo
    if fumador:
        puntos += 2 if sexo == "hombre" else 2

    # Interpretación de resultados (%)
    if sexo == "hombre":
        if puntos <= 4:
            riesgo_pct = "< 5%"
        elif puntos <= 8:
            riesgo_pct = "5-10%"
        elif puntos <= 12:
            riesgo_pct = "10-20%"
        else:
            riesgo_pct = "> 20%"
    else:
        if puntos <= 8:
            riesgo_pct = "< 5%"
        elif puntos <= 12:
            riesgo_pct = "5-10%"
        elif puntos <= 16:
            riesgo_pct = "10-20%"
        else:
            riesgo_pct = "> 20%"

    nivel = "BAJO" if "< 5%" in riesgo_pct else "MODERADO" if "5-10" in riesgo_pct else "ALTO"

    return puntos, riesgo_pct, nivel