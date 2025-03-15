__all__ = ["Allocator"]


import threading
import itertools
from collections import defaultdict
from typing import Dict, Tuple


class Allocator:
    """
    A thread-safe allocator for managing client IDs and session IDs.

    Features:
    - Assigns a unique client ID to each (IP, port) pair.
    - Maintains a session ID counter for each client ID, which increments automatically.
    - Provides methods to release client IDs and session IDs for resource management.
    """

    def __init__(self):
        """
        Initializes the Allocator.

        - Maintains a pool of client IDs (range: 1 to 0xFFFF).
        - Stores a mapping from (IP, port) to client IDs.
        - Stores a mapping from client IDs to session ID counters.
        """
        self.__lock = threading.RLock()
        self.__client_pool = set(range(1, 0xFFFF))  # Available client IDs
        self.__address_client_map: Dict[Tuple[str, int], int] = (
            dict()
        )  # (IP, port) -> client ID
        self.__client_session_map: Dict[int, itertools.count] = defaultdict(
            itertools.count
        )  # client ID -> session ID counter

    @property
    def lock(self) -> threading.RLock:
        """Returns the internal lock object for ensuring thread safety."""
        return self.__lock

    @property
    def client_pool(self) -> set:
        """Returns the current pool of available client IDs."""
        return self.__client_pool

    @property
    def address_client_map(self) -> Dict[Tuple[str, int], int]:
        """Returns the mapping of (IP, port) to client IDs."""
        return self.__address_client_map

    @property
    def client_session_map(self) -> Dict[int, itertools.count]:
        """Returns the mapping of client IDs to session ID counters."""
        return self.__client_session_map

    def get_client_id(self, local: Tuple[str, int]) -> int:
        """
        Retrieves the client ID for a given (IP, port) pair. Assigns a new one if not already assigned.

        Args:
            local (Tuple[str, int]): The (IP, port) pair.

        Returns:
            int: The assigned client ID.
        """
        with self.lock:
            if local not in self.address_client_map:
                self.address_client_map[local] = self.client_pool.pop()
            return self.address_client_map[local]

    def get_session_id(self, client_id: int) -> int:
        """
        Retrieves the next session ID for a given client ID. Resets if the limit is reached.

        Args:
            client_id (int): The client ID for which to get a session ID.

        Returns:
            int: The assigned session ID.
        """
        with self.lock:
            session_iter = self.client_session_map[client_id]
            session_id = next(session_iter)

            if session_id >= 0xFFFF:
                session_iter = self.client_session_map[client_id] = itertools.count()

            return next(session_iter)

    def release_client_id(self, local: Tuple[str, int]):
        """
        Releases the client ID associated with an (IP, port) pair and removes its session ID counter.

        Args:
            local (Tuple[str, int]): The (IP, port) pair.
        """
        with self.lock:
            if local in self.address_client_map:
                client_id = self.address_client_map.pop(local)
                self.client_session_map.pop(client_id, None)
                self.client_pool.add(client_id)

    def release(self):
        """
        Releases all allocated client IDs and session IDs, resetting all resources.
        """
        with self.lock:
            self.client_session_map.clear()
            self.address_client_map.clear()
            self.client_pool = set(range(1, 0xFFFF))
