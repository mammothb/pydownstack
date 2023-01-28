"""The board which contains lines of colored cells."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable

from common.doubly_linked_list import DoublyLinkedList
from common.enum import Mino
from common.vector import Vector2D
from model.line import Line

if TYPE_CHECKING:
    from model.piece import Piece


@dataclass
class Board:
    """The board which contains lines of colored cells."""

    num_cols: int
    num_rows: int
    row_idx: int = field(default=0, init=False)
    lines: DoublyLinkedList[Line] = field(init=False)

    def __post_init__(self) -> None:
        self.lines = DoublyLinkedList.fill_with_default(
            self.num_rows, lambda: Line(self.num_cols)
        )

    def __getitem__(self, coord: Vector2D) -> Mino:
        if not 0 <= coord.y < self.num_rows or not 0 <= coord.x < self.num_cols:
            raise IndexError
        return self.lines[coord.y][coord.x]

    def __iter__(self) -> "Board":
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

    def finalize(self, piece: "Piece") -> None:
        """Sets the piece in the board."""
        for coord in piece.coords:
            self[coord] = piece.mino

    def has_collision(self, coords: Iterable[Vector2D]) -> bool:
        """Checks if the provided `target` has collision with any cells in the
        board or the walls.
        """
        try:
            return any(self[coord] != Mino.EMPTY for coord in coords)
        except IndexError:
            return True

    def insert_below(self, line: Line) -> None:
        """Insert `line` at the bottom of the board."""
        self.lines.appendleft(line)

    def sift(self) -> None:
        """Removes lines that are full and appends the same number of empty
        lines.
        """
        num_removed = 0
        for line in reversed(self.lines):
            if line.data.is_full:
                self.lines.remove(line)
                num_removed += 1
        while num_removed != 0:
            self.lines.append(Line(self.num_cols))
            num_removed -= 1
