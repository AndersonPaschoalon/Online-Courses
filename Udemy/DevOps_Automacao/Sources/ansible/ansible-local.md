# Guia Conceitual + Tutorial 100% Local – Ansible Labs

> **Escopo explícito:**
> Este é um **tutorial de Ansible**, não de Azure, não de Terraform, não de cloud.
> A infraestrutura já existe localmente e é tratada como **caixa-preta**.

---

## Mental Model Geral do Lab

Antes do passo-a-passo, alinhe este modelo:

```
┌─────────────────────────────┐
│ Máquina local (host)        │
│                             │
│ ┌──────────────┐            │
│ │ controller   │  ansible   │
│ │ (VM/container├──────────► │
│ └──────────────┘            │
│                             │
│ ┌──────────────┐            │
│ │ target       │            │
│ │ (VM/container│            │
│ └──────────────┘            │
└─────────────────────────────┘
```

* **controller**: onde o Ansible roda
* **target**: máquina configurada pelo Ansible
* Comunicação: **SSH**
* O Ansible **não cria máquinas**, apenas **configura**

---

# Organização dos Labs Ansible – Estrutura Unificada (Local)

## Objetivo

Consolidar todos os labs de Ansible em uma estrutura única dentro de:

```bash
~/ansible-lab/
```

Usando:

* Um **inventário único**
* Playbooks organizados por função

---

## Estrutura de Diretório

```bash
~/ansible-lab/
├── hosts
├── playbooks/
│   ├── setup-basico.yaml
│   ├── docker-api.yaml
│   └── usuario-devops.yaml
```

---

# Lab Ansible 01 – Preparação do Ambiente Local

## Objetivo

Definir **duas máquinas locais já existentes** para o laboratório:

* `ansible-controller`
* `ansible-target`

> Essas máquinas podem ser:
>
> * VMs (VirtualBox, libvirt, WSL, Multipass)
> * Containers Docker com SSH
>
> **Para o Ansible, não importa.**

---

## Premissas (assumidas)

* Ambas as máquinas:

  * Rodam **Linux**
  * Possuem **SSH ativo**
  * Possuem **Python 3 instalado**
* A controller consegue acessar a target via SSH

---

## Convenção usada no lab

| Papel      | Hostname           | IP exemplo    |
| ---------- | ------------------ | ------------- |
| Controller | ansible-controller | 192.168.56.10 |
| Target     | ansible-target     | 192.168.56.11 |

> Ajuste IPs conforme seu ambiente local

---

# Lab Ansible 02 – Inventário e Teste de Conectividade

## Objetivo

* Criar inventário único
* Testar comunicação com o módulo `ping`

---

## 1. Criar estrutura base

```bash
mkdir -p ~/ansible-lab/playbooks
cd ~/ansible-lab
```

---

## 2. Criar o inventário

```bash
nano hosts
```

Conteúdo:

```ini
[targets]
target1 ansible_host=192.168.56.11 ansible_user=devops ansible_password=Devops123! ansible_python_interpreter=/usr/bin/python3
```

> ⚠️ **Uso de senha é apenas didático**
>
> Em ambientes reais, usa-se **SSH key + vault**

---

## 3. Desativar checagem de host key (temporário)

```bash
export ANSIBLE_HOST_KEY_CHECKING=False
```

---

## 4. Testar conectividade

```bash
ansible -i hosts targets -m ping
```

### Resultado esperado

```text
target1 | SUCCESS => {
  "ping": "pong"
}
```

---

# Lab Ansible 03 – Primeiro Playbook (Pacotes Básicos)

## Objetivo

Criar um playbook simples para:

* Atualizar cache APT
* Instalar utilitários comuns

---

## 1. Criar o playbook

```bash
cd ~/ansible-lab/playbooks
nano setup-basico.yaml
```

Conteúdo:

```yaml
---
- name: Configuração básica do sistema
  hosts: targets
  become: true

  tasks:
    - name: Atualizar cache de pacotes
      apt:
        update_cache: yes

    - name: Instalar pacotes básicos
      apt:
        name:
          - htop
          - curl
          - git
        state: present
```

---

## 2. Executar o playbook

```bash
cd ~/ansible-lab
ansible-playbook -i hosts playbooks/setup-basico.yaml
```

---

## 3. Validar idempotência

```bash
ansible-playbook -i hosts playbooks/setup-basico.yaml
```

### Resultado esperado

* Primeira execução: `changed`
* Segunda execução: `ok`

> Esse é o **conceito central do Ansible**

---

# Lab Ansible 04 – Docker + Aplicação Java

## Objetivo

* Instalar Docker
* Subir um container Java via Ansible

---

## 1. Criar playbook

```bash
cd ~/ansible-lab/playbooks
nano docker-api.yaml
```

Conteúdo:

```yaml
---
- name: Instalar Docker e rodar aplicação Java
  hosts: targets
  become: true

  tasks:
    - name: Atualizar pacotes
      apt:
        update_cache: yes

    - name: Instalar dependências
      apt:
        name:
          - ca-certificates
          - curl
          - gnupg
          - lsb-release
        state: present

    - name: Instalar Docker
      apt:
        name: docker.io
        state: present

    - name: Habilitar Docker
      systemd:
        name: docker
        enabled: yes
        state: started

    - name: Instalar SDK Docker para Python
      pip:
        name: docker

    - name: Rodar container Java
      docker_container:
        name: java-api
        image: iesodias/java-api:latest
        state: started
        restart_policy: always
        ports:
          - "8081:8081"
```

---

## 2. Executar

```bash
cd ~/ansible-lab
ansible-playbook -i hosts playbooks/docker-api.yaml
```

---

## 3. Validar

```bash
ansible -i hosts targets -m shell -a "docker ps"
```

---

# Lab Ansible 05 – Usuários, Permissões e Diretórios

## Objetivo

* Criar usuário `devops`
* Ajustar permissões
* Criar estrutura `/opt`

---

## 1. Criar playbook

```bash
cd ~/ansible-lab/playbooks
nano usuario-devops.yaml
```

Conteúdo:

```yaml
---
- name: Gerenciar usuários e diretórios
  hosts: targets
  become: true

  tasks:
    - name: Criar usuário devops
      user:
        name: devops
        password: "{{ 'Devops123!' | password_hash('sha512') }}"
        shell: /bin/bash
        groups: sudo,docker
        append: yes

    - name: Criar diretório /opt/app
      file:
        path: /opt/app
        state: directory
        owner: devops
        group: devops
        mode: '0755'

    - name: Criar diretório /opt/logs
      file:
        path: /opt/logs
        state: directory
        owner: devops
        group: devops
        mode: '0755'

    - name: Criar arquivo de status
      copy:
        content: "App iniciado em {{ ansible_date_time.iso8601 }}\n"
        dest: /opt/app/status.txt
        owner: devops
        group: devops
        mode: '0644'
```

---

## 2. Executar

```bash
cd ~/ansible-lab
ansible-playbook -i hosts playbooks/usuario-devops.yaml
```

---

## 3. Validar

```bash
ansible -i hosts targets -m shell -a "id devops"
ansible -i hosts targets -m shell -a "ls -l /opt"
```

---

# Lab Final – Destruir o Ambiente (Local)

## Objetivo

Reverter **estado**, não apagar máquinas.

> Em Ansible, destruição = **convergir para ausência**

---

## Exemplo conceitual

* Remover container
* Remover pacotes
* Remover usuários
* Remover diretórios

Isso seria feito com:

```yaml
state: absent
```

> Diferente de cloud, **Ansible não destrói infraestrutura**.

---

# Conclusão (Mental Model Final)

✔ Este tutorial é **100% Ansible**
✔ Totalmente reproduzível localmente
✔ Zero dependência de Azure
✔ Mesmo aprendizado conceitual
✔ Preparação correta para usar Ansible **com Azure depois**







