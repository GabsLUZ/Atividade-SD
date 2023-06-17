import socket

def enviar_respostas(host, port, arquivo_respostas):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Conectado ao servidor.")

    with open(arquivo_respostas, 'r') as file:
        for line in file:
            sock.send(line.encode())
            resposta_servidor = sock.recv(1024).decode()
            print("Resposta do servidor:", resposta_servidor)

    sock.close()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8888
    arquivo_respostas = "respostas.txt"
    enviar_respostas(host, port, arquivo_respostas)
