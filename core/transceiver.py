import socket
from typing import Tuple


class Transceiver:
    @staticmethod
    def send(
        local: Tuple[str, int], remote: Tuple[str, int], packet: bytes, timeout: float
    ) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.bind(local)
            s.connect(remote)
            s.sendall(packet)
            response = s.recv(2048)
        return response
