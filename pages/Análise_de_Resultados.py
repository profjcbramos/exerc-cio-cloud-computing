import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIGURAÇÃO BÁSICA
# ==============================

#--- Página: Análise de Resultados ---
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

# ==============================
# CARREGAMENTO DE DADOS
# ==============================
@st.cache_data(show_spinner="Carregando base otimizada...")
def carregar_base(caminho="data/base_amostra.parquet"):
    cols = [
        "NM_AVALIACAO", "DT_REFERENCIA", "TP_INSTANCIA",
        "NM_DISCIPLINA", "CD_DESCRITOR", "TX_ACERTO",
        "QTD_ITENS", "QTD_ACERTOS", "NM_ESCOLA",
        "NM_MUNICIPIO", "NM_REGIONAL"
    ]
    try:
        df = pd.read_parquet(caminho)
        if not pd.api.types.is_datetime64_any_dtype(df["DT_REFERENCIA"]):
            df["DT_REFERENCIA"] = pd.to_datetime(df["DT_REFERENCIA"], errors="coerce")
        if "TX_ACERTO" not in df.columns and {"QTD_ACERTOS", "QTD_ITENS"}.issubset(df.columns):
            df["TX_ACERTO"] = df["QTD_ACERTOS"] / df["QTD_ITENS"].replace(0, pd.NA)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar base: {e}")
        return pd.DataFrame()

df = carregar_base()

if df.empty:
    st.warning("A base tratada não foi encontrada ou está vazia. Verifique se o arquivo `data/base_tratada.parquet` existe.")
    st.stop()

# ==============================
# BARRA LATERAL DE FILTROS
# ==============================
st.sidebar.header("🎯 Filtros de Análise")

componentes = sorted(df["NM_DISCIPLINA"].dropna().unique())
componente = st.sidebar.selectbox("Componente curricular", componentes)

if not componente:
    st.info("Selecione um componente curricular para iniciar a análise.")
    st.stop()

descritores = sorted(df.query("NM_DISCIPLINA == @componente")["CD_DESCRITOR"].dropna().unique())
st.sidebar.markdown("#### Seleção de descritores")
select_all = st.sidebar.checkbox("Selecionar todos", value=True)

if select_all:
    descritores_selecionados = descritores
else:
    descritores_selecionados = st.sidebar.multiselect("Escolha os descritores", descritores)

nivel = st.sidebar.radio("Nível de granularidade", ["Estado", "Regional", "Município", "Escola"], horizontal=True)

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

st.markdown("---")
tab1, tab2, tab3 = st.tabs([
    "📈 Desempenho nas últimas avaliações",
    "📊 Série histórica",
    "ℹ️ Informações do descritor"
])

# ==============================
# TAB 1: DESEMPENHO NAS ÚLTIMAS AVALIAÇÕES
# ==============================
with tab1:
    st.subheader("📈 Desempenho nas últimas avaliações")

    df_2025 = df_filt[df_filt["DT_REFERENCIA"].dt.year == 2025]

    if df_2025.empty:
        st.warning("Não há dados de 2025 disponíveis.")
    else:
        df_grouped = (
            df_2025.groupby(["CD_DESCRITOR", "NM_AVALIACAO"], as_index=False)["TX_ACERTO"]
            .mean()
            .sort_values(["NM_AVALIACAO", "CD_DESCRITOR"])
        )

        fig_bar = px.bar(
            df_grouped,
            x="CD_DESCRITOR",
            y="TX_ACERTO",
            color="NM_AVALIACAO",
            barmode="group",
            title=f"Desempenho por descritor - {componente} (Avaliações 2025)",
            labels={"TX_ACERTO": "Taxa de acerto", "CD_DESCRITOR": "Descritor", "NM_AVALIACAO": "Avaliação"},
            text_auto=".1f",
        )
        fig_bar.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig_bar, use_container_width=True)

# ==============================
# TAB 2: SÉRIE HISTÓRICA
# ==============================
with tab2:
    st.subheader("📊 Série histórica")

    if df_filt.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
    else:
        df_time = (
            df_filt.groupby(["DT_REFERENCIA", "CD_DESCRITOR"], as_index=False)["TX_ACERTO"]
            .mean()
        )

        fig_line = px.line(
            df_time,
            x="DT_REFERENCIA",
            y="TX_ACERTO",
            color="CD_DESCRITOR",
            markers=True,
            hover_name="CD_DESCRITOR",
            title=f"Evolução da taxa de acerto - {componente}",
            labels={"DT_REFERENCIA": "Data da avaliação", "TX_ACERTO": "Taxa de acerto"},
        )
        fig_line.update_layout(height=500)
        st.plotly_chart(fig_line, use_container_width=True)

        # Crescimento médio
        df_growth = (
            df_time.groupby("CD_DESCRITOR")["TX_ACERTO"]
            .apply(lambda s: s.iloc[-1] - s.iloc[0] if len(s) > 1 else 0)
            .reset_index(name="Crescimento")
        )

        fig_growth = px.bar(
            df_growth.sort_values("Crescimento", ascending=False),
            x="CD_DESCRITOR",
            y="Crescimento",
            title="Crescimento médio dos descritores (último - primeiro registro)",
            text_auto=".2f",
        )
        fig_growth.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_growth, use_container_width=True)

# ==============================
# TAB 3: INFORMAÇÕES DO DESCRITOR
# ==============================
with tab3:
    st.subheader("ℹ️ Informações do descritor")

    st.write("Tabela com os descritores selecionados:")
    st.dataframe(
        df_filt[["CD_DESCRITOR", "NM_DISCIPLINA", "QTD_ITENS", "QTD_ACERTOS", "TX_ACERTO"]]
        .drop_duplicates(subset="CD_DESCRITOR")
        .reset_index(drop=True),
        use_container_width=True
    )

    st.write("Estatísticas descritivas:")
    st.dataframe(df_filt[["TX_ACERTO", "QTD_ITENS", "QTD_ACERTOS"]].describe(), use_container_width=True)

    fig_box = px.box(
        df_filt,
        x="CD_DESCRITOR",
        y="TX_ACERTO",
        title="Distribuição da taxa de acerto por descritor",
        labels={"TX_ACERTO": "Taxa de acerto", "CD_DESCRITOR": "Descritor"},
        points="all"
    )
    fig_box.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_box, use_container_width=True)
