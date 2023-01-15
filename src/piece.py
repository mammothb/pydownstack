from dataclasses import InitVar, dataclass, field

from polymino import Mino
from ruleset import Ruleset


@dataclass
class Piece:
    ruleset: InitVar[Ruleset]

    mino: Mino
    origin: list[int] = field(init=False)
    rot: int = field(default=0, init=False)

    def __post_init__(self, ruleset: Ruleset) -> None:
        self.origin = ruleset.get_origin(self.mino)

    def get_coords(self, ruleset: Ruleset) -> list[list[int]]:
        for coord in ruleset.get_coords(self.mino, self.rot):
            print(coord)
