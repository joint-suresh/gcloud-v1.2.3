import socket
import threading
import time

PROCESS_PORTS = [5001, 5002, 5003]
RECEIVED_REPLIES = set()

def listen(my_port):
    global RECEIVED_REPLIES
    server = socket.socket()
    server.bind(('localhost', my_port))
    server.listen()
    print(f"[{my_port}] Listening for messages...")

    while True:
        conn, addr = server.accept()
        try:
            msg = conn.recv(1024).decode()

            if msg.startswith("REQUEST"):
                sender_port = int(msg.split(":")[1])
                print(f"[{my_port}] Received REQUEST from {sender_port}")
                conn.send(f"REPLY:{my_port}".encode())

            elif msg.startswith("REPLY"):
                sender_port = int(msg.split(":")[1])
                print(f"[{my_port}] Received REPLY from {sender_port}")
                RECEIVED_REPLIES.add(sender_port)
        except Exception as e:
            print(f"[{my_port}] Error while receiving message: {e}")
        conn.close()

def request_cs(my_port):
    global RECEIVED_REPLIES
    RECEIVED_REPLIES = set()
    print(f"[{my_port}] Requesting Critical Section...")

    for port in PROCESS_PORTS:
        if port != my_port:
            s = socket.socket()
            try:
                s.connect(('localhost', port))
                s.send(f"REQUEST:{my_port}".encode())
                reply = s.recv(1024).decode()
                if reply.startswith("REPLY"):
                    sender_port = int(reply.split(":")[1])
                    print(f"[{my_port}] Received REPLY from {sender_port}")
                    RECEIVED_REPLIES.add(sender_port)
            except Exception as e:
                print(f"[{my_port}] Could not connect to {port}: {e}")
            s.close()

    while len(RECEIVED_REPLIES) < len(PROCESS_PORTS) - 1:
        print(f"[{my_port}] Waiting... Received replies: {RECEIVED_REPLIES}")
        time.sleep(0.5)

    print(f"[{my_port}] Entering Critical Section...")
    time.sleep(2)
    print(f"[{my_port}] Exiting Critical Section...")

def run(my_port):
    threading.Thread(target=listen, args=(my_port,), daemon=True).start()
    while True:
        input(f"[{my_port}] Press Enter to request CS...")
        request_cs(my_port)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    run(port)