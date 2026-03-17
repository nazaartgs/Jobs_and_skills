import streamlit as st
import pandas as pd 
import plotly.express as px

def Dataset(Data_aprocesar):

    #llamamos la funcion data
    resumen_dataset = Data_aprocesar

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
        Cantidad_columnas = resumen_dataset.shape[1]
        st.metric("Cantidad de Variables (Columnas)", f"{Cantidad_columnas}")

    st.divider()

    #------- tabla interactiva del dataframe ------
    st.subheader("Explorador de Datos 🔍")

    # 1. Controles de usuario
    col_filtro1, col_filtro2 = st.columns(2)

    with col_filtro1:
        #Definimos el límite de visualización (del slider)
        limite_filas = st.slider("Filas a visualizar en la tabla:", 1, 10, 1000)

    with col_filtro2:
        #Definimos el filtro de categoría
        opciones_industria = ["Todas"] + list(resumen_dataset['industry'].unique())
        seleccion_industria = st.selectbox("Filtrar por Industria:", opciones_industria)

    #Lógica de filtrado (Primero filtramos por industria)
    if seleccion_industria != "Todas":
        df_filtrado = resumen_dataset[resumen_dataset['industry'] == seleccion_industria]
    else:
        df_filtrado = resumen_dataset

    # 2. Usar el DataFrame filtrado para las métricas y la tabla
    total_en_seleccion = df_filtrado.shape[0]
    st.write(f"La industria **{seleccion_industria}** tiene un total de **{total_en_seleccion:,}** registros.")

    datos_a_mostrar = df_filtrado.head(limite_filas)
    st.dataframe(datos_a_mostrar, use_container_width=True)
    