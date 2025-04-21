import pandas as pd
import agent_api.agent.tools.grafico_lineas.prompts as p
from agent_api.providers.openai_provider import get_JSON_openAI, get_text_openAI

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

def extraer_params(query: str):
    prompt_p = p.get_prompt_params(query)
    json_params = get_JSON_openAI(prompt_p)
    return json_params

def organizar_params(data):
    prompt_p = p.get_prompt_org(data)
    json_data = get_JSON_openAI(prompt_p)
    return json_data