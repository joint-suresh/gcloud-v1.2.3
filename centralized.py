# Centralized coordinator server and clients
# This is a minimal prototype for 3 clients

import threading
import socket
import time

lock = threading.Lock()
current_holder = None

def coordinator_server():
    global current_holder
    s = socket.socket()
    s.bind(('localhost', 6000))
    s.listen(5)
    print("Coordinator started...")

    while True:
        conn, addr = s.accept()
        msg = conn.recv(1024).decode()
        if msg.startswith("REQUEST"):
            with lock:
                if current_holder is None:
                    current_holder = conn
                    conn.send("GRANT".encode())
                else:
                    conn.send("DENY".encode())
        elif msg.startswith("RELEASE"):
            with lock:
                current_holder = None
        conn.close()

def client(id):
    s = socket.socket()
    s.connect(('localhost', 6000))
    s.send("REQUEST".encode())
    reply = s.recv(1024).decode()
    if reply == "GRANT":
        print(f"Client {id} entered CS")
        time.sleep(2)
        s = socket.socket()
        s.connect(('localhost', 6000))
        s.send("RELEASE".encode())
        print(f"Client {id} exited CS")
    else:
        print(f"Client {id} denied access")

if __name__ == "__main__":
    threading.Thread(target=coordinator_server, daemon=True).start()
    time.sleep(1)
    for i in range(3):
        threading.Thread(target=client, args=(i,)).start()
