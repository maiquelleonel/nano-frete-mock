def _obter_dimensao(dimensoes: dict | None, chave: str) -> float:
    if not isinstance(dimensoes, dict):
        return 0.0
    valor = dimensoes.get(chave)
    if valor is None:
        return 0.0
    try:
        val = float(valor)
        return val if val > 0 else 0.0
    except (ValueError, TypeError):
        return 0.0


def calcular_frete(dimensoes: dict | None, peso_kg: float, cep_destino: str) -> dict:
    """Calcula o valor do frete e peso cubado."""
    altura = _obter_dimensao(dimensoes, "altura")
    largura = _obter_dimensao(dimensoes, "largura")
    profundidade = _obter_dimensao(dimensoes, "profundidade")

    volume_m3 = (altura * largura * profundidade) / 6000.0

    peso_taxavel = max(float(peso_kg or 0.0), volume_m3)
    valor_base = 15.0 + (peso_taxavel * 2.5)

    return {
        "cep_destino": cep_destino,
        "peso_taxavel": round(peso_taxavel, 2),
        "valor_frete": round(valor_base, 2),
    }
