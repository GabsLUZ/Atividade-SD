import socket
import threading

class Estatisticas:
    def __init__(self):
        self.resultados = {}  # Dicionário para armazenar as estatísticas
        self.lock = threading.Lock()  # Lock para garantir exclusão mútua

    def atualizar_estatisticas(self, questao, acertos, erros):
        with self.lock:
            if questao in self.resultados:
                self.resultados[questao][0] += acertos
                self.resultados[questao][1] += erros
            else:
                self.resultados[questao] = [acertos, erros]

    def obter_estatisticas(self):
        with self.lock:
            return self.resultados


class ServidorUDP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.estatisticas = Estatisticas()  # Instância da classe Estatisticas para armazenar as estatísticas
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Criação do socket UDP
        self.sock.bind((self.host, self.port))  # Vincula o socket ao endereço do host e porta

    def iniciar(self):
        print(f"Servidor iniciado em {self.host}:{self.port}")

        while True:
            data, addr = self.sock.recvfrom(1024)  # Recebe dados do cliente
            thread = threading.Thread(target=self.processar_conexao, args=(data, addr))  # Cria uma nova thread para processar a conexão
            thread.start()  # Inicia a thread

    def processar_conexao(self, data, addr):
        mensagem = data.decode()  # Decodifica a mensagem recebida
        partes = mensagem.split(';')  # Divide a mensagem em partes
        questao = partes[0]  # Obtém o número da questão
        num_alternativas = int(partes[1])  # Obtém o número de alternativas
        respostas = partes[2]  # Obtém as respostas

        num_acertos = respostas.count('V')  # Conta o número de acertos
        num_erros = num_alternativas - num_acertos  # Calcula o número de erros

        self.estatisticas.atualizar_estatisticas(questao, num_acertos, num_erros)  # Atualiza as estatísticas

        resposta = f"Questão: {questao}; Acertos: {num_acertos}; Erros: {num_erros}".encode()  # Prepara a resposta
        self.sock.sendto(resposta, addr)  # Envia a resposta de volta para o cliente


# Configurações do servidor
host = 'localhost'
port = 5000

# Inicia o servidor
servidor = ServidorUDP(host, port)
servidor.iniciar()
