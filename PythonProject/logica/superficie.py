import math


def calcular_superficie_corporal(peso, altura_cm):
    """
    Fórmula de Mosteller para Superficie Corporal (m²).
    """
    if peso <= 0 or altura_cm <= 0:
        return 0

    # math.sqrt es la raíz cuadrada
    bsa = math.sqrt((altura_cm * peso) / 3600)

    return round(bsa, 2)