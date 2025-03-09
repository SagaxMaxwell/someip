from enum import IntEnum


class OptionType(IntEnum):
    CONFIGURATION = 0x01
    IPV4_ENDPOINT = 0x04
    IPV6_ENDPOINT = 0x06
    IPV4_MULTICAST = 0x14
    IPV6_MULTICAST = 0x16
