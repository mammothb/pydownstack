from dataclasses import dataclass, field

from common.enum import Mino


@dataclass
class Line:
    size: int
    index: int = field(default=0, init=False)
    cells: list[Mino] = field(init=False)

    def __post_init__(self) -> None:
        self.cells = [Mino.EMPTY] * self.size

    def __getitem__(self, index: int) -> Mino:
        return self.cells[index]

    def __iter__(self) -> "Line":
        self.index = 0
        return self

    def __next__(self) -> tuple[int, Mino]:
        if self.index >= self.size:
            raise StopIteration
        mino = self.cells[self.index]
        self.index += 1
        return self.index - 1, mino

    def __setitem__(self, index: int, mino: Mino) -> None:
        self.cells[index] = mino

    @property
    def is_full(self) -> bool:
        return not any(cell == Mino.EMPTY for cell in self.cells)
