import socket
import multiprocessing
import threading
import time
import functools

PACKET_SIZE = 60000
SEG_SIZE = 16384


class TransportSocket:
    def __init__(self, addr: str, port: int):
        self.remote_addr = addr
        self.remote_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __del__(self):
        self.close()

    def bind(self, port):
        self.sock.bind(('', port))

    def close(self):
        self.sock.close()


class RealTimeSocket(TransportSocket):
    def __init__(self, addr: str, port: int):
        super(RealTimeSocket, self).__init__(addr, port)
        self.seq = 0
        self.seg = 0

    def sync(self):
        """
        synchronize with remote host
        :return: None
        """
        return

    def send(self, data: bytes):
        k = 0
        i = 0
        payload = data[k : k + SEG_SIZE]
        n = len(data) // SEG_SIZE
        while payload:
            header = i.to_bytes(4, 'big') + n.to_bytes(4, 'big')
            pkt = header + payload
            self.sock.sendto(pkt, (self.remote_addr, self.remote_port))
            i += 1
            k += SEG_SIZE
            payload = data[k : k + SEG_SIZE]
            # need some kind of flow control to prevent overwhelm receiver buffer (udp buffer)
            if i % 50 == 0:
                time.sleep(0.001)

        return len(data)

    def recv(self, max_waiting_time: float):
        """
        :param max_waiting_time: deadline to put content into buffer
        :return: partial or complete
        """
        def receiver(recv_buffer):
            while True:
                pkt = self.sock.recv(PACKET_SIZE)
                header = pkt[:8]
                i = int.from_bytes(header[0:4], 'big')
                n = int.from_bytes(header[4:8], 'big')
                payload = pkt[8:]
                recv_buffer.append((header, payload))
                if i == n:
                    print("break")
                    break
            return 0

        manager = multiprocessing.Manager()
        buffer = manager.list()

        p_recv = multiprocessing.Process(target=receiver, args=(buffer, ))
        p_recv.start()

        timer = threading.Timer(max_waiting_time, p_recv.terminate)
        timer.start()

        p_recv.join()
        timer.cancel()
        # if p_recv.exitcode != 0:
        #     print("partial data")
        # else:
        #     print("complete data")

        buffer.sort()
        buffer = [x[1] for x in buffer]
        if len(buffer) == 0:
            return None
        else:
            return functools.reduce((lambda x, y: x + y), buffer)
