# Comparação S4-COMP — Baseline vs Canário

## Configuração

- Rota: /chain
- VUs: 5
- Duração: 30s
- Requisições baseline: 150
- Requisições canário: 150

## Resultados

| Métrica | Baseline | Canário | Variação |
|---|---:|---:|---:|
| p95 latency (ms) | 42.58 | 27.20 | -36.12% |
| avg latency (ms) | 31.13 | 19.87 | -36.19% |
| HTTP failure rate | 0.0000 | 0.0000 | - |

## Interpretação

A comparação foi executada com mesma rota, mesma carga, mesma duração e mesmo número de requisições.
O canário apresentou latência p95 menor que o baseline nesta execução.
A variação observada não deve ser interpretada como overhead de PQC/mTLS, mas como comparação operacional entre os nós baseline e canário na topologia simulada.

## Arquivos de evidência

- Baseline: ~/infra/logs/revalidation/S4-COMP-baseline/k6-summary.json
- Canário: ~/infra/logs/revalidation/S4-COMP-canary/k6-summary.json
