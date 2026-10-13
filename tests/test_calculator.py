from frete.calculator import calcular_frete


def test_calcular_frete_valido():
    dimensoes = {"altura": 20, "largura": 15, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["cep_destino"] == "01001-000"
