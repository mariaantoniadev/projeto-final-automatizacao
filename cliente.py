import socket
import time

def show_menu():
    """Exibe o menu de comandos disponíveis."""
    print("\nComandos disponíveis:")
    print("1. ECHO")
    print("2. TIME")
    print("3. EXIT\n")

HOST = 'localhost'  # Endereço IP do servidor
PORT = 5000         # Porta que o servidor está escutando

def connect_to_server():
    """Tenta conectar ao servidor."""
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            cliente.connect((HOST, PORT))
            print('Conectado ao servidor.')
            return cliente
        except ConnectionRefusedError:
            print('Não foi possível conectar ao servidor. Tentando novamente...')
            time.sleep(5)
cliente = connect_to_server()
try:
    cliente.connect((HOST, PORT))
    print('Conectado ao servidor.')
except ConnectionRefusedError:
    print('Não foi possível conectar ao servidor.')
    exit()

try:
    while True:
        mensagem = input('Você (cliente): ')
        if mensagem.lower() == 'sair':
            print('Encerrando conexão.')
            break
        cliente.sendall(mensagem.encode())
        data = cliente.recv(1024)
        if not data:
            print('Conexão encerrada pelo servidor.')
            break
        resposta_servidor = data.decode()
        print(f'Servidor: {resposta_servidor}')
except KeyboardInterrupt:
    print('\nConexão interrompida pelo usuário.')
finally:
    cliente.close()
    print('Conexão fechada.')