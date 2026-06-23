# Requisitos de Ambiente para Simulação da Pesquisa em Supercomputador

## Objetivo

Este documento consolida, em formato de pedido de infraestrutura, o que a pesquisa precisa para simular o ambiente híbrido three-tier descrito no repositório e executar os experimentos propostos no artigo.

O ambiente pedido abaixo foi dimensionado para:

- simular a arquitetura em cinco camadas usada no artigo: `web`, `aplicação`, `dados`, `controle` e `integração`;
- executar o experimento com `10.000 transações sintéticas`;
- comparar perfis `clássico`, `híbrido` e, quando possível, `PQC`;
- coletar telemetria, validar canário, testar rollback e armazenar evidências CBOM.

Importante:

- o repositório define claramente a topologia e as métricas, mas não fixa `vCPU`, `RAM` e `disco`;
- por isso, os números abaixo são uma inferência técnica para um ambiente acadêmico estável, não um valor literal já escrito no artigo.


## Configuração 

Ambiente tipo `IaaS` ou `cloud-like`, com `8 instâncias/VMs`, persistentes, CPU-only, Linux `x86_64`, com acesso administrativo para instalação dos serviços da pesquisa.

| Instância | Qtd. | vCPU | RAM | Disco SSD | Função principal |
| --- | --- | --- | --- | --- | --- |
| `k8s-control` | 1 | 4 | 8 GB | 100 GB | Nó de controle do cluster Kubernetes |
| `k8s-worker` | 3 | 8 cada | 16 GB cada | 150 GB cada | Execução das camadas web, aplicação, gateway e canário |
| `data-node` | 1 | 8 | 16 GB | 400 GB | Banco relacional, object storage e evidências |
| `security-integration-node` | 1 | 4 | 8 GB | 120 GB | Vault/KMS equivalente, barramento de eventos e automação |
| `observability-node` | 1 | 8 | 32 GB | 400 GB | Prometheus, Grafana, logs, traces e SIEM equivalente |
| `load-chaos-node` | 1 | 4 | 8 GB | 80 GB | k6/Locust e testes de falha/caos |

Totais da configuração:

- `8 instâncias`
- `52 vCPU`
- `120 GB RAM`
- `1,55 TB` de armazenamento SSD


### `k8s-control`

Nó que controla o cluster Kubernetes. Ele não precisa ser grande, mas é obrigatório se o ambiente for entregue como VMs e o cluster for montado pela pesquisa. Serve para orquestrar namespaces como `dev`, `staging/canary` e `prod-sim`.

### `k8s-worker` (3 instâncias)

São os nós onde rodam os containers da aplicação simulada. Aqui ficam:

- frontend bancário;
- APIs e microsserviços de negócio;
- gateway de criptoagilidade;
- sidecars de service mesh;
- versões baseline e canário para os testes de migração.

Três workers são o mínimo recomendável para não misturar tudo em um único host e para permitir medições mais limpas de latência, mTLS e rollback.

### `data-node`

Instância da camada de dados. Deve hospedar:

- banco relacional da simulação;
- storage das evidências CBOM, relatórios e logs;
- volumes persistentes para backups e dados experimentais.

O disco desta VM precisa ser SSD porque o experimento depende de escrita frequente de logs, traces, artefatos e dados de teste.

### `security-integration-node`

É a instância de apoio ao plano de controle e à camada de integração. Ela deve suportar:

- `Vault` ou equivalente para simular `KMS/Secrets Manager`;
- emissão/rotação de segredos e certificados;
- `NATS` ou `Kafka` para eventos;
- runner ou serviços de automação/GitOps, se necessário.

Ela existe porque a pesquisa não mede apenas aplicação; ela mede também a propagação controlada das mudanças criptográficas.

### `observability-node`

É a instância dedicada à observabilidade. Deve suportar:

- `Prometheus`;
- `Grafana`;
- coleta de logs;
- traces OpenTelemetry;
- SIEM equivalente, se houver.

Essa VM precisa de mais memória porque concentra séries temporais, traces e logs dos testes de carga, canário e falha.

### `load-chaos-node`

É a instância separada para gerar carga e injetar falhas. Deve rodar:

- `k6` ou `Locust`;
- ferramentas de chaos testing;
- scripts de execução das `10.000 transações sintéticas`.

Ela precisa ser separada do cluster principal para não contaminar as métricas de CPU, memória e latência do sistema sob teste.

## Requisitos de Plataforma Que Devem Acompanhar as Instâncias

Além das VMs, importante:

- `Linux x86_64` nas instâncias, preferencialmente Ubuntu 22.04 LTS, Rocky Linux 9 ou equivalente;
- `acesso root` ou privilégio administrativo;
- `rede privada` entre as instâncias;
- `1 IP público` para bastion/ingress já é suficiente;
- `saída para internet` ou espelho interno de pacotes/imagens, para baixar containers e dependências;
- `armazenamento persistente em SSD`;
- `snapshot` ou backup das VMs e volumes;
- `sincronização de horário` entre os nós;
- possibilidade de instalar `Kubernetes`, `Helm`, `containerd/Docker`, `service mesh` e ferramentas de observabilidade.


## Configuração Mínima Se Houver Restrição de Recursos

Se a faculdade não puder disponibilizar a configuração recomendada, a menor configuração ainda aceitável é:

| Instância | Qtd. | vCPU | RAM | Disco SSD | Observação |
| --- | --- | --- | --- | --- | --- |
| `k8s-control` | 1 | 4 | 8 GB | 100 GB | obrigatório |
| `k8s-worker` | 2 | 8 cada | 16 GB cada | 150 GB cada | reduz isolamento |
| `data-security-node` | 1 | 8 | 16 GB | 350 GB | junta dados e Vault/KMS |
| `obs-integration-node` | 1 | 8 | 24 GB | 350 GB | junta observabilidade e eventos |
| `load-chaos-node` | 1 | 4 | 8 GB | 80 GB | obrigatório para carga separada |

Totais da configuração mínima:

- `6 instâncias`
- `40 vCPU`
- `88 GB RAM`
- `1,18 TB` de armazenamento SSD

Essa versão mínima executa a pesquisa, mas com menos isolamento entre camadas e menor margem para testes simultâneos.


