import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import base64

# Função para carregar dados do CSV
# Função para carregar dados do CSV e filtrar
def load_data(file_path):
    # Carrega o DataFrame do arquivo CSV
    df = pd.read_csv(file_path)

    # Filtra o DataFrame para manter apenas as linhas onde Suspeito=0
    filtered_df = df[df['Suspeito'] == 1]

    return filtered_df


st.subheader(" Pontos suspeitos")
file_path = 'pages/piscinas.csv'
df = load_data(file_path)
numero=len(df)
st.write(f"{numero} pontos")
if not df.empty:
    # Inicia o mapa
    m = folium.Map(location=[ -22.973356,-42.025602], zoom_start=16)

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
        icon_color = 'green' if row['status'] else 'red'
        # Construir o caminho da imagem usando o id_campo. Ajuste o caminho e a extensão conforme necessário.
        image_path = f"imagens/{row['id_campo']}.jpg"
        # Usar o método de incorporação de imagem base64 para inline das imagens
        encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode()
        image_html = f"<img src='data:image/jpeg;base64,{encoded_image}' width='200' height='200'><br>ID: {row['id_campo']}"
        iframe = folium.IFrame(image_html, width=220, height=220)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=[row['LAT'], row['LON']],
                      popup=popup,tooltip=f"ID: {row['id_campo']}",
                      icon=folium.Icon(color=icon_color)).add_to(m)

    with st.container():
        # Opção para salvar o DataFrame atualizado de volta para um arquivo CSV
        if st.button('Atualizar Alterações'):
            for idx, row in df.iterrows():
                icon_color = 'green' if row['status'] else 'red'
                folium.Marker(location=[row['LAT'], row['LON']], popup=f"ID: {row['id_campo']}",
                              icon=folium.Icon(color=icon_color)).add_to(m)

    folium_static(m)
