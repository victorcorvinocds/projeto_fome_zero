import pandas as pd
import numpy as np
import plotly.express as px
import inflection
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

df = pd.read_csv('zomato1.csv')
df = df.dropna()
df = df.drop_duplicates()

# FUNÇÕES AUXILIARES

# PREENCHENDO O NOME DOS PAÍSES
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]
# TRANSFORMANDO OS VALORES DA COLUNA COUNTRY CODE DE CÓDIGO PARA NOME DO PAÍS
df['Country Code'] = df.loc[:,'Country Code'].apply(country_name)
df['Country Code'].unique()

# CRIAÇÃO DO TIPO DE CATEGORIA DE COMIDA
#def create_price_tye(price_range):
#    if price_range == 1:
#        return "cheap"
#    elif price_range == 2:
#       return "normal"
#    elif price_range == 3:
#        return "expensive"
#   else:
#        return "gourmet

# CRIAÇÃO DO NOME DAS CORES
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

# RENOMEAR AS COLUNAS DO DATAFRAME
#def rename_columns(dataframe):
#    df = dataframe.copy()
#    title = lambda x: inflection.titleize(x)
#    snakecase = lambda x: inflection.underscore(x)
#    spaces = lambda x: x.replace(" ", "")
#    cols_old = list(df.columns)
#    cols_old = list(map(title, cols_old))
#    cols_old = list(map(spaces, cols_old))
#    cols_new = list(map(snakecase, cols_old))
#    df.columns = cols_new
#    return df

# CATEGORIZAR TODOS OS RESTAURANTES SOMENTE POR UM TIPO DE CULINÁRIA
df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

df1 = df.copy()

#streamlit
st.set_page_config(page_title='Geral', page_icon='📊', layout='wide')
st.sidebar.markdown('### Filtros')
filtro_paises = st.sidebar.multiselect(
    'Escolha os Países que deseja visualizar as informações:', df1['Country Code'].unique(), default=['Brazil', 'Australia', 'Canada','England', 'Qatar', 'South Africa'])
linhas_selecionadas = df1['Country Code'].isin(filtro_paises)
df1 = df1.loc[linhas_selecionadas,:]

st.markdown('# Fome Zero!')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        restaurantes_cadastrados= df1['Restaurant ID'].nunique()
        col1.metric('Restaurantes Cadastrados', restaurantes_cadastrados)
    with col2:
        paises_cadastrados = df1['Country Code'].nunique()
        col2.metric('Países Cadastrados', paises_cadastrados)
    with col3:
        cidades_cadastradas= df1['City'].nunique()
        col3.metric('Cidades Cadastradas', cidades_cadastradas)
    with col4:
        avaliacoes= df1['Votes'].sum()
        col4.metric('Avaliações Feitas', avaliacoes)
    with col5:
        tipo_culinaria= df1['Cuisines'].nunique()
        col5.metric('Tipo de Culinária', tipo_culinaria)
        
with st.container():
    map = folium.Map()
    for index, location_info in df1.iterrows():
            folium.Marker(  [location_info['Latitude'],
                            location_info['Longitude']],
                            popup= location_info[['Restaurant Name','Average Cost for two','Cuisines','Aggregate rating']]).add_to(map)
    folium_static(map, width=1024, height=600)