import socket
import threading
import logging
import datetime
from queue import Queue

#configuração do log
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

def handle_client(conn, addr, client_id):
    """Gerencia a comunicação com o cliente."""
    log_event(f'Conexão estabelecida com {addr} (Cliente {client_id})')
    print(f'Conexão estabelecida com {addr} (Cliente {client_id})')
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                log_event(f'Cliente {client_id} ({addr}) desconectou.')
                print(f'Cliente {client_id} ({addr}) desconectou.')
                break

            mensagem_cliente = data.decode().strip()
            log_event(f'Cliente {client_id}: {mensagem_cliente}')
            print(f'Cliente {client_id}: {mensagem_cliente}')

            if mensagem_cliente.upper() == "EXIT":
                conn.sendall("OK".encode())  
                log_event(f'Encerrando conexão com Cliente {client_id}')
                break

            resposta = process_command(mensagem_cliente.upper())
            conn.sendall(resposta.encode())
    except (socket.timeout, ConnectionResetError) as e:
        log_event(f'Erro no cliente {client_id} ({addr}): {e}')
        print(f'Erro no cliente {client_id} ({addr}): {e}')
    finally:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        log_event(f'Conexão encerrada com Cliente {client_id} ({addr})')
        print(f'Conexão encerrada com Cliente {client_id} ({addr})')

def start_server():
    """Inicia o servidor."""
    HOST = ''
    PORT = 5000
    max_clients = 10
    queue = Queue()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(max_clients)
    print(f'Servidor escutando na porta {PORT}...')

    client_id = 0
    try:
        while True:
            conn, addr = servidor.accept()
            client_id += 1
            if threading.active_count() - 1 < max_clients:
                thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
                thread.start()
                print(f'Clientes ativos: {threading.active_count() - 1}')
            else:
                log_event("Número máximo de clientes alcançado. Recusando conexão.")
                print("Número máximo de clientes alcançado. Recusando conexão.")
                conn.close()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.close()

if __name__ == "__main__":
    start_server()
