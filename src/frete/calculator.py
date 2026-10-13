def _extrair_dimensao(dimensoes: dict | None, chave: str) -> float:
    """Extrai e valida dimensões garantindo valor numérico não-negativo."""
    if not isinstance(dimensoes, dict):
        return 0.0
    valor = dimensoes.get(chave)
    if valor is None:
        return 0.0
    try:
        val = float(valor)
        return max(0.0, val)
    except (ValueError, TypeError):
        return 0.0


def calcular_frete(dimensoes: dict, peso_kg: float, cep_destino: str) -> dict:
    """Calcula o valor do frete e peso cubado."""
    altura = _extrair_dimensao(dimensoes, "altura")
    largura = _extrair_dimensao(dimensoes, "largura")
    profundidade = _extrair_dimensao(dimensoes, "profundidade")

    volume_m3 = (altura * largura * profundidade) / 6000.0

    peso_taxavel = max(float(peso_kg or 0.0), volume_m3)
    valor_base = 15.0 + (peso_taxavel * 2.5)

    return {
        "cep_destino": cep_destino,
        "peso_taxavel": round(peso_taxavel, 2),
        "valor_frete": round(valor_base, 2),
    }
