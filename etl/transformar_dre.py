from pathlib import Path

import pandas as pd


ARQUIVO_ORIGEM = Path(
    "data/raw/2Q26 Results Spreadsheet.xlsx"
)

ARQUIVO_DESTINO = Path(
    "data/processed/dre_pro_forma.csv"
)

ABA_ORIGEM = "P&L Pro Forma"
EMPRESA = "Azzas 2154"
TIPO_DEMONSTRACAO = "DRE Pro Forma"


dados_dre = pd.read_excel(
    ARQUIVO_ORIGEM,
    sheet_name=ABA_ORIGEM,
    header=3,
    usecols="B:U",
    engine="openpyxl"
)

dados_dre = (
    dados_dre
    .dropna(how="all")
    .reset_index(drop=True)
    .rename(
        columns={
            "Português": "conta_pt",
            "English": "conta_en"
        }
    )
)

dados_dre.insert(
    0,
    "ordem_linha",
    dados_dre.index + 1
)

colunas_identificacao = [
    "ordem_linha",
    "conta_pt",
    "conta_en"
]

colunas_periodos = [
    coluna
    for coluna in dados_dre.columns
    if coluna not in colunas_identificacao
]


dados_dre_longos = dados_dre.melt(
    id_vars=colunas_identificacao,
    value_vars=colunas_periodos,
    var_name="periodo",
    value_name="valor"
)
dados_dre_longos.insert(
    0,
    "empresa",
    EMPRESA
)

dados_dre_longos.insert(
    1,
    "tipo_demonstracao",
    TIPO_DEMONSTRACAO
)

dados_dre_longos.insert(
    2,
    "aba_origem",
    ABA_ORIGEM
)

dados_dre_longos.insert(
    2,
    "arquivo_origem",
    ARQUIVO_ORIGEM.name
)
periodos_validos = (
    dados_dre_longos["periodo"]
    .astype(str)
    .str.fullmatch(r"[1-4]Q\d{2}")
)

if not periodos_validos.all():
    raise ValueError(
        "Foi encontrado um período fora do padrão esperado."
    )

dados_dre_longos["trimestre"] = (
    dados_dre_longos["periodo"]
    .str[0]
    .astype(int)
)

dados_dre_longos["ano"] = (
    dados_dre_longos["periodo"]
    .str[-2:]
    .astype(int)
    + 2000
)
dados_dre_longos["unidade"] = "BRL_MILLIONS"

linhas_de_margem = (
    dados_dre_longos["conta_pt"]
    .str.startswith("Margem", na=False)
)

dados_dre_longos.loc[
    linhas_de_margem,
    "unidade"
] = "RATIO"

total_esperado = (
    len(dados_dre)
    * len(colunas_periodos)
)

total_transformado = len(dados_dre_longos)

if total_transformado != total_esperado:
    raise ValueError(
        "A quantidade de registros transformados "
        "é diferente da quantidade esperada."
    )
colunas_obrigatorias = [
    "empresa",
    "tipo_demonstracao",
    "conta_pt",
    "periodo",
    "valor"
]

valores_nulos = (
    dados_dre_longos[colunas_obrigatorias]
    .isna()
    .sum()
)

if valores_nulos.sum() > 0:
    raise ValueError(
        "Foram encontrados valores nulos:\n"
        f"{valores_nulos}"
    )


chave_registro = [
    "empresa",
    "tipo_demonstracao",
    "aba_origem",
    "ordem_linha",
    "periodo"
]

quantidade_duplicados = (
    dados_dre_longos
    .duplicated(subset=chave_registro)
    .sum()
)

if quantidade_duplicados > 0:
    raise ValueError(
        "Foram encontrados "
        f"{quantidade_duplicados} registros duplicados."
    )

colunas_finais = [
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
    "valor"
]

dados_dre_longos = dados_dre_longos[
    colunas_finais
]
print(
    f"\nTotal de registros transformados: "
    f"{len(dados_dre_longos)}"
)
print("Validação de campos obrigatórios: OK")
print(
    f"\nValidação de quantidade: OK "
    f"({total_transformado} registros)"
)
print("Validação de duplicidades: OK")

print("Validação do formato dos períodos: OK")




print(
    dados_dre_longos
    .tail(10)
    .to_string(index=False)
)

ARQUIVO_DESTINO.parent.mkdir(
    parents=True,
    exist_ok=True
)

dados_dre_longos.to_csv(
    ARQUIVO_DESTINO,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\nArquivo processado criado em: "
    f"{ARQUIVO_DESTINO}"
)