import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium


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
