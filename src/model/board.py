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

    _num_cols: int
    _num_rows: int
    _row_idx: int = field(default=0, init=False)
    _lines: DoublyLinkedList[Line] = field(init=False)

    def __post_init__(self) -> None:
        self._lines = DoublyLinkedList.fill_with_default(
            self._num_rows, lambda: Line(self._num_cols)
        )

    def __getitem__(self, coord: Vector2D) -> Mino:
        if not 0 <= coord.y < self._num_rows or not 0 <= coord.x < self._num_cols:
            raise IndexError
        return self._lines[coord.y][coord.x]

    def __iter__(self) -> "Board":
        self._row_idx = 0
        return self

    def __next__(self) -> Iterable[tuple[Vector2D, Mino]]:
        if self._row_idx >= self._num_rows:
            raise StopIteration
        line = self._lines[self._row_idx]
        self._row_idx += 1
        return ((Vector2D(col, self._row_idx - 1), mino) for col, mino in line)

    def __setitem__(self, coord: Vector2D, mino: Mino) -> None:
        self._lines[coord.y][coord.x] = mino

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
        self._lines.appendleft(line)

    def sift(self) -> None:
        """Removes lines that are full and appends the same number of empty
        lines.
        """
        num_removed = 0
        for line in reversed(self._lines):
            if line.data.is_full:
                self._lines.remove(line)
                num_removed += 1
        while num_removed != 0:
            self._lines.append(Line(self._num_cols))
            num_removed -= 1
