from sqlalchemy.engine import Connection

from app.repositories import kpi_repository
from app.schemas.kpi import KpiTrimestral


def obter_kpi_trimestral(
    conexao: Connection,
    ticker: str,
    periodo: str,
) -> KpiTrimestral | None:
    ticker_normalizado = (
        ticker
        .strip()
        .upper()
    )

    periodo_normalizado = (
        periodo
        .strip()
        .upper()
    )

    registro = (
        kpi_repository
        .buscar_por_empresa_e_periodo(
            conexao,
            ticker_normalizado,
            periodo_normalizado,
        )
    )

    if registro is None:
        return None

    return KpiTrimestral.model_validate(
        registro
    )

def listar_historico_trimestral(
    conexao: Connection,
    ticker: str,
) -> list[KpiTrimestral]:
    ticker_normalizado = (
        ticker
        .strip()
        .upper()
    )

    registros = (
        kpi_repository
        .listar_historico_por_empresa(
            conexao,
            ticker_normalizado,
        )
    )

    return [
        KpiTrimestral.model_validate(
            registro
        )
        for registro in registros
    ]