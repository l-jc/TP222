# import logging
# logging.basicConfig(level=logging.DEBUG)


class Buffer(object):
    def __init__(self):
        # start and end seq number
        self.content = bytearray(0)
        self.start = 0  # what should be the initial value of seq?
        self.end = 0

    def get(self, size: int):
        while len(self.content) == 0:
            pass
        d = self.content[:size]
        self.content = self.content[size:]
        self.start = self.start + len(d)
        return bytes(d)

    def get_copy(self, size: int):
        while len(self.content) == 0:
            pass
        d = self.content[:size]
        return bytes(d)

    def get_seqno(self):
        return self.start

    def empty(self) -> bool:
        return len(self.content) == 0

    def size(self):
        return len(self.content)


class SendBuffer(Buffer):
    def __init__(self):
        super(SendBuffer, self).__init__()

    def push(self, data: bytes):
        self.content += data


class RecvBuffer(Buffer):
    def __init__(self):
        super(RecvBuffer, self).__init__()

    def get_start(self):
        return self.start

    def insert(self, seq: int, data: bytes):
        if seq >= self.start + len(self.content):
            self.content += bytes(seq-self.start-self.size()) + data
        elif seq >= self.start:
            self.content[seq-self.start:seq-self.start+len(data)] = data
        else:
            # drop
            pass

    def whatever(self, data: bytes):
        self.content += data


class ShrimpBytes:
    def __init__(self):
        # sequence number range.
        pass

    def replace(self, start: int, size: int, data: bytes):
        pass
