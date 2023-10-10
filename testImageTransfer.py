import socket
import pickle
import struct

HOST = '192.168.29.16'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

conn, addr = server_socket.accept()

data = b''
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    if msg_size == 0:
        # No more data to receive, break out of the loop
        break

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Save the received image to a file
    with open("received_image.jpg", "wb") as image_file:
        image_file.write(frame_data)

# Close the connection and socket
conn.close()
server_socket.close()
