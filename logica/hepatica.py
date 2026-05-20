def evaluar_bilirrubina(directa, indirecta):
    """
    Calcula la Bilirrubina Total y evalúa predominio.
    Valores normales típicos: Total < 1.2, Directa < 0.3
    """
    total = round(directa + indirecta, 2)

    if total > 1.2:
        if directa > (total * 0.5):
            estado = "Ictericia de predominio Directo (Posible obstrucción)"
        else:
            estado = "Ictericia de predominio Indirecto (Posible hemólisis)"
        color = "rojo"
    else:
        estado = "Niveles dentro del rango normal"
        color = "verde"

    return total, estado, color