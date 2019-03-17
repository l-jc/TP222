import socket
import buffer
import threading


class SendingProcess(threading.Thread):
    def __init__(self):
        """
        has access to the sending buffer
        """
        super(SendingProcess, self).__init__()
        pass

    def run(self):
        """
        keep reading from sending buffer and send
        :return:
        """
        pass


class ReceivingProcess(threading.Thread):
    def __init__(self):
        """
        has access to receiving buffer
        """
        super(ReceivingProcess, self).__init__()
        pass

    def run(self):
        """
        keep receiving and writes to receiving buffer
        :return:
        """
        pass


class Dragon:
    remote_addr = None
    remote_port = None

    def __init__(self):
        """
        sending buffer
        receiving buffer
        sending routine
        receiving routine
        """
        self.send_buffer = buffer.SendBuffer()
        self.send_routine = SendingProcess()
        self.recv_buffer = buffer.RecvBuffer()
        self.recv_routine = ReceivingProcess()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect(self, addr: tuple):
        """
        synchronization between two end hosts
        :return:
        """
        self.remote_addr = addr[0]
        self.remote_port = addr[1]
        # connect...
        pass

    def send(self, data: bytes):
        self.send_buffer.push(data)

    def recv(self, size: int):
        return self.recv_buffer.get(size)

    def close(self):
        pass
