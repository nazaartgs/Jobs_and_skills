import streamlit as st
import pandas as pd
import os

@st.cache_data

def cargar_datos():
    #Obtenemos la ruta de la carpeta donde está este script
    ruta_actual = os.path.dirname(__file__) 
    
    #Construimos la ruta subiendo un nivel y entrando a Data
    ruta_csv = os.path.join(ruta_actual, "..", "Data", "Data_sinprocesar", "10. Job y Skills.csv")
    
    #cargamos el dataset que vamos a analizar.
    df =pd.read_csv(ruta_csv)

    #Limpieza: Eliminas filas duplicadas, el drop_duplicates evita contar dos veces el mismo empleo
    df = df.drop_duplicates(subset=['job_id'])

    #Limpieza: manejo de valores nulos (vacios)
    #Limpieza: si falta un dato de salario, dropna elimina la fila donde falta informacion critica
    df = df.dropna(subset=['salary_usd'])

    #Limpieza: si falta la habilidad, fillna rellena huecos con texto por defecto como "no especificado"
    df['skills_required'] = df['skills_required'].fillna("Skills no especificado") 

    #Limpieza: astype cambia el formato de los datos, en este caso a enteros
    df['salary_usd'] = df['salary_usd'].astype(int)

    #A la izquierda creamos una variable donde gurdaremos el resultado
    #a la derecha colocamos la funcion to_datatime para tranformar el archivo a fecha 
    df['posting_date'] = pd.to_datetime(df['posting_date'])

    return df

