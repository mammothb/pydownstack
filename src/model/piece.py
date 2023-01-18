"""The current piece controlled by the player."""

import copy
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Iterable

from common.enum import Direction, Mino, Rotation

if TYPE_CHECKING:
    from common.vector import Vector2D
    from model.board import Board
    from model.ruleset import Ruleset


@dataclass
class Piece:
    """The current piece controlled by the player."""

    ruleset: InitVar["Ruleset"]

    mino: Mino
    rot: int = field(default=0, init=False)
    origin: "Vector2D" = field(init=False)

    def __post_init__(self, ruleset: "Ruleset") -> None:
        self.origin = ruleset.get_origin(self.mino)

    def get_coords(self, ruleset: "Ruleset") -> Iterable["Vector2D"]:
        """Returns the coordinates occupied by the piece."""

        return (
            coord + self.origin for coord in ruleset.get_coords(self.mino, self.rot)
        )

    def soft_drop(self, board: "Board", ruleset: "Ruleset") -> int:
        """Drops piece down until there is a collision.

        Returns:
            The number of rows moved.
        """
        steps = 0
        while self.try_move(Direction.DOWN, board, ruleset):
            steps += 1
        return steps

    def try_move(
        self, displacement: "Vector2D", board: "Board", ruleset: "Ruleset"
    ) -> bool:
        """Returns a list of coordinates if moved by the provided
        `displacement`.
        """
        tmp = copy.deepcopy(self)
        tmp._move(displacement)  # pylint: disable=protected-access
        if not board.has_collision(tmp.get_coords(ruleset)):
            self._move(displacement)
            return True
        return False

    def try_rotate(self, dr: int, board: "Board", ruleset: "Ruleset") -> bool:
        """Returns possible a list of possible coordinates after rotating by
        `dr`.
        """
        rotation = Rotation.CW if dr > 0 else Rotation.CCW
        rot_dst = (self.rot + dr) % 4
        for displacement in ruleset.get_kicks(self.mino, rotation, rot_dst):
            tmp = copy.deepcopy(self)
            tmp._rotate(displacement, dr, ruleset)  # pylint: disable=protected-access
            if not board.has_collision(tmp.get_coords(ruleset)):
                self._rotate(displacement, dr, ruleset)
                return True
        return False

    def _move(self, displacement: "Vector2D") -> None:
        self.origin += displacement

    def _rotate(self, displacement: "Vector2D", dr: int, ruleset: "Ruleset") -> None:
        self._move(displacement)
        self.rot = (self.rot + dr) % ruleset.num_rots
