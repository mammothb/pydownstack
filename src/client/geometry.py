"""Class to converts coordinates from internal representation to rendered
representation.
"""

from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Callable

from pygame import Rect

if TYPE_CHECKING:
    from common.vector import Vector2D


@dataclass
class Geometry:
    """Class to converts coordinates from internal representation to rendered
    representation.
    """

    size: InitVar[tuple[int, int]]
    num_cols: int
    num_rows: int

    board_area: Rect = field(init=False)

    line_height: int = field(default=19, init=False)
    line_height_small: int = field(default=15, init=False)
    text_pad: int = field(default=6, init=False)

    def __post_init__(self, size: tuple[int, int]) -> None:
        self.cell = int(size[1] * 3 / 4 / self.num_rows)

        main_w = self.cell * self.num_cols
        main_h = self.cell * self.num_rows
        main_x = int((size[0] - main_w) / 2)
        main_y = int((size[1] - main_h) / 2 - self.line_height_small)
        self.board_area = Rect(main_x, main_y, main_w, main_h)

    def get_hud_loc(self, group: int, line: int) -> tuple[int, int]:
        """Creates the top-left position for HUD group."""
        y = self.text_pad
        y += line * self.line_height
        y += group * self.line_height
        return self.text_pad, y

    def transform(self, category: str) -> Callable:
        """Returns the coordinates transform function for the specified
        category.
        """
        return getattr(self, f"_map_{category}_coords")

    def _map_hold_coords(self, coord: "Vector2D") -> Rect:
        """Creates the geometry for the 'hold' cell."""
        x_0 = self.board_area.left - self.cell * 5
        y_0 = self.board_area.top + self.cell * 3
        return self._make_cell(x_0, y_0, self.cell, coord)

    def _map_main_coords(self, coord: "Vector2D") -> Rect:
        """Creates the geometry for the 'main' cells."""
        x_0, y_0 = self.board_area.bottomleft
        return self._make_cell(x_0, y_0, self.cell, coord)

    def _map_preview_coords(self, idx: int, coord: "Vector2D") -> Rect:
        """Creates the geometry for the 'preview' cells."""
        x_0 = self.board_area.right + self.cell
        y_0 = self.board_area.top + self.cell * (idx + 1) * 3
        return self._make_cell(x_0, y_0, self.cell, coord)

    @staticmethod
    def _make_cell(x_0: int, y_0: int, size: int, coord: "Vector2D") -> Rect:
        return Rect(x_0 + size * coord.x, y_0 - size * (coord.y - 1), size, size)
