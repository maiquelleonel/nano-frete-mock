def _converter_valor_positivo(valor) -> float:
    try:
        val = float(valor) if valor is not None else 0.0
        return max(0.0, val)
    except (ValueError, TypeError):
        return 0.0


def calcular_frete(dimensoes: dict, peso_kg: float, cep_destino: str) -> dict:
    """Calcula o valor do frete e peso cubado."""
    dados_dimensoes = dimensoes if isinstance(dimensoes, dict) else {}

    altura = _converter_valor_positivo(dados_dimensoes.get("altura"))
    largura = _converter_valor_positivo(dados_dimensoes.get("largura"))
    profundidade = _converter_valor_positivo(dados_dimensoes.get("profundidade"))

    volume_m3 = (altura * largura * profundidade) / 6000.0

    peso_seguro = _converter_valor_positivo(peso_kg)
    peso_taxavel = max(peso_seguro, volume_m3)
    valor_base = 15.0 + (peso_taxavel * 2.5)

    return {
        "cep_destino": cep_destino,
        "peso_taxavel": round(peso_taxavel, 2),
        "valor_frete": round(valor_base, 2),
    }
