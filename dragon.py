import socket
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
from multiprocessing.sharedctypes import Value
from buffer import SendBuffer, RecvBuffer
from packet import DragonPacket

MAX_DRAGON_LENGTH = 2048
MAX_DRAGON_PAYLOAD = 1280


def sender(buffer, credit, sock, addr):
    while True:
        if not buffer.empty() and credit.value > 0:
            d = buffer.get(MAX_DRAGON_PAYLOAD)
            packet = DragonPacket()
            sock.sendto(packet.toBytes(), addr)


def receiver(buffer, credit, sock, addr):
    while True:
        raw = sock.recv(MAX_DRAGON_LENGTH)
        packet = DragonPacket()
        # packet.parse(raw)
        if packet.is_ack():
            credit.value = packet.credit
        else:
            # buffer.insert(packet.seq, packet.payload)
            buffer.whatever(raw)


class DragonManager(BaseManager):
    pass


DragonManager.register('sbuffer', SendBuffer, exposed=['get', 'push'])
DragonManager.register('rbuffer', RecvBuffer, exposed=['get', 'insert', 'whatever'])


class Dragon:
    local_port = None
    accept_host = None

    def __init__(self, remote_ip, remote_port):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.addr = (self.remote_ip, self.remote_port)
        self.credit = Manager().Value('i', 1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        DragonManager.register('sbuffer', SendBuffer, exposed=None)
        # DragonManager.register('sbuffer', SendBuffer, exposed=['get', 'push', 'empty'])
        DragonManager.register('rbuffer', RecvBuffer, exposed=None)
        # DragonManager.register('rbuffer', RecvBuffer, exposed=['get', 'insert', 'empty'])
        self.manager = DragonManager()
        self.manager.start()

        self.sbuffer = self.manager.sbuffer()
        self.rbuffer = self.manager.rbuffer()

        self.sender = Process(target=sender, args=(self.sbuffer, self.credit, self.sock, self.addr))
        self.receiver = Process(target=receiver, args=(self.rbuffer, self.credit, self.sock, self.addr))
        self.sender.start()
        self.receiver.start()

    def connect(self):
        pass

    def bind(self, addr: tuple):
        self.accept_host, self.local_port = addr
        self.sock.bind(addr)

    def send(self, data: bytes):
        self.sbuffer.push(data)

    def recv(self, size: int):
        return self.rbuffer.get(size)

    def close(self):
        self.sender.terminate()
        self.receiver.terminate()

