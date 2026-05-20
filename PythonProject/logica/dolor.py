def evaluar_dolor(intensidad):
    """
    Clasifica el dolor y sugiere el escalón terapéutico.
    intensidad: int del 0 al 10
    """
    if intensidad == 0:
        nivel = "Sin dolor"
        sugerencia = "No requiere tratamiento analgésico."
        color = "verde"
    elif intensidad <= 3:
        nivel = "Dolor leve"
        sugerencia = "Escalón 1: Analgésicos no opioides (Paracetamol, AINEs)."
        color = "verde_claro"
    elif intensidad <= 6:
        nivel = "Dolor moderado"
        sugerencia = "Escalón 2: Opioides débiles (Tramadol, Codeína) + No opioides."
        color = "naranja"
    elif intensidad <= 9:
        nivel = "Dolor severo"
        sugerencia = "Escalón 3: Opioides potentes (Morfina, Fentanilo) + No opioides."
        color = "rojo"
    else:
        nivel = "Dolor insoportable"
        sugerencia = "Escalón 4: Métodos invasivos, bloqueo nervioso o cuidados paliativos."
        color = "rojo_oscuro"

    return intensidad, nivel.upper(), sugerencia