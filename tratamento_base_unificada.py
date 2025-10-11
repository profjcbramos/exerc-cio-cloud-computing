import pandas as pd
import os

def preparar_base(caminho_entrada: str = r"data/base_unificada.csv.gz",
                  caminho_saida: str = r"data/base_tratada.parquet") -> pd.DataFrame:
  
    """
    Carrega e trata a base unificada aplicando:
    - Anonimização de CD_ALUNO_INEP
    - Remoção de CHAVE_COMBINACAO
    - Padronização de NM_DISCIPLINA
    - Exclusão de linhas com descritor ausente
    - Ajuste de tipos de variáveis
    - Salvamento em formato parquet
    """

    print("🔄 Iniciando tratamento da base...")

    # Leitura da base original
    df = pd.read_csv(caminho_entrada, compression="gzip")
    print(f"✅ Base original carregada: {df.shape[0]} linhas e {df.shape[1]} colunas")

    # --- Anonimização ---
    if 'CD_ALUNO_INEP' in df.columns:
        df['ID_ANONIMO'] = pd.util.hash_pandas_object(df['CD_ALUNO_INEP'], index=False).astype(str)
        df.drop(columns=['CD_ALUNO_INEP'], inplace=True)
        print("🔐 Coluna 'CD_ALUNO_INEP' anonimizada com sucesso.")

    # --- Remover coluna desnecessária ---
    if 'CHAVE_COMBINACAO' in df.columns:
        df.drop(columns=['CHAVE_COMBINACAO'], inplace=True)
        print("🧹 Coluna 'CHAVE_COMBINACAO' removida.")

    # --- Padronizar nome dos componentes ---
    if 'NM_DISCIPLINA' in df.columns:
        df['NM_DISCIPLINA'] = (
            df['NM_DISCIPLINA']
            .astype(str)
            .str.strip()
            .str.upper()
            .replace({
                'LP': 'LÍNGUA PORTUGUESA',
                'Língua Portuguesa': 'LÍNGUA PORTUGUESA',
                'MAT': 'MATEMÁTICA',
                'Mt': 'MATEMÁTICA',
                'Matemática': 'MATEMÁTICA',
                'Lp': 'LÍNGUA PORTUGUESA',
                'MT': 'MATEMÁTICA'
            })
        )
        print("🎯 Coluna 'NM_DISCIPLINA' padronizada.")

    # --- Excluir linhas com descritor nulo ---
    if 'CD_DESCRITOR' in df.columns:
        linhas_antes = len(df)
        df = df[df['CD_DESCRITOR'].notna() & (df['CD_DESCRITOR'].astype(str).str.lower() != 'nan')]
        print(f"🧽 Linhas removidas com descritor ausente: {linhas_antes - len(df)}")

    # --- Ajuste de tipos ---
    col_int = ['QTD_ITENS', 'QTD_ACERTOS', 'QTD_ERROS']
    col_float = ['TX_ACERTO']
    col_data = ['DT_REFERENCIA']

    for col in df.columns:
        if col in col_int:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        elif col in col_float:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
        elif col in col_data:
            if not pd.api.types.is_datetime64_any_dtype(df["DT_REFERENCIA"]):
                df["DT_REFERENCIA"] = pd.to_datetime(df["DT_REFERENCIA"], errors="coerce")
        else:
            df[col] = df[col].astype(str)

    print("🧩 Tipos de dados ajustados.")

    # --- Salvamento final ---
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df.to_parquet(caminho_saida, index=False)
    print(f"💾 Base tratada salva em: {caminho_saida}")

    return df


if __name__ == "__main__":
    preparar_base()



# comando para executar no terminal: python data/tratamento/preparar_base.py
