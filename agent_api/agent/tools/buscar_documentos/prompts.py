from datetime import date

def get_prompt_parametros(query: str) -> str:
    hoy = date.today()
    return f"""
    Dado el siguiente input del usuario, realiza dos tareas:

    1. Reescribe la pregunta de forma explícita, remplazando expresiones vagas como "el año pasado", "último trimestre", "este mes", etc., por los valores concretos de año y mes. Esta versión servirá como texto optimizado para una búsqueda semántica (query).

    2. Extrae los filtros relevantes de la pregunta en un diccionario JSON. Incluye los campos si están presentes:
    - concepto
    - año
    - mes

    CONSIDERACIONES:
    - El año DEBE ser un número de 4 dígitos.
    - El mes DEBE ser el nombre completo del mes en español y OBLIGATORIAMENTE cualquiera de estas opciones: [marzo, junio, septiembre, diciembre]
    - El concepto DEBE ser OBLIGATORIAMENTE cualquiera de estas opciones : [ACTIVO, Fondos Disponibles, Fondos Interbancarios Vendidos, Inversiones, Cartera de Crédito neta, Cartera Vigente, Cartera Vencida, Provisión para Crédito Incobrables, Deudores por aceptación, Cuentas por Cobrar, Bienes Adjudicados por Pago, Activo Fijo, Otros Activos, PASIVO, Obligaciones con el Publico, Operaciones Interbancarias, Obligaciones Inmediatas, Aceptaciones en Circulacion, Cuentas por Pagar, Obligaciones Financieras, Valores en Circulacion, Obligaciones Conv. en Acciones y Aportes, Otros Pasivos, PATRIMONIO, Capital Social, Primas o Dsctos Colocacion Acciones, Reservas, Otros Aportes Patrimoniales, Superavit por Valuaciones, Resultados, Utilidad o Pérdida Acumulado, Resultados del Ejercicio, TOTAL PASIVO + PATRIMONIO, CONTINGENTES NETOS, TOTAL ACTIVOS + CONTINGEN. NETOS]
    - La fecha de HOY es {hoy}.
    - En cada campo pondrás una lista con todos los filtros encontrados.
    - Si te pide un resumen de algún año, DEBES incluir todos los conceptos: ['ACTIVO', 'PASIVO', 'PATRIMONIO', TOTAL PASIVO + PATRIMONIO', 'TOTAL ACTIVOS + CONTINGEN. NETOS'] y TODOS los meses: ['marzo', 'junio', 'septiembre', 'diciembre']
    - DEBES de incluir en el nuevo query todos los conceptos que hallaste.
    - DEBES de incluir la entidad bancaria. Si no se especifica, añade "Banco Guayaquil" como entidad por defecto.

    ==== EJEMPLO ====
    Input: 
    "cual fue el total de activos y pasivos del ultimo semestre del año pasado?"

    JSON:
    {{
    "query": "ACTIVOS y PASIVOS de Banco Guayaquil de diciembre y junio 2024",
    "filters": {{
        "concepto": ["ACTIVO", "PASIVO"],
        "año": ["2024"],
        "mes": [diciembre, junio]
    }}
    "reason": "La pregunta original se refiere a el último semestre que corresponde a junio y diciembre de 2024. Se han extraído los conceptos 'Activos' y 'Pasivos', que son lo que se solicita en la pregunta"
    }}

    ==== FIN DE EJEMPLO ====

    Input:
    {query}

    JSON:
    """

def get_prompt_informe(documentos_relevantes) -> str:
    return f"""
    Dada la información financiera de Banco Guayaquil, realiza estas 2 tareas:
    1. Resumir la información financiera de Banco Guayaquil.
    2. Generar una respuesta al usuario.

    CONSIDERACIONES:
    - Tu tuno es serio, formal y sin emojis.
    - Asegúrate de incluir todos los conceptos y datos relevantes en tu respuesta.
    - DEBES de incluir toda la información de los documentos y hacer comparaciones si es necesario.
    - DEBES de incluir todos los conceptos que estén disponibles e inferir los motivos de cada cantidad numérica.

    Datos: 
    {documentos_relevantes}
    """

# prompt_informe = f"""
    # Dada la información financiera de Banco Guayaquil, realiza estas 2 tareas:
    # 1. Resumir la información financiera de Banco Guayaquil.
    # 2. Generar un informe al usuario.

    # CONSIDERACIONES:
    # - Tu tuno es serio, formal y sin emojis.
    # - Asegúrate de incluir todos los conceptos y datos relevantes en el informe.
    # - DEBES de incluir toda la información de los documentos y hacer comparaciones.
    # - DEBES de incluir todos los conceptos que estén disponibles e inferir los motivos de cada cantidad numérica.

    # ==== EJEMPLO DE INFORME ====
    # - **Activos**:
    # Durante el año [Año], los activos totales del banco alcanzaron los [monto] millones de dólares, lo que representa un incremento/disminución del [variación]% respecto al cierre del año anterior.
    # Este crecimiento estuvo impulsado principalmente por [por ejemplo: el aumento en la cartera de crédito, la adquisición de nuevos activos fijos, o el incremento de fondos disponibles].
    # Los activos corrientes representaron el [porcentaje]% del total, destacando [comentar rubros relevantes: efectivo, inversiones, cuentas por cobrar, etc.]

    # - **Pasivos**:
    # Los pasivos totales al 31 de diciembre de [Año] fueron de [monto] millones, con una variación del [variación]% respecto a [Año anterior].
    # La mayor parte corresponde a [por ejemplo: depósitos del público, obligaciones financieras], lo que refleja [algún insight como: la confianza del mercado o la necesidad de financiamiento externo].
    # Es importante señalar que el endeudamiento de corto plazo se mantuvo/controló/redujo, representando el [porcentaje]% de los pasivos totales.

    # - **Patrimonio**:
    # El patrimonio neto cerró en [monto], con un crecimiento de [variación]% respecto al año anterior.
    # Esto se debió principalmente a [por ejemplo: utilidades retenidas, aumento de capital, etc.]
    # La relación patrimonio/activo se ubicó en [porcentaje], lo cual indica una [buena/sólida/estable] capacidad de respaldo financiero.

    # - **Conclusiones**:
    # En resumen, el Balance General del año [Año] muestra una situación financiera [estable/sólida/en mejora], con [destacar lo más relevante, por ejemplo: crecimiento en activos, control de pasivos y fortalecimiento patrimonial].
    # Se recomienda seguir monitoreando [por ejemplo: el endeudamiento de corto plazo, la calidad de los activos, la rentabilidad del patrimonio], para mantener una posición financiera saludable en el próximo año.

    # ==== FIN DE EJEMPLO DE INFORME ====

    # Datos:
    # {documentos_relevantes}
    # """