import streamlit as st
# --- Página: Análise de Resultados ---
# CABEÇALHO - Em linha única e próximo do topo
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; 
            font-size: 14px; font-weight: bold; margin-top: -30px; margin-bottom: 5px;'>
    <div>DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala</div>
    <div style='text-align: right;'>ANÁLISE DE RESULTADOS</div>
</div>
<hr style='margin-top: 0; margin-bottom: 10px;'>
""", unsafe_allow_html=True)
st.write("Gráficos com resultados dos descritores, número de itens, série histórica, com filtros por regional, escola, etapa, etc.")
st.markdown("""<hr style='margin-top: 0; margin-bottom: 10px;'>""", unsafe_allow_html=True)

with st.container(border=1):
        st.subheader("Filtros")

col1, col2 = st.columns((1,1))
with col1:
    with st.container(border=1):
        st.subheader("Informações do descritor")

with col2:
    with st.container(border=1):
        st.subheader("Desempenho nas últimas avaliações")

with st.container(border=1):
        st.subheader("Série histórica")