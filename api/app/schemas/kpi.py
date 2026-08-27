from pydantic import BaseModel


class KpiTrimestral(BaseModel):
    empresa_id: int
    empresa: str
    ticker: str
    setor: str | None

    ano: int
    trimestre: int
    periodo: str

    receita_liquida: float
    margem_bruta: float

    ebitda: float
    margem_ebitda: float

    lucro_liquido: float
    margem_liquida: float