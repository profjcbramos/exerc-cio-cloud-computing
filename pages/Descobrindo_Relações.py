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