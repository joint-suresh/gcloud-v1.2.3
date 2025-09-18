import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print(f"\n[Broadcast] {message}")
        except:
            print("Connection lost.")
            client.close()
            break

def send():
    while True:
        msg = input()
        client.send(msg.encode())

threading.Thread(target=receive).start()
threading.Thread(target=send).start()
