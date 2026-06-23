# Métricas e Protocolo de Migração PQC — Ambiente Híbrido Three-Tier

Documento técnico para avaliar e conduzir a criptoagilidade em um ambiente híbrido (on-premise + nuvem) com arquitetura three-tier (web/app/data) e gateway de criptoagilidade.

## 1. Premissas e escopo
- Serviços distribuídos entre data center e nuvem pública, conectados por mesh/gateway híbrido.
- Tráfego TLS 1.3, com perfis clássicos, híbridos e pós-quânticos (PQC) em experimentação controlada.
- Observabilidade padronizada via OpenTelemetry, integração com SIEM/FinOps e automação GitOps.
- Critérios alinhados às metas de Sprint 4–5 para validação de desempenho e resiliência.

## 2. Métricas de desempenho

| ID | Métrica | Descrição / Fórmula | Método de medição | Ferramentas de coleta | Critério de aceitação |
| --- | --- | --- | --- | --- | --- |
| LAT-01 | Latência ponta a ponta | `t_resp = t_end − t_start`; medir p50/p95 por rota/tier e diferença `Δlat_híbrido = lat_híbrido − lat_onprem`. | Testes de carga sintéticos e tracing distribuído com headers de tempo em cada tier. | k6/Locust, OpenTelemetry (traces), Prometheus/Grafana, service mesh metrics. | p95 ≤ 150 ms em chamadas intra-DC; `Δlat_híbrido` ≤ 5% vs base clássica. |
| THR-01 | Throughput efetivo | `req/s = total_req ÷ janela_s` e taxa de sucesso `sucesso = req_ok ÷ total_req`. | Carga crescente (step/stress) e observação de filas/conexões por tier. | k6/Locust, mesh metrics, Prometheus, APM (APM/Jaeger). | Manter ±5% do throughput base clássico com `sucesso ≥ 99%` em canário. |
| PQC-OVH-01 | Overhead de handshake PQC | `ovh = (t_handshake_pqc − t_handshake_clássico) ÷ t_handshake_clássico`. | Comparar perfis clássico vs híbrido/PQC em mesma rota sob carga fixa. | Wireshark/tcpdump com TLS secrets, OpenTelemetry spans de handshake, mesh debug metrics. | `ovh` ≤ 15% e variação p95 ≤ 20 ms por conexão. |
| PQC-OVH-02 | Overhead computacional (CPU/mem) | `ΔCPU = CPU_pqc − CPU_clássico`; `ΔMem = Mem_pqc − Mem_clássico` em app e gateway. | Profiling por pod/VM durante testes controlados (10–15 min). | Prometheus node/exporter, eBPF/profiler, HPA/KEDA métricas. | `ΔCPU` ≤ +20% e `ΔMem` ≤ +15% sem throttling. |
| COST-01 | Custo operacional em nuvem | `custo_inc = (custo_pqc − custo_base) ÷ 1M req` incluindo compute + egress + KMS. | Coletar custo diário por tag de ambiente e dividir por volume de requisições. | AWS/Azure/IBM Cost Explorer, FinOps dashboards, logs de API KMS. | Incremento ≤ +15% por 1M req; egress não deve crescer > +5%. |
| SEC-01 | Tempo de detecção (MTTD) | `MTTD = Σ(t_alert − t_event) ÷ N` para eventos de falha/violação cripto. | Injetar falhas (cert expirado, KMS indisponível) e medir tempo até alerta no SIEM. | SIEM (Splunk/QRadar), Prometheus alertmanager, OpenTelemetry. | MTTD ≤ 5 min (canário) para eventos críticos. |
| SEC-02 | Tempo de resposta (MTTR) | `MTTR = Σ(t_recovery − t_alert) ÷ N` até restabelecer perfil saudável/rollback. | Executar playbooks automáticos e medir restabelecimento de handshakes. | ITSM + automation logs, mesh metrics, runbooks orquestrados. | MTTR ≤ 30 min em canário; rollback completo ≤ 10 min. |
| RES-01 | Resiliência – tempo de recuperação | `RTO = t_restauro_serviço − t_falha`; sucesso de failover `sucesso = eventos_recuperados ÷ eventos_total`. | Falhas planejadas (chaos) em rota híbrida e no gateway, medindo restauração. | Chaos Mesh/Litmus, Prometheus, mesh health checks. | RTO ≤ 15 min; `sucesso` ≥ 99% em canário. |
| RES-02 | Resiliência – degradação controlada | `capacidade = req_ok_híbrido ÷ req_ok_base` durante falhas simuladas; avaliar erro p99. | Teste de carga durante falhas de KMS/PKI e perda parcial de região. | k6/Locust, mesh/APM, circuit breaker logs. | Capacidade ≥ 70% do baseline com erro p99 < 1%. |
| GW-01 | Eficiência do gateway de criptoagilidade | `eficácia = ações_aplicadas ÷ ações_recomendadas`; `lat_gw = p95_gw`; `erro_policy = falhas_policy ÷ execuções`. | Correlacionar decisões do gateway com execuções de automação e latência do hop do gateway. | Logs do gateway, queues (Kafka/NATS), Prometheus, traces APM. | `eficácia` ≥ 95%; `lat_gw` p95 ≤ 5 ms; `erro_policy` < 1%. |

### Notas de medição
- Sempre comparar perfil clássico vs híbrido/PQC na mesma janela e carga para isolar o overhead.
- Usar etiquetas (service, tier, ambiente, algoritmo) para permitir dashboards por componente.
- Exportar séries para o repositório de evidências (S3/Cloud Object Storage) com retenção mínima de 30 dias.

## 3. Protocolo de migração para algoritmos PQC

1. **Mapeamento de pontos criptográficos**
   - Inventariar todos os terminais TLS, APIs, filas e storage com o CBOM (manifestos por serviço/tier).
   - Classificar algoritmos atuais (RSA/ECDH/ECDSA) e dependências de PKI/KMS, inclusive bibliotecas embarcadas.

2. **Seleção de algoritmos PQC (NIST)**
   - Assimetria: Kyber-768/1024 (KEM) para troca; Dilithium-2/3 para assinatura; Falcon-512 apenas quando requerido por performance/verificação rápida.
   - Definir perfis híbridos (ex.: TLS 1.3 com X25519 + Kyber-768) para reduzir risco de compatibilidade.

3. **Estratégia de substituição gradual**
   - Ativar perfis híbridos primeiro em canário (1–5% do tráfego), depois em staging e produção progressiva.
   - Manter dual-stack (clássico + PQC) até que métricas LAT/THR/PQC-OVH cumpram critérios por 7 dias.

4. **Rotação e gerenciamento de chaves**
   - Gerar pares PQC via KMS/Engine compatível; armazenar certificados PQC/híbridos em cofre central.
   - Rotação automatizada com política < 90 dias e validação de revogação (CRL/OCSP) onde aplicável.

5. **Compatibilidade com sistemas legados**
   - Detectar stacks que não suportam extensões/algoritmos (ex.: dispositivos TLS 1.2 only) e manter fallback clássico controlado.
   - Documentar exceções com prazo de correção e monitorar uso via CBOM + telemetria.

6. **Fluxos de fallback**
   - Feature flags por serviço/tier para alternar entre perfil clássico, híbrido e PQC.
   - Playbook de rollback automático ao detectar `ovh > 15%`, `erro_policy > 1%` ou violação de LAT/THR/RES.

7. **Integração com gateway de criptoagilidade**
   - Gateway recebe inventário (CBOM), gera decisões de swap e aciona pipelines; registra evidências (before/after).
   - Métricas GW-01 alimentam painéis e gatilhos de rollback/chaos.

8. **Automação da migração**
   - Pipelines GitOps aplicam mudanças (config TLS/KEM, libs, certificados) com validação em staging.
   - Hooks para atualizar manifestos CBOM e publicar métricas automaticamente após cada deploy.

9. **Testes e validação**
   - Funcional: testes de handshakes, compatibilidade de clientes, verificação de certificados/algoritmos.
   - Desempenho: executar suite de carga e comparar todas as métricas da seção 2 entre perfis.
   - Segurança/resiliência: chaos de KMS/PKI, expiração forçada de certificado, falha de região e failover de gateway.

10. **Critérios de rollback**
    - Qualquer violação persistente (>30 min) de critérios LAT-01, THR-01, PQC-OVH, RES ou GW-01.
    - Falha de compatibilidade crítica (handshake inválido em clientes obrigatórios) não resolvida em 15 min.
    - Custo incremental > +15% em janela semanal sem justificativa de carga.

> Este protocolo deve ser executado em ciclos iterativos por serviço/tier, registrando evidências e decisões para auditoria e governança de criptoagilidade.
