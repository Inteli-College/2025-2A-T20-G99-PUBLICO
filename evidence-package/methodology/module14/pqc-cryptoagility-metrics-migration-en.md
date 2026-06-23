# Metrics and PQC Migration Protocol — Hybrid Three-Tier Environment

Technical reference to evaluate and execute crypto-agility in a hybrid (on-prem + cloud) three-tier architecture (web/app/data) with a crypto-agility gateway.

## 1. Assumptions and scope
- Services split across data center and public cloud, connected by hybrid mesh/gateway.
- TLS 1.3 traffic, operating classic, hybrid, and post-quantum (PQC) profiles in controlled experiments.
- Standardized observability via OpenTelemetry, SIEM/FinOps integration, and GitOps automation.
- Criteria aligned to Sprint 4–5 goals for performance and resilience validation.

## 2. Performance metrics

| ID | Metric | Description / Formula | Measurement method | Collection tools | Acceptance criteria |
| --- | --- | --- | --- | --- | --- |
| LAT-01 | End-to-end latency | `t_resp = t_end − t_start`; capture p50/p95 per route/tier and delta `Δlat_hybrid = lat_hybrid − lat_onprem`. | Synthetic load and distributed tracing with timing headers at each tier. | k6/Locust, OpenTelemetry (traces), Prometheus/Grafana, service mesh metrics. | p95 ≤ 150 ms for intra-DC calls; `Δlat_hybrid` ≤ 5% vs classic baseline. |
| THR-01 | Effective throughput | `req/s = total_req ÷ window_s` and success rate `success = req_ok ÷ total_req`. | Step/stress load while observing queues/connections per tier. | k6/Locust, mesh metrics, Prometheus, APM/Jaeger. | Within ±5% of classic baseline throughput with `success ≥ 99%` in canary. |
| PQC-OVH-01 | PQC handshake overhead | `ovh = (t_handshake_pqc − t_handshake_classic) ÷ t_handshake_classic`. | Compare classic vs hybrid/PQC on the same route under fixed load. | Wireshark/tcpdump with TLS secrets, OpenTelemetry handshake spans, mesh debug metrics. | `ovh` ≤ 15% and p95 variation ≤ 20 ms per connection. |
| PQC-OVH-02 | Computational overhead (CPU/mem) | `ΔCPU = CPU_pqc − CPU_classic`; `ΔMem = Mem_pqc − Mem_classic` on app and gateway. | Pod/VM profiling during controlled tests (10–15 min). | Prometheus node/exporter, eBPF/profiler, HPA/KEDA metrics. | `ΔCPU` ≤ +20% and `ΔMem` ≤ +15% without throttling. |
| COST-01 | Cloud operational cost | `cost_inc = (cost_pqc − cost_base) ÷ 1M req` including compute + egress + KMS. | Collect daily cost by environment tag and divide by request volume. | AWS/Azure/IBM Cost Explorer, FinOps dashboards, KMS API logs. | Increment ≤ +15% per 1M requests; egress growth ≤ +5%. |
| SEC-01 | Mean time to detect (MTTD) | `MTTD = Σ(t_alert − t_event) ÷ N` for crypto failures/violations. | Inject failures (expired cert, KMS outage) and measure alert time in SIEM. | SIEM (Splunk/QRadar), Prometheus alertmanager, OpenTelemetry. | MTTD ≤ 5 min (canary) for critical events. |
| SEC-02 | Mean time to respond (MTTR) | `MTTR = Σ(t_recovery − t_alert) ÷ N` until healthy profile/rollback is restored. | Run automated playbooks and measure handshake recovery. | ITSM + automation logs, mesh metrics, orchestrated runbooks. | MTTR ≤ 30 min in canary; full rollback ≤ 10 min. |
| RES-01 | Resilience – recovery time | `RTO = t_service_restore − t_failure`; failover success `success = events_recovered ÷ events_total`. | Planned chaos on hybrid routes and gateway, measuring restoration. | Chaos Mesh/Litmus, Prometheus, mesh health checks. | RTO ≤ 15 min; `success` ≥ 99% in canary. |
| RES-02 | Resilience – graceful degradation | `capacity = req_ok_hybrid ÷ req_ok_base` during simulated failures; check error p99. | Load during KMS/PKI faults and partial region loss. | k6/Locust, mesh/APM, circuit breaker logs. | Capacity ≥ 70% of baseline with error p99 < 1%. |
| GW-01 | Crypto-agility gateway efficiency | `effectiveness = actions_applied ÷ actions_recommended`; `lat_gw = p95_gw`; `policy_error = policy_failures ÷ executions`. | Correlate gateway decisions with automation executions and hop latency. | Gateway logs, queues (Kafka/NATS), Prometheus, APM traces. | `effectiveness` ≥ 95%; `lat_gw` p95 ≤ 5 ms; `policy_error` < 1%. |

### Measurement notes
- Always compare classic vs hybrid/PQC in the same window/load to isolate overhead.
- Tag metrics (service, tier, environment, algorithm) to enable per-component dashboards.
- Export time series to the evidence repository (S3/Cloud Object Storage) with ≥30 days retention.

## 3. PQC migration protocol

1. **Map crypto points**
   - Inventory all TLS endpoints, APIs, queues, and storage with CBOM (service/tier manifests).
   - Classify current algorithms (RSA/ECDH/ECDSA) and PKI/KMS dependencies, including embedded libraries.

2. **Select NIST PQC algorithms**
   - Asymmetric: Kyber-768/1024 (KEM) for key exchange; Dilithium-2/3 for signatures; Falcon-512 only when fast verification is required.
   - Define hybrid profiles (e.g., TLS 1.3 with X25519 + Kyber-768) to reduce compatibility risk.

3. **Gradual replacement strategy**
   - Enable hybrid profiles in canary first (1–5% traffic), then staging, then progressive production.
   - Keep dual-stack (classic + PQC) until LAT/THR/PQC-OVH metrics meet criteria for 7 days.

4. **Key rotation and management**
   - Generate PQC key pairs via compatible KMS/Engine; store PQC/hybrid certs in central vault.
   - Automated rotation with <90-day policy and revocation validation (CRL/OCSP) when applicable.

5. **Legacy compatibility**
   - Detect stacks lacking required extensions/algorithms (e.g., TLS 1.2-only devices) and maintain controlled classic fallback.
   - Document exceptions with remediation deadline and monitor usage via CBOM + telemetry.

6. **Fallback flows**
   - Feature flags per service/tier to toggle classic, hybrid, and PQC profiles.
   - Automatic rollback playbook when `ovh > 15%`, `policy_error > 1%`, or LAT/THR/RES violations occur.

7. **Integration with the crypto-agility gateway**
   - Gateway ingests CBOM inventory, produces swap decisions, triggers pipelines, and records evidence (before/after).
   - GW-01 metrics feed dashboards and rollback/chaos triggers.

8. **Migration automation**
   - GitOps pipelines apply changes (TLS/KEM config, libs, certs) with staging validation.
   - Hooks update CBOM manifests and publish metrics automatically after each deploy.

9. **Testing and validation**
   - Functional: handshake tests, client compatibility, certificate/algorithm verification.
   - Performance: run load suite and compare all metrics from section 2 across profiles.
   - Security/resilience: KMS/PKI chaos, forced cert expiration, region failure, and gateway failover.

10. **Rollback criteria**
    - Any persistent (>30 min) violation of LAT-01, THR-01, PQC-OVH, RES, or GW-01 criteria.
    - Critical compatibility failure (invalid handshake on mandatory clients) not resolved within 15 min.
    - Cost increase > +15% over a weekly window without workload justification.

> Execute this protocol iteratively per service/tier, recording evidence and decisions for crypto-agility governance and auditability.
