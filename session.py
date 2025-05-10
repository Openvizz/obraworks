import streamlit as st

def init_session():
    variaveis = {
        "logado": False,
        "usuario": None,
        "perfil": None,
        "tipo": None,
        "dados_compartilhados": {}
    }
    for chave, valor in variaveis.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor
