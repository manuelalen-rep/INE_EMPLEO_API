import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')
HOST = os.getenv('DB_HOST')
DB = os.getenv('DB_NAME')

if not all([USER, PASS, HOST, DB]):
    raise ValueError("Faltan variables en el archivo .env")


engine = create_engine(f"mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}")

def extraer_e_insertar_ine(id_tabla, tipo_tabla):
    print(f"Descargando la tabla {id_tabla} ({tipo_tabla})...")
    
    url = f"https://servicios.ine.es/wstempus/js/es/DATOS_TABLA/{id_tabla}?tip=AM"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Error HTTP: {response.status_code}")
        return
    
    data = response.json()
    registros = []
    
    for serie in data:

        nombre_serie = serie.get("Nombre", "")
        

        partes = [p.strip() for p in nombre_serie.split('.') if p.strip()]
        
        datos_serie = serie.get("Data", [])
        
        for dato in datos_serie:
            if tipo_tabla == "COMPOSICION_SALARIO_BRUTO":
   
                registros.append({
                    "sexo": partes[2] if len(partes) > 2 else "Total",
                    "cno11": partes[3] if len(partes) > 3 else "Total",
                    "componentes_salario": partes[4] if len(partes) > 4 else "Total",
                    "salario": dato.get("Valor")
                })
                
            elif tipo_tabla == "OCUPACIONES":

                registros.append({
                    "ocupacion": partes[3] if len(partes) > 3 else "Total",
                    "sexo": partes[2] if len(partes) > 2 else "Total",
                    "tipo_dato": partes[4] if len(partes) > 4 else "Total",
                    "periodo": dato.get("Anyo"),
                    "numero_trabajadores": dato.get("Valor")
                })

    df = pd.DataFrame(registros)
    
    if df.empty:
        print(f"⚠️ No hay datos para {id_tabla}.")
        return


    if tipo_tabla == "COMPOSICION_SALARIO_BRUTO":
        df = df[['sexo', 'cno11', 'componentes_salario', 'salario']]
    elif tipo_tabla == "OCUPACIONES":
        df = df[['ocupacion', 'sexo', 'tipo_dato', 'periodo', 'numero_trabajadores']]


    print(f"Insertando {len(df)} filas en la tabla {tipo_tabla}...")
    try:
        df.to_sql(name=tipo_tabla.lower(), con=engine, if_exists='append', index=False)
        print("✅ Inserción completada.\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


extraer_e_insertar_ine('36838', 'COMPOSICION_SALARIO_BRUTO')
extraer_e_insertar_ine('65967', 'OCUPACIONES')