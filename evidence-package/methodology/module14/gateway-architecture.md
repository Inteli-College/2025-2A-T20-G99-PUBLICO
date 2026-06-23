# Gateway de Criptoagilidade — Especificação Sprint 2

Documento alinhado ao escopo do Módulo 14 (design macro + componentes funcionais).

## 1. Contexto e objetivos
- Atender ao requisito da Sprint 2: especificar o gateway e seus módulos de monitoramento e resposta (docs/module14/TAPI-Modulo14.txt:242-260).
- Integrar o IBM CBOM Kit como fonte primária de inventário.
- Operar sobre um ambiente three-tier híbrido (web/app/data) com suporte a perfis clássicos, híbridos e PQC.

## 2. Visão lógica

```
CBOM Kit → Ingest Service → Policy Engine → Automation Orchestrator
                                ↓                  ↓
                         Telemetry Correlator   Rollback/Chaos Engine
                                ↓
                         Observability & GRC Bus
```

### 2.1 Módulos
| Módulo | Responsabilidades | Entradas/Saídas |
| --- | --- | --- |
| **CBOM Ingest Service** | Importa manifestos JSON (API/CLI IBM CBOM Kit), valida schema, versiona por serviço/tier. | Entrada: `cbom/*.json`; Saída: fila `inventory.events` |
| **Policy Engine** | Avalia políticas declarativas (nível PQC, perfis híbridos, SLO criptográficos). | Entrada: inventory events + policies; Saída: `decision.events` |
| **Automation Orchestrator** | Gera PRs/playbooks (TLS, mTLS, assinaturas, KMS) e aciona pipelines (Argo/GitHub Actions). | Entrada: decision events; Saída: `automation.jobs` |
| **Telemetry Correlator** | Correlaciona CBOM com métricas TLS/KMS, detecta harvest-now, mede latência e erros. | Entrada: métricas OpenTelemetry + traffic taps; Saída: alertas e métricas |
| **Rollback & Chaos Engine** | Mantém planos de rollback e testes canário/caos para perfis PQC/híbridos. | Entrada: automations + testes agendados; Saída: `rollback.reports` |
| **Observability & GRC Bus** | Consolida evidências para SRE/GRC (dashboards, ITSM, auditoria NIST). | Entrada: de todos os módulos; Saída: painéis, artefatos assinados |

## 3. Fluxos principais
1. **Inventário → Decisão**: CBOM Kit exporta manifestos nightly → Ingest normaliza → Policy Engine identifica riscos (RSA-2048, ECDH-P256) → ações registradas (ver `code/cbom_gateway.py`).
2. **Decisão → Execução**: Automation Orchestrator abre PRs com perfis TLS 1.3 híbridos, rotação de certificados Dilithium, etc.
3. **Observabilidade → Resposta**: Telemetry Correlator monitora sucesso dos handshakes e dispara rollback automático via Chaos Engine em caso de regressão > 5%.

## 4. Visão física / implantação
- **Ambiente**: cluster Kubernetes multi-ambiente (dev/stage/prod-sim) com service mesh que oferece métricas TLS/KEM.
- **Persistência**: banco documental para CBOM versionado + storage de evidências (S3/Cloud Object Storage).
- **Filas/eventos**: Kafka/NATS para `inventory.events`, `decision.events`, `automation.jobs`.
- **Integrações externas**:
  - IBM CBOM Kit (CLI/API) para geração dos manifestos.
  - Secrets Manager/KMS (AWS, IBM Hyper Protect, Vault) para rotação automatizada.
  - Git/CI para PRs, pipelines e validação de políticas.

## 5. Interfaces/contratos
- **API `/cbom/ingest`**: POST JSON (manifesto) → response com ID e status.
- **API `/policy/decisions/:component`**: GET com último diagnóstico, recomendação PQC e status SLO.
- **Webhook `automation.completed`**: Notifica GRC/SRE sobre swaps aplicados (inclui CBOM antes/depois).
- **Dashboard**: painéis com métricas definidas em `metrics-resilience-matrix.md`.

## 6. Roadmap técnico (Sprints 2–4)
| Sprint | Incremento | Dependências |
| --- | --- | --- |
| 2 | Protótipo CBOM Gateway (script + plano lógico) | Manifestos de exemplo (OK) |
| 3 | Modelagem completa (diagramas RM-ODP, IaC esqueleto) | Documento de requisitos RM-ODP (OK) |
| 4 | Métricas & protocolos PQC, integração com pipelines reais | Matriz de métricas (este módulo) |
| 5 | Relatório de validação preliminar (dados reais/ simulação) | Telemetria e playbooks configurados |

> Este documento deve ser atualizado conforme novos módulos evoluem ou quando o gateway for implementado em ambiente real.
