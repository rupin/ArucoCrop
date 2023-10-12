
import socket
import pickle
import struct
from PIL import Image

def read_image(file_path):
    with Image.open(file_path) as im:
        width, height=im.width, im.height
    with open(file_path, "rb") as file:
        image_bytes = file.read()
    return width, height, image_bytes


print("Result Generated, sending across")
# Constants
HOST = '192.168.29.213'
PORT = 12345

# Create a socket connection to Unity
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

width, height, imagebytes=read_image("result.png")

client_socket.sendall(width.to_bytes())
client_socket.sendall(height.to_bytes())

client_socket.close()
client_socket=None

