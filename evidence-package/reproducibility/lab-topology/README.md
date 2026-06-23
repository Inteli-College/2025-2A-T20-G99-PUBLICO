# Laboratório de Topologia Server-Only

Este diretório materializa uma simulação executável da topologia descrita em:

- `docs/governance/requisitos-ambiente.md`
- `docs/module14/sprint4/vm-network-topology.md`
- `docs/module14/sprint4/experiment-scenarios.md`

O objetivo aqui nao e reproduzir `8 VMs` reais, mas sim disponibilizar `8 nos logicos` em um unico host com isolamento por redes Docker, volumes persistentes e scripts operacionais.

## Nos logicos

- `k8s-control`
- `k8s-worker-1`
- `k8s-worker-2`
- `k8s-worker-3`
- `data-node`
- `security-integration-node`
- `observability-node`
- `load-chaos-node`

## O que esta implementado

- `docker-compose.yml` com redes separadas para ingresso, cluster, dados, seguranca e observabilidade.
- Servicos minimos para `web`, `app`, `controle` e `seguranca` usando uma imagem Python leve.
- `data-node` com `PostgreSQL`.
- `observability-node` com `Prometheus`.
- `load-chaos-node` com `k6`.
- Scripts para subir, parar, verificar o laboratorio, executar cenarios e empacotar evidencias.
- Integracao dos prototipos `code/cbom_gateway.py` e `code/cbomkit_cli.py` dentro do fluxo do laboratorio.

## Requisito externo

Para executar o laboratorio no servidor, a sua conta precisa conseguir usar Docker:

```bash
lab/topology/scripts/labctl.sh check
```

Se falhar com permissao negada, use o texto em `lab/topology/ACCESS_REQUEST.md`.

## Uso rapido

Do raiz do repositorio:

```bash
chmod +x lab/topology/scripts/labctl.sh
lab/topology/scripts/labctl.sh check
lab/topology/scripts/labctl.sh start
lab/topology/scripts/labctl.sh status
```

Executar cenarios prioritarios:

```bash
lab/topology/scripts/labctl.sh s4-t01
lab/topology/scripts/labctl.sh s4-t02
lab/topology/scripts/labctl.sh s4-t03
lab/topology/scripts/labctl.sh s4-t05
lab/topology/scripts/labctl.sh s4-e04
lab/topology/scripts/labctl.sh collect
```

Parar o laboratorio:

```bash
lab/topology/scripts/labctl.sh stop
```

## Implantacao no servidor academico

O procedimento completo de implantacao no servidor academico (SSH, Podman rootless, rsync, compatibilizacoes) esta documentado em:

- `docs/module14/setup-ambiente-8-nos.md`

## Estrutura de saida

Artefatos gerados em runtime ficam em:

- `lab/topology/runtime/evidence`
- `lab/topology/runtime/postgres`
- `lab/topology/runtime/prometheus`

O arquivo compactado final e criado em:

- `lab/topology/runtime/module14-evidence.tgz`
