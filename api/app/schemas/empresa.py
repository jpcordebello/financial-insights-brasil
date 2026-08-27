from pydantic import BaseModel


class EmpresaResumo(BaseModel):
    id: int
    nome: str
    ticker: str | None
    setor: str | None