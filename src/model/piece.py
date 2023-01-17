import copy
from dataclasses import dataclass, field
from typing import Iterable

from common.enum import Mino, Rotation
from common.vector import Vector2D
from model.ruleset import Ruleset


@dataclass
class Piece:
    """The current piece controlled by the player."""

    ruleset: Ruleset
    mino: Mino
    rot: int = field(default=0, init=False)
    num_rots: int = field(init=False)
    origin: Vector2D = field(init=False)

    def __post_init__(self) -> None:
        self.num_rots = self.ruleset.num_rots
        self.origin = self.ruleset.get_origin(self.mino)

    @property
    def coords(self) -> list[Vector2D]:
        """Returns the coordinates occupied by the piece."""
        return [
            coord + self.origin
            for coord in self.ruleset.get_coords(self.mino, self.rot)
        ]

    def move(self, displacement: Vector2D) -> None:
        """Moves by the provided `displacement."""
        self.origin += displacement

    def rotate(self, displacement: Vector2D, rot_dst: int) -> None:
        self.move(displacement)
        self.rot = rot_dst

    def try_move(self, displacement: Vector2D) -> list[Vector2D]:
        """Returns a list of coordinates if moved by the provided
        `displacement`.
        """
        return [coord + displacement for coord in self.coords]

    def try_rotate(
        self, dr: int, ruleset: Ruleset
    ) -> Iterable[tuple[list[Vector2D], Vector2D, int]]:
        rotation = Rotation.CW if dr > 0 else Rotation.CCW
        rot_dst = (self.rot + dr) % 4
        for displacement in ruleset.get_kicks(self.mino, rotation, rot_dst):
            tmp = copy.deepcopy(self)
            tmp.move(displacement)
            tmp.rot = rot_dst
            yield tmp.coords, displacement, rot_dst
