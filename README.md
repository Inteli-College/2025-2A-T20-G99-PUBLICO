# CBOM-Driven Crypto-Agility for Post-Quantum Migration

This repository presents the undergraduate thesis by Thomaz Klifson Falcao Barboza:

**CBOM-Driven Crypto-Agility for Post-Quantum Migration in Hybrid Three-Tier Environments**  
**Method and Experimental Validation in a Simulated Banking Topology**

The work proposes a Cryptography Bill of Materials (CBOM)-driven crypto-agility roadmap for governing the migration from classical public-key cryptography to post-quantum-ready approaches in hybrid enterprise architectures.

## What This Repository Contains

This public repository contains the thesis documents and the evidence package needed to understand, audit, and partially reproduce the experimental claims reported in the work.

| Path | Description |
| --- | --- |
| [TCC_Thomaz_Klifson_EN.pdf](<TCC_Thomaz_Klifson_EN.pdf>) | English version of the thesis. |
| [TCC_Thomaz_Klifson_PT.pdf](<TCC_Thomaz_Klifson_PT.pdf>) | Portuguese version of the thesis. |
| [evidence-package/](<evidence-package/>) | Public evidence package with raw experiment outputs, topology files, CBOM prototypes, methodology documents, traceability notes, and SHA-256 hashes. |
| [TERMO DE AUTORIZAÇÃO DE PUBLICAÇÃO DE TRABALHO ACADÊMICO - Título em EN.pdf](<TERMO DE AUTORIZAÇÃO DE PUBLICAÇÃO DE TRABALHO ACADÊMICO - Título em EN.pdf>) | Publication authorization document associated with the English title. |
| [TERMO DE AUTORIZAÇÃO DE PUBLICAÇÃO DE TRABALHO ACADÊMICO - Título em PT.pdf](<TERMO DE AUTORIZAÇÃO DE PUBLICAÇÃO DE TRABALHO ACADÊMICO - Título em PT.pdf>) | Publication authorization document associated with the Portuguese title. |
| [LICENSE](<LICENSE>) | Repository license. |
| [2025-2A-T20-G99-INTERNO.code-workspace](<2025-2A-T20-G99-INTERNO.code-workspace>) | VS Code workspace metadata for opening the public repository alongside the internal workspace locally. |

## Thesis Scope

The thesis treats crypto-agility as an operational governance problem, not only as the replacement of cryptographic primitives. It studies how organizations can:

- inventory cryptographic dependencies through CBOM and SBOM artifacts;
- classify risks and policy violations;
- decide migration actions through a governance gateway;
- deploy changes gradually through canary rollout;
- observe runtime behavior and retain evidence;
- define rollback and recovery criteria for cryptographic migration failures.

The validation uses a simulated banking topology with eight logical nodes, rootless Podman, and k6 scenarios. The experiments evaluate functional behavior, latency, stress response, controlled baseline-versus-canary comparison, and recovery after simulated secret-service unavailability.

## Evidence Package

The [evidence-package/](<evidence-package/>) directory is the technical support material for the thesis results. It was assembled from the internal repository so the public repository can retain the artifacts behind the reported evidence.

Its internal README, [evidence-package/README.md](<evidence-package/README.md>), is the best entry point. It explains the package structure and maps each experimental claim to the files that support it.

Main sections:

| Path | Purpose |
| --- | --- |
| [evidence-package/revalidation/](<evidence-package/revalidation/>) | Raw revalidated experiment evidence, including k6 JSON summaries, k6 textual outputs, HTTP captures, stress results, dependency-failure captures, and runtime state. |
| [evidence-package/reproducibility/](<evidence-package/reproducibility/>) | CBOM prototype code, sample manifests, k6 scripts, simulated lab topology, mock services, Prometheus config, and lab control script. |
| [evidence-package/methodology/](<evidence-package/methodology/>) | Scenario definitions, metrics, acceptance criteria, topology documentation, security-validation notes, and governance material. |
| [evidence-package/article-source/](<evidence-package/article-source/>) | Article source files and bibliography used for traceability between the written results and the public artifacts. |
| [evidence-package/archives/](<evidence-package/archives/>) | Original compressed revalidation evidence bundle retained for provenance. |
| [evidence-package/MANIFEST.sha256](<evidence-package/MANIFEST.sha256>) | SHA-256 hashes for the files in the evidence package. |

## Main Experimental Evidence

The principal observed results are stored under `evidence-package/revalidation/`:

| Scenario | Evidence summary | Supporting files |
| --- | --- | --- |
| S4-T01 baseline | 150 requests, 0 HTTP failures, p95 39.71 ms. | `revalidation/S4-T01/` |
| S4-T02 canary | 40 requests, 0 HTTP failures, p95 24.70 ms. | `revalidation/S4-T02/` |
| S4-T03 app-chain | Functional app, mock-vault, database, and canary chain; elapsed time 51.17 ms. | `revalidation/S4-T03/app-chain.json` |
| S4-COMP | Controlled baseline versus canary comparison with same route, 5 VUs, 30 s, and 150 requests per node. | `revalidation/S4-COMP-*`, `revalidation/S4-COMP-comparison.md` |
| S4-E03 stress | 10,000 requests completed without HTTP failures, but p95 1149.64 ms violated LAT-01. | `revalidation/S4-E03-stress/` |
| S4-E01 dependency failure | Simulated mock-vault/KMS unavailability returned HTTP 500 during failure and recovered to HTTP 200 after restart. | `revalidation/S4-E01-kms-unavailable/` |

## Interpretation Limits

The evidence package intentionally preserves both successful and limiting results. The thesis does not claim that the simulated environment proves production readiness.

Important boundaries:

- S4-T03 validates functional chaining over HTTP; it does not demonstrate real mTLS.
- S4-E01 uses a simulated mock-vault/KMS service; it does not demonstrate a real KMS, HSM, or high-availability design.
- S4-COMP is an operational node comparison; it is not a measurement of post-quantum cryptography or mTLS overhead.
- S4-E03 completed 10,000 requests without HTTP failures, but it failed the LAT-01 latency objective.
- S4-E04 manifest-integrity enforcement is included as complementary/local prototype evidence, not as part of the principal June 10, 2026 revalidation package.
- The workloads are synthetic and contain no real banking data.

## Academic Context

- **Author:** Thomaz Klifson Falcao Barboza
- **Advisor:** Prof. Reginaldo Arakaki
- **Institution:** Institute of Technology and Leadership (Inteli)
- **Program:** Bachelor of Computer Science
- **Year:** 2026

## Keywords

Crypto-agility, post-quantum cryptography, CBOM, SBOM, three-tier architecture, cryptographic migration, experimental validation.
