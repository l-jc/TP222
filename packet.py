class DragonPacket:
    flags = {
        'ack': False,
    }
    seq = None

    def __int__(self):
        pass

    def is_ack(self):
        return self.flags['ack'] is True

    def toBytes(self):
        """
        :return: the bytes format of the packet
        """
        return bytearray(b"fake packet")

    def parse(self, raw: bytes):
        """
        parse packets
        :param raw: bytes
        :return:
        """
        pass
