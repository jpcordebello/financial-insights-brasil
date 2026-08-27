from sqlalchemy import text
from sqlalchemy.engine import Connection


def listar_empresas(
    conexao: Connection,
) -> list[dict[str, object]]:
    consulta = text(
        """
        SELECT
            id,
            nome,
            ticker,
            setor
        FROM core.empresas
        ORDER BY nome
        """
    )

    resultado = conexao.execute(
        consulta
    )

    return [
        dict(linha)
        for linha in resultado.mappings().all()
    ]