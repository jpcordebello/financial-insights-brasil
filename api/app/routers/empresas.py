from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.engine import Connection

from app.core.database import obter_conexao
from app.repositories import empresa_repository
from app.schemas.empresa import EmpresaResumo


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"],
)


@router.get(
    "",
    response_model=list[EmpresaResumo],
    summary="Lista as empresas disponíveis",
)
def listar_empresas(
    conexao: Annotated[
        Connection,
        Depends(obter_conexao),
    ],
) -> list[EmpresaResumo]:
    registros = (
        empresa_repository.listar_empresas(
            conexao
        )
    )

    return [
        EmpresaResumo.model_validate(
            registro
        )
        for registro in registros
    ]