import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from page_2 import formatar_moeda

st.set_page_config(
    page_title='SUBCHADM',
    layout='wide'
)

# graduacao = ["SUBTEN BM","1 SGT BM","2 SGT BM","3 SGT BM","CB BM","SD BM"]
# posto =["CEL BM","TEN CEL BM","MAJ BM","CAP BM","1 TEN BM","2 TEN BM","ASP OF BM","CAD BM"]


header = st.container()
secao1 = st.container()
secao2 = st.container()
secao3 = st.container()
secao4 = st.container()

# Acessar os dados carregados
dados = st.session_state.get("dados")

def remover_ano(especialidade):
    # Verifica se o valor já foi processado (sem ano) ou não precisa ser alterado
    if "TEMP" in especialidade:
        partes = especialidade.split("/")
        # Verifica se já está processado ou contém mais de 2 barras
        if len(partes) == 3 and partes[-1].isdigit() and len(partes[-1]) == 2:
            return "/".join(partes[:-1])  # Remover o ano
        else:
            return especialidade  # Já está no formato correto
    else:
        # Caso geral: remover tudo após a primeira barra
        return especialidade.split("/")[0]

def formartaAnoIng(ano):
    if ano > 70:  # Anos maiores que 70 são do século 20 (1900s)
        return int(f"19{ano:02}")
    else:  # Anos menores ou iguais a 70 são do século 21 (2000s)
        return int(f"20{ano:02}")


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


# Aplicar a função à coluna ESPECIALIDADE
dados['QUADRO/ESPECIALIDADE'] = dados['QUADRO/ESPECIALIDADE'].apply(remover_ano)
# Filtrar o DataFrame para manter apenas as linhas onde a coluna 'CATEGORIA' é 'PRAÇA'
dados_praca = dados[dados['CATEGORIA'] == 'PRAÇA']
dados_of = dados[(dados['CATEGORIA'] != 'PRAÇA')]

# Agrupar pela especialidade e somar os custos
dados_q_praca = dados_praca.groupby('QUADRO/ESPECIALIDADE')['CUSTOS'].sum().reset_index().sort_values(by='CUSTOS', ascending= False)
dados_q_of = dados_of.groupby('QUADRO/ESPECIALIDADE')['CUSTOS'].sum().reset_index().sort_values(by='CUSTOS', ascending= False)
dados_q_of = dados_q_of[dados_q_of['QUADRO/ESPECIALIDADE'] != "INSIRA UM RG VÁLIDO"]

dados_graduacao = dados_praca.groupby('POSTO/GRADUAÇÃO')['CUSTOS'].sum().reset_index().sort_values(by='CUSTOS', ascending= False)
dados_posto = dados_of.groupby('POSTO/GRADUAÇÃO')['CUSTOS'].sum().reset_index().sort_values(by='CUSTOS', ascending= False)
dados_posto = dados_posto[dados_posto['POSTO/GRADUAÇÃO'] != "INSIRA UM RG VÁLIDO"]

# Contar os anos de ingresso
dados_ingresso = dados['ANO_INGRESSO'].value_counts().reset_index()
dados_ingresso.columns = ['ANO_INGRESSO', 'TOTAL']

# Selecionar apenas o Top 10
top_10_ingresso = dados_ingresso.head(5)
total_linhas = len(dados)

# Cálculo com formatação para 2 casas decimais
percentual = (top_10_ingresso.iloc[0, 1] / total_linhas) * 100

ano_ing = formartaAnoIng(top_10_ingresso.iloc[0, 0])

# Usando round
percentual_formatado = round(percentual, 2)
#st.write(f'Dos {total_linhas} servioços ofertados {top_10_ingresso.iloc[0, 1]} foram realizados por militares que ingressaram em {ano_ing}, percentualmente {percentual_formatado} %')

total_militares = dados['RG (SEM UTILIZAÇÃO DE PONTO)'].nunique()
prac = dados['CATEGORIA'].value_counts()

# Transformar a série em um DataFrame
prac_df = prac.reset_index()

# Renomear as colunas para facilitar o uso
prac_df.columns = ['CATEGORIA', 'TOTAL']

# Transformar os valores da coluna 'MILITAR EXERCE QUAL TIPO DE ATIVIDADE?' para caixa alta
dados['MILITAR EXERCE QUAL TIPO DE ATIVIDADE?'] = dados['MILITAR EXERCE QUAL TIPO DE ATIVIDADE?'].str.upper()

atividade = dados['MILITAR EXERCE QUAL TIPO DE ATIVIDADE?'].value_counts(dropna=False).reset_index()
atividade.columns = ['ATIVIDADE', 'TOTAL']

# Adicionar uma coluna com o percentual de cada atividade
atividade['PERCENTUAL'] = (atividade['TOTAL'] / atividade['TOTAL'].sum())*100

ferias_df = dados['O MILITAR SE ENCONTRA EM GOZO DE FÉRIAS?'].value_counts().reset_index()
ferias_df.columns = ['FERIAS', 'TOTAL']

with header:
    st.write("""# Perfil Profissional
             
             """)

            # Dados para o gráfico de pizza
    labels = prac_df['CATEGORIA']
    sizes = prac_df['TOTAL']

    graf_categoria = go.Figure(data=[go.Pie(labels=labels,
                                            values=sizes,
                                            textinfo='label+percent',
                                            insidetextorientation='radial'
                                )])
    graf_categoria.update_layout(
        title={
                'text': 'Distribuição dos Custos por Categoria',
                'y': 0.95,  # Posição do título no eixo vertical (1.0 é topo)
                'x': 0.5,   # Centralizar título no eixo horizontal
                'xanchor': 'center',
                'yanchor': 'top'
                },
            margin=dict(t=100)  # Ajustar a margem superior (t = top)
    )

    st.plotly_chart(graf_categoria)
    
with secao1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
                    ### PRAÇAS """)
        # Criar uma nova coluna com os valores formatados
        dados_q_praca['R$'] = dados_q_praca['CUSTOS'].apply(formatar_moeda)

        # Redefinir o índice do DataFrame para remover a coluna de índice
        dados_q_praca = dados_q_praca.reset_index(drop=True)
        
        st.dataframe(dados_q_praca, column_config={
            "CUSTOS": 
                    st.column_config.ProgressColumn("Porcentagem", 
                                                format=" ",
                                                max_value= dados_q_praca["CUSTOS"].max())})


    with col2:
        st.markdown("""
                    ### OFICIAIS """)
         # Criar uma nova coluna com os valores formatados
        dados_q_of['R$'] = dados_q_of['CUSTOS'].apply(formatar_moeda)

        # Redefinir o índice do DataFrame para remover a coluna de índice
        dados_q_of = dados_q_of.reset_index(drop=True)
        
        st.dataframe(dados_q_of, column_config={
            "CUSTOS": 
                    st.column_config.ProgressColumn("Porcentagem", 
                                                format=" ",
                                                max_value= dados_q_of["CUSTOS"].max())})
        
with secao2:
    # Calcular o percentual para cada valor
    dados_graduacao['PERCENTUAL'] = (dados_graduacao['CUSTOS'] / dados_graduacao['CUSTOS'].sum()) * 100

    # Criar o gráfico de barras com Plotly
    fig = px.bar(
        dados_graduacao, 
        y='CUSTOS', 
        x='POSTO/GRADUAÇÃO', 
        #orientation='h', 
        title='Gráfico de GRADUAÇÕES x CUSTOS',
        text='CUSTOS'  # Exibir os valores de custos como rótulo
    )

    # Ajustar os rótulos e o eixo para formatar como moeda brasileira
    fig.update_traces(
        texttemplate='R$ %{text:,.2f} (%{customdata:.2f}%)',  # Formata os rótulos com o prefixo "R$" e 2 casas decimais
        textposition='outside',  # Rótulos fora das barras
        customdata=dados_graduacao['PERCENTUAL']  # Inclui os percentuais como dados adicionais
    )
    fig.update_layout(
        xaxis_tickformat="R$,",  # Formata os valores no eixo X como moeda brasileira
        xaxis_title="Custos (R$)",  # Adiciona título ao eixo X
        yaxis_title="Graduação",  # Adiciona título ao eixo Y
        title_font=dict(size=16)  # Ajusta o tamanho da fonte do título
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)


    # Calcular o percentual para cada valor
    dados_posto['PERCENTUAL'] = (dados_posto['CUSTOS'] / dados_posto['CUSTOS'].sum()) * 100

    # Criar o gráfico de barras com Plotly
    fig2 = px.bar(
        dados_posto, 
        y='CUSTOS', 
        x='POSTO/GRADUAÇÃO', 
        #orientation='h', 
        title='Gráfico de POTOS x CUSTOS',
        text='CUSTOS'  # Exibir os valores de custos como rótulo
    )

    # Ajustar os rótulos e o eixo para formatar como moeda brasileira
    fig2.update_traces(
        texttemplate='R$ %{text:,.2f} (%{customdata:.2f}%)',  # Formata os rótulos com o prefixo "R$" e 2 casas decimais
        textposition='outside',  # Rótulos fora das barras
        customdata=dados_posto['PERCENTUAL']  # Inclui os percentuais como dados adicionais
    )
    fig2.update_layout(
    xaxis_tickformat="R$,",  # Formata os valores no eixo X como moeda brasileira
    xaxis_title="Custos (R$)",  # Adiciona título ao eixo X
    yaxis_title="Postos",  # Adiciona título ao eixo Y
    title_font=dict(size=16)  # Ajusta o tamanho da fonte do título
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig2)

with secao3:

    # Dados para o gráfico de pizza
    labels2 = ferias_df['FERIAS']
    sizes2 = ferias_df['TOTAL']

    graf_categoria = go.Figure(data=[go.Pie(labels=labels2, values=sizes2, textinfo='label+percent',
                                insidetextorientation='radial'
                                )])
    
    graf_categoria.update_layout(
        title={
                'text': 'RAS com Militares de Férias',
                'y': 0.95,  # Posição do título no eixo vertical (1.0 é topo)
                'x': 0.5,   # Centralizar título no eixo horizontal
                'xanchor': 'center',
                'yanchor': 'top'
                },
            margin=dict(t=100)  # Ajustar a margem superior (t = top)
    )

    st.plotly_chart(graf_categoria)


with secao4:
    dados_ingresso["ANO_INGRESSO"] = dados_ingresso["ANO_INGRESSO"].apply(formartaAnoIng)

    # Criar o histograma com Plotly
    histograma = px.histogram(
        dados_ingresso,
        x='ANO_INGRESSO',
        y='TOTAL',
        nbins=11,  # Número de bins (ajuste conforme necessário)
        title='Distribuição dos RAS por Ano de Ingresso na Corporação',
        labels={'ANO_INGRESSO': 'Ano de Ingresso'},  # Renomear rótulo do eixo x
        text_auto=True  # Mostrar os valores de cada barra
    )

    # Ajustar o layout para melhorar a visualização
    histograma.update_layout(
        xaxis_title='Ano de Ingresso',
        yaxis_title='Quantidade de RAS',
        #bargap=0.1  # Espaço entre as barras
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(histograma)