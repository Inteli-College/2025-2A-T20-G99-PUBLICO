#!/usr/bin/env python3
import json
import os
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import psycopg


NODE_NAME = os.getenv("NODE_NAME", "node")
NODE_ROLE = os.getenv("NODE_ROLE", "generic")
NODE_PORT = int(os.getenv("NODE_PORT", "8080"))
NEXT_URL = os.getenv("NEXT_URL", "").strip()
SECURITY_URL = os.getenv("SECURITY_URL", "").strip()
DB_DSN = os.getenv("DB_DSN", "").strip()
EVIDENCE_DIR = os.getenv("EVIDENCE_DIR", "").strip()
CANARY_FLAG = os.getenv("CANARY_FLAG", "baseline").strip()

STATE = {"requests_total": 0, "chain_total": 0, "errors_total": 0, "last_chain_ms": 0.0}
LOCK = threading.Lock()


def bump(metric: str, amount: int = 1) -> None:
    with LOCK:
        STATE[metric] = STATE.get(metric, 0) + amount


def set_metric(metric: str, value: float) -> None:
    with LOCK:
        STATE[metric] = value


def log_evidence(payload: dict) -> None:
    if not EVIDENCE_DIR:
        return
    evidence_dir = Path(EVIDENCE_DIR)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    target = evidence_dir / "runtime-events.jsonl"
    with target.open("a", encoding="utf-8") as handler:
        handler.write(json.dumps(payload, ensure_ascii=True) + "\n")


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "module14-lab/1.0"})
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def run_db_probe() -> dict:
    if not DB_DSN:
        return {"enabled": False}

    result = {"enabled": True, "ok": False}
    with psycopg.connect(DB_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS runtime_events (
                    node_name TEXT NOT NULL,
                    canary_flag TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
                """
            )
            cur.execute(
                "INSERT INTO runtime_events (node_name, canary_flag) VALUES (%s, %s) RETURNING created_at",
                (NODE_NAME, CANARY_FLAG),
            )
            row = cur.fetchone()
            cur.execute("SELECT COUNT(*) FROM runtime_events")
            count = cur.fetchone()[0]
        conn.commit()
    result["ok"] = True
    result["created_at"] = row[0].isoformat()
    result["event_count"] = count
    return result


class Handler(BaseHTTPRequestHandler):
    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _text(self, payload: str, status: int = 200, content_type: str = "text/plain; version=0.0.4") -> None:
        body = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        return

    def do_GET(self) -> None:
        bump("requests_total")

        if self.path == "/health":
            self._json({"status": "ok", "node": NODE_NAME, "role": NODE_ROLE, "canary": CANARY_FLAG})
            return

        if self.path == "/info":
            self._json(
                {
                    "node": NODE_NAME,
                    "role": NODE_ROLE,
                    "canary": CANARY_FLAG,
                    "next_url": NEXT_URL or None,
                    "security_url": SECURITY_URL or None,
                    "db_enabled": bool(DB_DSN),
                }
            )
            return

        if self.path == "/secret":
            self._json(
                {
                    "node": NODE_NAME,
                    "role": NODE_ROLE,
                    "secret_profile": "mock-vault",
                    "rotation_policy_days": 90,
                    "token_ttl_minutes": 30,
                }
            )
            return

        if self.path == "/metrics":
            with LOCK:
                metrics = dict(STATE)
            lines = [
                "# HELP module14_requests_total Total requests served by the node",
                "# TYPE module14_requests_total counter",
                f'module14_requests_total{{node="{NODE_NAME}",role="{NODE_ROLE}"}} {metrics["requests_total"]}',
                "# HELP module14_chain_total Total chain executions",
                "# TYPE module14_chain_total counter",
                f'module14_chain_total{{node="{NODE_NAME}",role="{NODE_ROLE}"}} {metrics["chain_total"]}',
                "# HELP module14_errors_total Total chain errors",
                "# TYPE module14_errors_total counter",
                f'module14_errors_total{{node="{NODE_NAME}",role="{NODE_ROLE}"}} {metrics["errors_total"]}',
                "# HELP module14_last_chain_ms Last chain duration in milliseconds",
                "# TYPE module14_last_chain_ms gauge",
                f'module14_last_chain_ms{{node="{NODE_NAME}",role="{NODE_ROLE}"}} {metrics["last_chain_ms"]}',
            ]
            self._text("\n".join(lines) + "\n")
            return

        if self.path == "/chain":
            start = time.perf_counter()
            bump("chain_total")
            payload = {"node": NODE_NAME, "role": NODE_ROLE, "canary": CANARY_FLAG}
            status = 200

            try:
                if SECURITY_URL:
                    payload["security"] = fetch_json(SECURITY_URL)
                if DB_DSN:
                    payload["database"] = run_db_probe()
                if NEXT_URL:
                    payload["next"] = fetch_json(NEXT_URL)
            except (urllib.error.URLError, psycopg.Error, TimeoutError, ValueError) as exc:
                bump("errors_total")
                payload["error"] = str(exc)
                status = 500

            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            payload["elapsed_ms"] = elapsed_ms
            set_metric("last_chain_ms", elapsed_ms)
            log_evidence({"event": "chain", "status": status, "payload": payload, "ts": time.time()})
            self._json(payload, status=status)
            return

        self._json({"error": "not-found", "node": NODE_NAME}, status=404)


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", NODE_PORT), Handler)
    log_evidence({"event": "startup", "node": NODE_NAME, "role": NODE_ROLE, "ts": time.time()})
    server.serve_forever()


if __name__ == "__main__":
    main()
