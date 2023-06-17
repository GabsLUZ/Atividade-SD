import socket

def enviar_respostas(host, port, respostas):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for resposta in respostas:
        sock.sendto(resposta.encode(), (host, port))
        data, _ = sock.recvfrom(1024)
        resposta_servidor = data.decode()
        print("Resposta do servidor:", resposta_servidor)

    sock.close()


# Configurações do cliente
host = 'localhost'
port = 5000

# Dados do questionário
respostas = [
    "1;5;VVFFV",
    "2;4;VVVV"
]

# Envia as respostas para o servidor
enviar_respostas(host, port, respostas)
