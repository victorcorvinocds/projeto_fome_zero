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
st.set_page_config(page_title='Tipo de Culinária', page_icon='🍽️', layout='wide')
st.sidebar.markdown('### Filtros')
filtro_paises = st.sidebar.multiselect(
    'Escolha os Países que deseja visualizar as informações:', df1['Country Code'].unique(), default=['Brazil', 'Australia', 'Canada','England', 'Qatar', 'South Africa'])
linhas_selecionadas = df1['Country Code'].isin(filtro_paises)
df1 = df1.loc[linhas_selecionadas,:]

quantidade_restaurantes = st.sidebar.slider(
    'Selecione a quantidade de Restaurantes que deseja visualizar',
    value=10, min_value=1, max_value= 20)

filtro_culinarias = st.sidebar.multiselect("Escolha os Tipos de Culinária", df1["Cuisines"].unique(), default=['BBQ','Japanese','Arabian','Brazilian', 'Italian','American'])

df_filtrado = df1[df1["Cuisines"].isin(filtro_culinarias)]
# Ordenar pelo rating médio em ordem decrescente
df_filtrado = df_filtrado.sort_values("Aggregate rating", ascending=False)
# Limitar a quantidade de restaurantes exibidos
colunas_mostradas =['Restaurant ID', 'Restaurant Name','Country Code','City','Cuisines','Aggregate rating','Average Cost for two']
df_filtrado = df_filtrado.head(quantidade_restaurantes)[colunas_mostradas]

st.markdown('# 🍽️ Visão Tipo de Culinária')
st.markdown('### Melhores restaurantes dos principais tipos Culinários')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        df_aux = df1[df1['Cuisines'] == 'Italian'][['Cuisines', 'Restaurant Name', 'Aggregate rating', 'Restaurant ID']] \
            .sort_values(['Aggregate rating', 'Restaurant ID'], ascending=[False, True]).reset_index(drop=True)
        melhor_italian = df_aux.iloc[0]
        st.markdown('#### Italiana')
        col1.metric(label=melhor_italian['Restaurant Name'], value=melhor_italian['Aggregate rating'])
    
    with col2:
        df_aux= df1[df1['Cuisines']=='American'][['Cuisines','Restaurant Name','Aggregate rating','Restaurant ID']] \
            .sort_values(['Aggregate rating','Restaurant ID'], ascending=[False, True]).reset_index(drop=True)
        melhor_american = df_aux.iloc[0]
        st.markdown('#### Americana')
        col2.metric(label=melhor_american['Restaurant Name'], value=melhor_american['Aggregate rating'])
    
    with col3:
        df_aux= df1[df1['Cuisines']=='Arabian'][['Cuisines','Restaurant Name','Aggregate rating','Restaurant ID']] \
            .sort_values(['Aggregate rating','Restaurant ID'], ascending=[False, True]).reset_index(drop=True)
        melhor_arabian = df_aux.iloc[0]
        st.markdown('#### Arábe')
        col3.metric(label=melhor_arabian['Restaurant Name'], value=melhor_arabian['Aggregate rating'])
        
    with col4:
        df_aux= df1[df1['Cuisines']=='Japanese'][['Cuisines','Restaurant Name','Aggregate rating','Restaurant ID']] \
            .sort_values(['Aggregate rating','Restaurant ID'], ascending=[False, True]).reset_index(drop=True)
        melhor_japanese = df_aux.iloc[0]
        st.markdown('#### Japonesa')
        col4.metric(label=melhor_japanese['Restaurant Name'], value=melhor_japanese['Aggregate rating'])
        
    with col5:
        df_aux= df1[df1['Cuisines']=='Brazilian'][['Cuisines','Restaurant Name','Aggregate rating','Restaurant ID']] \
            .sort_values(['Aggregate rating','Restaurant ID'], ascending=[False, True]).reset_index(drop=True)
        melhor_brasileira = df_aux.iloc[0]
        st.markdown('#### Brasileira')
        col5.metric(label=melhor_brasileira['Restaurant Name'], value=melhor_brasileira['Aggregate rating'])

with st.container():
    st.markdown('#### Top Restaurantes')
    st.dataframe(df_filtrado)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        cols = ['Cuisines','Aggregate rating']
        df_aux= df1.loc[:,cols].groupby('Cuisines').max().sort_values('Aggregate rating', ascending= False).reset_index()
        fig = px.bar(df_aux.head(10), x='Cuisines', y='Aggregate rating', 
                 text='Aggregate rating', title="Top 10 melhores tipos de culinárias", 
                 labels={'Cuisines': 'Tipo de Culinária', 'Aggregate rating': 'Avaliação Média',},)
    st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        cols = ['Cuisines','Aggregate rating']
        df_aux= df1.loc[:,cols].groupby('Cuisines').max().sort_values('Aggregate rating', ascending= True).reset_index()
        fig = px.bar(df_aux.head(10), x='Cuisines', y='Aggregate rating', 
                 text='Aggregate rating', title="Top 10 piores tipos de culinárias", 
                 labels={'Cuisines': 'Tipo de Culinária', 'Aggregate rating': 'Avaliação Média',},)
    st.plotly_chart(fig, use_container_width=True)