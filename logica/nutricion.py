def calcular_imc(peso, altura):
    """
    Calcula el Índice de Masa Corporal y determina la categoría nutricional.
    Recibe peso en kg y altura en metros.
    """
    try:
        # Validación de seguridad para evitar división por cero
        if altura <= 0:
            return None, "La altura debe ser mayor a 0 metros.", ""

        imc = peso / (altura ** 2)

        if imc < 18.5:
            categoria = "Bajo peso"
            recomendacion = "Se recomienda consultar con un nutricionista para aumentar la ingesta calórica."
        elif 18.5 <= imc < 24.9:
            categoria = "Peso normal"
            recomendacion = "Estado nutricional óptimo. Mantenga sus hábitos actuales."
        elif 25 <= imc < 29.9:
            categoria = "Sobrepeso"
            recomendacion = "Se recomienda incrementar la actividad física y cuidar la ingesta de grasas."
        else:
            categoria = "Obesidad"
            recomendacion = "Alerta: Riesgo para la salud. Se sugiere seguimiento médico especializado."

        return round(imc, 2), categoria, recomendacion

    except Exception as e:
        return None, f"Error en el cálculo: {str(e)}", ""