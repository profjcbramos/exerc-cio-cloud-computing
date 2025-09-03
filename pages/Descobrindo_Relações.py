# --- Página: Descobrindo Relações ---

import streamlit as st
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

with st.container(border=1):
        st.subheader("filtros de avaliações/ano")
with st.container(border=1):
        st.subheader("Heatmap dos descritores")
with st.container(border=1):
        st.subheader("Tabela dos Clusters encontrados por descritor")
col1, col2, col3 = st.columns((1,1,1))

with col1:
    with st.container(border=1):
        st.subheader("Histogramas cluster 1")
with col2:
    with st.container(border=1):
        st.subheader("Histogramas cluster 2")
with col3:
    with st.container(border=1):
        st.subheader("Histogramas cluster 3")
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