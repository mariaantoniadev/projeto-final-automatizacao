import socket
import threading
import random
import time

def cliente_simulado(id_cliente):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('localhost', 5000))
        print(f"Cliente {id_cliente} conectado.")

        comandos = ["ECHO", "TIME", "EXIT"]
        for _ in range(10):  
            comando = random.choice(comandos)  
            cliente.sendall(comando.encode())
            resposta = cliente.recv(1024).decode()
            print(f"Cliente {id_cliente}: {resposta}")
            time.sleep(0.5)  

        cliente.close()
    except Exception as e:
        print(f"Cliente {id_cliente} encontrou um erro: {e}")


def executar_testes_de_estresse():
    threads = []
    for i in range(5): 
        thread = threading.Thread(target=cliente_simulado, args=(i,))
        threads.append(thread)
        thread.start()
        time.sleep(0.2)  

    for thread in threads:
        thread.join()

    print("Teste de estresse concluído.")


if __name__ == "__main__":
    executar_testes_de_estresse()
