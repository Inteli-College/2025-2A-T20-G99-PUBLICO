# Relatório Público – Módulo 15
## Projeto: Criptoagilidade em Ambientes Corporativos Híbridos para Transição Pós-Quântica

### Contexto
O Módulo 15 consolida o projeto desde as bases teóricas e diagnóstico de vulnerabilidades até **design arquitetural**, **operacionalização da criptoagilidade**, **implantação de ambiente simulado** e **validação com foco em segurança com evidências de execução**. O cenário-alvo é um ambiente corporativo **híbrido** (on-premise + nuvem) com arquitetura **three-tier** (apresentação, aplicação e dados), no qual dependências criptográficas são continuamente inventariadas, governadas, migradas (clássico → híbrido/PQC) e monitoradas, com rollback seguro.

### Objetivo do Módulo 15
Entregar uma arquitetura coerente, replicável e **validada** que:
- Centralize governança criptográfica e agilidade de algoritmos via um **Gateway de Criptoagilidade**.
- Suporte adoção controlada de PQC (preferencialmente via **perfis híbridos**) preservando disponibilidade e desempenho.
- Defina **métricas, protocolos e cenários de validação** respaldados por simulação executável e evidências de runtime.
- Demonstre viabilidade prática via **simulação containerizada de 8 nós** em servidor acadêmico real.

---

## Entregáveis por sprint (Sprints 1–5)

### Sprint 1 — Fundamentos
Atividades que estabelecem a base para o módulo:
- Mapeamento de vulnerabilidades em ambientes three-tier.
- Revisão bibliográfica e análise de lacunas (PQC, criptoagilidade, resiliência).
- Mapeamento inicial do IBM CBOM Kit como fonte de inventário.

**Resultado**: definição de drivers de segurança e do problema, justificando criptoagilidade como capacidade ponta a ponta (inventário → mudança → detecção → recuperação).

### Sprint 2 — Especificação do Gateway de Criptoagilidade + protótipo de decisão via CBOM
Entregáveis:
- Documento de arquitetura do gateway (módulos lógicos, fluxos, integrações).
- Protótipo para ingestão/análise de manifestos CBOM e geração de recomendações acionáveis de migração (clássico → perfis híbridos/PQC).

**Resultado**: estabelecimento de um modelo de controle e automação que operacionaliza o ciclo "CBOM → decisão → automação/rollback".

### Sprint 3 — Modelagem do ambiente híbrido three-tier (web/app/data)
Entregáveis:
- Modelagem conceitual do three-tier híbrido (visões lógica/física/dados).
- Diagramas de fluxo para coleta CBOM, comunicação TLS/mTLS, observabilidade e resposta.
- Rastreabilidade entre requisitos e decisões arquiteturais.

**Resultado**: blueprint claro de onde há criptografia, onde instrumentar telemetria e onde ocorrem transações e armazenamento de dados críticos.

### Sprint 4 — Métricas, protocolo de migração PQC e critérios de resiliência/rollback
Entregáveis:
- Matriz de métricas e resiliência (cobertura de inventário, sucesso de handshake, overhead de latência, MTTD/MTTR, rollback seguro, custo incremental).
- Protocolo de migração PQC com rollout em canário, estratégia de compatibilidade e gates explícitos de rollback/fallback.
- Especificação da topologia de 8 nós/VMs e cenários experimentais.

**Resultado**: operacionalização da criptoagilidade com thresholds mensuráveis e rollback definido para preservar segurança e disponibilidade.

### Sprint 5 — Validação arquitetural, implantação do ambiente simulado e validação de segurança
Entregáveis:
- Relatório técnico (PT/EN) com validação documental e de runtime.
- Topologia de laboratório containerizada com **8 nós lógicos** implantada em servidor acadêmico.
- Execução de cenários experimentais (baseline, canário, fluxo CBOM, teste de integridade) com coleta de evidências.
- Tratamento explícito de criptografia (em trânsito/em repouso), autenticação/MFA, biometria (quando aplicável) e prontidão PQC.
- Análise de vulnerabilidades com classificação de risco (baixo/médio/alto), mitigações e red flags.

**Resultado**: consolidação do módulo como pacote validado com evidências de runtime, demonstrando a viabilidade prática da arquitetura proposta.

---

## Resumo da arquitetura (visão pública)

### Arquitetura em três camadas
- **Apresentação (Web)**: CDN/WAF/ingress, terminação TLS, política de cipher suites, endpoints de usuário.
- **Aplicação (App)**: microserviços + service mesh (mTLS), aplicação de políticas e observabilidade; plano de controle do gateway.
- **Dados (Data)**: bancos, backups, armazenamento de evidências, KMS/Secrets Manager, auditoria.

### Gateway de Criptoagilidade (plano de controle)
Módulos principais:
- **Ingestão de CBOM** (entrada/versionamento de inventário)
- **Policy Engine** (decisão de algoritmos/perfis)
- **Orquestração de automação** (GitOps, playbooks de troca)
- **Correlação de telemetria** (sinais runtime e evidências)
- **Rollback/caos criptográfico** (reversão segura e testes)
- **Barramento de observabilidade e GRC** (evidências auditáveis e reporting)

---

## Ambiente simulado e validação

### Topologia containerizada de 8 nós
A arquitetura foi exercitada em servidor acadêmico real (Ubuntu 24.04 LTS, 64 vCPUs Intel Xeon Gold 6454S, 125 GiB RAM) usando containers rootless Podman para simular a topologia de referência de 8 nós:

| Nó | Função | Tecnologia |
| --- | --- | --- |
| `k8s-control` | Plano de controle do cluster | Serviço mock Python |
| `k8s-worker-1` | Camada web (baseline) | Serviço mock Python |
| `k8s-worker-2` | Camada de aplicação | Serviço mock Python + cliente PostgreSQL |
| `k8s-worker-3` | Camada de aplicação (canário) | Serviço mock Python + cliente PostgreSQL |
| `data-node` | Camada de dados | PostgreSQL |
| `security-integration-node` | Integração de segurança/KMS | Serviço mock Python |
| `observability-node` | Monitoramento e telemetria | Prometheus |
| `load-chaos-node` | Carga e testes de caos | Grafana k6 |

O isolamento de rede foi obtido com cinco redes Docker/Podman dedicadas: `ingress_net`, `cluster_net`, `data_net`, `security_net` e `observability_net`.

### Resultados dos cenários executados

| Cenário | Objetivo resumido | Resultado observado | Status |
| --- | --- | --- | --- |
| S4-T01 | Baseline clássico com carga sintética | p95 = 41,78 ms, http_req_failed = 0,00%, 150 requisições bem-sucedidas | Aprovado |
| S4-T02 | Canário na rota `app-canary` | p95 = 25,47 ms, http_req_failed = 0,00%, 40 requisições bem-sucedidas | Aprovado |
| S4-T05 | Fluxo `discover → decision → swap` via CBOM | Gateway gerou 2 ações de migração (web + app); scanner identificou 10 arquivos com 1023 ocorrências | Aprovado (ressalva metodológica) |
| S4-E04 | Integridade/adulteração de CBOM | Manifesto original: 2 ações; manifesto adulterado: 1 ação, sem bloqueio interno da automação | Falha parcial importante |

### Principais achados
- Cenários de baseline e canário ficaram bem abaixo do limiar `LAT-01 p95 ≤ 150 ms`, demonstrando viabilidade da simulação em host único com isolamento lógico.
- O fluxo `discover → decision → swap` foi confirmado em ambiente de execução, fortalecendo a aderência prática aos requisitos funcionais.
- O teste de integridade CBOM revelou um **gap real do protótipo**: a adulteração do manifesto era observável externamente por hash, mas o gateway não rejeitou o artefato adulterado internamente. Isso valida a necessidade de enforcement obrigatório de assinatura/hash no plano de controle.

---

## Postura de segurança (cobertura explícita)

### Criptografia
- **Em trânsito**: TLS 1.3 na borda + mTLS leste-oeste; perfis híbridos para adoção incremental de PQC.
- **Em repouso**: envelope encryption via KMS/Secrets Manager; backups cifrados e evidências com governança.

### Autenticação e MFA
- Operações privilegiadas no plano de controle exigem autenticação forte (OIDC/OAuth2), RBAC, trilha de auditoria e **MFA obrigatório**.

### Biometria
- Opcional, tipicamente indireta via passkeys (FIDO2/WebAuthn), conforme IdP e apetite a risco.

### PQC (pós-quântica)
- Adoção definida por protocolos e métricas (Kyber para KEM; Dilithium/Falcon/SPHINCS+ para assinaturas conforme o caso).
- Estratégia híbrida é priorizada para reduzir risco de incompatibilidade.

---

## Riscos e red flags (resumo público)
- Plano de controle sem OIDC/RBAC/MFA é alvo crítico de comprometimento.
- CBOM sem controles de integridade/autenticidade aumenta risco de supply chain (confirmado pelo teste S4-E04).
- CI/CD sem governança (review/branch protection) torna a automação vetor de ataque.
- Dependência de KMS sem contingência/chaos testing pode causar indisponibilidade e bloquear recuperação.
- Fallback amplo para TLS legado compromete confidencialidade e objetivos PQC.

---

## Conclusão e próximos passos
O Módulo 15 conclui com uma arquitetura validada tanto por revisão documental quanto por evidências controladas de runtime. A simulação containerizada de 8 nós demonstrou que a topologia proposta é executável e produz resultados mensuráveis e auditáveis em condições realistas.

Próximos passos recomendados:
- Evoluir a simulação para service mesh/KMS/SIEM reais ou equivalentes.
- Implementar OIDC + RBAC + MFA no plano de controle.
- Adicionar assinatura obrigatória de CBOM e bloqueio de artefatos adulterados.
- Completar cenários dinâmicos restantes e coletar métricas LAT/THR/PQC-OVH/OBS/RES com retenção padronizada de evidências.
