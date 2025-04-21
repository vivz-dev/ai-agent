from openai import OpenAI
import json
from agent_api.utils.config import OPENAI_MODEL
from agent_api.data.session_store import get_responses
from agent_api.agent.prompts import prompt_system
from agent_api.agent.tools.export import tools
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key= api_key)

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
    historial = get_responses()
    response = client.responses.create(
            instructions=prompt_system,
            model=OPENAI_MODEL,
            input=historial,
            tool_choice="auto",
            tools=tools,
            parallel_tool_calls=False
    )
    return response

def get_tool_response():
    historial = get_responses()
    response = client.responses.create(
            model=OPENAI_MODEL,
            input=historial,
            tools=tools,
    )
    return response