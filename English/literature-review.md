# Literature Review: PQC, Crypto-Agility, and Resilience

## 1. Introduction
This review consolidates fundamentals of post-quantum cryptography (PQC), crypto-agility principles, and resilience guidelines (resist, detect, recover) applied to hybrid three-tier corporate architectures.

## 2. PQC Fundamentals
- Main classes: lattice-based (KEMs/signatures), code-based (e.g., McEliece), hash-based (e.g., SPHINCS+), isogeny-based.  
- Adoption properties: key/signature/ciphertext sizes, handshake latency, memory footprint, library maturity, and toolchain support (OpenSSL/liboqs, BoringSSL forks, Java/.NET bindings).

## 3. Crypto-Agility
- Definition: capability to inventory, switch, and orchestrate algorithms and keys with low operational friction.  
- Elements: inventory (CBOM), policy and mapping rules, automated execution (patching/PRs), continuous monitoring and audit.  
- Design patterns: separation of crypto policies, cryptographic abstraction layers, use of KMS/HSM, and safe rollback paths.

## 4. Cyber Resilience
- Tactics: resist (hardening and prevention), detect (telemetry and anomalies), recover (rotations, safe rollback, recomposition).  
- Indicators: cryptographic MTTR, algorithm-swap success rate, inventory coverage, cryptographic chaos testing.

## 5. Tools and Ecosystem
- Inventory/compliance: CBOM, SBOM extensions.  
- Libraries and toolchains: OpenSSL 3.x + PQC via liboqs; language wrappers.  
- Cloud: KMS and Certificate Managers; CDN and load-balancer integration.  
- Observability: APM, TLS logs, handshake metrics, and compatibility errors.

## 6. Practical Challenges
- Legacy compatibility and constrained devices.  
- Hybrid handshakes (classic + PQC) and performance impact.  
- Governance: change approvals, policy versioning, environment segregation.

## 7. Synthesis for the Project
The literature indicates that a successful PQC transition requires accurate inventory, automated replacement, and resilience mechanisms. The project adopts this triad as an architectural guide.
