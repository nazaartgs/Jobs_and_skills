import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def tierra(Data_aprocesar):  

    #Datos
    df_prueba = pd.DataFrame({
        'ciudad': ['Singapore', 'Tokyo', 'London', 'New York', 'Dubai', 'Berlin'],
        'salario_promedio': [150194, 149483, 152260, 152266, 148622, 147965],
        'vacantes': [1640, 1660, 1656, 1689, 1682, 1673],
        'lat': [1.3521, 35.6895, 51.5074, 40.7128, 25.2048, 52.5200],
        'lon': [103.8198, 139.6917, -0.1278, -74.0060, 55.2708, 13.4050]
    })

    #Construcción de la figura con Graph Objects
    fig = go.Figure(
        data=go.Scattergeo(
            lat=df_prueba['lat'],
            lon=df_prueba['lon'],
            mode='markers',
            marker=dict(
                size=df_prueba['vacantes']/50, # Ajuste de tamaño
                color=df_prueba['salario_promedio'],
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(
                    title="Salario Promedio (USD)",
                    orientation="h",
                    x=0.5, y=1.1,
                    xanchor="center"
                )
            ),
            text=df_prueba['ciudad'],
            hoverinfo="text+lat+lon"
        ),
    )

    #Configuración estética de la esfera
    fig.update_geos(
        projection_type="orthographic",
        showcountries=True, countrycolor="white",
        showland=True, landcolor="#228b22",
        showocean=True, oceancolor="#1a5e8a",
        bgcolor="rgba(0,0,0,0)",
        resolution=110
    )

    # ⚙️ Configuración del Layout
    fig.update_layout(
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        margin={"r":0,"t":100,"l":0,"b":0},
    )

    st.plotly_chart(fig, use_container_width=True)