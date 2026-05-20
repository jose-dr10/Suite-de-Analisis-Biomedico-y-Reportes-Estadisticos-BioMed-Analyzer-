def evaluar_glucemia(valor, estado_toma):
    # estado_toma: "ayunas" o "postprandial" (2h después de comer)
    if estado_toma == "ayunas":
        if valor < 70:
            res = "Hipoglucemia"
        elif valor < 100:
            res = "Normal"
        elif valor < 126:
            res = "Prediabetes"
        else:
            res = "Diabetes (Sugerido)"
    else:  # Postprandial
        if valor < 140:
            res = "Normal"
        elif valor < 200:
            res = "Tolerancia disminuida"
        else:
            res = "Diabetes (Sugerido)"

    return res.upper()