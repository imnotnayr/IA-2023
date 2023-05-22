import socket
import threading

SERVER_IP = '192.168.1.113'  # IP do servidor
PORT = 5050
FORMATO = 'utf-8'

def receber_mensagens(conn):
    while True:
        mensagem = conn.recv(1024).decode(FORMATO)
        print(mensagem)

def enviar_mensagem(conn):
    while True:
        mensagem = input()
        conn.send(mensagem.encode(FORMATO))

def iniciar_cliente():
    nome = input("Digite seu nome: ")

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((SERVER_IP, PORT))
    cliente.send(nome.encode(FORMATO))

    mensagem_bem_vindo = cliente.recv(1024).decode(FORMATO)
    print(mensagem_bem_vindo)

    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.start()

    thread_enviar = threading.Thread(target=enviar_mensagem, args=(cliente,))
    thread_enviar.start()

iniciar_cliente()
