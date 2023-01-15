from dataclasses import dataclass
from enum import Enum
from typing import Union

from pygame import Surface

from client.view import View
from model.stacker import Stacker


@dataclass
class Controller:
    view: View
    stacker: Stacker

    def __post_init__(self) -> None:
        self._update_view(Update.all())

    def paint(self, canvas: Surface) -> None:
        self.view.paint(canvas)

    def _update_view(self, instruction: Union["Update", list["Update"]]) -> None:
        instructions = [instruction] if isinstance(instruction, Update) else instruction
        if Update.QUEUE in instructions:
            self.view.set_queue(self.stacker.bag.previews, self.stacker.held)
        if Update.PIECE in instructions:
            self.view.set_piece(self.stacker.current, self.stacker.ghost)
        if Update.BOARD in instructions:
            pass


class Update(Enum):
    QUEUE = 0
    PIECE = 1
    BOARD = 2
    STACKER = 3

    @classmethod
    def all(cls) -> list["Update"]:
        return list(cls.__members__.values())
