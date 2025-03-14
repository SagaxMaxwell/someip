__all__ = ["Transceiver"]


import socket
from typing import Tuple


class Transceiver:
    def send(
        self, local: Tuple[str, int], remote: Tuple[str, int], packet: bytes
    ) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(local)
            s.connect(remote)
            s.sendall(packet)
            response = s.recv(2048)
        return response
