# 03-mapeamento-vulnerabilidades-three-tier.md
# Mapeamento de Vulnerabilidades em Arquiteturas Three-Tier

## 1. Escopo
Arquitetura de referência com camadas Web/App/DB em ambiente híbrido (on-premise + nuvem), com balanceadores, TLS interno, filas e cache.

## 2. Dataflow Simplificado (ASCII)
Client ──HTTPS/TLS──> Web ──mTLS/TLS──> App ──TLS/Native──> DB
                         │                 └──> Cache/Queue/Services
                         └──> CDN/WAF

## 3. Ativos e Superfícies
- Tráfego externo (TLS público, certificados públicos).
- Tráfego leste-oeste entre serviços (mTLS, segredos, certificados internos).
- Armazenamento de segredos (KMS, vaults, arquivos, variáveis).
- Bibliotecas criptográficas nos serviços e images.

## 4. Catálogo de Vulnerabilidades (resumo)
| ID | Local | Descrição | Impacto | Detecção | Mitigação Inicial |
|----|-------|-----------|---------|----------|-------------------|
| V1 | Web   | TLS clássico sem PQC/híbrido | Confidencialidade | CBOM + logs TLS | Handshake híbrido, políticas de cipher suite |
| V2 | App   | Dependência de RSA/ECC fixa no código | Integridade/Disponibilidade | SAST + CBOM | Abstração criptográfica + mapeamento PQC |
| V3 | App   | Falta de rotação de chaves/certs | Conformidade | Telemetria KMS | Playbooks de rotação automatizada |
| V4 | DB    | Criptografia em repouso não inventariada | Confidencialidade | CBOM+KMS audit | Chaves PQC-ready, validação periódica |
| V5 | Mesh  | mTLS entre serviços heterogêneos | Quebra de canal | PCAP/Service mesh | Perfis TLS com KEM PQC e fallback |
| V6 | CI/CD | Imagens com libs antigas | Exploração de lib | Scanner imagens | Gates de segurança e rebuild controlado |

## 5. Mapeamento PQC
- Canais: adotar perfis TLS com KEM PQC (quando disponível) ou estratégia híbrida e gradativa.
- Assinaturas: substituir ECDSA por esquemas pós-quânticos suportados nos pipelines de build e assinatura de artefatos.
- Segredos: preparar rotação e armazenamento compatíveis com chaves maiores e novos formatos.

## 6. Critérios de Priorização
- Exposição externa primeiro (Web/Edge), depois leste-oeste crítico.
- Baixo esforço/alto impacto: bibliotecas centralizadas, terminação TLS, gateways de API.
- Dependências compartilhadas: libs comuns utilizadas por muitos serviços.

## 7. Saídas
- Tabela de mapeamento serviço→algoritmo atual→algoritmo PQC alvo.
- Lista de PRs/patches candidatos para sprint de migração.
