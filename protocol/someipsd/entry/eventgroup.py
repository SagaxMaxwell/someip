__all__ = ["Eventgroup"]


from bitarray import bitarray
from bitarray.util import ba2int, int2ba

from protocol.someipsd.entry.length import Length
from utils.series_reader import SeriesReader


class Eventgroup:

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
        self.__reserved = reserved
        self.__counter = counter
        self.__eventgroup_id = eventgroup_id

    @property
    def type_field(self) -> int:
        """Returns the type field of the event group entry.

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
    def reserved(self) -> bitarray:
        """Returns the reserved bits.

        Returns:
            bitarray: The reserved bits (12 bits).
        """
        return self.__reserved

    @property
    def counter(self) -> bitarray:
        """Returns the counter value.

        Returns:
            bitarray: The counter value (4 bits).
        """
        return self.__counter

    @property
    def eventgroup_id(self) -> int:
        """Returns the event group identifier.

        Returns:
            int: The event group ID (16 bits).
        """
        return self.__eventgroup_id

    @staticmethod
    def expected_packet_length() -> int:
        """Returns the length of the event group packet.

        Returns:
            int: The length of the event group packet in bytes.
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
                Length.RESERVED,
                Length.COUNTER,
                Length.EVENTGROUP_ID,
            )
        )
        return length

    def encode(self) -> bytes:
        """Encodes the event group entry into bytes.

        Returns:
            bytes: The byte representation of the event group entry.
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
        series += self.reserved
        series += self.counter
        series += int2ba(self.eventgroup_id, length=Length.EVENTGROUP_ID)

        return series.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "Eventgroup":
        """Decodes a byte series into an Eventgroup object.

        Args:
            series (bytes): The byte series representing the event group entry.

        Returns:
            Eventgroup: The decoded event group entry object.

        Raises:
            ValueError: If the byte series has an invalid length.
        """
        packet = bitarray()
        packet.frombytes(series)

        if len(packet) != cls.expected_packet_length():
            raise ValueError("Invalid eventgroup entry length")

        reader = SeriesReader(packet)
        type_field = ba2int(reader.read(Length.TYPE_FIELD))
        index_first_option_run = ba2int(reader.read(Length.INDEX_FIRST_OPTION_RUN))
        index_second_option_run = ba2int(reader.read(Length.INDEX_SECOND_OPTION_RUN))
        number_of_options_1 = reader.read(Length.NUMBER_OF_OPTIONS_1)
        number_of_options_2 = reader.read(Length.NUMBER_OF_OPTIONS_2)
        service_id = ba2int(reader.read(Length.SERVICE_ID))
        instance_id = ba2int(reader.read(Length.INSTANCE_ID))
        major_version = ba2int(reader.read(Length.MAJOR_VERSION))
        ttl = ba2int(reader.read(Length.TTL))
        reserved = reader.read(Length.RESERVED)
        counter = reader.read(Length.COUNTER)
        eventgroup_id = ba2int(reader.read(Length.EVENTGROUP_ID))

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

    def __repr__(self) -> str:
        """Returns a string representation of the Eventgroup object.

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
                f"{'reserved':<32}: {self.reserved}",
                f"{'counter':<32}: {self.counter}",
                f"{'eventgroup id':<32}: {self.eventgroup_id}",
            )
        )
