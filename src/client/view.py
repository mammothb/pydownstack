"""Renderer."""

from dataclasses import dataclass, field
from functools import partial
from typing import TYPE_CHECKING, ClassVar

import pygame
from pygame import Color

from client.cells import Cells
from client.geometry import Geometry
from common.enum import CellStyle, Mino

if TYPE_CHECKING:
    from collections import deque

    from pygame.event import Event
    from pygame.surface import Surface

    from client.controls import Controls
    from client.timer import Timer
    from common.enum import Action
    from model.board import Board
    from model.piece import Piece
    from model.ruleset import Ruleset

DEFAULT_SIZE = (1200, 720)

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
    """Renderer."""

    colors: ClassVar[dict[Mino, Color]] = {
        key: Color(color) for key, color in COLORS.items()
    }
    styles: ClassVar[dict[Mino, CellStyle]] = {
        mino: CellStyle.OUTLINE if mino == Mino.EMPTY else CellStyle.SOLID
        for mino in Mino
    }

    ruleset: "Ruleset"
    controls: "Controls"
    geometry: Geometry = field(init=False)
    queue: Cells = field(init=False)
    board: Cells = field(init=False)
    piece: Cells = field(init=False)
    ghost: Cells = field(init=False)

    def __post_init__(self) -> None:
        num_cols = self.ruleset.num_cols
        num_rows = self.ruleset.num_visible_rows
        self.geometry = Geometry(DEFAULT_SIZE, num_cols, num_rows)
        self.queue = Cells()
        self.board = Cells(num_rows)
        self.piece = Cells(num_rows)
        self.ghost = Cells(num_rows)

    def handle(self, event: "Event", timer: "Timer") -> "Action | None":
        """Handles input event."""
        match event.type:
            case pygame.QUIT:
                raise SystemExit
            case pygame.KEYDOWN:
                return self._handle_key_down(event.key, timer)
            case pygame.KEYUP:
                self._handle_key_up(event.key, timer)
        return None

    def paint(self, canvas: "Surface") -> None:
        """Renders the screen."""
        canvas.fill(0)
        self.queue.paint(canvas, self.colors, CellStyle.SOLID)
        self.board.paint(canvas, self.colors, self.styles)
        self.piece.paint(canvas, self.colors, CellStyle.SOLID)
        self.ghost.paint(canvas, self.colors, CellStyle.OUTLINE)

    def set_board(self, board: "Board") -> None:
        """Sets the colors and geometry of the game board."""
        self.board.clear()
        for line in board:
            self.board.append(line, self.geometry.main_cell)

    def set_piece(self, piece: "Piece", ghost: "Piece") -> None:
        """Sets the colors and geometry of the current and ghost pieces."""
        self.piece.clear()
        self.ghost.clear()
        self.piece.append(
            ((coord, piece.mino) for coord in piece.get_coords(self.ruleset)),
            self.geometry.main_cell,
        )
        self.ghost.append(
            ((coord, ghost.mino) for coord in ghost.get_coords(self.ruleset)),
            self.geometry.main_cell,
        )

    def set_queue(self, previews: "deque[Mino]", hold: Mino | None) -> None:
        """Sets the colors and geometry of the preview queue."""
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

    def _handle_key_down(self, key: int, timer: "Timer") -> "Action | None":
        action = self.controls.parse(key)
        if action is None:
            return None
        if action.can_das:
            timer.start_autorepeat(action)
        return action

    def _handle_key_up(self, key: int, timer: "Timer") -> None:
        if (action := self.controls.parse(key)) is not None:
            timer.stop_autorepeat(action)
