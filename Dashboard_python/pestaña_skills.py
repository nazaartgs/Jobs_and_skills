import pandas as pd
import streamlit as st
import plotly.express as px

def habilidades(Datos_para_pestaña):
    # Trabajamos sobre una copia para no alterar el DataFrame original
    df_skills = Datos_para_pestaña.copy()
    
    # 1. Separamos por coma (así no dependemos de si hay un espacio o no)
    if df_skills['skills_required'].dtype == 'object':
        df_skills['skills_required'] = df_skills['skills_required'].str.split(',')
    
    # 2. Multiplicamos las filas para tener una habilidad por fila
    df_exploded = df_skills.explode('skills_required')
    
    # 3. LIMPIEZA CLAVE: Eliminamos espacios en blanco al inicio o final de cada palabra
    df_exploded['skills_required'] = df_exploded['skills_required'].str.strip()
    
    # 4. HOMOLOGACIÓN: Convertimos la primera letra en mayúscula (ej: "python" y "Python" se vuelven iguales)
    df_exploded['skills_required'] = df_exploded['skills_required'].str.capitalize()

    # 5. Eliminamos registros vacíos (por si en el CSV venían comas seguidas ",,")
    df_exploded = df_exploded[df_exploded['skills_required'] != '']

    # 6. EVITAR DOBLE CONTEO: No contamos la misma habilidad dos veces para un mismo empleo (job_id)
    if 'job_id' in df_exploded.columns:
        df_exploded = df_exploded.drop_duplicates(subset=['job_id', 'skills_required'])

    # Selector de industrias
    industrias = df_exploded['industry'].unique()
    sector_seleccionado = st.selectbox("Selecciona un sector para ver sus habilidades críticas:", industrias)

    # Filtrado por sector
    df_sector = df_exploded[df_exploded['industry'] == sector_seleccionado]
    
    # Conteo de frecuencias de cada habilidad
    conteo_skills = df_sector['skills_required'].value_counts().reset_index()
    conteo_skills.columns = ['Habilidad', 'Frecuencia']

    # Ordenamos de menor a mayor para que las barras más grandes queden arriba en la gráfica horizontal
    top_skills = conteo_skills.sort_values('Frecuencia', ascending=True)
    
    # Opcional: Limitamos a las top 20 habilidades para no saturar la gráfica si hay demasiadas
    top_skills = top_skills.tail(20)
    
    # Creación del gráfico de barras horizontal
    fig_bar = px.bar(
        top_skills,
        x='Frecuencia',
        y='Habilidad',
        orientation='h',
        title=f"Top Habilidades en el sector: {sector_seleccionado}",
        color='Frecuencia',
        color_continuous_scale='Blues'
    )
    
    # Hacemos el fondo transparente para que se acople al diseño
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Dibujamos la gráfica
    st.plotly_chart(fig_bar, use_container_width=True)