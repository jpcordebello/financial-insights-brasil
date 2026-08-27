from pathlib import Path

import pandas as pd


PASTA_RAIZ = Path(__file__).resolve().parent.parent

ARQUIVO_ORIGEM = (
    PASTA_RAIZ
    / "data"
    / "processed"
    / "dre_pro_forma.csv"
)

ARQUIVO_DESTINO = (
    PASTA_RAIZ
    / "data"
    / "mappings"
    / "contas_dre_pro_forma.csv"
)

COLUNAS_ORIGEM = [
    "tipo_demonstracao",
    "ordem_linha",
    "conta_pt",
    "conta_en",
    "unidade",
]


if ARQUIVO_DESTINO.exists():
    raise FileExistsError(
        "O arquivo de mapeamento já existe. "
        "Ele não será sobrescrito automaticamente."
    )

dados_dre = pd.read_csv(
    ARQUIVO_ORIGEM,
    encoding="utf-8-sig",
)

colunas_ausentes = [
    coluna
    for coluna in COLUNAS_ORIGEM
    if coluna not in dados_dre.columns
]

if colunas_ausentes:
    raise ValueError(
        "Colunas ausentes no arquivo de origem: "
        + ", ".join(colunas_ausentes)
    )

mapeamento = (
    dados_dre[COLUNAS_ORIGEM]
    .drop_duplicates()
    .sort_values(
        [
            "tipo_demonstracao",
            "ordem_linha",
        ]
    )
    .reset_index(drop=True)
)

mapeamento["codigo_core"] = ""
mapeamento["nome_padronizado"] = ""
mapeamento["ordem_exibicao"] = ""
mapeamento["incluir_core"] = ""
mapeamento["observacao"] = ""

mapeamento.to_csv(
    ARQUIVO_DESTINO,
    sep=",",
    index=False,
    encoding="utf-8-sig",
)

print(
    f"Mapeamento criado com "
    f"{len(mapeamento)} contas."
)
print(f"Arquivo: {ARQUIVO_DESTINO}")