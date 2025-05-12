import streamlit as st
import json
import os

CAMINHO_JSON = "utils/usuarios.json"

def carregar_usuarios():
    if not os.path.exists(CAMINHO_JSON):
        st.error(f"Arquivo {CAMINHO_JSON} não encontrado!")
        return {}
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def login():
    st.subheader("Acesso ao Projetum")
    st.write("Usuário: Alex")
    st.write("Senha: 123")
    st.logo("utils/Logo.svg", link="https://linktr.ee/openviz")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        dados = carregar_usuarios()
        usuarios = dados.get("usuarios", {})

        if usuario in usuarios and senha == usuarios[usuario]["senha"]:
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["perfil"] = usuarios[usuario]["perfil"]
            st.session_state["tipo"] = usuarios[usuario]["tipo"]
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Credenciais inválidas 🚨")
