import streamlit as st
from PIL import Image

st.set_page_config(page_title="DIDALE", layout="wide")


# CABEÇALHO - Em linha única e próximo do topo
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; 
            font-size: 14px; font-weight: bold; margin-top: -30px; margin-bottom: 5px;'>
    <div>DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala</div>
    <div style='text-align: right;'>APRESENTAÇÃO</div>
</div>
<hr style='margin-top: 0; margin-bottom: 10px;'>
""", unsafe_allow_html=True)


st.markdown("Atividade de Construção de Painel Interativo")
st.markdown("""<div style='display: flex; justify-content: space-between; align-items: center; 
            font-size: 20px; font-weight: bold; margin-top: -5px; margin-bottom: 5px;'>
    <div>João Carlos Barcelos Ramos</div>
    <div style='text-align: right;'>Cloud Computing para Produtos de Dados</div>
</div>""", unsafe_allow_html=True)


st.markdown("""
### Descrição Acadêmica


Aplicativo desenvolvido como parte das atividades da pós-graduação em Mineração de Dados Educacionais, 
como exercício prático na disciplina de Cloud Computing para Produtos de Dados, consistindo na construção 
de uma aplicação web sobre tema relevante escolhido pelo aluno.


### Apresentação


Este painel interativo foi criado com o objetivo de facilitar o acesso, 
o entendimento e a análise dos descritores utilizados em avaliações externas 
em larga escala. A partir de uma proposta de visualização e relação entre descritores 
e habilidades da BNCC, espera-se contribuir para um uso pedagógico mais 
refinado desses indicadores. 

Para isso, utilizamos como bases de dados os resultados de algumas avaliações em larga escala aplicadas
na rede pública estadual de educação do Espírito Santo para a etapa do Ensino Médio, como o 
Programa de Avaliação da Educação Básica do Espírito Santo (Paebes) e a 
Avaliação de Monitoramento da Aprendizagem (AMA);
as habilidades elencadas no currículo estadual, que são elaboradas a partir da Base Nacional Comum Curricular (BNCC);
dados do censo escolar presentes na base do Inep; e as participações dos usuários da aplicação.
              

A metodologia inclui análise textual para 
mapeamento entre descritores e habilidades, consulta histórica de resultados 
por filtro, exploração de relações entre os descritores e um espaço para dialogar 
com produções externas e com as participações de usuários.
            

""")