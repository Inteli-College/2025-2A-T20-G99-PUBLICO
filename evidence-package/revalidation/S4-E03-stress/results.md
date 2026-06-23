# S4-E03 — Carga comprimida / stress

## Objetivo
Executar 10.000 transações sintéticas sobre a rota `/chain` da topologia three-tier simulada, exercitando web, app, integração de segurança/mock-vault e banco de dados.

## Configuração
- Rota: `/chain`
- BASE_URL: `http://k8s-worker-1:8080`
- VUs: 50
- Iterações: 10.000
- Ferramenta: k6
- Ambiente: Podman rootless em servidor acadêmico
- Script: `lab/topology/k6/stress-10000.js`

## Resultados observados
- Requisições HTTP: 10.000
- Iterações concluídas: 10.000
- Falhas HTTP: 0
- Taxa de falha HTTP: 0,00%
- p95 de latência: 1149,64 ms
- Latência média: 203,47 ms
- Latência máxima: 6235,52 ms

## Critérios
- Disponibilidade: aprovado, pois 10.000/10.000 requisições foram concluídas sem falhas HTTP.
- LAT-01 p95 < 150 ms: reprovado sob carga comprimida de 50 VUs, pois o p95 observado foi 1149,64 ms.

## Interpretação
O cenário S4-E03 demonstrou que a topologia suporta 10.000 transações sintéticas sem falhas HTTP, mas apresentou degradação significativa de latência sob carga comprimida. Portanto, o resultado valida a disponibilidade funcional da arquitetura em stress, mas evidencia limitação de desempenho para o SLO LAT-01 nessa configuração.

## Evidências
- Log k6: `~/infra/logs/revalidation/S4-E03-stress/k6-output.txt`
- Resumo JSON: `~/infra/logs/revalidation/S4-E03-stress/k6-summary.json`
