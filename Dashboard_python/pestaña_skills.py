import pandas as pd

import streamlit as st

import plotly.express as px



def habilidades(Datos_para_pestaña):

    df_skills = Datos_para_pestaña.copy()

    df_skills['skills_required'] = df_skills['skills_required'].apply(

        lambda x: x.split(',') if isinstance(x, str) else x
    )

    df_exploded = df_skills.explode('skills_required')

    df_exploded['skills_required'] = df_exploded['skills_required'].str.strip().str.lower()

    df_exploded['skills_required'] = df_exploded['skills_required'].str.title()

    df_exploded = df_exploded[df_exploded['skills_required'] != '']

    if 'job_id' in df_exploded.columns:
        df_exploded = df_exploded.drop_duplicates(subset=['job_id', 'skills_required'])

    industrias = df_exploded['industry'].unique()

    sector_seleccionado = st.selectbox("Selecciona un sector para ver sus habilidades críticas:", industrias)

    df_sector = df_exploded[df_exploded['industry'] == sector_seleccionado]

    conteo_skills = df_sector['skills_required'].value_counts().reset_index()

    conteo_skills.columns = ['Habilidad', 'Frecuencia']

    top_skills = conteo_skills.head(10).sort_values('Frecuencia', ascending=True)

    #top_skills = top_skills.tail(20)
   
    fig_bar = px.bar(
        top_skills,
        x='Frecuencia',
        y='Habilidad',
        orientation='h',
        title=f"Top Habilidades en el sector: {sector_seleccionado}",
        color='Frecuencia',
        color_continuous_scale='rdylbu'
    )

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_bar, use_container_width=True)