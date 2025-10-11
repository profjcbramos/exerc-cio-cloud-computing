import pandas as pd
import os

def criar_amostra(caminho_entrada="data/base_tratada.parquet", caminho_saida="data/base_amostra.parquet", frac=0.05):
    print("🔄 Carregando base tratada completa...")
    df = pd.read_parquet(caminho_entrada)

    # Verifica se as colunas-chave estão presentes
    chaves = ["NM_DISCIPLINA", "NM_REGIONAL"]
    for col in chaves:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente: {col}")

    print(f"📊 Linhas totais antes da amostragem: {len(df):,}")

    # Cria amostra estratificada por disciplina e regional
    df_amostra = (
        df.groupby(chaves, group_keys=False)
        .apply(lambda x: x.sample(frac=frac, random_state=42) if len(x) > 50 else x)
        .reset_index(drop=True)
    )

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df_amostra.to_parquet(caminho_saida, index=False)

    print(f"✅ Amostra criada com {len(df_amostra):,} linhas ({frac*100:.0f}% da base).")
    print(f"💾 Arquivo salvo em: {caminho_saida}")

    return df_amostra


if __name__ == "__main__":
    criar_amostra()
