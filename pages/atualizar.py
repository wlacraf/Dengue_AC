import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium


# Função para carregar dados do CSV e filtrar
def load_data(file_path):
    # Carrega o DataFrame do arquivo CSV
    df = pd.read_csv(file_path)

    # Adiciona a coluna 'status' se não existir
    if 'status' not in df.columns:
        df['status'] = False  # Presume False como valor inicial

    # Filtra o DataFrame para manter apenas as linhas onde Suspeito=1
    filtered_df = df[df['Suspeito'] == 1]

    return filtered_df, df


# Função para atualizar o status no DataFrame original
def update_status(original_df, updates):
    for id_campo, status in updates.items():
        original_df.loc[original_df['id_campo'] == id_campo, 'status'] = status
    return original_df


st.title("Visualizador de Mapa com Coordenadas Geográficas dos Pontos Suspeitos")
file_path = 'pages/piscinas.csv'
filtered_df, original_df = load_data(file_path)

# Dicionário para rastrear atualizações de status
status_updates = {}

if not filtered_df.empty:
    st.subheader("Marque os pontos suspeitos como verificados:")
    for idx, row in filtered_df.iterrows():
        # Checkbox para cada ponto suspeito
        checked = st.checkbox(f"ID: {row['id_campo']}", key=row['id_campo'], value=row['status'])
        status_updates[row['id_campo']] = checked

    # Atualiza o DataFrame original com base nos checkboxes
    original_df = update_status(original_df, status_updates)

    # Inicia o mapa
    m = folium.Map(location=[filtered_df['LAT'].mean(), filtered_df['LON'].mean()], zoom_start=16)

    # Adicionando tilesets e marcadores
    folium.TileLayer('OpenStreetMap').add_to(m)
    esri_satellite_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    folium.TileLayer(tiles=esri_satellite_url, attr='Esri', name='Esri Satellite', overlay=False, control=True).add_to(
        m)
    folium.LayerControl().add_to(m)

    for idx, row in filtered_df.iterrows():
        icon_color = 'green' if status_updates.get(row['id_campo'], row['status']) else 'red'
        folium.Marker(location=[row['LAT'], row['LON']], popup=f"ID: {row['id_campo']}",
                      icon=folium.Icon(color=icon_color)).add_to(m)

    folium_static(m)

# Opção para salvar o DataFrame atualizado de volta para um arquivo CSV
if st.button('Salvar Alterações'):
    original_df.to_csv(file_path, index=False)
    st.success('Alterações salvas com sucesso!')
