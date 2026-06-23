# S4-E01 — Indisponibilidade do mock-vault / KMS simulado

## Objetivo
Avaliar o comportamento da topologia three-tier quando o serviço de integração de segurança, usado como mock-vault/KMS simulado, fica indisponível durante a execução da cadeia aplicacional.

## Configuração
- Serviço afetado: `security-integration-node`
- Serviço consumidor: `k8s-worker-2`
- Rota testada: `http://k8s-worker-2:8080/chain`
- Orquestração: Podman rootless
- Estratégia: parada manual do container de segurança, chamada da aplicação durante a falha e reinício do serviço para observar recuperação.

## Estado antes da falha
- Timestamp: 2026-06-10T16:23:32-03:00
- Resultado: HTTP 200
- Latência cliente: 40,09 ms
- Perfil de segredo: `mock-vault`
- Banco de dados: `ok=true`
- Event count: 11500

## Falha induzida
- Timestamp de parada: 2026-06-10T16:24:36-03:00
- Ação: `podman stop security-integration-node`
- Estado do container: `Exited (137)`
- Resultado da chamada: HTTP 500
- Latência cliente: 18,21 ms
- Erro observado: `<urlopen error [Errno -2] Name or service not known>`

## Recuperação
- Timestamp de reinício: 2026-06-10T16:24:50-03:00
- Ação: `podman start security-integration-node`
- Resultado após recuperação: HTTP 200
- Latência cliente: 36,25 ms
- Perfil de segredo recuperado: `mock-vault`
- Banco de dados: `ok=true`
- Event count: 11501

## Interpretação
O cenário demonstrou que a indisponibilidade do serviço de integração de segurança causa falha controlada na cadeia aplicacional, retornando HTTP 500 enquanto o mock-vault está inacessível. Após o reinício do serviço, a rota `/chain` voltou a responder HTTP 200, indicando recuperação operacional da dependência de segurança.

## Resultado
- Detecção da falha: aprovada.
- Recuperação após reinício: aprovada.
- Tolerância sem erro HTTP: reprovada, pois a aplicação retornou HTTP 500 durante a indisponibilidade.
- Observação: o experimento usa mock-vault/KMS simulado, não KMS real.

## Evidências
- Antes da falha: `~/infra/logs/revalidation/S4-E01-kms-unavailable/step-01-before.txt`
- Durante a falha: `~/infra/logs/revalidation/S4-E01-kms-unavailable/step-02-during.txt`
- Após recuperação: `~/infra/logs/revalidation/S4-E01-kms-unavailable/step-03-after.txt`
