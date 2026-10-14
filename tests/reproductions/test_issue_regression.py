from frete.calculator import calcular_frete


def test_calcular_frete_com_dimensao_nula():
    # Reproduz o erro do incidente: TypeError: unsupported operand type(s) for *: 'int' and 'NoneType'
    dimensoes = {"altura": 20, "largura": None, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["cep_destino"] == "01001-000"
    assert resultado["peso_taxavel"] == 2.0
    assert resultado["valor_frete"] > 0


def test_calcular_frete_com_campos_ausentes():
    dimensoes = {"altura": 20}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["cep_destino"] == "01001-000"
    assert resultado["peso_taxavel"] == 2.0
    assert resultado["valor_frete"] > 0


def test_calcular_frete_dimensoes_vazias_ou_nulas():
    resultado_vazio = calcular_frete({}, peso_kg=2.0, cep_destino="01001-000")
    assert resultado_vazio["valor_frete"] > 0

    resultado_none = calcular_frete(None, peso_kg=2.0, cep_destino="01001-000")
    assert resultado_none["valor_frete"] > 0


def test_calcular_frete_dimensoes_tipos_invalidos():
    dimensoes = {"altura": "invalido", "largura": -10, "profundidade": "10"}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["cep_destino"] == "01001-000"
