import agent_api.agent.tools.buscar_documentos.logic as tool_docs

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

def generar_dashboard(query: str) -> str:
    return "Generando dashboard..."