from pathlib import Path

import pandas as pd
from sqlalchemy import text

from conexao import criar_engine


PASTA_RAIZ = Path(__file__).resolve().parent.parent

ARQUIVO_ORIGEM = (
    PASTA_RAIZ
    / "data"
    / "processed"
    / "dre_pro_forma.csv"
)

COLUNAS_ESPERADAS = [
    "empresa",
    "tipo_demonstracao",
    "arquivo_origem",
    "aba_origem",
    "ordem_linha",
    "conta_pt",
    "conta_en",
    "ano",
    "trimestre",
    "periodo",
    "unidade",
    "valor",
]


dados_dre = pd.read_csv(
    ARQUIVO_ORIGEM,
    encoding="utf-8-sig",
)

colunas_ausentes = [
    coluna
    for coluna in COLUNAS_ESPERADAS
    if coluna not in dados_dre.columns
]

if colunas_ausentes:
    raise ValueError(
        "Colunas ausentes no CSV: "
        + ", ".join(colunas_ausentes)
    )

dados_dre = dados_dre[COLUNAS_ESPERADAS]

fontes_encontradas = (
    dados_dre[
        [
            "empresa",
            "tipo_demonstracao",
            "arquivo_origem",
            "aba_origem",
        ]
    ]
    .drop_duplicates()
)

if len(fontes_encontradas) != 1:
    raise ValueError(
        "O arquivo deve possuir apenas uma combinação "
        "de empresa, demonstração, arquivo e aba."
    )

fonte = fontes_encontradas.iloc[0]

parametros_fonte = {
    "empresa": fonte["empresa"],
    "tipo_demonstracao": fonte["tipo_demonstracao"],
    "arquivo_origem": fonte["arquivo_origem"],
    "aba_origem": fonte["aba_origem"],
}

engine = criar_engine()

with engine.begin() as conexao:
    conexao.execute(
        text(
            """
            DELETE FROM staging.resultados_financeiros
            WHERE empresa = :empresa
              AND tipo_demonstracao = :tipo_demonstracao
              AND arquivo_origem = :arquivo_origem
              AND aba_origem = :aba_origem
            """
        ),
        parametros_fonte,
    )

    dados_dre.to_sql(
        name="resultados_financeiros",
        schema="staging",
        con=conexao,
        if_exists="append",
        index=False,
        chunksize=500,
    )

    total_carregado = conexao.execute(
        text(
            """
            SELECT COUNT(*)
            FROM staging.resultados_financeiros
            WHERE empresa = :empresa
              AND tipo_demonstracao = :tipo_demonstracao
              AND arquivo_origem = :arquivo_origem
              AND aba_origem = :aba_origem
            """
        ),
        parametros_fonte,
    ).scalar_one()

print(
    f"Carga concluída: {total_carregado} "
    "registros no PostgreSQL."
)