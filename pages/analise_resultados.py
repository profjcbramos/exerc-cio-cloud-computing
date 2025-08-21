import streamlit as st
# --- Página: Análise de Resultados ---
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### Análise de Resultados")
with col2:
    st.markdown("""
<div style='text-align: right; font-size: 20px; font-weight: bold;'>
DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.write("Gráficos com resultados dos descritores, número de itens, série histórica, com filtros por regional, escola, etapa, etc.")