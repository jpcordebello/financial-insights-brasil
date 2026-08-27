from sqlalchemy import text
from sqlalchemy.engine import Connection


def buscar_por_empresa_e_periodo(
    conexao: Connection,
    ticker: str,
    periodo: str,
) -> dict[str, object] | None:
    consulta = text(
        """
        SELECT
            empresa_id,
            empresa,
            ticker,
            setor,
            ano,
            trimestre,
            periodo,
            receita_liquida,
            margem_bruta,
            ebitda,
            margem_ebitda,
            lucro_liquido,
            margem_liquida
        FROM analytics.vw_kpis_trimestrais
        WHERE
            ticker = :ticker
            AND periodo = :periodo
        """
    )

    resultado = conexao.execute(
        consulta,
        {
            "ticker": ticker,
            "periodo": periodo,
        },
    )

    linha = resultado.mappings().one_or_none()

    if linha is None:
        return None

    return dict(linha)

def listar_historico_por_empresa(
    conexao: Connection,
    ticker: str,
) -> list[dict[str, object]]:
    consulta = text(
        """
        SELECT
            empresa_id,
            empresa,
            ticker,
            setor,
            ano,
            trimestre,
            periodo,
            receita_liquida,
            margem_bruta,
            ebitda,
            margem_ebitda,
            lucro_liquido,
            margem_liquida
        FROM analytics.vw_kpis_trimestrais
        WHERE ticker = :ticker
        ORDER BY
            ano,
            trimestre
        """
    )

    resultado = conexao.execute(
        consulta,
        {
            "ticker": ticker,
        },
    )

    return [
        dict(linha)
        for linha in resultado.mappings().all()
    ]