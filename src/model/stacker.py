from dataclasses import dataclass, field

from model.bag import Bag
from model.board import Board
from model.piece import Piece
from model.polymino import Mino
from model.ruleset import Ruleset
from model.vector import Direction


@dataclass
class Stacker:
    ruleset: Ruleset

    bag: Bag = field(init=False)
    board: Board = field(init=False)
    current: Piece = field(init=False)

    def __post_init__(self) -> None:
        self.bag = Bag(self.ruleset)
        self.board = Board(self.ruleset.num_cols, self.ruleset.num_rows)
        self.spawn_from_bag()

    def hard_drop(self) -> None:
        """Drops current piece to the bottom and spawns new piece."""
        self.board.soft_drop(self.current)
        self.board.finalize(self.current)
        self.spawn_from_bag()

    def move_horizontal(self, dx: int) -> bool:
        """Moves the piece horizontally."""
        return self.board.move_horizontal(
            self.current, Direction.LEFT if dx < 0 else Direction.RIGHT
        )

    def soft_drop(self) -> bool:
        """Drops current piece to the bottom."""
        return self.board.soft_drop(self.current) > 0

    def spawn_from_bag(self) -> None:
        """Spawns next polymino from bag."""
        self._spawn(self.bag.next)

    def _spawn(self, mino: Mino) -> None:
        piece = Piece(self.ruleset, mino)
        if self.board.has_collision(piece):
            print("occupied")
            return
        self.current = piece
