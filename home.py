import streamlit as st
import pandas as pd
# import os
# import matplotlib.pyplot as plt
# import altair as alt
# import plotly.graph_objects as go

st.set_page_config(
    page_title='SUBCHADM',
    layout='wide'
)

@st.cache_data
def carregarDados():
    #df =pd.read_csv("./dadosComp/dadosCompletos.csv")
    #df = pd.read_excel("./dadosComp/dadosCompletos.xlsx")
    df = pd.read_excel("dadosCompletos.xlsx")

    return df

dados = carregarDados()

if "dados" not in st.session_state:
    st.session_state["dados"] = dados


# TITULO DA PAGINA
st.write("# DASHBOARD RAS - CBMERJ")


# # Define os Filtros

# #     verifica na planilha quais valores existem 
# setores = dados["SETOR"].unique()
# ano = dados['ANO'].unique()

# # cria os botões de multipla seleção
# lista_setores = st.multiselect("FILTROS", setores, placeholder="Selecione o Setor")
# lista_ano = st.multiselect("", ano, placeholder="Selecione o Ano")

# # filtra de acordo com o selecionado
# if lista_setores:
#    dados = dados[dados['SETOR'].isin(lista_setores)]

# if lista_ano:
#     dados = dados[dados['ANO'].isin(lista_ano)]

# soma_custos_por_setor = dados[["SETOR", "CUSTOS"]].groupby('SETOR')['CUSTOS'].sum().reset_index()


# # Defina a ordem dos meses
# meses_ordenados = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']

# df_agrupado = dados.groupby(['ANO', 'MES'])['CUSTOS'].sum().reset_index()

# df_agrupado['MES'] = pd.Categorical(df_agrupado['MES'], categories=meses_ordenados, ordered=True)

# # Use o Streamlit para exibir o gráfico
# st.title('Gráfico de Custo por Mês para Cada Ano')
# st.line_chart(df_agrupado, x="MES", y="CUSTOS", color="ANO")

# # Criar o primeiro gráfico
# st.title('Gráfico de SETOR x CUSTOS')
# st.bar_chart(soma_custos_por_setor, x='SETOR', y='CUSTOS', horizontal= True)

# df_categoria = dados.groupby(['CATEGORIA'])['CUSTOS'].sum().reset_index()

# print(df_categoria)

# # Dados para o gráfico de pizza
# labels = df_categoria['CATEGORIA']
# sizes = df_categoria['CUSTOS']

# fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, textinfo='label+percent',
#                              insidetextorientation='radial'
#                             )])

# st.plotly_chart(fig)

# # Use o Streamlit para exibir os gráficos lado a lado
# st.title('Gráficos Lado a Lado')
# col1, col2 = st.columns(2)

# with col1:
#     st.line_chart(df_agrupado, x="MES", y="CUSTOS", color="ANO", use_container_width=True)
# with col2:
#     st.bar_chart(soma_custos_por_setor, x='SETOR', y='CUSTOS', horizontal= True, use_container_width=True)

# # Crie o gráfico de barras
# # fig, ax = plt.subplots()
# # bars = ax.bar(soma_custos_por_setor['SETOR'], soma_custos_por_setor['CUSTOS'])

# # Adicione rótulos e título
# # ax.set_xlabel('Setores')
# # ax.set_ylabel('Custos')
# # ax.set_title('Custos por Setor')

# # Adicione rótulos de dados em cada barra
# # for bar in bars:
# #     height = bar.get_height()
# #     ax.annotate(f'{height:.2f}',
# #                 xy=(bar.get_x() + bar.get_width() / 2, height),
# #                 xytext=(0, 3),  # 3 points vertical offset
# #                 textcoords="offset points",
# #                 ha='center', va='bottom')

# # Rotacionar os rótulos do eixo x para melhor visualização
# # plt.xticks(rotation=45, ha='right')

# # Use o Streamlit para exibir o gráfico
# # st.title('Gráfico de Custos por Setor')
# # st.pyplot(fig)