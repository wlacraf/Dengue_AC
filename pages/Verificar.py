import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium


# Função para carregar dados do CSV
# Função para carregar dados do CSV e filtrar
def load_data(file_path):
    # Carrega o DataFrame do arquivo CSV
    df = pd.read_csv(file_path)

    # Filtra o DataFrame para manter apenas as linhas onde Suspeito=0
    filtered_df = df[df['Suspeito'] == 0]

    return filtered_df


st.title("Visualizador de Mapa com Coordenadas Geográficas dos Pontos suspeitos")
file_path = 'pages/piscinas.csv'
df = load_data(file_path)

if not df.empty:
    # Inicia o mapa
    m = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], zoom_start=16)

    # Adicionando um tileset padrão e alternativos
    folium.TileLayer('OpenStreetMap').add_to(m)


    # Adicionando Esri Satellite com URL específica
    esri_satellite_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    folium.TileLayer(
        tiles=esri_satellite_url,
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True,
    ).add_to(m)

    folium.LayerControl().add_to(m)  # Permite ao usuário escolher entre os estilos de mapa

    # Adicionando marcadores com popup
    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=f"ID: {row['id_campo']}",  # Supondo que 'id' seja o nome da coluna com a informação desejada
            icon=folium.Icon(color='blue')
        ).add_to(m)

    folium_static(m)
