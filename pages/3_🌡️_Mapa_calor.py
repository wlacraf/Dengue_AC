import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd



def load_data(file_path):
    # Carrega o DataFrame do arquivo CSV
    df = pd.read_csv(file_path)

    # Filtra o DataFrame para manter apenas as linhas onde Suspeito=0
    filtered_df = df[df['Suspeito'] == 1]
    return filtered_df


# st.subheader(" Pontos suspeitos")
file_path = 'pages/piscinas.csv'
df = load_data(file_path)
df['value'] = 1  # Adiciona uma coluna de valor constante ao DataFrame


# Inicializando um mapa base
#m = leafmap.Map()
latitude_central = df['LAT'].mean()
longitude_central = df['LON'].mean()
m=leafmap.Map(location=[latitude_central, longitude_central], zoom_start=16)

m.add_basemap("Stamen Toner")
# Adicionando o mapa de calor ao mapa base
# Assuma que 'latitude' e 'longitude' são as colunas do seu DataFrame 'dt' contendo as coordenadas
m.add_heatmap(df, latitude="LAT", longitude="LON", radius=20, name="Heat Map", value='value')

# Usando o Streamlit para exibir o mapa
# Primeiro, o mapa é salvo como um arquivo HTML temporário
map_html = m.to_html()

# Então, o Streamlit usa o método 'st.components.v1.html' para exibir o HTML
st.components.v1.html(map_html, height=500, scrolling=True)