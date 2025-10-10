# State of the Art in Cryptographic Transition Frameworks

## 1. Comparison Criteria
Inventory coverage, swap automation, PQC/hybrid support, CI/CD integration, observability, rollback, governance.

## 2. Solution Landscape
- Inventory and compliance:
  - CBOM/SBOM with cryptographic extensions.
- Toolchains and libraries:
  - OpenSSL 3.x with PQC via liboqs; bindings for multiple languages.
- Cloud/key management:
  - KMS and certificate managers with APIs for rotation and policies.
- Integrators/IDEs:
  - Static analysis plugins, legacy crypto API detectors, refactoring assistants.

## 3. Comparative Table (high level)
| Category | Strength | Limitations |
|----------|----------|-------------|
| CBOM Inventory | Visibility and auditability | Needs deep integration and specific parsers |
| OpenSSL+liboqs | Technical base for KEM/signatures | Partial ecosystem coverage; backports needed |
| KMS/Cert Managers | Rotation and policies | PQC/hybrid support uneven across providers |
| SAST/IDE Scanners | In-code detection | False positives; limited runtime context |
| Service Mesh/Edge | TLS profile enforcement | Compatibility requires hybrid strategies |

## 4. Synthesis
Existing solutions address parts of the problem (inventory, swapping, rotation, observability) but rarely integrate end-to-end with automated decisioning and resilient recovery. A gateway that coordinates the full cycle remains necessary: discover → decide → swap → validate → audit → rollback.
