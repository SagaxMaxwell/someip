__all__ = ["Transceiver"]


import socket
from typing import Tuple


class Transceiver:
    """
    A network transceiver for sending and receiving data over TCP.

    This class provides a method to establish a TCP connection between a local
    and remote address, send a data packet, and receive a response.
    """

    def send(
        self, local: Tuple[str, int], remote: Tuple[str, int], packet: bytes
    ) -> bytes:
        """
        Sends a data packet to a remote address and receives a response.

        This method creates a TCP socket, binds it to a local address, connects to the
        remote address, sends the packet, and waits for a response.

        Args:
            local (Tuple[str, int]): The local address (IP, port) to bind the socket.
            remote (Tuple[str, int]): The remote address (IP, port) to connect to.
            packet (bytes): The data packet to be sent.

        Returns:
            bytes: The response received from the remote address.

        Raises:
            socket.error: If a socket operation fails.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(local)
            s.connect(remote)
            s.sendall(packet)
            response = s.recv(2048)
        return response
