from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from agent_api.utils.config import EMBEDDING_MODEL, VECTORIAL_DATABASE_NAME, VECTORIAL_DB_PATH
import os
import agent_api.agent.tools.buscar_documentos.prompts as prompts
from agent_api.providers.openai_provider import get_JSON_openAI, get_text_openAI
from itertools import product

def leer_database():
    """
    Carga la base de datos vectorial desde el disco.
    """
    embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"{VECTORIAL_DATABASE_NAME}"))
    db = FAISS.load_local(VECTORIAL_DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def extraer_parametros(query: str):
    """
    Extrae los parámetros de la consulta del usuario utilizando un LLM.
    """
    prompt_usuario = prompts.get_prompt_parametros(query)
    respuesta_json = get_JSON_openAI(prompt_usuario)
    return respuesta_json

def obtener_combinaciones(filter_dict):
    """
    Genera todas las combinaciones posibles de filtros a partir de un diccionario de filtros.
    """
    valid_filters = {k: v if isinstance(v, list) else [v]
                     for k, v in filter_dict.items() if k != 'reason'}
    keys = list(valid_filters.keys())
    values = list(valid_filters.values())
    combinations = product(*values)
    return [dict(zip(keys, combo)) for combo in combinations]

# json_respuesta = {'query': 'Cuál fue el porcentaje de variación de cartera de crédito de Banco Guayaquil en marzo y junio de 2020',
# json_respuesta = {'query': 'Resumen de los ACTIVO, PASIVO, PATRIMONIO, TOTAL PASIVO + PATRIMONIO, TOTAL ACTIVOS + CONTINGEN. NETOS del año 2020 para marzo y junio',
#                   'filters': {'concepto': ['ACTIVO', 'PASIVO', 'PATRIMONIO', 'TOTAL PASIVO + PATRIMONIO', 'TOTAL ACTIVOS + CONTINGEN. NETOS'], 'año': ['2020'], 'mes': ['marzo', 'junio']},
#                   'reason': 'La pregunta original se refiere a los balances de los dos primeros trimestres del año 2020, por lo que se han incluido los meses marzo y junio. Además, se han extraído todos los conceptos relevantes para el resumen.'}

def realizar_informe(documentos_relevantes: list) -> str:
    """
    Genera un informe a partir de los documentos relevantes encontrados.
    """
    if len(documentos_relevantes) == 0: return "Actualmente no tengo acceso a los documentos que mencionas, ya que los datos aún no han sido cargados. Tan pronto como estén disponibles, podré analizarlos y entregarte un informe detallado."
    prompt_informe = prompts.get_prompt_informe(documentos_relevantes)
    respuesta_informe = get_text_openAI(prompt_informe)
    return respuesta_informe