__all__ = ["Constructor"]


import os
from pathlib import Path
from logging import Formatter


import toml


from core.environment import Environment
from core.part import Part
from core.allocator import Allocator
from core.transceiver import Transceiver
from core.constructor import Constructor
from tester.tester_base import TesterBase
from tester.tester_hima import TesterHima
from tester.tester_voyah import TesterVoyah


class Constructor:
    def __init__(self):
        self.__register = {"hima": TesterHima, "voyah": TesterVoyah}
        self.__environment = None
        self.__part = None
        self.__allocator = None
        self.__transceiver = None
        self.__tester = None

    @property
    def register(self) -> dict:
        return self.__register

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

    @property
    def tester(self) -> TesterBase:
        return self.__tester

    def build_environment(self) -> None:
        self.__environment = Environment(
            config_path=Path(os.getenv("CONFIG_PATH")),
            log_name=os.getenv("LOG_NAME"),
            log_path=Path(os.getenv("LOG_PATH")),
            log_level=int(os.getenv("LOG_LEVEL")),
            log_format=Formatter(os.getenv("LOG_FORMAT")),
        )

    def build_part(self) -> None:
        load_mdc = toml.load(Path(self.environment.config_path / "mdc.toml"))
        load_tbox = toml.load(Path(self.environment.config_path / "tbox.toml"))
        load_vdc = toml.load(Path(self.environment.config_path / "vdc.toml"))
        mdc = load_mdc.get("address")
        tbox = load_tbox.get("address")
        vdc = load_vdc.get("address")
        self.__part = Part(mdc=mdc, tbox=tbox, vdc=vdc)

    def build_allocator(self) -> None:
        self.__allocator = Allocator()

    def build__transceiver(self) -> None:
        self.__transceiver = Transceiver()

    def build_tester(self, vehicle_type: str) -> None:
        self.__tester = self.register.get(vehicle_type.strip().lower())(
            environment=self.environment,
            part=self.part,
            allocator=self.allocator,
            transceiver=self.transceiver,
        )
