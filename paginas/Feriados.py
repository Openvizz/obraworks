import streamlit as st
import pandas as pd
from datetime import date,datetime
import uuid
import time

def feriados():
    st.title("📅 Feriados")
    st.write("Cadastre feriados abaixo. A lista será exibida e você poderá remover posteriormente.")

    tabs = st.tabs(["📋 Feriados", "🗑️ Remover Feriados"])

    with tabs[0]:
        st.subheader("📖 Cadastro")

        # Inicializa a tabela de feriados com ID único para cada linha
        if "feriados_df" not in st.session_state:
            st.session_state.feriados_df = pd.DataFrame(columns=["id", "Data", "Nome do Feriado", "Tipo do Feriado"])

        # --- FORMULÁRIO DE CADASTRO ---
        with st.form("form_feriado"):
            col1, col2, col3 = st.columns(3)

            with col1:
                data_feriado = st.date_input("Data", value=date.today(),format="DD/MM/YYYY")
            with col2:
                nome_feriado = st.text_input("Nome do Feriado", placeholder="Ex: Natal")
            with col3:
                tipo_feriado = st.selectbox("Tipo do Feriado", ["Nacional", "Estadual", "Municipal"])

            submitted = st.form_submit_button("Adicionar Feriado")

            if submitted:
                if data_feriado in st.session_state.feriados_df["Data"].values:
                    st.warning("⚠️ Já existe um feriado cadastrado nessa data.")
                elif not nome_feriado.strip():
                    st.warning("⚠️ O nome do feriado não pode estar vazio.")

                else:
                    novo = {
                        "id": str(uuid.uuid4()),  # ID único oculto
                        "Data": data_feriado,
                        "Nome do Feriado": nome_feriado.strip(),
                        "Tipo do Feriado": tipo_feriado
                    }
                    st.session_state.feriados_df = pd.concat([st.session_state.feriados_df, pd.DataFrame([novo])], ignore_index=True)
                    st.success("✅ Feriado adicionado com sucesso!")

        # --- FILTROS E EXIBIÇÃO DE DADOS ---
        df_full = st.session_state.feriados_df.copy()

        if not df_full.empty:
            st.subheader("🗓️ Feriados Cadastrados")

            # 🔍 Filtros
            col4, col5 , col6 = st.columns([5, 1, 0.6])
            with col4:
                filtro_nome = st.text_input("🔎 Pesquisar por Nome do Feriado",icon=":material/manage_search:",placeholder="Natal")
            with col5:
                filtro_tipo = st.selectbox(
                    "Filtrar por Tipo",
                    options=["Todos", "Nacional", "Estadual", "Municipal"],
                    index=0
                )

            with col6:
                # Aplicar filtros ANTES da paginação
                if filtro_nome:
                    df_full = df_full[df_full["Nome do Feriado"].str.contains(filtro_nome, case=False, na=False)]
                if filtro_tipo != "Todos":
                    df_full = df_full[df_full["Tipo do Feriado"] == filtro_tipo]

                # Garantir tipo da coluna Data
                df_full["Data"] = pd.to_datetime(df_full["Data"], errors="coerce").dt.date
                df_full = df_full.sort_values(by="Data", ascending=False)

                # Paginação
                registros_por_pagina = 20
                total_registros = len(df_full)
                total_paginas = max(1, (total_registros - 1) // registros_por_pagina + 1)

                pagina = st.number_input(
                    "Página", min_value=1, max_value=total_paginas,
                    step=1, value=1, format="%d"
                )

                inicio = (pagina - 1) * registros_por_pagina
                fim = inicio + registros_por_pagina
                df_pagina = df_full.iloc[inicio:fim].copy()

            # 🔍 Tabela sem a coluna ID
            df_visual = df_pagina.drop(columns=["id"]) if "id" in df_pagina.columns else df_pagina
            df_visual["Data"] = pd.to_datetime(df_visual["Data"], errors="coerce").dt.strftime('%d/%m/%Y')
            st.dataframe(df_visual, use_container_width=True, hide_index=False)

            col7, col8 , col9 = st.columns([1, 8, 1])
            with col7:
                st.badge(f"Página {pagina} de {total_paginas}",icon=":material/sort:")
            with col8:
                None
            
            with col9:
                st.badge(f"Total de feriados: {total_registros}", icon=":material/done_all:", color="green")

    with tabs[1]:
        # 🗑️ Botões de Remoção por Data
        if not st.session_state.feriados_df.empty:
            st.subheader("🗑️ Remover Feriado por Data")

            col6 = st.columns([1,6])[0]
            with col6:
                # Garantir que a coluna "Data" está no formato correto
                df_remocao = st.session_state.feriados_df.copy()
                df_remocao["Data"] = pd.to_datetime(df_remocao["Data"], errors="coerce")

                # Mapeia datas formatadas para valores reais
                datas_para_exibir = df_remocao["Data"].dt.strftime('%d/%m/%Y')
                datas_reais = df_remocao["Data"].dt.date

                # Dicionário: "20/05/2025" → datetime.date(2025, 5, 20)
                mapa_datas = dict(zip(datas_para_exibir, datas_reais))

                # Selectbox com datas no padrão BR
                data_formatada = st.selectbox("Selecione a Data que deseja remover", list(mapa_datas.keys()))
                data_a_remover = mapa_datas[data_formatada]

            
            if st.button("Remover Feriado"):
                antes = len(st.session_state.feriados_df)
                st.session_state.feriados_df = st.session_state.feriados_df[
                    pd.to_datetime(st.session_state.feriados_df["Data"]).dt.date != data_a_remover
                ]
                depois = len(st.session_state.feriados_df)

                if antes != depois:
                    st.success(f"ℹ️ Feriado removido com sucesso.")
                    time.sleep(3)
                    st.rerun()
                else:
                    st.info("ℹ️ Nenhum feriado foi removido.")

        else:
            st.warning("⚠️ Nenhum feriado cadastrado.")