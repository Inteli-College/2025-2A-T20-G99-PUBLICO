# Public Report – Module 15
## Project: Crypto-Agility in Hybrid Corporate Environments for Post-Quantum Transition

### Context
Module 15 consolidates the project from theoretical foundations and vulnerability diagnosis through **architectural design**, **crypto-agility operationalization**, **simulated environment deployment**, and **security-focused validation with runtime evidence**. The target context is a **hybrid three-tier environment** (on-premises + cloud), where cryptographic dependencies are inventoried, governed, migrated (classic → hybrid/PQC), and continuously monitored with safe rollback.

### Module 15 goal
Deliver a coherent, replicable, and **validated** architecture that:
- Centralizes cryptographic governance and algorithm agility through a **Crypto-Agility Gateway**.
- Supports controlled PQC adoption (especially through **hybrid profiles**) and operational resilience.
- Provides **metrics, protocols, and validation scenarios** backed by executable simulation and runtime evidence.
- Demonstrates practical feasibility through a **containerized 8-node simulation** on a real academic server.

---

## Sprint-by-sprint deliverables (Sprints 1–5)

### Sprint 1 — Baseline foundations
Activities establishing the baseline for the module:
- Vulnerability mapping for three-tier environments.
- Literature review and gap analysis (PQC, crypto-agility, resilience).
- Initial mapping of the IBM CBOM Kit as an inventory source.

**Outcome**: defined the problem space and security drivers to justify crypto-agility as an end-to-end capability (inventory → change → detection → recovery).

### Sprint 2 — Crypto-Agility Gateway specification + CBOM decision prototype
Deliverables:
- Gateway architecture specification (logical modules, event flows, integrations).
- Prototype script to ingest CBOM-like manifests and produce actionable migration recommendations (classic → hybrid/PQC profiles).

**Outcome**: established a governance and automation-friendly gateway model, enabling "CBOM → policy decision → automation/rollback" as a repeatable control loop.

### Sprint 3 — Hybrid three-tier environment modeling (web/app/data)
Deliverables:
- Conceptual hybrid three-tier model (logical/physical/data perspectives).
- Flow diagrams for CBOM collection, TLS/mTLS inter-tier communication, observability, and incident response.
- Requirements traceability between architectural decisions and security constraints.

**Outcome**: created a clear blueprint for where cryptography exists, where it must be instrumented, and where sensitive transactions and critical data reside.

### Sprint 4 — Metrics, PQC migration protocol, resilience and rollback criteria
Deliverables:
- Metrics and resilience matrix (inventory coverage, success rate, latency overhead, MTTD/MTTR, rollback success, cost impact).
- PQC migration protocol with staged rollout, compatibility strategy, and explicit rollback/fallback gates.
- 8-node VM/network topology specification and experimental scenarios.

**Outcome**: operationalized crypto-agility with measurable acceptance thresholds and well-defined rollback to preserve security and availability.

### Sprint 5 — Architectural validation, simulated environment deployment, and security validation
Deliverables:
- Technical validation report (PT/EN) with document-based and runtime validation.
- Containerized lab topology with **8 logical nodes** deployed on an academic server.
- Execution of experimental scenarios (baseline, canary, CBOM flow, integrity testing) with collected evidence.
- Explicit treatment of encryption (in transit/at rest), authentication, MFA, biometrics (when applicable), and PQC readiness.
- Vulnerability analysis with risk classification (low/medium/high), mitigations, and red flags.

**Outcome**: consolidated the module into a validated package with runtime evidence, demonstrating practical feasibility of the proposed architecture.

---

## Architecture summary (public view)

### Three-tier layers
- **Presentation (Web)**: CDN/WAF/ingress termination, TLS policy enforcement, user-facing endpoints.
- **Application (App)**: microservices and service mesh with mTLS and policy enforcement; crypto-agility gateway control plane.
- **Data (Data)**: databases, backups, evidence storage, KMS/Secrets Manager, auditing.

### Crypto-Agility Gateway (control plane)
Key modules:
- **CBOM ingest** (inventory intake + versioning)
- **Policy engine** (algorithm/profile decisions)
- **Automation orchestrator** (GitOps playbooks, configuration swaps)
- **Telemetry correlator** (runtime signals and compliance evidence)
- **Rollback & chaos engine** (safe reversal + resilience testing)
- **Observability & GRC bus** (auditable evidence and reporting)

---

## Simulated environment and validation

### 8-node containerized topology
The architecture was exercised on a real academic server (Ubuntu 24.04 LTS, 64 vCPUs Intel Xeon Gold 6454S, 125 GiB RAM) using rootless Podman containers to simulate the 8-node reference topology:

| Node | Role | Technology |
| --- | --- | --- |
| `k8s-control` | Cluster control plane | Python mock service |
| `k8s-worker-1` | Web tier (baseline) | Python mock service |
| `k8s-worker-2` | Application tier | Python mock service + PostgreSQL client |
| `k8s-worker-3` | Application tier (canary) | Python mock service + PostgreSQL client |
| `data-node` | Data tier | PostgreSQL |
| `security-integration-node` | Security/KMS integration | Python mock service |
| `observability-node` | Monitoring and telemetry | Prometheus |
| `load-chaos-node` | Load and chaos testing | Grafana k6 |

Network isolation was achieved through five dedicated Docker/Podman networks: `ingress_net`, `cluster_net`, `data_net`, `security_net`, and `observability_net`.

### Executed scenario results

| Scenario | Summary goal | Observed result | Status |
| --- | --- | --- | --- |
| S4-T01 | Classic baseline under synthetic load | p95 = 41.78 ms, http_req_failed = 0.00%, 150 successful requests | Approved |
| S4-T02 | Canary deployment against `app-canary` route | p95 = 25.47 ms, http_req_failed = 0.00%, 40 successful requests | Approved |
| S4-T05 | `discover → decision → swap` CBOM flow | Gateway produced 2 migration actions (web + app); scanner identified 10 files with 1023 crypto occurrences | Approved (methodological caveat) |
| S4-E04 | CBOM integrity/tampering test | Original manifest: 2 actions; tampered manifest: 1 action, no internal automation block | Important partial failure |

### Key findings
- Baseline and canary scenarios stayed well below the `LAT-01 p95 ≤ 150 ms` threshold, demonstrating simulation viability on a single host with logical isolation.
- The `discover → decision → swap` flow was confirmed in a runtime environment, strengthening practical adherence to functional requirements.
- The CBOM integrity test revealed a **real prototype gap**: manifest tampering was externally observable via hashing, but the gateway did not reject the tampered artifact internally. This validates the need for mandatory signature/hash enforcement in the control plane.

---

## Security posture (explicit coverage)

### Encryption
- **In transit**: TLS 1.3 at the edge + mTLS east-west; hybrid profiles for incremental PQC adoption.
- **At rest**: envelope encryption using KMS/Secrets Manager; encrypted backups and auditable evidence storage.

### Authentication and MFA
- Control-plane operations require strong authentication (OIDC/OAuth2), RBAC, immutable audit logs, and **mandatory MFA** for privileged actions.

### Biometrics
- Treated as optional and indirect via passkeys (FIDO2/WebAuthn), depending on the Identity Provider.

### Post-quantum cryptography (PQC)
- PQC adoption is defined by protocols and metrics (Kyber for KEM; Dilithium/Falcon/SPHINCS+ for signatures depending on use cases).
- Hybrid approach is preferred first to mitigate client compatibility risk.

---

## Key risks and red flags (public summary)
- Control plane without OIDC/RBAC/MFA becomes a high-risk takeover target.
- Unsigned/unauthenticated CBOM manifests introduce supply-chain integrity risk (confirmed by S4-E04 testing).
- CI/CD without governance (reviews/branch protection) turns automation into an attack vector.
- KMS dependency without chaos/contingency testing can cause outages and block recovery.
- Excessive fallback to legacy TLS undermines confidentiality and PQC goals.

---

## Conclusion and next steps
Module 15 concludes with a validated architecture backed by both document-based review and controlled runtime evidence. The containerized 8-node simulation demonstrated that the proposed topology is executable and produces measurable, auditable results under realistic conditions.

Recommended next steps:
- Evolve the simulation toward real service mesh/KMS/SIEM equivalents.
- Implement OIDC + RBAC + MFA in the control plane.
- Add mandatory CBOM signing and blocking of tampered artifacts.
- Complete remaining dynamic scenarios and collect full LAT/THR/PQC-OVH/OBS/RES metrics with standardized evidence retention.
