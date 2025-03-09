__all__ = ["MessageType"]


from enum import IntEnum


class MessageType(IntEnum):
    REQUEST = 0x00
    REQUEST_NO_RETURN = 0x01
    NOTIFICATION = 0x02
    RESPONSE = 0x80
    ERROR = 0x81
    TP_REQUEST = 0x20
    TP_REQUEST_NO_RETURN = 0x21
    TP_NOTIFICATION = 0x22
    TP_RESPONSE = 0xA0
    TP_ERROR = 0xA1
