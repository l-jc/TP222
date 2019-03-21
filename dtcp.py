import socket
import time

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('52.79.237.101', 6000))
    buff = b''
    while True:
        data = sock.recv(1500)
        if not data:
            break
        buff = buff + data
    print(time.time())

main()
