def calcular_ovulacion(duracion_ciclo):
    # Estimación estándar: día de ovulación es duración - 14
    # La ventana fértil suele ser 3 días antes y 1 después
    dia_ovulacion = duracion_ciclo - 14
    ventana_inicio = dia_ovulacion - 3
    ventana_fin = dia_ovulacion + 1

    # Manejo de casos donde el ciclo es muy corto
    if ventana_inicio < 1:
        ventana_inicio = 1

    return dia_ovulacion, f"Días {ventana_inicio} al {ventana_fin}"