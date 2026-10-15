from frete.calculator import calcular_frete


def test_calcular_frete_com_dimensoes_ausentes():
    """Reproduz falha quando uma dimensão está ausente (ex: largura ausente)."""
    dimensoes = {"altura": 20, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 2.0


def test_calcular_frete_com_dimensoes_nulas():
    """Reproduz falha quando uma dimensão é explicitamente None."""
    dimensoes = {"altura": 20, "largura": None, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 2.0
