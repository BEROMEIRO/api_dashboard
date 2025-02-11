import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="API Dashboard", layout="wide")
st.title("📊 API Dashboard")

# 📌 1️⃣ Buscar todos os itens da API
response = requests.get(f"{API_URL}/items")
df = pd.DataFrame()

if response.status_code == 200:
    items = response.json()
    if items:
        df = pd.DataFrame(items)

    required_columns = {"created_at", "category", "name", "price", "id"}
    if not required_columns.issubset(df.columns):
        st.error("⚠ Erro: Colunas necessárias ausentes no DataFrame.")
    else:
        df["created_at"] = pd.to_datetime(df["created_at"], errors='coerce')

        # 📌 Sidebar para Filtros
        st.sidebar.header("🔍 Filtros")
        categorias = st.sidebar.multiselect("Filtrar por Categoria", df["category"].unique())
        if categorias:
            df = df[df["category"].isin(categorias)]

        # 📌 Expander para Itens
        st.subheader("📋 Itens Cadastrados")
        with st.expander("Clique para ver os itens"):
            st.dataframe(df)

        # 📌 2️⃣ Gráficos de Análise
        if "category" in df.columns and "price" in df.columns:
            category_counts = df['category'].value_counts().reset_index()
            category_counts.columns = ['category', 'item_count']

            fig_category = px.bar(
                category_counts, 
                x="item_count", 
                y="category", 
                orientation="h",
                title="📊 Análise por Categoria", 
                labels={'category': 'Categoria', 'item_count': 'Número de Itens'},
                color_discrete_sequence=["#0083B8"] * len(category_counts), 
                template="plotly_white"
            )

            fig_category.update_layout(height=300)
            fig_category.update_layout(width=200)

            fig_pie = px.pie(
                category_counts, 
                values="item_count", 
                names="category", 
                title="📊 Distribuição por Categoria"
            )

            fig_pie.update_layout(height=300)
            fig_pie.update_layout(width=200)

            left, right = st.columns(2)
            left.plotly_chart(fig_category, use_container_width=True)
            right.plotly_chart(fig_pie, use_container_width=True)

        # 📌 3️⃣ Buscar e Excluir um item - Como Expander
        with st.expander("🔎 Buscar e Excluir Item"):
            search_term = st.text_input("Digite o nome do item para buscar:")
            if search_term:
                filtered_df = df[df["name"].str.contains(search_term, case=False, na=False)]
                st.dataframe(filtered_df)

                if not filtered_df.empty:
                    delete_id = st.selectbox("Selecione o ID do item para excluir:", filtered_df["id"])
                    if st.button("❌ Excluir Item"):
                        res = requests.delete(f"{API_URL}/items/{delete_id}")
                        if res.status_code == 200:
                            st.success("Item excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao excluir item.")

# 📌 4️⃣ Adicionar Novo Item - Como Expander
with st.expander("➕ Adicionar Novo Item"):
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "description" not in st.session_state:
        st.session_state.description = ""
    if "category" not in st.session_state:
        st.session_state.category = ""
    if "price" not in st.session_state:
        st.session_state.price = 0.01

    with st.form("adicionar_item"):
        # Campos do formulário
        name = st.text_input("Nome do Item", value=st.session_state.name, key="name")
        description = st.text_area("Descrição", value=st.session_state.description, key="description")
        category = st.text_input("Categoria", value=st.session_state.category, key="category")
        price = st.number_input("Preço", min_value=0.01, format="%.2f", value=st.session_state.price, key="price")
        
        submit = st.form_submit_button("Adicionar")

        if submit:
            if not name.strip() or not description.strip() or not category.strip():
                st.error("Todos os campos são obrigatórios!")
            else:
                new_item = {
                    "name": name,
                    "description": description,
                    "category": category,
                    "price": price,
                }
                res = requests.post(f"{API_URL}/items", json=new_item)
                if res.status_code == 200:
                    st.success("Item adicionado com sucesso!")
                    del st.session_state["name"]
                    del st.session_state["description"]
                    del st.session_state["category"]
                    del st.session_state["price"]
                    st.rerun()
                else:
                    st.error("Erro ao adicionar o item.")

# 📌 5️⃣ Saída de Estoque - Como Expander
with st.expander("📦 Saída de Estoque"):
    saida_id = st.number_input("ID do item para saída", step=1, min_value=0)
    saida_qtd = st.number_input("Quantidade a remover", step=1, min_value=1)
    if st.button("Remover do Estoque"):
        res = requests.patch(f"{API_URL}/items/{saida_id}/reduce_stock", json={"quantity": saida_qtd})
        if res.status_code == 200:
            st.success("Estoque atualizado!")
            st.rerun()
        else:
            st.error("Erro ao atualizar estoque.")
