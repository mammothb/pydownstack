"""Stacker engine."""

import copy
import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from common.enum import Direction
from model.bag import Bag
from model.board import Board
from model.line import Line
from model.piece import Piece

if TYPE_CHECKING:
    from common.enum import Mino
    from model.ruleset import Ruleset


@dataclass
class Stacker:
    """Stacker engine."""

    ruleset: "Ruleset"

    garbage_interval: int = field(init=False)
    num_pieces: int = field(default=0, init=False)
    bag: Bag = field(init=False)
    board: Board = field(init=False)
    current: Piece = field(init=False)
    held: "Mino | None" = field(default=None, init=False)
    held_this_turn: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.garbage_interval = 6 - self.ruleset.difficulty
        self.bag = Bag(self.ruleset)
        self.board = Board(self.ruleset.num_cols, self.ruleset.num_rows)
        for _ in range(10):
            self._generate_cheese()
        self.spawn_from_bag()

    @property
    def ghost(self) -> Piece:
        """The ghost piece."""
        ghost = copy.deepcopy(self.current)
        ghost.soft_drop(self.board, self.ruleset)
        return ghost

    def hard_drop(self) -> None:
        """Drops current piece to the bottom and spawns new piece."""
        # self.board.soft_drop(self.current)
        self.current.soft_drop(self.board, self.ruleset)
        self.board.finalize(self.current, self.ruleset)
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
        if self.held is not None:
            self._spawn(self.held)
        else:
            self.spawn_from_bag()
        self.held = prev
        self.held_this_turn = True

    def move_horizontal(self, dx: int) -> bool:
        """Moves the piece horizontally."""
        return self.current.try_move(
            Direction.LEFT if dx < 0 else Direction.RIGHT, self.board, self.ruleset
        )

    def rotate(self, dr: int) -> bool:
        """Rotates the current piece."""
        return self.current.try_rotate(dr, self.board, self.ruleset)

    def soft_drop(self) -> bool:
        """Drops current piece to the bottom."""
        return self.current.soft_drop(self.board, self.ruleset) > 0

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
        if self.board.has_collision(piece.get_coords(self.ruleset)):
            print("occupied")
            return
        self.current = piece
