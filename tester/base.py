__all__ = ["Base"]


from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path
from typing import Any, Dict, Tuple

import toml

from core.allocator import Allocator
from core.environment import Environment
from core.part import Part
from core.transceiver import Transceiver


class Base(ABC):
    """Base class for testing operations. This class defines common
    functionality for setting up and managing test environments, parts,
    and resources needed for tests."""

    def __init__(
        self,
        environment: Environment,
        part: Part,
        allocator: Allocator,
        transceiver: Transceiver,
        logger: Logger,
    ):
        """Initializes a Base instance with environment, part,
        allocator, and transceiver.

        Args:
            environment (Environment): The environment configuration for the test.
            part (Part): The part being tested.
            allocator (Allocator): Resource allocator for the test.
            transceiver (Transceiver): The transceiver used for communication during tests.
        """
        self.__environment = environment
        self.__part = part
        self.__allocator = allocator
        self.__transceiver = transceiver
        self.__logger = logger

    @property
    def environment(self) -> Environment:
        """Returns the environment configuration for the test."""
        return self.__environment

    @property
    def part(self) -> Part:
        """Returns the part being tested."""
        return self.__part

    @property
    def allocator(self) -> Allocator:
        """Returns the allocator responsible for resource management."""
        return self.__allocator

    @property
    def transceiver(self) -> Transceiver:
        """Returns the transceiver used for communication during tests."""
        return self.__transceiver

    @property
    def logger(self) -> Logger:
        return self.__logger

    def load_fields(self, path: Path) -> Dict[str, Any]:
        """Loads test configuration fields from a TOML file.

        Args:
            path (Path): Path to the TOML configuration file.

        Returns:
            Dict[str, Any]: A dictionary containing the fields loaded from the file.
        """
        fields = toml.load(path)
        return fields

    def combine_fields(
        self, local: Tuple[str, int], *fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combines the provided fields into a single dictionary,
        including client ID and session ID.

        Args:
            local (Tuple[str, int]): The local identifier and its associated value.
            *fields (Dict[str, Any]): Additional fields to combine.

        Returns:
            Dict[str, Any]: A dictionary containing the combined fields,
            including client ID and session ID.
        """
        # Retrieve client ID and session ID based on the local identifier
        client_id = self.allocator.get_client_id(local)
        session_id = self.allocator.get_session_id(client_id)

        # Combine the IDs with other provided fields
        combined = {"client_id": client_id, "session_id": session_id}
        combined.update(*fields)
        return combined
