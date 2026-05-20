def evaluar_glasgow(ocular, verbal, motor):
    """
    Calcula el nivel de conciencia según la escala de Glasgow.
    Parámetros (int):
    - ocular: 1 a 4
    - verbal: 1 a 5
    - motor: 1 a 6
    """
    total = ocular + verbal + motor

    # Clasificación clínica del Trauma Craneoencefálico (TCE)
    if total >= 13:
        estado = "Leve"
        gravedad = "Bajo riesgo"
    elif total >= 9:
        estado = "Moderado"
        gravedad = "Riesgo intermedio - Requiere observación"
    else:
        estado = "Grave"
        gravedad = "Riesgo alto - Posible necesidad de intubación"

    return total, estado.upper(), gravedad


def obtener_descripcion_puntajes(tipo, puntos):
    """
    Devuelve la descripción médica de cada puntaje para el reporte.
    """
    descripciones = {
        "ocular": {
            4: "Espontánea", 3: "A la orden verbal",
            2: "Al dolor", 1: "Ninguna"
        },
        "verbal": {
            5: "Orientado", 4: "Desorientado/Confuso",
            3: "Palabras inapropiadas", 2: "Sonidos incomprensibles", 1: "Ninguna"
        },
        "motor": {
            6: "Obedece órdenes", 5: "Localiza el dolor",
            4: "Retirada al dolor", 3: "Flexión anormal (decorticación)",
            2: "Extensión anormal (descerebración)", 1: "Ninguna"
        }
    }
    return descripciones.get(tipo, {}).get(puntos, "Desconocido")