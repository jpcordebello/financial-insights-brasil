from sqlalchemy import text
from sqlalchemy.engine import Connection


def listar_por_empresa_e_periodo(
    conexao: Connection,
    ticker: str,
    periodo: str,
) -> list[dict[str, object]]:
    consulta = text(
        """
        SELECT
            empresa,
            ticker,
            periodo,
            codigo_conta,
            conta,
            conta_en,
            unidade,
            ordem_exibicao,
            valor
        FROM analytics.vw_resultados_financeiros
        WHERE
            ticker = :ticker
            AND periodo = :periodo
            AND tipo_demonstracao = 'DRE Pro Forma'
        ORDER BY ordem_exibicao
        """
    )

    resultado = conexao.execute(
        consulta,
        {
            "ticker": ticker,
            "periodo": periodo,
        },
    )

    return [
        dict(linha)
        for linha in resultado.mappings().all()
    ]