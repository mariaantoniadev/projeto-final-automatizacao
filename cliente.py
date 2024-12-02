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

def main():
    """Função principal para o cliente."""
    cliente = connect_to_server()
    try:
        while True:
            show_menu()
            mensagem = input('Você (cliente): ')
            
            if mensagem.strip() == "":
                print("Comando vazio. Tente novamente.")
                continue
            
            cliente.sendall(mensagem.encode())
            
            if mensagem.upper() == "EXIT":
                data = cliente.recv(1024)
                if data.decode().strip().upper() == "OK":
                    print("Conexão encerrada com sucesso pelo servidor.")
                else:
                    print("Servidor não confirmou encerramento.")
                cliente.shutdown(socket.SHUT_RDWR)  
                cliente.close()
                break
            
            data = cliente.recv(1024)
            if not data:
                print('Conexão encerrada pelo servidor.')
                break
            
            resposta_servidor = data.decode()
            print(f'Servidor: {resposta_servidor}')
    except KeyboardInterrupt:
        print('\nConexão interrompida pelo usuário.')
    except ConnectionResetError:
        print('A conexão foi encerrada inesperadamente pelo servidor.')
    finally:
        cliente.close()
        print('Conexão fechada.')

if __name__ == "__main__":
    main()
