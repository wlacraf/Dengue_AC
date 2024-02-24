import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap


# Função para carregar dados do CSV
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Filtra o DataFrame se necessário
    filtered_df = df[df['Suspeito'] == 1]
    return filtered_df


st.subheader("Mapa de Calor Avançado dos Pontos Georreferenciados")

file_path = 'pages/piscinas.csv'  # Substitua pelo caminho do seu arquivo
df = load_data(file_path)

if not df.empty:
    # Inicia o mapa
    m = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], zoom_start=16)

    # Cria uma lista de coordenadas a partir do DataFrame
    heat_data = [[row['LAT'], row['LON']] for index, row in df.iterrows()]

    # Adiciona o mapa de calor ao mapa com configurações personalizadas
    HeatMap(
        heat_data,
        min_opacity=0.5,
        max_zoom=20,
        radius=20,
        blur=15,
        gradient={0.4: 'blue', 0.4: 'cyan', 0.65: 'lime', 0.95: 'yellow', 1: 'red'}
    ).add_to(m)


    folium_static(m)
