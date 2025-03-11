#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 9 14:00:00 2025
"""

__all__ = ["IPv6Option"]


import ipaddress


from bitarray import bitarray
from bitarray.util import ba2int


class IPv6Option:
    __slots__ = (
        "__type",
        "__discardable_flag",
        "__ipv6_address",
        "__transport_protocol",
        "__transport_protocol_port_number",
    )

    def __init__(
        self,
        type: int,
        discardable_flag: bitarray,
        ipv6_address: str,
        transport_protocol: int,
        transport_protocol_port_number: int,
    ) -> None:
        self.__validate_bit("Type", type, 8)
        self.__validate_bit("Discardable Flag", discardable_flag, 1)
        self.__validate_bit("Transport Protocol", transport_protocol, 8)
        self.__validate_bit(
            "Transport Protocol Port Number", transport_protocol_port_number, 16
        )
        self.__validate_ipv6_address(ipv6_address)

        self.__type = type
        self.__discardable_flag = discardable_flag
        self.__ipv6_address = ipv6_address
        self.__transport_protocol = transport_protocol
        self.__transport_protocol_port_number = transport_protocol_port_number

    @property
    def type(self) -> int:
        return self.__type

    @property
    def discardable_flag(self) -> bitarray:
        return self.__discardable_flag

    @property
    def ipv6_address(self) -> str:
        return self.__ipv6_address

    @property
    def transport_protocol(self) -> int:
        return self.__transport_protocol

    @property
    def transport_protocol_port_number(self) -> int:
        return self.__transport_protocol_port_number

    @property
    def length(self) -> int:
        return 0x0015

    def encode(self) -> bytes:
        packet = bitarray()
        for feild, bits in zip(
            (
                self.length,
                self.type,
                self.discardable_flag,
                bitarray("0" * 7),
                self.ipv6_address,
                bitarray("0" * 8),
                self.transport_protocol,
                self.transport_protocol_port_number,
            ),
            (16, 8, 1, 7, 128, 8, 8, 16),
        ):
            if isinstance(feild, bitarray):
                packet.extend(feild)
            elif isinstance(feild, int):
                packet.frombytes(feild.to_bytes(bits // 8, "big"))
            elif isinstance(feild, str):
                packet.frombytes(ipaddress.ip_address(feild).packed)
        return packet.tobytes()

    @classmethod
    def decode(cls, series: bytes) -> "IPv6Option":
        if len(series) != 24:
            raise ValueError("Invalid IPv6 Option length")
        packet = bitarray()
        packet.frombytes(series)
        type = ba2int(packet[16:24])
        discardable_flag = packet[24:25]
        ipv6_address = ipaddress.IPv6Address(packet[32:160].tobytes())
        transport_protocol = ba2int(packet[168:176])
        transport_protocol_port_number = ba2int(packet[176:192])
        return cls(
            type,
            discardable_flag,
            ipv6_address,
            transport_protocol,
            transport_protocol_port_number,
        )

    @staticmethod
    def __validate_bit(name: str, value: int | bitarray, bits: int) -> None:
        if isinstance(value, int):
            max_value = (1 << bits) - 1
            if not (0 <= value <= max_value):
                raise ValueError(f"{name} must be a {bits}-bit unsigned integer")
        elif isinstance(value, bitarray):
            if len(value) != bits:
                raise ValueError(f"{name} must be a {bits}-bit bitarray")

    @staticmethod
    def __validate_ipv6_address(ipv6_address: str) -> None:
        if ipaddress.ip_address(ipv6_address).version != 6:
            raise ValueError("Invalid IPv6 address")

    def __repr__(self) -> str:
        return "\n".join(
            (
                f"{'length':<32}: 0x{self.length:04X}",
                f"{'type':<32}: 0x{self.type:02X}",
                f"{'discardable flag':<32}: {self.discardable_flag}",
                f"{'ipv6 dddress':<32}: {self.ipv6_address}",
                f"{'transport protocol':<32}: 0x{self.transport_protocol:02X}",
                f"{'transport protocol port number':<32}: 0x{self.transport_protocol_port_number:04X}",
            )
        )
