# --- Página: Descobrindo Relações ---

import streamlit as st

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import numpy as np
from pyvis.network import Network
import tempfile
import streamlit.components.v1 as components
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



st.set_page_config(layout="wide")


# CABEÇALHO - Em linha única e próximo do topo
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; 
            font-size: 14px; font-weight: bold; margin-top: -30px; margin-bottom: 5px;'>
    <div>DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala</div>
    <div style='text-align: right;'>DESCOBRINDO RELAÇÕES</div>
</div>
<hr style='margin-top: 0; margin-bottom: 10px;'>
""", unsafe_allow_html=True)
st.write("Visualização de relações entre descritores com base em dados: gráficos, KNN, heatmap, etc.")

pio.templates.default = "plotly_dark"

# --- Container: Heatmap dos descritores ---
with st.container(border=1):
    st.subheader("Heatmap dos descritores")

    componente = st.radio(
        "Selecione o componente curricular:",
        ["Língua Portuguesa", "Matemática"],
        horizontal=True
    )

    arquivo_corr = (
        "data/corr_descritores_LP.csv"
        if componente == "Língua Portuguesa"
        else "data/corr_descritores_MAT.csv"
    )

    @st.cache_data
    def carregar_corrigida(caminho):
        df = pd.read_csv(caminho, index_col=0)
        return df

    corr = carregar_corrigida(arquivo_corr)

    st.write(f"**Matriz de correlação dos descritores ({componente})**")

    # --- Heatmap interativo com Plotly ---
    fig = px.imshow(
        corr,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        aspect="auto",
        title=f"Mapa de Correlação entre Descritores - {componente}",
        labels=dict(color="Correlação de Pearson")
    )

    # 🧩 Ajustes visuais importantes
    fig.update_layout(
        autosize=True,
        width=None,             # permite se ajustar à tela
        height=800,             # altura aumentada
        margin=dict(l=50, r=50, t=80, b=50),
        title_x=0.5,            # centraliza título
        font=dict(size=12),
        coloraxis_colorbar=dict(len=0.8, y=0.5)
    )

    # Renderização no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔍 Tabela de correlações entre descritores")

    # 🔹 Mantém apenas o triângulo superior (remove duplicatas e autocorrelações)
    corr_masked = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))

    # Converter a matriz de correlação em formato longo
    corr_long = (
        corr_masked.stack()
        .reset_index()
        .rename(columns={'level_0': 'Descritor_1', 'level_1': 'Descritor_2', 0: 'Correlação'})
    )

    # Adicionar classificação textual
    def classificar_correlacao(valor):
        v = abs(valor)
        if v < 0.20:
            return "Muito fraca"
        elif v < 0.40:
            return "Fraca"
        elif v < 0.60:
            return "Moderada"
        elif v < 0.80:
            return "Forte"
        else:
            return "Muito forte"

    corr_long['Intensidade'] = corr_long['Correlação'].apply(classificar_correlacao)

    # 🔹 Seleção de descritor
    descritor_selecionado = st.selectbox(
        "Selecione um descritor para ver suas relações mais fortes (ou deixe em branco para ver todos):",
        options=[""] + sorted(corr.columns.tolist())
    )

    # 🔹 Aplicar filtro
    if descritor_selecionado:
        filtro = (corr_long['Descritor_1'] == descritor_selecionado) | (corr_long['Descritor_2'] == descritor_selecionado)
        tabela_filtrada = corr_long[filtro & (corr_long['Correlação'].abs() >= 0.4)].sort_values(by='Correlação', ascending=False)
    else:
        tabela_filtrada = corr_long.sort_values(by='Correlação', ascending=False)

    # Exibir tabela
    st.dataframe(
        tabela_filtrada,
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("### 🌐 Rede de correlações entre descritores")

    # 🔹 Caminhos de arquivos (usando o mesmo componente já selecionado acima)
    arquivo_arestas = (
        "data/arestas_descritores_LP.csv"
        if componente == "Língua Portuguesa"
        else "data/arestas_descritores_MAT.csv"
    )

    @st.cache_data
    def carregar_arestas(caminho):
        df = pd.read_csv(caminho)
        return df

    arestas = carregar_arestas(arquivo_arestas)

    # 🔹 Filtro opcional por força mínima de correlação
    limiar = st.slider(
        "Selecione o limite mínimo de correlação (|r|):",
        min_value=0.3, max_value=0.9, value=0.5, step=0.05
    )

    # Filtra as arestas pelo limiar escolhido
    arestas_filtradas = arestas[arestas["weight"].abs() >= limiar]

    # --- Criar rede com PyVis ---
    net = Network(height="700px", width="100%", bgcolor="#0E1117", font_color="white", notebook=False)

    # Adicionar nós e arestas
    for _, row in arestas_filtradas.iterrows():
        src, tgt, w = row["source"], row["target"], row["weight"]
        cor = "tomato" if w < 0 else "skyblue"
        net.add_node(src, label=src, color="skyblue", size=10)
        net.add_node(tgt, label=tgt, color="lightgreen", size=10)
        net.add_edge(src, tgt, value=abs(w), color=cor, title=f"r = {w:.2f}")

    # Layout da rede (força de repulsão ajustável)
    net.repulsion(node_distance=150, central_gravity=0.3, spring_length=150, damping=0.9)

    # --- Renderizar em arquivo temporário ---
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        net.save_graph(tmpfile.name)
        components.html(open(tmpfile.name, "r", encoding="utf-8").read(), height=700, scrolling=True)


with st.container(border=1):
    st.subheader("Tabela dos Clusters encontrados por descritor")

    # Parâmetros
    n_clusters = st.slider("Selecione o número de clusters:", 2, 10, 3)

    # Padroniza os dados
    corr_for_clust = corr.fillna(0)  # substitui NaN por 0
    scaler = StandardScaler()
    X = scaler.fit_transform(corr_for_clust)

    # Executa KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    # Cria DataFrame com os resultados
    clusters_df = pd.DataFrame({
        "Descritor": corr.columns,
        "Cluster": labels
    }).sort_values("Cluster")

    # Exibe tabela no Streamlit
    st.dataframe(
        clusters_df,
        use_container_width=True,
        hide_index=True
    )
col1, col2, col3 = st.columns((1,1,1))

with col1:
    with st.container(border=1):
        st.subheader("Histogramas cluster 0")
with col2:
    with st.container(border=1):
        st.subheader("Histogramas cluster 1")
with col3:
    with st.container(border=1):
        st.subheader("Histogramas cluster 2")
with st.container(border=1):
    col4, col5 = st.columns((1,2))

    with col4:
        with st.container(border=1):
            st.subheader("Pesquisa por descritor")
    with col5:
        with st.container(border=1):
            st.subheader("Descritores Relacionados")
    with st.container(border=1):
        st.text("Comentário")
    with st.container(border=1):
            st.subheader("Habilidade Relacionadas")
            with st.container(border=1):
                st.text("Comentário")