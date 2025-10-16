
import socket
import threading
import sys
import time

# Initialize Lamport clock
logical_clock = 0

# Function to increment the clock on local events (like sending or receiving)
def increment_clock(received_time=None):
    global logical_clock
    if received_time is not None:
        # On receiving a message: take the max and increment by 1
        logical_clock = max(logical_clock, received_time) + 1
    else:
        # On local event (like sending): just increment by 1
        logical_clock += 1

# ---------------------- SERVER CODE ----------------------
def server_program():
    global logical_clock
    host = '127.0.0.1'
    port = 5001

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[SERVER] Listening on {host}:{port}")

    conn, address = server_socket.accept()
    print(f"[SERVER] Connection from {address}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        msg, recv_time = data.split(',')
        recv_time = int(recv_time)

        # Update server clock using Lamport’s rule
        increment_clock(recv_time)
        print(f"[SERVER] Received '{msg}' with timestamp {recv_time}")
        print(f"[SERVER] Updated Logical Clock = {logical_clock}\n")

        # Send acknowledgment with updated clock
        increment_clock()
        reply = f"ACK,{logical_clock}"
        conn.send(reply.encode())

    conn.close()

# ---------------------- CLIENT CODE ----------------------
def client_program():
    global logical_clock
    host = '127.0.0.1'
    port = 5001

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while True:
        msg = input("[CLIENT] Enter a message (or 'exit' to quit): ")
        if msg.lower() == 'exit':
            break

        increment_clock()
        message = f"{msg},{logical_clock}"
        client_socket.send(message.encode())
        print(f"[CLIENT] Sent '{msg}' with timestamp {logical_clock}")

        # Receive acknowledgment
        data = client_socket.recv(1024).decode()
        reply, recv_time = data.split(',')
        recv_time = int(recv_time)

        increment_clock(recv_time)
        print(f"[CLIENT] Received ACK with timestamp {recv_time}")
        print(f"[CLIENT] Updated Logical Clock = {logical_clock}\n")

    client_socket.close()

# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python lamport_clock.py server")
        print("  python lamport_clock.py client")
        sys.exit(0)

    role = sys.argv[1]

    if role == 'server':
        server_program()
    elif role == 'client':
        client_program()
    else:
        print("Invalid role! Use 'server' or 'client'")