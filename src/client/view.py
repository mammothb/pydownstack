from collections import deque
from dataclasses import dataclass, field
from functools import partial
from typing import Optional, cast

from pygame import Color, Surface

from client.cells import Cells
from client.geometry import Geometry
from common.mino import Mino
from model.piece import Piece
from model.ruleset import Ruleset

DEFAULT_SIZE = (800, 600)

COLORS = {
    Mino.J: "#8193FF",
    Mino.L: "#FFCC90",
    Mino.S: "#91D9A6",
    Mino.Z: "#EA6989",
    Mino.T: "#E486FA",
    Mino.I: "#73BFEA",
    Mino.O: "#FFF978",
    Mino.EMPTY: "#222222",
    Mino.GARBAGE: "#D5D7E2",
}


@dataclass
class View:
    ruleset: Ruleset
    colors: dict[Mino, Color] = field(init=False)
    geometry: Geometry = field(init=False)
    queue: Cells = field(init=False)
    piece: Cells = field(init=False)
    ghost: Cells = field(init=False)

    def __post_init__(self) -> None:
        num_cols = self.ruleset.num_cols
        num_rows = self.ruleset.num_visible_rows
        self.colors = {key: Color(color) for key, color in COLORS.items()}
        self.geometry = Geometry(DEFAULT_SIZE, num_cols, num_rows)
        self.queue = Cells()
        self.piece = Cells(num_rows)
        self.ghost = Cells(num_rows)

    def paint(self, canvas: Surface) -> None:
        canvas.fill(0)
        self.queue.paint(canvas, self.colors)
        self.piece.paint(canvas, self.colors)
        self.ghost.paint(canvas, self.colors)

    def set_piece(self, piece: Piece, ghost: Piece) -> None:
        self.piece.clear()
        self.ghost.clear()
        self.piece.append(
            ((coord, piece.mino) for coord in piece.coords), self.geometry.main_cell
        )
        self.ghost.append(
            ((coord, ghost.mino) for coord in ghost.coords), self.geometry.main_cell
        )

    def set_queue(self, previews: deque[Mino], hold: Optional[Mino]) -> None:
        self.queue.clear()
        if hold is not None:
            self.queue.append(
                ((coord, hold) for coord in self.ruleset.get_coords(hold)),
                self.geometry.hold_cell,
            )
        for i, mino in enumerate(previews):
            preview_cell = partial(self.geometry.preview_cell, i)
            self.queue.append(
                ((coord, mino) for coord in self.ruleset.get_coords(mino)),
                preview_cell,
            )
