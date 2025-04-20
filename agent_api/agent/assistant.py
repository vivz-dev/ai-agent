from openai import OpenAI
import json
import agent.tools as tools_agente
import session_store as session_store
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall

client = OpenAI()

tools = [
    {
    "type": "function",
    "name": "buscar_documentos",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "consulta": {"type": "string", "description": "La consulta que hace el usuario acerca de los estados financieros de Banco Guayaquil."},
            "periodo": {"type": "string", "description": "El periodo de tiempo sobre el que desea realizar la consulta."}
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
            "periodo": {"type": "string", "description": "El periodo de tiempo sobre el que desea realizar el dashboard."}
            },
        },
    "description": "Genera un dashboard, gráfico o tabla con los datos financieros de Banco Guayaquil. Primero consultando a una base de datos sobre datos específicos.",
    }
]

prompt_system = """
Eres un asistente que proporciona información sobre datos financieros.
Tu tono es serio, formal y sin emojis.
"""

def crear_response(input_usuario: str, id: str):
    historial = session_store.get_responses()
    client = OpenAI()
    if id == "":
        session_store.add_response({"role": "user", "content": input_usuario})
        historial = session_store.get_responses()
        response = client.responses.create(
                instructions=prompt_system,
                model="gpt-4o-mini-2024-07-18",
                input=historial,
                tool_choice="auto",
                tools=tools
        )
    else:
        response = client.responses.create(
                instructions=prompt_system,
                model="gpt-4o-mini-2024-07-18",
                input=historial,
                tool_choice="auto",
                tools=tools,
                previous_response_id=id
        )
    
    if isinstance(response.output[0], ResponseFunctionToolCall):
        texto_response = ejecutar_tools(response.output, input_usuario)
    else:
        texto_response = response.output[0].content[0].text

    return [texto_response, response]

def chatear(input_usuario: str) -> str:
    texto_response = ""
    session_store.clear_responses()
    [texto_response, response] = crear_response(input_usuario, id="")
    return texto_response

def ejecutar_tools(output, input_usuario: str):
    respuesta = ""
    for tool in output:
        function_name = tool.name
        # function_args = json.loads(["arguments"])
        if function_name == "buscar_documentos":
            result = tools_agente.buscar_documentos(input_usuario)
            session_store.add_response(tool)
            session_store.add_response({
                "type": "function_call_output",
                "call_id": tool.call_id,
                "output": result,
            })
            historial = session_store.get_responses()
            response_2 = client.responses.create(
                model="gpt-4o-mini-2024-07-18",
                input=historial,
                tools=tools,
            )
            respuesta += response_2.output_text
            if respuesta == "":
                respuesta += result
            session_store.add_response({"role": "assistant", "content": respuesta})
        elif function_name == "generar_dashboard":
            # resultado = generar_dashboard(function_args["consulta"], function_args["periodo"])
            # print(f"Resultado de generar_dashboard: {resultado}")
            respuesta = "Generando dashboard..."
        else:
            print(f"Función desconocida: {function_name}")
    return respuesta