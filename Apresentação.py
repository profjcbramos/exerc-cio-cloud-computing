import streamlit as st
from PIL import Image
import pandas as pd
import io
import os

st.set_page_config(page_title="DIDALE", layout="wide", initial_sidebar_state="expanded")


# CABEÇALHO - Em linha única e próximo do topo
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; 
            font-size: 14px; font-weight: bold; margin-top: -30px; margin-bottom: 5px;'>
    <div>DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala</div>
    <div style='text-align: right;'>APRESENTAÇÃO</div>
</div>
<hr style='margin-top: 0; margin-bottom: 10px;'>
""", unsafe_allow_html=True)


st.header("Atividade de Construção de Painel Interativo", divider=True)

st.markdown("""<div style='display: flex; justify-content: space-between; align-items: center; 
            font-size: 20px; font-weight: bold; margin-top: -5px; margin-bottom: 5px;'>
    <div>João Carlos Barcelos Ramos</div>
    <div style='text-align: right;'>Cloud Computing para Produtos de Dados</div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<style>
.justificado {text-align: justify; }</style>""", unsafe_allow_html=True )

st.markdown("""
    ### Descrição Acadêmica
    <div class= "justificado" >
    
    Aplicativo desenvolvido como parte das atividades da pós-graduação em Mineração de Dados Educacionais, como exercício prático na disciplina de Cloud Computing para Produtos de Dados, consistindo na construção de uma aplicação web sobre tema relevante escolhido pelo aluno.</div> 
    <hr style='margin-top: 0; margin-bottom: 10px;'>""", unsafe_allow_html=True)

col1, col2 = st.columns((2,1))

with col1:


    with st.container():

        st.subheader("Apresentação", divider=True)

        st.markdown("""
        
        <div class = "justificado"> 
        <p>Este painel interativo foi criado com o objetivo de facilitar o acesso, o entendimento e a análise dos descritores utilizados em avaliações externas em larga escala. A partir de uma proposta de visualização e relação entre descritores e habilidades da BNCC, espera-se contribuir para um uso pedagógico mais refinado desses indicadores.</p> 
        <p>Para isso, utilizamos como bases de dados os resultados de algumas avaliações em larga escala aplicadas na rede pública estadual de educação do Espírito Santo para a etapa do Ensino Médio, como o Programa de Avaliação da Educação Básica do Espírito Santo (Paebes) e a Avaliação de Monitoramento da Aprendizagem (AMA); as habilidades elencadas no currículo estadual, que são elaboradas a partir da Base Nacional Comum Curricular (BNCC); dados do censo escolar presentes na base do Inep; e as participações dos usuários da aplicação.</p>
        <p>A metodologia inclui análise textual para mapeamento entre descritores e habilidades, consulta histórica de resultados por filtro, exploração de relações entre os descritores e um espaço para dialogar com produções externas e com as participações de usuários.</p></div>
                    

        """, unsafe_allow_html=True)

with col2:
    with col2:
        

        with st.container():
            st.subheader("Metodologia", divider=False)

            st.markdown("""
            <div class="justificado">
            A metodologia aplicada inclui o mapeamento entre descritores e habilidades, análise semântica de termos, e
            visualização de resultados por níveis (escola, regional e estado), visando apoiar o uso pedagógico dos indicadores.
            </div>
            """, unsafe_allow_html=True)
with st.container():
    st.subheader("Bases de dados", divider=True)

    caminho_base = r"data/base_tratada.parquet"

    if os.path.exists(caminho_base):
        try:
            df = pd.read_parquet(caminho_base)

            st.markdown("""
            <div class="justificado">
            A base unificada tratada reúne informações das avaliações AMA e Paebes, vinculando descritores, habilidades da BNCC e
            resultados de desempenho das escolas e regionais. Abaixo, uma amostra inicial da base carregada:
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"📊 Total de registros: {df.shape[0]} linhas | {df.shape[1]} colunas")

            # --- DESCRIBE ---
            st.subheader("Resumo estatístico", divider=False)
            st.dataframe(df.describe(include='all').T, use_container_width=True)

            # --- INFO ---
            st.subheader("Estrutura da base", divider=False)
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())

        except Exception as e:
            st.error(f"Erro ao carregar a base tratada: {e}")
    else:
        st.warning("⚠️ A base tratada ainda não foi gerada. Execute o script `preparar_base.py` antes de continuar.")
