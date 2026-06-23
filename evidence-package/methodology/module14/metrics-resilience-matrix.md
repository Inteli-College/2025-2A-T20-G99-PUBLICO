# Matriz de Métricas e Resiliência — Módulo 14

Base para as Sprints 4–5 (definição de métricas, protocolos PQC e critérios de validação).

## 1. Estrutura de medição
- **Domínios**: Inventário, Automação, Compatibilidade, Observabilidade, Resiliência, Custo.
- **Fontes**: CBOM Kit, pipelines CI/CD, service mesh, KMS/Secrets Manager, SIEM, testes de carga.
- **Frequência**: diária (inventário), por deploy (automação), contínua (observabilidade), mensal (custo).

## 2. Métricas principais

| ID | Métrica | Definição | Meta Sprint 4 | Fonte |
| --- | --- | --- | --- | --- |
| INV-01 | Cobertura CBOM por serviço | `serviços inventariados ÷ serviços ativos` | ≥ 95% | CBOM Kit export |
| INV-02 | Precisão de detecção | `1 − (FP ÷ achados)` | ≥ 97% | Validação amostral + gateway |
| GOV-01 | Mudanças com CBOM before/after | % swaps com manifesto anexado | 100% | Git/CI |
| SWP-01 | Tempo discover→swap | `T(swap) − T(discover)` | ≤ 48h (staging) | Pipelines |
| HYB-01 | Handshake híbrido sucesso | `handshakes_ok ÷ total` | > 99% canário | Mesh/APM |
| HYB-02 | Overhead latência | `lat_híbrido − lat_clássico` | ≤ 5% por serviço | Load tests |
| KLC-01 | Rotação automatizada | % segredos/certs com rotação | ≥ 90% | KMS logs |
| OBS-01 | Cobertura métricas TLS/KEM | % serviços com métricas ativas | 100% | Observability stack |
| OBS-02 | MTTD de política | Tempo para detectar violação | ≤ 5 min | SIEM |
| RES-01 | MTTR criptográfico | Tempo para recuperar incidente | ≤ 4h (canário) | ITSM |
| RES-02 | Taxa de rollback seguro | `rollbacks_ok ÷ total` | ≥ 99% | Automation logs |
| COST-01 | Custo incremental PQC | Δ custo por 1M reqs | ≤ +15% | FinOps |

## 3. Protocolos de migração PQC
1. **Inventariar**: executar CBOM diário; verificar se novas dependências aparecem fora de política.
2. **Planejar**: selecionar serviços com alto risco (RSA-2048/ECDH-P256) e criar PRs com perfis híbridos (Kyber-768 + TLS 1.3).
3. **Executar**: aplicar mudança em canário com feature flag; medir HYB-01/02 durante 24h.
4. **Validar**: anexar CBOM before/after e relatório de telemetria; atualizar tabela de ações (via `cbom_gateway.py`).
5. **Auditar**: registrar mudança em ITSM com evidências; atualizar indicadores GOV/OBS/RES.

## 4. Planos de resiliência
- **Rollback rápido**: cada automação deve incluir plano documentado e teste semestral; alvo RES-02 ≥ 99%.
- **Chaos criptográfico**: injetar falhas (latência, caducidade de certificado, indisponibilidade KMS) mensalmente; registrar evidências.
- **Detecção harvest-now**: monitorar padrões de download/handshake e alertar SecOps; usar `OBS-02` como gatilho para playbooks de resposta.

## 5. Relato e governança
- Os resultados das métricas devem alimentar o relatório da Sprint 4 e o artefato final do módulo.
- Variáveis e metas podem ser calibradas após cada sprint; registrar revisões nesta matriz.

> Esta matriz complementa a tabela de critérios de criptoagilidade (`docs/governance/...`) adaptando-a para as fases de design e validação do Módulo 14.
