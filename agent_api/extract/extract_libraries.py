import pdfplumber
from datetime import datetime
from pdf_to_csv import leer_txt
import pandas as pd

def read_file(ruta_archivo: str, primera_fila: bool):
    try:
        return crear_balance_general(ruta_archivo, primera_fila)
    except Exception as e:
        print(f"Error al procesar el archivo {ruta_archivo}: {e}")

# def use_tabula(ruta_archivo: str):
#     dfs = tabula.read_pdf(ruta_archivo, stream=True)
#     nombre_logs = generar_nombre_archivo("tabula", ".csv")
#     tabula.convert_into(ruta_archivo, nombre_logs, output_format="csv")

def crear_balance_general(ruta_archivo: str, primera_fila: bool):
    nombre_logs = generar_nombre_archivo("plumber", ".txt")
    with pdfplumber.open(ruta_archivo) as pdf, open(nombre_logs, "a", encoding="utf-8") as log_file:
        pagina_0 = pdf.pages[0]
        text_line = pagina_0.extract_text()
        list_atributos = text_line.split(" ")
        log_file.write(("|").join(list_atributos) + "\n")
    [balance_general, columnas] = leer_txt(nombre_logs, primera_fila)
    return [balance_general, columnas]

# def use_pymupdf(ruta_archivo: str):
#     nombre_logs = generar_nombre_archivo("pymupdf", ".txt")
#     doc = pymupdf.open(ruta_archivo)
#     with open(nombre_logs, "a", encoding="utf-8") as log_file:
#         for page in doc:
#             # print("PYMU ->", page) # page 0 of /Users/vivianavera03/Desktop/Bco Guayaquil/ai-agent/extract/../docs/uploaded/BalancesBG/ESTADOS_FINANCIEROS_WEB_BG_SEPTIEMBRE2024.pdf
#             text = page.get_text()
#             log_file.write(text + "\n")

def generar_nombre_archivo(libreria: str, extension: str):
    ahora = datetime.now()
    timestamp = ahora.strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"./ai-agent/docs/txt/{libreria}_{timestamp}.{extension}"
    return nombre_archivo