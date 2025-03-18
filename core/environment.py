__all__ = ["Environment"]


from pathlib import Path
from logging import Formatter


from utils import singleton


@singleton
class Environment:
    """
    A singleton class that holds environment configurations.

    This class provides configuration settings related to logging and application paths.
    It ensures that only a single instance is created throughout the application lifecycle.
    """

    def __init__(
        self,
        config_path: Path,
        log_name: str,
        log_path: Path,
        log_level: int,
        log_format: Formatter,
        vehicle_type: str,
    ) -> None:
        """
        Initializes the environment settings.

        Args:
            config_path (Path): The path to the configuration file.
            log_name (str): The name of the log file.
            log_path (Path): The directory where logs are stored.
            log_level (int): The logging level.
            log_format (Formatter): The logging format.
            vehicle_type (str): The vehicle type.
        """
        self.__config_path = config_path
        self.__log_name = log_name
        self.__log_path = log_path
        self.__log_level = log_level
        self.__log_format = log_format
        self.__vehicle_type = vehicle_type

    @property
    def config_path(self) -> Path:
        """Gets the configuration file path."""
        return self.__config_path

    @property
    def log_name(self) -> str:
        """Gets the log file name."""
        return self.__log_name

    @property
    def log_path(self) -> Path:
        """Gets the log storage directory."""
        return self.__log_path

    @property
    def log_level(self) -> int:
        """Gets the logging level."""
        return self.__log_level

    @property
    def log_format(self) -> Formatter:
        """Gets the logging format."""
        return self.__log_format

    @property
    def vehicle_type(self) -> str:
        """Gets the vehicle type."""
        return self.__vehicle_type
