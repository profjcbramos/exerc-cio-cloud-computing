# --- Página: Descritores x Habilidades ---
import streamlit as st

if "Descritores x Habilidades" in st.session_state.get("pagina", ""):
    col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### Descritores x Habilidades")
with col2:
    st.markdown("""
<div style='text-align: right; font-size: 20px; font-weight: bold;'>
DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.write("Aqui será possível pesquisar um descritor e ver as habilidades da BNCC relacionadas, com um campo para anotações/comentários dos visitantes.")