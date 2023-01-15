from dataclasses import dataclass, field

from bag import Bag
from board import Board
from piece import Piece
from polymino import Mino
from ruleset import Ruleset


@dataclass
class Stacker:
    ruleset: Ruleset

    bag: Bag = field(init=False)
    board: Board = field(init=False)

    def __post_init__(self) -> None:
        self.bag = Bag(self.ruleset)
        self.board = Board(self.ruleset.num_cols, self.ruleset.num_rows)

    def spawn_from_bag(self) -> None:
        self._spawn(self.bag.next)

    def _spawn(self, mino: Mino) -> None:
        piece = Piece(self.ruleset, mino)
        print(piece)
        piece.get_coords(self.ruleset)
        piece.rot += 1
        piece.get_coords(self.ruleset)
