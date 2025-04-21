import json
import os

historial_responses = []

def get_response_id():
    if len(historial_responses) == 0:
        return ""
    else:
        last_response = historial_responses[-1]
        return last_response.id

def get_responses():
    return historial_responses.copy()

def add_response(response):
    historial_responses.append(response)
    
def clear_responses():
    historial_responses.clear()