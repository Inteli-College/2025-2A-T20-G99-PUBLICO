/**
 * S4-E03 — Janela Comprimida de 10.000 Transações (Stress Curto)
 *
 * Executa o mesmo volume de S4-T01 em janela ~2x menor e com VUs maiores,
 * medindo overhead PQC sob carga agressiva.
 * Referência: docs/module16/sprint2-extreme-scenarios.md
 *
 * Execução:
 *   k6 run --vus 100 --duration 60s /scripts/stress.js \
 *     --summary-export /tmp/S4-E03-stress.json
 */
import http from "k6/http";
import { check, sleep } from "k6";
import { Trend, Rate } from "k6/metrics";

const p95Latency  = new Trend("stress_p95_latency_ms");
const failureRate = new Rate("stress_failure_rate");

export const options = {
  vus: 100,
  duration: "60s",
  thresholds: {
    // LAT-01: mesmo sob stress, p95 deve manter-se <= 150 ms
    http_req_duration: ["p(95)<150"],
    // THR-01: sucesso >= 99%
    http_req_failed: ["rate<0.01"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://k8s-worker-1:8080";

export default function () {
  const res = http.get(`${BASE_URL}/chain`, {
    tags: { scenario: "S4-E03", tier: "web-app-data", phase: "stress" },
  });

  const ok = check(res, {
    "stress: status 200":    (r) => r.status === 200,
    "stress: latency < 150": (r) => r.timings.duration < 150,
  });

  p95Latency.add(res.timings.duration);
  failureRate.add(!ok);

  // Sem sleep — janela comprimida intencional
}

export function handleSummary(data) {
  const p95   = data.metrics.http_req_duration?.values["p(95)"] ?? 0;
  const rps   = data.metrics.http_reqs?.values.rate ?? 0;
  const fails = data.metrics.http_req_failed?.values.rate ?? 0;

  console.log(
    `[S4-E03] p95=${p95.toFixed(2)}ms | rps=${rps.toFixed(1)} | ` +
    `fail=${(fails * 100).toFixed(3)}%`
  );

  return { stdout: JSON.stringify(data, null, 2) };
}
