from datetime import datetime
import streamlit as st
import pandas as pd

caminho_datasets = "datasets"

df_compras = pd.read_csv(f"{caminho_datasets}/compras.csv", sep=";", decimal=",", index_col=0)
df_lojas = pd.read_csv(f"{caminho_datasets}/lojas.csv", sep=";", decimal=",")
df_produtos = pd.read_csv(f"{caminho_datasets}/produtos.csv", sep=";", decimal=",")

df_lojas["cidade/estado"] = df_lojas["cidade"] + " / " + df_lojas["estado"]
lista_lojas = df_lojas["cidade/estado"].to_list()
loja_selecionada = st.sidebar.selectbox("Selecione a loja:", lista_lojas)

lista_vendedores_df = df_lojas.loc[df_lojas["cidade/estado"] == loja_selecionada, "vendedores"].iloc[0]
lista_vendedores = lista_vendedores_df.strip("[]").replace("'", "").split(", ")
vendedor_selecionado = st.sidebar.selectbox("Selecione o vendedor:", lista_vendedores)

lista_produtos = df_produtos["nome"].to_list()
produto_selecionado = st.sidebar.selectbox("Selecione o produto:", lista_produtos)

nome_cliente = st.sidebar.text_input("Nome do Cliente")
genero_selecionado = st.sidebar.selectbox("Gênero do Cliente:", ["masculino", "feminino"])

forma_pagto_selecionado = st.sidebar.selectbox("Forma de Pagamento:", ["cartão de crédito", "boleto", "pix", "dinheiro"])

if st.sidebar.button("Adicionar Nova Compra"):
    nova_id_compra = df_compras["id_compra"].max() + 1 if not df_compras.empty else 1
    lista_adicionar = [
        nova_id_compra,
        loja_selecionada,
        vendedor_selecionado,
        produto_selecionado,
        nome_cliente,
        genero_selecionado,
        forma_pagto_selecionado
    ]
    nova_compra = pd.DataFrame([lista_adicionar], columns=["id_compra", "loja", "vendedor", "produto", "cliente_nome", "cliente_genero", "forma_pagamento"])
    df_compras = pd.concat([df_compras, nova_compra], ignore_index=True)
    df_compras.to_csv(f"{caminho_datasets}/compras.csv", index=False, decimal=",", sep=";")
    st.success("Compra adicionada")

st.dataframe(df_compras)