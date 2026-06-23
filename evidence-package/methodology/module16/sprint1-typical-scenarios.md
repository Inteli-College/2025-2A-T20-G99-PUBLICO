# Sprint 1 — Cenários Típicos Pendentes (S4-T03, S4-T04, S4-T06)

**Módulo**: 16 | **Sprint**: 1 | **Semanas**: 1–2

---

## Objetivo

Executar os três cenários típicos que ficaram pendentes do Módulo 14 Sprint 4, coletando
evidências JSON para substituir os dados sintéticos do artigo.

---

## S4-T03 — mTLS Híbrido entre Microsserviços

### Objetivo
Validar mTLS com perfil híbrido (X25519 + Kyber-768) no tráfego leste-oeste entre
`k8s-worker-1` → `k8s-worker-2` (rota `api-orders` ↔ `api-payments`).

### Pré-condições
- Topologia Podman rodando: `podman compose -f lab/topology/docker-compose.yml ps`
- Baseline S4-T01 aprovado (já executado no Módulo 15).

### Execução
```bash
# 1. Executar cenário mTLS híbrido a partir do load-chaos-node
podman exec load-chaos-node sh -lc \
  'BASE_URL=http://k8s-worker-2:8080 \
   k6 run /scripts/mtls-hybrid.js \
   --summary-export /tmp/S4-T03-k6-summary.json 2>&1 | tee /tmp/S4-T03-k6-output.txt'

# 2. Copiar evidências para o host
podman cp load-chaos-node:/tmp/S4-T03-k6-summary.json ~/infra/logs/
podman cp load-chaos-node:/tmp/S4-T03-k6-output.txt  ~/infra/logs/
```

### Métricas alvo
| ID | Meta | Descrição |
|---|---|---|
| HYB-01 | > 99% | Sucesso de handshake mTLS híbrido |
| HYB-02 | ≤ 5% | Overhead de latência vs. baseline clássico |
| OBS-02 | ≤ 5 min | MTTD de desvio de política simulado |
| RES-02 | ≥ 99% | Rollback seguro após desvio |

### Critérios de aceitação
- `http_req_failed < 1%` na rota leste-oeste.
- `p95 latência` dentro de 5% do baseline de S4-T01 (41,78 ms → ≤ 43,87 ms).
- Desvio de política detectado em ≤ 5 min após injeção.

### Evidências esperadas
- `S4-T03-k6-summary.json`
- `S4-T03-k6-output.txt`
- Comparativo clássico vs. mTLS híbrido no relatório.

---

## S4-T04 — Rotação Planejada de Segredos e Certificados

### Objetivo
Confirmar rotação automatizada de certificados TLS no `security-integration-node`
(Vault simulado) com CBOM before/after vinculado.

### Pré-condições
- `security-integration-node` rodando com Vault em modo dev.
- CBOM pré-rotação gerado por `code/cbomkit_cli.py`.

### Execução
```bash
# 1. Gerar CBOM antes da rotação
podman exec k8s-control sh -lc \
  "python /workspace/code/cbomkit_cli.py \
   --target web-portal:web:src \
   --target api-orders:app:src \
   --output /evidence/S4-T04/cbom-before-rotation.json"

# 2. Executar rotação de segredos no Vault simulado
podman exec security-integration-node sh -lc \
  "vault write pki/intermediate/rotate \
   && echo '{\"rotated_at\":\"'$(date -Iseconds)'\"}' \
      > /evidence/S4-T04/rotation-log.json"

# 3. Gerar CBOM após rotação
podman exec k8s-control sh -lc \
  "python /workspace/code/cbomkit_cli.py \
   --target web-portal:web:src \
   --target api-orders:app:src \
   --output /evidence/S4-T04/cbom-after-rotation.json"

# 4. Copiar evidências
podman cp k8s-control:/evidence/S4-T04 ~/infra/logs/S4-T04/
```

### Métricas alvo
| ID | Meta | Descrição |
|---|---|---|
| KLC-01 | ≥ 90% | Rotação automatizada de segredos |
| GOV-01 | 100% | CBOM before/after em todas as trocas |
| OBS-01 | 100% | Cobertura de métricas nos serviços envolvidos |

### Critérios de aceitação
- CBOM before e after presentes e com `cbom_version` diferente.
- Log de rotação registrado com timestamp.
- Nenhuma interrupção de serviço durante rotação.

### Evidências esperadas
- `S4-T04/cbom-before-rotation.json`
- `S4-T04/cbom-after-rotation.json`
- `S4-T04/rotation-log.json`

---

## S4-T06 — Cobertura de Observabilidade e Custo

### Objetivo
Verificar que a arquitetura proposta separa coleta de métricas e permite comparar custo
incremental do perfil híbrido sem contaminar o sistema sob teste.

### Pré-condições
- `observability-node` com Prometheus e Grafana ativos.
- Perfis clássico e híbrido disponíveis em rotas separadas.

### Execução
```bash
# 1. Coletar métricas com perfil CLÁSSICO
podman exec load-chaos-node sh -lc \
  'PROFILE=classic BASE_URL=http://k8s-worker-1:8080 \
   k6 run /scripts/cost-obs.js \
   --summary-export /tmp/S4-T06-classic.json'

# 2. Coletar métricas com perfil HÍBRIDO
podman exec load-chaos-node sh -lc \
  'PROFILE=hybrid BASE_URL=http://k8s-worker-3:8080 \
   k6 run /scripts/cost-obs.js \
   --summary-export /tmp/S4-T06-hybrid.json'

# 3. Comparar throughput e estimar custo
podman exec load-chaos-node sh -lc \
  'python3 /scripts/compare-cost.py \
   /tmp/S4-T06-classic.json \
   /tmp/S4-T06-hybrid.json \
   > /tmp/S4-T06-cost-delta.json'

# 4. Copiar
podman cp load-chaos-node:/tmp/S4-T06-classic.json ~/infra/logs/
podman cp load-chaos-node:/tmp/S4-T06-hybrid.json  ~/infra/logs/
podman cp load-chaos-node:/tmp/S4-T06-cost-delta.json ~/infra/logs/
```

### Métricas alvo
| ID | Meta | Descrição |
|---|---|---|
| OBS-01 | 100% | Todos os serviços com métricas ativas |
| OBS-02 | ≤ 5 min | MTTD para desvio controlado de baixa severidade |
| COST-01 | ≤ +15% | Custo incremental por 1M req (perfil híbrido vs. clássico) |
| THR-01 | ≥ 99% | Taxa de sucesso de requisições |

### Critérios de aceitação
- `S4-T06-cost-delta.json` com campo `cost_increase_pct ≤ 15`.
- `THR-01 sucesso ≥ 99%` em ambos os perfis.

### Evidências esperadas
- `S4-T06-classic.json`
- `S4-T06-hybrid.json`
- `S4-T06-cost-delta.json`

---

## Checklist de Encerramento da Sprint 1

- [ ] S4-T03 executado e `S4-T03-k6-summary.json` coletado.
- [ ] S4-T04 executado com CBOM before/after registrado.
- [ ] S4-T06 executado com comparativo de custo clássico vs. híbrido.
- [ ] Todos os JSONs em `~/infra/logs/` e versionados em `docs/module16/evidence/`.
- [ ] Tabela de resultados no artigo atualizada com dados reais desta sprint.
