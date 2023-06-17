import threading
import socket

class Estatisticas:
    def __init__(self):
        self.questoes = {}

    def atualizar_estatisticas(self, num_questao, acertos, erros):
        self.questoes[num_questao] = {'acertos': acertos, 'erros': erros}

    def obter_estatisticas(self):
        return self.questoes

def tratar_conexao(conn, addr, estatisticas):
    print("Cliente conectado:", addr)
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        num_questao, _, respostas = data.split(";")
        acertos, erros = calcular_acertos_erros(respostas)
        estatisticas.atualizar_estatisticas(num_questao, acertos, erros)

        resposta = f"Questão: {num_questao}; Acertos: {acertos}; Erros: {erros}"
        conn.send(resposta.encode())

    print("Cliente desconectado:", addr)
    conn.close()

def calcular_acertos_erros(respostas):
    acertos = respostas.count('V')
    erros = respostas.count('F')
    return acertos, erros

def iniciar_servidor(host, port):
    estatisticas = Estatisticas()
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))
    servidor.listen(5)
    print("Servidor iniciado. Aguardando conexões...")

    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=tratar_conexao, args=(conn, addr, estatisticas))
        thread.start()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8888
    iniciar_servidor(host, port)
