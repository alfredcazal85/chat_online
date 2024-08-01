import socket #libreria que permite conectarse a las compus en el chat para envio de mensajes
import threading #libreria que permite manejar hilos de ejecucion para que se puedan hacer cosas de manera simultanea

# Configuración donde establecemos a que computadora conectarnos, donde se aloja el servidor
HOST = '127.0.0.1'
PORT = 12345

def start_client(): #funcion de instrucciones y logica para conectarse y chatear
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client_socket.connect((HOST, PORT))

    user = input("Introduce tu nombre de usuario: ") #pide al usuario que ingrese su nombre para mostrarlo en el chat y a los demas participantes
    client_socket.send(user.encode('utf-8'))

    print("Conectado al servidor de chat. Puedes empezar a enviar mensajes. Escribe '/salir' para desconectarte.") #mensaje que se muestra al conectarse y comando para salir

    def receive_messages(): #funcion para recibir mensajes desde el servidor, usa bucle
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    print("Conexión cerrada por el servidor")
                    client_socket.close()#si no hay conexion cierra el socket
                    break
                else:
                    print(message)
            except:
                print("Error al recibir mensaje")
                client_socket.close() #si hay error cierra el socket
                break

    def send_messages():#funcion para enviar mensajes al servidor, usa bucle
        while True:
            try:
                message = input()
                client_socket.send(message.encode('utf-8'))
                if message == "/salir": #si el usuario da comando salir desconecta del chat
                    print("Te has desconectado del chat.")
                    client_socket.close()
                    break
            except:
                print("Error al enviar mensaje")
                client_socket.close() #si hay error se imprime y cierra el socket del cliente 
                break

    receive_thread = threading.Thread(target=receive_messages) #se crea un hilo para la funcion receive messages 
    receive_thread.start()

    send_messages() #ejecuta hilo principal y asegura que se complete antes de seguir con el programa
    receive_thread.join()

def main(): #funcion que pregunta cuando le pone salir del chat, si desea iniciar otra conversacion, si no responde si, sale del chat
    while True:
        start_client()
        response = input("¿Quieres iniciar una nueva conversación? (sí/no): ").strip().lower()
        if response != "sí":
            print("Saliendo del chat. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main() #asegura que la función main se ejecute solo si el script se ejecuta directamente
