# --- Página: Diálogos ---
import streamlit as st

if "Diálogos" in st.session_state.get("pagina", ""):
    col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### Diálogos")
with col2:
    st.markdown("""
<div style='text-align: right; font-size: 20px; font-weight: bold;'>
DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.write("Espaço para artigos, propostas de atividades, referências externas e fórum para debate.")