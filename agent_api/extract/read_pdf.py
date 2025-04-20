import glob
import os
from extract_libraries import read_file
import pandas as pd
import re
import json

# source env/bin/activate
'/Users/vivianavera03/Desktop/Bco Guayaquil/ai-agent/agent_api/extract/../data/uploaded/BalancesBG'
pdf_dir ='/Users/vivianavera03/Desktop/Bco Guayaquil/ai-agent/agent_api/data/uploaded/BalancesBG'
# pdf_dir = os.path.join(os.path.dirname(__file__), '/data/uploaded/BalancesBG')
pdf_paths = glob.glob(os.path.join(pdf_dir, '*.pdf'))
# pdf_paths = ["/Users/vivianavera03/Desktop/Bco Guayaquil/ai-agent/extract/../docs/uploaded/BalancesBG/ESTADOS_FINANCIEROS_WEB_BG_SEPTIEMBRE2024.pdf"]

balance_general = pd.DataFrame()
columnas = []

def convertir_columnas_a_json(df: pd.DataFrame):
    df.columns = df.columns.str.replace('\n', ' ', regex=True).str.strip().str.replace('"', '')
    columnas = df.columns# Detectar los periodos disponibles desde los nombres de las columnas
    periodos = set()
    patron_periodo = r"hasta (.*?)$"
    for col in df.columns:
        match = re.search(patron_periodo, col)
        if match:
            periodos.add(match.group(1).strip())  # saltamos la primera columna que es el concepto (ej. ACTIVO)
    # Estructura de columnas por período
    agrupaciones = {}

    for periodo in sorted(periodos, key=lambda x: pd.to_datetime("01 " + x, errors='coerce')):
        agrupaciones[periodo] = {
            "sistema": next((c for c in df.columns if c.startswith("Total Sistema") and periodo in c), None),
            "banco_guayaquil": next((c for c in df.columns if c.startswith("Guayaquil") and periodo in c), None),
            "var_monto_bg": next((c for c in df.columns if "Variación Banco Guayaquil Monto" in c and periodo in c), None),
            "var_pct_bg": next((c for c in df.columns if "Variación Banco Guayaquil %" in c and periodo in c), None),
            "var_monto_sis": next((c for c in df.columns if "Variación Total Sistema Monto" in c and periodo in c), None),
            "var_pct_sis": next((c for c in df.columns if "Variación Total Sistema %" in c and periodo in c), None),
        }

    agrupaciones = {k: v for k, v in agrupaciones.items() if all(v.values())}

    # Generar textos embeddables
    resultados = []
    for _, fila in df.iterrows():
        concepto = fila[0]
        for periodo, columnas in agrupaciones.items():
            try:
                texto = f"""
                Concepto: {concepto}.
                Periodo: hasta {periodo}.
                Total del Sistema: {fila[columnas['sistema']]} millones de dólares.
                Banco Guayaquil: {fila[columnas['banco_guayaquil']]} millones de dólares.
                Variación Banco Guayaquil: {fila[columnas['var_monto_bg']]} millones ({fila[columnas['var_pct_bg']]}%).
                Variación Total Sistema: {fila[columnas['var_monto_sis']]} millones ({fila[columnas['var_pct_sis']]}%).
                Interpretación: En el período hasta {periodo}, el concepto {concepto} presentó estos cambios tanto a nivel del sistema financiero como en Banco Guayaquil.
                """
                texto.replace("\n", " ") #"septiembre 2024",
                [mes, year] = periodo.split(" ")
                resultados.append({
                    "text": texto.strip(),
                    "metadata": {
                        "concepto": concepto,
                        "periodo": periodo,
                        "año": year,
                        "mes": mes,
                    }
                })
            except Exception as e:
                print(f"⚠️ Error en {concepto} - {periodo}: {e}")

    return resultados


try:
    for path_archivo in pdf_paths:
        if (len(balance_general) == 0):
            [balance_general, columnas_nuevas] = read_file(path_archivo, True)
            columnas.extend(columnas_nuevas)
        else:
            [nuevo_balance, columnas_nuevas] = read_file(path_archivo, False)
            columnas.extend(columnas_nuevas)
            balance_general = pd.concat([balance_general, nuevo_balance], ignore_index=True, axis=1)
    balance_general.columns = columnas
    balance_general.to_csv('../agent_api/data/database/mi_archivo.csv', index=False, sep=";")
    balance_general = balance_general.dropna(axis=0)
    json_datos = convertir_columnas_a_json(balance_general)
    with open("./agent_api/data/database/datos_financieros.json", "w") as f:
        json.dump(json_datos, f, indent=2)

except Exception as e:
    print(f"❌Error al procesar el archivo {path_archivo}: {e}")