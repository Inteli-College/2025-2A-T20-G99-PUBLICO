# Pedido Minimo ao Administrador

Use este texto quando precisar liberar o laboratorio no servidor.

```text
Preciso executar um laboratorio academico que simula uma topologia de 8 nos logicos para testes de criptoagilidade.

O host ja possui recursos suficientes e suporte a virtualizacao, mas a minha conta nao consegue acessar o Docker daemon.

Peço uma destas opcoes, em ordem de preferencia:
1. adicionar o usuario `thomaz-barboza` ao grupo `docker`;
2. liberar `sudo` para uso de Docker;
3. se a exigencia for isolamento em VM real, instalar/liberar `virsh`, `virt-install`, `qemu-img` e `qemu-system-x86_64`.

Validacao esperada apos a liberacao:
- `docker ps`
- `docker info`

Objetivo do laboratorio:
- simular os nos `k8s-control`, `k8s-worker-1`, `k8s-worker-2`, `k8s-worker-3`, `data-node`, `security-integration-node`, `observability-node` e `load-chaos-node`;
- rodar cenarios de baseline, discover->decision->swap, canario inicial e integridade de CBOM;
- coletar evidencias tecnicas para a validacao arquitetural das Sprints 4 e 5.
```

## Confirmacao apos o admin atuar

Saia e entre novamente no servidor e rode:

```bash
id -nG
docker ps
docker info --format '{{.ServerVersion}}'
```
