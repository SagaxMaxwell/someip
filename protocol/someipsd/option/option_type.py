__all__ = ["OptionType"]


from enum import IntEnum


class OptionType(IntEnum):
    """Enumeration representing different option types in the SOME/IP protocol.

    This enum defines various option types used in the protocol to specify
    network configurations, including endpoint types and multicast options.

    Attributes:
        CONFIGURATION (int): Represents a configuration option (0x01).
        IPV4_ENDPOINT (int): Represents an IPv4 endpoint option (0x04).
        IPV6_ENDPOINT (int): Represents an IPv6 endpoint option (0x06).
        IPV4_MULTICAST (int): Represents an IPv4 multicast option (0x14).
        IPV6_MULTICAST (int): Represents an IPv6 multicast option (0x16).
    """

    CONFIGURATION = 0x01
    IPV4_ENDPOINT = 0x04
    IPV6_ENDPOINT = 0x06
    IPV4_MULTICAST = 0x14
    IPV6_MULTICAST = 0x16
