import streamlit as st

import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIGURAÇÃO BÁSICA
# ==============================

#--- Página: Análise de Resultados ---
# CABEÇALHO - Em linha única e próximo do topo

st.set_page_config(
    page_title="Análise de Resultados",
    layout="wide"
)

st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; 
            font-size: 14px; font-weight: bold; margin-top: -30px; margin-bottom: 5px;'>
    <div>DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala</div>
    <div style='text-align: right;'>ANÁLISE DE RESULTADOS</div>
</div>
<hr style='margin-top: 0; margin-bottom: 10px;'>
""", unsafe_allow_html=True)
st.write("Gráficos com resultados dos descritores, número de itens, série histórica, com filtros por regional, escola, etapa, etc.")


# st.title("📊 DIDALE - Dossiê Interativo dos Descritores das Avaliações em Larga Escala")
# st.caption("Gráficos com resultados dos descritores, número de itens, série histórica, "
#            "com filtros por regional, escola, etapa, etc.")

# st.markdown("---")

# ==============================
# CARREGAMENTO DE DADOS
# ==============================
@st.cache_data
def carregar_base(caminho=r"data/base_unificada.csv.gz"):
    try:
        df = pd.read_csv(caminho, compression="infer", low_memory=False)
        df["DT_REFERENCIA"] = pd.to_datetime(df["DT_REFERENCIA"], errors="coerce")
        df["TX_ACERTO"] = df.get("TX_ACERTO", df["QTD_ACERTOS"] / df["QTD_ITENS"].replace(0, pd.NA))
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar base: {e}")
        return pd.DataFrame()

df = carregar_base()

if df.empty:
    st.warning("A base de dados não foi encontrada ou está vazia. "
               "Verifique se o arquivo `data/saidas/base_unificada.csv.gz` existe.")
    st.stop()

# ==============================
# BARRA LATERAL DE FILTROS
# ==============================
st.sidebar.header("🎯 Filtros de Análise")

# Componente curricular (obrigatório)
componentes = sorted(df["NM_DISCIPLINA"].dropna().unique())
componente = st.sidebar.selectbox("Componente curricular", componentes)

if not componente:
    st.info("Selecione um componente curricular para iniciar a análise.")
    st.stop()

# Filtro de descritores (checkbox)
descritores = sorted(df.query("NM_DISCIPLINA == @componente")["CD_DESCRITOR"].dropna().unique())
st.sidebar.markdown("#### Seleção de descritores")
select_all = st.sidebar.checkbox("Selecionar todos", value=True)

if select_all:
    descritores_selecionados = descritores
else:
    descritores_selecionados = st.sidebar.multiselect(
        "Escolha os descritores",
        descritores,
        placeholder="Selecione um ou mais descritores"
    )

# Granularidade
nivel = st.sidebar.radio(
    "Nível de granularidade",
    ["Estado", "Regional", "Município", "Escola"],
    horizontal=True
)

# Filtros adicionais conforme granularidade
regiao = municipio = escola = None

if nivel in ["Regional", "Município", "Escola"]:
    regioes = sorted(df["NM_REGIONAL"].dropna().unique())
    regiao = st.sidebar.selectbox("Regional", regioes)

if nivel in ["Município", "Escola"] and regiao:
    municipios = sorted(df.query("NM_REGIONAL == @regiao")["NM_MUNICIPIO"].dropna().unique())
    municipio = st.sidebar.selectbox("Município", municipios)

if nivel == "Escola" and municipio:
    escolas = sorted(df.query("NM_MUNICIPIO == @municipio")["NM_ESCOLA"].dropna().unique())
    escola = st.sidebar.selectbox("Escola", escolas)

# ==============================
# FILTRO APLICADO À BASE
# ==============================
df_filt = df.query("NM_DISCIPLINA == @componente and CD_DESCRITOR in @descritores_selecionados").copy()

if nivel == "Regional" and regiao:
    df_filt = df_filt.query("NM_REGIONAL == @regiao")
elif nivel == "Município" and municipio:
    df_filt = df_filt.query("NM_MUNICIPIO == @municipio")
elif nivel == "Escola" and escola:
    df_filt = df_filt.query("NM_ESCOLA == @escola")

# ==============================
# ESTRUTURA DE CONTEÚDO
# ==============================
st.markdown("---")
tab1, tab2, tab3 = st.tabs([
    "📈 Desempenho nas últimas avaliações",
    "📊 Série histórica",
    "ℹ️ Informações do descritor"
])

# --- TAB 1: DESEMPENHO ---
with tab1:
    st.subheader("📈 Desempenho nas últimas avaliações")
    st.info("Aqui serão exibidos gráficos comparando o desempenho por descritor e avaliação.")
    st.empty()  # espaço reservado

# --- TAB 2: SÉRIE HISTÓRICA ---
with tab2:
    st.subheader("📊 Série histórica")
    st.info("Aqui será exibido o gráfico de evolução temporal da taxa de acerto.")
    st.empty()

# --- TAB 3: INFORMAÇÕES DO DESCRITOR ---
with tab3:
    st.subheader("ℹ️ Informações do descritor")
    st.info("Aqui aparecerão as estatísticas descritivas da base filtrada.")
    st.dataframe(
        df_filt[["CD_DESCRITOR", "QTD_ITENS", "QTD_ACERTOS", "TX_ACERTO"]].describe(),
        use_container_width=True
    )

# CÓDIGO ANTERIOR
# --- Página: Análise de Resultados ---
# CABEÇALHO - Em linha única e próximo do topo
# st.markdown("""
# <div style='display: flex; justify-content: space-between; align-items: center; 
#             font-size: 14px; font-weight: bold; margin-top: -30px; margin-bottom: 5px;'>
#     <div>DIDALE - Dossiê Interativo dos descritores das Avaliações em Larga Escala</div>
#     <div style='text-align: right;'>ANÁLISE DE RESULTADOS</div>
# </div>
# <hr style='margin-top: 0; margin-bottom: 10px;'>
# """, unsafe_allow_html=True)
# st.write("Gráficos com resultados dos descritores, número de itens, série histórica, com filtros por regional, escola, etapa, etc.")
# st.markdown("""<hr style='margin-top: 0; margin-bottom: 10px;'>""", unsafe_allow_html=True)

# with st.container(border=1):
#         st.subheader("Filtros")

# col1, col2 = st.columns((1,1))
# with col1:
#     with st.container(border=1):
#         st.subheader("Informações do descritor")

# with col2:
#     with st.container(border=1):
#         st.subheader("Desempenho nas últimas avaliações")

# with st.container(border=1):
#         st.subheader("Série histórica")