import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine


PASTA_RAIZ = Path(__file__).resolve().parent.parent


def criar_engine():
    load_dotenv(PASTA_RAIZ / ".env")

    configuracoes = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_NAME"),
        "username": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    configuracoes_faltantes = [
        nome
        for nome, valor in configuracoes.items()
        if not valor
    ]

    if configuracoes_faltantes:
        raise ValueError(
            "Configurações ausentes no .env: "
            + ", ".join(configuracoes_faltantes)
        )

    url_conexao = URL.create(
        drivername="postgresql+psycopg",
        host=configuracoes["host"],
        port=int(configuracoes["port"]),
        database=configuracoes["database"],
        username=configuracoes["username"],
        password=configuracoes["password"],
    )

    return create_engine(url_conexao)