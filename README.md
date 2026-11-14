# Honeypot SSH em Python

Honeypot SSH construído do zero em Python, sem usar ferramentas prontas, simulando um servidor SSH vulnerável para capturar tentativas de ataque de força bruta.

## Como funciona

1. Um servidor Python escuta na porta 2222, implementando o protocolo SSH real com a biblioteca Paramiko
2. Quando um atacante (ou ferramenta como Hydra) tenta se conectar, o honeypot completa a negociação SSH normalmente
3. Toda tentativa de usuário/senha é capturada e registrada em um log, mas o acesso nunca é concedido
4. Um script separado (relatorio.py) analisa o log capturado e gera um resumo: senhas mais tentadas, usuários mais tentados e IPs mais ativos

## Tecnologias usadas

- Python 3 (socket, threading)
- Paramiko (protocolo SSH)
- Hydra (testado contra o próprio honeypot)

## Como executar

1. Gere uma chave de servidor: `ssh-keygen -t rsa -b 2048 -f chave_servidor -N ""`
2. Instale as dependências: `pip install paramiko`
3. Rode o honeypot: `python3 honeypot.py`
4. Gere o relatório depois de capturar tentativas: `python3 relatorio.py`

## Autora

Vitória Chuarts
