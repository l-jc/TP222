class ShrimpWindow():
    def __init__(self):
        self.packets = dict()

    def get(self, expno):
        return self.packets[expno]

    def put(self, expno, packet):
        self.packets[expno] = packet

    def pop(self, expno):
        self.packets.pop(expno)

    def size(self):
        return len(self.packets)

    def items(self):
        return self.packets.items()

