from dataclasses import InitVar, dataclass, field

from model.polymino import Mino
from model.ruleset import Ruleset
from model.vector import Vector2D


@dataclass
class Piece:
    ruleset: InitVar[Ruleset]

    mino: Mino
    rot: int = field(default=0, init=False)
    num_rots: int = field(init=False)
    origin: Vector2D = field(init=False)
    all_coords: list[list[Vector2D]] = field(init=False)

    def __post_init__(self, ruleset: Ruleset) -> None:
        self.num_rots = ruleset.num_rots
        self.origin = ruleset.get_origin(self.mino)
        self.all_coords = [
            ruleset.get_coords(self.mino, rot) for rot in range(self.num_rots)
        ]

    @property
    def coords(self) -> list[Vector2D]:
        """Returns the coordinates occupied by the piece."""
        return [
            coord + self.origin for coord in self.all_coords[self.rot % self.num_rots]
        ]

    def move(self, direction: Vector2D) -> None:
        self.origin += direction

    def try_move(self, direction: Vector2D) -> list[Vector2D]:
        return [coord + direction for coord in self.coords]
