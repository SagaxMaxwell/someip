__all__ = ["Packet"]


from bitarray import bitarray
from bitarray.util import ba2int


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
        entries_array: bytes,
        options_array: bytes,
    ):
        self.__validate_bit("Service ID", service_id, 16)
        self.__validate_bit("Method ID", method_id, 16)
        self.__validate_bit("Client ID", client_id, 16)
        self.__validate_bit("Session ID", session_id, 16)
        self.__validate_bit("Protocol Version", protocol_version, 8)
        self.__validate_bit("Interface Version", interface_version, 8)
        self.__validate_bit("Message Type", message_type, 8)
        self.__validate_bit("Return Code", return_code, 8)
        self.__validate_bit("Flags", flags, 8)
        self.__service_id = service_id
        self.__method_id = method_id
        self.__client_id = client_id
        self.__session_id = session_id
        self.__protocol_version = protocol_version
        self.__interface_version = interface_version
        self.__message_type = message_type
        self.__return_code = return_code
        self.__flags = flags
        self.__entries_array = bytes(entries_array)
        self.__options_array = bytes(options_array)

    @property
    def service_id(self) -> int:
        return self.__service_id

    @property
    def method_id(self) -> int:
        return self.__method_id

    @property
    def client_id(self) -> int:
        return self.__client_id

    @property
    def session_id(self) -> int:
        return self.__session_id

    @property
    def protocol_version(self) -> int:
        return self.__protocol_version

    @property
    def interface_version(self) -> int:
        return self.__interface_version

    @property
    def message_type(self) -> int:
        return self.__message_type

    @property
    def return_code(self) -> int:
        return self.__return_code

    @property
    def flags(self) -> int:
        return self.__flags

    @property
    def entries_array(self) -> bytes:
        return self.__entries_array

    @property
    def options_array(self) -> bytes:
        return self.__options_array

    @property
    def length_of_entries_array(self) -> int:
        return len(self.entries_array)

    @property
    def length_of_options_array(self) -> int:
        return len(self.options_array)

    @property
    def length(self) -> int:
        return 20 + self.length_of_entries_array + self.length_of_options_array

    def encode(self) -> bytes:
        packet = bitarray()
        for field, bits in zip(
            (
                self.service_id,
                self.method_id,
                self.length,
                self.client_id,
                self.session_id,
                self.protocol_version,
                self.interface_version,
                self.message_type,
                self.return_code,
                self.flags,
                bitarray("0" * 24),
                self.length_of_entries_array,
                self.entries_array,
                self.length_of_options_array,
                self.options_array,
            ),
            (16, 16, 32, 16, 16, 8, 8, 8, 8, 8, 24, 32, 0, 32, 0),
        ):
            if isinstance(field, int):
                packet.frombytes(field.to_bytes(bits // 8, "big"))
            elif isinstance(field, bitarray) and len(field) == bits:
                packet.extend(field)
            elif isinstance(field, bytes):
                packet.frombytes(field)
        return packet.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "Packet":
        if len(series) != 28:
            raise ValueError("Invalid entry length")
        packet = bitarray()
        packet.frombytes(series)

        # compute base fields
        service_id = ba2int(packet[:16])
        method_id = ba2int(packet[16:32])
        client_id = ba2int(packet[64:80])
        session_id = ba2int(packet[80:96])
        protocol_version = ba2int(packet[96:104])
        interface_version = ba2int(packet[104:112])
        message_type = ba2int(packet[112:120])
        return_code = ba2int(packet[120:128])
        flags = ba2int(packet[128:136])

        # compute length of entries array
        start = 160
        end = 192
        length_of_entries_array = ba2int(packet[start:end])

        # compute entries array
        start = end
        end += length_of_entries_array
        entries_array = packet[start:end].tobytes()

        # compute length of options array
        start = end
        end += 32
        length_of_options_array = ba2int(packet[start:end])

        # compute options array
        start = end
        end += length_of_options_array
        options_array = packet[start:end].tobytes()

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
            entries_array=entries_array,
            options_array=options_array,
        )

    @staticmethod
    def __validate_bit(name: str, value: int, bits: int) -> None:
        max_value = (1 << bits) - 1
        if not (0 <= value <= max_value):
            raise ValueError(f"{name} must be a {bits}-bit unsigned integer")

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"{'service id':<32}: 0x{self.service_id:04X}",
                f"{'method id':<32}: 0x{self.method_id:04X}",
                f"{'client id':<32}: 0x{self.client_id:04X}",
                f"{'session id':<32}: 0x{self.session_id:04X}",
                f"{'protocol version':<32}: 0x{self.protocol_version:02X}",
                f"{'interface version':<32}: 0x{self.interface_version:02X}",
                f"{'message type':<32}: 0x{self.message_type:02X}",
                f"{'return code':<32}: 0x{self.return_code:02X}",
                f"{'flags':<32}: 0x{self.flags:02X}",
                f"{'entries array':<32}: {self.entries_array}",
                f"{'options array':<32}: {self.options_array}",
            )
        )
