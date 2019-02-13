"""
A simple example of using raw ip socket
"""

import socket

# ip protocol numbers.
# see : https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
protocol = 254

# AF_INET: use IPv4
# SOCK_RAW: use raw socket
# protocol: our protocol number
sender = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol)

# destination: localhost
dst = ("127.0.0.1", 0)
pkt = b"<OUR PROTOCOL PACKET>"
sender.sendto(pkt, dst)

# close socket
sender.close()
