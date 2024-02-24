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

    # Retorna os DataFrames filtrados e o DataFrame original
    suspeitos_df = df[df['Suspeito'] == 1]
    nao_suspeitos_df = df[df['Suspeito'] == 0]
    return suspeitos_df, nao_suspeitos_df, df

# Função para atualizar o status no DataFrame original
def update_status(original_df, updates):
    for id_campo, status in updates.items():
        original_df.loc[original_df['id_campo'] == id_campo, 'status'] = status
    return original_df


st.subheader("Marque os pontos suspeitos como verificados:")
file_path = 'pages/piscinas.csv'
suspeitos_df, nao_suspeitos_df, original_df = load_data(file_path)

# Dicionário para rastrear atualizações de status
status_updates = {}


# Usando st.columns para criar duas colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Suspeitos")
    if not suspeitos_df.empty:
        for idx, row in suspeitos_df.iterrows():
            # Checkbox para cada ponto suspeito
            checked = st.checkbox(f"ID: {row['id_campo']} Suspeito", key=f"suspeito_{row['id_campo']}", value=row['status'])
            status_updates[row['id_campo']] = checked

with col2:
    st.subheader("Não Suspeitos")
    if not nao_suspeitos_df.empty:
        for idx, row in nao_suspeitos_df.iterrows():
            # Checkbox para cada ponto não suspeito
            checked = st.checkbox(f"ID: {row['id_campo']} Não Suspeito", key=f"nao_suspeito_{row['id_campo']}", value=row['status'])
            status_updates[row['id_campo']] = checked

# Atualiza o DataFrame original com base nos checkboxes
original_df = update_status(original_df, status_updates)

# Inclua aqui o código para visualização no mapa, se necessário

# Opção para salvar o DataFrame atualizado de volta para um arquivo CSV

with st.container():
    if st.button('Salvar Alterações'):
        original_df.to_csv(file_path, index=False)
        st.success('Alterações salvas com sucesso!')


