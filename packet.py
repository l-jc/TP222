"""
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
          Sequence Number
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        Acknowledge Number
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
Length | flags | window or credit
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""
from bitarray import bitarray


class DragonPacket:
    flags = {
        'ack': False,
        'syn': False,
        'fin': False,
        'cre': True,
        'fec': False,
        'ooo': False,
    }
    seqno = 0
    ackno = 0
    headerlen = 12
    wndsize = 100
    credit = 0
    payload = b''

    def __int__(self):
        pass

    def populate(self, payload: bytes):
        self.payload = payload

    def is_ack(self):
        return self.flags['ack'] is True

    def use_credit(self):
        return self.flags['cre'] is True

    def tobytes(self):
        """
        :return: the bytes format of the packet
        """
        fs = bitarray('00000000')
        fs[0] = self.flags['syn']
        fs[1] = self.flags['fin']
        fs[2] = self.flags['ack']
        fs[3] = self.flags['cre']
        fs[4] = self.flags['fec']
        fs[5] = self.flags['ooo']
        header = self.seqno.to_bytes(4, 'big') + self.ackno.to_bytes(4, 'big') + self.headerlen.to_bytes(1, 'big') + fs.tobytes()
        if self.flags['cre']:
            header += self.credit.to_bytes(2, 'big')
        else:
            header += self.wndsize.to_bytes(2, 'big')
        assert(len(header) == self.headerlen)
        return header + self.payload

    def parse(self, raw: bytes):
        """
        parse packets
        :param raw: bytes
        :return:
        """
        self.seqno = int.from_bytes(raw[:4], 'big')
        self.ackno = int.from_bytes(raw[4:8], 'big')
        self.headerlen = int.from_bytes(raw[8:9], 'big')
        fs = bitarray()
        fs.frombytes(raw[9:10])
        self.flags['syn'] = fs[0]
        self.flags['fin'] = fs[1]
        self.flags['ack'] = fs[2]
        self.flags['cre'] = fs[3]
        self.flags['fec'] = fs[4]
        self.flags['ooo'] = fs[5]
        if self.flags['cre']:
            self.credit = int.from_bytes(raw[10:12], 'big')
        else:
            self.wndsize = int.from_bytes(raw[10:12], 'big')
        self.payload = raw[12:]
        return

    def __str__(self):
        return f"seqno: {self.seqno} " \
            f"ackno: {self.ackno} " \
            f"ack_f: {self.flags['ack']} " \
            f"len payload: {len(self.payload)}"

