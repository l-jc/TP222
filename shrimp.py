# reliable stream
import logging
import socket
from multiprocessing import Process, Value, Event
from multiprocessing.managers import BaseManager
from buffer import SendBuffer, RecvBuffer
from packet import DragonPacket
from window import ShrimpWindow

MAX_DRAGON_LENGTH = 2048
MAX_DRAGON_PAYLOAD = 1280
logging.basicConfig(level=logging.DEBUG)


class Sender(Process):
    def __init__(self, sock, peer, buffer, window, wndsize):
        super(Sender, self).__init__()
        self.sock = sock
        self.peer = peer
        self.buffer = buffer
        self.window = window
        self.sig = Event()
        self.wndsize = wndsize

    def stop(self):
        self.sig.set()

    def run(self):
        while not self.sig.is_set():
            if not self.buffer.empty() and self.window.size() < self.wndsize.value:
                packet = DragonPacket()
                packet.flags = {
                    'ack': False,
                    'syn': False,
                    'fin': False,
                    'cre': False,
                    'fec': False,
                    'ooo': False,
                }
                packet.seqno = self.buffer.get_seqno()
                packet.wndsize = self.wndsize.value
                data = self.buffer.get(MAX_DRAGON_PAYLOAD)
                packet.populate(data)
                binary = packet.tobytes()
                self.window.put(packet.seqno + len(data), binary)
                self.sock.sendto(binary, self.peer)
                logging.debug(f'SEND {packet}')
                logging.debug(f'SEND binary : {binary}')
        # clean
        self.clean()

    def clean(self):
        if self.window.size() > 0:
            logging.warning(f'socket closed when there are unacknowledged packets')
        self.sock.close()


class Receiver(Process):
    def __init__(self, sock, peer, buffer, window, wndsize):
        super(Receiver, self).__init__()
        self.sock = sock
        self.peer = peer
        self.buffer = buffer
        self.sig = Event()
        self.window = window
        self.wndsize = wndsize

    def stop(self):
        self.sig.set()

    def run(self):
        while not self.sig.is_set():
            raw = self.sock.recv(MAX_DRAGON_LENGTH)
            packet = DragonPacket()
            packet.parse(raw)
            logging.debug(f'RECEIVED {packet}')
            logging.debug(f'RECEIVED binary : {raw}')
            if packet.is_ack():
                # to do: set window size
                acked = packet.ackno
                self.window.pop(acked)
                if packet.flags['ooo']:
                    # retransmit out of order packet
                    for (expno, packetbytes) in self.window.items():
                        if expno < acked:
                            self.sock.sendto(packetbytes, self.peer)
            else:
                ack = DragonPacket()
                # to do: set window size
                ack.flags['ack'] = True
                if self.buffer.get_start() + self.buffer.size() < packet.seqno:
                    ack.flags['ooo'] = True
                ack.ackno = packet.seqno + len(packet.payload)
                ack.populate(b'')
                self.sock.sendto(ack.tobytes(), self.peer)
                self.buffer.insert(packet.seqno, packet.payload)
        self.sock.close()


class ShrimpManager(BaseManager):
    pass


class Shrimp:
    local_port = None
    accept_host = None

    def __init__(self, remote_ip, remote_port):
        self.wndsize = Value('i', 100)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.peer = (self.remote_ip, self.remote_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        ShrimpManager.register('SendBuffer', SendBuffer, exposed=None)
        ShrimpManager.register('RecvBuffer', RecvBuffer, exposed=None)
        ShrimpManager.register('ShrimpWindow', ShrimpWindow, exposed=None)
        self.manager = ShrimpManager()
        self.manager.start()

        self.sender_buffer = self.manager.SendBuffer()
        self.receiver_buffer = self.manager.RecvBuffer()
        self.window = self.manager.ShrimpWindow()

        self.sender = Sender(self.sock, self.peer, self.sender_buffer, self.window, self.wndsize)
        self.receiver = Receiver(self.sock, self.peer, self.receiver_buffer, self.window, self.wndsize)
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
