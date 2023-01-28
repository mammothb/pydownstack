"""Stacker engine."""

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from common.enum import Direction
from model.bag import Bag
from model.board import Board
from model.line import Line
from model.piece import BasePiece, Piece

if TYPE_CHECKING:
    from common.enum import Mino
    from model.piece import GhostPiece
    from model.ruleset import Ruleset


@dataclass
class Stacker:  # pylint: disable=too-many-instance-attributes
    """Stacker engine."""

    ruleset: "Ruleset"

    garbage_interval: int = field(init=False)
    num_pieces: int = field(default=0, init=False)
    bag: Bag = field(init=False)
    board: Board = field(init=False)
    current: Piece = field(init=False)
    _held: "Mino | None" = field(default=None, init=False)
    held_this_turn: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.garbage_interval = 6 - self.ruleset.difficulty
        self.bag = Bag(self.ruleset)
        self.board = Board(self.ruleset.num_cols, self.ruleset.num_rows)
        for _ in range(10):
            self._generate_cheese()
        self.spawn_from_bag()

    @property
    def ghost(self) -> "GhostPiece":
        """The ghost piece."""
        ghost = self.current.ghost
        ghost.soft_drop(self.board)
        return ghost

    @property
    def held(self) -> BasePiece | None:
        """The held piece."""
        if self._held is None:
            return None
        return BasePiece(self._held, self.ruleset.get_all_coords(self._held))

    @property
    def previews(self) -> list[BasePiece]:
        """The preview pieces."""
        return [
            BasePiece(mino, self.ruleset.get_all_coords(mino))
            for mino in self.bag.previews
        ]

    def hard_drop(self) -> None:
        """Drops current piece to the bottom and spawns new piece."""
        self.current.soft_drop(self.board)
        self.board.finalize(self.current)
        self.board.sift()
        self._calculate_cheese()
        self.spawn_from_bag()
        self.held_this_turn = False

    def hold(self) -> None:
        """Holds the current piece, swaps with previously held piece is
        available.
        """
        if self.held_this_turn:
            return
        prev = self.current.mino
        if self._held is not None:
            self._spawn(self._held)
        else:
            self.spawn_from_bag()
        self._held = prev
        self.held_this_turn = True

    def move_horizontal(self, dx: int) -> bool:
        """Moves the piece horizontally."""
        return self.current.try_move(
            Direction.LEFT if dx < 0 else Direction.RIGHT, self.board
        )

    def rotate(self, dr: int) -> bool:
        """Rotates the current piece."""
        return self.current.try_rotate(dr, self.board)

    def soft_drop(self) -> bool:
        """Drops current piece to the bottom."""
        return self.current.soft_drop(self.board) > 0

    def spawn_from_bag(self) -> None:
        """Spawns next polymino from bag."""
        self._spawn(self.bag.next)

    def _calculate_cheese(self) -> None:
        self.num_pieces += 1
        if self.num_pieces >= self.garbage_interval:
            self._generate_cheese()
            self.num_pieces %= self.garbage_interval

    def _generate_cheese(self) -> None:
        self.board.insert_below(
            Line.as_garbage(
                self.ruleset.num_cols, random.randrange(self.ruleset.num_cols)
            )
        )

    def _spawn(self, mino: "Mino") -> None:
        piece = Piece(self.ruleset, mino)
        if self.board.has_collision(piece.coords):
            print("occupied")
            return
        self.current = piece
