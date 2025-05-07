__all__ = ["Packet"]


from bitarray import bitarray
from bitarray.util import ba2int, int2ba

from protocol.someip.length import Length
from utils.bit_reader import BitReader


class Packet:
    """
    Completely immutable design for SOME/IP packet.

    Attributes:
        service_id (int): The service ID.
        method_id (int): The method ID.
        client_id (int): The client ID.
        session_id (int): The session ID.
        protocol_version (int): The protocol version.
        interface_version (int): The interface version.
        message_type (int): The message type.
        return_code (int): The return code.
        payload (bytes): The payload.

    Methods:
        encode(): Encode the packet to bytes.
        decode(series: bytes) -> Packet: Decode the packet from bytes.
    """

    __slots__ = (
        "__service_id",
        "__method_id",
        "__client_id",
        "__session_id",
        "__protocol_version",
        "__interface_version",
        "__message_type",
        "__return_code",
        "__payload",
    )

    def __init__(
        self,
        service_id: int,
        method_id: int,
        client_id: int,
        session_id: int,
        protocol_version: int,
        interface_version: int,
        message_type: int,
        return_code: int,
        payload: bytes,
    ) -> None:
        """Initializes the Packet with the provided attributes.

        Args:
            service_id (int): The service ID.
            method_id (int): The method ID.
            client_id (int): The client ID.
            session_id (int): The session ID.
            protocol_version (int): The protocol version.
            interface_version (int): The interface version.
            message_type (int): The message type.
            return_code (int): The return code.
            payload (bytes): The payload.
        """

        self.__service_id = service_id
        self.__method_id = method_id
        self.__client_id = client_id
        self.__session_id = session_id
        self.__protocol_version = protocol_version
        self.__interface_version = interface_version
        self.__message_type = message_type
        self.__return_code = return_code
        self.__payload = bytes(payload)

    @property
    def service_id(self) -> int:
        """Returns the service ID."""
        return self.__service_id

    @property
    def method_id(self) -> int:
        """Returns the method ID."""
        return self.__method_id

    @property
    def client_id(self) -> int:
        """Returns the client ID."""
        return self.__client_id

    @property
    def session_id(self) -> int:
        """Returns the session ID."""
        return self.__session_id

    @property
    def protocol_version(self) -> int:
        """Returns the protocol version."""
        return self.__protocol_version

    @property
    def interface_version(self) -> int:
        """Returns the interface version."""
        return self.__interface_version

    @property
    def message_type(self) -> int:
        """Returns the message type."""
        return self.__message_type

    @property
    def return_code(self) -> int:
        """Returns the return code."""
        return self.__return_code

    @property
    def payload(self) -> bytes:
        """Returns the payload."""
        return self.__payload

    @property
    def length(self) -> int:
        """Returns the total length of the packet (header + payload)."""
        return Packet.expected_header_length() // 8 + len(self.payload)

    @staticmethod
    def expected_header_length() -> int:
        """Returns the length of the header."""
        length = sum(
            (
                Length.SERVICE_ID,
                Length.METHOD_ID,
                Length.LENGTH,
                Length.CLIENT_ID,
                Length.SESSION_ID,
                Length.PROTOCOL_VERSION,
                Length.INTERFACE_VERSION,
                Length.MESSAGE_TYPE,
                Length.RETURN_CODE,
            )
        )
        return length

    def encode(self) -> bytes:
        """Encodes the packet into a byte sequence.

        Returns:
            bytes: The encoded packet.
        """
        series = bitarray()
        series += int2ba(self.service_id, length=Length.SERVICE_ID)
        series += int2ba(self.method_id, length=Length.METHOD_ID)
        series += int2ba(self.length, length=Length.LENGTH)
        series += int2ba(self.client_id, length=Length.CLIENT_ID)
        series += int2ba(self.session_id, length=Length.SESSION_ID)
        series += int2ba(self.protocol_version, length=Length.PROTOCOL_VERSION)
        series += int2ba(self.interface_version, length=Length.INTERFACE_VERSION)
        series += int2ba(self.message_type, length=Length.MESSAGE_TYPE)
        series += int2ba(self.return_code, length=Length.RETURN_CODE)

        return series.tobytes() + self.payload

    @classmethod
    def decode(cls, series: bytes) -> "Packet":
        """Decodes the packet from a byte sequence using bitarray.

        Args:
            series (bytes): The byte sequence representing the packet.

        Returns:
            Packet: The decoded Packet object.

        Raises:
            ValueError: If the packet header is invalid.
        """
        bits = bitarray()
        bits.frombytes(series)

        if len(bits) < cls.expected_header_length():
            raise ValueError("Invalid SOME/IP header length")

        reader = BitReader(bits)
        service_id = reader.read(Length.SERVICE_ID)
        method_id = reader.read(Length.METHOD_ID)
        _ = reader.read(Length.LENGTH)
        client_id = reader.read(Length.CLIENT_ID)
        session_id = reader.read(Length.SESSION_ID)
        protocol_version = reader.read(Length.PROTOCOL_VERSION)
        interface_version = reader.read(Length.INTERFACE_VERSION)
        message_type = reader.read(Length.MESSAGE_TYPE)
        return_code = reader.read(Length.RETURN_CODE)
        payload = bits[reader.index :]

        return cls(
            service_id=ba2int(service_id),
            method_id=ba2int(method_id),
            client_id=ba2int(client_id),
            session_id=ba2int(session_id),
            protocol_version=ba2int(protocol_version),
            interface_version=ba2int(interface_version),
            message_type=ba2int(message_type),
            return_code=ba2int(return_code),
            payload=payload.tobytes(),
        )

    def __repr__(self) -> str:
        """Returns a string representation of the Packet object."""
        return "\n".join(
            (
                f"{'service id':<24}: {self.service_id}",
                f"{'method id':<24}: {self.method_id}",
                f"{'length':<24}: {self.length}",
                f"{'client id':<24}: {self.client_id}",
                f"{'session id':<24}: {self.session_id}",
                f"{'protocol version':<24}: {self.protocol_version}",
                f"{'interface version':<24}: {self.interface_version}",
                f"{'message type':<24}: {self.message_type}",
                f"{'return code':<24}: {self.return_code}",
                f"{'payload':<24}: {self.payload}",
            )
        )
