
def get_prompt_divisas(query: str, divisas):
    return f"""
    Lee la siguiente consulta realizada por el usuario: {query}
    Si el usuario especifica que quiere transformar o convertir una divisa sigue estos pasos:
    1. Extrae la información relevante de la pregunta en un diccionario JSON. Incluye los campos si están presentes:
    - moneda_actual (la moneda en la que está la consulta)
    - moneda_destino (la moneda o divisa a transformar)
    - cantidad

    2. Analiza la lista de divisas y extrae la cantidad de la 

    2. Realiza el cálculo matemático:
    cambio_destino = moneda_actual * usd_to_eur

    Si el usuario solo quiere consultar el estado de una divisa, entonces solamente realiza un informe de las divisas actuales.
    Divisas Actuales:
    {divisas}
    """