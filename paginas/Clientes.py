import streamlit as st
import pandas as pd
from datetime import datetime

def clientes():
    st.title("Clientes")
    st.write("Preencha as informações necessárias para registrar um novo cliente no sistema.")

    def cadastro():
        st.subheader("Formulário de Cadastro de Clientes")

        # Obter data e hora atual
        data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # 🔑 Controle fora do formulário
        options = ["Pessoa Física", "Pessoa Jurídica"]
        selection = st.segmented_control("Selecione o Tipo de Cliente:", options, selection_mode="single")
        
        if selection != None:
            if selection == "Pessoa Física":
                with st.form("Cadastro de Cliente", clear_on_submit=True, border=True):
                    st.subheader("Informações do Cliente")
                    st.write("Você está cadastrando um cliente do tipo: **{}**".format(selection))
                    col1, col2 = st.columns(2)

                    with col1:
                        nome = st.text_input("Nome Completo", placeholder="Ex: João da Silva")
                        telefone = st.text_input("Telefone", placeholder="Ex: (11) 99999-9999")
                        email = st.text_input("E-mail", placeholder="Ex: exemplo@exemplo.com")
                    with col2:
                        cidade = st.selectbox("Cidade", ["Selecione a cidade", "São Paulo", "Rio de Janeiro", "Outro"])
                        uf = st.selectbox("UF", ["Selecione o estado", "SP", "RJ", "MG", "Outro"])
                        st.text_input("Data do Cadastro", value=data_hora_atual, disabled=True)

                    submitted = st.form_submit_button("Cadastrar Cliente")

                    if submitted:
                        erros = []
                        if not nome:
                            erros.append("Nome Completo")
                        if not telefone:
                            erros.append("Telefone")

                        if cidade == "Selecione a cidade":
                            erros.append("Cidade")
                        if uf == "Selecione o estado":
                            erros.append("UF")

                        if erros:
                            st.error(f"Os seguintes campos são obrigatórios: {', '.join(erros)}.")
                        else:
                            st.success(f"Cliente '{nome}' cadastrado com sucesso!")
            else:
                with st.form("Cadastro de Cliente", clear_on_submit=True, border=True):
                    st.subheader("Informações do Cliente")
                    st.write("Você está cadastrando um cliente do tipo: **{}**".format(selection))
                    col1, col2 = st.columns(2)

                    with col1:
                        Razao = st.text_input("Razão Social", placeholder="Ex: Empresa LTDA")
                        Fantasia = st.text_input("Nome Fantasia", placeholder="Ex: Empresa LTDA")
                        CNPJ = st.text_input("CNPJ", placeholder="Ex: 99.999.999/9999-99")
                    with col2:
                        cidade = st.selectbox("Cidade", ["Selecione a cidade", "São Paulo", "Rio de Janeiro", "Outro"])
                        uf = st.selectbox("UF", ["Selecione o estado", "SP", "RJ", "MG", "Outro"])
                        st.text_input("Data do Cadastro", value=data_hora_atual, disabled=True)

                    submitted = st.form_submit_button("Cadastrar Cliente")

                if submitted:
                    erros = []
                    if not Razao:
                        erros.append("Razão Social")
                    if not Fantasia:
                        erros.append("Fantasia")
                    if not CNPJ:
                        erros.append("CNPJ")
                    if cidade == "Selecione a cidade":
                        erros.append("Cidade")
                    if uf == "Selecione o estado":
                        erros.append("UF")

                    if erros:
                        st.error(f"Os seguintes campos são obrigatórios: {', '.join(erros)}.")
                    else:
                        st.success(f"Cliente '{nome}' cadastrado com sucesso!")
        else:
            st.info("Selecione primeiro o tipo de cliente para continuar o cadastro.")

    # ==========================================
    # TABELA DE CLIENTES (simulada para exemplo)
    # ==========================================
    def lista_clientes():
        st.subheader("Tabela de Clientes")
        st.write("Tabela com os clientes cadastrados no sistema.")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.selectbox("Código:", [1,2,3,4,5,6,7,8,9,10],placeholder="Pesquisar por Código",index=None)
        with col2:
            st.selectbox("Nome/Razão:", ["Empresa A", "Empresa B", "Empresa C"],placeholder="Pesquisar por Nome",index=None)
        with col3:
            st.selectbox("Filtrar por Tipo:", ["Pessoa Física", "Pessoa Jurídica"],placeholder="Pesquisar por Tipo",index=None)
        with col4:
            st.selectbox("Situação:", ["Ativo", "Inativo"],placeholder="Pesquisar por Situação",index=None)

        # Exemplo de dados simulados
        dados_clientes = pd.DataFrame({
            "ID": [1, 2, 3],
            "Tipo": ["Pessoa Física", "Pessoa Jurídica", "Pessoa Jurídica"],
            "Nome/Razão": ["João da Silva", "Empresa X LTDA", "Empresa Y ME"],
            "Telefone/CNPJ": ["(11) 99999-9999", "12.345.678/0001-90", "98.765.432/0001-55"],
            "Cidade": ["São Paulo", "Rio de Janeiro", "Outro"],
            "UF": ["SP", "RJ", "MG"],
            "Data Cadastro": ["10/05/2025 14:00:00", "10/05/2025 14:05:00", "10/05/2025 14:10:00"],
            "Situação": ["Ativo", "Inativo", "Pendente"]
            })

        dados_limitados = dados_clientes.head(20)  # Exibe apenas os 20 primeiros registros

        editado = st.data_editor(
            dados_clientes,
            column_config={
                "ID": st.column_config.NumberColumn(disabled=True),
                "Tipo": st.column_config.TextColumn(disabled=True),
                "Nome/Razão": st.column_config.TextColumn(disabled=True),
                "Telefone/CNPJ": st.column_config.TextColumn(disabled=True),
                "Cidade": st.column_config.TextColumn(disabled=True),
                "UF": st.column_config.TextColumn(disabled=True),
                "Data Cadastro": st.column_config.TextColumn(disabled=True),
                "Situação": st.column_config.SelectboxColumn(options=["Ativo", "Inativo", "Pendente"])
            },
            use_container_width=True,
            hide_index=True,
            row_height = 40
        )

        # Contar clientes ativos e inativos
        contagem = dados_clientes["Situação"].value_counts()

        ativos = contagem.get("Ativo", 0)
        inativos = contagem.get("Inativo", 0)
        
        st.badge(f"Ativos: **{ativos}**", icon=":material/check:", color="green")
        st.badge(f"Inativos: **{inativos}**", icon=":material/delete:", color="red")


    # st.write("Dados após edição (não salva no banco ainda):")
    # st.dataframe(editado, use_container_width=True, hide_index=True,row_height = 40)

    tabs = st.tabs(["Cadastro", "Lista de Clientes"])

    with tabs[0]:
        cadastro()
    with tabs[1]:
        lista_clientes()