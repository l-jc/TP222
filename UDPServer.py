# https://wiki.python.org/moin/UdpCommunication\
import socket
# import RealTimeSocket
# LOCALHOST = "127.0.0.1"
# MUMBAI = "13.233.94.35"

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"


def main():
    # print "UDP target IP:", UDP_IP
    # print "UDP target port:", UDP_PORT
    # print "message:", MESSAGE
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))    

if __name__ == "__main__":
    main()





