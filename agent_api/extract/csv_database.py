import pandas as pd
import os

ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'data', 'database', 'mi_archivo.csv')
ruta_archivo_output = os.path.join(os.path.dirname(__file__), '..', 'data', 'database', 'mi_archivo2.csv')

ruta_absoluta = os.path.abspath(ruta_archivo)

df = pd.read_csv(ruta_absoluta, header=None, sep=";")
df = df.T
df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)
df.to_csv(ruta_archivo_output, index=False, encoding="utf-8", sep=";")

print(df.head())