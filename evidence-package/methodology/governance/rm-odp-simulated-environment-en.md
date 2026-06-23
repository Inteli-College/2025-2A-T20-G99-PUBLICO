# Simulated Environment Requirements — RM-ODP

> Reference blueprint for the hybrid three-tier environment used in the crypto-agility simulation modules. The structure follows the five viewpoints of the **Reference Model of Open Distributed Processing (RM-ODP)**.

## 1. Enterprise View
- **Primary goal**: validate a crypto-agility gateway that orchestrates CBOM-based inventory, PQC/hybrid algorithm swaps, and incident response across corporate environments.
- **Stakeholders**: Security Engineering, SRE/DevOps, GRC, FinOps, and Product Owners represented in the cryptographic change board.
- **Business domains**:  
  1. Inventory & governance (policies, CBOM, metrics).  
  2. Swap execution (pipelines, playbooks, canary testing).  
  3. Observability/telemetry (TLS, KMS, SIEM).  
  4. Resilience & continuity (rollback, crypto-chaos, response plans).  
- **Policies**: algorithm swaps must not degrade service SLOs by >5% without approval; every change must attach CBOM before/after artifacts; harvest-now indicators are handled with highest priority.

## 2. Information View
- **Data models**:  
  - Versioned CBOM manifests per service/tier.  
  - Algorithm-policy catalog (security level, allowed curves, transition windows).  
  - TLS/KEM telemetry datasets (latency, success, compatibility errors).  
  - Cryptographic incident register (MTTD, MTTR, corrective actions).  
- **Quality & governance**: ≥97% accuracy for CBOM, minimum 12-month retention, full traceability requirement → evidence → decision.  
- **Integration**: APIs for consuming CBOM, logs, and indicators by the gateway, dashboards, and audit systems.

## 3. Computational View
- **Logical components**:  
  - Crypto-agility gateway (decision + automation services).  
  - Three-tier simulator (web front, API/microservices, database).  
  - Test orchestrator (canary, load, chaos).  
  - Observability bus (TLS/KEM collectors, KMS events, CBOM ingestion).  
  - Compliance service (RACV matrix, reports, approvals).  
- **Interfaces**: REST/gRPC for inventory/swap requests; webhook/event channels for policy alerts; local agents for CBOM and telemetry harvesting.
- **Contracts**: each component exposes an internal SLA; messages must carry policy version and change IDs for auditability.

## 4. Engineering View
- **Topology**:  
  - Presentation layer on Kubernetes or equivalent managed cluster with configurable TLS termination.  
  - Application layer split into microservices (Web/API, Job Worker, Auth).  
  - Data layer replicated in two zones (relational DB + cache + log storage).  
- **Environments**: dev, staging/canary, and production-simulated, all instrumented with CI/CD pipelines and crypto feature flags.  
- **Supporting services**: Git + automated pipelines, Secrets Manager/KMS, observability stack (Prometheus/Grafana or similar), SIEM.  
- **Non-functional requirements**:  
  - Reproducible deployments via IaC (Terraform/Ansible).  
  - Ability to inject failures (handshake latency, cert expiration, KMS outage).  
  - Centralized audit logging with signed records.

## 5. Technology View
- **Stacks**:  
  - Languages: Go/Java/Python for services; React/Node for the front end.  
  - Crypto libraries: OpenSSL 3.x + liboqs, BoringSSL hybrid patches, PQC reference libs (CRYSTALS-Kyber, Dilithium).  
  - Service mesh/ingress with TLS 1.3 + hybrid profile support.  
  - KMS with programmable rotation (AWS KMS, HashiCorp Vault PQC plugins, IBM Hyper Protect).  
- **Tooling**:  
  - CBOM scanning via IBM CBOM Kit (plus custom extensions).  
  - Observability with OpenTelemetry and TLS/KMS exporters.  
  - Automation pipelines using ArgoCD/GitHub Actions for swap pull requests.  
  - Chaos/performance testing via LitmusChaos, k6, Locust.  
- **Compliance**: alignment with NIST SP 800-208, SP 1800-38, FIPS 203–205; all artifacts and logs digitally signed.

---

> This document defines the minimum contract for any replica of the simulation environment. Deviations must keep the RM-ODP structure and document the rationale.
