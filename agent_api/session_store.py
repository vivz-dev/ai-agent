import json
import os

ruta_archivo = os.path.join(os.path.dirname(__file__), './historial.json')
historial_responses = []

def get_response_id():
    if len(historial_responses) == 0:
        return ""
    else:
        last_response = historial_responses[-1]
        return last_response.id

def get_responses():
    # with open(ruta_archivo, 'r', encoding='utf-8') as f:
    #     historial = json.load(f)
    return historial_responses

def add_response(response):
    if len(historial_responses) > 10:
        del historial_responses[0]
    historial_responses.append(response)
    # with open(ruta_archivo, 'w', encoding='utf-8') as f:
    #     json.dump(historial_responses, f, indent=4, ensure_ascii=False)

def clear_responses():
    historial_responses.clear()