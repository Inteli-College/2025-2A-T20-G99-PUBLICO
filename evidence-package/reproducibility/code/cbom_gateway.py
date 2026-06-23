#!/usr/bin/env python3
"""
CBOM → Three-Tier Crypto-Agility Gateway (Sprint 2 prototype).

This helper ingests IBM CBOM Kit manifests (JSON) and produces
an actionable view for the tree-tier reference architecture:
  - inventory coverage by tier (web/app/data)
  - high-risk classical algorithms that require PQC/hybrid swaps
  - recommended target profiles (Kyber/Dilithium, etc.)
  - readiness metrics aligned to Module 14 sprint goals

Module 16 additions (closes V-03 / S4-E04 gap):
  - --sign   : add HMAC-SHA256 integrity signature to a manifest
  - --verify : reject tampered manifests before any automation step
  - --key    : HMAC key (env CBOM_SIGNING_KEY takes precedence)

Usage:
    python code/cbom_gateway.py --cbom code/samples/cbom-three-tier.json
    python code/cbom_gateway.py --cbom /path/to/*.json --output summary.json
    python code/cbom_gateway.py --cbom manifest.json --sign --key mysecret
    python code/cbom_gateway.py --cbom manifest.json --verify --key mysecret
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

AlgoMap = Dict[str, Dict[str, str]]

ALGO_MAPPINGS: AlgoMap = {
    "RSA-2048": {
        "target": "TLS 1.3 híbrido (Kyber-768 + RSA-3072)",
        "action": "Atualizar terminação web e CDN para perfil híbrido",
    },
    "RSA-3072": {
        "target": "Assinatura híbrida (Dilithium-3 + RSA-3072)",
        "action": "Rotacionar certificados internos e playbooks de backup",
    },
    "ECDSA-P256": {
        "target": "Dilithium-2 para tokens/JWT e assinatura de artefatos",
        "action": "Atualizar pipelines de build e provedores de identidade",
    },
    "ECDH-P256": {
        "target": "mTLS híbrido (Kyber-768 + ECDH) ou KEM TLS 1.3",
        "action": "Atualizar sidecars/service mesh e automatizar validação",
    },
}

TIER_NORMALIZATION = {
    "presentation": "web",
    "web": "web",
    "frontend": "web",
    "application": "app",
    "app": "app",
    "business": "app",
    "data": "data",
    "database": "data",
}

_INTEGRITY_FIELD = "_integrity"


# ---------------------------------------------------------------------------
# CBOM integrity helpers (Module 16 — closes V-03)
# ---------------------------------------------------------------------------

def _canonical_payload(manifest: Any) -> bytes:
    """Produce a deterministic JSON bytes representation (no _integrity field)."""
    if isinstance(manifest, list):
        clean = [
            {k: v for k, v in item.items() if k != _INTEGRITY_FIELD}
            if isinstance(item, dict) else item
            for item in manifest
        ]
    elif isinstance(manifest, dict):
        clean = {k: v for k, v in manifest.items() if k != _INTEGRITY_FIELD}
    else:
        clean = manifest
    return json.dumps(clean, sort_keys=True, ensure_ascii=False).encode("utf-8")


def sign_manifest(manifest: Any, key: str) -> Any:
    """Return a copy of *manifest* with an HMAC-SHA256 _integrity block added."""
    if isinstance(manifest, list):
        return [sign_manifest(item, key) if isinstance(item, dict) else item for item in manifest]
    if isinstance(manifest, dict):
        payload = _canonical_payload(manifest)
        sig = hmac.new(key.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        integrity_block = {"algo": "hmac-sha256", "sig": sig}
        return {**manifest, _INTEGRITY_FIELD: integrity_block}
    return manifest


def verify_manifest(manifest: Any, key: str) -> bool:
    """Return True if the manifest's HMAC matches *key*; False otherwise."""
    if isinstance(manifest, list):
        for item in manifest:
            if not isinstance(item, dict):
                continue
            block = item.get(_INTEGRITY_FIELD, {})
            if not block:
                return False
            sig = block.get("sig", "")
            payload = _canonical_payload(item)
            expected = hmac.new(key.encode("utf-8"), payload, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(sig, expected):
                return False
        return True
    if isinstance(manifest, dict):
        block = manifest.get(_INTEGRITY_FIELD, {})
        if not block:
            return False
        sig = block.get("sig", "")
        payload = _canonical_payload(manifest)
        expected = hmac.new(key.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected)
    return False


# ---------------------------------------------------------------------------
# Core gateway logic (unchanged from Sprint 2)
# ---------------------------------------------------------------------------

def load_cbom(payloads: List[Path]) -> List[Dict[str, Any]]:
    components: List[Dict[str, Any]] = []
    for path in payloads:
        with path.open("r", encoding="utf-8") as handler:
            data = json.load(handler)
        if isinstance(data, dict):
            components.append(data)
        elif isinstance(data, list):
            components.extend(data)
        else:
            raise ValueError(f"Formato CBOM inválido em {path}")
    return components


def normalize_tier(value: str) -> str:
    return TIER_NORMALIZATION.get(value.lower(), value.lower())


def build_actions(components: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    actions: List[Dict[str, Any]] = []
    for component in components:
        tier = normalize_tier(component.get("tier", "desconhecido"))
        for finding in component.get("crypto", []):
            algo = finding.get("algo")
            mapping = ALGO_MAPPINGS.get(algo)
            if not mapping:
                continue
            if finding.get("risk", "").lower() not in {"high", "alto"} and not finding.get(
                "policy_violation", False
            ):
                # Already compliant or low priority.
                continue
            actions.append(
                {
                    "component": component.get("component"),
                    "tier": tier,
                    "mode": finding.get("mode"),
                    "usage": finding.get("usage"),
                    "current_algo": algo,
                    "target_profile": mapping["target"],
                    "next_step": mapping["action"],
                }
            )
    return actions


def compute_metrics(components: Iterable[Dict[str, Any]], actions: List[Dict[str, Any]]) -> Dict[str, Any]:
    tiers = Counter()
    violations = 0
    high_risk = 0
    crypto_entries = 0

    for component in components:
        tier = normalize_tier(component.get("tier", "desconhecido"))
        tiers[tier] += 1
        for finding in component.get("crypto", []):
            crypto_entries += 1
            risk = finding.get("risk", "").lower()
            if finding.get("policy_violation"):
                violations += 1
            if risk in {"high", "alto"}:
                high_risk += 1

    coverage = {
        "web": tiers["web"],
        "app": tiers["app"],
        "data": tiers["data"],
    }
    readiness = max(0, 1 - (high_risk / crypto_entries if crypto_entries else 0))

    return {
        "components_total": sum(tiers.values()),
        "coverage_by_tier": coverage,
        "high_risk_findings": high_risk,
        "policy_violations": violations,
        "actions_required": len(actions),
        "pqc_readiness_index": round(readiness, 2),
    }


def render_report(metrics: Dict[str, Any], actions: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("=== CBOM Gateway — Module 16 Report ===")
    lines.append(
        f"Inventário: {metrics['components_total']} componentes | "
        f"Web/App/Data = {metrics['coverage_by_tier']['web']}/"
        f"{metrics['coverage_by_tier']['app']}/{metrics['coverage_by_tier']['data']}"
    )
    lines.append(
        f"Riscos altos: {metrics['high_risk_findings']} | Violações de política: {metrics['policy_violations']}"
    )
    lines.append(
        f"Ações de migração PQC/híbrida necessárias: {metrics['actions_required']} | "
        f"Índice de prontidão PQC: {metrics['pqc_readiness_index']}"
    )
    lines.append("")
    lines.append("Top ações por camada three-tier:")
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for action in actions:
        grouped[action["tier"]].append(action)
    for tier in ("web", "app", "data"):
        tier_actions = grouped.get(tier, [])
        if not tier_actions:
            lines.append(f"- {tier.upper()}: sem pendências críticas.")
            continue
        lines.append(f"- {tier.upper()}:")
        for action in tier_actions:
            lines.append(
                f"    • {action['component']} → {action['mode']} ({action['current_algo']}) "
                f"⇒ {action['target_profile']} | Próximo passo: {action['next_step']}"
            )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CBOM Gateway three-tier analyzer.")
    parser.add_argument(
        "--cbom",
        nargs="+",
        default=[Path("code/samples/cbom-three-tier.json")],
        type=Path,
        help="Arquivos CBOM exportados pelo IBM CBOM Kit (JSON).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Caminho opcional para salvar o resumo (JSON).",
    )
    parser.add_argument(
        "--sign",
        action="store_true",
        help="Adiciona assinatura HMAC-SHA256 ao manifesto e salva em --output.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verifica integridade HMAC antes de processar. Aborta com exit 1 se inválido.",
    )
    parser.add_argument(
        "--key",
        default=os.environ.get("CBOM_SIGNING_KEY", ""),
        help="Chave HMAC (ou use a variável de ambiente CBOM_SIGNING_KEY).",
    )
    args = parser.parse_args(argv)

    # Load raw JSON (list or dict) for signing/verification
    raw_data: List[Any] = []
    for path in args.cbom:
        with path.open("r", encoding="utf-8") as fh:
            raw_data.append(json.load(fh))

    # --sign mode: write signed manifest and exit
    if args.sign:
        if not args.key:
            print("ERROR: --sign requires --key or CBOM_SIGNING_KEY env var.", file=sys.stderr)
            return 2
        signed = [sign_manifest(m, args.key) for m in raw_data]
        out_path = args.output or Path("cbom-signed.json")
        out_path.write_text(
            json.dumps(signed if len(signed) > 1 else signed[0], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Manifesto assinado salvo em {out_path}")
        return 0

    # --verify mode: abort if any manifest is tampered
    if args.verify:
        if not args.key:
            print("ERROR: --verify requires --key or CBOM_SIGNING_KEY env var.", file=sys.stderr)
            return 2
        for i, manifest in enumerate(raw_data):
            if not verify_manifest(manifest, args.key):
                print(
                    f"ERROR: manifest integrity check FAILED for {args.cbom[i]} — "
                    "aborting automation (V-03 enforcement).",
                    file=sys.stderr,
                )
                return 1
        print("OK: all manifests passed integrity verification.")

    # Normal analysis flow
    components = load_cbom(args.cbom)
    actions = build_actions(components)
    metrics = compute_metrics(components, actions)

    report = render_report(metrics, actions)
    print(report)

    if args.output:
        payload = {"metrics": metrics, "actions": actions}
        args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nResumo salvo em {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
