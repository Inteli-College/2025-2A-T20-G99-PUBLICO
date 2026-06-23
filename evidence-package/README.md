# Evidence Package

This directory contains the public evidence package for the thesis:

**CBOM-Driven Crypto-Agility for Post-Quantum Migration in Hybrid Three-Tier Environments**

The package was assembled from the internal repository to support the experimental claims, limitations, and reproducibility notes reported in the thesis and article source. It contains only selected public-facing artifacts: raw experiment evidence, scripts, topology files, CBOM prototypes, methodology documents, and article source files.

## Structure

| Path | Purpose |
| --- | --- |
| `revalidation/` | Raw revalidated evidence used in the final thesis: k6 summaries, k6 outputs, app-chain response, stress report, dependency-failure captures, and runtime captures. |
| `archives/` | Original compressed revalidation bundle retained for provenance. |
| `reproducibility/code/` | CBOM scanner and crypto-agility gateway prototypes, including signed and tampered manifest samples. |
| `reproducibility/lab-topology/` | Executable simulated topology, k6 workloads, mock node, Prometheus configuration, and lab control script. |
| `methodology/` | Planning, metrics, topology, security-validation, governance, and scenario documentation needed to interpret the experiments. |
| `article-source/` | Article source files and bibliography used to cross-check artifact references and reported results; this is not a standalone build package. |
| `MANIFEST.sha256` | SHA-256 hashes for every file in this package. |

## Evidence Traceability

| Claim or scenario | Public artifacts |
| --- | --- |
| S4-T01 baseline: 150 requests, 0 failures, p95 39.71 ms | `revalidation/S4-T01/k6-summary.json`, `revalidation/S4-T01/k6-output.txt` |
| S4-T02 canary: 40 requests, 0 failures, p95 24.70 ms | `revalidation/S4-T02/k6-summary.json`, `revalidation/S4-T02/k6-output.txt` |
| S4-T03 functional app, mock-vault, database, and canary chain | `revalidation/S4-T03/app-chain.json` |
| S4-COMP controlled baseline vs canary comparison | `revalidation/S4-COMP-comparison.md`, `revalidation/S4-COMP-baseline/k6-summary.json`, `revalidation/S4-COMP-canary/k6-summary.json` |
| S4-E03 stress: 10,000 requests, 0 HTTP failures, LAT-01 violation | `revalidation/S4-E03-stress/results.md`, `revalidation/S4-E03-stress/k6-summary.json`, `revalidation/S4-E03-stress/k6-output.txt` |
| S4-E01 simulated mock-vault/KMS unavailability and recovery | `revalidation/S4-E01-kms-unavailable/results.md`, `step-01-before.txt`, `step-02-during.txt`, `step-03-after.txt` |
| Runtime state after lab startup | `revalidation/runtime/podman-ps-after-start.txt`, `container-logs-after-start.txt`, `start-order.log` |
| Lab topology and workload scripts | `reproducibility/lab-topology/docker-compose.yml`, `k6/*.js`, `mock-node/app.py`, `scripts/labctl.sh` |
| CBOM decision flow and integrity control | `reproducibility/code/cbom_gateway.py`, `reproducibility/code/cbomkit_cli.py`, `reproducibility/code/samples/*.json` |
| S4-E04 complementary/local manifest-integrity evidence | `methodology/module16/sprint3-cbom-integrity.md`, `reproducibility/code/samples/cbom-signed.json`, `reproducibility/code/samples/cbom-tampered.json` |
| Metrics, acceptance criteria, and limitations | `methodology/module14/metrics-resilience-matrix.md`, `methodology/module14/pqc-cryptoagility-metrics-migration*.md`, `methodology/module14/sprint4/experiment-scenarios.md` |

## Interpretation Notes

- The observed results are the files under `revalidation/`.
- Some methodology files describe planned or target scenarios. They are included to explain the experiment design, not to imply that every planned control was demonstrated.
- S4-T03 validates functional chaining over HTTP. It does not demonstrate real mTLS.
- S4-E01 uses a simulated mock-vault/KMS service. It does not demonstrate a production KMS, HSM, or high-availability recovery.
- S4-COMP is an operational comparison between nodes under the same workload. It is not a measurement of PQC or mTLS overhead.
- S4-E03 completed without HTTP failures but violated the LAT-01 p95 latency objective.
- S4-E04 is complementary/local prototype evidence for manifest-integrity enforcement; it is not part of the principal June 10, 2026 revalidation package.
- Workloads are synthetic and contain no real banking data.
- The lab topology may contain local-only default credentials for synthetic services. Change them before any reuse outside the controlled lab.

## Reproducibility Entry Points

Use `reproducibility/lab-topology/README.md` for the topology workflow and `reproducibility/code/README.md` for the CBOM prototype workflow.

The main lab commands are documented in `reproducibility/lab-topology/scripts/labctl.sh`; the scenario definitions and acceptance criteria are documented in `methodology/module14/sprint4/experiment-scenarios.md`.
