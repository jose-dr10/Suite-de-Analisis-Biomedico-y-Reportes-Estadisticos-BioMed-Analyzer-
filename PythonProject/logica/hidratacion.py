def calcular_deficit_agua(peso, sodio_actual, sexo):
    """
    Fórmula: Agua Corporal Total * ((Sodio actual / 140) - 1)
    ACT: 0.6 en hombres, 0.5 en mujeres.
    """
    factor_act = 0.6 if sexo == "hombre" else 0.5
    agua_corporal = peso * factor_act

    deficit = round(agua_corporal * ((sodio_actual / 140) - 1), 2)

    return max(0, deficit)  # No devuelve valores negativos