from pathlib import Path

import pandas as pd


caminho_planilha = Path("data/raw/2Q26 Results Spreadsheet.xlsx")

if not caminho_planilha.exists():
    raise FileNotFoundError(
        f"Planilha não encontrada: {caminho_planilha}"
    )

arquivo_excel = pd.ExcelFile(
    caminho_planilha,
    engine="openpyxl"
)

print("Abas encontradas:")

for aba in arquivo_excel.sheet_names:
    print(f"- {aba}")

    nome_aba = "P&L Pro Forma"

dados_brutos = pd.read_excel(
    caminho_planilha,
    sheet_name=nome_aba,
    header=None,
    nrows=10,
    usecols="A:H",
    engine="openpyxl"
)

dados_dre = pd.read_excel(
    caminho_planilha,
    sheet_name=nome_aba,
    header=3,
    usecols="B:U",
    engine="openpyxl"
)
dados_dre = (
    dados_dre
    .dropna(how="all")
    .reset_index(drop=True)
)
colunas_importantes = [
    "Português",
    "1Q25",
    "2Q25",
    "1Q26",
    "2Q26"
]

print(f"\nDados selecionados da aba: {nome_aba}")

print(
    dados_dre[colunas_importantes]
    
    .to_string(index=False)
)



print(f"\nTotal de linhas carregadas: {len(dados_dre)}")