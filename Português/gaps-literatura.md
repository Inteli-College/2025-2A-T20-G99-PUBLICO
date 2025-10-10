# 05-gaps-literatura.md
# Gaps Identificados na Literatura e no Mercado

## 1. Lacunas Técnicas
- Integração ponta a ponta entre inventário (CBOM), decisão de troca, execução automatizada e auditoria.
- Suporte consistente a handshakes híbridos em ambientes heterogêneos e multi-nuvem.
- Observabilidade criptográfica que correlacione tráfego real, inventário e políticas.

## 2. Lacunas de Processo e Governança
- Fluxos de aprovação e rollback específicos para mudanças criptográficas.
- Versionamento de políticas de criptografia e testes canários controlados.
- Indicadores de risco e SLOs voltados à postura criptográfica.

## 3. Lacunas de Ferramental
- Scanners contextuais que entendam uso real (runtime) além do código.
- Playbooks reprodutíveis de migração PQC por stack/linguagem/protocolo.
- Simuladores de impacto (performance, custo, compatibilidade).

## 4. Questões de Pesquisa Derivadas
- Como orquestrar, de forma segura, trocas de algoritmos com mínimo downtime?
- Quais estratégias híbridas maximizam compatibilidade sem sacrificar segurança?
- Como medir “agilidade criptográfica” de uma organização ao longo do tempo?

## 5. Hipótese de Trabalho
Um gateway de criptoagilidade, integrado a CBOM e instrumentação de tráfego, é capaz de reduzir tempo de migração, erros operacionais e riscos de compatibilidade, elevando a maturidade PQC de forma mensurável.
