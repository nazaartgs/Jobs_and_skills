import streamlit as st
import pandas as pd 
import plotly.express as px
from procesamiento_datos import cargar_datos as data

def Dataset():

    #llamamos la funcion data
    resumen_dataset = data()

    #creamos columnas para mostrar la informacion resumida.
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        Cantidad_datos = resumen_dataset['job_id'].count()
        st.metric("Registros", f"{Cantidad_datos:,}")

    with m2:
        Cantidad_Null = resumen_dataset.isnull().sum().sum()
        st.metric("Registros NULL", f"{Cantidad_Null}")

    with m3:
        Cantidad_dtype = resumen_dataset.dtypes.nunique()
        st.metric("Cantidad de tipos de variables ", f"{Cantidad_dtype}")

    with m4:
        Cantidad_columnas = resumen_dataset.shape
        st.metric("Cantidad de Variables (filas, Columnas)", f"{Cantidad_columnas}")
    