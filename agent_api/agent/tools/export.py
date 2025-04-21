tools = [
    {
    "type": "function",
    "name": "consultar_divisas",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "query_completo": {"type": "string", "description": "La consulta completa o query completo que hace el usuario acerca de las divisas."},
            "moneda": {"type": "string", "description": "La moneda a consultar, puede ser euros, yenes, dólar canadiense, australiano, pesos. en formato ISO 4217 (por ejemplo USD, EUR, JPY, etc.)."},
            }
        },
    "description": "Consulta el estado actual de una divisa.",
    },
    {
    "type": "function",
    "name": "buscar_documentos",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "query_completo": {"type": "string", "description": "La consulta completa o query completo que hace el usuario acerca de los estados financieros de Banco Guayaquil."},
            }
        },
    "description": "Consulta el estado financiero de Banco Guayaquil en una base de conocimiento,",
    },
    {
    "type": "function",
    "name": "olvidar_historial",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "consulta": {"type": "string", "description": "La intención de olvidar el historial de la conversación actual."},
            },
        },
    "description": "Olvida o borra el historial de la conversación actual.",
    }
]