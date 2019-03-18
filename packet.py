"""
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
          Sequence Number
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        Acknowledge Number
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
Length | flags | window or credit
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""


class DragonPacket:
    flags = {
        'ack': False,
        'syn': False,
        'fin': False,
        'cre': True,
        'fec': False,
    }
    seqno = None
    ackno = None
    headerlen = 12
    wndsize = None
    credit = None

    def __int__(self):
        pass

    def populate(self, **kwargs):
        pass

    def is_ack(self):
        return self.flags['ack'] is True

    def use_credit(self):
        return self.flags['cre'] is True

    def toBytes(self, payload: bytes):
        """
        :return: the bytes format of the packet
        """
        fs = bytearray(8)
        fs[0] = self.flags['syn']
        fs[1] = self.flags['fin']
        fs[2] = self.flags['ack']
        fs[3] = self.flags['cre']
        fs[4] = self.flags['fec']
        header = self.seqno.to_bytes(4, 'big') + self.ackno.to_bytes(4, 'big') + self.headerlen.to_bytes(1,
                                                                                                         'big') + fs + \
                 self.credit.to_bytes(2, 'big') if self.flags['cre'] else self.wndsize.to_bytes(1, 'big')

        return header + payload

    def parse(self, raw: bytes):
        """
        parse packets
        :param raw: bytes
        :return:
        """
        self.seqno = int.from_bytes(raw[:4], 'big')
        self.ackno = int.from_bytes(raw[4:8], 'big')
        self.headerlen = int.from_bytes(raw[8:9], 'big')
        fs = raw[9:10]
        self.flags['syn'] = fs[0]
        self.flags['fin'] = fs[1]
        self.flags['ack'] = fs[2]
        self.flags['cre'] = fs[3]
        self.flags['fec'] = fs[4]
        if self.flags['cre']:
            self.credit = int.from_bytes(raw[10:12], 'big')
        else:
            self.wndsize = int.from_bytes(raw[10:12], 'big')
