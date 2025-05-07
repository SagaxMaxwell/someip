__all__ = ["Length"]


from enum import IntEnum


class Length(IntEnum):
    """Enumeration for message fields with their bit lengths."""

    LENGTH = 16
    TYPE = 8
    DISCARDABLE_FLAG = 1
    BIT_1_TO_BIT_7 = 7
    IPV4_ADDRESS = 32
    IPV6_ADDRESS = 128
    RESERVED = 8
    TRANSPORT_PROTOCOL = 8
    TRANSPORT_PROTOCOL_PORT_NUMBER = 16
