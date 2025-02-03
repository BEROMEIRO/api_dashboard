import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📊 API Dashboard")

# Listar os itens
st.subheader("Itens Cadastrados")
response = requests.get(f"{API_URL}/items")

if response.status_code == 200:
    items = response.json()
    for item in items:
        st.write(f"**ID**: {item['id']} | **Nome**: {item['name']} | **Descrição**: {item['description']}")
else:
    st.error("Erro ao buscar os itens!")

# Formulário para adicionar item
st.subheader("Adicionar Novo Item")
name = st.text_input("Nome do Item")
description = st.text_area("Descrição")

if st.button("Adicionar"):
    new_item = {"name": name, "description": description}
    res = requests.post(f"{API_URL}/items", json=new_item)
    if res.status_code == 200:
        st.success("Item adicionado com sucesso!")
        st.rerun()
    else:
        st.error("Erro ao adicionar o item.")
