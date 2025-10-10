# Public Report – Módulo 13  
## Projeto: Criptoagilidade em Ambientes Corporativos Híbridos para Transição Pós-Quântica

---

## Descrição Geral do Projeto
Este projeto propõe o desenvolvimento e validação de um modelo arquitetural inovador de **criptoagilidade** voltado para ambientes corporativos híbridos (on-premise + nuvem) com **arquitetura three-tier**.  
O modelo integra um **gateway especializado** capaz de realizar migrações ágeis e automatizadas para algoritmos de **criptografia pós-quântica (PQC)**, além de implementar mecanismos inteligentes de **detecção em tempo real** e **recuperação resiliente** de incidentes de segurança.  

O objetivo é entregar um **framework prático, replicável e validado em ambiente de simulação**, contribuindo para preparar organizações críticas frente à ameaça iminente dos computadores quânticos.

---

## Problema e Motivação
A **computação quântica** representa uma ameaça concreta aos sistemas criptográficos atuais, especialmente em ambientes corporativos complexos que dependem de RSA e ECC.  
Embora a PQC ofereça resistência a ataques quânticos, as soluções existentes focam apenas na substituição de algoritmos, sem abordar de forma integrada **monitoramento, resposta e recuperação de incidentes**.  

A lacuna identificada é a **ausência de frameworks completos de criptoagilidade**, capazes de combinar migração automática, detecção e resiliência em arquiteturas corporativas híbridas e distribuídas.

---

## Objetivos do Projeto

### Objetivo Geral
Desenvolver e validar um **modelo arquitetural de criptoagilidade** para ambientes corporativos híbridos, capaz de realizar migrações ágeis para algoritmos pós-quânticos e reforçar os mecanismos de detecção e recuperação de incidentes.

### Objetivos Específicos
- Mapear vulnerabilidades de um ambiente three-tier em relação à transição para PQC  
- Projetar um **gateway de criptoagilidade** integrado a módulos de monitoramento e resposta  
- Simular, em nuvem, a migração de um sistema legado para PQC com detecção e recuperação automáticas  
- Avaliar desempenho, custo e eficácia do modelo proposto em comparação com implementações convencionais de PQC  

---

## Entregáveis do Módulo 13

### 1. Mapeamento do IBM CBOM Kit
- Estudo detalhado da ferramenta **IBM CBOM Kit** e de sua aplicabilidade como suporte à criptoagilidade.  
- Identificação de seus componentes, APIs e potenciais integrações com o gateway proposto.

### 2. Revisão Bibliográfica sobre PQC e Criptoagilidade
- Levantamento das principais referências científicas e institucionais, incluindo:  
  - **NIST PQC Standardization Project**  
  - **Arquiteturas de Resiliência Cibernética** (táticas Resistir, Detectar, Recuperar)  
  - **Ferramentas comerciais** de transição criptográfica.  

### 3. Mapeamento de Vulnerabilidades em Ambientes Three-Tier
- Identificação dos pontos críticos de segurança entre camadas de **aplicação**, **servidor** e **banco de dados**.  
- Análise dos riscos associados a módulos legados e protocolos não compatíveis com PQC.  

### 4. Estado da Arte em Frameworks de Transição Criptográfica
- Estudo comparativo de soluções existentes (IBM, Microsoft, AWS, etc.) e suas limitações frente à migração PQC.  

### 5. Identificação de Gaps na Literatura
- Levantamento de lacunas técnicas e conceituais entre a teoria da PQC e a prática corporativa de migração de sistemas.  

### 6. Definição do Referencial Teórico
- Consolidação das bases teóricas sobre **criptoagilidade, PQC, segurança em arquiteturas híbridas** e **resiliência cibernética**.  

---

## Tecnologias e Ferramentas
- **IBM CBOM Kit** – referência técnica para mapeamento de criptossistemas legados  
- **Python / OpenSSL / liboqs** – bibliotecas para simulação e teste de algoritmos PQC  
- **AWS / IBM Cloud / Azure** – plataformas para simulação em nuvem  
- **NIST PQC Algorithms** – Kyber, Dilithium, Falcon  
- **Draw.io / Lucidchart** – modelagem arquitetural e fluxos de migração  

---

## Resultados Esperados do Módulo 13
- Entendimento aprofundado do **estado atual da criptoagilidade corporativa**  
- Definição das **bases teóricas e técnicas** para o gateway de criptoagilidade  
- Estruturação do **modelo conceitual** que será detalhado no design arquitetural (Módulo 14)

---

## Referências Principais
- NIST. *Post-Quantum Cryptography Standardization Project*.  
- IBM Research. *CBOM Kit – Cryptographic Bill of Materials Toolkit*.  
- Gartner (2023). *Crypto-Agility and Quantum-Readiness Frameworks*.  
- Arakaki, R. et al. (2024). *Arquiteturas de Resiliência Cibernética*.  
- ETSI TR 103 619 V2.1.1 (2020). *Quantum-Safe Cryptography and Security*.  
