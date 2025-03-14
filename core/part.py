__all__ = ["Part"]


from typing import Tuple


class Part:
    def __init__(
        self, mdc: Tuple[str, int], tbox: Tuple[str, int], vdc: Tuple[str, int]
    ):
        self.__mdc = mdc
        self.__tbox = tbox
        self.__vdc = vdc

    @property
    def mdc(self) -> Tuple[str, int]:
        return self.__mdc

    @property
    def tbox(self) -> Tuple[str, int]:
        return self.__tbox

    @property
    def vdc(self) -> Tuple[str, int]:
        return self.__vdc
