__all__ = ["Environment"]


from pathlib import Path
from logging import Formatter


from tools import singleton


@singleton
class Environment:
    def __init__(
        self,
        config_path: Path,
        log_name: str,
        log_path: Path,
        log_level: int,
        log_format: Formatter,
    ) -> None:
        self.__config_path = config_path
        self.__log_name = log_name
        self.__log_path = log_path
        self.__log_level = log_level
        self.__log_format = log_format

    @property
    def config_path(self) -> Path:
        return self.__config_path

    @property
    def log_name(self) -> str:
        return self.__log_name

    @property
    def log_path(self) -> Path:
        return self.__log_path

    @property
    def log_level(self) -> int:
        return self.__log_level

    @property
    def log_format(self) -> Formatter:
        return self.__log_format
