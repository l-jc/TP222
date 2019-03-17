#!/usr/bin/env python
# https://wiki.python.org/moin/TcpCommunication

# import RealTimeSocket
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
# LOCALHOST = "127.0.0.1"
# MUMBAI = "13.233.94.35"

# def main():
#     sock = RealTimeSocket.Dragon()
#     ip, port = sock.accept()

#     data = sock.recv(1024)

#     print(data)
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    # print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print ("received data:", data  )  
        conn.send(data)  # echo
    conn.close()


if __name__ == '__main__':
    main()



