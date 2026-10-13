def calcular_frete(dimensoes: dict, peso_kg: float, cep_destino: str) -> dict:
    """Calcula o valor do frete e peso cubado."""
    altura = dimensoes.get("altura")
    largura = dimensoes.get("largura")
    profundidade = dimensoes.get("profundidade")

    # Bug de produção: falta de validação de valores ausentes ou nulos
    volume_m3 = (altura * largura * profundidade) / 6000.0

    peso_taxavel = max(peso_kg, volume_m3)
    valor_base = 15.0 + (peso_taxavel * 2.5)

    return {
        "cep_destino": cep_destino,
        "peso_taxavel": round(peso_taxavel, 2),
        "valor_frete": round(valor_base, 2),
    }
