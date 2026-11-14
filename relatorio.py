from collections import Counter

senhas = []
usuarios = []
ips = []

with open("honeypot.log", "r") as arquivo:
    for linha in arquivo:
        partes = linha.strip().split(" | ")
        for parte in partes:
            if parte.startswith("IP: "):
                ips.append(parte.replace("IP: ", ""))
            elif parte.startswith("usuario: "):
                usuarios.append(parte.replace("usuario: ", ""))
            elif parte.startswith("senha: "):
                senhas.append(parte.replace("senha: ", ""))

print(f"Total de tentativas capturadas: {len(senhas)}")

print("\nTop 5 senhas mais tentadas:")
for senha, quantidade in Counter(senhas).most_common(5):
    print(f"  {senha} -> {quantidade} vezes")

print("\nTop 5 usuarios mais tentados:")
for usuario, quantidade in Counter(usuarios).most_common(5):
    print(f"  {usuario} -> {quantidade} vezes")

print("\nIPs que mais atacaram:")
for ip, quantidade in Counter(ips).most_common(5):
    print(f"  {ip} -> {quantidade} tentativas")
