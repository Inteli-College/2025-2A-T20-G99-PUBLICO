# Relatório Público – Módulo 14
## Projeto: Criptoagilidade em Ambientes Corporativos Híbridos para Transição Pós-Quântica

### Contexto
O Módulo 14 avança o projeto a partir da base teórica e diagnóstica consolidada no Módulo 13 para uma etapa de **design arquitetural**, **operacionalização da criptoagilidade** e **validação preliminar com foco em segurança**. O cenário-alvo é um ambiente corporativo **híbrido** (on-premise + nuvem) com arquitetura **three-tier** (apresentação, aplicação e dados), no qual dependências criptográficas precisam ser continuamente inventariadas, governadas, migradas (clássico → híbrido/PQC) e monitoradas, com rollback seguro.

### Objetivo do Módulo 14
Entregar uma arquitetura coerente e replicável que:
- Centralize governança criptográfica e agilidade de algoritmos via um **Gateway de Criptoagilidade**.
- Suporte adoção controlada de PQC (preferencialmente via **perfis híbridos**) preservando disponibilidade e desempenho.
- Defina **métricas, protocolos e cenários de validação** executáveis em ambiente de simulação nos módulos subsequentes.

---

## Entregáveis por sprint (Sprints 1–5)

### Sprint 1 — Fundamentos (herdados do Módulo 13)
Embora as atividades da Sprint 1 tenham sido realizadas no Módulo 13, elas fundamentam o Módulo 14:
- Mapeamento de vulnerabilidades em ambientes three-tier.
- Revisão bibliográfica e análise de lacunas (PQC, criptoagilidade, resiliência).
- Mapeamento inicial do IBM CBOM Kit como fonte de inventário.

**Resultado**: definição de drivers de segurança e do problema, justificando criptoagilidade como capacidade ponta a ponta (inventário → mudança → detecção → recuperação).

### Sprint 2 — Especificação do Gateway de Criptoagilidade + protótipo de decisão via CBOM
Entregáveis:
- Documento de arquitetura do gateway (módulos lógicos, fluxos, integrações).
- Protótipo para ingestão/análise de manifestos CBOM e geração de recomendações acionáveis de migração (clássico → perfis híbridos/PQC).

**Resultado**: estabelecimento de um modelo de controle e automação que operacionaliza o ciclo “CBOM → decisão → automação/rollback”.

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

**Resultado**: operacionalização da criptoagilidade com thresholds mensuráveis e rollback definido para preservar segurança e disponibilidade.

### Sprint 5 — Validação preliminar da arquitetura e playbook de validação de segurança
Entregáveis:
- Relatório técnico (PT/EN) documentando:
  - descrição objetiva da arquitetura;
  - justificativa das decisões arquiteturais;
  - aderência a requisitos funcionais e não funcionais;
  - cenários de validação com foco em segurança (inspeção estática e dinâmica);
  - tratamento explícito de criptografia (em trânsito/em repouso), autenticação/login, MFA, biometria (quando aplicável) e prontidão PQC;
  - análise de vulnerabilidades com classificação de risco (baixo/médio/alto), mitigações e red flags.

**Resultado**: consolidação do módulo como pacote de validação documental, pronto para orientar a fase de simulação e coleta de evidências.

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
- CBOM sem controles de integridade/autenticidade aumenta risco de supply chain.
- CI/CD sem governança (review/branch protection) torna a automação vetor de ataque.
- Dependência de KMS sem contingência/chaos testing pode causar indisponibilidade e bloquear recuperação.
- Fallback amplo para TLS legado compromete confidencialidade e objetivos PQC.

---

## Próximos passos
O Módulo 14 conclui a prontidão arquitetural. A próxima fase é executar os cenários definidos em ambiente de simulação:
- Implementar plano de controle mínimo com OIDC + RBAC + MFA.
- Implantar mesh/KMS/observabilidade e executar testes (carga + caos).
- Coletar evidências das métricas e validar rollback.

