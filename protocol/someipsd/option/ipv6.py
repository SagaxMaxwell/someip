__all__ = ["IPv6"]


import ipaddress

from bitarray import bitarray
from bitarray.util import ba2int, int2ba

from protocol.someipsd.option.length import Length
from utils.series_reader import SeriesReader


class IPv6:
    """Represents an IPv6 option field with necessary attributes and methods
    for encoding and decoding."""

    __slots__ = (
        "__type",
        "__discardable_flag",
        "__bit_1_to_bit_7",
        "__ipv6_address",
        "__reserved",
        "__transport_protocol",
        "__transport_protocol_port_number",
    )

    def __init__(
        self,
        type: int,
        discardable_flag: bitarray,
        bit_1_to_bit_7: bitarray,
        ipv6_address: str,
        reserved: int,
        transport_protocol: int,
        transport_protocol_port_number: int,
    ) -> None:
        self.__type = type
        self.__discardable_flag = discardable_flag
        self.__bit_1_to_bit_7 = bit_1_to_bit_7
        self.__ipv6_address = ipv6_address
        self.__reserved = reserved
        self.__transport_protocol = transport_protocol
        self.__transport_protocol_port_number = transport_protocol_port_number

    @property
    def type(self) -> int:
        """Returns the type of the IPv6 option."""
        return self.__type

    @property
    def discardable_flag(self) -> bitarray:
        """Returns the discardable flag of the IPv6 option."""
        return self.__discardable_flag

    @property
    def bit_1_to_bit_7(self) -> bitarray:
        """Returns the bits 1 to 7 of the IPv6 option."""
        return self.__bit_1_to_bit_7

    @property
    def ipv6_address(self) -> str:
        """Returns the IPv6 address as a string."""
        return self.__ipv6_address

    @property
    def reserved(self) -> int:
        """Returns the reserved field of the IPv6 option."""
        return self.__reserved

    @property
    def transport_protocol(self) -> int:
        """Returns the transport protocol number."""
        return self.__transport_protocol

    @property
    def transport_protocol_port_number(self) -> int:
        """Returns the transport protocol port number."""
        return self.__transport_protocol_port_number

    @property
    def length(self) -> int:
        """Returns the fixed length of the IPv6 option (0x0015)."""
        return 0x0015

    @staticmethod
    def expected_packet_length() -> int:
        """Returns the expected length of the IPv6 option packet.

        Returns:
            int: The expected length of the IPv6 option packet.
        """
        length = sum(
            (
                Length.LENGTH,
                Length.TYPE,
                Length.DISCARDABLE_FLAG,
                Length.BIT_1_TO_BIT_7,
                Length.IPV6_ADDRESS,
                Length.RESERVED,
                Length.TRANSPORT_PROTOCOL,
                Length.TRANSPORT_PROTOCOL_PORT_NUMBER,
            )
        )
        return length

    def encode(self) -> bytes:
        """Encodes the IPv6 option into a byte sequence.

        Returns:
            bytes: The encoded byte representation of the IPv6 option.
        """
        series = bitarray()
        series += int2ba(self.length, length=Length.LENGTH)
        series += int2ba(self.type, length=Length.TYPE)
        series += self.discardable_flag
        series += self.bit_1_to_bit_7
        series.frombytes(ipaddress.ip_address(self.ipv6_address).packed)
        series += int2ba(self.reserved, length=Length.RESERVED)
        series += int2ba(self.transport_protocol, length=Length.TRANSPORT_PROTOCOL)
        series += int2ba(
            self.transport_protocol_port_number,
            length=Length.TRANSPORT_PROTOCOL_PORT_NUMBER,
        )

        return series.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "IPv6":
        """Decodes a byte sequence into an IPv6 object.

        Args:
            series (bytes): The byte sequence to decode.

        Returns:
            IPv6: The decoded IPv6 object.

        Raises:
            ValueError: If the length of the byte sequence is invalid.
        """
        packet = bitarray()
        packet.frombytes(series)

        if len(packet) != cls.expected_packet_length():
            raise ValueError("Invalid message length")

        reader = SeriesReader(packet)
        _ = reader.read(Length.LENGTH)
        type_ = ba2int(reader.read(Length.TYPE))
        discardable_flag = reader.read(Length.DISCARDABLE_FLAG)
        bit_1_to_bit_7 = reader.read(Length.BIT_1_TO_BIT_7)
        ipv6_address = str(
            ipaddress.ip_address(reader.read(Length.IPV6_ADDRESS).tobytes())
        )
        reserved = ba2int(reader.read(Length.RESERVED))
        transport_protocol = ba2int(reader.read(Length.TRANSPORT_PROTOCOL))
        transport_protocol_port_number = ba2int(
            reader.read(Length.TRANSPORT_PROTOCOL_PORT_NUMBER)
        )

        return cls(
            type=type_,
            discardable_flag=discardable_flag,
            bit_1_to_bit_7=bit_1_to_bit_7,
            ipv6_address=ipv6_address,
            reserved=reserved,
            transport_protocol=transport_protocol,
            transport_protocol_port_number=transport_protocol_port_number,
        )

    def __repr__(self) -> str:
        """Returns a string representation of the IPv6 object."""
        return "\n".join(
            (
                f"{'length':<32}: {self.length}",
                f"{'type':<32}: {self.type}",
                f"{'discardable flag':<32}: {self.discardable_flag}",
                f"{'bit 1 to bit 7':<32}: {self.bit_1_to_bit_7}",
                f"{'ipv6 address':<32}: {self.ipv6_address}",
                f"{'reserved':<32}: {self.reserved}",
                f"{'transport protocol':<32}: {self.transport_protocol}",
                f"{'transport protocol port number':<32}: {self.transport_protocol_port_number}",
            )
        )
