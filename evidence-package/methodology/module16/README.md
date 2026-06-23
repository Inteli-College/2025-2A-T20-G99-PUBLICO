# Módulo 16 — Execução Experimental, Fechamento de Gaps e Artigo Final IEEE

## Visão geral

O Módulo 16 conclui o projeto de criptoagilidade PQC em ambiente híbrido three-tier,
executando os cenários experimentais pendentes, fechando o gap de integridade do CBOM
(V-03) e produzindo a versão final dos artigos para submissão em conferência IEEE.

## Contexto

| Módulo | Principal contribuição |
|---|---|
| 13 | Revisão bibliográfica, CBOM Kit, critérios de criptoagilidade |
| 14 | Gateway architecture, métricas PQC, topologia 8-nós, cenários Sprint 4/5 |
| 15 | Artigos bilíngues `artigo.tex` / `paper.tex` (dados parcialmente sintéticos) |
| **16** | **Experimentos completos, fix V-03, artigo final com dados reais** |

## Lacunas fechadas neste módulo

1. **Cenários não executados**: S4-T03, S4-T04, S4-T06, S4-E01, S4-E02, S4-E03.
2. **Gap V-03 (adulteração CBOM)**: `sign_manifest()` / `verify_manifest()` com HMAC-SHA256.
3. **Artigo IEEE expandido**: Seções 10 (ambiente), 11 (resultados), 12 (limitações/discussão).

## Estrutura

```
docs/module16/
├── README.md                         ← este arquivo
├── sprint1-typical-scenarios.md      ← S4-T03, S4-T04, S4-T06
├── sprint2-extreme-scenarios.md      ← S4-E01, S4-E02, S4-E03
├── sprint3-cbom-integrity.md         ← fix V-03, assinatura CBOM
└── sprint4-paper-final.md            ← processo de revisão e submissão IEEE
```

## Infraestrutura

- **Servidor**: Ubuntu 24.04.3 LTS, 64 vCPU (Intel Xeon Gold 6454S), 125 GiB RAM.
- **Runtime**: Podman 4.9.3 rootless, topologia `lab/topology/docker-compose.yml`.
- **Scripts novos**: `lab/topology/k6/` e `lab/topology/scripts/`.

## Artefatos principais

| Artefato | Descrição |
|---|---|
| `artigo.tex` / `artigo.pdf` | Artigo final em português (IEEE, ~8 pp.) |
| `paper.tex` / `paper.pdf` | Artigo final em inglês (IEEE, ~8 pp.) |
| `code/cbom_gateway.py` | Gateway com `--sign` / `--verify` |
| `code/samples/cbom-signed.json` | Manifesto de referência com HMAC |
| `code/samples/cbom-tampered.json` | Manifesto adulterado para S4-E04 |
| `docs/module16/evidence/` | JSONs de evidência por cenário |
