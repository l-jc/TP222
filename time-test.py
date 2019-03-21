from packet import DragonPacket
import time


def main():

    start = time.time()
    for i in range(100):
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
        data = bytearray(1500)
        packet.populate(data)
        binary = packet.tobytes()
        binary += b''


