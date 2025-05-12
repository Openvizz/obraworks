import streamlit as st
import pandas as pd
from datetime import datetime, time

def equipes():
    st.title("🧑‍🔧 Equipe")
    st.write("Preencha as informações necessárias para registrar um novo membro de equipe.")

    def cadastro():
        st.subheader("Cadastro de Equipe")

        # Obter data e hora atual
        data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with st.form("Cadastro de Equipe", clear_on_submit=True, border=True):
            st.subheader("Dados Pessoais e Identificação")
            col1, col2 = st.columns(2)

            with col1:
                nome = st.text_input("Nome Completo", placeholder="Ex: João da Silva",icon=":material/badge:")
                CPF = st.text_input("CPF", placeholder="Ex: 000.000.000-00", max_chars=11,icon=":material/id_card:")
                RG = st.text_input("RG", placeholder="Ex: 00.000.000-0",max_chars=9,icon=":material/id_card:")
                Nascimento = st.date_input("Data de Nascimento",value=None,format="DD/MM/YYYY")
            with col2:
                Sexo = st.selectbox("Sexo", ["Masculino", "Feminino"],placeholder="Selecione o sexo",index=None)
                estado_civil = st.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)","Viúvo(a)"],placeholder="Selecione o estado civil",index=None)
                nacionalidade = st.selectbox("Nacionalidade", ["Brasileiro", "Estrangeiro"],placeholder="Selecione a nacionalidade",index=None)

            st.divider()

            st.subheader("Informações Trabalhistas")
            col3, col4 = st.columns(2)

            with col3:
                area = st.selectbox("Área", ["Canteiro de Obras"],placeholder="Selecione a área",index=None)
                cargo = st.selectbox("Cargo", ["Mestre de Obras",
                                                "Encarregado de Obras",
                                                "Encarregado de Elétrica",
                                                "Encarregado de Hidráulica",
                                                "Carpinteiro",
                                                "Pedreiro",
                                                "Armador",
                                                "Eletricista",
                                                "Encanador",
                                                "Operador de Máquinas",
                                                "Ajudante Geral"],
                                                placeholder="Selecione o cargo",
                                                index=None
                                                )
                                        
            with col4:
                Tipo_Vinculo = st.selectbox("Tipo de Vinculo", ["CLT","Pessoa Jurídica","Temporário", "Estagiário","Autonomo"],placeholder="Selecione o tipo de vinculo",index=None)
                Admissao = st.date_input("Data de Admissão",value="today",format="DD/MM/YYYY")
            
            st.divider()

            st.subheader("Produtividade")
            col5, col6 = st.columns(2)

            with col5:
                Carga_horaria = st.number_input("Carga Horária Semanal",value=None,min_value=0,max_value=48,step=1,icon=":material/calendar_clock:")
                produtividade = st.slider("Produtividade", min_value=0, max_value=100, value=80, step=1, format="%d%%")
            with col6:
                cadastro = st.text_input("Data de Cadastro", value=data_hora_atual, disabled=True)   
                situacao = st.selectbox("Situação", ["Ativo", "Inativo"],disabled=True)

            submitted = st.form_submit_button("Cadastrar Colaborador")

            if submitted:
                erros = []
                if not nome:
                    erros.append("Nome Completo")
                if not CPF:
                    erros.append("CPF")

                if not RG:
                    erros.append("RG")

                if not Nascimento:
                    erros.append("Nascimento")
                
                if not Sexo:
                    erros.append("Sexo")

                if not estado_civil:
                    erros.append("Estado Civil")

                if not nacionalidade:
                    erros.append("Nacionalidade")
                
                if not area:
                    erros.append("Area")

                if not cargo:
                    erros.append("Cargo")

                if not Tipo_Vinculo:
                    erros.append("Tipo de Vinculo")

                if not Admissao:
                    erros.append("Data de Admissão")

                if not Carga_horaria:
                    erros.append("Carga Horária Semanal")

                if not produtividade:
                    erros.append("Produtividade")

                if erros:
                    st.error(f"**Os seguintes campos são obrigatórios**: {', '.join(erros)}.")
                else:
                    st.success(f"Colaborador '{nome}' cadastrado com sucesso!")

    # ==========================================
    # TABELA DE CLIENTES (simulada para exemplo)
    # ==========================================
    def lista_clientes():
        st.subheader("Equipes Cadastradas")
        st.write("Tabela com os equipes cadastradas no sistema.")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.selectbox("Código:", [1,2,3,4,5,6,7,8,9,10],placeholder="Pesquisar por Código",index=None)
        with col2:
            st.selectbox("Nome:", ["João da Silva", "José Ferreira", "Maria Silva"],placeholder="Pesquisar por Nome",index=None)
        with col3:
            st.selectbox("Área:", ["TI", "RH", "Comercial"],placeholder="Pesquisar por Área",index=None)
        with col4:
            st.selectbox("Cargo:", ["Desenvolvedor", "Analista", "Gerente"],placeholder="Pesquisar por Cargo",index=None)
        with col5:
            st.selectbox("Tipo de vinculo:", ["Pessoa Física", "Pessoa Jurídica"],placeholder="Pesquisar por Tipo de Vinculo",index=None)
        with col6:
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
            "Situação": ["Ativo", "Inativo", "Ativo"]
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
                "Situação": st.column_config.SelectboxColumn(options=["Ativo", "Inativo"])
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

    tabs = st.tabs(["Cadastro", "Listagem de Equipes"])

    with tabs[0]:
        cadastro()
    with tabs[1]:
        lista_clientes()