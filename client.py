import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with open("text.txt", "rb") as f:
    content = f.read(2048)
    while content:
        sock.sendto(content, ("13.127.24.32", 65001))
        content = f.read(2048)

sock.close()
