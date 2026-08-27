from sqlalchemy.engine import Connection

from app.repositories import dre_repository
from app.schemas.dre import ItemDre


def listar_dre_por_periodo(
    conexao: Connection,
    ticker: str,
    periodo: str,
) -> list[ItemDre]:
    ticker_normalizado = (
        ticker
        .strip()
        .upper()
    )

    periodo_normalizado = (
        periodo
        .strip()
 .strip()
        .upper()
    )

    registros = (
        dre_repository
        .listar_por_empresa_e_periodo(
            conexao,
            ticker_normalizado,
            periodo_normalizado,
        )
    )

    return [
        ItemDre.model_validate(
            registro
        )
        for registro in registros
    ]