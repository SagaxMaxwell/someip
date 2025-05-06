__all__ = ["Constructor"]


import os
from logging import FileHandler, Formatter, Logger, StreamHandler
from pathlib import Path

import toml

from core.allocator import Allocator
from core.environment import Environment
from core.part import Part
from core.transceiver import Transceiver
from tester.base import Base as TesterBase


class Constructor:
    def __init__(self):
        self.build_environment()
        self.build_part()
        self.build_allocator()
        self.build_transceiver()
        self.build_logger()
        self.build_tester()

    @property
    def environment(self) -> Environment:
        """Gets the environment configuration instance.

        Returns:
            Environment: The environment configuration instance.
        """
        return self.__environment

    @property
    def part(self) -> Part:
        """Gets the part configuration instance.

        Returns:
            Part: The part configuration instance.
        """
        return self.__part

    @property
    def allocator(self) -> Allocator:
        """Gets the allocator instance.

        Returns:
            Allocator: The allocator instance for managing client-session allocation.
        """
        return self.__allocator

    @property
    def transceiver(self) -> Transceiver:
        """Gets the transceiver instance.

        Returns:
            Transceiver: The transceiver instance for network communication.
        """
        return self.__transceiver

    @property
    def logger(self) -> Logger:
        """Gets the logger instance.

        Returns:
            Logger: The logger instance for handling log messages.
        """
        return self.__logger

    @property
    def tester(self) -> TesterBase:
        """Gets the selected tester instance.

        Returns:
            TesterBase: The selected tester instance based on the vehicle type.
        """
        return self.__tester

    def build_environment(self) -> None:
        """Builds and initializes the environment configuration."""
        self.__environment = Environment(
            config_path=Path(os.getenv("CONFIG_PATH")),
            log_name=os.getenv("LOG_NAME"),
            log_path=Path(os.getenv("LOG_PATH")),
            log_level=int(os.getenv("LOG_LEVEL")),
            log_format=Formatter(os.getenv("LOG_FORMAT")),
            vehicle_type=os.getenv("VEHICLE_TYPE"),
        )

    def build_part(self) -> None:
        """Builds and initializes the part configuration.

        Loads configuration data from TOML files for MDC, TBOX, and VDC.
        """
        load_mdc = toml.load(self.environment.config_path / "mdc.toml")
        load_tbox = toml.load(self.environment.config_path / "tbox.toml")
        load_vdc = toml.load(self.environment.config_path / "vdc.toml")
        mdc = tuple(load_mdc.get("address").values())
        tbox = tuple(load_tbox.get("address").values())
        vdc = tuple(load_vdc.get("address").values())
        self.__part = Part(mdc=mdc, tbox=tbox, vdc=vdc)

    def build_allocator(self) -> None:
        """Builds and initializes the allocator."""
        self.__allocator = Allocator()

    def build_transceiver(self) -> None:
        """Builds and initializes the transceiver."""
        self.__transceiver = Transceiver()

    def build_logger(self) -> None:
        """Builds and initializes the logger.

        Configures both a file handler and a stream handler for logging.
        """
        file_handler = FileHandler(
            self.environment.log_path, mode="a", encoding="utf-8"
        )
        file_handler.setLevel(self.environment.log_level)
        file_handler.setFormatter(self.environment.log_format)

        stream_handler = StreamHandler()
        stream_handler.setLevel(self.environment.log_level)
        stream_handler.setFormatter(self.environment.log_format)

        self.__logger = Logger(self.environment.log_name, self.environment.log_level)
        self.__logger.propagate = False
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

    def build_tester(self) -> None:
        """Builds and initializes the tester based on the specified vehicle type.

        Raises:
            ValueError: If the vehicle type is not registered.
        """
        self.__tester = TesterBase(
            environment=self.environment,
            part=self.part,
            allocator=self.allocator,
            transceiver=self.transceiver,
            logger=self.logger,
        )
