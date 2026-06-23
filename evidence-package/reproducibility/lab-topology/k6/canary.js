import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 2,
  duration: "20s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<150"],
  },
};

const baseUrl = __ENV.BASE_URL || "http://k8s-worker-3:8080";

export default function () {
  const response = http.get(`${baseUrl}/chain`, {
    tags: { scenario: "S4-T02", tier: "canary" },
  });

  check(response, {
    "status is 200": (r) => r.status === 200,
    "response is canary": (r) => {
      const body = r.json();
      return body && body.canary === "canary";
    },
  });

  sleep(1);
}
