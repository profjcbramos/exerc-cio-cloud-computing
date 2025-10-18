# scripts/build_corr_descritores.py
# Requisitos: polars>=1.0, pandas, numpy, pyarrow (para parquet)

import polars as pl
import pandas as pd
import numpy as np
from pathlib import Path

# ========= CONFIG =========
PATH_IN  = Path("data/") / "base_unificada.csv"         # sua base "longa"
PATH_OUT = Path("data/")
COL_ESCOLA     = "CD_ESCOLA"        # ou "Inep" / "NM_ESCOLA" (ajuste aqui)
COL_DESCRITOR  = "CD_DESCRITOR"
COL_ACERTOS    = "QTD_ACERTOS"
COL_ERROS      = "QTD_ERROS"
MIN_ESCOLAS_POR_DESCRITOR = 30      # filtre descritores muito raros
MIN_PONTOS_PARA_PAREAR    = 20      # min_periods para correlação
SMOOTH_A = 1                        # Laplace smoothing: +a / +2a
# ==========================

PATH_OUT.mkdir(parents=True, exist_ok=True)

# 1) Ler base
df = pl.read_csv(PATH_IN, ignore_errors=True)

# 2) Agregar por escola × descritor
agg = (
    df.group_by([COL_ESCOLA, COL_DESCRITOR])
      .agg([
          pl.col(COL_ACERTOS).sum().alias("acertos"),
          pl.col(COL_ERROS).sum().alias("erros")
      ])
      .with_columns([
          ( (pl.col("acertos")+SMOOTH_A) / (pl.col("acertos")+pl.col("erros")+2*SMOOTH_A) )
          .alias("tx_acerto")
      ])
)

# 3) Mantém só descritores com presença mínima de escolas
valid_descritores = (
    agg.group_by(COL_DESCRITOR)
       .agg(pl.n_unique(COL_ESCOLA).alias("n_escolas"))
       .filter(pl.col("n_escolas") >= MIN_ESCOLAS_POR_DESCRITOR)
       [COL_DESCRITOR]
       .to_list()
)
agg = agg.filter(pl.col(COL_DESCRITOR).is_in(valid_descritores))

# 4) Pivot: linhas = escola; colunas = descritor; valores = tx_acerto
mat = (
    agg.pivot(index=COL_ESCOLA, columns=COL_DESCRITOR, values="tx_acerto")
       .sort(by=COL_ESCOLA)
)

# 5) Para correlação pairwise com min_periods, passo para pandas
mat_pd = mat.to_pandas()

# 6) Correlação Pearson (pairwise), exigindo sobreposição mínima
corr = mat_pd.corr(method="pearson", min_periods=MIN_PONTOS_PARA_PAREAR)

# 7) Salvar matriz e metadados
corr_path = PATH_OUT / "corr_descritor.parquet"
cols_path = PATH_OUT / "descritores_validos.parquet"
pd.DataFrame({"descritor": corr.columns}).to_parquet(cols_path, index=False)
corr.to_parquet(corr_path)

# 8) (Opcional) Exportar arestas > limiar para grafos/filtragem
THRESHOLDS = [0.3, 0.5, 0.7]
upper = np.triu(np.ones_like(corr, dtype=bool), k=1)
corr_vals = corr.where(upper)  # upper triangle

for th in THRESHOLDS:
    edges = []
    cols = corr.columns
    arr = corr_vals.to_numpy()
    idx_i, idx_j = np.where(arr >= th)
    for i, j in zip(idx_i, idx_j):
        edges.append((cols[i], cols[j], float(arr[i, j])))
    edges_df = pd.DataFrame(edges, columns=["descritor_u", "descritor_v", "corr"])
    edges_df.to_parquet(PATH_OUT / f"corr_edges_ge_{str(th).replace('.','_')}.parquet", index=False)

print(f"[OK] Matriz salva em: {corr_path}")
