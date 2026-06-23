# Sprint 3 — Fechamento do Gap V-03: Integridade de Manifestos CBOM

**Módulo**: 16 | **Sprint**: 3 | **Semanas**: 5–6

---

## Contexto

O cenário S4-E04 (Módulo 15) revelou que a adulteração de um manifesto CBOM
reduzia as ações recomendadas de 2 para 1 **sem qualquer bloqueio da automação**.
Esse gap (V-03) é crítico: um atacante que corrompa ou substitua um manifesto pode
fazer o gateway ignorar vulnerabilidades deliberadamente.

A correção implementada nesta sprint adiciona verificação obrigatória de HMAC-SHA256
sobre o payload canônico de cada manifesto antes de qualquer etapa de automação.

---

## Implementação

### Funções adicionadas em `code/cbom_gateway.py`

```python
def sign_manifest(manifest, key) -> dict:
    """Adiciona bloco _integrity com HMAC-SHA256 ao manifesto."""
    payload = _canonical_payload(manifest)   # JSON determinístico, sem _integrity
    sig = hmac.new(key.encode(), payload, hashlib.sha256).hexdigest()
    return {**manifest, "_integrity": {"algo": "hmac-sha256", "sig": sig}}

def verify_manifest(manifest, key) -> bool:
    """Retorna True se a assinatura do manifesto é válida para key."""
    block = manifest.get("_integrity", {})
    if not block:
        return False
    sig      = block.get("sig", "")
    payload  = _canonical_payload(manifest)
    expected = hmac.new(key.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)
```

### Novos flags CLI

```
--sign    Assina o manifesto e salva em --output (ou cbom-signed.json).
--verify  Verifica a assinatura antes de processar. Aborta com exit 1 se inválida.
--key     Chave HMAC. Usa CBOM_SIGNING_KEY como variável de ambiente.
```

---

## Como Gerar um Manifesto Assinado

```bash
# Definir chave segura
export CBOM_SIGNING_KEY="sua-chave-secreta-aqui"

# Assinar manifesto de referência
python3 code/cbom_gateway.py \
  --cbom code/samples/cbom-three-tier.json \
  --sign \
  --key "$CBOM_SIGNING_KEY" \
  --output code/samples/cbom-signed.json

# Verificar manifesto íntegro → deve imprimir OK e gerar 2 ações
python3 code/cbom_gateway.py \
  --cbom code/samples/cbom-signed.json \
  --verify \
  --key "$CBOM_SIGNING_KEY"
# Saída esperada: "OK: all manifests passed integrity verification."

# Verificar manifesto adulterado → deve abortar com exit 1
python3 code/cbom_gateway.py \
  --cbom code/samples/cbom-tampered.json \
  --verify \
  --key "$CBOM_SIGNING_KEY"
# Saída esperada:
# ERROR: manifest integrity check FAILED for ... — aborting automation (V-03 enforcement).
# exit code: 1
```

---

## Reexecução do Cenário S4-E04 com a Correção

```bash
# No servidor acadêmico (podman):

# 1. Assinar manifesto de referência no k8s-control
podman exec k8s-control sh -lc \
  "CBOM_SIGNING_KEY='minha-chave' \
   python /workspace/code/cbom_gateway.py \
   --cbom /workspace/code/samples/cbom-three-tier.json \
   --sign \
   --output /evidence/scenarios/S4-E04/cbom-signed.json"

# 2. Tentar processar manifesto adulterado → deve bloquear
podman exec k8s-control sh -lc \
  "CBOM_SIGNING_KEY='minha-chave' \
   python /workspace/code/cbom_gateway.py \
   --cbom /workspace/code/samples/cbom-tampered.json \
   --verify \
   2>&1 | tee /evidence/scenarios/S4-E04/tampered-rejection.log"
# Resultado esperado: exit code 1 + mensagem de erro

# 3. Verificar manifesto íntegro e processar normalmente → deve gerar 2 ações
podman exec k8s-control sh -lc \
  "CBOM_SIGNING_KEY='minha-chave' \
   python /workspace/code/cbom_gateway.py \
   --cbom /evidence/scenarios/S4-E04/cbom-signed.json \
   --verify \
   --output /evidence/scenarios/S4-E04/gateway-summary.json"
# Resultado esperado: 2 ações de migração (web + app)
```

---

## Critérios de Aceitação da Sprint 3

| Critério | Esperado | Validação |
|---|---|---|
| Manifesto íntegro | Processado normalmente, 2 ações geradas | exit code 0 |
| Manifesto adulterado | BLOQUEADO antes da automação | exit code 1 |
| Cobertura S4-E04 revisado | 100% de artefatos adulterados bloqueados | log de rejeição presente |
| Assinatura reprodutível | Mesma chave + mesmo payload = mesma assinatura | teste unitário |

---

## Amostras Criadas

| Arquivo | Descrição |
|---|---|
| `code/samples/cbom-signed.json` | Manifesto de referência com campo `_integrity` (placeholder — rodar `--sign` para gerar assinatura real) |
| `code/samples/cbom-tampered.json` | Manifesto com assinatura inválida e achado crítico removido (para S4-E04) |

---

## Checklist de Encerramento da Sprint 3

- [ ] `sign_manifest()` e `verify_manifest()` implementados e testados localmente.
- [ ] Flags `--sign`, `--verify`, `--key` funcionando na CLI.
- [ ] S4-E04 reexecutado no servidor: manifesto adulterado rejeitado com exit code 1.
- [ ] S4-E04 confirmado: manifesto íntegro gera 2 ações (sem regressão).
- [ ] `tampered-rejection.log` copiado para `docs/module16/evidence/S4-E04/`.
