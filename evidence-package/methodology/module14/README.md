# Módulo 14 — Planejamento e Acompanhamento

Resumo do plano acadêmico (ver `TAPI-Modulo14.txt`) e estado de cumprimento por sprint.

## Visão Geral
- **Problema de pesquisa**: desenvolver e validar um modelo de criptoagilidade que una migração PQC, detecção em tempo real e recuperação resiliente em arquitetura three-tier híbrida.
- **Objetivo do módulo**: entregar o design macro do gateway de criptoagilidade, o modelo do ambiente three-tier e as métricas que suportarão as simulações dos módulos seguintes.

## Quadro por Sprint

| Sprint | Foco | Entregáveis obrigatórios | Status |
| --- | --- | --- | --- |
| 1 | Revisão bibliográfica e levantamento de vulnerabilidades | Atualização das tabelas PT/EN + matriz R–A–C/V | Concluído (realizado no Módulo 13) |
| 2 | Especificação do gateway e de seus módulos | Documento de arquitetura (este repositório), protótipo CBOM gateway | Concluído (entregue: `docs/module14/gateway-architecture.md`, `code/cbom_gateway.py`) |
| 3 | Modelagem conceitual do ambiente híbrido e fluxos | Diagramas RM-ODP + requisitos (ver `docs/governance/*rm-odp*`) | Concluído (entregue: `docs/module14/sprint3/*`) |
| 4 | Métricas, protocolos PQC e preparação dos experimentos | Matriz de métricas/resiliência + protocolo PQC (pt/en) + cenários/topologia da campanha experimental | Concluído (entregue: `docs/module14/metrics-resilience-matrix.md`, `docs/module14/pqc-cryptoagility-metrics-migration.md`, `docs/module14/pqc-cryptoagility-metrics-migration-en.md`, `docs/module14/sprint4/*`) |
| 5 | Validação preliminar e documentação | Relatório técnico de validação e cenários de segurança (pt/en) | Concluído (entregue: `docs/module14/sprint5-validacao-arquitetural-seguranca.md`, `docs/module14/sprint5-architectural-security-validation.md`) |


## Checklist Sprint 4
- [x] Cenários típicos e extremos com critérios de aceitação mensuráveis (`docs/module14/sprint4/experiment-scenarios.md`).
- [x] Topologia de `8 VMs`, isolamento de rede e três diagramas Mermaid (`docs/module14/sprint4/vm-network-topology.md`).
- [x] Índice curto dos artefatos da sprint (`docs/module14/sprint4/README.md`).

## Checklist Sprint 5
- [x] Relatório técnico de validação preliminar e cenários de segurança (PT) (`docs/module14/sprint5-validacao-arquitetural-seguranca.md`).
- [x] Technical report (EN) for preliminary validation and security scenarios (`docs/module14/sprint5-architectural-security-validation.md`).
- [x] Evidência mínima por execução de protótipo (CBOM → ações), conforme anexos dos relatórios.
- [x] Configuração e implantação do ambiente simulado de 8 nós em servidor acadêmico com Podman rootless (`docs/module14/setup-ambiente-8-nos.md`).
- [x] Topologia containerizada com scripts de orquestração e cenários executáveis (`lab/topology/`).
