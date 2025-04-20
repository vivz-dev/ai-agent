from openai import OpenAI
import data.session_store as session_store
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from agent_api.providers.openai_provider import get_response, get_tool_response
from agent_api.agent.tools.definitions import buscar_documentos, generar_dashboard
from agent_api.data.session_store import historial_responses

client = OpenAI()

def crear_response(input_usuario: str, id: str):
    response = get_response()
    if isinstance(response.output[0], ResponseFunctionToolCall):
        texto_response = ejecutar_tools(response.output, input_usuario)
    else:
        texto_response = response.output[0].content[0].text
    return texto_response

def chatear(input_usuario: str) -> str:
    session_store.add_response({"role": "user", "content": input_usuario})
    texto_response, = crear_response(input_usuario, id="")
    return texto_response

def ejecutar_tools(output, input_usuario: str):
    respuesta = ""
    tool = output[0]
    function_name = tool.name
    function_args = tool.arguments
    if function_name == "buscar_documentos":
        result = buscar_documentos(f"{function_args["consulta"]} {function_args["periodo"]}")
        session_store.add_response(tool)
        session_store.add_response({
            "type": "function_call_output",
            "call_id": tool.call_id,
            "output": result,
        })
        response_2 = get_tool_response()
        respuesta = response_2.output_text
        session_store.add_response({"role": "assistant", "content": respuesta})
    elif function_name == "generar_dashboard":
        respuesta = generar_dashboard()
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