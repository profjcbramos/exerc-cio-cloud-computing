# tratamento_ama.py
# -------------------------------------------------------------
# Este script trata a base da AMA (Avaliação de Monitoramento da Aprendizagem)
# no nível aluno–descritor, padronizando colunas e formatos
# para integração com as bases do Paebes.
# -------------------------------------------------------------

import pandas as pd
from datetime import datetime
import re


# -------------------------------------------------------------
# Funções auxiliares
# -------------------------------------------------------------

def extrair_data_referencia(nome_avaliacao):
    """
    Extrai o ano e o trimestre do nome da avaliação e retorna uma data (AAAA-MM-01)
    Exemplo: 'AMA - 3º Trimestre 2024' → 2024-10-01
    """
    match = re.search(r'(\d{4}).*?(\d)[ºo]\s*Trimestre', str(nome_avaliacao))
    if match:
        ano, tri = int(match.group(1)), int(match.group(2))
        mes_ref = {1: 4, 2: 7, 3: 10}.get(tri, 6)
        return datetime(ano, mes_ref, 1)
    return pd.NaT


def expandir_listas(row):
    """
    Recebe uma linha com campos:
      - CD_HABILIDADE (descritores)
      - DC_HABILIDADE_ACERTO (acertos)
      - DC_HABILIDADE_TOTAL (totais)
    e devolve uma lista de dicionários, um por descritor.
    """
    habilidades = str(row["CD_HABILIDADE"]).split("|")
    acertos = str(row["DC_HABILIDADE_ACERTO"]).split("|")
    totais = str(row["DC_HABILIDADE_TOTAL"]).split("|")

    registros = []
    for i, desc in enumerate(habilidades):
        if desc.strip() == "nan" or desc.strip() == "":
            continue
        try:
            qtd_acertos = int(acertos[i]) if i < len(acertos) else 0
            qtd_total = int(totais[i]) if i < len(totais) else 0
            registros.append({
                "CD_DESCRITOR": desc.strip(),
                "QTD_ACERTOS": qtd_acertos,
                "QTD_ITENS": qtd_total,
                "QTD_ERROS": qtd_total - qtd_acertos
            })
        except ValueError:
            continue
    return registros


# -------------------------------------------------------------
# Função principal de tratamento
# -------------------------------------------------------------

def tratar_ama(caminho_arquivo, caminho_saida):
    print(f"\n📂 Lendo arquivo: {caminho_arquivo}")
    df = pd.read_csv(caminho_arquivo, compression='infer', low_memory=False)

    # 🔧 Padroniza nomes de colunas
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

    print("🔎 Filtrando apenas alunos avaliados (FL_AVALIADO_GERAL == 1)...")
    df = df[df["FL_AVALIADO_GERAL"] == 1].copy()

    print("🎓 Filtrando apenas 3ª série do Ensino Médio...")
    filtro_3serie = df["DC_ETAPA_APLICACAO"].str.contains("3|3A|3ª|3º", case=False, na=False) & \
                df["DC_ETAPA_APLICACAO"].str.contains("MÉDIO", case=False, na=False)
    df = df[filtro_3serie].copy()
    if df.empty:
        print("⚠️ Nenhum registro encontrado após aplicar o filtro (3ª série).")
        print("💡 Verifique se o campo DC_ETAPA_APLICACAO contém valores como 'ENSINO MÉDIO - 3ª SÉRIE'.")
    return pd.DataFrame()

    
    print(f"✅ Total de alunos após filtro: {len(df):,}")

    print("🧩 Expandindo listas de descritores e acertos...")
    registros_expandidos = []

    for _, row in df.iterrows():
        base_info = {
            "NM_AVALIACAO": row["NM_AVALIACAO"],
            "DT_REFERENCIA": extrair_data_referencia(row["NM_AVALIACAO"]),
            "TP_INSTANCIA": "ALUNO",
            "NM_DISCIPLINA": row["NM_DISCIPLINA"],
            "TX_ACERTO": row.get("TX_ACERTO", None),
            "DC_TIPO_ENSINO": "ENSINO MÉDIO",  # fixo após filtro
            "CD_ALUNO_INEP": row.get("CD_ALUNO_INEP", None),
            "CD_ESCOLA": row.get("CD_ESCOLA", None),
            "CD_MUNICIPIO": row.get("CD_MUNICIPIO", None),
            "CD_REGIONAL": row.get("CD_REGIONAL", None)
        }

        descritores = expandir_listas(row)
        for desc in descritores:
            registros_expandidos.append({**base_info, **desc})

    print(f"✅ Registros expandidos: {len(registros_expandidos):,}")

    df_final = pd.DataFrame(registros_expandidos)

    print("🔑 Gerando chave de combinação...")
    # tratamento seguro para valores ausentes e ausência da coluna
    df_final["CD_ALUNO_INEP"] = df_final.get("CD_ALUNO_INEP", 0).fillna(0).astype("Int64").astype(str)
    df_final["CD_ESCOLA"] = df_final.get("CD_ESCOLA", 0).fillna(0).astype("Int64").astype(str)
    df_final["CD_MUNICIPIO"] = df_final.get("CD_MUNICIPIO", 0).fillna(0).astype("Int64").astype(str)
    df_final["CD_REGIONAL"] = df_final.get("CD_REGIONAL", 0).fillna(0).astype("Int64").astype(str)

    df_final["CHAVE_COMBINACAO"] = (
        df_final["CD_ALUNO_INEP"] + "|" +
        df_final["CD_ESCOLA"] + "|" +
        df_final["CD_MUNICIPIO"] + "|" +
        df_final["CD_REGIONAL"]
    )

    print("🧹 Ajustando tipos e removendo inconsistências...")
    df_final["QTD_ACERTOS"] = pd.to_numeric(df_final["QTD_ACERTOS"], errors="coerce").fillna(0).astype(int)
    df_final["QTD_ITENS"] = pd.to_numeric(df_final["QTD_ITENS"], errors="coerce").fillna(0).astype(int)
    df_final["QTD_ERROS"] = pd.to_numeric(df_final["QTD_ERROS"], errors="coerce").fillna(0).astype(int)

    print("💾 Selecionando colunas finais...")
    colunas_finais = [
        "NM_AVALIACAO", "DT_REFERENCIA", "TP_INSTANCIA",
        "NM_DISCIPLINA", "CD_DESCRITOR", "QTD_ITENS", "QTD_ACERTOS", "QTD_ERROS",
        "TX_ACERTO", "DC_TIPO_ENSINO",
        "CD_ALUNO_INEP", "CD_ESCOLA", "CD_MUNICIPIO", "CD_REGIONAL",
        "CHAVE_COMBINACAO"
    ]
    df_final = df_final[colunas_finais]

    nome_saida = caminho_saida
    df_final.to_csv(nome_saida, index=False, compression="gzip")
    print(f"\n✅ Base tratada salva com sucesso em: {nome_saida}")
    print(f"Total de linhas: {len(df_final):,}")
    return df_final


# -------------------------------------------------------------
# Execução direta (para teste local)
# -------------------------------------------------------------
if __name__ == "__main__":
    caminho = "AMA_2024_3T.csv.gz"  # ajuste conforme o nome do arquivo real
    caminho_saida = 'data/tratamento/ama_2024_1T.csv'
    tratar_ama(caminho,caminho_saida)
