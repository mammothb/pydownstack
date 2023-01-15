from dataclasses import InitVar, dataclass, field

from pygame import Rect

from common.vector import Vector2D


@dataclass
class Geometry:
    size: InitVar[tuple[int, int]]
    num_cols: int
    num_rows: int

    board_area: Rect = field(init=False)

    line_height: int = field(default=19, init=False)
    line_height_small: int = field(default=15, init=False)
    text_pad: int = field(default=6, init=False)

    def __post_init__(self, size: tuple[int, int]) -> None:
        self.bottom = size[1]
        self.cell = int(size[1] * 3 / 4 / self.num_rows)

        main_w = self.cell * self.num_cols
        main_h = self.cell * self.num_rows
        main_x = int((size[0] - main_w) / 2)
        main_y = int((size[1] - main_h) / 2 - self.line_height_small)
        self.board_area = Rect(main_x, main_y, main_w, main_h)

    def hold_cell(self, coord: Vector2D) -> Rect:
        x_0 = self.board_area.left
        y_0 = self.board_area.top
        return self._make_cell(x_0, y_0, self.cell, coord)

    def main_cell(self, coord: Vector2D) -> Rect:
        x_0, y_0 = self.board_area.bottomleft
        return self._make_cell(x_0, y_0, self.cell, coord)

    def preview_cell(self, idx: int, coord: Vector2D) -> Rect:
        x_0 = self.board_area.right + self.cell
        y_0 = self.board_area.top + (idx + 1) * self.cell * 3
        return self._make_cell(x_0, y_0, self.cell, coord)

    @staticmethod
    def _make_cell(x_0: int, y_0: int, size: int, coord: Vector2D) -> Rect:
        return Rect(x_0 + coord.x * size, y_0 + coord.y * size, size, size)
