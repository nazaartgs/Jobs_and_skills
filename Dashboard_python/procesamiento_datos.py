import pandas as pd

def cargar_datos():
    #cargamos el dataset que vamos a analizar.
    df =pd.read_csv("data/Data_sinprocesar/10. Job y Skills.csv")

    return df


def exploracion_datos(cargar_datos, top_ciudades):
    #exploramos las 10 primeras filas del data set
    print(" ")
    print("--- Primeras 10 filas del Dataset ---")
    print(cargar_datos.head(10))

    #evaluamos la informacion del dataset
    print(" ")
    print("--- Informacion del Dataset ---")
    print(cargar_datos.info())


    #Hacemos una descripcion estadistica del Dataset
    print(" ")
    print("--- Descripcion estadistica del Dataset ---")
    print(cargar_datos.describe())
    print(" ")

    top_pais = cargar_datos.groupby('location')['salary_usd'].agg(['mean', 'count']).reset_index()
    top_ciudades = top_pais.sort_values('location', ascending=True)

    return cargar_datos, top_ciudades


def skills_copy(datos_sinprocesar, top_skills):
    
    #creamos una copia de la columna
    df_skills = datos_sinprocesar.copy()

    #separamos los datos de la columna en listas
    df_skills["skills_required"] = df_skills["skills_required"].str.split(',')

    #le asignamo una fila a cada skill
    df_skills = df_skills.explode('skills_required')

    #limpieza de cadenas
    df_skills["skills_required"] = df_skills["skills_required"].str.strip()


    print(df_skills)

    skills_count = df_skills.groupby(['skills_required','industry'])['salary_usd' ].agg([ 'mean', 'count']).reset_index()
    top_skills = skills_count.sort_values('count', ascending=True)


    return df_skills, top_skills
