__all__ = ["Length"]


from enum import IntEnum


class Length(IntEnum):
    """Enumeration for fields in a message header, defined by their bit lengths."""

    MESSAGE_ID = 32
    LENGTH = 32
    REQUEST_ID = 32
    PROTOCOL_VERSION = 8
    INTERFACE_VERSION = 8
    MESSAGE_TYPE = 8
    RETURN_CODE = 8
