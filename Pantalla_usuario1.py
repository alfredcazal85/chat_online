import socket
import threading

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 12345

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    user = input("Introduce tu nombre de usuario: ")
    client_socket.send(user.encode('utf-8'))

    print("Conectado al servidor de chat. Puedes empezar a enviar mensajes. Escribe '/salir' para desconectarte.")

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print("Conexión cerrada por el servidor")
                    client_socket.close()
                    break
                else:
                    print(message)
            except:
                print("Error al recibir mensaje")
                client_socket.close()
                break

    def send_messages():
        while True:
            try:
                message = input()
                client_socket.send(message.encode('utf-8'))
                if message == "/salir":
                    print("Te has desconectado del chat.")
                    client_socket.close()
                    break
            except:
                print("Error al enviar mensaje")
                client_socket.close()
                break

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_messages()
    receive_thread.join()

def main():
    while True:
        start_client()
        response = input("¿Quieres iniciar una nueva conversación? (sí/no): ").strip().lower()
        if response != "sí":
            print("Saliendo del chat. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
