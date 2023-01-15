from dataclasses import InitVar, dataclass, field

from polymino import Mino


@dataclass
class Line:
    num_cols: InitVar[int]
    cells: list[Mino] = field(init=False)

    def __post_init__(self, num_cols: int) -> None:
        self.cells = [Mino.EMPTY] * num_cols
