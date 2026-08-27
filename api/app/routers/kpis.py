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
from app.schemas.kpi import KpiTrimestral
from app.services import kpi_service


router = APIRouter(
    prefix="/empresas",
    tags=["Indicadores"],
)


@router.get(
    "/{ticker}/kpis",
    response_model=KpiTrimestral,
    summary="Consulta os KPIs de um trimestre",
)
def obter_kpis(
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
) -> KpiTrimestral:
    kpi = kpi_service.obter_kpi_trimestral(
        conexao,
        ticker,
        periodo,
    )

    if kpi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Indicadores não encontrados para "
                f"{ticker.upper()} no período "
                f"{periodo.upper()}."
            ),
        )

    return kpi


@router.get(
    "/{ticker}/kpis/historico",
    response_model=list[KpiTrimestral],
    summary="Lista o histórico trimestral de KPIs",
)
def listar_historico_kpis(
    ticker: Annotated[
        str,
        Path(
            min_length=4,
            max_length=10,
            pattern=r"^[A-Za-z0-9]+$",
            examples=["AZZA3"],
        ),
    ],
    conexao: Annotated[
        Connection,
        Depends(obter_conexao),
    ],
) -> list[KpiTrimestral]:
    historico = (
        kpi_service
        .listar_historico_trimestral(
            conexao,
            ticker,
        )
    )

    if not historico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Histórico não encontrado para "
                f"{ticker.upper()}."
            ),
        )

    return historico