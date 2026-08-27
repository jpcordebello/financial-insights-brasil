from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    status,
)
from sqlalchemy.engine import Connection

from app.core.database import obter_conexao
from app.schemas.dre import ItemDre
from app.services import dre_service


router = APIRouter(
    prefix="/empresas",
    tags=["DRE"],
)


@router.get(
    "/{ticker}/dre",
    response_model=list[ItemDre],
    summary="Consulta a DRE de um trimestre",
)
def listar_dre(
    ticker: Annotated[
        str,
        Path(
            min_length=4,
            max_length=10,
            pattern=r"^[A-Za-z0-9]+$",
            examples=["AZZA3"],
        ),
    ],
    periodo: Annotated[
        str,
        Query(
            pattern=r"^[1-4][Qq][0-9]{2}$",
            examples=["2Q26"],
        ),
    ],
    conexao: Annotated[
        Connection,
        Depends(obter_conexao),
    ],
) -> list[ItemDre]:
    itens = (
        dre_service
        .listar_dre_por_periodo(
            conexao,
            ticker,
            periodo,
        )
    )

    if not itens:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "DRE não encontrada para "
                f"{ticker.upper()} no período "
                f"{periodo.upper()}."
            ),
        )

    return itens