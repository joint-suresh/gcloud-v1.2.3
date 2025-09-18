import socket
import pickle
from ipc.data import DataObject


host = '127.0.0.1'
port = 8000

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((host,port))
print("Client connnected to the server")
obj = [1,2,3,4,5,6,7,8]
raw_data = DataObject(obj)
data  = pickle.dumps(raw_data)

client_socket.send(data)

total_value= client_socket.recv(1024).decode()
print("Total received at the server", total_value)

raw_exit = pickle.dumps('Exit')
response = client_socket.send(raw_exit)
print(" Server rsponse",response)
client_socket.close()











































































# import socket
# import pickle
# from data import DataObject

# host = '127.0.0.1'
# port = 8000

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((host,port))

# print("client connected to the server")
# values=[1,2,3,4,5,6,7]
# obj = DataObject(values)
# raw_data = pickle.dumps(obj)

# client_socket.send(raw_data)

# total_value = client_socket.recv(1024).decode()
# print("Server sent", total_value)

# raw_exit = pickle.dumps("Exit")
# response = client_socket.send(raw_exit)
# print("Server response",response)
# client_socket.close()