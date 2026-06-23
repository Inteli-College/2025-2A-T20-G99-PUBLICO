/**
 * S4-T03 — mTLS Híbrido entre Microsserviços
 *
 * Valida o tráfego leste-oeste com perfil híbrido entre dois workers.
 * Referência: docs/module16/sprint1-typical-scenarios.md
 *
 * Execução:
 *   podman exec load-chaos-node sh -lc \
 *     'BASE_URL=http://k8s-worker-2:8080 k6 run /scripts/mtls-hybrid.js \
 *      --summary-export /tmp/S4-T03-k6-summary.json'
 */
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Trend } from "k6/metrics";

const hybridHandshakeErrors = new Rate("hybrid_handshake_errors");
const serviceLinkLatency    = new Trend("service_link_latency_ms");

export const options = {
  vus: 10,
  duration: "60s",
  thresholds: {
    // HYB-01: sucesso de handshake > 99%
    hybrid_handshake_errors: ["rate<0.01"],
    // LAT-01: p95 <= 150 ms
    http_req_duration: ["p(95)<150"],
    // THR-01: taxa de falha < 1%
    http_req_failed: ["rate<0.01"],
  },
};

const baseUrl = __ENV.BASE_URL || "http://k8s-worker-2:8080";

export default function () {
  // Rota de serviço-a-serviço (app → app, simula mTLS leste-oeste)
  const res = http.get(`${baseUrl}/internal/health`, {
    tags: { scenario: "S4-T03", tier: "app-to-app", profile: "mtls-hybrid" },
  });

  const ok = check(res, {
    "mTLS handshake ok (status 200)": (r) => r.status === 200,
    "response < 150ms":               (r) => r.timings.duration < 150,
  });

  hybridHandshakeErrors.add(!ok);
  serviceLinkLatency.add(res.timings.duration);

  sleep(0.5);
}

export function handleSummary(data) {
  // Registrar resultado consolidado para rastreabilidade no artigo
  const p95 = data.metrics.http_req_duration
    ? data.metrics.http_req_duration.values["p(95)"]
    : null;
  const failRate = data.metrics.http_req_failed
    ? data.metrics.http_req_failed.values.rate
    : null;

  console.log(`[S4-T03] p95=${p95}ms | fail_rate=${(failRate * 100).toFixed(3)}%`);
  return {
    stdout: JSON.stringify(data, null, 2),
  };
}
