
class DragonPacket:
    flags = dict()

    def __int__(self, payload):
        pass

    def is_ack(self):
        return self.flags['ack'] == 1

    def toBytes(self):
        """
        :return: the bytes format of the packet
        """
        pass

    def parse(self, raw: bytes):
        """
        parse packets
        :param raw: bytes
        :return:
        """
        pass

