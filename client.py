import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sock.sendto(b"Hello world", ("127.0.0.1", 65001))
    x = input("Continue? ")

sock.close()