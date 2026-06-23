# Vulnerabilidades em Arquitetura 3-Tier (Aplicação / Serviços / Dados)

> Foco: classes de vulnerabilidade mais frequentes e **mitigações orientadas à criptoagilidade**.

## Visão geral

| Camada | Classe de Vulnerabilidade | Exemplo típico | Mitigação orientada à criptoagilidade | Métrica sugerida |
|-------|----------------------------|----------------|----------------------------------------|------------------|
| Aplicação (front/API) | TLS legado / negociação fraca | Permitir TLS 1.0/1.1; suites sem PFS | Política de suites → **TLS 1.2+/1.3**, auditoria de cipher-suites, mTLS quando aplicável | % conexões fortes; tempo p/ trocar suite |
| Aplicação | Hardcode de segredos | Keys em código/variáveis em plain | **KMS/Secrets Manager**, rotação periódica, varredura de repositórios | MTTR para rotação |
| Aplicação | Falta de telemetria cripto | Sem logs de handshake/falhas | **Observabilidade** de handshakes, códigos de erro, renegociações atípicas | Cobertura de eventos cripto |
| Serviços (negócio) | Bibliotecas cripto desatualizadas | OpenSSL/Boring/BC defasadas | **Inventário CBOM**, política de versões e janela de migração | Lead time de atualização |
| Serviços | Falhas em políticas de chave | Chaves long-lived, sem escrow | **Gestão de ciclo de chaves**, RPO de rotação, split de privilégios | % chaves com política aplicada |
| Serviços | Falha de rollback | Troca de suite quebra integração | **Feature flags/rollback** em rotas/sistemas | Tempo de backout |
| Dados (armazenamento) | Cripto em repouso ausente/fraca | Volumes/backups sem cifragem | **Envelope com KMS**, classificação por sensibilidade | % datasets com KMS |
| Dados | Indexação/logs com dados sensíveis | Logs queryable sem máscara | **Mascaramento/tokenização**, retenção mínima | % logs sensíveis mascarados |
| Dados | Backups legados exportados | Dump sem cripto em storage antigo | **Inventário/cripto retroativa** + destruição programada | % backups legados protegidos |

### Checklists rápidos

- **Aplicação**: exigir TLS 1.2+/1.3; remover suites fracas; avaliar mTLS; varredura de segredos; logs de handshakes e falhas.  
- **Serviços**: CBOM por serviço; política “algoritmo como config”; rotação de chaves; feature-flags para troca; integração com SIEM.  
- **Dados**: KMS/Envelope; classificação; tokenização/máscara; backups cifrados; retenção mínima; destruição programada.

> **Trade-offs**: endurecer cripto pode afetar disponibilidade/latência; use **canárias** e **rollback**.
