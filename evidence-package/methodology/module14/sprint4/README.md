# Sprint 4 — Cenários Experimentais e Topologia

Esta pasta consolida a especificação documental da Sprint 4 do Módulo 14. O foco aqui é preparar a execução futura dos experimentos, definir a topologia mínima de 8 VMs e alinhar cenários, métricas e evidências sem afirmar provisionamento real imediato.

## Artefatos
- `experiment-scenarios.md`: cenários típicos e extremos, infraestrutura de referência, critérios de aceitação mensuráveis, rastreabilidade e ordem sugerida de execução.
- `vm-network-topology.md`: topologia de rede/VMs, fluxos lógicos e mapa da superfície de ataque simulada com três diagramas Mermaid.

## Relação com os demais artefatos do módulo
- Complementa a matriz de métricas e resiliência (`docs/module14/metrics-resilience-matrix.md`) com cenários executáveis e critérios por experimento.
- Complementa o protocolo de migração PQC (`docs/module14/pqc-cryptoagility-metrics-migration.md`) com preparo de infraestrutura e rotas de observação/rollback.
- Reaproveita a modelagem híbrida da Sprint 3 (`docs/module14/sprint3/hybrid-three-tier-model.md`) e prepara a validação documental da Sprint 5 (`docs/module14/sprint5-validacao-arquitetural-seguranca.md`).

## Fontes de verdade utilizadas
- `docs/governance/requisitos-ambiente.md`
- `docs/module14/metrics-resilience-matrix.md`
- `docs/module14/pqc-cryptoagility-metrics-migration.md`
- `docs/module14/gateway-architecture.md`
- `docs/module14/sprint3/hybrid-three-tier-model.md`
- `docs/module14/sprint5-validacao-arquitetural-seguranca.md`
- `docs/module14/README.md`

## Limites desta sprint
- Os artefatos desta pasta descrevem ambiente alvo, critérios e sequências de teste.
- CIDRs, portas numéricas definitivas, manifests Kubernetes, IaC e integrações reais com mesh/KMS/SIEM permanecem dependentes do provisionamento do módulo seguinte.
