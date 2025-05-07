__all__ = ["Length"]


from enum import IntEnum


class Length(IntEnum):
    """Enumeration for message fields with associated bit lengths."""

    SERVICE_ID = 16
    METHOD_ID = 16
    LENGTH = 32
    CLIENT_ID = 16
    SESSION_ID = 16
    PROTOCOL_VERSION = 8
    INTERFACE_VERSION = 8
    MESSAGE_TYPE = 8
    RETURN_CODE = 8
    FLAGS = 8
    RESERVED = 24
    LENGTH_OF_ENTRIES_ARRAY = 32
    ENTRIES_ARRAY = -1
    LENGTH_OF_OPTIONS_ARRAY = 32
    OPTIONS_ARRAY = -1
