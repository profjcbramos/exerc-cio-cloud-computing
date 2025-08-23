# --- Página: Descritores x Habilidades ---
import streamlit as st

# CABEÇALHO - Em linha única e próximo do topo
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; 
            font-size: 14px; font-weight: bold; margin-top: -30px; margin-bottom: 5px;'>
    <div>DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala</div>
    <div style='text-align: right;'>DESCRITORES X HABILIDADES</div>
</div>
<hr style='margin-top: 0; margin-bottom: 10px;'>
""", unsafe_allow_html=True)
st.write("Aqui será possível pesquisar um descritor e ver as habilidades da BNCC relacionadas, com um campo para anotações/comentários dos visitantes.")