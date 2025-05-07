__all__ = ["Length"]


from enum import IntEnum


class Length(IntEnum):
    """Enumeration for Entry fields with their bit lengths."""

    TYPE_FIELD = 8
    INDEX_FIRST_OPTION_RUN = 8
    INDEX_SECOND_OPTION_RUN = 8
    NUMBER_OF_OPTIONS_1 = 4
    NUMBER_OF_OPTIONS_2 = 4
    SERVICE_ID = 16
    INSTANCE_ID = 16
    MAJOR_VERSION = 8
    TTL = 24
    MINOR_VERSION = 32
    RESERVED = 12
    COUNTER = 4
    EVENTGROUP_ID = 16
