"""Renderer."""

from dataclasses import InitVar, dataclass, field
from functools import partial
from typing import TYPE_CHECKING, ClassVar

import pygame
from pygame import Color

from client.cells import Cells
from client.geometry import Geometry
from client.label import Label
from common.enum import Action, CellStyle, Mino

if TYPE_CHECKING:
    from pygame.event import Event
    from pygame.font import Font
    from pygame.surface import Surface

    from client.controls import Controls
    from client.timer import Timer
    from model.board import Board
    from model.piece import BasePiece, GhostPiece, Piece

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
class View:  # pylint: disable=too-many-instance-attributes
    """Renderer."""

    colors: ClassVar[dict[Mino, Color]] = {
        key: Color(color) for key, color in COLORS.items()
    }
    styles: ClassVar[dict[Mino, CellStyle]] = {
        mino: CellStyle.OUTLINE if mino == Mino.EMPTY else CellStyle.SOLID
        for mino in Mino
    }

    num_cols: InitVar[int]
    num_rows: InitVar[int]

    _controls: "Controls"
    _font: "Font"
    _geometry: Geometry = field(init=False)
    _queue: Cells = field(init=False)
    _board: Cells = field(init=False)
    _piece: Cells = field(init=False)
    _ghost: Cells = field(init=False)
    _help: list[Label] = field(default_factory=lambda: [], init=False)

    def __post_init__(self, num_cols: int, num_rows: int) -> None:
        self._geometry = Geometry(DEFAULT_SIZE, num_cols, num_rows)
        self._queue = Cells()
        self._board = Cells(num_rows)
        self._piece = Cells(num_rows)
        self._ghost = Cells(num_rows)
        self._set_control_labels()

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
        self._queue.paint(canvas, self.colors, CellStyle.SOLID)
        self._board.paint(canvas, self.colors, self.styles)
        self._piece.paint(canvas, self.colors, CellStyle.SOLID)
        self._ghost.paint(canvas, self.colors, CellStyle.ALPHA)

        num_lines = 0
        for label in self._help:
            label.paint(canvas, self._geometry.get_hud_loc(0, num_lines))
            num_lines += 1

    def render_labels(self) -> None:
        """Renders the texts."""
        for label in self._help:
            label.render(self._font)

    def set_board(self, board: "Board") -> None:
        """Sets the colors and geometry of the game board."""
        self._board.clear()
        for line in board:
            self._board.append(line, self._geometry.transform("main"))

    def set_piece(self, piece: "Piece", ghost: "GhostPiece") -> None:
        """Sets the colors and geometry of the current and ghost pieces."""
        self._piece.clear()
        self._ghost.clear()
        self._piece.append(
            ((coord, piece.mino) for coord in piece.coords),
            self._geometry.transform("main"),
        )
        self._ghost.append(
            ((coord, ghost.mino) for coord in ghost.coords),
            self._geometry.transform("main"),
        )

    def set_queue(self, previews: "list[BasePiece]", hold: "BasePiece | None") -> None:
        """Sets the colors and geometry of the preview queue."""
        self._queue.clear()
        if hold is not None:
            self._queue.append(
                ((coord, hold.mino) for coord in hold.base_coords),
                self._geometry.transform("hold"),
            )
        for i, preview in enumerate(previews):
            preview_cell = partial(self._geometry.transform("preview"), i)
            self._queue.append(
                ((coord, preview.mino) for coord in preview.base_coords), preview_cell
            )

    def _handle_key_down(self, key: int, timer: "Timer") -> "Action | None":
        action = self._controls.parse(key)
        if action is None:
            return None
        if action.can_das:
            timer.start_autorepeat(action)
        return action

    def _handle_key_up(self, key: int, timer: "Timer") -> None:
        if (action := self._controls.parse(key)) is not None:
            timer.stop_autorepeat(action)

    def _set_control_labels(self) -> None:
        # pylint: disable=line-too-long
        # fmt: off
        labels_and_keys = [
            ("Left, Right", f"{self._controls.get_key_name(Action.MOVE_LEFT)}, {self._controls.get_key_name(Action.MOVE_RIGHT)}"),
            ("CCW, CW", f"{self._controls.get_key_name(Action.ROTATE_CCW)}, {self._controls.get_key_name(Action.ROTATE_CW)}"),
            ("Soft Drop, Hard Drop", f"{self._controls.get_key_name(Action.SOFT_DROP)}, {self._controls.get_key_name(Action.HARD_DROP)}"),
            ("Hold", self._controls.get_key_name(Action.HOLD)),
            ("Reset", self._controls.get_key_name(Action.RESET)),
        ]
        # fmt: on
        longest_label = max(labels_and_keys, key=lambda x: len(x[0]))[0]
        label_width = len(longest_label) + 1

        self._help.append(Label("Game Controls:"))
        for label, key in labels_and_keys:
            self._help.append(Label(f"{label:<{label_width}}: {key}"))
