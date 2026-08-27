from fastapi.testclient import TestClient

from app.main import app


cliente = TestClient(app)


def test_health_deve_retornar_status_ok():
    resposta = cliente.get(
        "/health"
    )

    assert resposta.status_code == 200

    assert resposta.json() == {
        "status": "ok",
        "servico": "financial-insights-api",
    }