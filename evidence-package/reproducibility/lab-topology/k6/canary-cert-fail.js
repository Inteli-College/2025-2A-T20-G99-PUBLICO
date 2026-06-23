/**
 * S4-E02 — Certificado Expirado em Rota Canário
 *
 * Executa carga na rota canário após injeção de certificado expirado.
 * Espera falhas de handshake elevadas; mede recuperação pós-rollback.
 * Referência: docs/module16/sprint2-extreme-scenarios.md
 *
 * Execução (durante falha):
 *   BASE_URL=http://k8s-worker-3:8080 k6 run /scripts/canary-cert-fail.js \
 *     --summary-export /tmp/S4-E02-failure.json
 */
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

const handshakeFailures = new Rate("handshake_failures");

export const options = {
  vus: 5,
  duration: "30s",
  // Durante a injeção de cert expirado, NÃO queremos thresholds que abortam o teste.
  // Os dados de falha são as evidências do cenário.
  thresholds: {},
};

const BASE_URL = __ENV.BASE_URL || "http://k8s-worker-3:8080";

export default function () {
  const res = http.get(`${BASE_URL}/chain`, {
    tags: { scenario: "S4-E02", tier: "canary", phase: "cert-expired" },
  });

  const isOk = check(res, {
    "handshake success": (r) => r.status === 200,
  });

  handshakeFailures.add(!isOk);
  sleep(1);
}

export function handleSummary(data) {
  const failRate = data.metrics.http_req_failed?.values.rate ?? 0;
  const p95      = data.metrics.http_req_duration?.values["p(95)"] ?? 0;

  console.log(
    `[S4-E02] fail_rate=${(failRate * 100).toFixed(2)}% | p95=${p95.toFixed(2)}ms`
  );
  console.log(
    failRate > 0.5
      ? "[S4-E02] ✓ Falhas detectadas — certificado expirado em efeito."
      : "[S4-E02] ✗ Falhas não detectadas — verificar injeção do certificado."
  );

  return { stdout: JSON.stringify(data, null, 2) };
}
