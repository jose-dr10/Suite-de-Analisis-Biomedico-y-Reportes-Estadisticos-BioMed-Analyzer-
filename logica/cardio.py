def evaluar_perfil_lipidico(col_total, hdl, ldl, trig):
    # Índice aterogénico (Col Total / HDL)
    indice = round(col_total / hdl, 2)

    # Evaluación básica
    if col_total < 200 and ldl < 130 and trig < 150:
        estado = "Perfil Óptimo"
        riesgo = "Bajo"
    elif col_total >= 240 or ldl >= 160 or trig >= 200:
        estado = "Dislipidemia Detectada"
        riesgo = "Alto"
    else:
        estado = "Límites Moderados"
        riesgo = "Moderado"

    return estado, riesgo, indice