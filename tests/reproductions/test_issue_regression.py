from frete.calculator import calcular_frete


def test_calcular_frete_com_dimensao_nula():
    """Reproduz falha quando uma dimensão possui valor nulo."""
    dimensoes = {"altura": 20, "largura": 15, "profundidade": None}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 2.0


def test_calcular_frete_com_dimensoes_ausentes():
    """Reproduz falha quando dimensões estão ausentes."""
    dimensoes = {"altura": 20, "largura": 15}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 2.0


def test_calcular_frete_com_dicionario_vazio():
    """Reproduz cálculo com dicionário de dimensões vazio."""
    dimensoes = {}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 2.0


def test_calcular_frete_com_tipos_invalidos():
    """Reproduz cálculo quando dimensões contêm tipos inválidos ou strings não numéricas."""
    dimensoes = {"altura": "invalid", "largura": 15, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 2.0

