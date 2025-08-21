import streamlit as st
from PIL import Image


st.set_page_config(page_title="DIDALE", layout="wide")


# CABEÇALHO
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### Apresentação")
with col2:
    st.markdown("""
<div style='text-align: right; font-size: 20px; font-weight: bold;'>
DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala
</div>
""", unsafe_allow_html=True)


st.markdown("---")


st.title("Atividade de Construção de Painel Interativo")
st.subheader("João Carlos Barcelos - Língua Portuguesa")


st.markdown("""
### Descrição Acadêmica


Aplicativo desenvolvido como parte das atividades da pós-graduação, com foco na exploração e relação dos descritores das avaliações externas com as habilidades do Currículo Estadual.


### Apresentação


Este painel interativo foi criado com o objetivo de facilitar o acesso, o entendimento e a análise dos descritores utilizados em avaliações externas em larga escala. A partir de uma proposta de visualização e relação entre descritores e habilidades da BNCC, espera-se contribuir para um uso pedagógico mais refinado desses indicadores. A metodologia inclui análise textual para mapeamento entre descritores e habilidades, consulta histórica de resultados por filtro, exploração de relações entre os descritores e um espaço para dialogar com produções externas.
""")