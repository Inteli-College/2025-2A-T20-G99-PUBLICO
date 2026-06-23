/**
 * S4-T06 — Cobertura de Observabilidade e Custo Incremental
 *
 * Compara throughput e latência entre perfil clássico e híbrido
 * para estimar custo incremental (COST-01).
 * Referência: docs/module16/sprint1-typical-scenarios.md
 *
 * Execução (clássico):
 *   PROFILE=classic BASE_URL=http://k8s-worker-1:8080 k6 run /scripts/cost-obs.js \
 *     --summary-export /tmp/S4-T06-classic.json
 *
 * Execução (híbrido):
 *   PROFILE=hybrid BASE_URL=http://k8s-worker-3:8080 k6 run /scripts/cost-obs.js \
 *     --summary-export /tmp/S4-T06-hybrid.json
 */
import http from "k6/http";
import { check, sleep } from "k6";
import { Counter, Trend } from "k6/metrics";

const requestsOk   = new Counter("requests_ok");
const endToEndTime = new Trend("end_to_end_ms");

const PROFILE  = __ENV.PROFILE  || "unknown";
const BASE_URL = __ENV.BASE_URL || "http://k8s-worker-1:8080";

export const options = {
  stages: [
    { duration: "15s", target: 20 },   // ramp-up
    { duration: "30s", target: 20 },   // estável — janela de medição
    { duration: "15s", target:  0 },   // ramp-down
  ],
  thresholds: {
    // THR-01
    http_req_failed:   ["rate<0.01"],
    // LAT-01
    http_req_duration: ["p(95)<150"],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/chain`, {
    tags: { scenario: "S4-T06", profile: PROFILE, tier: "web-app-data" },
  });

  const ok = check(res, {
    "status 200": (r) => r.status === 200,
  });

  if (ok) requestsOk.add(1);
  endToEndTime.add(res.timings.duration);

  sleep(0.5);
}

export function handleSummary(data) {
  const p95      = data.metrics.http_req_duration?.values["p(95)"];
  const rps      = data.metrics.http_reqs?.values.rate;
  const failRate = data.metrics.http_req_failed?.values.rate;

  console.log(
    `[S4-T06][${PROFILE}] p95=${p95?.toFixed(2)}ms | ` +
    `rps=${rps?.toFixed(1)} | fail=${(failRate * 100).toFixed(3)}%`
  );

  return { stdout: JSON.stringify(data, null, 2) };
}
