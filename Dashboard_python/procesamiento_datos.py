import pandas as pd

def cargar_datos():
    #cargamos el dataset que vamos a analizar.
    df =pd.read_csv("data/Data_sinprocesar/10. Job y Skills.csv")

    return df

datos_sinprocesar = cargar_datos()

def exploracion_datos(datos_sinprocesar):
    #exploramos las 10 primeras filas del data set
    print(" ")
    print("--- Primeras 10 filas del Dataset ---")
    print(datos_sinprocesar.head(10))

    #evaluamos la informacion del dataset
    print(" ")
    print("--- Informacion del Dataset ---")
    print(datos_sinprocesar.info())


    #Hacemos una descripcion estadistica del Dataset
    print(" ")
    print("--- Descripcion estadistica del Dataset ---")
    print(datos_sinprocesar.describe())
    print(" ")

    
    return datos_sinprocesar

datos_explo = exploracion_datos(datos_sinprocesar)
data_pais = datos_explo.groupby('location')['salary_usd'].agg(['mean', 'count']).reset_index()
top_ciudades = data_pais.sort_values('location', ascending=True)

print(data_pais)

def skills_copy():
    
    #creamos una copia de la columna
    df_skills = datos_explo.copy()

    #separamos los datos de la columna en listas
    df_skills["skills_required"] = df_skills["skills_required"].str.split(',')

    #le asignamo una fila a cada skill
    df_skills = df_skills.explode('skills_required')

    print(df_skills)
    return skills_copy

datos_skills = skills_copy()