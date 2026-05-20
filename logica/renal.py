def calcular_tfg_avanzado(creatinina, edad, sexo):
    # Fórmula CKD-EPI 2021 (Sin factor de raza)
    # Constantes según sexo
    kappa = 0.7 if sexo == "mujer" else 0.9
    alfa = -0.241 if sexo == "mujer" else -0.302
    f_sexo = 1.012 if sexo == "mujer" else 1.0

    # Cálculo base
    termino_1 = min(creatinina / kappa, 1) ** alfa
    termino_2 = max(creatinina / kappa, 1) ** -1.2
    termino_3 = 0.9938 ** edad

    tfg = 142 * termino_1 * termino_2 * termino_3 * f_sexo
    tfg = round(tfg, 1)

    if tfg >= 90:
        est = "G1: Normal"
    elif tfg >= 60:
        est = "G2: Disminución Leve"
    elif tfg >= 45:
        est = "G3a: Disminución Leve-Moderada"
    elif tfg >= 30:
        est = "G3b: Disminución Moderada-Grave"
    elif tfg >= 15:
        est = "G4: Disminución Grave"
    else:
        est = "G5: Falla Renal"

    return tfg, est.upper()