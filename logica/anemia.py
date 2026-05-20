def diagnosticar_anemia(edad, unidad, sexo, hemoglobina):
    # Normalización de edad
    edad_final = edad / 12 if unidad.lower() == "meses" else edad

    # Rangos de referencia
    if 0 <= edad_final <= 0.083:
        minimo, maximo = 13.0, 26.0
    elif 0.083 < edad_final <= 0.5:
        minimo, maximo = 10.0, 18.0
    elif 0.5 < edad_final <= 1:
        minimo, maximo = 11.0, 15.0
    elif 1 < edad_final <= 5:
        minimo, maximo = 11.5, 15.0
    elif 5 < edad_final <= 10:
        minimo, maximo = 12.6, 15.5
    elif 10 < edad_final <= 15:
        minimo, maximo = 13.0, 15.5
    else:
        if sexo.lower() == "mujer":
            minimo, maximo = 12.0, 16.0
        else:
            minimo, maximo = 14.0, 18.0

    positivo = hemoglobina < minimo
    return positivo, minimo, maximo