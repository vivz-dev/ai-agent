from openai import OpenAI
import agent_api.data.session_store as session_store
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from agent_api.providers.openai_provider import get_response, get_tool_response
from agent_api.agent.tools.definitions import buscar_documentos, generar_dashboard, olvidar_historial
from agent_api.data.session_store import historial_responses
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def crear_response(input_usuario: str, id: str):
    response = get_response()
    if isinstance(response.output[0], ResponseFunctionToolCall):
        texto_response = ejecutar_tools(response.output, input_usuario)
    else:
        texto_response = response.output[0].content[0].text
        session_store.add_response({"role": "assistant", "content": texto_response})
    return texto_response

def chatear(input_usuario: str) -> str:
    session_store.add_response({"role": "user", "content": input_usuario})
    texto_response = crear_response(input_usuario, id="")
    return texto_response

def ejecutar_tools(output, input_usuario: str):
    respuesta = ""
    tool = output[0]
    function_name = tool.name
    function_args = json.loads(tool.arguments)
    if function_name == "buscar_documentos":
        result = json.dumps(buscar_documentos(function_args['consulta']))
        respuesta = add_tool(tool, result)
    elif function_name == "generar_dashboard":
        respuesta = generar_dashboard()
    elif function_name == "olvidar_historial":
        result = olvidar_historial()
        respuesta = add_tool(tool, result)
    return respuesta

def add_tool(tool, respuesta):
    session_store.add_response(tool)
    session_store.add_response({
            "type": "function_call_output",
            "call_id": tool.call_id,
            "output": respuesta,
    })
    response_2 = get_tool_response()
    respuesta = response_2.output_text
    session_store.add_response({"role": "assistant", "content": respuesta})
    return respuesta
        
    # for tool in output:
    #     function_name = tool.name
    #     # function_args = json.loads(["arguments"])
    #     if function_name == "buscar_documentos":
    #         result = buscar_documentos(input_usuario)
    #         session_store.add_response(tool)
    #         session_store.add_response({
    #             "type": "function_call_output",
    #             "call_id": tool.call_id,
    #             "output": result,
    #         })
    #         historial = session_store.get_responses()
    #         response_2 = client.responses.create(
    #             model="gpt-4o-mini-2024-07-18",
    #             input=historial,
    #             tools=tools2,
    #         )
    #         respuesta += response_2.output_text
    #         if respuesta == "":
    #             respuesta += result
    #         session_store.add_response({"role": "assistant", "content": respuesta})
    #     elif function_name == "generar_dashboard":
    #         # resultado = generar_dashboard(function_args["consulta"], function_args["periodo"])
    #         # print(f"Resultado de generar_dashboard: {resultado}")
    #         respuesta = "Generando dashboard..."
    #     else:
    #         print(f"Función desconocida: {function_name}")
    # return respuesta


query1 = "cual fue el porcentaje de variación de cartera de credito de banco guayaquil en el Q1 y Q2 de hace 5 años atrás?"
query2 = "dame un resumen de lo que pasó en los balances del Q1 y Q2 de hace 5 años atrás?"
query3 = "compara el año pasado con este"
query4 = "hola"
query5 = "ahora, dame un resumen de lo que te pregunté al inicio, pero solo de activos"
query6 = "ok, ahora dame el reporte de marzo del año pasado pero solo de patrimonios"

# respuesta = chatear(query6)
# print(respuesta)
# respuesta = chatear(query4)
# print(respuesta)
# respuesta = chatear(query5)
# print(respuesta)