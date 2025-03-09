#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 14:00:00 2021
"""

__all__ = ["Packet"]


import struct


class Packet:
    """Completely immutable design for SOME/IP packet.
    Attributes:
        service_id (int): The service ID.
        method_id (int): The method ID.
        client_id (int): The client ID.
        session_id (int): The session ID.
        protocol_version (int): The protocol version.
        interface_version (int): The interface version.
        message_type (MessageType): The message type.
        return_code (ReturnCode): The return code.
        payload (bytes): The payload.
    Methods:
        encode(): Encode the packet to bytes.
        decode(series: bytes) -> Packet: Decode the packet from bytes.
    """

    __slots__ = (
        "__service_id",
        "__method_id",
        "__client_id",
        "__session_id",
        "__protocol_version",
        "__interface_version",
        "__message_type",
        "__return_code",
        "__payload",
    )

    def __init__(
        self,
        service_id: int,
        method_id: int,
        client_id: int,
        session_id: int,
        protocol_version: int,
        interface_version: int,
        message_type: int,
        return_code: int,
        payload: bytes,
    ):
        self.__validate_bit("Service ID", service_id, 16)
        self.__validate_bit("Method ID", method_id, 16)
        self.__validate_bit("Client ID", client_id, 16)
        self.__validate_bit("Session ID", session_id, 16)
        self.__validate_bit("Protocol Version", protocol_version, 8)
        self.__validate_bit("Interface Version", interface_version, 8)
        self.__validate_bit("Message Type", message_type, 8)
        self.__validate_bit("Return Code", return_code, 8)
        self.__service_id = service_id
        self.__method_id = method_id
        self.__client_id = client_id
        self.__session_id = session_id
        self.__protocol_version = protocol_version
        self.__interface_version = interface_version
        self.__message_type = message_type
        self.__return_code = return_code
        self.__payload = bytes(payload)

    @property
    def service_id(self) -> int:
        return self.__service_id

    @property
    def method_id(self) -> int:
        return self.__method_id

    @property
    def client_id(self) -> int:
        return self.__client_id

    @property
    def session_id(self) -> int:
        return self.__session_id

    @property
    def protocol_version(self) -> int:
        return self.__protocol_version

    @property
    def interface_version(self) -> int:
        return self.__interface_version

    @property
    def message_type(self) -> int:
        return self.__message_type

    @property
    def return_code(self) -> int:
        return self.__return_code

    @property
    def payload(self) -> bytes:
        return self.__payload

    @property
    def length(self) -> int:
        return 8 + len(self.__payload)

    def encode(self) -> bytes:
        """Encode the packet to bytes.
        Args:
            None.
        Returns:
            bytes: The encoded packet.
        """
        header = struct.pack(
            ">HHIHHBBBB",
            self.service_id,
            self.method_id,
            self.length,
            self.client_id,
            self.session_id,
            self.protocol_version,
            self.interface_version,
            self.message_type,
            self.return_code,
        )
        return header + self.payload

    @classmethod
    def decode(cls, series: bytes) -> "Packet":
        if len(series) < 16:
            raise ValueError("Invalid SOME/IP header length")
        (
            service_id,
            method_id,
            _,
            client_id,
            session_id,
            protocol_version,
            interface_version,
            message_type,
            return_code,
        ) = struct.unpack(">HHIHHBBBB", series[:16])
        return cls(
            service_id=service_id,
            method_id=method_id,
            client_id=client_id,
            session_id=session_id,
            protocol_version=protocol_version,
            interface_version=interface_version,
            message_type=message_type,
            return_code=return_code,
            payload=series[16:],
        )

    @staticmethod
    def __validate_bit(name: str, value: int, bits: int):
        max_value = (1 << bits) - 1
        if not (0 <= value <= max_value):
            raise ValueError(f"{name} must be a {bits}-bit unsigned integer")

    def __repr__(self):
        return "\n".join(
            (
                f"{'service id':<32}: 0x{self.service_id:04X}",
                f"{'method id':<32}: 0x{self.method_id:04X}",
                f"{'client id':<32}: 0x{self.client_id:04X}",
                f"{'session id':<32}: 0x{self.session_id:04X}",
                f"{'protocol version':<32}: 0x{self.protocol_version:02X}",
                f"{'interface version':<32}: 0x{self.interface_version:02X}",
                f"{'message type':<32}: 0x{self.message_type:02X}",
                f"{'return code':<32}: 0x{self.return_code:02X}",
                f"{'payload':<32}: {self.payload}",
            )
        )
