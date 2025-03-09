__all__ = ["ServiceEntry"]


from bitarray import bitarray
from bitarray.util import ba2int


class ServiceEntry:
    __slots__ = (
        "__type_field",
        "__index_first_option_run",
        "__index_second_option_run",
        "__number_of_options_1",
        "__number_of_options_2",
        "__service_id",
        "__instance_id",
        "__major_version",
        "__ttl",
        "__minor_version",
    )

    def __init__(
        self,
        type_field: int,
        index_first_option_run: int,
        index_second_option_run: int,
        number_of_options_1: bitarray,
        number_of_options_2: bitarray,
        service_id: int,
        instance_id: int,
        major_version: int,
        ttl: int,
        minor_version: int,
    ):
        self.__validate_bit("Entry Type", type_field, 8)
        self.__validate_bit("Index First Option Run", index_first_option_run, 8)
        self.__validate_bit("Index Second Option Run", index_second_option_run, 8)
        self.__validate_bit("number of Options 1", number_of_options_1, 4)
        self.__validate_bit("number of Options 2", number_of_options_2, 4)
        self.__validate_bit("Service ID", service_id, 16)
        self.__validate_bit("Instance ID", instance_id, 16)
        self.__validate_bit("Major Version", major_version, 8)
        self.__validate_bit("TTL", ttl, 24)
        self.__validate_bit("Minor Version", minor_version, 32)

        self.__type_field = type_field
        self.__index_first_option_run = index_first_option_run
        self.__index_second_option_run = index_second_option_run
        self.__number_of_options_1 = number_of_options_1
        self.__number_of_options_2 = number_of_options_2
        self.__service_id = service_id
        self.__instance_id = instance_id
        self.__major_version = major_version
        self.__ttl = ttl
        self.__minor_version = minor_version

    @property
    def type_field(self) -> int:
        return self.__type_field

    @property
    def index_first_option_run(self) -> int:
        return self.__index_first_option_run

    @property
    def index_second_option_run(self) -> int:
        return self.__index_second_option_run

    @property
    def number_of_options_1(self) -> bitarray:
        return self.__number_of_options_1

    @property
    def number_of_options_2(self) -> bitarray:
        return self.__number_of_options_2

    @property
    def service_id(self) -> int:
        return self.__service_id

    @property
    def instance_id(self) -> int:
        return self.__instance_id

    @property
    def major_version(self) -> int:
        return self.__major_version

    @property
    def ttl(self) -> int:
        return self.__ttl

    @property
    def minor_version(self) -> int:
        return self.__minor_version

    def encode(self) -> bytes:
        """Encode the entry to bytes."""
        packet = bitarray()
        for field, bits in zip(
            (
                self.type_field,
                self.index_first_option_run,
                self.index_second_option_run,
                self.number_of_options_1,
                self.number_of_options_2,
                self.service_id,
                self.instance_id,
                self.major_version,
                self.ttl,
                self.minor_version,
            ),
            (8, 8, 8, 4, 4, 16, 16, 8, 24, 32),
        ):
            if isinstance(field, int):
                packet.frombytes(field.to_bytes(bits // 8, "big"))
            elif isinstance(field, bitarray) and len(field) == bits:
                packet.extend(field)
        return packet.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "ServiceEntry":
        """Decode bytes into a ServiceEntry object."""
        if len(series) != 16:
            raise ValueError("Invalid entry length")
        packet = bitarray()
        packet.frombytes(series)
        type_field = ba2int(packet[:8])
        index_first_option_run = ba2int(packet[8:16])
        index_second_option_run = ba2int(packet[16:24])
        number_of_options_1 = packet[24:28]
        number_of_options_2 = packet[28:32]
        service_id = ba2int(packet[32:48])
        instance_id = ba2int(packet[48:64])
        major_version = ba2int(packet[64:72])
        ttl = ba2int(packet[72:96])
        minor_version = ba2int(packet[96:128])
        return cls(
            type_field=type_field,
            index_first_option_run=index_first_option_run,
            index_second_option_run=index_second_option_run,
            number_of_options_1=number_of_options_1,
            number_of_options_2=number_of_options_2,
            service_id=service_id,
            instance_id=instance_id,
            major_version=major_version,
            ttl=ttl,
            minor_version=minor_version,
        )

    @staticmethod
    def __validate_bit(name: str, value: int | bitarray, bits: int):
        if isinstance(value, int):
            max_value = (1 << bits) - 1
            if not (0 <= value <= max_value):
                raise ValueError(f"{name} must be a {bits}-bit unsigned integer")
        elif isinstance(value, bitarray):
            if len(value) != bits:
                raise ValueError(f"{name} must be a {bits}-bit bitarray")

    def __repr__(self):
        return "\n".join(
            (
                f"{'type field':<32}: 0x{self.type_field:02X}",
                f"{'index first option run':<32}: 0x{self.index_first_option_run:02X}",
                f"{'index second option run':<32}: 0x{self.index_second_option_run:02X}",
                f"{'number of options 1':<32}: {self.number_of_options_1}",
                f"{'number of options 2':<32}: {self.number_of_options_2}",
                f"{'service id':<32}: 0x{self.service_id:04X}",
                f"{'instance id':<32}: 0x{self.instance_id:04X}",
                f"{'major version':<32}: 0x{self.major_version:02X}",
                f"{'ttl':<32}: 0x{self.ttl:06X}",
                f"{'minor version':<32}: 0x{self.minor_version:08X}",
            )
        )
