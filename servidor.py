import socket
import threading
import logging
import datetime

#configuracao do log
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
    """Gerencia a comunicação com o cliente."""
    log_event(f'Conexão estabelecida com {addr}')
    print(f'Conexão estabelecida com {addr}')
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                log_event(f'Conexão encerrada pelo cliente {addr}')
                print(f'Conexão encerrada pelo cliente {addr}')
                break
            
            mensagem_cliente = data.decode()
            log_event(f'Cliente {addr}: {mensagem_cliente}')
            print(f'Cliente {addr}: {mensagem_cliente}')
            
            if mensagem_cliente.upper() == "EXIT":
                conn.sendall("EXIT: Encerrando conexão.".encode())
                break
            
            resposta = process_command(mensagem_cliente.upper())
            conn.sendall(resposta.encode())
    except ConnectionResetError:
        log_event(f'Conexão com {addr} foi encerrada abruptamente.')
        print(f'Conexão com {addr} foi encerrada abruptamente.')
    finally:
        conn.close()
        log_event(f'Conexão fechada com {addr}')
        print(f'Conexão fechada com {addr}')

#configuracao do servidor
HOST = ''  
PORT = 5000  

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print(f'Servidor escutando na porta {PORT}...')

try:
    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'Clientes ativos: {threading.active_count() - 1}')
except KeyboardInterrupt:
    print("\nServidor encerrado.")
finally:
    servidor.close()
