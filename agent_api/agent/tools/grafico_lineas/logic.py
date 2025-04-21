import pandas as pd
import agent_api.agent.tools.grafico_lineas.prompts as p
from agent_api.providers.openai_provider import get_JSON_openAI, get_text_openAI
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from imgurpython import ImgurClient
from datetime import datetime

client_id = '5432f96e9520d83'
client_secret = 'fe81f6a821c79e0d07c2db12d815050d6cc22bbc'

client = ImgurClient(client_id, client_secret)

def consultarCSV(params):
    filtros = params["filters"]
    entidad = "Guayaquil"
    meses="|".join(filtros["meses"])
    years="|".join(filtros["años"])
    concepto = "".join(filtros["concepto"])
    #{ "meses": ["junio", "septiembre", "diciembre", "marzo"], "años": ["2022", "2023"]}
    df = pd.read_csv("./agent_api/data/database/mi_archivo2.csv")
    primera_columna = df.columns[0]
    df_filtrado_columnas = df[[primera_columna, concepto]]
    filtro = (
        df['(En millones de dólares)'].str.startswith(entidad) &
        df['(En millones de dólares)'].str.contains(meses, case=False) &
        df['(En millones de dólares)'].str.contains(years)
    )
    df_filtrado = df_filtrado_columnas[filtro]
    return df_filtrado

def get_URL(json_data, params):
    filtros = params["filters"]
    concepto = "".join(filtros["concepto"])

    x = json_data['X']
    y = json_data['Y']
    # "X": ["marzo 2022", "junio 2022", "marzo 2023", junio 2023"]
    # "Y": [7394.0, 31023.0, 10.0, 343.0]
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', linestyle='-', linewidth=2)
    for i, valor in enumerate(y):
        plt.text(x[i], y[i], f'{valor:,.2f}', ha='center', va='bottom', fontsize=9, color='black')
    plt.title(f'{concepto}', fontsize=14, weight='bold')
    plt.xlabel('Periodo')
    plt.ylabel('Valor')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    fecha = datetime.now()
    str_fecha = fecha.strftime("%Y-%m-%d_%H-%M-%S")
    output_path = f'/Users/vivianavera03/Desktop/Bco Guayaquil/ai-agent/agent_api/data/img/grafico_{str_fecha}.png'
    plt.savefig(output_path, dpi=300)

    response = client.upload_from_path(output_path, config=None, anon=True)
    print(response)
    id = response["id"]# https://i.imgur.com/3hjZnrz.png
    URL = f"https://i.imgur.com/{id}.png"
    return URL

def extraer_params(query: str):
    prompt_p = p.get_prompt_params(query)
    json_params = get_JSON_openAI(prompt_p)
    return json_params

def organizar_params(data):
    prompt_p = p.get_prompt_org(data)
    json_data = get_JSON_openAI(prompt_p)
    return json_data