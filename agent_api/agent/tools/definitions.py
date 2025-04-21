import agent_api.agent.tools.buscar_documentos.logic as tool_docs
import agent_api.agent.tools.olvidar_historial.logic as tool_olvidar_historial
import agent_api.agent.tools.consultar_divisas.logic as tool_consulta_divisas
import agent_api.agent.tools.grafico_lineas.logic as tool_grafico
import agent_api.agent.tools.enviar_correo.logic as tool_correo
import json
import agent_api.providers.openai_provider as openAIP

def buscar_documentos(query: str):
    db = tool_docs.leer_database()
    json_respuesta = tool_docs.extraer_parametros(query)
    combinaciones_posibles = tool_docs.obtener_combinaciones(json_respuesta["filters"])
    resultados_finales = []
    for filtro in combinaciones_posibles:
        results = db.similarity_search(
            query=f"{filtro['concepto']} {filtro['mes']} {filtro['año']}",
            filter={
                "concepto": filtro["concepto"],
                "año": filtro["año"],
                "mes": filtro["mes"],
            },
            k=3)
        for doc in results:
            resultados_finales.append({
                "contenido": doc.page_content,
                "metadata": doc.metadata
            })

    # informe = tool_docs.realizar_informe(resultados_finales)
    return resultados_finales

def generar_grafico_lineas(query: str) -> str:
    params = tool_grafico.extraer_params(query)
    # print(params)
    #{ "entidad": "Guayaquil", "meses": ["junio", "septiembre", "diciembre", "marzo"], "años": ["2022", "2023"], "concepto": ""}
    df_filtrado = tool_grafico.consultarCSV(params) # dataframe con 2 columnas
    data_df = df_filtrado.to_json(orient='records')
    json_ejes = tool_grafico.organizar_params(data_df)
    graficoURL = tool_grafico.get_URL(json_ejes, params)
    return graficoURL

def generar_imagen(query: str) -> str:
    imgURL = openAIP.get_image_url(query)
    return imgURL

def consultar_divisas(function_args):
    divisas_actuales = tool_consulta_divisas.consultar(function_args)
    return divisas_actuales

def olvidar_historial() -> str:
    tool_olvidar_historial.olvidar_historial()
    return "Olvidando historial"

def enviar_correo(function_args):
    correo = tool_correo.enviar_correo_to(function_args)
    return correo