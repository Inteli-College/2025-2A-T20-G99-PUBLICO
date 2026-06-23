# Code

Espaço para scripts auxiliares (ex.: varredura de repositório por segredos, coleta de métricas cripto, geradores de relatórios).

## Ferramentas incluídas

### `cbomkit_cli.py`
- Scanner inspirado no IBM CBOM Kit para ambientes desconectados.
- Percorre diretórios do componente, detecta menções a algoritmos (RSA, ECDSA, Kyber, etc.) e gera manifestos JSON compatíveis com o gateway.

Exemplo:

```bash
python code/cbomkit_cli.py \
  --target web-portal:web:code \
  --target api-orders:app:docs \
  --output cbom-manifest.json
```

### `cbom_gateway.py`
- Protótipo da sprint 2 para o gateway de criptoagilidade.
- Consome manifestos JSON exportados pelo IBM CBOM Kit e gera um plano de ação para a arquitetura three-tier (web/app/data).
- Relata cobertura de inventário, violações de política e recomendações PQC/híbridas (Kyber/Dilithium).

Uso básico:

```bash
python code/cbom_gateway.py --cbom code/samples/cbom-three-tier.json --output /tmp/cbom-summary.json
```

### `samples/`
- `cbom-three-tier.json`: manifesto manual usado pelo gateway.
- `cbom-manifest-scan.json`: resultado gerado pelo `cbomkit_cli.py` ao escanear este repositório (exemplo de uso offline).
