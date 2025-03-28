import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import geopandas as gpd

st.set_page_config(layout="wide")

#dados para a tabela
dados = st.session_state.get("dados")
st.sidebar.markdown("# Filtros")

# Define os Filtros

# verifica na planilha quais valores existem 
setores = dados["SETOR"].unique()
ano = dados['ANO'].unique()
mes = dados['MES'].unique()

# cria os botões de multipla seleção
lista_setores = st.sidebar.multiselect("Setores", setores, placeholder="Selecione o Setor")
lista_ano = st.sidebar.multiselect("Anos", ano, placeholder="Selecione o Ano")
lista_mes = st.sidebar.multiselect("Mes", mes, placeholder="Selecione o Mês")

# filtra de acordo com o selecionado
if lista_setores:
   dados = dados[dados['SETOR'].isin(lista_setores)]

if lista_ano:
    dados = dados[dados['ANO'].isin(lista_ano)]

if lista_mes:
    dados = dados[dados['MES'].isin(lista_mes)]



df_top_unidades = dados[["LOCAL DO SERVIÇO", "CUSTOS"]].groupby("LOCAL DO SERVIÇO")["CUSTOS"].sum().reset_index().sort_values(by='CUSTOS', ascending=False)
# Criar uma nova coluna com os valores formatados
#df_top_unidades['R$'] = df_top_unidades['CUSTOS'].apply(formatar_moeda)

# Redefinir o índice do DataFrame para remover a coluna de índice
custos = df_top_unidades.reset_index(drop=True)

# Carregar os dados das tabelas lat_lon
#custos = st.session_state.get("top_custos")  # Tabela com LOCAL_SERVICO e CUSTO
locais = pd.read_excel('dadosCompletos.xlsx', sheet_name='lat_lon')  # Tabela com LOCAL_SERVICO, LATITUDE e LONGITUDE
#locais = pd.read_excel('Gisgeo Posição Grupamento 2.xlsx', sheet_name='Planilha1')  # Tabela com LOCAL_SERVICO, LATITUDE e LONGITUDE

# Juntar os dois dataframes pelo nome do local
dados = pd.merge(custos, locais, on='LOCAL DO SERVIÇO', how='inner')
#perimetro = pd.read_json('mapa_so_estado.json')

# Criar o mapa centralizado no Rio de Janeiro
mapa = folium.Map(location=[-22.365906062519695, -41.79027491827975],
                   zoom_start=8)

# Normalizar os custos para que estejam entre 0 e 1
dados['CUSTOS_NORMALIZADOS'] = dados['CUSTOS'] / dados['CUSTOS'].max()

st.markdown(
    """
    <style>
    .full-width {
        max-width: 100%;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Preparar os dados para o HeatMap (usando custos normalizados)
heat_data = dados[['Latitude', 'Longitude', 'CUSTOS_NORMALIZADOS']].values.tolist()

# Adicionar a camada de calor ao mapa
HeatMap(heat_data, max_zoom=12, radius=15).add_to(mapa)

mapa_br = gpd.read_file('BR_UF_2021')
br_rj = mapa_br[mapa_br.SIGLA== 'RJ']
limites = folium.features.GeoJson(br_rj,
                                  style_function = lambda feature: {
                                      'color': 'black',
                                      'weight': 1,
                                      'fillOpacity': 0.0
                                  })
mapa.add_child(limites)

# Exibir o mapa no Streamlit
st.title("Mapa de Calor - Custos por Local de Serviço")
st_folium(mapa, width=1400, height=800)




