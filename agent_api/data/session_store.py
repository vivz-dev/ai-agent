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
    historial_responses.append(response)
    
def clear_responses():
    historial_responses.clear()