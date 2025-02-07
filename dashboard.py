import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import random
import time
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.title("📊 API Dashboard")

# 📌 Buscar todos os itens da API
response = requests.get(f"{API_URL}/items")

if response.status_code == 200:
    items = response.json()
    df = pd.DataFrame(items)

    # Converter datas
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"])

    # 📌 Tabela interativa
    st.subheader("📋 Itens Cadastrados")
    st.dataframe(df)

    # 📌 1️⃣ Gráfico de dispersão (Nome x Descrição x Popularidade)
    fig1 = px.scatter(df, 
                      x=df["name"].apply(len), 
                      y=df["description"].apply(len), 
                      size=df["price"], 
                      color=df["stock"].astype(str),
                      hover_data=["name", "description", "price", "stock"],
                      title="Nome vs Descrição vs Estoque")
    st.plotly_chart(fig1)

    # 📌 2️⃣ Gráfico de linhas (Evolução de cadastros)
    df_sorted = df.sort_values("created_at")
    fig2 = px.line(df_sorted, 
                   x="created_at", 
                   y="stock", 
                   title="Evolução do Estoque ao Longo do Tempo")
    st.plotly_chart(fig2)

    # 📌 3️⃣ Pesquisar e Excluir um item
    st.subheader("🔎 Buscar e Excluir Item")
    search_term = st.text_input("Digite o nome do item para buscar:")
    if search_term:
        filtered_df = df[df["name"].str.contains(search_term, case=False)]
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

else:
    st.error("Erro ao buscar os itens!")

# 📌 4️⃣ Formulário para adicionar item
with st.form("adicionar_item"):
    st.subheader("➕ Adicionar Novo Item")

    name = st.text_input("Nome do Item")
    description = st.text_area("Descrição")
    category = st.text_input("Categoria")
    price = st.number_input("Preço", min_value=0.01, format="%.2f")
    stock = st.number_input("Quantidade em Estoque", min_value=0, step=1)

    submit = st.form_submit_button("Adicionar")

    if submit:
        if not name.strip() or not description.strip() or not category.strip():
            st.error("Todos os campos são obrigatórios!")
        else:
            new_item = {
                # "id": int(time.time()),  # ID baseado no timestamp
                "name": name,
                "description": description,
                "category": category,
                "price": price,
                "stock": stock,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            res = requests.post(f"{API_URL}/items", json=new_item)
            if res.status_code == 200:
                st.success("Item adicionado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao adicionar o item.")

# 📌 5️⃣ Botão para saída de estoque
st.subheader("📦 Saída de Estoque")
saida_id = st.number_input("ID do item para saída", step=1, min_value=0)
saida_qtd = st.number_input("Quantidade a remover", step=1, min_value=1)

if st.button("Remover do Estoque"):
    res = requests.patch(f"{API_URL}/items/{saida_id}/reduce_stock", json={"quantity": saida_qtd})
    if res.status_code == 200:
        st.success("Estoque atualizado!")
        st.rerun()
    else:
        st.error("Erro ao atualizar estoque.")
