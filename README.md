# Financial Insights Brasil

Projeto de portfólio para transformar dados financeiros públicos de empresas listadas na bolsa em informações organizadas para análise e visualização.

A primeira empresa estudada é a **Azzas 2154**, utilizando sua planilha de resultados do 2T26.

## Fluxo do projeto

```text
Planilha Excel → Python/Pandas → CSV tratado → PostgreSQL → API → Dashboard React
```

O Python realiza a leitura, padronização e validação dos dados. O PostgreSQL armazena os registros estruturados. Nas próximas etapas, uma API e um dashboard apresentarão indicadores, demonstrativos e gráficos financeiros.

## Tecnologias

- Python e Pandas
- PostgreSQL
- SQLAlchemy e Psycopg
- React (próxima etapa)

## Situação atual

- transformação da DRE Pro Forma para formato tabular;
- validação de períodos, campos obrigatórios e duplicidades;
- carga de 540 registros no schema `staging` do PostgreSQL;
- estrutura preparada para receber novas demonstrações e empresas.

O projeto tem caráter educacional e busca unir análise financeira, contabilidade e automação de dados.
