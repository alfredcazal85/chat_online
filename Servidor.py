import socket #libreria que nos ayuda a comunicarnos en una red
import select #libreria que permite manejar conexiones

# Configuración del servidor del chat
HOST = '127.0.0.1' #direccion a utilizarse
PORT = 12345 #puerto a utilizarse
MAX_USERS = 5 #cantidad de usuarios para el chat, 

# Inicializa el socket del servidor 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #nos ayuda a enviar y recibir mensajes
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reutilizar el programa 
server_socket.bind((HOST, PORT)) #establecemos la direccion y puerto
server_socket.listen(MAX_USERS) #decimos que puede recibir hasta 5 usuarios en este caso

# Lista de sockets conectados
sockets_list = [server_socket] #guardamos las conexiones que se hacen, tanto del servidor como clientes conectados, gestiona conexiones activas y su comunicacion
clients = {} #diccionario de usuarios del chat para asociar quien envia mensaje 

print(f"Servidor de chat iniciado en {HOST}:{PORT}") #muestra un mensaje cuando se inicio el chat en el servidor cual es la dire y puerta utilizada

def broadcast(message, client_socket): #toma el mensaje de un usuario y lo envia a los demas, si no puede enviar a alguien cierra la conexion y lo elimina de la lista 
    for client in clients:
        if client != client_socket: #enviamos el mensaje a todos menos al remitente
            try:
                client.send(message)
            except:
                client.close() #cerramos conexion con ese cliente
                sockets_list.remove(client) #removemos de la lista de sockets
                del clients[client] #removemos del diccionario clientes

try: #es un bucle, usamos select hasta que haya algo que hacer como un nuevo mensaje o conexion
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
#Aqui revisamos todos los socket, si hay uno nuevo lo agregamos y comunicamos a los demas participantes del chat 
        for notified_socket in read_sockets: 
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                user = client_socket.recv(1024).decode('utf-8')
                sockets_list.append(client_socket)
                clients[client_socket] = user
                print(f"Conexión aceptada de {client_address[0]}:{client_address[1]} - Usuario: {user}")
                broadcast(f"{user} se ha unido al chat.\n".encode('utf-8'), client_socket)
            else: #Si el socket no es server socket, uno de los usuarios envio mensaje
                try:
                    message = notified_socket.recv(1024)
                    if not message: # si el mensaje viene vacio cerramos la conexion del usuario y lo removemos
                        print(f"Conexión cerrada por {clients[notified_socket]}")
                        sockets_list.remove(notified_socket)
                        broadcast(f"{clients[notified_socket]} ha salido del chat.\n".encode('utf-8'), notified_socket)
                        del clients[notified_socket]
                    else: #si el usuario le da el comando /salir, lo removemos y comunicamos al resto
                        user = clients[notified_socket]
                        decoded_message = message.decode('utf-8')
                        if decoded_message == "/salir":
                            print(f"{user} ha salido del chat.")
                            sockets_list.remove(notified_socket)
                            broadcast(f"{user} ha salido del chat.\n".encode('utf-8'), notified_socket)
                            del clients[notified_socket]
                            notified_socket.close()
                        else: #si el usuario manda un mensaje, compartimos a todos los conectados
                            print(f"Mensaje recibido de {user}: {decoded_message}")
                            broadcast(f"{user}: {decoded_message}".encode('utf-8'), notified_socket)
                except: 
                    sockets_list.remove(notified_socket) #evitamos que el servidor intente gestionar ese socket en el futuro.
                    del clients[notified_socket] #eliminamos de usuarios conectados para evitar posibles errores cuando tratemos de acceder a un cliente que ya no está conectado.
                    continue #asegura que el bucle continúe con el siguiente socket en la lista sin intentar realizar más operaciones con el socket problemático.

        for notified_socket in exception_sockets: #manejan los socket con problema 
            sockets_list.remove(notified_socket) #removemos de la lista sockets y diccionario clientes
            del clients[notified_socket]
except KeyboardInterrupt: #si alguien presiona ctrol c detiene el servidor y mostramos 
    print("\nServidor de chat cerrado.")
    server_socket.close()
