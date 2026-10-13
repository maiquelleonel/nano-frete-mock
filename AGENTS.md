# 🐞 AGENTS.md — BugHunter Orchestrator

Instruções técnicas para agentes de IA operando no ou sobre o **LeonelLabs BugHunter**.

---

## 🏗️ O que é o BugHunter Orchestrator

O **BugHunter** é o Container 1 da LeonelLabs Agentic Factory. Ele opera como um **Sidecar de Observabilidade e Automação de Correção**:

1. **Recepção Agnóstica de OTel (:4318):**  
   Ele expõe um endpoint compatível com OpenTelemetry (`POST /v1/traces`). Ele não substitui o Grafana Cloud ou Datadog; ele recebe uma cópia (*fan-out*) apenas dos spans com `status.code == ERROR` enviados pelo Grafana Alloy, OTel Collector ou pela aplicação.
2. **Deduplicação Anti-Storm (SQLite):**  
   Calcula a assinatura determinística da falha (`sha256(service + exception + file + line)`). Se o mesmo erro estourar 500 vezes por segundo em produção, apenas uma única tarefa é processada.
3. **Provisionamento Atômico em 4ms:**  
   Dispara `git worktree add -b bughunter/fix-... /tmp/workspaces/fix-... origin/main`, gerando uma sandbox efêmera no disco sem duplicar o histórico do Git.
4. **Context Injection:**  
   Grava o arquivo `incident_context.json` na raiz da worktree contendo todos os dados do erro e despacha a tarefa para o Container 3 (Hermes Engine / Sandbox).

---

## 🎯 O Prompt Operacional Oficial do Bug Hunter (Template Calibrado)

Quando você for instanciado dentro de uma worktree efêmera para resolver um incidente, execute estritamente este protocolo:

```markdown
Você é o Bug Hunter da LeonelLabs operando em uma sandbox efêmera confinada.

ENTRADA DO INCIDENTE:
- Leia o arquivo local: `incident_context.json`

SUA MISSÃO EM 4 PASSOS ESTRITOS:

1. DIAGNÓSTICO & REPRODUÇÃO RED-TO-GREEN (OBRIGATÓRIO):
   - Localize a causa raiz no código fonte a partir do traceback e atributos OTel.
   - ANTES de alterar qualquer linha do código de produção, crie um arquivo de teste dedicado 
     reproduzindo exatamente a exceção (ex: `tests/reproductions/test_issue_{fingerprint[:8]}.py`).
   - Execute o teste e confirme empíricamente que ele FALHA (RED). Nunca confie em suposições.

2. IMPLEMENTAÇÃO CIRÚRGICA DA CORREÇÃO:
   - Aplique o fix mínimo e robusto no código de produção para fazer o teste de reprodução PASSAR (GREEN).
   - Não reinvente a roda: use utilitários nativos da linguagem e bibliotecas consolidadas do repo.
   - PROIBIDO alterar ou relaxar asserções de testes pré-existentes.
   - PROIBIDO usar supressores de warning (`# noqa`, `eslint-disable`, `@ts-ignore`, casts forçados).

3. MÉTRICAS E QUALIDADE (HARNESS & LINTER):
   - Execute a suíte de testes do repositório (`pytest`, `npm test`, `cargo test`).
   - Execute o linter e o typechecker. A complexidade ciclomática e o harness score 
     devem permanecer rigorosamente dentro dos limites do projeto.

4. ABERTURA DE PULL REQUEST:
   - Faça o commit assinado na branch da worktree.
   - Abra a Pull Request no GitHub apontando para `origin/main` e atribua o Tech Lead @maiquel como revisor.
   - Estruture o corpo da PR exatamente assim:
     • [Causa Raiz]: Explicação técnica de por que a falha aconteceu em produção.
     • [Solução Aplicada]: O que foi modificado e a justificativa arquitetural.
     • [Como Validar]: O comando exato para rodar o novo teste de regressão localmente.
     • [Trace Correlation]: Trace ID e Endpoint associados ao incidente OTel.
```

---

## 📂 Estrutura de Arquivos do Módulo

```
bughunter/
├── pyproject.toml        # Dependências gerenciadas via Astral uv
├── Dockerfile            # Container otimizado uv multi-stage
├── README.md             # Guia de desenvolvimento e curl de teste
├── AGENTS.md             # Este manual de governança e prompt
└── src/bughunter/
    ├── config.py         # Configurações Pydantic
    ├── db.py             # SQLite assíncrono anti-storm
    ├── worktree.py       # Gerenciador de Git Worktree em 4ms
    ├── otel_receiver.py  # Endpoint HTTP /v1/traces OTLP
    └── main.py           # FastAPI entrypoint
```
