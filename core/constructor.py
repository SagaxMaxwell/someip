__all__ = ["Constructor"]


import os
from pathlib import Path
from logging import Formatter


import toml


from core.environment import Environment
from core.part import Part
from core.allocator import Allocator
from core.transceiver import Transceiver
from tester.tester_base import TesterBase
from tester.tester_hima import TesterHima
from tester.tester_voyah import TesterVoyah


class Constructor:
    """A class responsible for constructing and initializing system components.

    The `Constructor` class manages the creation of various components such as
    `Environment`, `Part`, `Allocator`, `Transceiver`, and `Tester`. It also
    maintains a registry for different tester types.

    Attributes:
        register (dict): A dictionary mapping vehicle types to their corresponding tester classes.
        environment (Environment): The environment configuration instance.
        part (Part): The part configuration instance.
        allocator (Allocator): The allocator instance for managing client-session allocation.
        transceiver (Transceiver): The transceiver instance for network communication.
        tester (TesterBase): The selected tester instance based on vehicle type.
    """

    def __init__(self):
        """Initializes the Constructor class and sets up the tester registry."""
        self.__register = {"hima": TesterHima, "voyah": TesterVoyah}
        self.__environment = None
        self.__part = None
        self.__allocator = None
        self.__transceiver = None
        self.__tester = None

    @property
    def register(self) -> dict:
        """Gets the tester registry.

        Returns:
            dict: A mapping of vehicle types to tester classes.
        """
        return self.__register

    @property
    def environment(self) -> Environment:
        """Gets the environment configuration instance.

        Returns:
            Environment: The environment configuration.
        """
        return self.__environment

    @property
    def part(self) -> Part:
        """Gets the part configuration instance.

        Returns:
            Part: The part configuration.
        """
        return self.__part

    @property
    def allocator(self) -> Allocator:
        """Gets the allocator instance.

        Returns:
            Allocator: The session allocator.
        """
        return self.__allocator

    @property
    def transceiver(self) -> Transceiver:
        """Gets the transceiver instance.

        Returns:
            Transceiver: The transceiver used for network communication.
        """
        return self.__transceiver

    @property
    def tester(self) -> TesterBase:
        """Gets the selected tester instance.

        Returns:
            TesterBase: The tester instance based on vehicle type.
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
        )

    def build_part(self) -> None:
        """Builds and initializes the Part configuration.

        This loads configuration data from TOML files for MDC, TBOX, and VDC.
        """
        load_mdc = toml.load(Path(self.environment.config_path / "mdc.toml"))
        load_tbox = toml.load(Path(self.environment.config_path / "tbox.toml"))
        load_vdc = toml.load(Path(self.environment.config_path / "vdc.toml"))
        mdc = load_mdc.get("address")
        tbox = load_tbox.get("address")
        vdc = load_vdc.get("address")
        self.__part = Part(mdc=mdc, tbox=tbox, vdc=vdc)

    def build_allocator(self) -> None:
        """Builds and initializes the allocator."""
        self.__allocator = Allocator()

    def build_transceiver(self) -> None:
        """Builds and initializes the transceiver."""
        self.__transceiver = Transceiver()

    def build_tester(self, vehicle_type: str) -> None:
        """Builds and initializes the tester based on the specified vehicle type.

        Args:
            vehicle_type (str): The type of vehicle (e.g., 'hima' or 'voyah').

        Raises:
            ValueError: If the vehicle type is not registered.
        """
        tester_class = self.register.get(vehicle_type.strip().lower())
        if not tester_class:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")

        self.__tester = tester_class(
            environment=self.environment,
            part=self.part,
            allocator=self.allocator,
            transceiver=self.transceiver,
        )
