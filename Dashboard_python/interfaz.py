import streamlit as st
import plotly.express as px
#importacion de scripts
from procesamiento_datos import cargar_datos, exploracion_datos, skills_copy as data


#configuramos la app web
st.set_page_config(page_title="Mercado Laboral 2025", page_icon="💼", layout="wide")