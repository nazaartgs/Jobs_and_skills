import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def tierra(df):  

    st.subheader("Análisis Geográfico: Salarios y Vacantes por Industria")

    coordenadas = {
        'Singapore': {'lat': 1.3521, 'lon': 103.8198},
        'Tokyo': {'lat': 35.6895, 'lon': 139.6917},
        'London': {'lat': 51.5074, 'lon': -0.1278},
        'New York': {'lat': 40.7128, 'lon': -74.0060},
        'Dubai': {'lat': 25.2048, 'lon': 55.2708},
        'Berlin': {'lat': 52.5200, 'lon': 13.4050}
    }

    df_geo = df.groupby(['location', 'industry']).agg(
        salario_promedio=('salary_usd', 'mean'),
        vacantes=('job_id', 'count')
    ).reset_index()

    df_mapa = df.groupby('location').agg(
    salario_promedio=('salary_usd', 'mean'),
    vacantes=('job_id', 'count')
).reset_index()

    df_mapa['lat'] = df_mapa['location'].map(lambda x: coordenadas.get(x, {}).get('lat'))
    df_mapa['lon'] = df_mapa['location'].map(lambda x: coordenadas.get(x, {}).get('lon'))
    df_mapa = df_mapa.dropna(subset=['lat', 'lon'])

    hover_text = []
    for loc in df_mapa['location']:
        detalles = df_geo[df_geo['location'] == loc]
        texto = f"<b>{loc}</b><br>"
        for _, row in detalles.iterrows():
            texto += f"• {row['industry']}: {row['vacantes']} vacantes<br>"
        hover_text.append(texto)

    fig = go.Figure(
        data=go.Scattergeo(
            lat=df_mapa['lat'],
            lon=df_mapa['lon'],
            mode='markers',
            marker=dict(
                size=df_mapa['vacantes'] / df_mapa['vacantes'].max() * 50, 
                color=df_mapa['salario_promedio'],
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(
                    title="Salario Promedio (USD)",
                    orientation="h",
                    x=0.5, y=1.1,
                    xanchor="center",
                    len=0.4
                )
            ),
            text=hover_text,
            hoverinfo='text'
        ),
    )

    fig.update_geos(
        projection_type="orthographic",
        showcountries=True, countrycolor="white",
        showland=True, landcolor="#228b22",
        showocean=True, oceancolor="#1a5e8a",
        bgcolor="rgba(0,0,0,0)",
        resolution=110
    )

    fig.update_layout(
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        margin={"r":0,"t":100,"l":0,"b":0},
    )

    st.plotly_chart(fig, use_container_width=True)