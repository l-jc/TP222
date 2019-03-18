class Buffer(object):
    def __init__(self):
        # start and end seq number
        self.content = bytearray(0)
        self.start = 0  # what should be the initial value of seq?
        self.end = 0

    def get(self, size: int) -> bytes:
        while len(self.content) == 0:
            pass
        d = self.content[:size]
        self.content = self.content[size:]
        return d

    def empty(self):
        return len(self.content) == 0


class SendBuffer(Buffer):
    def __init__(self):
        super(SendBuffer, self).__init__()

    def push(self, data: bytes):
        self.content += data


class RecvBuffer(Buffer):
    def __init__(self):
        super(RecvBuffer, self).__init__()

    def insert(self, seq: int, data: bytes):
        if seq >= self.end:
            self.content += bytes(seq-self.end) + data
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
