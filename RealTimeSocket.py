import socket
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


class Dragon():
    def __init__(self):
        """
        sending buffer
        receiving buffer
        sending routine
        receiving routine
        """
        pass

    def connect(self):
        """
        synchronization between two end hosts
        :return:
        """
        pass

    def send(self, data: bytes):
        pass

    def recv(self, size: int):
        pass
