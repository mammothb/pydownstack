"""A line of the board."""

from dataclasses import dataclass, field

from common.enum import Mino


@dataclass
class Line:
    """A line of the board."""

    _size: int
    _index: int = field(default=0, init=False)
    _cells: list[Mino] = field(init=False)

    def __post_init__(self) -> None:
        self._cells = [Mino.EMPTY] * self._size

    def __getitem__(self, index: int) -> Mino:
        return self._cells[index]

    def __iter__(self) -> "Line":
        self._index = 0
        return self

    def __next__(self) -> tuple[int, Mino]:
        if self._index >= self._size:
            raise StopIteration
        mino = self._cells[self._index]
        self._index += 1
        return self._index - 1, mino

    def __setitem__(self, index: int, mino: Mino) -> None:
        self._cells[index] = mino

    @property
    def is_full(self) -> bool:
        """Flag to indicate of line is full."""
        return not any(cell == Mino.EMPTY for cell in self._cells)

    @classmethod
    def as_garbage(cls, size: int, hole: int) -> "Line":
        """Constructs as a garbage line.

        Args:
            size: Size of the line.
            hole: Position of the empty cell.
        """
        line = cls(size)
        for i, _ in enumerate(line):
            if i != hole:
                line[i] = Mino.GARBAGE
        return line
