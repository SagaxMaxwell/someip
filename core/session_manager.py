__all__ = ["SessionManager"]


import threading
import itertools
import os
from collections import defaultdict
from typing import Dict, Tuple


class SessionManager:
    def __init__(self):
        self.__lock = threading.RLock()
        self.__client_pool: Dict[Tuple[str, int], int] = dict()
        self.__session_pool: Dict[int, itertools.count] = defaultdict(itertools.count)

    @property
    def lock(self) -> threading.RLock:
        return self.__lock

    @property
    def client_pool(self) -> Dict[Tuple[str, int], int]:
        return self.__client_pool

    @property
    def session_pool(self) -> Dict[int, itertools.count]:
        return self.__session_pool

    def get_client_id(self, local: Tuple[str, int]) -> int:
        with self.lock:
            if local not in self.client_pool:
                self.client_pool[local] = self.generate_client_id()
            return self.client_pool[local]

    def get_session_id(self, client_id: int) -> int:
        with self.lock:
            return next(self.session_pool[client_id])

    def generate_client_id(self) -> int:
        return int.from_bytes(os.urandom(4), "big")

    def release_client(self, local: Tuple[str, int]):
        with self.lock:
            if local in self.client_pool:
                client_id = self.client_pool.pop(local)
                self.session_pool.pop(client_id, None)

    def release_all(self):
        with self.lock:
            self.client_pool.clear()
            self.session_pool.clear()
