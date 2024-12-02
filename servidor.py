import socket
import threading
import logging
import datetime
from queue import Queue

# Configuração do log
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
        conn.settimeout(10)  # Define um timeout de 10 segundos para conexões
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
    except socket.timeout:
        log_event(f'Conexão com {addr} expirou por inatividade.')
        print(f'Conexão com {addr} expirou por inatividade.')
    except ConnectionResetError:
        log_event(f'Conexão com {addr} foi encerrada abruptamente.')
        print(f'Conexão com {addr} foi encerrada abruptamente.')
    except Exception as e:
        log_event(f'Erro no cliente {addr}: {e}')
        print(f'Erro no cliente {addr}: {e}')
    finally:
        conn.close()
        log_event(f'Conexão fechada com {addr}')
        print(f'Conexão fechada com {addr}')


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
