import streamlit as st


def render_sidebar(df=None):
    with st.sidebar:
        st.markdown("## Navegacion")
        st.markdown("Usa el menu para moverte entre capitulos.")
        if df is not None:
            st.markdown("---")
            st.markdown("### Filtros")
            st.markdown("Los filtros se agregaran aqui segun el dataset.")
