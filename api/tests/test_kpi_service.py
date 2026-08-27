from unittest.mock import MagicMock

import pytest
from sqlalchemy.engine import Connection

from app.repositories import kpi_repository
from app.services import kpi_service


def test_deve_normalizar_ticker_e_periodo(
    monkeypatch: pytest.MonkeyPatch,
):
    conexao = MagicMock(
        spec=Connection
    )

    def buscar_simulado(
        conexao_recebida,
        ticker,
        periodo,
    ):
        assert conexao_recebida is conexao
        assert ticker == "AZZA3"
        assert periodo == "2Q26"

        return {
            "empresa_id": 1,
            "empresa": "Azzas 2154",
            "ticker": "AZZA3",
            "setor": "Consumo Cíclico",
            "ano": 2026,
            "trimestre": 2,
            "periodo": "2Q26",
            "receita_liquida": 2664.1,
            "margem_bruta": 0.547,
            "ebitda": 279.2,
            "margem_ebitda": 0.105,
            "lucro_liquido": 29.8,
            "margem_liquida": 0.011,
        }

    monkeypatch.setattr(
        kpi_repository,
        "buscar_por_empresa_e_periodo",
        buscar_simulado,
    )

    resultado = (
        kpi_service.obter_kpi_trimestral(
            conexao,
            " azza3 ",
            " 2q26 ",
        )
    )

    assert resultado is not None
    assert resultado.ticker == "AZZA3"
    assert resultado.periodo == "2Q26"
    assert resultado.receita_liquida == 2664.1


def test_deve_retornar_none_quando_nao_encontrar(
    monkeypatch: pytest.MonkeyPatch,
):
    conexao = MagicMock(
        spec=Connection
    )

    monkeypatch.setattr(
        kpi_repository,
        "buscar_por_empresa_e_periodo",
        lambda conexao, ticker, periodo: None,
    )

    resultado = (
        kpi_service.obter_kpi_trimestral(
            conexao,
            "AZZA3",
            "4Q99",
        )
    )

    assert resultado is None