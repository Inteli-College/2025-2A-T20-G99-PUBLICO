# Sumário de evidências revalidadas — Módulo 14 / S4

## Cenários revalidados

| Cenário | Objetivo | Resultado | Métrica principal | Status |
|---|---|---|---|---|
| S4-T03 app-chain | Validar cadeia app → segurança/mock-vault → banco → canário | HTTP 200, cadeia funcional | elapsed_ms = 51,17 ms | Aprovado |
| S4-T01 baseline | Validar baseline `/chain` com carga nominal | 150 requisições, 0 falhas | p95 = 39,71 ms | Aprovado |
| S4-T02 canário | Validar nó canário com carga nominal | 40 requisições, 0 falhas | p95 = 24,70 ms | Aprovado |
| S4-COMP baseline vs canário | Comparar baseline e canário com mesma carga | 150 vs 150 requisições, 0 falhas | p95 baseline = 42,58 ms; p95 canário = 27,20 ms | Aprovado |
| S4-E03 stress | Executar 10.000 transações sintéticas | 10.000 requisições, 0 falhas HTTP | p95 = 1149,64 ms | Disponibilidade aprovada; LAT-01 reprovado |
| S4-E01 mock-vault/KMS simulado indisponível | Testar falha e recuperação da dependência de segurança | HTTP 500 durante falha; HTTP 200 após recuperação | recuperação em chamada posterior após restart | Parcialmente aprovado |

## Interpretação geral

Os experimentos revalidados demonstram que a topologia simulada permanece funcional em baseline, canário e cadeia app-security-data, com 0% de falhas HTTP nos testes nominais. A comparação controlada entre baseline e canário foi refeita com mesma rota, mesma duração, mesma carga e mesmo número de requisições, evitando a limitação metodológica da comparação anterior.

O cenário S4-E03 acrescenta evidência de stress com 10.000 transações sintéticas: a arquitetura manteve disponibilidade, mas violou o SLO LAT-01 de p95 < 150 ms sob 50 VUs. O cenário S4-E01 demonstrou falha e recuperação da dependência de segurança: a indisponibilidade do mock-vault/KMS simulado causou HTTP 500, e o serviço voltou a operar após reinício do container.

## Limitações

- O cenário S4-E01 usa mock-vault/KMS simulado, não KMS real.
- A comparação S4-COMP não deve ser interpretada como overhead de PQC/mTLS.
- A cadeia observada usa `http://security-integration-node:8080/secret`; portanto, ainda não comprova mTLS real.
- Os healthchecks dos containers aparecem como `unhealthy`, mas os endpoints funcionais responderam corretamente nos testes.
- O cenário S4-E03 mostra limite de desempenho sob carga comprimida, não falha funcional da arquitetura.

## Evidências principais

- S4-T01: `~/infra/logs/revalidation/S4-T01/k6-summary.json`
- S4-T02: `~/infra/logs/revalidation/S4-T02/k6-summary.json`
- S4-COMP baseline: `~/infra/logs/revalidation/S4-COMP-baseline/k6-summary.json`
- S4-COMP canário: `~/infra/logs/revalidation/S4-COMP-canary/k6-summary.json`
- S4-COMP comparação: `~/infra/logs/revalidation/S4-COMP-comparison.md`
- S4-E03 stress: `~/infra/logs/revalidation/S4-E03-stress/results.md`
- S4-E01 mock-vault indisponível: `~/infra/logs/revalidation/S4-E01-kms-unavailable/results.md`
