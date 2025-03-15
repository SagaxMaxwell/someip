__all__ = ["EntryType"]


from enum import IntEnum


class EntryType(IntEnum):
    """Enumeration representing different entry types in the SOME/IP protocol.

    This enum defines the various types of entries used in the protocol,
    including service requests, service offers, event group subscriptions,
    and acknowledgment types. The entry types specify different operations
    or states in the SOME/IP messaging system.

    Attributes:
        FIND_SERVICE (int): Represents a request to find a service (0x00).
        OFFER_SERVICE (int): Represents a service offer (0x01).
        STOP_OFFER_SERVICE (int): Represents a request to stop offering a service (0x01).
        SUBSCRIBE_EVENTGROUP (int): Represents a request to subscribe to an event group (0x06).
        STOP_SUBSCRIBE_EVENTGROUP (int): Represents a request to stop subscribing to an event group (0x06).
        SUBSCRIBE_EVENTGROUP_ACK (int): Represents an acknowledgment for event group subscription (0x07).
        SUBSCRIBE_EVENTGROUP_NACK (int): Represents a negative acknowledgment for event group subscription (0x07).
    """

    FIND_SERVICE = 0x00
    OFFER_SERVICE = 0x01
    STOP_OFFER_SERVICE = 0x01
    SUBSCRIBE_EVENTGROUP = 0x06
    STOP_SUBSCRIBE_EVENTGROUP = 0x06
    SUBSCRIBE_EVENTGROUP_ACK = 0x07
    SUBSCRIBE_EVENTGROUP_NACK = 0x07
