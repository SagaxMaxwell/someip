__all__ = ["Service"]


from bitarray import bitarray
from bitarray.util import ba2int, int2ba

from protocol.someipsd.entry.length import Length
from utils.bit_reader import BitReader


class Service:

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
    ) -> None:
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
        """Returns the type field of the service entry.

        Returns:
            int: The type field (8 bits).
        """
        return self.__type_field

    @property
    def index_first_option_run(self) -> int:
        """Returns the index of the first option run.

        Returns:
            int: The index of the first option run (8 bits).
        """
        return self.__index_first_option_run

    @property
    def index_second_option_run(self) -> int:
        """Returns the index of the second option run.

        Returns:
            int: The index of the second option run (8 bits).
        """
        return self.__index_second_option_run

    @property
    def number_of_options_1(self) -> bitarray:
        """Returns the number of options in the first option run.

        Returns:
            bitarray: The number of options (4 bits).
        """
        return self.__number_of_options_1

    @property
    def number_of_options_2(self) -> bitarray:
        """Returns the number of options in the second option run.

        Returns:
            bitarray: The number of options (4 bits).
        """
        return self.__number_of_options_2

    @property
    def service_id(self) -> int:
        """Returns the service identifier.

        Returns:
            int: The service ID (16 bits).
        """
        return self.__service_id

    @property
    def instance_id(self) -> int:
        """Returns the instance identifier.

        Returns:
            int: The instance ID (16 bits).
        """
        return self.__instance_id

    @property
    def major_version(self) -> int:
        """Returns the major version.

        Returns:
            int: The major version (8 bits).
        """
        return self.__major_version

    @property
    def ttl(self) -> int:
        """Returns the time-to-live (TTL).

        Returns:
            int: The TTL value (24 bits).
        """
        return self.__ttl

    @property
    def minor_version(self) -> int:
        """Returns the minor version.

        Returns:
            int: The minor version (32 bits).
        """
        return self.__minor_version

    @staticmethod
    def expected_packet_length() -> int:
        """Returns the length of the service entry.

        Returns:
            int: The length of the service entry in bytes.
        """
        length = sum(
            (
                Length.TYPE_FIELD,
                Length.INDEX_FIRST_OPTION_RUN,
                Length.INDEX_SECOND_OPTION_RUN,
                Length.NUMBER_OF_OPTIONS_1,
                Length.NUMBER_OF_OPTIONS_2,
                Length.SERVICE_ID,
                Length.INSTANCE_ID,
                Length.MAJOR_VERSION,
                Length.TTL,
                Length.MINOR_VERSION,
            )
        )
        return length

    def encode(self) -> bytes:
        """Encodes the service entry into bytes.

        Returns:
            bytes: The byte representation of the service entry.
        """
        series = bitarray()
        series += int2ba(self.type_field, length=Length.TYPE_FIELD)
        series += int2ba(
            self.index_first_option_run, length=Length.INDEX_FIRST_OPTION_RUN
        )
        series += int2ba(
            self.index_second_option_run, length=Length.INDEX_SECOND_OPTION_RUN
        )
        series += self.number_of_options_1
        series += self.number_of_options_2
        series += int2ba(self.service_id, length=Length.SERVICE_ID)
        series += int2ba(self.instance_id, length=Length.INSTANCE_ID)
        series += int2ba(self.major_version, length=Length.MAJOR_VERSION)
        series += int2ba(self.ttl, length=Length.TTL)
        series += int2ba(self.minor_version, length=Length.MINOR_VERSION)

        return series.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "Service":
        """Decodes a byte series into an Service object.

        Args:
            series (bytes): The byte series representing the service entry.

        Returns:
            Service: The decoded service entry object.

        Raises:
            ValueError: If the byte series has an invalid length.
        """
        packet = bitarray()
        packet.frombytes(series)

        if len(packet) != cls.expected_packet_length():
            raise ValueError("Invalid service entry length")

        reader = BitReader(packet)
        type_field = ba2int(reader.read(Length.TYPE_FIELD))
        index_first_option_run = ba2int(reader.read(Length.INDEX_FIRST_OPTION_RUN))
        index_second_option_run = ba2int(reader.read(Length.INDEX_SECOND_OPTION_RUN))
        number_of_options_1 = reader.read(Length.NUMBER_OF_OPTIONS_1)
        number_of_options_2 = reader.read(Length.NUMBER_OF_OPTIONS_2)
        service_id = ba2int(reader.read(Length.SERVICE_ID))
        instance_id = ba2int(reader.read(Length.INSTANCE_ID))
        major_version = ba2int(reader.read(Length.MAJOR_VERSION))
        ttl = ba2int(reader.read(Length.TTL))
        minor_version = ba2int(reader.read(Length.MINOR_VERSION))

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

    def __repr__(self) -> str:
        """Returns a string representation of the ServiceEntry object.

        Returns:
            str: The string representation of the object.
        """
        return "\n".join(
            (
                f"{'type field':<32}: {self.type_field}",
                f"{'index first option run':<32}: {self.index_first_option_run}",
                f"{'index second option run':<32}: {self.index_second_option_run}",
                f"{'number of options 1':<32}: {self.number_of_options_1}",
                f"{'number of options 2':<32}: {self.number_of_options_2}",
                f"{'service id':<32}: {self.service_id}",
                f"{'instance id':<32}: {self.instance_id}",
                f"{'major version':<32}: {self.major_version}",
                f"{'ttl':<32}: {self.ttl}",
                f"{'minor version':<32}: {self.minor_version}",
            )
        )
