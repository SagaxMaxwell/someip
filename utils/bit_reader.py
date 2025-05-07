__all__ = ["BitReader"]


class BitReader:
    def __init__(self, bits):
        self.bits = bits
        self.index = 0

    def read(self, length):
        value = self.bits[self.index : self.index + length]
        self.index += length
        return value
