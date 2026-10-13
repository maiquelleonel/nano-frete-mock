import pytest
from httpx import ASGITransport, AsyncClient

from frete.calculator import calcular_frete
from frete.main import app


def test_calcular_frete_com_dimensoes_nulas():
    # Reproducao exata do incidente 372ddf47dc: TypeError int * NoneType
    dimensoes = {"altura": 20, "largura": None, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["cep_destino"] == "01001-000"
    assert resultado["peso_taxavel"] == 2.0


def test_calcular_frete_com_chaves_ausentes():
    dimensoes = {"altura": 20}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["cep_destino"] == "01001-000"
    assert resultado["peso_taxavel"] == 2.0


def test_calcular_frete_com_dimensoes_vazias():
    resultado = calcular_frete({}, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["cep_destino"] == "01001-000"
    assert resultado["peso_taxavel"] == 2.0


@pytest.mark.anyio
async def test_endpoint_calcular_frete_com_dimensoes_nulas():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/frete/calcular",
            json={"dimensoes": {"altura": 20, "largura": None, "profundidade": 10}, "peso_kg": 2.0},
        )
    assert response.status_code == 200
    dados = response.json()
    assert dados["cep_destino"] == "01001-000"
    assert dados["peso_taxavel"] == 2.0
    assert dados["valor_frete"] > 0
