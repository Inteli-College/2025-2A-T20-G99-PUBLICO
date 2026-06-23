#!/usr/bin/env python3
"""
cbomkit_cli.py — Scanner simplificado inspirado no IBM CBOM Kit.

Objetivo: permitir que gere manifestos CBOM a partir do código-fonte
em um ambiente desconectado, mantendo compatibilidade com o protótipo
`cbom_gateway.py`.

Uso básico:

    python code/cbomkit_cli.py \
        --target web-portal:web:src/frontend \
        --target api-orders:app:src/backend \
        --target ledger-db:data:infra/db \
        --output cbom-manifest.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".c",
    ".cpp",
    ".cs",
    ".kt",
    ".rb",
    ".php",
    ".rs",
    ".swift",
    ".json",
    ".yaml",
    ".yml",
    ".tf",
    ".tfvars",
    ".ini",
    ".cfg",
    ".properties",
    ".sh",
    ".bash",
    ".ps1",
}

ALGORITHMS: Dict[str, Sequence[str]] = {
    "RSA": [r"RSA[-_ ]?(?:1024|2048|3072|4096)?"],
    "ECDSA": [r"ECDSA[-_ ]?(?:P[0-9]+)?"],
    "ECDH": [r"ECDH[-_ ]?(?:P[0-9]+)?"],
    "AES": [r"AES[-_ ]?(?:128|192|256)?"],
    "ChaCha20": [r"ChaCha20"],
    "DES": [r"\bDES(?:-EDE3)?\b"],
    "3DES": [r"3DES"],
    "MD5": [r"MD5"],
    "SHA-1": [r"SHA[-_ ]?1"],
    "SHA-256": [r"SHA[-_ ]?256"],
    "SHA-512": [r"SHA[-_ ]?512"],
    "Kyber": [r"Kyber[-_ ]?(?:512|768|1024)?"],
    "Dilithium": [r"Dilithium[-_ ]?(?:2|3|5)?"],
    "Falcon": [r"Falcon[-_ ]?(?:512|1024)?"],
}


@dataclass
class Finding:
    algorithm: str
    category: str
    line: int
    context: str


def detect_algorithms(text: str) -> List[Finding]:
    findings: List[Finding] = []
    lines = text.splitlines()
    for name, patterns in ALGORITHMS.items():
        category = classify_algorithm(name)
        for pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            for match in regex.finditer(text):
                char_index = match.start()
                line_number = text.count("\n", 0, char_index) + 1
                context = lines[line_number - 1].strip() if 0 < line_number <= len(lines) else ""
                findings.append(Finding(name, category, line_number, context))
    return findings


def classify_algorithm(name: str) -> str:
    upper = name.upper()
    if any(key in upper for key in ("RSA", "ECDSA", "ECDH", "DILITHIUM", "FALCON")):
        return "asymmetric"
    if any(key in upper for key in ("AES", "DES", "3DES", "CHACHA20")):
        return "symmetric"
    if "SHA" in upper or "MD5" in upper:
        return "hash"
    return "other"


def iter_files(root: Path, extensions: Iterable[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


def scan_component(component: str, tier: str, root: Path) -> Dict:
    files_data: List[Dict] = []
    summary = Counter()

    for file_path in iter_files(root, EXTENSIONS):
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        findings = detect_algorithms(text)
        if not findings:
            continue
        rel_path = file_path.relative_to(root)
        file_entry = {
            "path": str(rel_path),
            "absolute_path": str(file_path.resolve()),
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc).isoformat(),
            "algorithms": [
                {
                    "name": f.algorithm,
                    "category": f.category,
                    "line": f.line,
                    "context": f.context,
                }
                for f in findings
            ],
        }
        files_data.append(file_entry)
        summary.update(f.algorithm for f in findings)

    return {
        "component": component,
        "tier": tier,
        "root": str(root),
        "files": files_data,
        "summary": dict(summary),
        "finding_count": sum(summary.values()),
    }


def render_manifest(components: List[Dict]) -> Dict:
    totals = defaultdict(int)
    for comp in components:
        totals["components_scanned"] += 1
        totals["files_with_findings"] += len(comp["files"])
        totals["total_findings"] += comp["finding_count"]
    return {
        "schema": "cbomkit-cli/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "totals": totals,
        "components": components,
    }


def parse_target(raw: str) -> (str, str, Path):
    parts = raw.split(":")
    if len(parts) < 3:
        raise argparse.ArgumentTypeError(
            f"Target '{raw}' inválido. Use o formato component:tier:/caminho/para/raiz"
        )
    component = parts[0].strip()
    tier = parts[1].strip()
    path = ":".join(parts[2:]).strip()
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise argparse.ArgumentTypeError(f"Caminho não encontrado para target '{raw}': {root}")
    return component, tier, root


def main() -> int:
    parser = argparse.ArgumentParser(description="Scanner simplificado do CBOM Kit.")
    parser.add_argument(
        "--target",
        action="append",
        required=True,
        help="Formato: component:tier:/caminho (pode repetir). Ex.: web-portal:web:src/frontend",
    )
    parser.add_argument(
        "--output",
        default=Path("cbom-manifest.json"),
        type=Path,
        help="Arquivo de saída (JSON).",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Identação JSON (padrão 2). Use 0 para compacto.",
    )
    args = parser.parse_args()

    components: List[Dict] = []
    for raw_target in args.target:
        component, tier, root = parse_target(raw_target)
        comp_data = scan_component(component, tier, root)
        components.append(comp_data)

    manifest = render_manifest(components)
    indent = None if args.indent <= 0 else args.indent
    args.output.write_text(json.dumps(manifest, indent=indent), encoding="utf-8")
    print(f"Manifesto salvo em {args.output}")
    print(
        f"Resumo: {manifest['totals']['components_scanned']} componentes, "
        f"{manifest['totals']['files_with_findings']} arquivos com achados, "
        f"{manifest['totals']['total_findings']} ocorrências."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
