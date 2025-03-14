__all__ = ["TesterBase"]


from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Tuple


import toml


from core.environment import Environment
from core.part import Part
from core.allocator import Allocator
from core.transceiver import Transceiver


class TesterBase(ABC):
    def __init__(
        self,
        environment: Environment,
        part: Part,
        allocator: Allocator,
        transceiver: Transceiver,
    ):
        self.__environment = environment
        self.__part = part
        self.__allocator = allocator
        self.__transceiver = transceiver

    @property
    def environment(self) -> Environment:
        return self.__environment

    @property
    def part(self) -> Part:
        return self.__part

    @property
    def allocator(self) -> Allocator:
        return self.__allocator

    @property
    def transceiver(self) -> Transceiver:
        return self.__transceiver

    def load_fields(self, path: Path) -> Dict[str, Any]:
        fields = toml.load(path)
        return fields

    def combine_fields(
        self, local: Tuple[str, int], *fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        client_id = self.allocator.get_client_id(local)
        session_id = self.allocator.get_session_id(client_id)
        combined = {"client_id": client_id, "session_id": session_id}
        combined.update(*fields)
        return combined
