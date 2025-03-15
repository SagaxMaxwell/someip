__all__ = ["IPv4Option"]


import ipaddress
from bitarray import bitarray
from bitarray.util import ba2int


class IPv4Option:
    """Represents an IPv4 option field with necessary attributes and methods
    for encoding and decoding."""

    __slots__ = (
        "__type",
        "__discardable_flag",
        "__ipv4_address",
        "__transport_protocol",
        "__transport_protocol_port_number",
    )

    def __init__(
        self,
        type: int,
        discardable_flag: bitarray,
        ipv4_address: str,
        transport_protocol: int,
        transport_protocol_port_number: int,
    ) -> None:
        """Initializes an IPv4Option instance.

        Args:
            type (int): Type of the IPv4 option.
            discardable_flag (bitarray): A 1-bit flag indicating if the option
                is discardable.
            ipv4_address (str): The IPv4 address in string format (e.g., '192.168.0.1').
            transport_protocol (int): Transport protocol number (e.g., 6 for TCP).
            transport_protocol_port_number (int): The transport protocol port number.

        Raises:
            ValueError: If any argument does not conform to the expected format or range.
        """
        self.__validate_bit("Type", type, 8)
        self.__validate_bit("Discardable Flag", discardable_flag, 1)
        self.__validate_bit("Transport Protocol", transport_protocol, 8)
        self.__validate_bit(
            "Transport Protocol Port Number", transport_protocol_port_number, 16
        )
        self.__validate_ipv4_address(ipv4_address)

        self.__type = type
        self.__discardable_flag = discardable_flag
        self.__ipv4_address = ipv4_address
        self.__transport_protocol = transport_protocol
        self.__transport_protocol_port_number = transport_protocol_port_number

    @property
    def type(self) -> int:
        """Returns the type of the IPv4 option."""
        return self.__type

    @property
    def discardable_flag(self) -> bitarray:
        """Returns the discardable flag of the IPv4 option."""
        return self.__discardable_flag

    @property
    def ipv4_address(self) -> str:
        """Returns the IPv4 address as a string."""
        return self.__ipv4_address

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
        """Returns the fixed length of the IPv4 option (0x0009)."""
        return 0x0009

    def encode(self) -> bytes:
        """Encodes the IPv4 option into a byte sequence.

        Returns:
            bytes: The encoded byte representation of the IPv4 option.
        """
        packet = bitarray()
        for feild, bits in zip(
            (
                self.length,
                self.type,
                self.discardable_flag,
                bitarray("0" * 7),
                self.ipv4_address,
                bitarray("0" * 8),
                self.transport_protocol,
                self.transport_protocol_port_number,
            ),
            (16, 8, 1, 7, 32, 8, 8, 16),
        ):
            if isinstance(feild, bitarray):
                packet.extend(feild)
            elif isinstance(feild, int):
                packet.frombytes(feild.to_bytes(bits // 8, "big"))
            elif isinstance(feild, str):
                packet.frombytes(ipaddress.ip_address(feild).packed)
        return packet.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "IPv4Option":
        """Decodes a byte sequence into an IPv4Option object.

        Args:
            series (bytes): The byte sequence to decode.

        Returns:
            IPv4Option: The decoded IPv4Option object.

        Raises:
            ValueError: If the length of the byte sequence is invalid.
        """
        if len(series) != 12:
            raise ValueError("Invalid ipv4 Option length")
        packet = bitarray()
        packet.frombytes(series)
        type = ba2int(packet[16:24])
        discardable_flag = packet[24:25]
        ipv4_address = ipaddress.IPv4Address(packet[32:64].tobytes())
        transport_protocol = ba2int(packet[72:80])
        transport_protocol_port_number = ba2int(packet[80:96])
        return cls(
            type,
            discardable_flag,
            ipv4_address,
            transport_protocol,
            transport_protocol_port_number,
        )

    @staticmethod
    def __validate_bit(name: str, value: int | bitarray, bits: int) -> None:
        """Validates that a value fits within a specified bit size.

        Args:
            name (str): The name of the value being validated.
            value (int | bitarray): The value to validate.
            bits (int): The number of bits the value should occupy.

        Raises:
            ValueError: If the value does not fit within the specified bit range.
        """
        if isinstance(value, int):
            max_value = (1 << bits) - 1
            if not (0 <= value <= max_value):
                raise ValueError(f"{name} must be a {bits}-bit unsigned integer")
        elif isinstance(value, bitarray):
            if len(value) != bits:
                raise ValueError(f"{name} must be a {bits}-bit bitarray")

    @staticmethod
    def __validate_ipv4_address(ipv4_address: str) -> None:
        """Validates that the given string is a valid IPv4 address.

        Args:
            ipv4_address (str): The IPv4 address to validate.

        Raises:
            ValueError: If the provided string is not a valid IPv4 address.
        """
        if ipaddress.ip_address(ipv4_address).version != 4:
            raise ValueError("Invalid ipv4 address")

    def __repr__(self) -> str:
        """Returns a string representation of the IPv4Option object."""
        return "\n".join(
            (
                f"{'length':<32}: 0x{self.length:04X}",
                f"{'type':<32}: 0x{self.type:02X}",
                f"{'discardable flag':<32}: {self.discardable_flag}",
                f"{'ipv4 address':<32}: {self.ipv4_address}",
                f"{'transport protocol':<32}: 0x{self.transport_protocol:02X}",
                f"{'transport protocol port number':<32}: 0x{self.transport_protocol_port_number:04X}",
            )
        )
