from frete.calculator import calcular_frete


def test_calcular_frete_com_dimensoes_nulas():
    """Reproduz falha com dimensões contendo valores None (TypeError: int * NoneType)."""
    dimensoes = {"altura": 20, "largura": None, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 2.0
    assert resultado["cep_destino"] == "01001-000"


def test_calcular_frete_com_campos_ausentes():
    """Reproduz cenário com chaves ausentes no dicionário de dimensões."""
    dimensoes = {"altura": 15}
    resultado = calcular_frete(dimensoes, peso_kg=3.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 3.0


def test_calcular_frete_com_dimensoes_none():
    """Reproduz cenário quando dimensoes é None."""
    resultado = calcular_frete(None, peso_kg=1.5, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 1.5


def test_calcular_frete_com_tipos_invalidos():
    """Reproduz cenário com dimensões com valores não numéricos."""
    dimensoes = {"altura": "invalido", "largura": None, "profundidade": 10}
    resultado = calcular_frete(dimensoes, peso_kg=2.0, cep_destino="01001-000")
    assert resultado["valor_frete"] > 0
    assert resultado["peso_taxavel"] == 2.0
