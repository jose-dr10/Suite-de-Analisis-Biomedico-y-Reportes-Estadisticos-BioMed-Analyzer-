def evaluar_ica(cintura_cm, altura_cm):
    ica = round(cintura_cm / altura_cm, 2)
    if ica <= 0.50:
        res, nivel = "Saludable", "Bajo"
    elif ica <= 0.57:
        res, nivel = "Sobrepeso", "Moderado"
    else:
        res, nivel = "Obesidad Abdominal", "Alto"
    return ica, res.upper(), nivel.upper()