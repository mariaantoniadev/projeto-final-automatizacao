import socket
import threading
import logging
import datetime

#configuracao do logging
logging.basicConfig(filename='server_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def log_event(message):
    logging.info(message)

def process_command(command):
    """Processa os comandos enviados pelo cliente."""
    if command == "ECHO":
        return "ECHO: Comando recebido com sucesso."
    elif command == "TIME":
        return f"TIME: {datetime.datetime.now()}"
    elif command == "EXIT":
        return "EXIT: Encerrando conexão."
    else:
        return "ERROR: Comando não reconhecido."

def handle_client(conn, addr):
    print(f'Conexão estabelecida com {addr}')
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f'Conexão encerrada pelo cliente {addr}')
                break
            mensagem_cliente = data.decode()
            print(f'Cliente {addr}: {mensagem_cliente}')
            mensagem_servidor = input('Você (servidor): ')
            conn.sendall(mensagem_servidor.encode())
    except ConnectionResetError:
        print(f'Conexão com {addr} foi encerrada abruptamente.')
    finally:
        conn.close()
        print(f'Conexão fechada com {addr}')

HOST = ''  # Escuta em todas as interfaces de rede disponíveis
PORT = 5000  # Porta para escutar as conexões

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print(f'Servidor escutando na porta {PORT}...')

while True:
    conn, addr = servidor.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f'Clientes ativos: {threading.active_count() - 1}')   
