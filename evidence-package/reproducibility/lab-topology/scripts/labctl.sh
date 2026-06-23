#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPOLOGY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
COMPOSE_FILE="${TOPOLOGY_DIR}/docker-compose.yml"
RUNTIME_DIR="${TOPOLOGY_DIR}/runtime"
EVIDENCE_DIR="${RUNTIME_DIR}/evidence"

require_docker() {
  if ! docker ps >/dev/null 2>&1; then
    echo "Docker nao esta acessivel para a sua conta." >&2
    echo "Consulte: ${TOPOLOGY_DIR}/ACCESS_REQUEST.md" >&2
    exit 1
  fi
}

compose() {
  docker compose -f "${COMPOSE_FILE}" "$@"
}

prepare_runtime() {
  mkdir -p \
    "${EVIDENCE_DIR}/gateway" \
    "${EVIDENCE_DIR}/inventory" \
    "${EVIDENCE_DIR}/integrity" \
    "${EVIDENCE_DIR}/scenarios/S4-T01" \
    "${EVIDENCE_DIR}/scenarios/S4-T02" \
    "${EVIDENCE_DIR}/scenarios/S4-T03" \
    "${EVIDENCE_DIR}/scenarios/S4-T05" \
    "${EVIDENCE_DIR}/scenarios/S4-E04" \
    "${RUNTIME_DIR}/postgres" \
    "${RUNTIME_DIR}/prometheus"
}

check_access() {
  if docker ps >/dev/null 2>&1; then
    echo "Docker acessivel."
    docker info --format 'ServerVersion={{.ServerVersion}}'
  else
    echo "Docker indisponivel para esta conta."
    echo "Pedido sugerido: ${TOPOLOGY_DIR}/ACCESS_REQUEST.md"
    return 1
  fi
}

start_lab() {
  require_docker
  prepare_runtime
  compose up -d --build
  compose ps
}

stop_lab() {
  require_docker
  compose down --remove-orphans
}

status_lab() {
  require_docker
  compose ps
}

run_s4_t01() {
  require_docker
  prepare_runtime
  compose up -d
  compose exec -T load-chaos-node sh -lc \
    'mkdir -p /evidence/scenarios/S4-T01 && k6 run /scripts/baseline.js --summary-export /evidence/scenarios/S4-T01/k6-summary.json' \
    | tee "${EVIDENCE_DIR}/scenarios/S4-T01/k6-output.txt"
}

run_s4_t02() {
  require_docker
  prepare_runtime
  compose up -d
  compose exec -T load-chaos-node sh -lc \
    'mkdir -p /evidence/scenarios/S4-T02 && BASE_URL=http://k8s-worker-3:8080 k6 run /scripts/canary.js --summary-export /evidence/scenarios/S4-T02/k6-summary.json' \
    | tee "${EVIDENCE_DIR}/scenarios/S4-T02/k6-output.txt"
}

run_s4_t03() {
  require_docker
  prepare_runtime
  compose up -d
  compose exec -T k8s-control python - <<'PY' | tee "${EVIDENCE_DIR}/scenarios/S4-T03/app-chain.json"
import json
import urllib.request

with urllib.request.urlopen("http://k8s-worker-2:8080/chain", timeout=10) as response:
    payload = json.loads(response.read().decode("utf-8"))

print(json.dumps(payload, indent=2))
PY
}

run_s4_t05() {
  require_docker
  prepare_runtime
  compose up -d
  compose exec -T k8s-control sh -lc "
    mkdir -p /evidence/scenarios/S4-T05/gateway /evidence/scenarios/S4-T05/inventory && \
    python /workspace/code/cbom_gateway.py \
      --cbom /workspace/code/samples/cbom-three-tier.json \
      --output /evidence/scenarios/S4-T05/gateway/cbom-summary.json \
      | tee /evidence/scenarios/S4-T05/gateway/cbom-gateway-report.txt && \
    python /workspace/code/cbomkit_cli.py \
      --target repo:web:/workspace \
      --output /evidence/scenarios/S4-T05/inventory/cbomkit-scan.json \
      | tee /evidence/scenarios/S4-T05/inventory/cbomkit-scan.log
  "
}

run_s4_e04() {
  require_docker
  prepare_runtime
  compose up -d
  compose exec -T k8s-control sh -lc "
    mkdir -p /evidence/scenarios/S4-E04 && \
    python - <<'PY'
import hashlib
import json
from pathlib import Path

source = Path('/workspace/code/samples/cbom-three-tier.json')
target = Path('/evidence/scenarios/S4-E04/cbom-three-tier-tampered.json')
data = json.loads(source.read_text())
target.write_text(json.dumps(data, indent=2), encoding='utf-8')
tampered = json.loads(target.read_text())
tampered[0]['crypto'][0]['algo'] = 'RSA-1024'
target.write_text(json.dumps(tampered, indent=2), encoding='utf-8')

for label, path in [('original', source), ('tampered', target)]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    out = Path(f'/evidence/scenarios/S4-E04/{label}.sha256.txt')
    out.write_text(f'{digest}  {path}\\n', encoding='utf-8')
PY
    python /workspace/code/cbom_gateway.py \
      --cbom /workspace/code/samples/cbom-three-tier.json \
      --output /evidence/scenarios/S4-E04/original-summary.json \
      | tee /evidence/scenarios/S4-E04/original-report.txt && \
    python /workspace/code/cbom_gateway.py \
      --cbom /evidence/scenarios/S4-E04/cbom-three-tier-tampered.json \
      --output /evidence/scenarios/S4-E04/tampered-summary.json \
      | tee /evidence/scenarios/S4-E04/tampered-report.txt
  "
}

collect_evidence() {
  prepare_runtime
  tar -czf "${RUNTIME_DIR}/module14-evidence.tgz" -C "${RUNTIME_DIR}" evidence
  ls -lh "${RUNTIME_DIR}/module14-evidence.tgz"
}

usage() {
  cat <<'EOF'
Uso: lab/topology/scripts/labctl.sh <comando>

Comandos:
  check      Verifica se Docker esta acessivel para a conta atual
  start      Sobe a topologia de 8 nos logicos
  stop       Remove o laboratorio
  status     Mostra o estado atual dos servicos
  s4-t01     Executa o baseline classico com k6
  s4-t02     Executa o canario inicial contra o no app-canary
  s4-t03     Exercita a comunicacao interna app -> seguranca -> dados
  s4-t05     Executa o fluxo discover -> decision -> swap com CBOM
  s4-e04     Executa o teste de integridade/adulteracao de CBOM
  collect    Compacta as evidencias geradas em runtime
EOF
}

main() {
  command="${1:-}"
  case "${command}" in
    check) check_access ;;
    start) start_lab ;;
    stop) stop_lab ;;
    status) status_lab ;;
    s4-t01) run_s4_t01 ;;
    s4-t02) run_s4_t02 ;;
    s4-t03) run_s4_t03 ;;
    s4-t05) run_s4_t05 ;;
    s4-e04) run_s4_e04 ;;
    collect) collect_evidence ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"
