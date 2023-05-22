import socket
import threading
import datetime

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conexoes = []

def enviar_mensagem_todos(mensagem):
    for conexao in conexoes:
        conexao['conn'].send(mensagem.encode(FORMATO))

def handle_cliente(conn, addr):
    print(f"[NOVA CONEXÃO] Um novo usuário se conectou pelo endereço {addr} às {datetime.datetime.now()}")
    nome = conn.recv(1024).decode(FORMATO)
    print(f"[CONEXÃO ESTABELECIDA] Usuário {nome} conectado às {datetime.datetime.now()}")
    mensagem = f"[CONEXÃO ESTABELECIDA] Bem-vindo, {nome}!"
    conn.send(mensagem.encode(FORMATO))
    conexoes.append({'conn': conn, 'addr': addr, 'nome': nome})
    
    while True:
        try:
            msg = conn.recv(1024).decode(FORMATO)
            if msg == 'sair':
                print(f"[DESCONEXÃO] Usuário {nome} saiu às {datetime.datetime.now()}")
                enviar_mensagem_todos(f"[DESCONEXÃO] Usuário {nome} saiu.")
                conexoes.remove({'conn': conn, 'addr': addr, 'nome': nome})
                conn.close()
                break
            else:
                enviar_mensagem_todos(f"{nome}: {msg}")
        except ConnectionResetError:
            print(f"[DESCONEXÃO] Usuário {nome} desconectado inesperadamente às {datetime.datetime.now()}")
            enviar_mensagem_todos(f"[DESCONEXÃO] Usuário {nome} desconectado inesperadamente.")
            conexoes.remove({'conn': conn, 'addr': addr, 'nome': nome})
            conn.close()
            break

def iniciar_servidor():
    print("[INICIANDO] Iniciando servidor...")
    server.listen()
    print(f"[SERVIDOR ESCUTANDO] Servidor escutando no endereço {SERVER_IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_cliente, args=(conn, addr))
        thread.start()

iniciar_servidor()
