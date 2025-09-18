import socket
import threading

HOST = '127.0.0.1'
PORT = 65432
clients = []

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"[{address}] {message.decode()}")
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[STARTED] Server listening on {HOST}:{PORT}")
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
