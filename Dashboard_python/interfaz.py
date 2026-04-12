import streamlit as st
#importacion de scripts
from procesamiento_datos import cargar_datos
from pestaña_resumenDataset import Dataset
from pestaña_salario import salario
from pestaña_remoto import remoto
from pestaña_geogafria import tierra
from pestaña_skills import habilidades
from pestaña_empresa import empresa


#configuramos la app web
st.set_page_config(page_title="Mercado Laboral 2025", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

def cambiar_fondo_color(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
cambiar_fondo_color("#FFFFFF")

def aplicar_estilos_globales(fondo, texto_principal, texto_titulos):
    st.markdown(
        f"""
        <style>
        /* Fondo de la aplicación */
        .stApp {{
            background-color: {fondo};
        }}

        /* Color de texto general (párrafos, listas, etc.) */
        .stApp p, .stApp span, .stApp label, .stApp li {{
            color: {texto_principal} !important;
        }}

        /* Color de los Títulos (h1, h2, h3) */
        h1, h2, h3, h4, h5, h6 {{
            color: {texto_titulos} !important;
        }}

        /* Color de los nombres de las Pestañas (Tabs) */
        button[data-baseweb="tab"] div p {{
            color: {texto_titulos} !important;
            font-weight: bold;
        }}
        
        /* Color de los textos en la barra lateral */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
            color: {texto_principal} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
#Aplicamos los colores (Fondo Blanco, Texto Azul Marino, Títulos Azul Oscuro)
aplicar_estilos_globales("#FFFFFF", "#1E3A8A", "#0F172A")

#Llamamos las funcion cargar_datos y cargamos los datos en cache
Data_aprocesar = cargar_datos()

#creamos titulo de la pagina
st.title("Mercado laboral - Alta Tecnologia 2025")

#creamos las pestañas con nombres referentes a nuestros objetivos.
pestaña_resumen_dataset, pestaña_salarial, pestaña_remoto, pestaña_geogafria, pestaña_skills, pestaña_empresa = st.tabs([
    "Resumen dataset",
    "Distribución Salarial", 
    "Impacto Remoto", 
    "Análisis Geográfico", 
    "Habilidades Críticas", 
    "Tamaño de Empresa"
    ])

#1. Pestaña resumen
with pestaña_resumen_dataset:
    st.header("Analisis descriptivo del Dataset 📁")
    Dataset(Data_aprocesar)

#2. Pestaña salarial
with pestaña_salarial:
    st.header("Estadistica descriptiva del salario en las industrias")
    salario(Data_aprocesar)

#3. Pestaña de trabajo remoto
with pestaña_remoto:
    st.header("Análisis del impacto salarial en los trabajos remotos")
    remoto(Data_aprocesar)
    

#4. Pestaña de geografia
with pestaña_geogafria:
    st.header("Globo Terráqueo de Empleos 🌍")
    tierra(Data_aprocesar)

#5. Pestaña de habilidades
with pestaña_skills:
    st.header("Habilidades más demandadas por Sector")
    habilidades(Data_aprocesar)

#6. Pestaña tamaño de la empresa
with pestaña_empresa:
    st.header("Análisis de Salarios según Tamaño de Empresa")
    empresa(Data_aprocesar)