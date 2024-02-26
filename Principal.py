import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import leafmap.foliumap as leafmap

st.set_page_config(page_title="Combate a Arbovirose")

with st.container():
    st.title("Mapeamento Aéreo ")
    st.subheader("Prefeitura Municipal de Arraial do Cabo - Arbovirose")
    st.write("Geolocalização de Piscinas, Caixas dáguas e Hidromassagens descobertas")


with st.sidebar:
 st.sidebar.markdown("*Eng Wagner Cunha*")
 st.sidebar.write("🔵 Pontos a verificar")
 st.sidebar.write("🔴 Pontos suspeitos")
 st.sidebar.write("🟢 Pontos verificados")



with st.container():

    # Função para carregar dados do CSV
    def load_data(file_path):
        # Carrega o DataFrame do arquivo CSV
        df = pd.read_csv(file_path)

        # Verifica e adiciona a coluna 'status' se não existir, com valor padrão False
        if 'status' not in df.columns:
            df['status'] = False

        return df


    # Caminho para o arquivo CSV
    file_path = 'pages/piscinas.csv'
    # Carrega os dados
    original_df = load_data(file_path)
    numero = len( original_df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write(f"{numero} pontos")
    with col3:
        st.write("PMAC")


    # Inicia o mapa centrado nas médias das coordenadas
    m = folium.Map(location=[original_df['LAT'].mean(), original_df['LON'].mean()], zoom_start=18)

    # Adicionando camadas de mapa
    folium.TileLayer('OpenStreetMap').add_to(m)
    esri_satellite_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    folium.TileLayer(tiles=esri_satellite_url, attr='Esri', name='Esri Satellite', overlay=False, control=True).add_to(
        m)
    folium.LayerControl().add_to(m)

    # Adiciona marcadores para todos os pontos com condições de cores específicas
    for idx, row in original_df.iterrows():
        # Define a cor do ícone com base no status e se é suspeito
        if row['status']:
            icon_color = 'green'  # Status verdadeiro
        else:
            icon_color = 'red' if row['Suspeito'] == 1 else 'blue'  # Vermelho para suspeito, azul para não suspeito

        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=f"ID: {row['id_campo']} - Status: {'Verificado' if row['status'] else 'Não Verificado'} - Suspeito: {'Sim' if row['Suspeito'] == 1 else 'Não'}",
            icon=folium.Icon(color=icon_color)
        ).add_to(m)

    # Exibe o mapa no Streamlit
    folium_static(m)

####################################
# Inicializando um mapa base
#m = leafmap.Map()
# latitude_central = original_df['LAT'].mean()
# longitude_central = original_df['LON'].mean()
# m2=leafmap.Map(location=[latitude_central, longitude_central], zoom_start=13)
#
# m2.add_basemap("Stamen Toner")
# # Adicionando o mapa de calor ao mapa base
# # Assuma que 'latitude' e 'longitude' são as colunas do seu DataFrame 'dt' contendo as coordenadas
#
#
# # Usando o Streamlit para exibir o mapa
# # Primeiro, o mapa é salvo como um arquivo HTML temporário
# map_html = m2.to_html()
#
# # Então, o Streamlit usa o método 'st.components.v1.html' para exibir o HTML
# st.components.v1.html(map_html, height=500, scrolling=True)