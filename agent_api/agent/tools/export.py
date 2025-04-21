tools = [
    {
    "type": "function",
    "name": "consultar_divisas",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "query_completo": {"type": "string", "description": "La consulta completa o query completo que hace el usuario acerca de las divisas."},
            "moneda": {"type": "string", "description": "La moneda a consultar, puede ser euros, yenes, dólar canadiense, australiano, pesos. en formato ISO 4217 (por ejemplo USD, EUR, JPY, etc.)."},
            },
        "required": ["query_completo", "moneda"],
        "additionalProperties": False
        },
    "description": "Consulta el estado actual de una divisa.",
    },
    {
    "type": "function",
    "name": "buscar_documentos",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "query_completo": {"type": "string", "description": "La consulta completa o query completo que hace el usuario acerca de los estados financieros de Banco Guayaquil."},
            },
        "required": ["query_completo"],
        "additionalProperties": False
        },
    "description": "Consulta el estado financiero de Banco Guayaquil en una base de conocimiento,",
    },
    {
    "type": "function",
    "name": "olvidar_historial",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "consulta": {"type": "string", "description": "La intención de olvidar el historial de la conversación actual."},
            },
        "required": ["consulta"],
        "additionalProperties": False
        },
    "description": "Olvida o borra el historial de la conversación actual.",
    },
    {
    "type": "function",
    "name": "generar_grafico_lineas",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "query_completo": {"type": "string", "description": "La consulta completa o query completo que hace el usuario."},
            },
        "required": ["query_completo"],
        "additionalProperties": False
        },
    "description": "Genera un gráfico de lineas de un concepto a través del tiempo. El tiempo puede ser en meses o años.",
    },
    {
    "type": "function",
    "name": "enviar_correo",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "contenido": {"type": "string", "description": "El contenido del correo."},
            "subject": {"type": "string", "description": "Encabezado o Asunto del correo electrónico."},
            "text": {"type": "string", "description": "Contenido o cuerpo del correo electrónico."},
            "from": {"type": "string", "description": "Desde qué cuenta se envía el correo."},
            "to": {"type": "string", "description": "Hacia qué dirección o direcciones (puede ser una lista) de correo se envía el mensaje. Con comillas dobles"}
            },
        "required": ["contenido", "subject", "text", "from", "to"],
        "additionalProperties": False
        },
    "description": "Envía un correo a la dirección correo electrónico especificada, con el contenido que dice la respuesta del usuario o con contenido de conversaciones anteriores del historial.",
    }
]