# CBOM-Driven Crypto-Agility for Post-Quantum Migration

This repository presents the undergraduate thesis by Thomaz Klifson Falcão Barboza:

**CBOM-Driven Crypto-Agility for Post-Quantum Migration in Hybrid Three-Tier Environments**  
**Method and Experimental Validation in a Simulated Banking Topology**

The work proposes a Cryptography Bill of Materials (CBOM)-driven crypto-agility roadmap for governing the migration from classical public-key cryptography to post-quantum-ready approaches in hybrid enterprise architectures.

## Thesis Scope

The thesis focuses on crypto-agility as an operational governance problem, not only as a cryptographic primitive replacement. It studies how organizations can inventory cryptographic dependencies, prioritize migration decisions, deploy changes gradually, observe runtime behavior, and define rollback criteria across hybrid three-tier systems.

The proposed method combines:

- CBOM and SBOM-based inventory of cryptographic dependencies.
- Policy-driven migration decisions.
- A crypto-agility governance gateway.
- Canary deployment for controlled rollout.
- Observability and evidence retention.
- Rollback and recovery criteria for migration failures.

The validation uses a simulated banking topology with eight logical nodes, rootless Podman, and k6 scenarios to evaluate functional behavior, latency, stress response, and recovery under simulated secret-service unavailability.

## Repository Contents

| File | Description |
| --- | --- |
| [TCC_Thomaz_Klifson_EN.pdf](<TCC_Thomaz_Klifson_EN.pdf>) | English version of the thesis. |
| [TCC_Thomaz_Klifson_PT.pdf](<TCC_Thomaz_Klifson_PT.pdf>) | Portuguese version of the thesis. |
| [TERMO DE AUTORIZAÇÃO DE PUBLICAÇÃO DE TRABALHO ACADÊMICO - Título em EN.pdf](<TERMO DE AUTORIZAÇÃO DE PUBLICAÇÃO DE TRABALHO ACADÊMICO - Título em EN.pdf>) | Publication authorization document associated with the English title. |
| [TERMO DE AUTORIZAÇÃO DE PUBLICAÇÃO DE TRABALHO ACADÊMICO - Título em PT.pdf](<TERMO DE AUTORIZAÇÃO DE PUBLICAÇÃO DE TRABALHO ACADÊMICO - Título em PT.pdf>) | Publication authorization document associated with the Portuguese title. |
| [LICENSE](<LICENSE>) | Repository license. |
| [2025-2A-T20-G99-INTERNO.code-workspace](<2025-2A-T20-G99-INTERNO.code-workspace>) | VS Code workspace metadata for opening the repository locally. |

## Academic Context

- **Author:** Thomaz Klifson Falcão Barboza
- **Advisor:** Prof. Reginaldo Arakaki
- **Institution:** Institute of Technology and Leadership (Inteli)
- **Program:** Bachelor of Computer Science
- **Year:** 2026

## Keywords

Crypto-agility, post-quantum cryptography, CBOM, three-tier architecture, cryptographic migration.
