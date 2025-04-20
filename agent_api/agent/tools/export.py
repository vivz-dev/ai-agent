tools = [
    {
    "type": "function",
    "name": "buscar_documentos",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "consulta": {"type": "string", "description": "La consulta que hace el usuario acerca de los estados financieros de Banco Guayaquil."},
            },
        },
    "description": "Consulta una base de conocimiento para encontrar información relevante de los estados financieros de Banco Guayaquil.",
    },
    {
    "type": "function",
    "name": "generar_dashboard",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "consulta": {"type": "string", "description": "La consulta que hace el usuario acerca de los datos del dashboard que quiere hacer acerca de los estados financieros de Banco Guayaquil."},
            },
        },
    "description": "Genera un dashboard, gráfico o tabla con los datos financieros de Banco Guayaquil. Primero consultando a una base de datos sobre datos específicos.",
    }
]