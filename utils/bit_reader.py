__all__ = ["BitReader"]


from bitarray import bitarray


class BitReader:
    def __init__(self, bits: bitarray) -> None:
        self.__bits = bits
        self.__index = 0

    @property
    def bits(self) -> bitarray:
        return self.__bits

    @property
    def index(self) -> int:
        return self.__index

    @index.setter
    def index(self, value: int) -> None:
        if value < 0 or value > len(self.bits):
            raise ValueError("Index out of range")
        self.__index = value

    def read(self, length: int) -> bitarray:
        value = self.bits[self.index : self.index + length]
        self.index += length
        return value
