# unreliable stream

import socket
from multiprocessing import Process, Value, Event
from multiprocessing.managers import BaseManager
from buffer import SendBuffer, RecvBuffer
from packet import DragonPacket
import logging

MAX_DRAGON_LENGTH = 2048
MAX_DRAGON_PAYLOAD = 1280
logging.basicConfig(level=logging.DEBUG)


class Sender(Process):
    def __init__(self, sock, peer, buffer, credit: Value):
        super(Sender, self).__init__()
        self.sock = sock
        self.peer = peer
        self.buffer = buffer
        self.credit = credit
        self.sig = Event()

    def stop(self):
        self.sig.set()

    def run(self):
        while not self.sig.is_set():
            if not self.buffer.empty() and self.credit.value > 0:
                packet = DragonPacket()
                packet.flags = {
                    'ack': False,
                    'syn': False,
                    'fin': False,
                    'cre': True,
                    'fec': False,
                    'ooo': False,
                }
                packet.seqno = self.buffer.get_seqno()
                data = self.buffer.get(MAX_DRAGON_PAYLOAD)
                binary = packet.tobytes(data)
                self.sock.sendto(binary, self.peer)
                logging.debug(f'SEND\n{packet}')

        # clean
        self.clean()

    def clean(self):
        while not self.buffer.empty():
            packet = DragonPacket()
            packet.flags = {
                'ack': False,
                'syn': False,
                'fin': False,
                'cre': True,
                'fec': False,
                'ooo': False,
            }
            packet.seqno = self.buffer.get_seqno()
            data = self.buffer.get(MAX_DRAGON_PAYLOAD)
            self.sock.sendto(packet.tobytes(data), self.peer)
        self.sock.close()


class Receiver(Process):
    def __init__(self, sock, peer, buffer, credit: Value):
        super(Receiver, self).__init__()
        self.sock = sock
        self.peer = peer
        self.buffer = buffer
        self.credit = credit
        self.sig = Event()

    def stop(self):
        self.sig.set()

    def run(self):
        while not self.sig.is_set():
            raw = self.sock.recv(MAX_DRAGON_LENGTH)
            packet = DragonPacket()
            packet.parse(raw)
            logging.debug(f'RECEIVED\n{packet}')
            if packet.is_ack():
                self.credit.value = packet.credit
            else:
                ack = DragonPacket()
                ack.credit = self.credit.value
                ack.flags['ack'] = True
                ack.ackno = packet.seqno + len(packet.payload)
                self.sock.sendto(ack.tobytes(b''), self.peer)
                self.buffer.insert(packet.seqno, packet.payload)
        self.sock.close()


class DragonManager(BaseManager):
    pass


# DragonManager.register('sbuffer', SendBuffer, exposed=['get', 'push'])
# DragonManager.register('rbuffer', RecvBuffer, exposed=['get', 'insert', 'whatever'])


class Dragon:
    local_port = None
    accept_host = None

    def __init__(self, remote_ip, remote_port):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.peer = (self.remote_ip, self.remote_port)
        self.credit = Value('i', 1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        DragonManager.register('SendBuffer', SendBuffer, exposed=None)
        DragonManager.register('RecvBuffer', RecvBuffer, exposed=None)
        self.manager = DragonManager()
        self.manager.start()

        self.sender_buffer = self.manager.SendBuffer()
        self.receiver_buffer = self.manager.RecvBuffer()

        self.sender = Sender(self.sock, self.peer, self.sender_buffer, self.credit)
        self.receiver = Receiver(self.sock, self.peer, self.receiver_buffer, self.credit)
        self.sender.start()
        self.receiver.start()

    def connect(self):
        pass

    def bind(self, addr: tuple):
        self.accept_host, self.local_port = addr
        self.sock.bind(addr)

    def send(self, data: bytes):
        self.sender_buffer.push(data)

    def recv(self, size: int):
        return bytes(self.receiver_buffer.get(size))

    def close(self):
        self.sender.stop()
        self.receiver.terminate()
        self.sock.close()

