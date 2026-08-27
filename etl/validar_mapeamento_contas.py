from pathlib import Path

import pandas as pd


PASTA_RAIZ = Path(__file__).resolve().parent.parent

ARQUIVO_MAPEAMENTO = (
    PASTA_RAIZ
    / "data"
    / "mappings"
    / "contas_dre_pro_forma.csv"
)

COLUNAS_ESPERADAS = [
    "tipo_demonstracao",
    "ordem_linha",
    "conta_pt",
    "conta_en",
    "unidade",
    "codigo_core",
    "nome_padronizado",
    "ordem_exibicao",
    "incluir_core",
    "observacao",
]


mapeamento = pd.read_csv(
    ARQUIVO_MAPEAMENTO,
    encoding="utf-8-sig",
)

if list(mapeamento.columns) != COLUNAS_ESPERADAS:
    raise ValueError(
        "As colunas do mapeamento estão diferentes "
        "do formato esperado."
    )

if len(mapeamento) != 30:
    raise ValueError(
        "O mapeamento deveria possuir 30 contas, "
        f"mas possui {len(mapeamento)}."
    )

if mapeamento["ordem_linha"].duplicated().any():
    raise ValueError(
        "Existem linhas de origem duplicadas."
    )

mapeamento["incluir_core"] = (
    mapeamento["incluir_core"]
    .astype("string")
    .str.strip()
    .str.upper()
)

if mapeamento["incluir_core"].isna().any():
    raise ValueError(
        "Existem contas sem decisão de inclusão."
    )

decisoes_validas = {"SIM", "NAO"}

decisoes_encontradas = set(
    mapeamento["incluir_core"]
)

if not decisoes_encontradas.issubset(
    decisoes_validas
):
    raise ValueError(
        "A coluna incluir_core aceita apenas "
        "SIM ou NAO."
    )

contas_incluidas = mapeamento[
    mapeamento["incluir_core"] == "SIM"
].copy()

contas_excluidas = mapeamento[
    mapeamento["incluir_core"] == "NAO"
].copy()

campos_obrigatorios_core = [
    "codigo_core",
    "nome_padronizado",
    "ordem_exibicao",
]

if (
    contas_incluidas[campos_obrigatorios_core]
    .isna()
    .any()
    .any()
):
    raise ValueError(
        "Existem contas incluídas com campos "
        "de mapeamento vazios."
    )

codigos_validos = (
    contas_incluidas["codigo_core"]
    .str.fullmatch(r"[A-Z0-9_]+")
)

if not codigos_validos.all():
    raise ValueError(
        "Foi encontrado um código fora do padrão."
    )

if contas_incluidas["codigo_core"].duplicated().any():
    raise ValueError(
        "Existem códigos do core duplicados."
    )

ordens = pd.to_numeric(
    contas_incluidas["ordem_exibicao"],
    errors="coerce",
)

if ordens.isna().any():
    raise ValueError(
        "Existem ordens de exibição inválidas."
    )

if (ordens % 1 != 0).any():
    raise ValueError(
        "As ordens de exibição devem ser inteiras."
    )

ordens = ordens.astype(int)

ordens_esperadas = list(
    range(1, len(contas_incluidas) + 1)
)

if sorted(ordens.tolist()) != ordens_esperadas:
    raise ValueError(
        "As ordens de exibição devem formar uma "
        "sequência sem repetições ou intervalos."
    )

if contas_excluidas["observacao"].isna().any():
    raise ValueError(
        "Toda conta excluída precisa de uma "
        "justificativa."
    )

print("Mapeamento validado: OK")
print(f"Contas de origem: {len(mapeamento)}")
print(f"Contas incluídas: {len(contas_incluidas)}")
print(f"Contas excluídas: {len(contas_excluidas)}")
print(
    f"Ordem de exibição: "
    f"1 a {len(contas_incluidas)}"
)