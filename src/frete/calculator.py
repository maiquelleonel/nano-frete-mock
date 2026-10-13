def _tratar_dimensao(valor) -> float:
    if valor is None:
        return 0.0
    try:
        return max(0.0, float(valor))
    except (ValueError, TypeError):
        return 0.0


def calcular_frete(dimensoes: dict, peso_kg: float, cep_destino: str) -> dict:
    """Calcula o valor do frete e peso cubado."""
    dimensoes_dict = dimensoes if isinstance(dimensoes, dict) else {}

    altura = _tratar_dimensao(dimensoes_dict.get("altura"))
    largura = _tratar_dimensao(dimensoes_dict.get("largura"))
    profundidade = _tratar_dimensao(dimensoes_dict.get("profundidade"))

    volume_m3 = (altura * largura * profundidade) / 6000.0

    try:
        peso_efetivo = max(0.0, float(peso_kg)) if peso_kg is not None else 0.0
    except (ValueError, TypeError):
        peso_efetivo = 0.0

    peso_taxavel = max(peso_efetivo, volume_m3)
    valor_base = 15.0 + (peso_taxavel * 2.5)

    return {
        "cep_destino": cep_destino,
        "peso_taxavel": round(peso_taxavel, 2),
        "valor_frete": round(valor_base, 2),
    }
