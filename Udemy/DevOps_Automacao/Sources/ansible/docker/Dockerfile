FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    openssh-server \
    sudo \
    python3 \
    python3-pip \
    curl \
    vim \
    && mkdir /var/run/sshd

# Criar usuário padrão
RUN useradd -m -s /bin/bash devops && \
    echo "devops:Devops123!" | chpasswd && \
    usermod -aG sudo devops

# Permitir sudo sem senha (lab only)
RUN echo "devops ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configuração SSH
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]



