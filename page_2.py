import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from home import carregarDados


st.set_page_config(
    page_title='SUBCHADM',
    layout='wide'
)

header = st.container()
secao1 = st.container()
secao2 = st.container()

dados = carregarDados()


st.sidebar.markdown("# Filtros")

# Define os Filtros

# verifica na planilha quais valores existem 
setores = dados["SETOR"].unique()
ano = dados['ANO'].unique()

# cria os botões de multipla seleção
lista_setores = st.sidebar.multiselect("Setores", setores, placeholder="Selecione o Setor")
lista_ano = st.sidebar.multiselect("Anos", ano, placeholder="Selecione o Ano")

# filtra de acordo com o selecionado
if lista_setores:
   dados = dados[dados['SETOR'].isin(lista_setores)]

if lista_ano:
    dados = dados[dados['ANO'].isin(lista_ano)]



# Definir uma função para formatar os valores como moeda brasileira
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with header:
    st.write( """
    <div style="display: flex; justify-content: center; align-items: center;">
        <h1>Visualização Geral dos Dados</h1>
    </div>
    """, unsafe_allow_html= True)

    total_custos = dados['CUSTOS'].sum()

    st.write( f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <h3>Total Pago {formatar_moeda(total_custos)}</h3>
    </div>
    """, unsafe_allow_html= True)

with secao1:
    # Defina a ordem dos meses
    meses_ordenados = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']

    df_agrupado = dados.groupby(['ANO', 'MES'])['CUSTOS'].sum().reset_index()

    # Converter a coluna "ANO" para string
    df_agrupado['ANO'] = df_agrupado['ANO'].astype(str)

    df_agrupado['MES'] = pd.Categorical(df_agrupado['MES'], categories=meses_ordenados, ordered=True)
    # Use o Streamlit para exibir o gráfico
    #st.title('Custo por Mês')
    #st.line_chart(df_agrupado, x="MES", y="CUSTOS", color="ANO")
    
    # Ordenar o DataFrame pelo mês para garantir a ordem correta no gráfico
    df_agrupado = df_agrupado.sort_values(by=['ANO', 'MES'])

    # Criar o gráfico com Plotly
    fig = px.line(df_agrupado, x='MES', y='CUSTOS', color='ANO',
                title='Custo Anual ao Longo dos Meses', line_shape='spline')

    # Configurar a aparência das etiquetas do eixo x
    fig.update_layout(xaxis_tickangle=-45)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

with secao2:
    #col1, col2 = st.columns(2)
    
    
#    with col1:
    soma_custos_por_setor = dados[["SETOR", "CUSTOS"]].groupby('SETOR')['CUSTOS'].sum().reset_index().sort_values(by='CUSTOS', ascending= True)
    # # Criar o gráfico de barras com Plotly
    # fig = px.bar(soma_custos_por_setor, 
    #              x='CUSTOS', 
    #              y='SETOR', 
    #              orientation='h', 
    #              title='Gráfico de SETORES x CUSTOS',
    #              text='CUSTOS')
    # # Ajustar a posição e o formato dos rótulos
    # fig.update_traces(textposition='outside',  # Exibe os rótulos fora das barras
    #                   texttemplate='%{text:.0f}')  # Formata os valores com 2 casas decimais
    
    # # Exibir o gráfico no Streamlit
    # st.plotly_chart(fig)
    # Criar um DataFrame de exemplo

    # Criar o gráfico de mapa em árvore (treemap) com Plotly
    graficoArvore = px.treemap(soma_custos_por_setor, path=['SETOR'], values='CUSTOS', title='Setores x Custos')

    # Exibir o gráfico no Streamlit
    st.plotly_chart(graficoArvore)


    df_categoria = dados.groupby(['CATEGORIA'])['CUSTOS'].sum().reset_index()

    # with col2:
    #     # Dados para o gráfico de pizza
    #     labels = df_categoria['CATEGORIA']
    #     sizes = df_categoria['CUSTOS']

    #     graf_categoria = go.Figure(data=[go.Pie(labels=labels, values=sizes, textinfo='label+percent',
    #                                 insidetextorientation='radial'
    #                                 )])

    #     st.plotly_chart(graf_categoria)

    #dados para a tabela
    df_top_unidades = dados[["LOCAL DO SERVIÇO", "CUSTOS"]].groupby("LOCAL DO SERVIÇO")["CUSTOS"].sum().reset_index().sort_values(by='CUSTOS', ascending=False)
    # Criar uma nova coluna com os valores formatados
    df_top_unidades['R$'] = df_top_unidades['CUSTOS'].apply(formatar_moeda)

    # Redefinir o índice do DataFrame para remover a coluna de índice
    df_top_unidades = df_top_unidades.reset_index(drop=True)
    
    st.dataframe(df_top_unidades, column_config={
        "CUSTOS": 
                st.column_config.ProgressColumn("Porcentagem", 
                                            format=" ",
                                            max_value= df_top_unidades["CUSTOS"].max())})
        
        

