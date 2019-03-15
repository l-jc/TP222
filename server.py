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
MUMBAI = "13.233.94.35"


def main():
    pass

if __name__ == '__main__':
    main()
