__all__ = ["Packet"]


from bitarray import bitarray
from bitarray.util import ba2int, int2ba

from protocol.someipsd.length import Length
from utils.series_reader import SeriesReader


class Packet:

    __slots__ = (
        "__service_id",
        "__method_id",
        "__client_id",
        "__session_id",
        "__protocol_version",
        "__interface_version",
        "__message_type",
        "__return_code",
        "__flags",
        "__reserved",
        "__entries_array",
        "__options_array",
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
        flags: int,
        reserved: int,
        entries_array: bytes,
        options_array: bytes,
    ):
        self.__service_id = service_id
        self.__method_id = method_id
        self.__client_id = client_id
        self.__session_id = session_id
        self.__protocol_version = protocol_version
        self.__interface_version = interface_version
        self.__message_type = message_type
        self.__return_code = return_code
        self.__flags = flags
        self.__reserved = reserved
        self.__entries_array = bytes(entries_array)
        self.__options_array = bytes(options_array)

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
    def flags(self) -> int:
        """Returns the flags."""
        return self.__flags

    @property
    def reserved(self) -> int:
        """Returns the reserved field."""
        return self.__reserved

    @property
    def length_of_entries_array(self) -> int:
        """Returns the length of the entries array."""
        return len(self.entries_array)

    @property
    def entries_array(self) -> bytes:
        """Returns the entries array."""
        return self.__entries_array

    @property
    def length_of_options_array(self) -> int:
        """Returns the length of the options array."""
        return len(self.options_array)

    @property
    def options_array(self) -> bytes:
        """Returns the options array."""
        return self.__options_array

    @property
    def length(self) -> int:
        """Returns the total length of the packet including headers and arrays."""
        return (
            Packet.expected_minimum_length() // 8
            + self.length_of_entries_array
            + self.length_of_options_array
        )

    @staticmethod
    def expected_minimum_length() -> int:
        """Returns the expected length of the packet.

        Returns:
            int: The expected length of the packet in bytes.
        """
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
                Length.FLAGS,
                Length.RESERVED,
            )
        )
        return length

    def encode(self) -> bytes:
        """Encodes the packet into a byte sequence.

        Returns:
            bytes: The encoded byte sequence representing the packet.
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
        series += int2ba(self.flags, length=Length.FLAGS)
        series += int2ba(self.reserved, length=Length.RESERVED)
        series += int2ba(
            self.length_of_entries_array, length=Length.LENGTH_OF_ENTRIES_ARRAY
        )
        series.frombytes(self.entries_array)
        series += int2ba(
            self.length_of_options_array, length=Length.LENGTH_OF_OPTIONS_ARRAY
        )
        series.frombytes(self.options_array)

        return series.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "Packet":
        """Decodes a byte sequence into a Packet object.

        Args:
            series (bytes): The byte sequence representing the packet.

        Returns:
            Packet: The decoded Packet object.

        Raises:
            ValueError: If the byte sequence is of invalid length.
        """
        packet = bitarray()
        packet.frombytes(series)

        if len(packet) < cls.expected_minimum_length():
            raise ValueError("Invalid SOME/IP SD minimum length")

        reader = SeriesReader(packet)
        service_id = ba2int(reader.read(Length.SERVICE_ID))
        method_id = ba2int(reader.read(Length.METHOD_ID))
        _ = ba2int(reader.read(Length.LENGTH))
        client_id = ba2int(reader.read(Length.CLIENT_ID))
        session_id = ba2int(reader.read(Length.SESSION_ID))
        protocol_version = ba2int(reader.read(Length.PROTOCOL_VERSION))
        interface_version = ba2int(reader.read(Length.INTERFACE_VERSION))
        message_type = ba2int(reader.read(Length.MESSAGE_TYPE))
        return_code = ba2int(reader.read(Length.RETURN_CODE))
        flags = ba2int(reader.read(Length.FLAGS))
        reserved = ba2int(reader.read(Length.RESERVED))
        length_of_entries_array = ba2int(reader.read(Length.LENGTH_OF_ENTRIES_ARRAY))
        entries_array = reader.read(length_of_entries_array * 8).tobytes()
        length_of_options_array = ba2int(reader.read(Length.LENGTH_OF_OPTIONS_ARRAY))
        options_array = reader.read(length_of_options_array * 8).tobytes()

        return cls(
            service_id=service_id,
            method_id=method_id,
            client_id=client_id,
            session_id=session_id,
            protocol_version=protocol_version,
            interface_version=interface_version,
            message_type=message_type,
            return_code=return_code,
            flags=flags,
            reserved=reserved,
            entries_array=entries_array,
            options_array=options_array,
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
                f"{'flags':<24}: {self.flags}",
                f"{'reserved':<24}: {self.reserved}",
                f"{'length of entries array':<24}: {self.length_of_entries_array}",
                f"{'entries array':<24}: {self.entries_array}",
                f"{'length of options array':<24}: {self.length_of_options_array}",
                f"{'options array':<24}: {self.options_array}",
            )
        )
