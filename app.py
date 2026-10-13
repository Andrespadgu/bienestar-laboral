import streamlit as st
from utils.styles import inject_css

st.set_page_config(
    page_title="Bienestar Laboral — EDA",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

pg = st.navigation([
    st.Page("portada.py",                                title="Portada"),
    st.Page("pages/01_introduccion.py",                  title="Introducción"),
    st.Page("pages/02_panorama_general.py",              title="Panorama general"),
    st.Page("pages/03_distribucion_variables.py",        title="Distribución de variables"),
    st.Page("pages/04_relaciones.py",                    title="Relaciones"),
    st.Page("pages/05_hallazgos.py",                     title="Hallazgos"),
])
pg.run()
