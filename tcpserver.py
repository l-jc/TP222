import socket
import time

CLIENT = "34.210.120.119"
CPORT = 7000
PORT = 6000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', PORT))
    sock.listen(1)

    conn, addr = sock.accept()
    fake_frame = bytearray(491520)
    print(time.time())
    conn.send(fake_frame)

    conn.close()

if __name__ == "__main__":
    main()


