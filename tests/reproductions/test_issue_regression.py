from frete.calculator import calcular_frete


def test_calcular_frete_com_dimensao_nula():
    """Reproduz o erro reportado no incident_context.json (TypeError: unsupported operand type(s) for *: 'int' and 'NoneType')."""
    dimensoes = {"altura": 20, "largura": None, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["cep_destino"] == "01001-000"


def test_calcular_frete_com_dimensoes_ausentes():
    """Valida resiliência contra chaves de dimensões ausentes."""
    dimensoes = {"altura": 20}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["cep_destino"] == "01001-000"


def test_calcular_frete_com_dimensoes_vazias():
    """Valida cálculo com dicionário de dimensões vazio."""
    dimensoes = {}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["cep_destino"] == "01001-000"


def test_calcular_frete_com_tipos_invalidos_e_nulos():
    """Valida tratamento defensivo de tipos inválidos e valores nulos gerais."""
    dimensoes = {"altura": "invalid", "largura": None, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=None, cep_destino="01001-000")
    assert resultado["valor_frete"] >= 15.0
    assert resultado["peso_taxavel"] == 0.0
    assert resultado["cep_destino"] == "01001-000"
