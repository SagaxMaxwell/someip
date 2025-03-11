__all__ = ["Env"]


from tools import singleton


@singleton
class Env:
    def __init__(
        self,
        config_path: str,
        log_name: str,
        log_path: str,
        log_level: str,
        log_format: str,
    ) -> None:
        self.__config_path = config_path
        self.__log_name = log_name
        self.__log_path = log_path
        self.__log_level = log_level
        self.__log_format = log_format

    @property
    def config_path(self) -> str:
        return self.__config_path

    @property
    def log_name(self) -> str:
        return self.__log_name

    @property
    def log_path(self) -> str:
        return self.__log_path

    @property
    def log_level(self) -> str:
        return self.__log_level

    @property
    def log_format(self) -> str:
        return self.__log_format
