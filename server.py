import socket

HOST = ""
PORT = 65001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

content = b""

try:
    while True:
        data, addr = sock.recvfrom(4096)
        content += data
except KeyboardInterrupt:
    open("receive.txt", 'wb').write(content)

sock.close()

