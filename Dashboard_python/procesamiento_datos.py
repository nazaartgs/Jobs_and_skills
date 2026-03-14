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
top_pais = datos_explo.groupby('location')['salary_usd'].agg(['mean', 'count']).reset_index()
top_ciudades = top_pais.sort_values('location', ascending=True)

print(top_pais)

def skills_copy(datos_sinprocesar):
    
    #creamos una copia de la columna
    df_skills = datos_sinprocesar.copy()

    #separamos los datos de la columna en listas
    df_skills["skills_required"] = df_skills["skills_required"].str.split(',')

    #le asignamo una fila a cada skill
    df_skills = df_skills.explode('skills_required')

    #limpieza de cadenas
    df_skills["skills_required"] = df_skills["skills_required"].str.strip()


    print(df_skills)

    

    return df_skills

datos_skills = skills_copy(datos_sinprocesar)


skills_count = datos_skills.groupby(['skills_required','industry'])['salary_usd' ].agg([ 'mean', 'count']).reset_index()
top_skills = skills_count.sort_values('count', ascending=True)

print(top_skills)
