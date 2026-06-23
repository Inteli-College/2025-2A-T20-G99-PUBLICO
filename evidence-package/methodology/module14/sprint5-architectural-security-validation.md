# Technical Report — Sprint 5 (Module 14)
## Preliminary architectural and security validation

**Project/Artifact**: Crypto-Agility Gateway for PQC migration in a hybrid three-tier environment (web/app/data)  
**Module**: 14  
**Sprint**: 5  
**Date**: 2026-04-07  
**Version**: 1.1  

---

## 1. Purpose and scope

This document consolidates **preliminary (design-time)** and **document-based** validation of the architecture delivered for Module 14, Sprint 5, with an emphasis on **information security** and **crypto-agility** (progressive migration toward post-quantum cryptography — PQC — backed by observability and rollback).

### 1.1 Included scope
- Objective architecture description and justification of key decisions.
- Evidence of architectural adherence to functional and non-functional requirements (performance, resilience, auditability, and security).
- Architectural validation scenarios (static and dynamic inspection) focused on:
  - encryption in transit and at rest;
  - login/authentication and authorization, including MFA;
  - biometrics (when applicable);
  - use of post-quantum algorithms (or technical justification when not implemented).
- Vulnerability analysis, risk classification, and mitigation recommendations.
- Security component map in a **three-tier** architecture.
- Alerts (red flags) and points of attention.

### 1.2 Excluded scope (Sprint boundaries)
- Full implementation of the Kubernetes/mesh/SIEM/FinOps environment in production.
- Implementation of a real Identity Provider (IdP) and MFA for a running system.
- Real deployment of PQC runtime libraries (e.g., OpenSSL+liboqs) in the data plane.

> Note: Sprint 4 focused on **metrics, protocols, and readiness** (PQC migration/rollback). Sprint 5 consolidates **preliminary validation** (document-based) and a **scenario playbook** for static and dynamic inspection.

---

## 2. Project architecture (objective view)

### 2.1 Context
The project follows a hybrid **three-tier** model (presentation, application, and data) and introduces a **Crypto-Agility Gateway** responsible for cryptographic inventory (CBOM), migration decisions (policies), automation, observability, and rollback.

Baseline artifacts:
- Gateway specification: `docs/module14/gateway-architecture.md`.
- Hybrid three-tier environment modeling: `docs/module14/sprint3/hybrid-three-tier-model.md`.
- Metrics and resilience matrix: `docs/module14/metrics-resilience-matrix.md`.
- PQC migration protocol and metrics: `docs/module14/pqc-cryptoagility-metrics-migration.md`.
- Reference prototypes: `code/cbom_gateway.py`, `code/cbomkit_cli.py`.

### 2.2 Logical view (macro-components)
The gateway is event-oriented and organized into cohesive modules:

1. **CBOM Ingest Service**: ingestion/validation/versioning of CBOM manifests per service/tier.
2. **Policy Engine**: policy-based decisions (e.g., disallow legacy TLS; migrate RSA-2048/ECDH-P256).
3. **Automation Orchestrator**: GitOps execution (PRs/playbooks) to update TLS/mTLS profiles, PKI, KMS integration, and libraries.
4. **Telemetry Correlator**: correlation between inventory (CBOM) and runtime signals (handshakes, failures, latency, KMS events).
5. **Rollback & Chaos Engine**: automated fallback/rollback and crypto chaos testing.
6. **Observability & GRC Bus**: auditable evidence (metrics, logs, signed artifacts) for SRE/SecOps/GRC.

### 2.3 Physical view (deployment and integrations)
The target environment is a multi-environment Kubernetes setup (dev/stage/canary/prod-sim) with a service mesh, integrating with:
- **KMS/Secrets Manager** (Vault/Cloud KMS) for key rotation and segregation of duties.
- **Event bus** (Kafka/NATS) to decouple ingestion, decision, and automation.
- **Observability** (OpenTelemetry + mesh metrics) and **SIEM** for detection and response.
- **CI/CD** (GitHub Actions/ArgoCD) as the cryptographic change control plane.

---

## 3. Key architectural decisions (justification)

### 3.1 Three-tier architecture + dedicated gateway (separation of responsibilities)
- **Decision**: keep a three-tier reference architecture for clarity and to control the attack surface, and introduce a dedicated gateway for cryptographic lifecycle management.
- **Rationale**: improves traceability by layer (web/app/data), centralizes policies, reduces ad-hoc crypto changes, and enables tier-based observability.

### 3.2 CBOM-based cryptographic inventory as “source of truth”
- **Decision**: use CBOM (IBM CBOM Kit or a compatible scanner) to inventory algorithms, usage modes, and policy violations.
- **Rationale**: PQC migration requires end-to-end visibility of the cryptographic surface; CBOM supports continuous governance and before/after auditability.

### 3.3 Declarative policies and GitOps automation
- **Decision**: treat “algorithm/key/profile” as versioned configuration; changes flow through PRs and pipelines.
- **Rationale**: reduces operational risk, creates an audit trail, and enables reproducible rollback.

### 3.4 Hybrid approach (classical + PQC) for compatibility
- **Decision**: start with hybrid profiles (classical + PQC) before moving to “PQC-only” where feasible.
- **Rationale**: mitigates client compatibility risks while enabling measurable, incremental adoption and controlled overhead.

### 3.5 Observability and resilience as acceptance criteria
- **Decision**: gate crypto swaps by SLOs and metrics (LAT/THR/OBS/RES), with automated rollback.
- **Rationale**: cryptographic changes can impact latency/CPU and availability; without telemetry and rollback, the operational risk is high.

---

## 4. Requirements adherence (functional and non-functional)

### 4.1 Functional requirements (FR)
The functional scope is addressed through documentation and prototype support:

- **FR-01 Inventory crypto posture per service/tier**: defined in the architecture and demonstrated by `code/cbom_gateway.py` consuming manifests such as `code/samples/cbom-three-tier.json`.
- **FR-02 Decide migration (classical → hybrid/PQC)**: action mapping and recommendations in the prototype; formal protocol in `docs/module14/pqc-cryptoagility-metrics-migration.md`.
- **FR-03 Orchestrate changes via pipelines**: specified in `docs/module14/gateway-architecture.md` (Automation Orchestrator) and RM-ODP (`docs/governance/rm-odp-simulated-environment-pt.md`).
- **FR-04 Measure and correlate telemetry**: metrics defined in `docs/module14/metrics-resilience-matrix.md` and detailed in the PQC metrics/protocol document.
- **FR-05 Perform rollback/fallback and crypto chaos**: protocols and rollback criteria in `docs/module14/pqc-cryptoagility-metrics-migration.md` and `docs/module14/metrics-resilience-matrix.md`.

### 4.2 Non-functional requirements (NFR)
- **NFR-Security**: TLS/mTLS policies, KMS/envelope encryption, harvest-now detection, least privilege, and traceability (see `docs/governance/vulnerabilidades-3tier.md` and `docs/governance/pontos-executivos-hndl.md`).
- **NFR-Performance**: overhead and latency targets (e.g., HYB-02 ≤ 5%; PQC-OVH ≤ 15%) defined in `docs/module14/pqc-cryptoagility-metrics-migration.md`.
- **NFR-Availability/Resilience**: rollback and MTTR targets (RES-01/RES-02) in `docs/module14/metrics-resilience-matrix.md`.
- **NFR-Auditability/Compliance**: before/after CBOM attachment for changes (GOV-01) and retained/signed evidence (RM-ODP + gateway).

---

## 5. Architectural validation scenarios (security-focused)

### 5.1 Validation approach
Sprint 5 validation is **preliminary** and combines:
- **Static inspection** (design review and prototype review): consistency across architecture, requirements, and security mechanisms.
- **Dynamic inspection** (controlled prototype runs and simulations): validate the CBOM→decision flow; verify metrics and rollback triggers in a test setting.

### 5.2 Documented scenarios

#### SCN-01 — CBOM inventory and policy violation detection
- **Goal**: ensure the architecture supports continuous inventory and identifies legacy/high-risk algorithms.
- **Protected asset**: cryptographic visibility (algorithm and key governance).
- **Static inspection**: review ingestion/normalization contracts in `docs/module14/gateway-architecture.md`; review mappings and metrics in `code/cbom_gateway.py`.
- **Dynamic inspection**: run `python3 code/cbom_gateway.py --cbom code/samples/cbom-three-tier.json` and confirm actions for RSA-2048/TLS 1.2 and ECDH-P256/mTLS.
- **Acceptance criteria**: INV-01 (coverage) and INV-02 (precision) in `docs/module14/metrics-resilience-matrix.md`.

#### SCN-02 — Migrate legacy TLS (web) to TLS 1.3 hybrid profile
- **Goal**: demonstrate the “discover→swap” flow with risk control and performance criteria.
- **Protected asset**: confidentiality and PFS for web traffic, reducing HNDL exposure.
- **Static inspection**: verify hybrid profile decision rationale in `docs/module14/pqc-cryptoagility-metrics-migration.md` and in the prototype mappings.
- **Dynamic inspection**: simulate PR/playbook in an academic environment and measure HYB-01/HYB-02; if no real mesh exists, document the test plan and capture synthetic evidence.
- **Acceptance criteria**: HYB-01 > 99% (canary) and HYB-02 ≤ 5%.

#### SCN-03 — Service-to-service mTLS (app) with hybrid profile
- **Goal**: validate that the architecture supports mTLS migration under a service mesh with compatibility and rollback.
- **Protected asset**: service authentication and integrity of internal calls.
- **Static inspection**: review mesh dependency and Automation Orchestrator design in `docs/module14/gateway-architecture.md`.
- **Dynamic inspection**: simulate handshake failures and validate OBS-02/RES-02 triggers.
- **Acceptance criteria**: OBS-02 (MTTD ≤ 5 min) and RES-02 (safe rollback ≥ 99%).

#### SCN-04 — Encryption at rest (data and evidence)
- **Goal**: validate protection of critical data and evidence (CBOM, reports, logs) against unauthorized access.
- **Protected asset**: persisted data (DB, object storage, backups, audit evidence).
- **Static inspection**: review envelope encryption/KMS requirements in RM-ODP and threats in `docs/governance/vulnerabilidades-3tier.md`.
- **Dynamic inspection**: in simulation, verify critical datasets use SSE-KMS/volume encryption and backups are encrypted and signed.
- **Acceptance criteria**: KLC-01 (automated rotation) and GOV-01 (100% of swaps have CBOM before/after).

#### SCN-05 — KMS/Secrets Manager outage
- **Goal**: assess secure behavior under a critical dependency failure.
- **Protected asset**: secure availability and key/certificate consistency.
- **Static inspection**: review fallback/rollback strategy and chaos requirements in `docs/module14/pqc-cryptoagility-metrics-migration.md`.
- **Dynamic inspection**: inject a simulated KMS failure and measure MTTD/MTTR (SEC-01/SEC-02) and RTO (RES-01).
- **Acceptance criteria**: SEC-01 ≤ 5 min; rollback ≤ 10 min; MTTR ≤ 30 min (canary).

#### SCN-06 — CBOM integrity and authenticity (supply chain)
- **Goal**: prevent CBOM tampering and downstream policy decisions based on corrupted data.
- **Protected asset**: inventory integrity and Policy Engine trustworthiness.
- **Static inspection**: assess CBOM signing needs, repository access controls, and pipeline segregation.
- **Dynamic inspection**: simulate a modified manifest and confirm detection (hash/signature invalid) and automation blocking.
- **Acceptance criteria**: GOV-01 and “error_policy < 1%” (GW-01) in `docs/module14/pqc-cryptoagility-metrics-migration.md`.

#### SCN-07 — Authentication and authorization for the control plane (Gateway/APIs)
- **Goal**: ensure privileged operations (swaps, rollback, approvals) are restricted and auditable.
- **Protected asset**: cryptographic change control and telemetry.
- **Static inspection**: validate (i) role segregation (SecOps/SRE/GRC), (ii) immutable audit trail, and (iii) minimal exposure of the gateway.
- **Dynamic inspection**: in a real environment, validate OIDC/MFA and RBAC; for this sprint, record the design and test criteria.
- **Acceptance criteria**: strong authentication + MFA for privileged actions; per-request audit logs.

#### SCN-08 — Legacy client and controlled fallback
- **Goal**: avoid outages caused by incompatibility while controlling security degradation.
- **Protected asset**: service continuity and confidentiality.
- **Static inspection**: verify dual-stack strategy and exception deadlines in `docs/module14/pqc-cryptoagility-metrics-migration.md`.
- **Dynamic inspection**: simulate a TLS 1.2-only client and validate fallback with telemetry and a deprecation deadline.
- **Acceptance criteria**: fallback only on allowed routes and fully observable; progressive reduction of legacy usage.

### 5.3 Controlled execution on an academic server (rootless Podman)

After the document-based consolidation of Sprint 5, the architecture was also exercised on a **real academic server** using rootless `podman`, reducing the gap between design-time validation and an executable simulation of the topology described in `docs/governance/requisitos-ambiente.md` and `docs/module14/sprint4/vm-network-topology.md`.

**Observed environment**
- Ubuntu 24.04.3 LTS host.
- `64` vCPUs (`Intel Xeon Gold 6454S`) and `125 GiB` RAM available on the host.
- Execution with `podman 4.9.3`, rootless mode, and `podman.socket` enabled.
- Simulated topology with `8` logical nodes: `k8s-control`, `k8s-worker-1`, `k8s-worker-2`, `k8s-worker-3`, `data-node`, `security-integration-node`, `observability-node`, and `load-chaos-node`.

**Adjustments required for this runtime**
- Python-node `healthchecks` had to be changed from `CMD` to `CMD-SHELL`, because the server-side `podman compose` provider incorrectly parsed inline Python commands and marked healthy services as `unhealthy`.
- `k6` JSON summaries were written to `/tmp` inside the `load-chaos-node` container and then copied to the host, because the evidence bind mount on that node showed write restrictions for that specific artifact.

**Executed scenario results**

| Scenario | Summary goal | Observed result | Status |
| --- | --- | --- | --- |
| `S4-T01` | Classic baseline under synthetic load | `p95 = 41.78 ms`, `http_req_failed = 0.00%`, `150` successful requests in the test window | approved |
| `S4-T02` | Initial canary against `app-canary` | `p95 = 25.47 ms`, `http_req_failed = 0.00%`, `40` successful requests in the test window | approved |
| `S4-T05` | `discover -> decision -> swap` flow | `code/cbom_gateway.py` produced `2` migration actions (web and app); `code/cbomkit_cli.py` generated a repository manifest with `10` files containing findings and `1023` textual occurrences | approved with methodological caveat |
| `S4-E04` | CBOM integrity/tampering | original manifest produced `2` actions; tampered manifest reduced the output to `1` action, with no internal automation block | important partial failure |

**Interpretation**
- The simulated topology started successfully on the academic server and remained stable enough to execute baseline, canary, and governance-oriented scenarios.
- `S4-T01` and `S4-T02` stayed comfortably below the `LAT-01 p95 <= 150 ms` target, showing that a server-only simulation with isolated logical nodes can still provide useful performance evidence.
- The `discover -> decision -> swap` flow was confirmed in an actual runtime environment, strengthening practical adherence to `FR-01`, `FR-02`, and `FR-03`.
- `S4-E04` confirmed a **real prototype gap**: the manifest tampering was observable through external hashing, but the gateway did not reject the corrupted artifact; instead, it stopped recommending the migration action for the `web` layer. This reinforces risk `V-03` and validates the need for signature/hash enforcement in the control plane.

**Evidence generated**
- Consolidated evidence archive on the server: `~/infra/logs/module14-podman-evidence.tgz`.
- Load summaries: `~/infra/logs/S4-T01-k6-summary.json`, `~/infra/logs/S4-T02-k6-summary.json`.
- Load textual outputs: `~/infra/logs/S4-T01-k6-output.txt`, `~/infra/logs/S4-T02-k6-output.txt`.
- Additional in-lab evidence under `lab/topology/runtime/evidence/...`.

---

## 6. Security controls: implementation status

This section explicitly states **(a) what is implemented as a repository prototype**, **(b) what is specified for the target environment**, and **(c) gaps/limitations**.

### 6.1 Encryption in transit

**Target architecture (specified)**
- TLS 1.3 at the edge (CDN/WAF/ingress) and **mTLS** for east-west traffic (service mesh).
- **Hybrid** profiles (classical + PQC) to mitigate compatibility risk, as defined in `docs/module14/pqc-cryptoagility-metrics-migration.md`.
- Handshake/failure telemetry via OpenTelemetry/mesh (`docs/module14/metrics-resilience-matrix.md`).

**Prototype (implemented)**
- `code/cbom_gateway.py` flags legacy TLS (e.g., TLS 1.2 + RSA-2048 in the sample) and recommends migrating to “TLS 1.3 hybrid (Kyber-768 + RSA-3072)”.

**Gaps (justified)**
- Actual TLS/mTLS termination and mesh instrumentation require a Kubernetes/mesh environment (outside the scope of this sprint’s code artifacts).

### 6.2 Encryption at rest

**Target architecture (specified)**
- **Envelope encryption with KMS** for critical data (DB, object storage, backups), with rotation and audit (`docs/governance/vulnerabilidades-3tier.md`).
- Evidence and backups integrity via digital signatures (planned in RM-ODP and the gateway).

**Prototype (implemented)**
- The sample manifest `code/samples/cbom-three-tier.json` includes “AES-256 data-at-rest/tablespace”, enabling inventory-level posture tracking.

**Gaps (justified)**
- Real KMS/DB/storage configuration is not part of the prototype; validation is by design and by simulation acceptance criteria.

### 6.3 Login and authentication (control plane)

**Target architecture (specified)**
- Gateway APIs/dashboards protected via **OIDC/OAuth2**, short-lived tokens (JWT), and **RBAC** (SRE/SecOps/GRC).
- Strict separation between **data plane** (application traffic) and **control plane** (decisions/automation), with network restriction (zero trust) and auditability.

**Prototype (implemented)**
- Repository scripts are local tools and **do not expose authenticated APIs**.

**Gaps (justified)**
- IdP, endpoints, and RBAC are expected as part of the full simulation environment (next module). In this sprint, this control is captured as a requirement and scenario (SCN-07).

### 6.4 Multi-factor authentication (MFA)

**Target architecture (specified)**
- Mandatory MFA for privileged users in the IdP (e.g., FIDO2/WebAuthn, TOTP, or push), with step-up authentication for high-risk actions (approve swaps, trigger rollback, change policies).
- MFA is also recommended for source control and CI/CD access.

**Prototype (implemented)**
- Not applicable (local tools).

### 6.5 Biometrics (when applicable)

**Target architecture (optional)**
- Biometrics may be used indirectly through **passkeys (FIDO2/WebAuthn)** depending on the IdP and risk appetite.

**Rationale**
- Biometrics are not a core crypto-agility requirement; they are a strong authentication mechanism for reducing credential compromise risk in the control plane.

### 6.6 Post-quantum algorithms (PQC) and crypto-agility

**Target architecture (specified)**
- Adoption aligned to NIST recommendations (FIPS 203–205) and hybrid strategy:
  - KEM: Kyber (levels selected based on risk/overhead)
  - Signatures: Dilithium/Falcon/SPHINCS+ depending on use case
- Governance through metrics (PQC-OVH, HYB, GOV, RES) and incremental rollout (canary → staging → production).

**Prototype (implemented)**
- The prototype does not execute PQC primitives; it **recommends** target profiles and prioritizes swaps based on CBOM findings.

**Technical justification for not executing PQC in the prototype**
- The prototype’s purpose is to support **inventory, decisioning, and traceability**. Executing PQC requires runtime dependencies (libraries, mesh, endpoints) and integration with the target environment.

---

## 7. Vulnerability analysis (risks and mitigation)

The following issues consider the hybrid three-tier environment, the gateway/control plane, and software supply chain risks. Risk is classified as **low/medium/high** based on likelihood and impact.

| ID | Vulnerability (architectural/security) | Layer | Risk | Potential impact | Recommended mitigation |
|---|---|---|---|---|---|
| V-01 | Legacy TLS / weak cipher suites / lack of PFS | Presentation/App | High | MITM, downgrade, HNDL data capture | Enforce TLS 1.2+/1.3; cipher suite policy; CBOM inventory; hybrid migration with canary and rollback; monitor handshakes (OBS-01/02). |
| V-02 | Weak authentication/authorization in the control plane | Application (gateway) | High | Malicious crypto changes; improper rollback; loss of trust | OIDC/OAuth2 + RBAC; mandatory MFA; network segmentation; immutable audit; change approvals (GRC). |
| V-03 | CBOM manifest tampering (supply chain) | App/Data | High | Wrong policy decisions; insecure swaps; hiding legacy crypto | Sign CBOM; store immutably; validate hash/signature; pipeline-based access control; before/after evidence (GOV-01). |
| V-04 | Hardcoded secrets and long-lived keys | App/Data | High | Credential exfiltration; lateral compromise | Secrets Manager/KMS; automated rotation (KLC-01); secret scanners; least privilege; code review. |
| V-05 | KMS dependency without tested contingency | Data/App | Medium | Outage, decrypt failures, availability incidents | Safe caching/TTL; contingency procedures; chaos testing; circuit breakers; monitor and measure MTTR (SEC-02/RES). |
| V-06 | Insufficient crypto telemetry | All | Medium | Late detection; weak audit evidence | OpenTelemetry + handshake/KMS logs; SIEM alerts; MTTD (OBS-02) and change trail. |
| V-07 | Hybrid/PQC compatibility issues (legacy clients) | Presentation/App | Medium | Service disruption; overly broad fallback weakens security | Controlled dual-stack; time-bounded exceptions; per-route feature flags; client dashboards; rollback criteria. |
| V-08 | Expanded attack surface via automation (CI/CD) | App | Medium | Compromised PR/pipeline alters policies/crypto | Branch protection; signed commits; mandatory reviews; environment separation; keep secrets out of CI; auditing. |
| V-09 | Logs containing sensitive data (e.g., tokens, PII) | App/Data | Medium | Exposure via SIEM/storage; compliance issues | Masking/tokenization; minimal retention; classification; access controls; encryption at rest. |
| V-10 | Event bus without strong controls (authz/crypto) | App | Medium | Event injection, replay, decision diversion | mTLS between producers/consumers; service auth; signatures/nonce; topic ACLs; auditing. |

---

## 8. Security component map (three-tier)

### 8.1 Presentation layer (Web)
**Critical security components**
- CDN/WAF, rate limiting, DDoS protection.
- TLS 1.3 termination (preferably hybrid) and cipher suite policy.
- API gateway (when applicable) with JWT validation and secure routing.

**Sensitive transactions**
- User login and token issuance.
- Session establishment and PII-bearing traffic.

**Critical data (where it resides)**
- Cookies/sessions (client and/or edge), authentication metadata, TLS/cert configuration.

### 8.2 Application layer (App)
**Critical security components**
- Service mesh with mTLS, L7 authorization policies, and observability.
- Crypto-agility gateway (Policy Engine, Automation, Telemetry, Rollback).
- CI/CD controls (integrity, review, environment segregation).

**Sensitive transactions**
- Policy decisions and pipeline execution.
- Certificate/secret rotation and rollback execution.
- Security telemetry and alerts.

**Critical data (where it resides)**
- Declarative policies, recorded decisions, automation tokens, test evidence.

### 8.3 Data layer (Data)
**Critical security components**
- Relational DB (volume/tablespace encryption) and access controls.
- Object storage (evidence/CBOM) with SSE-KMS.
- KMS/Secrets Manager (Vault/Cloud KMS) with rotation and auditing.

**Sensitive transactions**
- Encrypt/decrypt operations via KMS.
- Key rotation and certificate issuance.
- Backup/restore and integrity verification.

**Critical data (where it resides)**
- Keys/certificates (KMS), business data (DB), evidence and logs (storage/SIEM).

---

## 9. Alerts and points of attention (Red Flags)

1. **Control plane without strong authentication** (if deployed without OIDC/MFA): high risk of takeover and malicious crypto policy changes.
2. **CBOM without integrity controls (signing/hashing)**: enables tampering and incorrect policy decisions.
3. **Automation without governance (branch protection/reviews)**: CI/CD becomes the primary attack vector.
4. **KMS dependency without chaos/contingency testing**: failures can break services and prevent rollback.
5. **Broad fallback to legacy TLS**: preserves availability but undermines confidentiality and PQC objectives.
6. **Insufficient telemetry**: prevents SLO validation, MTTD/MTTR measurement, and auditable evidence.
7. **Unmeasured PQC overhead**: risk of silent latency/cost regressions and operational rejection of migration.

---

## 10. Conclusion and next steps

In Sprint 5, the architecture is validated both **documentally** and through a **controlled server-only simulation** for coherence across the three-tier model, the crypto-agility gateway, metrics, migration protocols, and resilience mechanisms. The available prototype supported the **inventory and migration recommendation** flow based on CBOM, enabling initial evidence and allowing baseline/canary measurements in an actual runtime environment.

**Recommended next steps (for full dynamic validation)**
- Evolve the simulation toward real or closer equivalents of service mesh/KMS/SIEM per `docs/governance/rm-odp-simulated-environment-pt.md`.
- Implement OIDC + RBAC + MFA for the control plane (SCN-07).
- Add CBOM signing and mandatory blocking of tampered artifacts (SCN-06).
- Complete the remaining dynamic scenarios (`S4-T03`, `S4-E01`, `S4-E02`, `S4-E03`) and collect LAT/THR/PQC-OVH/OBS/RES metrics with standardized evidence retention.

---

## Appendix A — Minimal evidence and verification commands

### A.1 Running the CBOM Gateway prototype

1. Generate/use a sample CBOM manifest.
   - Existing sample: `code/samples/cbom-three-tier.json`.

2. Run the report:
   - `python3 code/cbom_gateway.py --cbom code/samples/cbom-three-tier.json`

3. Expected evidence:
   - Actions generated for **RSA-2048/TLS 1.2** (web) and **ECDH-P256/mTLS** (app) recommending a hybrid profile.

### A.2 Generating a CBOM manifest (simplified scanner)

- Example execution (adjust paths):
  - `python3 code/cbomkit_cli.py --target web-portal:web:src/frontend --target api-orders:app:src/backend --target ledger-db:data:infra/db --output cbom-manifest.json`

> Note: the simplified scanner searches for textual occurrences of algorithms. In a real environment, IBM CBOM Kit and build/runtime integrations are recommended.

### A.3 Running the simulated topology with Podman

On the academic server, the simulation ran with rootless `podman` and an external `compose` provider:

```bash
systemctl --user enable --now podman.socket
podman compose -f lab/topology/docker-compose.yml up -d --build
podman compose -f lab/topology/docker-compose.yml ps
```

Baseline execution:

```bash
podman exec load-chaos-node sh -lc 'k6 run /scripts/baseline.js --summary-export /tmp/S4-T01-k6-summary.json'
podman cp load-chaos-node:/tmp/S4-T01-k6-summary.json ~/infra/logs/S4-T01-k6-summary.json
```

Canary execution:

```bash
podman exec load-chaos-node sh -lc 'BASE_URL=http://k8s-worker-3:8080 k6 run /scripts/canary.js --summary-export /tmp/S4-T02-k6-summary.json'
podman cp load-chaos-node:/tmp/S4-T02-k6-summary.json ~/infra/logs/S4-T02-k6-summary.json
```

CBOM flow execution:

```bash
podman exec k8s-control sh -lc "
python /workspace/code/cbom_gateway.py \
  --cbom /workspace/code/samples/cbom-three-tier.json \
  --output /evidence/scenarios/S4-T05/gateway/cbom-summary.json
"
```

---

## Normative references and best practices (selected)

- NIST — FIPS 203/204/205 (PQC: KEM and digital signatures).
- NIST — SP 800-208 (Stateful Hash-Based Signatures) and related guidance.
- NIST — SP 1800-38 (applied PQC migration/integration guidance).
- OWASP — ASVS/Top 10 (authentication, session management, logging, and data protection controls).
- Security-by-design, zero trust, and segregation of duties in the control plane.
