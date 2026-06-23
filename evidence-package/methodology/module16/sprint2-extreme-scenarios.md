# Sprint 2 — Cenários Extremos Pendentes (S4-E01, S4-E02, S4-E03)

**Módulo**: 16 | **Sprint**: 2 | **Semanas**: 3–4

---

## Objetivo

Executar os três cenários extremos que ficaram pendentes do Módulo 14 Sprint 4,
validando resiliência, rollback e comportamento sob carga agressiva com perfil híbrido.

---

## S4-E01 — Indisponibilidade do security-integration-node (KMS/Event Bus)

### Objetivo
Medir comportamento seguro quando KMS, secrets e barramento de eventos tornam-se
indisponíveis, verificando MTTD, MTTR e rollback automático.

### Pré-condições
- Rota canário ativa com perfil híbrido (resultado de S4-T02 aprovado).
- Runbooks de contingência documentados em `docs/module14/pqc-cryptoagility-metrics-migration.md`.
- `observability-node` com alertas Prometheus configurados para `up{job="vault"}`.

### Execução
```bash
# 1. Registrar timestamp inicial
T_START=$(date -Iseconds)

# 2. Derrubar o security-integration-node (falha planejada)
podman stop security-integration-node
echo "Falha injetada em: $T_START" | tee ~/infra/logs/S4-E01-timeline.txt

# 3. Executar carga mínima contínua enquanto o nó está indisponível
podman exec load-chaos-node sh -lc \
  'k6 run --vus 2 --duration 120s /scripts/baseline.js \
   --summary-export /tmp/S4-E01-during-failure.json' &

# 4. Aguardar detecção pelo observability-node (MTTD)
podman exec observability-node sh -lc \
  'until promtool query instant "up{job=\"vault\"}" | grep -q "0"; do sleep 5; done
   echo "DETECTADO em: $(date -Iseconds)"' | tee -a ~/infra/logs/S4-E01-timeline.txt

# 5. Restaurar o nó e medir MTTR
T_RESTORE=$(date -Iseconds)
podman start security-integration-node
echo "Restaurado em: $T_RESTORE" | tee -a ~/infra/logs/S4-E01-timeline.txt

# 6. Aguardar serviços estabilizarem e coletar evidências
sleep 30
podman cp load-chaos-node:/tmp/S4-E01-during-failure.json ~/infra/logs/
```

### Métricas alvo
| ID | Meta | Descrição |
|---|---|---|
| OBS-02 | ≤ 5 min | MTTD da falha de KMS |
| RES-01 | ≤ 4 h | MTTR completo até serviço saudável |
| RES-02 | ≥ 99% | Rollback seguro se acionado |
| SEC-01 | ≤ 5 min | Tempo de detecção de incidente crítico |
| SEC-02 | ≤ 30 min | Tempo de resposta/mitigação completa |

### Critérios de aceitação
- `MTTD ≤ 5 min` confirmado via `S4-E01-timeline.txt`.
- Restauração completa com `MTTR ≤ 30 min`.
- Rollback para perfil clássico executado sem intervenção manual, se acionado.

### Evidências esperadas
- `S4-E01-timeline.txt` com timestamps de falha, detecção e restauração.
- `S4-E01-during-failure.json` (métricas de carga durante indisponibilidade).

---

## S4-E02 — Certificado Expirado em Rota Canário

### Objetivo
Validar detecção rápida de erro criptográfico de certificado e rollback seguro sem
propagação para todo o ambiente.

### Pré-condições
- Rota canário `k8s-worker-3:8080` ativa.
- Certificado de teste expirado disponível.
- Critérios de interrupção definidos em `docs/module14/metrics-resilience-matrix.md`.

### Execução
```bash
# 1. Gerar certificado expirado (-1 dia)
openssl req -x509 -newkey rsa:2048 -days -1 \
  -keyout /tmp/expired.key -out /tmp/expired.crt -nodes \
  -subj "/CN=canary-test-expired"

# 2. Injetar certificado expirado SOMENTE na rota canário
podman cp /tmp/expired.crt k8s-worker-3:/certs/server.crt
podman cp /tmp/expired.key  k8s-worker-3:/certs/server.key
podman exec k8s-worker-3 sh -lc "kill -HUP 1"  # reload sem restart

# 3. Executar carga controlada e capturar falhas de handshake
podman exec load-chaos-node sh -lc \
  'BASE_URL=http://k8s-worker-3:8080 \
   k6 run /scripts/canary-cert-fail.js \
   --summary-export /tmp/S4-E02-failure.json 2>&1 | tee /tmp/S4-E02-output.txt'

# 4. Registrar timestamp de detecção do alerta
T_ALERT=$(date -Iseconds)
echo "Alerta em: $T_ALERT" | tee ~/infra/logs/S4-E02-timeline.txt

# 5. Executar rollback — restaurar certificado válido
podman exec k8s-worker-3 sh -lc \
  "cp /certs/server.crt.bak /certs/server.crt && kill -HUP 1"
T_ROLLBACK=$(date -Iseconds)
echo "Rollback em: $T_ROLLBACK" | tee -a ~/infra/logs/S4-E02-timeline.txt

# 6. Confirmar restabelecimento com nova rodada de carga
podman exec load-chaos-node sh -lc \
  'BASE_URL=http://k8s-worker-3:8080 \
   k6 run --vus 2 --duration 30s /scripts/canary.js \
   --summary-export /tmp/S4-E02-after-rollback.json'

podman cp load-chaos-node:/tmp/S4-E02-failure.json      ~/infra/logs/
podman cp load-chaos-node:/tmp/S4-E02-after-rollback.json ~/infra/logs/
podman cp load-chaos-node:/tmp/S4-E02-output.txt        ~/infra/logs/
```

### Métricas alvo
| ID | Meta | Descrição |
|---|---|---|
| HYB-01 | > 99% | Sucesso de handshake após rollback |
| OBS-02 | ≤ 5 min | MTTD da falha de certificado |
| RES-02 | ≥ 99% | Rollback seguro |
| SEC-01 | ≤ 5 min | Tempo de detecção |
| SEC-02 | ≤ 30 min | Tempo de mitigação completa |

### Critérios de aceitação
- `http_req_failed` alto durante falha, caindo para < 1% após rollback.
- Rollback completo em ≤ 10 min.
- `HYB-01 > 99%` confirmado em `S4-E02-after-rollback.json`.

### Evidências esperadas
- `S4-E02-failure.json`
- `S4-E02-after-rollback.json`
- `S4-E02-output.txt`
- `S4-E02-timeline.txt`

---

## S4-E03 — Janela Comprimida de 10.000 Transações (Stress Curto)

### Objetivo
Verificar se a separação física do `load-chaos-node` mantém métricas observáveis
mesmo quando a carga total é comprimida em janela mais agressiva.

### Pré-condições
- Baseline S4-T01 aprovado (41,78 ms p95).
- Telemetria por pod/VM ativa no `observability-node`.

### Execução
```bash
# 1. Stress com 100 VUs durante 60s — mesma carga de S4-T01 em janela ~2x menor
podman exec load-chaos-node sh -lc \
  'k6 run --vus 100 --duration 60s /scripts/stress.js \
   --summary-export /tmp/S4-E03-stress.json 2>&1 | tee /tmp/S4-E03-output.txt'

# 2. Coletar métricas de CPU/memória do host durante o teste
podman stats --no-stream \
  k8s-worker-1 k8s-worker-2 k8s-worker-3 \
  --format "{{.Name}},{{.CPUPerc}},{{.MemPerc}}" \
  > ~/infra/logs/S4-E03-resource-snapshot.csv

podman cp load-chaos-node:/tmp/S4-E03-stress.json  ~/infra/logs/
podman cp load-chaos-node:/tmp/S4-E03-output.txt   ~/infra/logs/
```

### Métricas alvo
| ID | Meta | Descrição |
|---|---|---|
| HYB-02 | ≤ 5% | Overhead de latência híbrido vs. baseline |
| COST-01 | ≤ +15% | Custo incremental por 1M req |
| LAT-01 | p95 ≤ 150 ms | Latência ponta a ponta |
| THR-01 | ≥ 99% | Taxa de sucesso |
| PQC-OVH-01 | ≤ 15% | Overhead de handshake PQC |
| PQC-OVH-02 | ΔCPU ≤ +20% | Overhead computacional |

### Critérios de aceitação
- `p95 ≤ 150 ms` mesmo com 100 VUs simultâneos.
- `ΔCPU ≤ +20%` vs. baseline S4-T01 (conforme snapshot de recursos).
- Carga gerada **somente** do `load-chaos-node`, sem contaminação do cluster principal.

### Evidências esperadas
- `S4-E03-stress.json`
- `S4-E03-output.txt`
- `S4-E03-resource-snapshot.csv`

---

## Checklist de Encerramento da Sprint 2

- [ ] S4-E01 executado com timeline de falha/detecção/restauração registrada.
- [ ] S4-E02 executado com evidência de rollback e recovery de handshake.
- [ ] S4-E03 executado com snapshot de recursos durante stress.
- [ ] Todos os JSONs e CSVs em `~/infra/logs/` e versionados em `docs/module16/evidence/`.
- [ ] MTTD/MTTR registrados e comparados com metas da Tabela de Métricas do artigo.
