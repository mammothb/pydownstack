from dataclasses import InitVar, dataclass, field

from model.polymino import Mino


@dataclass
class Line:
    num_cols: InitVar[int]
    cells: list[Mino] = field(init=False)

    def __post_init__(self, num_cols: int) -> None:
        self.cells = [Mino.EMPTY] * num_cols

    def __getitem__(self, index: int) -> Mino:
        return self.cells[index]

    def __setitem__(self, index: int, mino: Mino) -> None:
        self.cells[index] = mino
