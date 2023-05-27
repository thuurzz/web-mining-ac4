import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np


def run():
    # Criando dataframe a partir do banco de dados que foi criado com o script de extração
    df = pd.read_sql_table('jogos_nuuvem', 'sqlite:///./3_scripts/nuuvem.db')
    df['porcentagem_desconto'] = df['porcentagem_desconto'].astype('int')
    df["preco_original"] = df["preco"] / (1 - (df["porcentagem_desconto"]/100))
    df["preco_original"] = round(df["preco_original"], 2)
    # -------------------------------------------------------

    # Título da página
    col1, col2, col3 = st.columns(3)
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <h1>Extração - Loja Nuuvem</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    with col2:
        image = Image.open('assets/nuuvem.png')
        st.image(image, caption='Logo Loja Nuuvem')

        st.divider()
    # -------------------------------------------------------

    # Filtra jogos pelo nome
    st.subheader('Encontre o jogo pelo nome')
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    text_input = st.text_input(
        "Nome do jogo buscado 👇",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder="Digite o nome do jogo",
    )

    if text_input:
        df_filtrado = df[df["nome"].str.contains(text_input, case=False)]
        df_filtrado = df_filtrado.rename(columns={
            "nome": "Nome do Jogo",
            "porcentagem_desconto": "Desconto (%)",
            "preco": "Preço (R$)",
            "tipo": "Tipo de Jogo",
            "preco_original": "Preço original(R$)"
        })
        st.dataframe(df_filtrado[["Nome do Jogo", "Preço original(R$)",
                     "Preço (R$)", "Desconto (%)"]], use_container_width=True)
        if len(df_filtrado) == 0:
            st.info('Jogo não encontrado!', icon="ℹ️")
    st.divider()
    # -------------------------------------------------------

    # Filtro para listar jogos pelo preço
    st.subheader('Encontre os jogos pela faixa de preço')
    max = int(df['preco'].max()) + 1
    valor_jogo_min = st.slider('Mínimo BRL$', 0, max, 5)
    valor_jogo_max = st.slider('Máximo BRL$', 0, max, 100)
    if valor_jogo_min > valor_jogo_max:
        st.error('O valor mínimo, não pode ser maior que o máximo.', icon="🚨")
        valores_filtrados_preco = df.loc[df['preco'].between(
            valor_jogo_min, valor_jogo_max)].sort_values(by=['porcentagem_desconto'], ascending=False)
        valores_filtrados_preco = valores_filtrados_preco.rename(columns={
            "nome": "Nome do Jogo",
            "porcentagem_desconto": "Desconto (%)",
            "preco": "Preço (R$)",
            "tipo": "Tipo de Jogo",
            "preco_original": "Preço original(R$)"
        })
        st.dataframe(valores_filtrados_preco[[
            "Nome do Jogo", "Preço original(R$)", "Preço (R$)", "Desconto (%)"]], use_container_width=True)
        st.caption(f'Quantidade de itens: {len(valores_filtrados_preco)}')
        st.divider()
    # -------------------------------------------------------

    # Gráfico com line chart do preço dos jogos
    st.subheader('Variação do preço dos jogos')
    st.line_chart(df.preco)
    st.caption(f'Quantidade de itens: {len(df)}')
    jogo_mais_caro = df['preco'].max()
    jogo_mais_barato = df['preco'].min()
    media_precos = df['preco'].mean()
    std_precos = df['preco'].std()
    df['outlier'] = np.abs(df['preco'] - media_precos) > 3 * std_precos
    qtd_outliers = df['outlier'].sum()
    st.markdown(
        f"""
        <span>Jogo mais caro: {jogo_mais_caro} (BRL)</span> </br>
        <span>Jogo mais barato: {jogo_mais_barato} (BRL)</span> </br>
        <span>Média do preço dos jogos: {media_precos:.2f} (BRL)</span> </br>
        <span>Quantidade de outliers no preço dos jogos: {qtd_outliers}</span>
        """,
        unsafe_allow_html=True
    )
    st.divider()
    # -------------------------------------------------------

    # Distribuição dos jogos por quantidade de desconto
    st.subheader("Didstribuição de jogos por quantidade de desconto")

    jogos_pre_venda_com_desconto = df[(df['tipo'] == 'prevenda') & (
        df['porcentagem_desconto'] > 0)]
    tipo_selecionado = st.selectbox('Selecione um tipo', options=[
                                    'todos', 'padrao', 'pacote', 'prevenda'])
    if tipo_selecionado == 'todos':
        df_filtrado = df
    else:
        df_filtrado = df.loc[df['tipo'] == tipo_selecionado]
    jogos_prevenda_com_desconto = df_filtrado.loc[df_filtrado['porcentagem_desconto'] > 0,]
    quantidade_jogos_pre_venda_com_desconto = len(jogos_prevenda_com_desconto)
    st.write(
        f"Existem {quantidade_jogos_pre_venda_com_desconto} jogos do tipo: {tipo_selecionado}, com desconto.")
    jogos_prevenda_com_desconto = jogos_prevenda_com_desconto.rename(columns={
        "nome": "Nome do Jogo",
        "porcentagem_desconto": "Desconto (%)",
        "preco": "Preço (R$)",
        "tipo": "Tipo de Jogo",
        "preco_original": "Preço original(R$)"
    })
    st.dataframe(jogos_prevenda_com_desconto[[
                 "Nome do Jogo", "Preço original(R$)", "Preço (R$)", "Desconto (%)", "outlier"]], use_container_width=True)
    st.subheader("Distribuição Preço por Desconto")

    # Plotly Chart
    fig_sc = px.scatter(
        df,
        x="porcentagem_desconto",
        y="preco",
        color="tipo",
        color_continuous_scale="reds",
    )
    st.plotly_chart(fig_sc, use_container_width=True)
    st.caption(f'Quantidade de itens: {len(df)}')
    st.divider()
    # -------------------------------------------------------

    # TOP 10 Jogos com maior desconto
    st.subheader('TOP 10 Jogos com maior desconto')
    jogos_mais_85_desconto = df.sort_values(
        by=['porcentagem_desconto'], ascending=False).head(10)
    jogos_mais_85_desconto = jogos_mais_85_desconto.rename(columns={
        "nome": "Nome do Jogo",
        "porcentagem_desconto": "Desconto (%)",
        "preco": "Preço (R$)",
        "tipo": "Tipo de Jogo",
        "preco_original": "Preço original(R$)"
    })
    fig_bar = px.bar(jogos_mais_85_desconto, x="Nome do Jogo", y="Preço (R$)", hover_data=[
                     'Preço (R$)', 'Preço original(R$)'], color='Desconto (%)',)
    idx = df['porcentagem_desconto'].idxmax()
    jogo_maior_desconto = df.loc[idx, 'nome']
    quantidade_desconto = df.loc[idx, 'porcentagem_desconto']
    st.markdown(
        f"""
        <span>O jogo com o maior desconto é: "{jogo_maior_desconto}", com um desconto de {quantidade_desconto}%.</span>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption(f'Quantidade de itens: {len(jogos_mais_85_desconto)}')
    st.divider()
    # -------------------------------------------------------

    # plotly
    # Agrupamento de jogos por quantidade de desconto
    # --------------------------------------------------
    st.subheader('Agrupamento de jogos por quantidade de desconto')
    categorias = pd.cut(df['porcentagem_desconto'],
                        bins=[-0.1, 5, 30, 50, 75, 100],
                        labels=['0-5%', '6-30%', '31-50%', '51-75%', '76-100%'])
    df['categoria_desconto'] = categorias
    contagem_categorias = df['categoria_desconto'].value_counts()
    categoria_mais_jogos = contagem_categorias.idxmax()
    st.markdown(
        f"""
        <span>A categoria com a maior quantidade de jogos em desconto é: {categoria_mais_jogos}</span>
        """,
        unsafe_allow_html=True
    )
    porcentagem_desconto = st.selectbox('Selecione a porcentagem de desconto:',
                                        ['0-5%', '6-30%', '31-50%', '51-75%', '76-100%'])
    df_filtrado = df[df['categoria_desconto'] == porcentagem_desconto]
    quantidade_jogos = len(df_filtrado)
    st.markdown(
        f"""
        <span>A quantidade de jogos com {porcentagem_desconto} de desconto é: {quantidade_jogos}</span>
        """,
        unsafe_allow_html=True
    )
    fig = px.pie(df, values="preco", names="categoria_desconto",
                 title='Quantidade de desconto')
    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------

    # Box Plot preço e outlier de valores
    # --------------------------------------------------
    st.subheader('Box Plot Preço (R$)')
    categorias = pd.cut(df['porcentagem_desconto'],
                        bins=[-0.1, 15, 30, 45, 60, 75, 90, 100],
                        labels=['0-15%', '16-30%', '31-45%', '46-60%', '61-75%', '76-90%', '91-100%'])
    df['categoria_desconto'] = categorias
    categoria_selecionada = st.selectbox("Selecione a categoria de desconto:", [
                                         '0-15%', '16-30%', '31-45%', '46-60%', '61-75%', '76-90%', '91-100%'])
    dados_filtrados = df[df['categoria_desconto'] == categoria_selecionada]
    contagem_categorias = dados_filtrados['categoria_desconto'].value_counts()
    filtro = df['categoria_desconto'] == categoria_selecionada
    df_filtrado = df[filtro]
    nome_mais_caro = df_filtrado.loc[df_filtrado['preco'].idxmax(), 'nome']
    jogo_mais_caro = df_filtrado.loc[df_filtrado['preco'].idxmax(), 'preco']
    st.markdown(
        f"""
    <span>O jogo mais caro, está custando: R$ {jogo_mais_caro}</span>
    </br>
    <span>O nome do jogo mais caro é: {nome_mais_caro}</span>
    """,
        unsafe_allow_html=True
    )
    fig = px.box(dados_filtrados, x='categoria_desconto', y='preco',
                 color='tipo', title='Distribuição de preços por categoria de desconto')
    st.plotly_chart(fig)
    # --------------------------------------------------
    st.markdown(
        """
        <h4 style='text-align: center;'>
            Designed by
            </br>
            <a href="https://github.com/thuurzz" style='text-decoration: none;'>
                @thuurrzz
            </a> 
            </br>
            <a href="https://github.com/y0naha" style='text-decoration: none;'>
                @y0naha
            </a>
            </br>
            <a href="https://github.com/lucas-silvs" style='text-decoration: none;'>
                @lucas-silvs
            </a>
        </h4>
    """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    run()
