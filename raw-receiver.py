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
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol)
# set sniffer to include the IP header. don't understand...
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# buffsize = 65536 (max size of payload) + 20 (ip header)
pkt = sniffer.recv(65556)
header = pkt[:20]
print(f'IP header: {header}')
payload = pkt[20:]
print(f'Payload: {payload}')

# close socket
sniffer.close()
