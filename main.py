import streamlit as st
from paginas import (
    Home, Configuracao, Credenciamento,
    Obras, Clientes, Equipes, Feriados, Materiais
)
from auth import login
from session import init_session

init_session()

st.set_page_config(layout="wide", page_title="Openviz | Home", page_icon="utils/favicon.svg")

# Logo
st.logo("utils/Logo.svg", link="https://linktr.ee/openviz")

def logout():
    chaves = list(st.session_state.keys())
    for chave in chaves:
        del st.session_state[chave]
    st.rerun()

if not st.session_state["logado"]:
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        login()
else:
    if st.session_state["logado"]:
        st.sidebar.write(f"🧑‍💻 **Usuário**: `{st.session_state['usuario']}`")
        if st.sidebar.button("🔓 Sair"):
            logout()
        st.sidebar.markdown("---")

    # Menu com st.navigation
    tipo = st.session_state.get("tipo", "")

    pages = {
        "Principal": [
            st.Page(Home.home, title="🏠 Home")
        ],
        "Cadastros": [
            st.Page(Obras.obras, title="🏗️ Obras"),
            st.Page(Clientes.clientes, title="👥 Clientes"),
            st.Page(Equipes.equipes, title="🧑‍🔧 Equipes"),
            st.Page(Feriados.feriados, title="📅 Feriados"),
            st.Page(Materiais.materiais, title="📦 Materiais")
        ]
    }

    # Apenas master pode ver menu de Credenciamento
    if tipo == "master":
        pages["Credenciamento"] = [
            st.Page(Credenciamento.credenciamento, title="🛂 Credenciamento"),
            st.Page(Configuracao.configuracao, title="⚙️ Configuração")
        ]

    pg = st.navigation(pages)
    pg.run()