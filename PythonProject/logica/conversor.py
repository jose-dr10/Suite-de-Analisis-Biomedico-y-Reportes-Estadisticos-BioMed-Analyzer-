def convertir_glucosa(valor, direccion):
    """
    Direccion: 'mg_a_mmol' o 'mmol_a_mg'
    Factor: 18.0182
    """
    if direccion == "mg_a_mmol":
        res = valor / 18.0182
        unidad = "mmol/L"
    else:
        res = valor * 18.0182
        unidad = "mg/dL"
    return round(res, 2), unidad

def convertir_lipidos(valor, direccion):
    """
    Direccion: 'mg_a_mmol' o 'mmol_a_mg'
    Factor para Colesterol: 38.67
    """
    if direccion == "mg_a_mmol":
        res = valor / 38.67
        unidad = "mmol/L"
    else:
        res = valor * 38.67
        unidad = "mg/dL"
    return round(res, 2), unidad

def convertir_trigliceridos(valor, direccion):
    """
    Factor para Triglicéridos: 88.57
    """
    if direccion == "mg_a_mmol":
        res = valor / 88.57
        unidad = "mmol/L"
    else:
        res = valor * 88.57
        unidad = "mg/dL"
    return round(res, 2), unidad