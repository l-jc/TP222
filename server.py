# import socket

# HOST = ""
# PORT = 65001
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((HOST, PORT))
#
# content = b""
#
# try:
#     while True:
#         data, addr = sock.recvfrom(4096)
#         content += data
#         print(data[:2])
# except KeyboardInterrupt:
#     open("receive.txt", 'wb').write(content)
#
# sock.close()
#

import RealTimeSocket

LOCALHOST = "127.0.0.1"


def main():
    sock = RealTimeSocket.RealTimeSocket(LOCALHOST, 9999)
    data = open("big.txt", 'rb').read()

    sock.send(data)

    sock.close()


if __name__ == '__main__':
    main()
