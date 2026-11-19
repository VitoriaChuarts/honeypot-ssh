from siem_client import enviar_alerta
import socket
import threading
import paramiko
from datetime import datetime

CHAVE_SERVIDOR = paramiko.RSAKey(filename="chave_servidor")

class ServidorFalso(paramiko.ServerInterface):
    def __init__(self, ip_atacante):
        self.ip_atacante = ip_atacante
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        return "password"

    def check_auth_password(self, username, password):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha_log = f"{agora} | IP: {self.ip_atacante} | usuario: {username} | senha: {password}\n"
        with open("honeypot.log", "a") as log:
            log.write(linha_log)
        print(f"Capturado -> usuario: {username} | senha: {password}")
        enviar_alerta(self.ip_atacante, username, password)
        return paramiko.AUTH_FAILED


def tratar_conexao(cliente_socket, ip_atacante):
    try:
        transporte = paramiko.Transport(cliente_socket)
        transporte.add_server_key(CHAVE_SERVIDOR)
        servidor = ServidorFalso(ip_atacante)
        transporte.start_server(server=servidor)
        canal = transporte.accept(20)
        if canal is not None:
            canal.close()
    except Exception as erro:
        print(f"Erro na conexao: {erro}")


servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor_socket.bind(("0.0.0.0", 2222))
servidor_socket.listen(100)

print("Honeypot SSH (Paramiko) escutando na porta 2222...")

while True:
    cliente_socket, endereco = servidor_socket.accept()
    ip_atacante = endereco[0]
    print(f"Conexao recebida de {ip_atacante}")
    thread = threading.Thread(target=tratar_conexao, args=(cliente_socket, ip_atacante))
    thread.start()
