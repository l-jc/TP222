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
MUMBAI = "13.233.94.35"


def main():
    pass


if __name__ == "__main__":
    main()
