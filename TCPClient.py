#!/usr/bin/env python
# https://wiki.python.org/moin/TcpCommunication

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
# import RealTimeSocket
# LOCALHOST = "127.0.0.1"
# MUMBAI = "13.233.94.35"


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE.encode())
    data = s.recv(BUFFER_SIZE)
    s.close()
    # sock = RealTimeSocket.Dragon()
    # sock.connect((MUMBAI, 6000))
    # sock.send(b'Hello world!')
    # sock.close()

if __name__ == "__main__":
    main()