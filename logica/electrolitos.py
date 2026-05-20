# Contenido de logica/electrolitos.py

def calcular_anion_gap(sodio, cloro, bicarbonato):
    """
    Fórmula: Na - (Cl + HCO3)
    """
    gap = round(sodio - (cloro + bicarbonato), 1)

    if gap > 12:
        interpretacion = "Anión Gap Elevado (Acidosis normoclorémica)"
    elif gap < 8:
        interpretacion = "Anión Gap Bajo (Posible hipoalbuminemia)"
    else:
        interpretacion = "Anión Gap Normal"

    return gap, interpretacion


def calcular_deficit_agua(peso, sodio_actual, sexo):
    """
    Fórmula: Agua Corporal Total * ((Sodio actual / 140) - 1)
    """
    factor_act = 0.6 if sexo == "hombre" else 0.5
    agua_corporal = peso * factor_act

    deficit = round(agua_corporal * ((sodio_actual / 140) - 1), 2)

    return max(0, deficit)  # No devuelve valores negativos