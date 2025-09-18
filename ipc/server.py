import socket
import pickle
from ipc.data import DataObject

host = '127.0.0.1'
port = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host,port))
server_socket.listen()

print(f"Server Started Listening")

conn,addr = server_socket.accept()
print(f"Server is conected by {addr}")


while 1:
    raw_data = conn.recv(1024)
    data = pickle.loads(raw_data)
    if isinstance(data,str):
        conn.send("Connnection Ended".encode())
        print('Connnection Closed')
        conn.close()
        break
    print("Server received the values",data.values)
    total  = str(sum(data.values))
    conn.send(total.encode())
server_socket.close()
















































































































# #IPC

# import socket
# import pickle
# from data import DataObject

# host = '127.0.0.1'
# port = 8000

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((host,port))

# server_socket.listen()

# print("Server Started")

# conn,addr = server_socket.accept()
# print("Server connected to ",addr)

# while 1:
#     raw_data = conn.recv(1024)
#     data = pickle.loads(raw_data)

#     if isinstance(data,str):
#         conn.send("Connection Ended".encode())
#         conn.close()
#         print('Server connecetion closed')
#         break
#     print("Server received the data",data.values)
#     total = str(sum(data.values))
#     conn.send(total.encode())
# server_socket.close()