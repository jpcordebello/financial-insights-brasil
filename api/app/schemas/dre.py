from pydantic import BaseModel


class ItemDre(BaseModel):
    empresa: str
    ticker: str
    periodo: str

    codigo_conta: str
    conta: str
    conta_en: str | None

    unidade: str
    ordem_exibicao: int
    valor: float