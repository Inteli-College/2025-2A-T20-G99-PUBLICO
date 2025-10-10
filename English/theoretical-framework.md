# Theoretical Framework

## 1. Definitions
- Crypto-agility: capability to inventory, swap, and govern algorithms/keys with low friction.  
- PQC: set of algorithms resistant to adversaries with quantum capabilities.  
- Cryptographic resilience: resisting, detecting, and recovering from failures/incidents.

## 2. Conceptual Models
- Crypto-agility pipeline:
  1) Inventory (CBOM)  
  2) Policy and mapping classic→PQC  
  3) Automated execution (patch/PR/rotations)  
  4) Validation and canary tests  
  5) Observability and audit  
  6) Rollback and continuous learning
- Hybrid three-tier architecture as the reference scenario.

## 3. Assumptions
- Availability of toolchains with PQC/hybrid support.  
- Access to cloud simulation environments.  
- Mixed validation: quantitative metrics and qualitative expert interviews.

## 4. Metrics and Indicators
- Inventory coverage (% of services with valid CBOM).  
- Swap time per service (discover → patch → validate → audit).  
- Hybrid handshake success rate.  
- Performance overhead (latency, CPU, memory).  
- Cryptographic MTTR and safe rollback rate.

## 5. Evaluation Methodology
- Controlled experiments in a cloud environment with a reference three-tier system.  
- Comparative analysis versus conventional approaches (manual swap / no CBOM).  
- Expert interviews assessing feasibility and governance.

## 6. Risks and Mitigations
- Client/service incompatibilities: hybrid profiles and canaries.  
- Performance regressions: load testing and per-service profiles.  
- Automation failures: rollback plans, change management, approvals.

## 7. Expected Results
- Reproducible architectural model for crypto-agility.  
- Operational and governance guidelines for corporate adoption.  
- Quantitative evidence of reduced time/errors in PQC migration.
