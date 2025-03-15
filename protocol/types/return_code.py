__all__ = ["ReturnCode"]


from enum import IntEnum


class ReturnCode(IntEnum):
    """Enumeration representing return codes for communication responses.

    This enum defines various return codes that indicate the status of a request
    or response in communication protocols.

    Attributes:
        E_OK (int): Operation successful (0x00).
        E_NOT_OK (int): General failure (0x01).
        E_UNKNOWN_SERVICE (int): The requested service is unknown (0x02).
        E_UNKNOWN_METHOD (int): The requested method is unknown (0x03).
        E_NOT_READY (int): The system is not ready to process the request (0x04).
        E_NOT_REACHABLE (int): The target is not reachable (0x05).
        E_TIMEOUT (int): Operation timed out (0x06).
        E_WRONG_PROTOCOL_VERSION (int): Incorrect protocol version (0x07).
        E_WRONG_INTERFACE_VERSION (int): Incorrect interface version (0x08).
        E_MALFORMED_MESSAGE (int): The message format is incorrect (0x09).
        E_WRONG_MESSAGE_TYPE (int): The message type is incorrect (0x0A).
        E_E2E_REPEATED (int): End-to-end protection detected repeated message (0x0B).
        E_E2E_WRONG_SEQUENCE (int): End-to-end protection detected sequence error (0x0C).
        E_E2E (int): General end-to-end protection error (0x0D).
        E_E2E_NOT_AVAILABLE (int): End-to-end protection is unavailable (0x0E).
        E_E2E_NO_NEW_DATA (int): No new data available for end-to-end protection (0x0F).
        RESERVED_GENERIC_START (int): Start of generic reserved range (0x10).
        RESERVED_GENERIC_END (int): End of generic reserved range (0x1F).
        RESERVED_SPECIFIC_START (int): Start of specific reserved range (0x20).
        RESERVED_SPECIFIC_END (int): End of specific reserved range (0x5E).
    """

    E_OK = 0x00
    E_NOT_OK = 0x01
    E_UNKNOWN_SERVICE = 0x02
    E_UNKNOWN_METHOD = 0x03
    E_NOT_READY = 0x04
    E_NOT_REACHABLE = 0x05
    E_TIMEOUT = 0x06
    E_WRONG_PROTOCOL_VERSION = 0x07
    E_WRONG_INTERFACE_VERSION = 0x08
    E_MALFORMED_MESSAGE = 0x09
    E_WRONG_MESSAGE_TYPE = 0x0A
    E_E2E_REPEATED = 0x0B
    E_E2E_WRONG_SEQUENCE = 0x0C
    E_E2E = 0x0D
    E_E2E_NOT_AVAILABLE = 0x0E
    E_E2E_NO_NEW_DATA = 0x0F
    RESERVED_GENERIC_START = 0x10
    RESERVED_GENERIC_END = 0x1F
    RESERVED_SPECIFIC_START = 0x20
    RESERVED_SPECIFIC_END = 0x5E
