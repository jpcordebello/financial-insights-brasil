from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import obter_configuracoes
from app.routers.dre import (
    router as dre_router,
)
from app.routers.empresas import (
    router as empresas_router,
)
from app.routers.kpis import (
    router as kpis_router,
)


configuracoes = obter_configuracoes()

app = FastAPI(
    title="Financial Insights Brasil API",
    description=(
        "API para consulta de indicadores "
        "financeiros de empresas listadas."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        configuracoes.lista_cors_origins
    ),
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(
    empresas_router,
    prefix="/api/v1",
)

app.include_router(
    kpis_router,
    prefix="/api/v1",
)

app.include_router(
    dre_router,
    prefix="/api/v1",
)


@app.get(
    "/health",
    tags=["Health"],
)
def verificar_saude() -> dict[str, str]:
    return {
        "status": "ok",
        "servico": "financial-insights-api",
    }