# 01-mapeamento-cbom.md
# Mapeamento do IBM CBOM Kit

## 1. Visão Geral
O IBM Cryptographic Bill of Materials (CBOM) Kit é um conjunto de ferramentas e especificações para inventariar ativos criptográficos de um sistema: algoritmos, parâmetros, chaves, bibliotecas, certificados, protocolos e pontos de uso em código e infraestrutura. No contexto de criptoagilidade, o CBOM atua como inventário-fonte para planejar e auditar a migração para algoritmos pós-quânticos (PQC).

## 2. Objetivos do Mapeamento
1. Entender capacidades do CBOM para descoberta de dependências criptográficas.
2. Avaliar formatos de saída (manifestos CBOM) e como integrá-los ao gateway de criptoagilidade.
3. Identificar extensões necessárias para ambientes three-tier híbridos (on-premise + nuvem).
4. Definir processo de coleta, normalização e versionamento do inventário.

## 3. Componentes e Artefatos
- Coleta de código-fonte e binários: scanners estáticos para bibliotecas (OpenSSL, BoringSSL, libsodium, Java JCA/JCE, .NET Cryptography).
- Coleta de runtime/config: varredura de containers, VMs, secrets managers e KMS.
- Manifesto CBOM: documento estruturado descrevendo artefatos criptográficos, com campos típicos:
  - `component`, `version`, `location`, `algo`, `mode`, `key_size`, `hash`, `cert_chain`, `protocol`, `usage`.
- Conectores: pipelines CI/CD, agentes em hosts, integração com SCM (Git), registries e orquestradores (Kubernetes).

## 4. Fluxo Operacional Proposto
1) Descoberta: varredura de repositórios, imagens e hosts.  
2) Normalização: deduplicação e consolidação por serviço e ambiente.  
3) Enriquecimento: correlação com SBOMs, certificados, políticas e telemetria.  
4) Publicação: armazenamento versionado do CBOM em repositório de compliance.  
5) Consumo: o gateway de criptoagilidade lê o CBOM para propor migrações PQC.

## 5. Integração com o Gateway de Criptoagilidade
- Entrada: CBOM como fonte de verdade para localizar “pontos de troca”.
- Decisão: regras de mapeamento (ex.: RSA→Kyber, ECDSA→Dilithium).
- Ação: geração de PRs/patches, playbooks de TLS/KMS e rotação de chaves.
- Auditoria: anexar CBOM antes/depois da remediação para rastreabilidade.

## 6. Métricas de Qualidade do Inventário
- Cobertura (percentual de serviços inventariados).
- Precisão (falsos positivos/negativos na detecção de algos/parametrizações).
- Latência (tempo de coleta-publicação).
- Reprodutibilidade (inventários consistentes a cada execução).

## 7. Limitações Observadas e Extensões Sugeridas
- Desafio em plataformas heterogêneas e linguagens dinâmicas.
- Necessidade de parsers para stacks específicos (Android/iOS, HSMs).
- Módulo de correlação com tráfego real (PCAPs, logs TLS) para validar uso efetivo.
- Template CBOM estendido para atributos PQC (KEM/Signature, nível de segurança, artefatos híbridos).

## 8. Próximos Passos
- Prototipar pipeline de varredura em um sistema three-tier de referência.
- Definir schema CBOM estendido para PQC e publicar exemplo versionado.
- Integrar CBOM ao mecanismo de decisão do gateway e ao relatório de conformidade.
