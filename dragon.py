import socket
import multiprocessing
from buffer import SendBuffer, RecvBuffer

MAX_DRAGON_LENGTH = 2048
MAX_DRAGON_PAYLOAD = 1280


class Sender(multiprocessing.Process):
    def __init__(self):
        super(Sender, self).__init__()

    def run(self):
        pass


class Receiver(multiprocessing.Process):
    def __init__(self):
        super(Receiver, self).__init__()

    def run(self):
        pass


class Dragon:
    local_port = None
    accept_host = None

    def __init__(self):
        self.credit = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sbuffer = SendBuffer()
        self.rbuffer = RecvBuffer()

        self.sender = Sender()
        self.receiver = Receiver()

    def bind(self, addr: tuple):
        self.accept_host, self.local_port = addr
        self.sock.bind(addr)

    def send(self, data: bytes):
        self.sbuffer.push(data)

    def recv(self, size: int):
        return self.rbuffer.get(size)

