from dataclasses import dataclass, field

from line import Line


@dataclass
class Board:
    num_cols: int
    num_rows: int
    lines: list[Line] = field(init=False)

    def __post_init__(self) -> None:
        self.lines = [Line(self.num_cols) for _ in range(self.num_rows)]

    def print_debug(self) -> None:
        print(f"    {' '.join(map(str, range(self.num_cols)))}")
        for i, line in enumerate(self.lines):
            print(f"{i:2}| {' '.join(map(lambda x: str(x.value), line.cells))}")
