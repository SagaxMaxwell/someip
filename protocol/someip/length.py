__all__ = ["Length"]


from enum import IntEnum


class Length(IntEnum):
    """Enumeration for fields in a message header, defined by their bit lengths."""

    SERVICE_ID = 16
    METHOD_ID = 16
    LENGTH = 32
    CLIENT_ID = 16
    SESSION_ID = 16
    PROTOCOL_VERSION = 8
    INTERFACE_VERSION = 8
    MESSAGE_TYPE = 8
    RETURN_CODE = 8
    PAYLOAD = -1
