import pandas as pd

columnas = []
df_balance_general = pd.DataFrame()

def leer_txt(nombre_archivo: str, primera_fila: bool):
    n_linea = 1
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()
        for linea in lineas:
            lista = linea.split("|")
            if n_linea == 4:
                ultimos = lista[-8:]
                # periodo_inicial = convertir_fecha(c[0])
                periodo_final = convertir_fecha(ultimos[1])
                columnas = [
                    f"Total Sistema hasta {periodo_final}",
                    f"Guayaquil hasta {periodo_final}",
                    f"Variación Banco Guayaquil {ultimos[4]} hasta {periodo_final}",
                    f"Variación Banco Guayaquil {ultimos[5]} hasta {periodo_final}",
                    f"Variación Total Sistema {ultimos[6]} hasta {periodo_final}",
                    f"Variación Total Sistema {ultimos[7]} hasta {periodo_final}"
                    ]
                if primera_fila == True: 
                    titulo = "(En millones de dólares)"
                    columnas.insert(0, titulo)
                df_balance_general = pd.DataFrame(columns=columnas)
            if n_linea > 4:
                ultimos = lista[-8:]
                primeros = lista[:-8]
                lista_float = [float(x.replace(",", "").replace("%", "")) for x in ultimos]
                del lista_float[0]
                del lista_float[1]
                if primera_fila == True: 
                    titulo = (" ").join(primeros)
                    lista_float.insert(0, titulo)
                nueva_fila = pd.DataFrame([lista_float], columns=columnas)
                df_balance_general = pd.concat([df_balance_general, nueva_fila], ignore_index=True)
            n_linea += 1
    return [df_balance_general, columnas]


meses = {
    "ene.": "enero", "feb.": "febrero", "mar.": "marzo",
    "abr.": "abril", "may.": "mayo", "jun.": "junio",
    "jul.": "julio", "ago.": "agosto", "sep.": "septiembre",
    "oct.": "octubre", "nov.": "noviembre", "dic.": "diciembre"
}

def convertir_fecha(fecha_abreviada):
    partes = fecha_abreviada.split("-")
    mes_abrev = partes[0]
    anio = partes[1]
    mes_completo = meses.get(mes_abrev, mes_abrev)
    return f"{mes_completo} 20{anio}"