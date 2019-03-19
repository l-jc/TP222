#!/usr/bin/env python
# https://wiki.python.org/moin/TcpCommunication

import socket
import utils
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

def main():
    startTime = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()


    frameGen = utils.Generator()
    itr = 0
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print ("received data:","iterations: ", itr)
        itr = itr + 1
        # frameGen.byteToFrame(data)) 
        # conn.send(data)  # echo
    duration = time.time() - startTime
    print("Minutes: ", duration/60, "Seconds: ", duration%60)
    conn.close()

if __name__ == '__main__':
    main()