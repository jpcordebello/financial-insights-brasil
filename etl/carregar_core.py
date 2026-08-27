from pathlib import Path

import pandas as pd
from sqlalchemy import text

from conexao import criar_engine


PASTA_RAIZ = Path(__file__).resolve().parent.parent

ARQUIVO_MAPEAMENTO = (
    PASTA_RAIZ
    / "data"
    / "mappings"
    / "contas_dre_pro_forma.csv"
)


def ler_mapeamento() -> pd.DataFrame:
    mapeamento = pd.read_csv(
        ARQUIVO_MAPEAMENTO,
        encoding="utf-8-sig",
    )

    mapeamento["incluir_core"] = (
        mapeamento["incluir_core"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    contas_incluidas = mapeamento[
        mapeamento["incluir_core"] == "SIM"
    ].copy()

    contas_incluidas["ordem_exibicao"] = (
        contas_incluidas["ordem_exibicao"]
        .astype(int)
    )

    return contas_incluidas


def ler_dados_staging(
    conexao,
) -> pd.DataFrame:
    consulta = text(
        """
        SELECT
            empresa,
            tipo_demonstracao,
            arquivo_origem,
            aba_origem,
            ordem_linha,
            conta_pt,
            conta_en,
            ano,
            trimestre,
            periodo,
            unidade,
            valor
        FROM staging.resultados_financeiros
        ORDER BY
            ano,
            trimestre,
            ordem_linha
        """
    )

    return pd.read_sql_query(
        consulta,
        conexao,
    )


def preparar_dados_core(
    dados_staging: pd.DataFrame,
    mapeamento: pd.DataFrame,
) -> pd.DataFrame:
    colunas_mapeamento = [
        "tipo_demonstracao",
        "ordem_linha",
        "conta_en",
        "unidade",
        "codigo_core",
        "nome_padronizado",
        "ordem_exibicao",
    ]

    dados_core = dados_staging.merge(
        mapeamento[colunas_mapeamento],
        on=[
            "tipo_demonstracao",
            "ordem_linha",
        ],
        how="inner",
        validate="many_to_one",
        suffixes=(
            "_staging",
            "_mapeamento",
        ),
    )

    unidades_divergentes = (
        dados_core["unidade_staging"]
        != dados_core["unidade_mapeamento"]
    )

    if unidades_divergentes.any():
        raise ValueError(
            "Existem unidades diferentes entre "
            "o staging e o mapeamento."
        )

    quantidade_periodos = (
        dados_staging["periodo"].nunique()
    )

    total_esperado = (
        len(mapeamento)
        * quantidade_periodos
    )

    if len(dados_core) != total_esperado:
        raise ValueError(
            "A quantidade de resultados preparados "
            "para o core está incorreta."
        )

    dados_core = dados_core.rename(
        columns={
            "conta_en_mapeamento": "nome_en_core",
            "unidade_mapeamento": "unidade_core",
        }
    )

    return dados_core


def carregar_empresa(
    conexao,
    dados_core: pd.DataFrame,
) -> int:
    empresas_encontradas = (
        dados_core["empresa"]
        .drop_duplicates()
    )

    if len(empresas_encontradas) != 1:
        raise ValueError(
            "A carga deve possuir apenas uma empresa."
        )

    nome_empresa = empresas_encontradas.iloc[0]

    comando = text(
        """
        INSERT INTO core.empresas (
            nome
        )
        VALUES (
            :nome
        )
        ON CONFLICT (nome)
        DO UPDATE SET
            nome = EXCLUDED.nome
        RETURNING id
        """
    )

    empresa_id = conexao.execute(
        comando,
        {
            "nome": nome_empresa,
        },
    ).scalar_one()

    return empresa_id

def carregar_periodos(
    conexao,
    dados_core: pd.DataFrame,
) -> None:
    periodos = (
        dados_core[
            [
                "ano",
                "trimestre",
                "periodo",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "ano",
                "trimestre",
            ]
        )
    )

    registros = periodos.to_dict(
        orient="records"
    )

    comando = text(
        """
        INSERT INTO core.periodos (
            ano,
            trimestre,
            periodo
        )
        VALUES (
            :ano,
            :trimestre,
            :periodo
        )
        ON CONFLICT (
            ano,
            trimestre
        )
        DO UPDATE SET
            periodo = EXCLUDED.periodo
        """
    )

    conexao.execute(
        comando,
        registros,
    )


def carregar_contas_financeiras(
    conexao,
    dados_core: pd.DataFrame,
) -> None:
    contas = (
        dados_core[
            [
                "tipo_demonstracao",
                "codigo_core",
                "nome_padronizado",
                "nome_en_core",
                "unidade_core",
                "ordem_exibicao",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "nome_padronizado": "nome_pt",
                "nome_en_core": "nome_en",
                "unidade_core": "unidade",
            }
        )
        .sort_values("ordem_exibicao")
    )

    if len(contas) != 28:
        raise ValueError(
            "A carga deveria possuir 28 contas "
            "financeiras padronizadas."
        )

    registros = contas.to_dict(
        orient="records"
    )

    comando = text(
        """
        INSERT INTO core.contas_financeiras (
            codigo,
            tipo_demonstracao,
            nome_pt,
            nome_en,
            unidade,
            ordem_exibicao,
            ativo
        )
        VALUES (
            :codigo_core,
            :tipo_demonstracao,
            :nome_pt,
            :nome_en,
            :unidade,
            :ordem_exibicao,
            TRUE
        )
        ON CONFLICT (
            tipo_demonstracao,
            codigo
        )
        DO UPDATE SET
            nome_pt = EXCLUDED.nome_pt,
            nome_en = EXCLUDED.nome_en,
            unidade = EXCLUDED.unidade,
            ordem_exibicao = EXCLUDED.ordem_exibicao,
            ativo = TRUE
        """
    )

    conexao.execute(
        comando,
        registros,
    )

def carregar_importacao(
    conexao,
    dados_core: pd.DataFrame,
    empresa_id: int,
) -> int:
    fontes_encontradas = (
        dados_core[
            [
                "tipo_demonstracao",
                "arquivo_origem",
                "aba_origem",
            ]
        ]
        .drop_duplicates()
    )

    if len(fontes_encontradas) != 1:
        raise ValueError(
            "A carga deve possuir apenas uma origem."
        )

    fonte = fontes_encontradas.iloc[0]

    comando = text(
        """
        INSERT INTO core.importacoes (
            empresa_id,
            tipo_demonstracao,
            arquivo_origem,
            aba_origem
        )
        VALUES (
            :empresa_id,
            :tipo_demonstracao,
            :arquivo_origem,
            :aba_origem
        )
        ON CONFLICT (
            empresa_id,
            tipo_demonstracao,
            arquivo_origem,
            aba_origem
        )
        DO UPDATE SET
            importado_em = CURRENT_TIMESTAMP
        RETURNING id
        """
    )

    importacao_id = conexao.execute(
        comando,
        {
            "empresa_id": empresa_id,
            "tipo_demonstracao": (
                fonte["tipo_demonstracao"]
            ),
            "arquivo_origem": (
                fonte["arquivo_origem"]
            ),
            "aba_origem": (
                fonte["aba_origem"]
            ),
        },
    ).scalar_one()

    return importacao_id


def adicionar_ids_core(
    conexao,
    dados_core: pd.DataFrame,
    empresa_id: int,
    importacao_id: int,
) -> pd.DataFrame:
    consulta_contas = text(
        """
        SELECT
            id AS conta_financeira_id,
            codigo AS codigo_core,
            tipo_demonstracao
        FROM core.contas_financeiras
        WHERE ativo = TRUE
        """
    )

    contas_com_ids = pd.read_sql_query(
        consulta_contas,
        conexao,
    )

    consulta_periodos = text(
        """
        SELECT
            id AS periodo_id,
            ano,
            trimestre,
            periodo
        FROM core.periodos
        """
    )

    periodos_com_ids = pd.read_sql_query(
        consulta_periodos,
        conexao,
    )

    dados_com_ids = dados_core.merge(
        contas_com_ids,
        on=[
            "tipo_demonstracao",
            "codigo_core",
        ],
        how="left",
        validate="many_to_one",
    )

    dados_com_ids = dados_com_ids.merge(
        periodos_com_ids,
        on=[
            "ano",
            "trimestre",
            "periodo",
        ],
        how="left",
        validate="many_to_one",
    )

    dados_com_ids["empresa_id"] = empresa_id
    dados_com_ids["importacao_id"] = importacao_id

    colunas_ids = [
        "empresa_id",
        "conta_financeira_id",
        "periodo_id",
        "importacao_id",
    ]

    ids_ausentes = (
        dados_com_ids[colunas_ids]
        .isna()
        .sum()
    )

    if ids_ausentes.sum() > 0:
        raise ValueError(
            "Não foi possível localizar todos os IDs:\n"
            f"{ids_ausentes}"
        )

    if len(dados_com_ids) != len(dados_core):
        raise ValueError(
            "A associação dos IDs alterou a "
            "quantidade de resultados."
        )

    return dados_com_ids

def carregar_resultados_financeiros(
    conexao,
    dados_com_ids: pd.DataFrame,
) -> None:
    colunas_resultados = [
        "empresa_id",
        "conta_financeira_id",
        "periodo_id",
        "importacao_id",
        "valor",
    ]

    chave_resultado = [
        "empresa_id",
        "conta_financeira_id",
        "periodo_id",
    ]

    quantidade_duplicados = (
        dados_com_ids
        .duplicated(subset=chave_resultado)
        .sum()
    )

    if quantidade_duplicados > 0:
        raise ValueError(
            "Foram encontrados "
            f"{quantidade_duplicados} resultados duplicados."
        )

    registros = (
        dados_com_ids[colunas_resultados]
        .to_dict(orient="records")
    )

    comando = text(
        """
        INSERT INTO core.resultados_financeiros (
            empresa_id,
            conta_financeira_id,
            periodo_id,
            importacao_id,
            valor
        )
        VALUES (
            :empresa_id,
            :conta_financeira_id,
            :periodo_id,
            :importacao_id,
            :valor
        )
        ON CONFLICT (
            empresa_id,
            conta_financeira_id,
            periodo_id
        )
        DO UPDATE SET
            valor = EXCLUDED.valor,
            importacao_id = EXCLUDED.importacao_id
        """
    )

    conexao.execute(
        comando,
        registros,
    )
def main():
    engine = criar_engine()

    with engine.begin() as conexao:
        mapeamento = ler_mapeamento()

        dados_staging = ler_dados_staging(
            conexao
        )

        dados_core = preparar_dados_core(
            dados_staging,
            mapeamento,
        )

        empresa_id = carregar_empresa(
            conexao,
            dados_core,
        )

        carregar_periodos(
            conexao,
            dados_core,
        )

        carregar_contas_financeiras(
            conexao,
            dados_core,
        )

        importacao_id = carregar_importacao(
            conexao,
            dados_core,
            empresa_id,
        )

        dados_com_ids = adicionar_ids_core(
            conexao,
            dados_core,
            empresa_id,
            importacao_id,
        )

        carregar_resultados_financeiros(
            conexao,
            dados_com_ids,
        )

        total_core = conexao.execute(
            text(
                """
                SELECT COUNT(*)
                FROM core.resultados_financeiros
                WHERE empresa_id = :empresa_id
                """
            ),
            {
                "empresa_id": empresa_id,
            },
        ).scalar_one()

        if total_core != len(dados_com_ids):
            raise ValueError(
                "A quantidade gravada no core "
                "é diferente da quantidade esperada."
            )

    print("Carga do core finalizada com sucesso.")

    print(
        f"Empresa ID: {empresa_id}"
    )

    print(
        f"Importação ID: {importacao_id}"
    )

    print(
        f"Resultados gravados: {total_core}"
    )


if __name__ == "__main__":
    main()