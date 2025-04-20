from openai import OpenAI
import json
from agent_api.utils.config import OPENAI_MODEL
from agent_api.data.session_store import historial_responses
from agent_api.agent.prompts import prompt_system
from agent_api.agent.tools.export import tools

client = OpenAI()

def get_JSON_openAI(prompt_usuario: str):
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt_usuario,
        text={ "format": { "type": "json_object" }}
    )
    #TODO: validar finish reason
    #TODO: validar errores 400
    #TODO: validar refusals o penalizaciones
    #TODO: lista de filtros
    return json.loads(response.output[0].content[0].text)

def get_text_openAI(prompt_usuario: str):
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt_usuario
    )
    return response.output[0].content[0].text

def get_response():
    response = client.responses.create(
            instructions=prompt_system,
            model=OPENAI_MODEL,
            input=historial_responses,
            tool_choice="auto",
            tools=tools,
            parallel_tool_calls=False
    )
    return response

def get_tool_response():
    response = client.responses.create(
            model=OPENAI_MODEL,
            input=historial_responses,
            tools=tools,
    )
    return response