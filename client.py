# import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# with open("sample.txt", "rb") as f:
#     content = f.read(2048)
#     while content:
#         sock.sendto(content, ("127.0.0.1", 65001))
#         content = f.read(2048)
#
# sock.close()


import RealTimeSocket
import time

LOCALHOST = "127.0.0.1"


def main():
    sock = RealTimeSocket.RealTimeSocket(LOCALHOST, 9998)

    sock.bind(9999)
    t = time.time()
    buff = sock.recv(0.2)
    print(f"received {time.time() - t}")

    if buff:
        open("receive.txt", "wb").write(buff)

    sock.close()


if __name__ == "__main__":
    main()
