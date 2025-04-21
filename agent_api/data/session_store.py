import json
import os

ruta_archivo = "/Users/vivianavera03/Desktop/Bco Guayaquil/ai-agent/agent_api/data/database/historial.json"
historial_responses = []

def get_response_id():
    if len(historial_responses) == 0:
        return ""
    else:
        last_response = historial_responses[-1]
        return last_response.id

def get_responses2():
    # with open(ruta_archivo, 'r', encoding='utf-8') as f:
    #     historial = json.load(f)
    return historial_responses

# def get_historial_as_list():

def get_responses():
    return historial_responses.copy()
    
def guardar_historial(historial):
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def add_response(response):
    historial_responses.append(response)
    
def clear_responses():
    historial_responses.clear()