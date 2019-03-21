# reliable stream
#
import logging
import random
import socket
from multiprocessing import Process, Value, Event
from multiprocessing.managers import BaseManager
from buffer import SendBuffer, RecvBuffer
from packet import DragonPacket
from window import ShrimpWindow
from resetable import RepeatedTask

MAX_DRAGON_LENGTH = 1500
MAX_DRAGON_PAYLOAD = 1480
logging.basicConfig(level=logging.DEBUG)

TEST = 0


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
                if TEST:
                    if random.random() < 0.7:
                        logging.debug(f'simulate drop')
                        pass
                    else:
                        self.sock.sendto(binary, self.peer)
                else:
                    self.sock.sendto(binary, self.peer)
                    logging.debug(f'SEND {packet}')
                    # logging.debug(f'SEND binary : {binary}')
        # clean
        self.clean()

    def clean(self):
        if self.window.size() > 0:
            logging.warning(f'socket closed when there are unacknowledged packets')
        self.sock.close()


class Receiver(Process):
    def __init__(self, sock, peer, buffer, window, wndsize, control):
        super(Receiver, self).__init__()
        self.sock = sock
        self.peer = peer
        self.buffer = buffer
        self.sig = Event()
        self.window = window
        self.wndsize = wndsize
        self.control = control

    def stop(self):
        self.sig.set()

    def run(self):
        while not self.sig.is_set():
            raw = self.sock.recv(MAX_DRAGON_LENGTH)
            packet = DragonPacket()
            packet.parse(raw)
            logging.debug(f'RECEIVED {packet}')
            # logging.debug(f'RECEIVED binary : {raw}')
            if packet.is_ack():
                # to do: set window size
                self.control.set()
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
        self.wndsize = Value('i', 500)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.peer = (self.remote_ip, self.remote_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout = 0.2  # 500 ms

        ShrimpManager.register('SendBuffer', SendBuffer, exposed=None)
        ShrimpManager.register('RecvBuffer', RecvBuffer, exposed=None)
        ShrimpManager.register('ShrimpWindow', ShrimpWindow, exposed=None)
        self.manager = ShrimpManager()
        self.manager.start()

        self.sender_buffer = self.manager.SendBuffer()
        self.receiver_buffer = self.manager.RecvBuffer()
        self.window = self.manager.ShrimpWindow()
        self.resender = RepeatedTask(self.timeout, self.resend)

        self.sender = Sender(self.sock, self.peer, self.sender_buffer, self.window, self.wndsize)
        self.receiver = Receiver(self.sock, self.peer, self.receiver_buffer, self.window, self.wndsize, self.resender.rtimer.reset)
        self.sender.start()
        self.receiver.start()
        self.resender.start()

    def resend(self):
        if self.window.size() > 0:
            logging.debug(f"RESEND")
            binary = self.window.get_min()
            self.sock.sendto(binary, self.peer)
            logging.debug(f'resend')

    def connect(self):
        pass

    def bind(self, addr: tuple):
        self.accept_host, self.local_port = addr
        self.sock.bind(addr)

    def send(self, data: bytes):
        self.sender_buffer.push(data)
        while not self.sender_buffer.empty() or self.window.size() > 0:
            pass
        return

    def recv(self, size: int):
        return bytes(self.receiver_buffer.get_copy(size))

    def close(self):
        self.sender.stop()
        self.receiver.terminate()
        self.resender.stop()
        self.sock.close()
