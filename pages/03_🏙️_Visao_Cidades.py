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
df['Cuisines'] = df.loc[:, 'Cuisines'].apply(lambda x: x.split(',')[0])

df1 = df.copy()

#streamlit
st.set_page_config(page_title='Cidades', page_icon='🏙️', layout='wide')
st.markdown('# 🏙️ Visão Cidades')
st.sidebar.markdown('### Filtros')
filtro_paises = st.sidebar.multiselect(
    'Escolha os Países que deseja visualizar as informações:', df1['Country Code'].unique(), default=['Brazil', 'Australia', 'Canada','England', 'Qatar', 'South Africa'])
linhas_selecionadas = df1['Country Code'].isin(filtro_paises)
df1 = df1.loc[linhas_selecionadas,:]

with st.container():
    cols= ['City','Restaurant ID','Country Code']
    df_aux= df1.loc[:,cols].groupby('City').count().sort_values('Restaurant ID', ascending=False).reset_index()
    fig = px.bar(df_aux.head(10), x='City', y='Restaurant ID', 
                 text='Restaurant ID', title='Top 10 Cidades com mais Restaurantes', 
                 labels={'City': 'Cidade', 'Restaurant ID': 'Restaurantes',},)
    st.plotly_chart(fig, use_container_widht=True)
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        df_aux = df1[df1['Aggregate rating'] >= 4].groupby('City').size().reset_index(name='Total de restaurantes com média > 4') \
            .sort_values('Total de restaurantes com média > 4', ascending=False, ignore_index=True)
        fig = px.bar(df_aux.head(7), x='City', y='Total de restaurantes com média > 4', 
                 text='Total de restaurantes com média > 4', title='Top 7 Cidades com Restaurantes com média de avaliação acima de 4', 
                 labels={'City': 'Cidade', 'Total de restaurantes com média > 4': 'Restaurantes',},)
        st.plotly_chart(fig, use_container_widht=True)
        
    with col2:
        df_aux = df1[df1['Aggregate rating'] <= 2.5].groupby('City').size().reset_index(name='Total de restaurantes com média < 2.5') \
            .sort_values('Total de restaurantes com média < 2.5', ascending=False, ignore_index=True)
        fig = px.bar(df_aux.head(7), x='City', y='Total de restaurantes com média < 2.5', 
                 text='Total de restaurantes com média < 2.5', title='Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5', 
                 labels={'City': 'Cidade', 'Total de restaurantes com média < 2.5': 'Restaurantes',},)
        st.plotly_chart(fig, use_container_widht=True)

with st.container():
    cols = ['City','Cuisines']
    df_aux= df1.loc[:, cols].groupby('City').nunique().sort_values('Cuisines', ascending=False).reset_index()
    fig = px.bar(df_aux.head(10), x='City', y='Cuisines', 
                 text='Cuisines', title='Top 10 Cidades com mais Restaurantes com tipos de Culinária distintos', 
                 labels={'City': 'Cidade', 'Cuisines': 'Tipo de Culinária',},)
    st.plotly_chart(fig, use_container_widht=True)