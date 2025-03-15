__all__ = ["MessageType"]


from enum import IntEnum


class MessageType(IntEnum):
    """Enumeration representing different message types.

    This enum defines various types of messages used in communication, including
    requests, responses, notifications, and error messages. It also includes
    transport protocol (TP) variants.

    Attributes:
        REQUEST (int): Standard request message (0x00).
        REQUEST_NO_RETURN (int): Request message without expecting a return (0x01).
        NOTIFICATION (int): Notification message (0x02).
        RESPONSE (int): Standard response message (0x80).
        ERROR (int): Error response message (0x81).
        TP_REQUEST (int): Transport Protocol request message (0x20).
        TP_REQUEST_NO_RETURN (int): TP request message without expecting a return (0x21).
        TP_NOTIFICATION (int): TP notification message (0x22).
        TP_RESPONSE (int): TP response message (0xA0).
        TP_ERROR (int): TP error message (0xA1).
    """

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
