from bitarray import bitarray


class EventgroupEntry:
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
        "__reserved",
        "__counter",
        "__eventgroup_id",
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
        reserved: bitarray,
        counter: bitarray,
        eventgroup_id: int,
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
        self.__validate_bit("Reserved", reserved, 12)
        self.__validate_bit("Counter", counter, 4)
        self.__validate_bit("Eventgroup ID", eventgroup_id, 16)

        self.__type_field = type_field
        self.__index_first_option_run = index_first_option_run
        self.__index_second_option_run = index_second_option_run
        self.__number_of_options_1 = number_of_options_1
        self.__number_of_options_2 = number_of_options_2
        self.__service_id = service_id
        self.__instance_id = instance_id
        self.__major_version = major_version
        self.__ttl = ttl
        self.__reserved = reserved
        self.__counter = counter
        self.__eventgroup_id = eventgroup_id

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
    def reserved(self) -> bitarray:
        return self.__reserved

    @property
    def counter(self) -> bitarray:
        return self.__counter

    @property
    def eventgroup_id(self) -> int:
        return self.__eventgroup_id

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
                self.reserved,
                self.counter,
                self.eventgroup_id,
            ),
            (8, 8, 8, 4, 4, 16, 16, 8, 24, 12, 4, 16),
        ):
            if isinstance(field, int):
                packet.frombytes(field.to_bytes(bits // 8, "big"))
            elif isinstance(field, bitarray) and len(field) == bits:
                packet.extend(field)
        return packet.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "EventgroupEntry":
        """Decode bytes into an EventgroupEntry object."""
        if len(series) != 16:
            raise ValueError("Invalid entry length")
        packet = bitarray()
        packet.frombytes(series)
        type_field = int(packet[:8].to01(), 2)
        packet = packet[8:]
        index_first_option_run = int(packet[:8].to01(), 2)
        packet = packet[8:]
        index_second_option_run = int(packet[:8].to01(), 2)
        packet = packet[8:]
        number_of_options_1 = packet[:4]
        packet = packet[4:]
        number_of_options_2 = packet[:4]
        packet = packet[4:]
        service_id = int(packet[:16].to01(), 2)
        packet = packet[16:]
        instance_id = int(packet[:16].to01(), 2)
        packet = packet[16:]
        major_version = int(packet[:8].to01(), 2)
        packet = packet[8:]
        ttl = int(packet[:24].to01(), 2)
        packet = packet[24:]
        reserved = packet[:12]
        packet = packet[12:]
        counter = packet[:4]
        packet = packet[4:]
        eventgroup_id = int(packet[:16].to01(), 2)
        packet = packet[16:]
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
            reserved=reserved,
            counter=counter,
            eventgroup_id=eventgroup_id,
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
                f"{'type field':<20}: 0x{self.type_field:02X}",
                f"{'index first option run':<20}: 0x{self.index_first_option_run:02X}",
                f"{'index second option run':<20}: 0x{self.index_second_option_run:02X}",
                f"{'number of options 1':<20}: {self.number_of_options_1}",
                f"{'number of options 2':<20}: {self.number_of_options_2}",
                f"{'service id':<20}: 0x{self.service_id:04X}",
                f"{'instance id':<20}: 0x{self.instance_id:04X}",
                f"{'major version':<20}: 0x{self.major_version:02X}",
                f"{'ttl':<20}: 0x{self.ttl:06X}",
                f"{'reserved':<20}: {self.reserved}",
                f"{'counter':<20}: {self.counter}",
                f"{'eventgroup id':<20}: 0x{self.eventgroup_id:04X}",
            )
        )
