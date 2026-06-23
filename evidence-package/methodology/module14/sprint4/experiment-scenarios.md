# Sprint 4 — Cenários Experimentais

## 1. Objetivo
Definir antecipadamente os cenários de experimento da pesquisa para o ambiente híbrido three-tier do Módulo 14, alinhando infraestrutura, métricas, critérios de aceitação e evidências antes do provisionamento real do laboratório. Este documento usa como base os requisitos de ambiente, a arquitetura do gateway, a modelagem híbrida da Sprint 3, a matriz de métricas e o protocolo de migração PQC já presentes no repositório.

## 2. Fontes de verdade e harmonização de métricas
Fontes obrigatórias utilizadas nesta especificação:
- `docs/governance/requisitos-ambiente.md`
- `docs/module14/metrics-resilience-matrix.md`
- `docs/module14/pqc-cryptoagility-metrics-migration.md`
- `docs/module14/gateway-architecture.md`
- `docs/module14/sprint3/hybrid-three-tier-model.md`
- `docs/module14/sprint5-validacao-arquitetural-seguranca.md`
- `docs/module14/README.md`

Para evitar ambiguidade entre métricas de resiliência e desempenho já distribuídas em mais de um artefato:
- Os IDs `INV-*`, `GOV-*`, `SWP-*`, `HYB-*`, `KLC-*`, `OBS-*`, `RES-*` e `COST-*` seguem como referência canônica as metas de `docs/module14/metrics-resilience-matrix.md`.
- As métricas `LAT-*`, `THR-*`, `PQC-OVH-*`, `SEC-*` e `GW-01` são tratadas como métricas complementares de instrumentação operacional, conforme `docs/module14/pqc-cryptoagility-metrics-migration.md`.

## 3. Escopo e premissas
- Esta sprint é de preparação documental e não afirma a implantação real de Kubernetes, service mesh, KMS, SIEM, FinOps ou bibliotecas PQC no dataplane.
- O ambiente-alvo continua sendo o ambiente híbrido five-layer/three-tier descrito em `docs/governance/requisitos-ambiente.md` e `docs/module14/sprint3/hybrid-three-tier-model.md`, com separação entre `web`, `aplicação`, `dados`, `controle` e `integração`.
- A campanha experimental deve ser capaz de executar `10.000 transações sintéticas`, comparar perfis `clássico`, `híbrido` e, quando possível, `PQC`, além de validar canário, rollback e coleta de evidências CBOM.
- Os ambientes lógicos considerados para execução futura permanecem `dev`, `staging/canário` e `prod-sim`, conforme o RM-ODP do repositório.
- Todos os cenários abaixo já nascem com evidências mínimas esperadas para auditoria e reaproveitamento na Sprint 5.

## 4. Infraestrutura de referência com 8 VMs

| VM | Quantidade | Camada principal | Papel experimental na Sprint 4 | Base documental |
| --- | --- | --- | --- | --- |
| `k8s-control` | 1 | controle | Orquestra namespaces, janelas de canário e políticas de agendamento; não deve receber carga de experimento nem telemetria pesada. | `docs/governance/requisitos-ambiente.md` |
| `k8s-worker-1` | 1 de 3 | web/aplicação | Hospedagem preferencial de workloads de borda e baseline/canário para comparação controlada. | `docs/governance/requisitos-ambiente.md` |
| `k8s-worker-2` | 1 de 3 | aplicação/controle | Hospedagem preferencial de APIs, gateway de criptoagilidade e sidecars de observabilidade. | `docs/governance/requisitos-ambiente.md`, `docs/module14/gateway-architecture.md` |
| `k8s-worker-3` | 1 de 3 | aplicação/integração | Hospedagem preferencial de réplicas, jobs e cargas auxiliares para evitar colocalização total em um único host. | `docs/governance/requisitos-ambiente.md` |
| `data-node` | 1 | dados | Banco relacional, object storage de evidências, volumes persistentes, backups e artefatos CBOM. | `docs/governance/requisitos-ambiente.md` |
| `security-integration-node` | 1 | integração | Vault/KMS equivalente, barramento de eventos e runners de automação/GitOps usados nos cenários de troca criptográfica. | `docs/governance/requisitos-ambiente.md`, `docs/module14/gateway-architecture.md` |
| `observability-node` | 1 | controle | Prometheus, Grafana, logs, traces, SIEM equivalente e retenção das evidências de teste. | `docs/governance/requisitos-ambiente.md` |
| `load-chaos-node` | 1 | controle de experimento | Geração de carga, testes de falha e caos, mantendo separação física para não contaminar CPU, memória e latência do sistema sob teste. | `docs/governance/requisitos-ambiente.md`, `docs/module14/sprint3/hybrid-three-tier-model.md` |

Notas de planejamento:
- A atribuição entre `k8s-worker-1`, `k8s-worker-2` e `k8s-worker-3` é preferencial para fins de preparação; o agendamento definitivo continua dependente do cluster real.
- A VM `load-chaos-node` permanece fora do cluster principal por exigência metodológica, garantindo comparabilidade das métricas HYB/LAT/THR/RES.

## 5. Catálogo de métricas adotado na Sprint 4

### 5.1 Métricas centrais

| Domínio | IDs usados na Sprint 4 | Meta de referência |
| --- | --- | --- |
| Inventário | `INV-01`, `INV-02` | `INV-01 ≥ 95%`; `INV-02 ≥ 97%` |
| Governança | `GOV-01` | `100%` das trocas com CBOM before/after |
| Automação de troca | `SWP-01` | `≤ 48h` em `staging/canário` |
| Híbrido/PQC | `HYB-01`, `HYB-02` | `HYB-01 > 99%`; `HYB-02 ≤ 5%` |
| Chaves/ciclo de vida | `KLC-01` | `≥ 90%` de rotação automatizada |
| Observabilidade | `OBS-01`, `OBS-02` | `OBS-01 = 100%`; `OBS-02 ≤ 5 min` |
| Resiliência | `RES-01`, `RES-02` | `RES-01 ≤ 4h`; `RES-02 ≥ 99%` |
| Custo | `COST-01` | `≤ +15%` por `1M reqs` |

### 5.2 Métricas complementares

| Grupo | IDs complementares | Meta de referência |
| --- | --- | --- |
| Desempenho ponta a ponta | `LAT-01`, `THR-01` | `LAT-01 p95 ≤ 150 ms`; `THR-01 sucesso ≥ 99%` e throughput dentro de `±5%` do baseline |
| Overhead PQC | `PQC-OVH-01`, `PQC-OVH-02` | `PQC-OVH-01 ≤ 15%`; `PQC-OVH-02 ΔCPU ≤ +20%` e `ΔMem ≤ +15%` |
| Resposta a incidente | `SEC-01`, `SEC-02` | `SEC-01 ≤ 5 min`; `SEC-02 ≤ 30 min`; rollback completo `≤ 10 min` |
| Eficiência do gateway | `GW-01` | efetividade `≥ 95%`, `lat_gw p95 ≤ 5 ms`, `policy_error < 1%` |

## 6. Cenários experimentais

### 6.1 Visão-resumo

| ID | Tipo | Camada | Objetivo resumido |
| --- | --- | --- | --- |
| `S4-T01` | típico | web | Estabelecer baseline clássico com carga representativa e inventário inicial. |
| `S4-T02` | típico | web | Validar canário TLS 1.3 híbrido na borda. |
| `S4-T03` | típico | aplicação | Validar mTLS híbrido entre serviços e detecção de desvio de política. |
| `S4-T04` | típico | dados | Validar rotação planejada de segredos/certificados e evidências de dados/backup. |
| `S4-T05` | típico | controle | Exercitar o fluxo CBOM `discover -> decision -> swap` com governança completa. |
| `S4-T06` | típico | integração | Validar cobertura de observabilidade, trilha de custo e retenção de evidências. |
| `S4-E01` | extremo | integração | Simular indisponibilidade do `security-integration-node` (KMS/event bus). |
| `S4-E02` | extremo | aplicação | Simular expiração/erro de certificado em rota canário e acionar rollback. |
| `S4-E03` | extremo | web | Comprimir a janela das `10.000 transações sintéticas` e medir overhead/isolamento. |
| `S4-E04` | extremo | controle | Simular adulteração de CBOM ou evento indevido no plano de controle. |

### 6.2 Detalhamento dos cenários

#### `S4-T01` — Baseline clássico com carga representativa

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Estabelecer a linha de base do perfil clássico para comparação futura entre `clássico`, `híbrido` e `PQC`, usando o fluxo `web -> app -> data` com `10.000 transações sintéticas`. |
| Camada | `web` |
| Tipo | `típico` |
| Pré-condições | `load-chaos-node` separado do cluster; inventário CBOM inicial disponível; dashboards e etiquetas de serviço/tier definidos; rota clássica ativa sem alteração criptográfica experimental. |
| Passos de execução | 1. Executar export CBOM inicial dos serviços ativos. 2. Rodar a carga sintética a partir do `load-chaos-node`. 3. Coletar traces, métricas e logs por tier. 4. Registrar baseline de latência, throughput e cobertura de telemetria. |
| Falha/ataque simulado | Nenhum; cenário nominal de referência. |
| Métricas alvo | `INV-01`, `OBS-01`, `LAT-01`, `THR-01` |
| Critérios de aceitação numéricos | `INV-01 ≥ 95%`; `OBS-01 = 100%`; `LAT-01 p95 ≤ 150 ms` nas chamadas intra-DC; `THR-01 sucesso ≥ 99%` e throughput dentro de `±5%` da própria linha de base do teste repetido. |
| Evidências esperadas | Export CBOM versionado; snapshot de dashboard por tier; traces ponta a ponta; relatório de baseline anexado ao pacote da Sprint 4. |

#### `S4-T02` — Canário TLS 1.3 híbrido na borda

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Validar a migração controlada do ingresso web de perfil clássico para TLS 1.3 híbrido com tráfego de canário. |
| Camada | `web` |
| Tipo | `típico` |
| Pré-condições | Baseline de `S4-T01` aprovado; feature flag de canário preparada; política alvo documentada no gateway; rota de rollback pronta. |
| Passos de execução | 1. Selecionar uma rota web com `1% a 5%` do tráfego sintético. 2. Aplicar perfil híbrido na borda. 3. Reexecutar a carga sintética. 4. Comparar handshakes, latência e sucesso contra o baseline. 5. Registrar CBOM before/after. |
| Falha/ataque simulado | Nenhum; mudança controlada de perfil criptográfico. |
| Métricas alvo | `GOV-01`, `SWP-01`, `HYB-01`, `HYB-02`, `LAT-01`, `PQC-OVH-01` |
| Critérios de aceitação numéricos | `GOV-01 = 100%`; `SWP-01 ≤ 48h`; `HYB-01 > 99%`; `HYB-02 ≤ 5%`; `LAT-01 p95 ≤ 150 ms`; `PQC-OVH-01 ≤ 15%` e variação p95 `≤ 20 ms` por conexão. |
| Evidências esperadas | Manifestos CBOM before/after; relatório de canário; comparação clássico vs híbrido; evidência de decisão do gateway e plano de rollback associado. |

#### `S4-T03` — mTLS híbrido entre microsserviços

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Validar o uso de mTLS híbrido no tráfego leste-oeste entre APIs e workers, incluindo detecção de desvio de política. |
| Camada | `aplicação` |
| Tipo | `típico` |
| Pré-condições | Service mesh e sidecars previstos na topologia; pelo menos dois serviços candidatos ao teste; exporters TLS/KEM planejados para o `observability-node`. |
| Passos de execução | 1. Selecionar dois serviços com comunicação interna crítica. 2. Aplicar perfil híbrido apenas entre eles. 3. Executar carga dirigida. 4. Introduzir um desvio de política controlado em um dos serviços. 5. Confirmar geração de alerta e retorno ao estado saudável. |
| Falha/ataque simulado | Desvio controlado de política criptográfica em um serviço do canário. |
| Métricas alvo | `HYB-01`, `HYB-02`, `OBS-01`, `OBS-02`, `RES-02`, `SEC-01` |
| Critérios de aceitação numéricos | `HYB-01 > 99%`; `HYB-02 ≤ 5%`; `OBS-01 = 100%`; `OBS-02 ≤ 5 min`; `RES-02 ≥ 99%`; `SEC-01 ≤ 5 min`. |
| Evidências esperadas | Métricas do mesh; trilha temporal do alerta; logs de rollback/fallback; comparação entre serviço saudável e serviço com desvio. |

#### `S4-T04` — Rotação planejada de segredos, certificados e evidências de dados

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Confirmar que o desenho experimental cobre rotação automatizada de segredos/certificados e proteção dos dados/evidências no `data-node`. |
| Camada | `dados` |
| Tipo | `típico` |
| Pré-condições | Objetos críticos classificados; integração planejada entre `data-node` e `security-integration-node`; política de retenção e armazenamento de evidências definida. |
| Passos de execução | 1. Selecionar segredos/certificados e um conjunto mínimo de backups/evidências. 2. Executar rotação planejada em ambiente controlado. 3. Confirmar atualização do inventário e anexação de evidências before/after. 4. Verificar coleta de logs de rotação e acesso. |
| Falha/ataque simulado | Nenhum; cenário de operação de rotina. |
| Métricas alvo | `KLC-01`, `GOV-01`, `OBS-01` |
| Critérios de aceitação numéricos | `KLC-01 ≥ 90%`; `GOV-01 = 100%`; `OBS-01 = 100%` para os serviços envolvidos na rotação. |
| Evidências esperadas | Log de rotação; manifesto before/after; registro de backup/evidência cifrada; checklist de objetos protegidos. |

#### `S4-T05` — Fluxo CBOM `discover -> decision -> swap`

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Exercitar o encadeamento do gateway desde a descoberta CBOM até a geração de ações de troca com governança e rastreabilidade. |
| Camada | `controle` |
| Tipo | `típico` |
| Pré-condições | Manifestos CBOM de amostra disponíveis; política de decisão documentada; templates de PR/playbook preparados; `code/cbom_gateway.py` validado como apoio à análise. |
| Passos de execução | 1. Ingerir manifestos CBOM. 2. Rodar o gateway de decisão. 3. Gerar ações recomendadas. 4. Simular abertura de PR/playbook. 5. Medir o tempo até a troca estar pronta para execução em `staging/canário`. |
| Falha/ataque simulado | Nenhum; cenário de governança normal. |
| Métricas alvo | `INV-02`, `GOV-01`, `SWP-01`, `GW-01` |
| Critérios de aceitação numéricos | `INV-02 ≥ 97%`; `GOV-01 = 100%`; `SWP-01 ≤ 48h`; `GW-01 efetividade ≥ 95%`; `lat_gw p95 ≤ 5 ms`; `policy_error < 1%`. |
| Evidências esperadas | Saída do gateway; pacote de decisão; PR ou playbook simulado; trilha temporal `discover -> swap`; vinculação para o manifesto analisado. |

#### `S4-T06` — Cobertura de observabilidade, custo e retenção de evidências

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Verificar se a arquitetura proposta separa corretamente a coleta de métricas e permite comparar custo incremental do perfil híbrido sem contaminação do sistema sob teste. |
| Camada | `integração` |
| Tipo | `típico` |
| Pré-condições | Etiquetas por serviço/tier/algoritmo definidas; `observability-node` isolado das cargas de aplicação; trilha de retenção de evidências documentada. |
| Passos de execução | 1. Ativar coleta em todos os serviços participantes do experimento. 2. Rodar uma janela estável de carga típica. 3. Consolidar métricas, logs, traces e custos por ambiente/tag. 4. Verificar se a coleta não altera a rota funcional observada. |
| Falha/ataque simulado | Nenhum; cenário de observação contínua. |
| Métricas alvo | `OBS-01`, `OBS-02`, `COST-01`, `THR-01` |
| Critérios de aceitação numéricos | `OBS-01 = 100%`; `OBS-02 ≤ 5 min` para um desvio controlado de baixa severidade; `COST-01 ≤ +15%` por `1M reqs`; `THR-01 sucesso ≥ 99%`. |
| Evidências esperadas | Inventário de métricas ativas; pacote de evidências retido no `data-node`; relatório de custo por tag; dashboard comparativo clássico vs híbrido. |

#### `S4-E01` — Indisponibilidade do `security-integration-node`

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Medir o comportamento seguro do ambiente quando KMS, secrets ou barramento de eventos se tornam indisponíveis. |
| Camada | `integração` |
| Tipo | `extremo` |
| Pré-condições | Rota canário ativa; runbooks de contingência preparados; caminhos de fallback documentados; observabilidade de KMS/event bus ativa. |
| Passos de execução | 1. Induzir indisponibilidade controlada do `security-integration-node`. 2. Executar carga mínima contínua. 3. Medir detecção, resposta e restauração. 4. Se necessário, acionar rollback para perfil clássico. |
| Falha/ataque simulado | Queda planejada de dependência crítica de KMS/eventos. |
| Métricas alvo | `OBS-02`, `RES-01`, `RES-02`, `SEC-01`, `SEC-02` |
| Critérios de aceitação numéricos | `OBS-02 ≤ 5 min`; `RES-01 ≤ 4h`; `RES-02 ≥ 99%`; `SEC-01 ≤ 5 min`; `SEC-02 ≤ 30 min`; rollback completo `≤ 10 min` quando acionado. |
| Evidências esperadas | Timeline do incidente; alertas correlacionados; logs de fallback/rollback; relatório de lições aprendidas e impacto observado por tier. |

#### `S4-E02` — Certificado expirado ou inválido em rota canário

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Validar detecção rápida de erro criptográfico de certificado e rollback seguro sem propagação para todo o ambiente. |
| Camada | `aplicação` |
| Tipo | `extremo` |
| Pré-condições | Canário ativo para ao menos um serviço; critérios de interrupção definidos; trilha de certificado/segredo vinculada ao inventário CBOM. |
| Passos de execução | 1. Introduzir certificado expirado ou incompatível somente na rota de canário. 2. Rodar carga controlada. 3. Detectar falhas de handshake. 4. Acionar rollback. 5. Confirmar restabelecimento do tráfego saudável. |
| Falha/ataque simulado | Erro de certificado em serviço isolado do canário. |
| Métricas alvo | `HYB-01`, `OBS-02`, `RES-02`, `SEC-01`, `SEC-02` |
| Critérios de aceitação numéricos | `OBS-02 ≤ 5 min`; `RES-02 ≥ 99%`; `SEC-01 ≤ 5 min`; `SEC-02 ≤ 30 min`; rollback completo `≤ 10 min`; `HYB-01 > 99%` após a estabilização pós-rollback. |
| Evidências esperadas | Logs de handshake com erro; alerta correlacionado; evidência de troca e reversão do certificado; comparação de disponibilidade antes/depois. |

#### `S4-E03` — Janela comprimida das `10.000 transações sintéticas`

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Verificar se a separação física do `load-chaos-node` mantém as métricas de desempenho observáveis mesmo quando a mesma carga total é comprimida em janela menor e mais agressiva. |
| Camada | `web` |
| Tipo | `extremo` |
| Pré-condições | Baseline clássico e híbrido já medidos; telemetria por pod/VM ativa; limites de interrupção definidos para não causar falsa leitura por saturação do gerador. |
| Passos de execução | 1. Reexecutar o volume de `10.000 transações sintéticas` em janela mais curta que a do cenário típico. 2. Comparar latência, throughput e overhead de CPU/memória. 3. Confirmar que a carga segue originando apenas do `load-chaos-node`. |
| Falha/ataque simulado | Pico controlado de carga a partir da VM de teste, com perfil próximo de stress/soak curto. |
| Métricas alvo | `HYB-02`, `COST-01`, `LAT-01`, `THR-01`, `PQC-OVH-01`, `PQC-OVH-02` |
| Critérios de aceitação numéricos | `HYB-02 ≤ 5%`; `COST-01 ≤ +15%` por `1M reqs`; `LAT-01 p95 ≤ 150 ms`; `THR-01 sucesso ≥ 99%`; `PQC-OVH-01 ≤ 15%`; `PQC-OVH-02 ΔCPU ≤ +20%` e `ΔMem ≤ +15%` sem throttling. |
| Evidências esperadas | Relatório de step/stress; métricas por VM; comparação entre baseline e janela comprimida; registro de isolamento do gerador de carga. |

#### `S4-E04` — Adulteração de CBOM ou evento indevido no plano de controle

| Campo | Conteúdo |
| --- | --- |
| Objetivo | Garantir que a cadeia `CBOM -> Policy -> Automation` rejeite entradas adulteradas e preserve auditabilidade do plano de controle. |
| Camada | `controle` |
| Tipo | `extremo` |
| Pré-condições | Hashing/assinatura e critérios de aprovação definidos; pipeline de automação separado do gerador de carga; trilha de auditoria do gateway habilitada. |
| Passos de execução | 1. Alterar propositalmente um manifesto CBOM ou evento de decisão. 2. Tentar ingerir o artefato adulterado. 3. Verificar bloqueio antes da automação. 4. Registrar alerta e evidência de rejeição. 5. Reexecutar com artefato íntegro para confirmar recuperação do fluxo. |
| Falha/ataque simulado | Adulteração de manifesto ou evento malicioso no plano de controle. |
| Métricas alvo | `INV-02`, `GOV-01`, `OBS-02`, `GW-01` |
| Critérios de aceitação numéricos | `INV-02 ≥ 97%`; `GOV-01 = 100%`; `OBS-02 ≤ 5 min`; `GW-01 policy_error < 1%`; `100%` dos artefatos adulterados da amostra devem ser bloqueados antes da automação. |
| Evidências esperadas | Log de rejeição; hash/assinatura inválida; trilha de auditoria; comparação entre artefato íntegro e artefato bloqueado. |

## 7. Matriz de rastreabilidade cenário -> métricas da Sprint 4

| Cenário | Métricas centrais | Métricas complementares | Evidência-chave |
| --- | --- | --- | --- |
| `S4-T01` | `INV-01`, `OBS-01` | `LAT-01`, `THR-01` | baseline clássico por tier |
| `S4-T02` | `GOV-01`, `SWP-01`, `HYB-01`, `HYB-02` | `LAT-01`, `PQC-OVH-01` | canário web com CBOM before/after |
| `S4-T03` | `HYB-01`, `HYB-02`, `OBS-01`, `OBS-02`, `RES-02` | `SEC-01` | mTLS híbrido entre serviços |
| `S4-T04` | `KLC-01`, `GOV-01`, `OBS-01` | — | rotação e proteção de evidências |
| `S4-T05` | `INV-02`, `GOV-01`, `SWP-01` | `GW-01` | fluxo `discover -> swap` |
| `S4-T06` | `OBS-01`, `OBS-02`, `COST-01` | `THR-01` | cobertura de observabilidade e custo |
| `S4-E01` | `OBS-02`, `RES-01`, `RES-02` | `SEC-01`, `SEC-02` | falha de KMS/event bus |
| `S4-E02` | `HYB-01`, `OBS-02`, `RES-02` | `SEC-01`, `SEC-02` | certificado expirado com rollback |
| `S4-E03` | `HYB-02`, `COST-01` | `LAT-01`, `THR-01`, `PQC-OVH-01`, `PQC-OVH-02` | stress curto sem contaminação |
| `S4-E04` | `INV-02`, `GOV-01`, `OBS-02` | `GW-01` | rejeição de artefato adulterado |

Cobertura consolidada:
- Inventário/governança: `S4-T01`, `S4-T05`, `S4-E04`.
- Híbrido/desempenho: `S4-T02`, `S4-T03`, `S4-E02`, `S4-E03`.
- Dados/chaves: `S4-T04`, `S4-E01`.
- Observabilidade/resiliência: `S4-T03`, `S4-T06`, `S4-E01`, `S4-E02`.
- Custo e eficiência operacional: `S4-T06`, `S4-E03`, `S4-T05`.

## 8. Sequência de execução sugerida

| Ordem | Cenário | Justificativa |
| --- | --- | --- |
| 1 | `S4-T01` | Cria baseline clássico e valida se a telemetria mínima está pronta. |
| 2 | `S4-T05` | Garante que a cadeia de decisão e governança funcione antes de qualquer troca experimental. |
| 3 | `S4-T02` | Move a borda web para canário híbrido com risco controlado e comparação direta contra o baseline. |
| 4 | `S4-T03` | Estende a mudança para mTLS leste-oeste somente após o sucesso da borda. |
| 5 | `S4-T04` | Consolida rotação e proteção de dados/evidências antes dos cenários de falha severa. |
| 6 | `S4-T06` | Fecha a camada de observabilidade/custo para sustentar interpretação correta dos extremos. |
| 7 | `S4-E02` | Testa rollback criptográfico localizado com impacto contido. |
| 8 | `S4-E01` | Exercita dependência crítica de integração/KMS já com trilha de evidências madura. |
| 9 | `S4-E03` | Mede comportamento sob carga mais agressiva depois de validar governança e rollback. |
| 10 | `S4-E04` | Finaliza com cenário de integridade do plano de controle, preservando a confiabilidade documental da campanha. |

## 9. Priorização MoSCoW

| Cenário | Prioridade | Racional |
| --- | --- | --- |
| `S4-T01` | `Must` | Sem baseline não há comparação confiável entre perfis. |
| `S4-T05` | `Must` | Sem trilha `discover -> swap` a Sprint 4 perde governança e mensuração de tempo. |
| `S4-T02` | `Must` | É o principal ensaio de migração controlada exigido pelo protocolo PQC. |
| `S4-T03` | `Must` | Garante cobertura da camada de aplicação e do mTLS interno. |
| `S4-T04` | `Should` | Reforça dados, backup e rotação, mas depende das bases anteriores. |
| `S4-T06` | `Should` | Necessário para leitura correta de custo e evidência, porém pode ser refinado depois do provisionamento. |
| `S4-E01` | `Must` | Queda de KMS/eventos é risco crítico documentado na Sprint 5. |
| `S4-E02` | `Must` | Expiração de certificado é falha provável e diretamente ligada a rollback seguro. |
| `S4-E03` | `Should` | Stress controlado é valioso para desempenho, mas exige ambiente já estável. |
| `S4-E04` | `Must` | Integridade do CBOM/plano de controle é requisito estrutural da pesquisa. |

## 10. Limites desta sprint
- Os cenários foram especificados para preparação e validação futura; não substituem a execução prática em laboratório provisionado.
- A distribuição exata de pods por worker, ranges de IP, portas numéricas, manifests e políticas de firewall ainda depende do ambiente real.
- O repositório contém protótipo de decisão CBOM e documentação arquitetural, mas não comprova implantação real de `Vault`, `KMS`, `service mesh`, `SIEM`, `ArgoCD`, `Kafka/NATS` ou bibliotecas PQC no dataplane.
- Os critérios de custo (`COST-01`) e overhead computacional (`PQC-OVH-02`) permanecem como alvos de medição, não como resultados já obtidos.

## 11. Riscos abertos
- Persistem dependências fortes de observabilidade correta; sem exporters TLS/KEM ou trilha temporal consistente, `HYB-*`, `OBS-*` e `RES-*` podem perder confiabilidade.
- A ausência temporária de ambiente provisionado impede calibrar janelas reais de carga, retenção de logs e capacidade efetiva de storage no `data-node`.
- A convergência entre métricas centrais (`RES-*`) e complementares (`SEC-*`, `LAT-*`, `THR-*`) precisa ser mantida explícita para evitar leituras divergentes em relatórios posteriores.
- A política de assinatura/hashing de CBOM e o fluxo de aprovação do plano de controle ainda precisam ser materializados no módulo seguinte para que `S4-E04` deixe de ser apenas desenho.
