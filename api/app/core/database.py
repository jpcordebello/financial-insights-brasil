from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Connection, Engine

from .config import obter_configuracoes


@lru_cache
def obter_engine() -> Engine:
    configuracoes = obter_configuracoes()

    url_banco = URL.create(
        drivername="postgresql+psycopg",
        username=configuracoes.db_user,
        password=configuracoes.db_password,
        host=configuracoes.db_host,
        port=configuracoes.db_port,
        database=configuracoes.db_name,
    )

    return create_engine(
        url_banco,
        pool_pre_ping=True,
    )


def obter_conexao() -> Generator[
    Connection,
    None,
    None,
]:
    engine = obter_engine()

    with engine.connect() as conexao:
        yield conexao