import requests
import json

URL = "https://v6.exchangerate-api.com/v6/91ca673f02fa22dd35b04a9b/latest/" # USD

def consultar(function_args):
    moneda = function_args["moneda"]
    # json.loads(tool.arguments)
    response = requests.get(f"{URL}{moneda}")
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return ""