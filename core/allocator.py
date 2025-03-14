__all__ = ["Allocator"]


import threading
import itertools
from collections import defaultdict
from typing import Dict, Tuple


class Allocator:
    def __init__(self):
        self.__lock = threading.RLock()
        self.__client_pool = set(range(1, 0xFFFF))
        self.__address_client_map: Dict[Tuple[str, int], int] = dict()
        self.__client_session_map: Dict[int, itertools.count] = defaultdict(
            itertools.count
        )

    @property
    def lock(self) -> threading.RLock:
        return self.__lock

    @property
    def client_pool(self) -> set:
        return self.__client_pool

    @property
    def address_client_map(self) -> Dict[Tuple[str, int], int]:
        return self.__address_client_map

    @property
    def client_session_map(self) -> Dict[int, itertools.count]:
        return self.__client_session_map

    def get_client_id(self, local: Tuple[str, int]) -> int:
        with self.lock:
            if local not in self.address_client_map:
                self.address_client_map[local] = self.client_pool.pop()
            return self.address_client_map[local]

    def get_session_id(self, client_id: int) -> int:
        with self.lock:
            session_id = next(self.client_session_map[client_id])
            if session_id >= 0xFFFF:
                self.client_session_map[client_id] = itertools.count()
            return next(self.client_session_map[client_id])

    def release_client_id(self, local: Tuple[str, int]):
        with self.lock:
            if local in self.address_client_map:
                client_id = self.address_client_map.pop(local)
                self.client_session_map.pop(client_id, None)
                self.client_pool.add(client_id)

    def release(self):
        with self.lock:
            self.client_session_map.clear()
            self.address_client_map.clear()
            self.client_pool = set(range(1, 0xFFFF))
