# Configuração do Ambiente Simulado de 8 Nós no Servidor Acadêmico

**Projeto/Artefato**: Gateway de Criptoagilidade para migração PQC em ambiente híbrido three-tier  
**Módulo**: 14  
**Data**: 2026-04-07  

---

## 1. Objetivo

Documentar o procedimento completo de configuração e implantação da topologia simulada de **8 nós lógicos** em servidor acadêmico, conforme especificado em `docs/governance/requisitos-ambiente.md` e `docs/module14/sprint4/vm-network-topology.md`.

A simulação substitui 8 VMs reais por 8 containers isolados em redes dedicadas, executados via **Podman rootless** em host único, preservando o isolamento lógico entre camadas e a separação de responsabilidades descrita na arquitetura.

---

## 2. Ambiente do servidor

| Atributo | Valor observado |
| --- | --- |
| Sistema operacional | Ubuntu 24.04.3 LTS (GNU/Linux 6.8.0-100-generic x86_64) |
| CPU | 64 vCPUs — Intel Xeon Gold 6454S (1 socket, 32 cores, 2 threads/core) |
| Virtualização | VT-x habilitado, KVM disponível |
| RAM | 125 GiB |
| Disco raiz | 98 GB (`/dev/mapper/ubuntu--vg-ubuntu--lv`) |
| Disco adicional | 2.4 TB (`/dev/mapper/ubuntu--vg-lv_mnt_sda3`, montado em `/mnt/sda3`) |
| GPU | NVIDIA L4 23 GB (disponível, não utilizada pela simulação) |
| Container runtime | Podman 4.9.3, modo rootless |
| Compose provider | `/usr/libexec/docker/cli-plugins/docker-compose` v5.0.2 (via `podman compose`) |
| Home do usuário | `/home2/thomaz-barboza` (symlink para `/mnt/sda3/home2/...`) |
| Acesso | SSH via VPN acadêmica (`thomaz-barboza@10.8.8.10`) |

O servidor atende com folga os requisitos mínimos de `52 vCPU` e `120 GB RAM` descritos em `docs/governance/requisitos-ambiente.md`, mesmo consolidando tudo em host único.

---

## 3. Preparação do servidor

### 3.1 Acesso e estrutura de diretórios

```bash
ssh thomaz-barboza@10.8.8.10

mkdir -p ~/infra/{apps,data,logs,envs,scripts}
cd ~/infra
```

### 3.2 Sessão persistente com tmux

```bash
tmux new -s infra
```

O uso de `tmux` garante que a sessão sobrevive a desconexões de rede, essencial para operações longas como build de imagens.

### 3.3 Ambiente Python (para protótipos)

```bash
python3 -m venv ~/infra/envs/app
source ~/infra/envs/app/bin/activate
pip install --upgrade pip
```

### 3.4 Ativação do Podman socket

O servidor possui `podman 4.9.3` instalado, mas o socket de API não estava ativo por padrão. O provider `docker-compose` (usado por `podman compose`) requer esse socket:

```bash
systemctl --user enable --now podman.socket
systemctl --user status podman.socket
ls -l /run/user/$UID/podman/podman.sock
```

Resultado esperado: socket ativo em `/run/user/<UID>/podman/podman.sock`.

---

## 4. Transferência do repositório

O repositório foi sincronizado da máquina local para o servidor via `rsync`, excluindo artefatos de runtime gerados localmente:

```bash
# Executar na máquina local (não no servidor)
rsync -av \
  --exclude ".git" \
  --exclude "lab/topology/runtime/" \
  "/Users/klubi/Documents/GitHub/2025-2A-T20-G99-INTERNO/" \
  thomaz-barboza@10.8.8.10:~/infra/apps/2025-2A-T20-G99-INTERNO/
```

A exclusão de `lab/topology/runtime/` é obrigatória: esse diretório contém dados de PostgreSQL e evidências com permissões específicas de container que causam erros de `rsync` se copiados entre hosts.

---

## 5. Implantação da topologia de 8 nós

### 5.1 Validação do compose

```bash
cd ~/infra/apps/2025-2A-T20-G99-INTERNO
podman compose -f lab/topology/docker-compose.yml config
```

Este comando valida a sintaxe e resolve caminhos antes do build. Se reportar erro de socket, verificar o passo 3.4.

### 5.2 Build e inicialização

```bash
podman compose -f lab/topology/docker-compose.yml up -d --build
```

O primeiro build:
- Baixa as imagens base: `python:3.12-slim`, `postgres:latest`, `prom/prometheus:latest`, `grafana/k6:latest`.
- Constrói a imagem do mock-node (Python + psycopg) para os 5 nós customizados.
- Cria as 5 redes isoladas e os 8 containers.

Tempo típico do primeiro build: ~2 minutos (dependente da rede).

### 5.3 Verificação de estado

```bash
podman compose -f lab/topology/docker-compose.yml ps
```

Todos os 8 nós devem estar `Up` e os nós com healthcheck devem estar `healthy`:

| Container | Imagem | Estado esperado |
| --- | --- | --- |
| `k8s-control` | topology-k8s-control | Up (healthy) |
| `k8s-worker-1` | topology-k8s-worker-1 | Up (healthy) |
| `k8s-worker-2` | topology-k8s-worker-2 | Up (healthy) |
| `k8s-worker-3` | topology-k8s-worker-3 | Up (healthy) |
| `data-node` | postgres:latest | Up (healthy) |
| `security-integration-node` | topology-security-integration-node | Up (healthy) |
| `observability-node` | prom/prometheus:latest | Up |
| `load-chaos-node` | grafana/k6:latest | Up |

### 5.4 Verificação de saúde individual

```bash
podman inspect k8s-control --format '{{json .State.Health}}'
podman inspect security-integration-node --format '{{json .State.Health}}'
```

---

## 6. Mapeamento entre nós lógicos e arquitetura

| Nó container | Papel na arquitetura | Rede(s) | Correspondência em `requisitos-ambiente.md` |
| --- | --- | --- | --- |
| `k8s-control` | Plano de controle do cluster | cluster_net, observability_net | VM `k8s-control` |
| `k8s-worker-1` | Camada web (baseline) | ingress_net, cluster_net, observability_net | VM `k8s-worker` #1 |
| `k8s-worker-2` | Camada de aplicação | cluster_net, data_net, security_net, observability_net | VM `k8s-worker` #2 |
| `k8s-worker-3` | Camada de aplicação (canário) | ingress_net, cluster_net, data_net, security_net, observability_net | VM `k8s-worker` #3 |
| `data-node` | Banco relacional (PostgreSQL) | data_net, observability_net | VM `data-node` |
| `security-integration-node` | Integração de segurança/KMS mock | security_net, observability_net | VM `security-integration-node` |
| `observability-node` | Prometheus para telemetria | observability_net | VM `observability-node` |
| `load-chaos-node` | k6 para carga e caos | ingress_net, observability_net | VM `load-chaos-node` |

### Redes isoladas

| Rede | Tipo | Propósito |
| --- | --- | --- |
| `ingress_net` | bridge (externa) | Tráfego norte-sul; acesso do load-chaos-node aos workers web |
| `cluster_net` | bridge (interna) | Comunicação intra-cluster entre control e workers |
| `data_net` | bridge (interna) | Acesso dos workers ao banco de dados |
| `security_net` | bridge (interna) | Acesso dos workers ao nó de segurança/KMS |
| `observability_net` | bridge (interna) | Coleta de métricas de todos os nós pelo Prometheus |

Redes marcadas como `internal: true` impedem acesso externo direto, preservando o isolamento descrito em `docs/module14/sprint4/vm-network-topology.md`.

---

## 7. Compatibilizações necessárias para Podman rootless

### 7.1 Healthchecks: CMD → CMD-SHELL

O provider `docker-compose` usado pelo `podman compose` no servidor interpretava incorretamente healthchecks com `CMD` e argumentos Python inline, marcando serviços saudáveis como `unhealthy`.

**Antes** (falha no servidor):
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; ..."]
```

**Depois** (funciona no servidor):
```yaml
healthcheck:
  test: ["CMD-SHELL", "python -c \"import urllib.request; ...\""]
```

### 7.2 Volume do PostgreSQL

O bind mount do PostgreSQL precisou apontar para `/var/lib/postgresql` (não `/var/lib/postgresql/data`) para evitar erros de inicialização quando o diretório de dados é criado pelo Podman rootless com mapeamento de UID.

### 7.3 Entrypoint do k6

A imagem `grafana/k6` tem o binário `k6` como entrypoint padrão. Para manter o container ativo como "nó de carga disponível", o entrypoint foi substituído:

```yaml
entrypoint: ["/bin/sh", "-ec", "sleep 31536000"]
```

### 7.4 Escrita de evidências do k6

Os resumos JSON gerados pelo k6 apresentaram restrição de escrita no bind mount `/evidence` dentro do container `load-chaos-node`. A solução foi gravar em `/tmp` e copiar para o host:

```bash
podman exec load-chaos-node sh -lc 'k6 run /scripts/baseline.js --summary-export /tmp/k6-summary.json'
podman cp load-chaos-node:/tmp/k6-summary.json ~/infra/logs/S4-T01-k6-summary.json
```

---

## 8. Execução dos cenários experimentais

### 8.1 S4-T01 — Baseline clássico

```bash
podman exec load-chaos-node sh -lc \
  'k6 run /scripts/baseline.js --summary-export /tmp/S4-T01-k6-summary.json' \
  | tee ~/infra/logs/S4-T01-k6-output.txt
podman cp load-chaos-node:/tmp/S4-T01-k6-summary.json ~/infra/logs/S4-T01-k6-summary.json
```

Resultado: `p95 = 41,78 ms`, `http_req_failed = 0,00%`, 150 requisições bem-sucedidas.

### 8.2 S4-T02 — Canário

```bash
podman exec load-chaos-node sh -lc \
  'BASE_URL=http://k8s-worker-3:8080 k6 run /scripts/canary.js --summary-export /tmp/S4-T02-k6-summary.json' \
  | tee ~/infra/logs/S4-T02-k6-output.txt
podman cp load-chaos-node:/tmp/S4-T02-k6-summary.json ~/infra/logs/S4-T02-k6-summary.json
```

Resultado: `p95 = 25,47 ms`, `http_req_failed = 0,00%`, 40 requisições bem-sucedidas.

### 8.3 S4-T05 — Fluxo CBOM discover → decision → swap

```bash
podman exec k8s-control sh -lc "
  python /workspace/code/cbom_gateway.py \
    --cbom /workspace/code/samples/cbom-three-tier.json \
    --output /evidence/scenarios/S4-T05/gateway/cbom-summary.json
"
```

Resultado: 2 ações de migração geradas (web e app).

```bash
podman exec k8s-control sh -lc "
  python /workspace/code/cbomkit_cli.py \
    --target repo:web:/workspace \
    --output /evidence/scenarios/S4-T05/inventory/cbomkit-scan.json
"
```

Resultado: manifesto com 10 arquivos contendo achados e 1023 ocorrências textuais.

### 8.4 S4-E04 — Teste de integridade/adulteração de CBOM

Execução em duas etapas:
1. Gerar manifesto adulterado com algoritmo alterado e calcular hashes.
2. Comparar as saídas do gateway para manifesto original vs. adulterado.

```bash
podman exec k8s-control sh -lc "
  python /workspace/code/cbom_gateway.py \
    --cbom /workspace/code/samples/cbom-three-tier.json
"
# Resultado: 2 ações de migração

podman exec k8s-control sh -lc "
  python /workspace/code/cbom_gateway.py \
    --cbom /evidence/scenarios/S4-E04/cbom-three-tier-tampered.json
"
# Resultado: 1 ação de migração (gap — artefato adulterado não foi bloqueado)
```

---

## 9. Coleta e preservação de evidências

### 9.1 Evidências no servidor

```bash
~/infra/logs/S4-T01-k6-summary.json
~/infra/logs/S4-T01-k6-output.txt
~/infra/logs/S4-T02-k6-summary.json
~/infra/logs/S4-T02-k6-output.txt
```

### 9.2 Arquivo consolidado

```bash
tar -czf ~/infra/logs/module14-podman-evidence.tgz \
  -C ~/infra/apps/2025-2A-T20-G99-INTERNO/lab/topology/runtime evidence \
  -C ~/infra/logs S4-T01-k6-summary.json S4-T01-k6-output.txt \
                  S4-T02-k6-summary.json S4-T02-k6-output.txt
```

### 9.3 Evidências dentro do laboratório

Artefatos gerados pelos cenários ficam em:
- `lab/topology/runtime/evidence/gateway/`
- `lab/topology/runtime/evidence/inventory/`
- `lab/topology/runtime/evidence/integrity/`
- `lab/topology/runtime/evidence/scenarios/S4-T01/`
- `lab/topology/runtime/evidence/scenarios/S4-T02/`
- `lab/topology/runtime/evidence/scenarios/S4-T05/`
- `lab/topology/runtime/evidence/scenarios/S4-E04/`
- `lab/topology/runtime/evidence/runtime/` (eventos JSONL dos nós)

---

## 10. Encerramento do laboratório

```bash
podman compose -f lab/topology/docker-compose.yml down --remove-orphans
```

Para limpeza completa (remove dados de runtime):

```bash
rm -rf lab/topology/runtime/postgres lab/topology/runtime/prometheus lab/topology/runtime/evidence
```

---

## 11. Referências internas

- Requisitos de ambiente: `docs/governance/requisitos-ambiente.md`
- Topologia de rede: `docs/module14/sprint4/vm-network-topology.md`
- Cenários experimentais: `docs/module14/sprint4/experiment-scenarios.md`
- Relatório de validação (PT): `docs/module14/sprint5-validacao-arquitetural-seguranca.md`
- Relatório de validação (EN): `docs/module14/sprint5-architectural-security-validation.md`
- README do laboratório: `lab/topology/README.md`
- Script de orquestração: `lab/topology/scripts/labctl.sh`
- Docker Compose: `lab/topology/docker-compose.yml`
