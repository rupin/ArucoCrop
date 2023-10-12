
import socket
import pickle
import struct

def read_image(file_path):
    with open(file_path, "rb") as file:
        image_bytes = file.read()
    return image_bytes


print("Result Generated, sending across")
# Constants
HOST = '192.168.29.16'
PORT = 12345

# Create a socket connection to Unity
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.sendall(read_image("result.png"))
client_socket.close()
client_socket=None

