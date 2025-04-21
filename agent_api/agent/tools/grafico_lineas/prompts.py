from datetime import date

def get_prompt_params(query: str) -> str:
    hoy = date.today()
    return f"""
    Dado el siguiente input del usuario, realiza dos tareas:

    1. Reescribe la pregunta de forma explícita, remplazando expresiones vagas como "el año pasado", "último trimestre", "este mes", etc., por los valores concretos de año y mes. Esta versión servirá como texto optimizado para una búsqueda semántica (query).

    2. Extrae los filtros relevantes de la pregunta en un diccionario JSON. Incluye los campos si están presentes:
    - concepto
    - años
    - meses

    CONSIDERACIONES:
    - El año DEBE ser un número de 4 dígitos.
    - El mes DEBE ser el nombre completo del mes en español y OBLIGATORIAMENTE cualquiera de estas opciones: [marzo, junio, septiembre, diciembre]
    - El concepto DEBE ser OBLIGATORIAMENTE cualquiera de estas opciones : [ACTIVO, Fondos Disponibles, Fondos Interbancarios Vendidos, Inversiones, Cartera de Crédito neta, Cartera Vigente, Cartera Vencida, Provisión para Crédito Incobrables, Deudores por aceptación, Cuentas por Cobrar, Bienes Adjudicados por Pago, Activo Fijo, Otros Activos, PASIVO, Obligaciones con el Publico, Operaciones Interbancarias, Obligaciones Inmediatas, Aceptaciones en Circulacion, Cuentas por Pagar, Obligaciones Financieras, Valores en Circulacion, Obligaciones Conv. en Acciones y Aportes, Otros Pasivos, PATRIMONIO, Capital Social, Primas o Dsctos Colocacion Acciones, Reservas, Otros Aportes Patrimoniales, Superavit por Valuaciones, Resultados, Utilidad o Pérdida Acumulado, Resultados del Ejercicio, TOTAL PASIVO + PATRIMONIO, CONTINGENTES NETOS, TOTAL ACTIVOS + CONTINGEN. NETOS]
    - La fecha de HOY es {hoy}.
    - En cada campo pondrás una lista con todos los filtros encontrados.
    - Si te pide un resumen de algún año, DEBES incluir todos los meses: [marzo, junio, septiembre, diciembre]
    - DEBES de incluir en el nuevo query todos los conceptos que hallaste.
    - DEBES de respetar las mayúsculas y minúsculas al extraer cada concepto, insertándolos tal cual están en las listas proporcionadas.
    ==== EJEMPLO ====
    Input: 
    "cual fue el total de activos y pasivos del ultimo semestre del año pasado?"

    JSON:
    {{
    "query": "Fondos Disponibles de Banco Guayaquil de diciembre y junio 2024",
    "filters": {{
        "concepto": "Fondos Disponibles",
        "años": ["2024"],
        "meses": [diciembre, junio]
    }}
    "reason": "La pregunta original se refiere a el último semestre que corresponde a junio y diciembre de 2024. Se ha extraído el concepto 'Fondos Disponibles' que se solicita en la pregunta"
    }}

    ==== FIN DE EJEMPLO ====

    Input:
    {query}

    JSON:
    """

def get_prompt_image(dataf_data) -> str:
    ejeX = "".join(dataf_data["X"])
    ejeY = dataf_data["Y"]
    return f"""
    Dada la siguiente información, Genera un gráfico de líneas profesional con fondo blanco en 2 ejes (Eje X, eje Y.).
    CONSIDERACIONES:
    - Dibuja 1 sola línea.
    - La línea debe de ser color rojo.
    - DEBES de colocar esto en el eje X: {ejeX}.
    - DEBES de colocar estos valores en el eje Y: {ejeY}.
    """

def get_prompt_org(data):
    return f"""
    Realiza estas 2 tareas:

    1. Analiza la información proporcionada.
    2. Identifica los tiempos y ordénalos.
    3. Organízala de manera que tenga la siguiente estructura JSON:

    {{
        "X": ["marzo 2022", "junio 2022", "marzo 2023", junio 2023"]
        "Y": [7394.0, 31023.0, 10.0, 343.0]
    }}

    DATOS:
    {data}

    JSON:
    """