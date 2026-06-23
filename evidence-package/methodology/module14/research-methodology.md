# Plano Metodológico — Módulo 14

Consolida as diretrizes metodológicas descritas no plano acadêmico (`TAPI-Modulo14.txt`) e conecta-as às entregas em andamento.

## 1. Abordagem geral
- **Tipo**: pesquisa exploratória/aplicada com abordagem mista (qualitativa + quantitativa) (ver TAPI-Modulo14.txt:182-188).
- **Objetivo**: validar o modelo de criptoagilidade por meio de simulações em nuvem e entrevistas com especialistas.

## 2. Coleta de dados
### 2.1 Qualitativa
- **Participantes**: arquitetos de segurança, engenheiros SRE, especialistas em PQC (mín. 5 anos de experiência).
- **Técnica**: entrevistas semiestruturadas (perguntas sobre governança, PQC readiness, práticas CBOM).
- **Instrumentos**: roteiro aprovado pelo orientador + termo de consentimento; registro em áudio/texto.

### 2.2 Quantitativa
- **Cenários**: simulações three-tier em ambientes controlados (AWS/Azure/IBM) com workloads representativos (TAPI-Modulo14.txt:211-219).
- **Dados coletados**: métricas do gateway (`metrics-resilience-matrix.md`), custo incremental, MTTR, handshakes híbridos.
- **Ferramentas**: `code/cbom_gateway.py` para inventário; testes de carga (k6/Locust) para medir impacto PQC.

## 3. Técnicas de análise
- **Comparativa**: avaliar desempenho/custo/tempo de resposta entre perfis clássico, híbrido e PQC puro.
- **Qualitativa**: análise temática das entrevistas (viabilidade, replicabilidade, riscos).
- **Estudo de caso**: consolidar resultados das simulações e dos especialistas para validar o framework (TAPI-Modulo14.txt:220-225).

## 4. Roteiro Sprint 2 → Sprint 5
| Sprint | Atividades metodológicas |
| --- | --- |
| 2 | Definir instrumentos (questionário, template de simulação), validar com orientador. |
| 3 | Executar entrevistas piloto e configurar ambiente three-tier em nuvem. |
| 4 | Rodar simulações com perfis híbridos/PQC; coletar métricas definidas. |
| 5 | Analisar resultados, consolidar estudo de caso e preparar documentação para o módulo seguinte. |

## 5. Ética e conformidade
- Uso de dados sintéticos e ambientes controlados (TAPI-Modulo14.txt:300-314).
- Aderência aos padrões NIST de PQC e princípios de segurança by design.
- Registro das entrevistas em repositório seguro; anonimização antes da publicação.

## 6. Integração com CBOM protótipo
- `code/cbom_gateway.py` será usado como ferramenta de apoio à coleta quantitativa, gerando relatórios de cobertura e recomendações para cada simulação.
- Manifestos gerados pelo IBM CBOM Kit devem ser armazenados em `data/cbom/<sprint>/` (a ser criado) para garantir rastreabilidade e anexação às mudanças.

> Atualize este plano conforme novas entrevistas ou simulações forem aprovadas, garantindo rastreamento das versões utilizadas na pesquisa.
