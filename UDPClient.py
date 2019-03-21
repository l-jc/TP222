# UDP client
import socket
import utils

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

def main():
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    frameGen = utils.Generator()

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print ("received message:", frameGen.byteToFrame(data))
        
if __name__ == '__main__':
    main()