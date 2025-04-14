__all__ = ["TesterVoyah"]


from logging import Logger


from core.environment import Environment
from core.part import Part
from core.allocator import Allocator
from core.transceiver import Transceiver
from tester.tester_base import TesterBase


class TesterVoyah(TesterBase):
    def __init__(
        self,
        environment: Environment,
        part: Part,
        allocator: Allocator,
        transceiver: Transceiver,
        logger: Logger,
    ):
        super().__init__(environment, part, allocator, transceiver, logger)

    def open_window(self):
        return super().open_window()
