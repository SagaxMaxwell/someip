__all__ = ["Part"]


from typing import Tuple


class Part:
    """
    Represents a hardware or software component with three main attributes.

    This class encapsulates the details of an MDC, TBOX, and VDC, each represented
    as a tuple containing an identifier (str) and a corresponding integer value.
    """

    def __init__(
        self, mdc: Tuple[str, int], tbox: Tuple[str, int], vdc: Tuple[str, int]
    ) -> None:
        """
        Initializes a Part instance.

        Args:
            mdc (Tuple[str, int]): The MDC (Main Data Controller) identifier and value.
            tbox (Tuple[str, int]): The TBOX (Telematics Box) identifier and value.
            vdc (Tuple[str, int]): The VDC (Vehicle Data Controller) identifier and value.
        """
        self.__mdc = mdc
        self.__tbox = tbox
        self.__vdc = vdc

    @property
    def mdc(self) -> Tuple[str, int]:
        """Gets the MDC (Main Data Controller) information."""
        return self.__mdc

    @property
    def tbox(self) -> Tuple[str, int]:
        """Gets the TBOX (Telematics Box) information."""
        return self.__tbox

    @property
    def vdc(self) -> Tuple[str, int]:
        """Gets the VDC (Vehicle Data Controller) information."""
        return self.__vdc
