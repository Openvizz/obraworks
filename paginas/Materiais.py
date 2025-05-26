import streamlit as st
from datetime import datetime
import locale
import json
import os
import pandas as pd
import time
import uuid

# Define locale brasileiro para moeda com fallback
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    except locale.Error:
        # Fallback para locale padrão
        locale.setlocale(locale.LC_ALL, '')

# Caminho do JSON de unidades
UNIDADES_PATH = r"utils/un.json"

# Carrega unidades do JSON
def carregar_unidades(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error("Arquivo de unidades não encontrado.")
        return {}

# Formata moeda para R$
def format_brl(value):
    try:
        return locale.currency(float(value), grouping=True)
    except:
        return "Valor inválido"

def materiais():
    if "materiais_df" not in st.session_state:
        st.session_state.materiais_df = pd.DataFrame(columns=[
            "id", "Código", "Descrição", "Unidade", "Preço Unitário",
            "Coeficiente (%)", "Data de Cadastro", "Status"
        ])

    if "material_id" not in st.session_state:
        if not st.session_state.materiais_df.empty:
            st.session_state.material_id = int(st.session_state.materiais_df["Código"].max()) + 1
        else:
            st.session_state.material_id = 1
    st.title("📦 Materiais")
    st.write("Gerencie materiais cadastrados. Use as abas para cadastrar ou remover.")

    unidades_dict = carregar_unidades(UNIDADES_PATH)
    if not unidades_dict:
        return

    # Inicializa DataFrame de materiais
    if "materiais_df" not in st.session_state:
        st.session_state.materiais_df = pd.DataFrame(columns=[
            "id", "Código", "Descrição", "Unidade", "Preço Unitário", "Coeficiente (%)", "Data de Cadastro"
        ])

    tabs = st.tabs(["📊 Dashboard","📋 Cadastro de Materiais", "🗑️ Remover/Editar Materiais"])

    with tabs[0]:
        st.write("")

        # Contagem de materiais ativos e inativos
        total_materiais = st.session_state.materiais_df.shape[0]
        materiais_ativos = st.session_state.materiais_df[st.session_state.materiais_df["Status"] == "Ativo"].shape[0]
        materiais_inativos = st.session_state.materiais_df[st.session_state.materiais_df["Status"] == "Inativo"].shape[0]

        col_Chart1, col_Chart2, col_Chart3 = st.columns(3)
        
        with col_Chart1:
            st.metric("Total de Materiais", total_materiais)
        
        with col_Chart2:
            st.metric("Materiais Ativos", materiais_ativos)
        
        with col_Chart3:
            st.metric("Materiais Inativos", materiais_inativos)

        # Gráfico da Quantidade de itens Cadatrados por unidade
        st.subheader("Quantidade de itens cadastrados por unidade")
        st.bar_chart(st.session_state.materiais_df.groupby("Unidade").count()["Código"])

        # Download de arquivo CSV
        csv = st.session_state.materiais_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="materiais.csv",
            mime="text/csv"
        )


    # 📋 Aba de Cadastro
    with tabs[1]:
        with st.form("form_material"):
            st.subheader("📋 Cadastro de Materiais")
            col1, col2, col3, col4, col5, col6 = st.columns([0.8, 4, 1, 1, 1, 1])

            with col1:
                cod_itens = st.text_input("Código", value=str(st.session_state.material_id), disabled=True)
            with col2:
                descricao = st.text_input("Descrição", placeholder="Ex: Areia fina")
            with col3:
                unidade = st.selectbox("Unidade", options=list(unidades_dict.keys()))
            with col4:
                preco_unitario = st.number_input("Preço Unitário (R$)", min_value=0.00, step=0.01, format="%.2f")
            with col5:
                coeficiente_percentual = st.number_input("Coeficiente (%)", min_value=0.0, max_value=100.0, step=0.1)
                coeficiente_decimal = coeficiente_percentual / 100
            with col6:
                data_cadastro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                st.text_input("Data e Hora do Cadastro", value=data_cadastro, disabled=True)

            submitted = st.form_submit_button("Cadastrar Material")
            
            if submitted:
                erros = []

                if not descricao.strip():
                    erros.append("A descrição não pode estar vazia.")
                if preco_unitario == 0.0:
                    erros.append("O preço unitário deve ser maior que zero.")
                if coeficiente_percentual == 0.0:
                    erros.append("O coeficiente deve ser maior que zero.")

                if erros:
                    for erro in erros:
                        st.warning(f"⚠️ {erro}")
                else:
                    novo_material = {
                        "id": str(uuid.uuid4()),
                        "Código": st.session_state.material_id,
                        "Descrição": descricao.strip(),
                        "Unidade": f"{unidade}",
                        "Preço Unitário": preco_unitario,
                        "Coeficiente (%)": coeficiente_percentual,
                        "Data de Cadastro": data_cadastro,
                        "Status": "Ativo"
                    }
                    st.session_state.materiais_df = pd.concat(
                        [st.session_state.materiais_df, pd.DataFrame([novo_material])],
                        ignore_index=True
                    )
                    st.success(f"✅ Material cadastrado com sucesso!")
                    st.session_state.material_id += 1
                    time.sleep(1)                    
                    st.rerun()


        # 🔍 Exibir Tabela com Filtros
        df = st.session_state.materiais_df.copy()

        if not df.empty:
            st.subheader("📦 Materiais Cadastrados")
            col_f1, col_f2, col_f3 = st.columns([5, 1,0.6])

            with col_f1:
                filtro_desc = st.text_input("🔍 Filtrar por Descrição")
            with col_f2:
                filtro_unidade = st.selectbox(
                    "Filtrar por Unidade",
                    options=["Todos"] + sorted(df["Unidade"].unique().tolist())
                )

            if filtro_desc:
                df = df[df["Descrição"].str.contains(filtro_desc, case=False, na=False)]
            if filtro_unidade != "Todos":
                df = df[df["Unidade"] == filtro_unidade]

            with col_f3:
                # Remove ID da visualização
                df_visual = df.drop(columns=["id"])

                # Paginação
                registros_por_pagina = 20
                total_registros = len(df_visual)
                total_paginas = max(1, (total_registros - 1) // registros_por_pagina + 1)

                pagina = st.number_input(
                    "Página", min_value=1, max_value=total_paginas,
                    step=1, value=1, format="%d"
                )

                inicio = (pagina - 1) * registros_por_pagina
                fim = inicio + registros_por_pagina
                df_pagina = df_visual.iloc[inicio:fim].copy()
            
            st.dataframe(df_pagina, use_container_width=True, hide_index=True)

            col7, col8, col9 = st.columns([1, 8, 1])
            with col7:
                st.badge(f"Página {pagina} de {total_paginas}", icon=":material/sort:")
            with col9:
                st.badge(f"Total de materiais: {total_registros}", icon=":material/done_all:", color="green")


    # 🗑️ Aba de Remoção
    with tabs[2]:
        st.subheader("🗑️ Remover Materiais por Código")

        df_remover = st.session_state.materiais_df.copy()
        if not df_remover.empty:
            df_remover["Código + Nome"] = df_remover["Código"].astype(str) + " — " + df_remover["Descrição"]

            codigo_nome = st.selectbox(
                "Selecione o Código do Material",
                options=df_remover["Código + Nome"].tolist()
            )
            cod_selecionado = int(codigo_nome.split(" — ")[0])

            if st.button("Remover Material"):
                antes = len(st.session_state.materiais_df)
                st.session_state.materiais_df = df_remover[df_remover["Código"] != cod_selecionado]
                depois = len(st.session_state.materiais_df)

                if antes != depois:
                    st.success("✅ Material removido com sucesso!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.info("ℹ️ Nenhum material foi removido.")
        else:
            st.warning("⚠️ Nenhum material cadastrado ainda.")

        # 🔧 Divider visual
        st.divider()

        # Edição de Material
        st.subheader("✏️ Editar Material Existente")

        df_edicao = st.session_state.materiais_df.copy()

        col_busca1, col_busca2 = st.columns([1, 10])
        with col_busca1:
            codigo_edit = st.number_input("Buscar por Código", min_value=0, step=1, format="%d")
        with col_busca2:
            nome_edit = st.selectbox("Ou buscar por nome", options=["Todos"] + sorted(df_edicao["Descrição"].unique().tolist()))
            #nome_edit = st.text_input("Ou buscar por nome", placeholder="Ex: Areia fina")

        if codigo_edit != 0:
            material = df_edicao[df_edicao["Código"] == codigo_edit]
        elif nome_edit:
            material = df_edicao[df_edicao["Descrição"].str.contains(nome_edit, case=False, na=False)]
        else:
            material = pd.DataFrame()

        if not material.empty:
            dados = material.iloc[0]  # Assume que só um material será retornado
            st.info(f"Material encontrado: **{dados['Descrição']}**")

            with st.form("editar_material"):
                col1, col2, col3 , col4, col5, col6 = st.columns([1.5, 10, 2,2,2,2])
                with col1:
                    cod_itens = st.text_input("Código", value=dados["Código"], disabled=True)
                with col2:
                    nova_descricao = st.text_input("Descrição", value=dados["Descrição"])
                with col3:
                    nova_unidade = st.text_input("Unidade", value=dados["Unidade"])
                with col4:
                    novo_status = st.selectbox("Status", ["Ativo", "Inativo"], index=0 if dados["Status"] == "Ativo" else 1)                
                with col5:
                    novo_preco = st.number_input("Preço Unitário (R$)", value=float(dados["Preço Unitário"]), step=0.01)
                with col6:
                    novo_coef = st.number_input("Coeficiente (%)", value=float(dados["Coeficiente (%)"]), min_value=0.0, max_value=100.0, step=0.1)

                salvar = st.form_submit_button("Salvar Alterações")

                if salvar:
                    idx = st.session_state.materiais_df.index[st.session_state.materiais_df["Código"] == dados["Código"]].tolist()[0]
                    st.session_state.materiais_df.at[idx, "Descrição"] = nova_descricao
                    st.session_state.materiais_df.at[idx, "Unidade"] = nova_unidade
                    st.session_state.materiais_df.at[idx, "Status"] = novo_status
                    st.session_state.materiais_df.at[idx, "Preço Unitário"] = novo_preco
                    st.session_state.materiais_df.at[idx, "Coeficiente (%)"] = novo_coef
                    st.success("✅ Alterações salvas com sucesso!")
                    time.sleep(2)
                    st.rerun()
        else:
            st.caption("🔍 Digite o código ou parte do nome do material para editar.")