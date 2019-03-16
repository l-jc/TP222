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

LOCALHOST = "127.0.0.1"
MUMBAI = "13.233.94.35"


def main():
    sock = RealTimeSocket.Dragon()
    sock.connect((MUMBAI, 6000))

    sock.send(b'Hello world!')

    sock.close()


if __name__ == "__main__":
    main()
