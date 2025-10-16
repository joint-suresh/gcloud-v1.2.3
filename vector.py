import socket
import threading
import sys
import ast  # To safely convert string back to list

# ---------------------- CLOCK FUNCTIONS ----------------------

def increment_clock(vc, index):
    """Increment the vector clock for the process at given index"""
    vc[index] += 1

def update_clock(local_vc, recv_vc):
    """Merge received vector into local vector (element-wise max)"""
    for i in range(len(local_vc)):
        local_vc[i] = max(local_vc[i], recv_vc[i])

# ---------------------- SERVER CODE ----------------------
def server_program():
    server_id = 1  # Index for server in vector [client, server]
    vector_clock = [0, 0]

    host = '127.0.0.1'
    port = 5002

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[SERVER] Listening on {host}:{port}")

    conn, address = server_socket.accept()
    print(f"[SERVER] Connection established with {address}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        msg, recv_vector = data.split('|')
        recv_vector = ast.literal_eval(recv_vector)  # Convert string "[x, y]" to list

        # Step 1: Merge clocks
        update_clock(vector_clock, recv_vector)

        # Step 2: Increment server’s own clock
        increment_clock(vector_clock, server_id)

        print(f"[SERVER] Received '{msg}' with client vector {recv_vector}")
        print(f"[SERVER] Updated Vector Clock: {vector_clock}\n")

        # Step 3: Send acknowledgment with current vector
        increment_clock(vector_clock, server_id)
        reply = f"ACK|{vector_clock}"
        conn.send(reply.encode())

    conn.close()

# ---------------------- CLIENT CODE ----------------------
def client_program():
    client_id = 0  # Index for client in vector [client, server]
    vector_clock = [0, 0]

    host = '127.0.0.1'
    port = 5002

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while True:
        msg = input("[CLIENT] Enter message (or 'exit' to quit): ")
        if msg.lower() == 'exit':
            break

        # Step 1: Increment client’s own clock before sending
        increment_clock(vector_clock, client_id)

        # Step 2: Send message and vector
        payload = f"{msg}|{vector_clock}"
        client_socket.send(payload.encode())
        print(f"[CLIENT] Sent '{msg}' with vector {vector_clock}")

        # Step 3: Receive ACK and update clock
        data = client_socket.recv(1024).decode()
        reply, recv_vector = data.split('|')
        recv_vector = ast.literal_eval(recv_vector)

        update_clock(vector_clock, recv_vector)
        increment_clock(vector_clock, client_id)

        print(f"[CLIENT] Received '{reply}' with server vector {recv_vector}")
        print(f"[CLIENT] Updated Vector Clock: {vector_clock}\n")

    client_socket.close()

# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python vector_clock.py server")
        print("  python vector_clock.py client")
        sys.exit(0)

    role = sys.argv[1]

    if role == 'server':
        server_program()
    elif role == 'client':
        client_program()
    else:
        print("Invalid role! Use 'server' or 'client'")