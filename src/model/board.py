from dataclasses import dataclass, field
from typing import Iterable

from common.enum import Mino
from common.vector import Vector2D
from model.direction import Direction
from model.line import Line
from model.piece import Piece
from model.ruleset import Ruleset


@dataclass
class Board:
    """The tetris board which contains lines of colored cells."""

    num_cols: int
    num_rows: int
    col_idx: int = field(default=0, init=False)
    row_idx: int = field(default=0, init=False)
    lines: list[Line] = field(init=False)

    def __post_init__(self) -> None:
        self.lines = [Line(self.num_cols) for _ in range(self.num_rows)]

    def __getitem__(self, coord: Vector2D) -> Mino:
        if not 0 <= coord.y < self.num_rows or not 0 <= coord.x < self.num_cols:
            raise IndexError
        return self.lines[coord.y][coord.x]

    def __iter__(self) -> "Board":
        self.col_idx = 0
        self.row_idx = 0
        return self

    def __next__(self) -> Iterable[tuple[Vector2D, Mino]]:
        if self.row_idx >= self.num_rows:
            raise StopIteration
        line = self.lines[self.row_idx]
        self.row_idx += 1
        return ((Vector2D(col, self.row_idx - 1), mino) for col, mino in line)

    def __setitem__(self, coord: Vector2D, mino: Mino) -> None:
        self.lines[coord.y][coord.x] = mino

    def finalize(self, piece: Piece) -> None:
        """Sets the piece in the board."""
        for coord in piece.coords:
            self[coord] = piece.mino

    def has_collision(self, target: Piece | list[Vector2D]) -> bool:
        """Checks if the provided `target` has collision with any cells in the
        board or the walls.
        """
        coords = target.coords if isinstance(target, Piece) else target
        try:
            return any(self[coord] != Mino.EMPTY for coord in coords)
        except IndexError:
            return True

    def move_horizontal(self, piece: Piece, displacement: Vector2D) -> bool:
        """Moves piece horizontally unless there is a collision.

        Args:
            piece: The piece to be moved.
            displacement: The amount to be moved.

        Returns:
            True if the move is successful, False is there is a collision.
        """
        if self.has_collision(piece.try_move(displacement)):
            return False
        piece.move(displacement)
        return True

    def rotate(self, piece: Piece, dr: int, ruleset: Ruleset) -> bool:
        for coords, displacement, rot_dst in piece.try_rotate(dr, ruleset):
            if not self.has_collision(coords):
                piece.rotate(displacement, rot_dst)
                return True
        return False

    def sift(self) -> None:
        dst = 0
        for src, line in enumerate(self.lines):
            if not line.is_full:
                self.lines[dst], self.lines[src] = self.lines[src], self.lines[dst]
                dst += 1
        self.lines = self.lines[:dst] + [
            Line(self.num_cols) for _ in range(self.num_rows - dst)
        ]

    def soft_drop(self, piece: Piece) -> int:
        """Drops piece down until there is a collision.

        Args:
            piece: The piece to be moved.

        Returns:
            The number of rows moved.
        """
        steps = 0
        while not self.has_collision(piece.try_move(Direction.DOWN)):
            piece.move(Direction.DOWN)
            steps += 1
        return steps
