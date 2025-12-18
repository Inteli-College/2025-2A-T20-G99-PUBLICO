# Public Report – Module 14
## Project: Crypto-Agility in Hybrid Corporate Environments for Post-Quantum Transition

### Context
Module 14 advances the project from the theoretical and diagnostic foundation (Module 13) into **architectural design**, **crypto-agility operationalization**, and **preliminary security-focused validation**. The target context is a **hybrid three-tier environment** (on-premises + cloud), where cryptographic dependencies must be inventoried, governed, migrated (classic → hybrid/PQC), and continuously monitored with safe rollback.

### Module 14 goal
Deliver a coherent, replicable architecture that:
- Centralizes cryptographic governance and algorithm agility through a **Crypto-Agility Gateway**.
- Supports controlled PQC adoption (especially through **hybrid profiles**) and operational resilience.
- Provides **metrics, protocols, and validation scenarios** that can be executed in a simulated environment in subsequent modules.

---

## Sprint-by-sprint deliverables (Sprints 1–5)

### Sprint 1 — Baseline foundations (carried from Module 13)
Although Sprint 1’s activities were performed in Module 13, they are the baseline for Module 14:
- Vulnerability mapping for three-tier environments.
- Literature review and gap analysis (PQC, crypto-agility, resilience).
- Initial mapping of the IBM CBOM Kit as an inventory source.

**Outcome**: defined the problem space and security drivers to justify crypto-agility as an end-to-end capability (inventory → change → detection → recovery).

### Sprint 2 — Crypto-Agility Gateway specification + CBOM decision prototype
Deliverables:
- Gateway architecture specification (logical modules, event flows, integrations).
- Prototype script to ingest CBOM-like manifests and produce actionable migration recommendations (classic → hybrid/PQC profiles).

**Outcome**: established a governance and automation-friendly gateway model, enabling “CBOM → policy decision → automation/rollback” as a repeatable control loop.

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

**Outcome**: operationalized crypto-agility with measurable acceptance thresholds and well-defined rollback to preserve security and availability.

### Sprint 5 — Preliminary architectural validation and security validation playbook
Deliverables:
- Technical validation report (PT/EN) documenting:
  - objective architecture description;
  - architectural decision rationale;
  - adherence to functional and non-functional requirements;
  - security-focused validation scenarios (static inspection and dynamic inspection);
  - explicit treatment of encryption (in transit/at rest), authentication, MFA, biometrics (when applicable), and PQC readiness;
  - vulnerability analysis with risk classification (low/medium/high), mitigations, and red flags.

**Outcome**: consolidated the module into a documented validation package, ready to guide the simulation and evidence collection phase.

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
- Unsigned/unauthenticated CBOM manifests introduce supply-chain integrity risk.
- CI/CD without governance (reviews/branch protection) turns automation into an attack vector.
- KMS dependency without chaos/contingency testing can cause outages and block recovery.
- Excessive fallback to legacy TLS undermines confidentiality and PQC goals.

---

## Next steps
Module 14 concludes with architectural readiness. The next phase is to execute the defined scenarios in a simulated environment:
- Implement a minimal control plane with OIDC + RBAC + MFA.
- Deploy mesh/KMS/observability and run staged tests (load + chaos).
- Collect evidence for the defined metrics and validate rollback behavior.

