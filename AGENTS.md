# 📦 AGENTS.md — Nano Frete Service
## Diretrizes de Engenharia e Governança para Agentes de IA

Este documento define as regras de desenvolvimento, arquitetura e testes para agentes de IA operando no repositório **Nano Frete Service**.

---

## 🏛️ 1. Visão Geral do Projeto
Micro-serviço em FastAPI responsável pelo cálculo de precificação de frete e cubagem volumétrica para e-commerce.

* **Stack:** Python 3.13+, Astral uv, FastAPI, Pytest, Ruff.
* **Layout:** src/frete/ (código de produção), tests/ (suíte de testes).

---

## ⚡ 2. Comandos Operacionais

* **Executar Testes:** uv run pytest
* **Executar Teste Isolado:** uv run pytest tests/test_calculator.py -v
* **Verificar Linters:** uv run ruff check .
* **Subir API Local:** uv run uvicorn frete.main:app --port 8000

---

## 🛡️ 3. Protocolo de Correção de Bugs (Red-to-Green)

1. **Reprodução Obrigatória (RED):**
   * Antes de alterar qualquer linha em src/frete/, crie um teste unitário reproduzindo o cenário do erro em tests/ (ex: tests/reproductions/test_issue_regression.py).
   * Execute o teste e confirme empiricamente que ele falha.
2. **Correção Cirúrgica (GREEN):**
   * Aplique a correção mínima no código fonte (ex: tratamento defensivo de dimensões nulas, tipos inválidos ou campos ausentes).
   * Confirme que o novo teste passa e que testes legados permanecem verdes.
3. **Padrões de Código:**
   * Proibido usar supressores de warning (# noqa).
   * Proibido alterar asserções de testes pré-existentes para forçar aprovação.
