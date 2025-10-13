import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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

st.write("Gráficos com resultados dos descritores, número de itens, série histórica, com filtros por regional, escola, etapa, etc. [Dados de amostra]")

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

# ---- Componente curricular ----
componentes = sorted(df["NM_DISCIPLINA"].dropna().unique())
componente = st.sidebar.selectbox("Componente curricular", componentes)

if not componente:
    st.info("Selecione um componente curricular para iniciar a análise.")
    st.stop()

# ---- Descritores ----
descritores = sorted(df.query("NM_DISCIPLINA == @componente")["CD_DESCRITOR"].dropna().unique())
st.sidebar.markdown("#### Seleção de descritores")
select_all = st.sidebar.checkbox("Selecionar todos", value=True)

if select_all:
    descritores_selecionados = descritores
else:
    descritores_selecionados = st.sidebar.multiselect("Escolha os descritores", descritores)

# ---- Nível de análise ----
nivel = st.sidebar.radio("Nível de granularidade", ["Estado", "Regional", "Município", "Escola"], horizontal=True)

# ---- Filtros dinâmicos ----
regiao = municipio = escola = None

if nivel in ["Regional", "Município", "Escola"]:
    regioes = sorted(
    df["NM_REGIONAL"]
    .dropna()                              # remove np.nan
    .astype(str)                           # garante strings
    .loc[lambda x: ~x.str.lower().eq("nan")]  # remove 'nan' textual
    .unique()
    )

    regiao = st.sidebar.selectbox("Regional", ["(Todas)"] + regioes)

if nivel in ["Município", "Escola"] and regiao and regiao != "(Todas)":
    municipios = sorted(df.query("NM_REGIONAL == @regiao")["NM_MUNICIPIO"].dropna().unique())
    municipio = st.sidebar.selectbox("Município", ["(Todos)"] + municipios)

if nivel == "Escola" and municipio and municipio != "(Todos)":
    escolas = sorted(df.query("NM_MUNICIPIO == @municipio")["NM_ESCOLA"].dropna().unique())
    escola = st.sidebar.selectbox("Escola", ["(Todas)"] + escolas)

# ==============================
# FILTRO APLICADO À BASE
# ==============================
df_filt = df.query("NM_DISCIPLINA == @componente and CD_DESCRITOR in @descritores_selecionados").copy()

# ---- Aplicação condicional dos filtros ----
if nivel == "Regional" and regiao and regiao != "(Todas)":
    df_filt = df_filt.query("NM_REGIONAL == @regiao")
elif nivel == "Município" and municipio and municipio != "(Todos)":
    df_filt = df_filt.query("NM_MUNICIPIO == @municipio")
elif nivel == "Escola" and escola and escola != "(Todas)":
    df_filt = df_filt.query("NM_ESCOLA == @escola")
elif nivel == "Estado":
    # Se o nível for Estado, nenhuma filtragem adicional é aplicada
    # Isso representa a rede estadual completa
    pass

# =======================================
# CÁLCULO UNIFICADO DA TAXA DE ACERTO
# =======================================
df_filt = df_filt.copy()
df_filt["QTD_ACERTOS"] = pd.to_numeric(df_filt["QTD_ACERTOS"], errors="coerce").fillna(0)
df_filt["QTD_ERROS"] = pd.to_numeric(df_filt["QTD_ERROS"], errors="coerce").fillna(0)

# --- Taxa de acerto ponderada ---
df_filt["TX_ACERTO"] = np.where(
    (df_filt["QTD_ACERTOS"] + df_filt["QTD_ERROS"]) > 0,
    (df_filt["QTD_ACERTOS"] / (df_filt["QTD_ACERTOS"] + df_filt["QTD_ERROS"])) * 100,
    np.nan
)

# =======================================
# MERGE COM A BASE DE DESCRITORES
# =======================================
descritores_info = pd.read_csv(
    '/workspaces/exerc-cio-cloud-computing/data/descritores_paebes_23_24.csv',
    encoding='ISO-8859-1', sep=';'
)
descritores_info["CD_DESCRITOR"] = descritores_info["CD_DESCRITOR"].astype(str).str.strip()
descritores_info["NM_DESCRITOR"] = descritores_info["NM_DESCRITOR"].astype(str).str.strip()

df_filt["CD_DESCRITOR"] = df_filt["CD_DESCRITOR"].astype(str).str.strip()

# --- Junta as descrições dos descritores ---
df_descritor = df_filt.merge(descritores_info, on="CD_DESCRITOR", how="left")

# =======================================
# TABS
# =======================================
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
        # --- Agregar corretamente ---
        df_grouped = (
            df_2025.groupby(["CD_DESCRITOR", "NM_AVALIACAO"], as_index=False)
            .agg({"QTD_ACERTOS": "sum", "QTD_ERROS": "sum"})
        )
        df_grouped["TX_ACERTO"] = (
            df_grouped["QTD_ACERTOS"] / (df_grouped["QTD_ACERTOS"] + df_grouped["QTD_ERROS"])
        ) * 100

        # --- Gráfico de barras agrupadas ---
        fig_bar = px.bar(
            df_grouped,
            x="CD_DESCRITOR",
            y="TX_ACERTO",
            color="NM_AVALIACAO",
            barmode="group",
            title=f"Desempenho por descritor - {componente} (Avaliações 2025)",
            labels={"TX_ACERTO": "Taxa de acerto (%)", "CD_DESCRITOR": "Descritor", "NM_AVALIACAO": "Avaliação"},
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
            df_filt.groupby(["DT_REFERENCIA", "CD_DESCRITOR"], as_index=False)
            .agg({"QTD_ACERTOS": "sum", "QTD_ERROS": "sum"})
        )

        df_time["TX_ACERTO"] = np.where(
            (df_time["QTD_ACERTOS"] + df_time["QTD_ERROS"]) > 0,
            (df_time["QTD_ACERTOS"] / (df_time["QTD_ACERTOS"] + df_time["QTD_ERROS"])) * 100,
            np.nan,
        )

        # --- Linha histórica ---
        fig_line = px.line(
            df_time,
            x="DT_REFERENCIA",
            y="TX_ACERTO",
            color="CD_DESCRITOR",
            markers=True,
            hover_name="CD_DESCRITOR",
            title=f"Evolução da taxa de acerto - {componente}",
            labels={"DT_REFERENCIA": "Data da avaliação", "TX_ACERTO": "Taxa de acerto (%)"},
        )
        fig_line.update_layout(height=500)
        st.plotly_chart(fig_line, use_container_width=True)

        # --- Crescimento ---
        df_growth = (
            df_time.sort_values(["CD_DESCRITOR", "DT_REFERENCIA"])
            .groupby("CD_DESCRITOR")
            .apply(lambda s: s["TX_ACERTO"].iloc[-1] - s["TX_ACERTO"].iloc[0] if len(s) > 1 else 0)
            .reset_index(name="Crescimento")
        )

        fig_growth = px.bar(
            df_growth.sort_values("Crescimento", ascending=False),
            x="CD_DESCRITOR",
            y="Crescimento",
            title="Crescimento médio dos descritores (último - primeiro registro)",
            text_auto=".2f",
            labels={"Crescimento": "Variação da taxa de acerto (p.p.)"},
        )
        fig_growth.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_growth, use_container_width=True)


# ==============================
# TAB 3: INFORMAÇÕES DO DESCRITOR
# ==============================
with tab3:
    st.subheader("ℹ️ Informações do descritor")

    st.write("Tabela com os descritores selecionados:")

    # --- Agregação final por descritor ---
    df_descritor_agg = (
        df_descritor.groupby(["CD_DESCRITOR", "NM_DESCRITOR", "NM_DISCIPLINA"], as_index=False)
        .agg({"QTD_ITENS": "sum", "QTD_ACERTOS": "sum", "QTD_ERROS": "sum"})
    )

    df_descritor_agg["TX_ACERTO"] = np.where(
        (df_descritor_agg["QTD_ACERTOS"] + df_descritor_agg["QTD_ERROS"]) > 0,
        (df_descritor_agg["QTD_ACERTOS"] / (df_descritor_agg["QTD_ACERTOS"] + df_descritor_agg["QTD_ERROS"])) * 100,
        np.nan
    )

    # --- Exibir tabela agregada ---
    st.dataframe(
        df_descritor_agg[[
            "CD_DESCRITOR", "NM_DESCRITOR", "NM_DISCIPLINA",
            "QTD_ITENS", "QTD_ACERTOS", "TX_ACERTO"
        ]].round({"TX_ACERTO": 2}),
        use_container_width=True
    )

    st.write("Estatísticas descritivas:")
    st.dataframe(
        df_filt[["TX_ACERTO", "QTD_ITENS", "QTD_ACERTOS"]].describe(),
        use_container_width=True
    )

    # --- Boxplot estético e legível ---
    # Ordena os descritores pela mediana de acerto (do menor ao maior)
    ordenacao_descritores = (
        df_filt.groupby("CD_DESCRITOR")["TX_ACERTO"].median().sort_values().index
    )

    fig_box = px.box(
        df_filt,
        x="CD_DESCRITOR",
        y="TX_ACERTO",
        category_orders={"CD_DESCRITOR": ordenacao_descritores},
        color="CD_DESCRITOR",
        title="Distribuição da taxa de acerto por descritor",
        labels={"TX_ACERTO": "Taxa de acerto (%)", "CD_DESCRITOR": "Descritor"},
    )

    # --- Ajustes visuais ---
    fig_box.update_traces(
        marker=dict(opacity=0.35, size=3),  # pontos discretos
        line=dict(width=1.2),
        fillcolor="rgba(66, 135, 245, 0.3)"
    )

    fig_box.update_layout(
        height=600,
        showlegend=False,
        xaxis_tickangle=-45,
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(range=[0, 100], title="Taxa de acerto (%)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f5f5f5"),
    )

    st.plotly_chart(fig_box, use_container_width=True)
