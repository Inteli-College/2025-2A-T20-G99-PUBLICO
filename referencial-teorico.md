# 06-referencial-teorico.md
# Referencial Teórico do Projeto

## 1. Definições
- Criptoagilidade: capacidade de inventariar, trocar e governar algoritmos/chaves com baixo atrito.
- PQC: conjunto de algoritmos resistentes a adversários com capacidade quântica.
- Resiliência criptográfica: resistir, detectar e recuperar frente a falhas/incidentes.

## 2. Modelos Conceituais
- Pipeline de criptoagilidade:
  1) Inventário (CBOM)  
  2) Políticas e mapeamento clássico→PQC  
  3) Execução automatizada (patch/PR/rotações)  
  4) Validação e testes canários  
  5) Observabilidade e auditoria  
  6) Rollback e aprendizagem contínua
- Arquitetura three-tier híbrida como cenário de referência.

## 3. Pressupostos
- Disponibilidade de toolchains com suporte a PQC/híbrido.
- Acesso a ambientes de simulação em nuvem.
- Validação mista: métricas quantitativas e entrevistas qualitativas.

## 4. Métricas e Indicadores
- Cobertura de inventário (% serviços com CBOM válido).
- Tempo de troca por serviço (descobrir→patch→validar→auditar).
- Taxa de sucesso de handshakes híbridos.
- Overhead de performance (latência, CPU, memória).
- MTTR criptográfico e taxa de rollback seguro.

## 5. Metodologia de Avaliação
- Experimentos controlados em ambiente de nuvem com sistema three-tier de referência.
- Análise comparativa com abordagens convencionais (troca manual/sem CBOM).
- Entrevistas com especialistas para avaliação de viabilidade e governança.

## 6. Riscos e Mitigações
- Incompatibilidades de clientes/serviços: uso de perfis híbridos e canários.
- Regressões de desempenho: testes de carga e perfis por serviço.
- Falhas de automação: planos de rollback, change management e approvals.

## 7. Resultados Esperados
- Modelo arquitetural reprodutível de criptoagilidade.
- Diretrizes operacionais e de governança para adoção corporativa.
- Evidências quantitativas de redução de tempo/erros em migração PQC.
