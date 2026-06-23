# Sprint 4 — Artigo Final IEEE

**Módulo**: 16 | **Sprint**: 4 | **Semanas**: 7–8

---

## Objetivo

Substituir os dados sintéticos das Tabelas 1 e 2 dos artigos pelos dados reais coletados
nas Sprints 1–3, expandir as seções de discussão e limitações, incorporar as novas
referências, e produzir os PDFs finais para revisão dos orientadores.

---

## Checklist de Conteúdo

### Dados a preencher nas tabelas

Após as execuções das Sprints 1 e 2, preencher na Tabela 2 dos artigos (PT e EN):

| Cenário | Indicador | Resultado real (a coletar) |
|---|---|---|
| S4-T03 | Sucesso mTLS híbrido (HYB-01) | `S4-T03-k6-summary.json` → `hybrid_handshake_errors.rate` |
| S4-T03 | Overhead de latência mTLS (HYB-02) | Δ p95 vs. S4-T01 baseline |
| S4-T04 | Rotação automatizada (KLC-01) | `S4-T04/rotation-log.json` → `rotated_count / total` |
| S4-T06 | Custo incremental/1M req (COST-01) | `S4-T06-cost-delta.json` → `cost_increase_pct` |
| S4-E01 | MTTD falha KMS | `S4-E01-timeline.txt` → `t_detect - t_start` |
| S4-E01 | MTTR completo | `S4-E01-timeline.txt` → `t_restored - t_start` |
| S4-E02 | Tempo de rollback | `S4-E02-timeline.txt` → `t_rollback - t_alert` |
| S4-E03 | p95 stress | `S4-E03-stress.json` → `http_req_duration.p(95)` |
| S4-E03 | ΔCPU overhead | `S4-E03-resource-snapshot.csv` → CPU delta vs. S4-T01 |

### Seções que precisam de revisão dos orientadores

1. **Seção 10 — Implementação do Ambiente Experimental**: validar descrição do servidor e Podman.
2. **Seção 11 — Dados Práticos e Experimentais**: validar Tabelas com dados reais.
3. **Seção 12 — Discussão e Limitações**: validar interpretação dos resultados e limitações listadas.
4. **Abstract/Resumo**: atualizar com resultados finais (substituir projeções por dados reais).

---

## Compilação dos Artigos

```bash
# Compilar artigo PT
cd c:\Users\Inteli\Documents\GitHub\2025-2A-T20-G99-INTERNO
pdflatex artigo.tex
pdflatex artigo.tex    # segunda passagem para referências

# Compilar paper EN
pdflatex paper.tex
pdflatex paper.tex

# Verificar ausência de erros críticos
grep -i "error\|fatal" artigo.log
grep -i "error\|fatal" paper.log
```

### Verificações antes de enviar para revisão

- [ ] Nenhum `\textbf{??}` (referências não resolvidas) nos PDFs.
- [ ] Tabelas numeradas corretamente (Tabela 1 = controles base, Tabela 2 = cenários).
- [ ] Abstract em inglês e Resumo em português alinhados entre si.
- [ ] Todos os `\cite{}` resolvidos (sem `[?]` no PDF).
- [ ] Limite IEEE: verificar se o artigo não excede 8 páginas (IEEEtran conference).

---

## Processo de Revisão pelos Orientadores

1. **Enviar PDFs**: `artigo.pdf` e `paper.pdf` para Reginaldo Arakaki e Hayashi.
2. **Canal de feedback**: issues no repositório ou comentários diretos no `.tex`.
3. **Prazo sugerido**: 5 dias úteis para retorno.
4. **Incorporar feedback**: aplicar correções nas Sprints 4/5.

---

## Estrutura Final dos Artigos (ambos)

| Seção | Status |
|---|---|
| 1. Introdução/Introduction | ✅ Existia desde M15 |
| 2. Objetivo/Article Objective | ✅ Existia |
| 3. Fundamentos/Conceptual Foundations | ✅ Existia |
| 4. Proposta de Experimentação | ✅ Existia |
| 5. Requisitos do Método | ✅ Atualizado (M16: integridade CBOM) |
| 6. Processo/Stages | ✅ Atualizado (M16: manifesto assinado) |
| 7. Indicadores/Quality Controls | ✅ Existia |
| 8. Ferramentas/Tools | ✅ Atualizado (M16: HMAC, k6) |
| 9. Caso Prático/Practical Case | ✅ Existia |
| **10. Ambiente Experimental** | 🆕 **Novo no M16** |
| **11. Dados e Resultados Detalhados** | 🆕 **Novo no M16 (dados reais)** |
| **12. Discussão e Limitações** | 🆕 **Novo no M16** |
| 13. Case Exemplo | ✅ Atualizado |
| 14. Aplicação do Roteiro | ✅ Existia |
| 15. Resultados | ✅ Atualizado |
| 16. Avaliação | ✅ Existia |
| 17. Conclusões | ✅ Atualizado |
| Referências | ✅ +4 novas (Kyber, Podman, NIST IR8545, OWASP) |

---

## Checklist de Encerramento da Sprint 4

- [ ] Tabela 2 preenchida com dados reais de S4-T03 a S4-E03.
- [ ] Abstract/Resumo atualizado com resultados finais.
- [ ] `artigo.pdf` compilado sem erros.
- [ ] `paper.pdf` compilado sem erros.
- [ ] PDFs enviados para revisão dos orientadores.
- [ ] Feedback incorporado.
