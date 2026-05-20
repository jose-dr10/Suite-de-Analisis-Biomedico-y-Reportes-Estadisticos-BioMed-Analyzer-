def calcular_metabolismo_y_agua(peso, altura, edad, sexo, actividad):
    # TMB - Ecuación de Mifflin-St Jeor
    if sexo == "hombre":
        tmb = (10 * peso) + (6.25 * (altura * 100)) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * (altura * 100)) - (5 * edad) - 161

    # Factor de actividad
    factores = {"sedentario": 1.2, "moderado": 1.55, "atleta": 1.9}
    calorias_mantener = round(tmb * factores.get(actividad, 1.2))

    # Hidratación (35ml por kg)
    litros_agua = round((peso * 0.035), 2)

    return calorias_mantener, litros_agua