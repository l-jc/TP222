#!/usr/bin/env python
# https://wiki.python.org/moin/TcpCommunication

import socket
import utils
import time

# iframe refreshes every 15 secs, pframe 0.1 sec
CONST_iFrame_Ref = 15
CONST_pFrame_Ref = 0.1
# transmission lasts 10 mins
CONST_Last_Time = 60

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

def main():

    startTime = time.time()
    iLastTime = startTime
    pLastTime = startTime
    curTime = startTime

    frameGen = utils.Generator()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    # s.send(MESSAGE.encode())
    # data = s.recv(BUFFER_SIZE)
    
    s.send(frameGen.get_iframe())
    s.send(frameGen.get_pframe())

    while(pLastTime < startTime + CONST_Last_Time):
        curTime = time.time()
        duration = time.time() - startTime
        # print("Minutes: ", duration/60, "Seconds: ", duration%60)
        if(curTime > iLastTime + CONST_iFrame_Ref):
            s.send(frameGen.get_iframe())
            iLastTime = curTime
        elif(curTime > pLastTime + CONST_pFrame_Ref):
            s.send(frameGen.get_pframe())
            pLastTime = curTime

    frameGen.store()
    s.close()
    duration = time.time() - startTime
    print("Minutes: ", duration/60, "Seconds: ", duration%60)

if __name__ == "__main__":
    main()