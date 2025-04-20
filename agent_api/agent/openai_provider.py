from openai import OpenAI
import json

def get_JSON_openAI(prompt_usuario: str):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4o-mini-2024-07-18",
        input=prompt_usuario,
        text={ "format": { "type": "json_object" }}
    )
    #TODO: validar finish reason
    #TODO: validar errores 400
    #TODO: validar refusals o penalizaciones
    #TODO: lista de filtros
    return json.loads(response.output[0].content[0].text)


def get_text_openAI(prompt_usuario: str):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4o-mini-2024-07-18",
        input=prompt_usuario
    )
    return response.output[0].content[0].text