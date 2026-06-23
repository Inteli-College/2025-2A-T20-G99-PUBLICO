import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 5,
  duration: "30s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<150"],
  },
};

const baseUrl = __ENV.BASE_URL || "http://k8s-worker-1:8080";

export default function () {
  const response = http.get(`${baseUrl}/chain`, {
    tags: { scenario: "S4-T01", tier: "web-app-data" },
  });

  check(response, {
    "status is 200": (r) => r.status === 200,
    "response has elapsed_ms": (r) => {
      const body = r.json();
      return body && body.elapsed_ms !== undefined;
    },
  });

  sleep(1);
}
