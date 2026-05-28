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

def extraer_nueva_tabla_ine_nombres():
    id_tabla = '69069'
    esquema_destino = 'BRONZE'
    nombre_tabla = 'm_agregados_x_rama'
    
    print(f"Descargando todos los datos de la tabla {id_tabla}...")
    url = f"https://servicios.ine.es/wstempus/js/es/DATOS_TABLA/{id_tabla}?tip=AM"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Error HTTP: {response.status_code}")
        return
    
    data = response.json()
    registros = []
    
    
    nombres_campos = ['Total_Nac', 'Tipo_variable', 'rama', 'tipo_precio', 'tipo_dato']
    
  
    for serie in data:
        nombre_serie = serie.get("Nombre", "")
        partes = [p.strip() for p in nombre_serie.split('.') if p.strip()]
        
        for dato in serie.get("Data", []):
            registro = {
                "anyo": dato.get("Anyo"),
                "fk_periodo": dato.get("FK_Periodo"),
                "fecha": dato.get("Fecha"),
                "valor": dato.get("Valor")
            }
            

            for i, col in enumerate(nombres_campos):
                registro[col] = partes[i] if i < len(partes) else None
                
            registros.append(registro)
            
    df = pd.DataFrame(registros)
    
    if df.empty:
        print("⚠️ No se han encontrado datos.")
        return
        
    df = df[nombres_campos + ['anyo', 'fk_periodo', 'fecha', 'valor']]
    
    print(f"Insertando {len(df)} filas en {esquema_destino}.{nombre_tabla}...")
    

    try:
        df.to_sql(
            name=nombre_tabla, 
            con=engine, 
            schema=esquema_destino, 
            if_exists='replace',
            index=False
        )
        print(f"✅ Tabla creada y datos insertados con éxito en BRONZE.{nombre_tabla}.")
    except Exception as e:
        print(f"❌ Error crítico: {e}")

extraer_nueva_tabla_ine_nombres()