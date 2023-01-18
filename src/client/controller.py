"""Controller class."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from common.enum import Action, Update
from model.stacker import Stacker

if TYPE_CHECKING:
    from pygame.event import Event
    from pygame.surface import Surface

    from client.timer import Timer
    from client.view import View


@dataclass
class Controller:
    """Controller class."""

    view: "View"
    stacker: Stacker

    def __post_init__(self) -> None:
        self._update_view(Update.all())

    def handle(self, event: "Event", timer: "Timer") -> None:
        """Handles input event."""
        if (action := self.view.handle(event, timer)) is not None:
            self.handle_action(action)

    def paint(self, canvas: "Surface") -> None:
        """Renders view."""
        self.view.paint(canvas)

    def handle_action(self, action: Action) -> None:
        """Handles game operations."""
        instruction: Update | list[Update] | None = None
        match action:
            case Action.MOVE_LEFT | Action.MOVE_RIGHT:
                dx = -1 if action == Action.MOVE_LEFT else 1
                self.stacker.move_horizontal(dx)
                instruction = Update.PIECE
            case Action.ROTATE_CCW | Action.ROTATE_CW:
                dr = 1 if action == Action.ROTATE_CW else -1
                self.stacker.rotate(dr)
                instruction = Update.PIECE
            case Action.SOFT_DROP:
                self.stacker.soft_drop()
                instruction = Update.PIECE
            case Action.HARD_DROP:
                self.stacker.hard_drop()
                instruction = Update.all()
            case Action.HOLD:
                self.stacker.hold()
                instruction = [Update.PIECE, Update.QUEUE]
            case Action.RESET:
                ruleset = self.stacker.ruleset
                self.stacker = Stacker(ruleset)
                instruction = Update.all()

        self._update_view(instruction)

    def _update_view(self, instruction: Update | list[Update] | None) -> None:
        if instruction is None:
            return
        instructions = [instruction] if isinstance(instruction, Update) else instruction
        if Update.QUEUE in instructions:
            self.view.set_queue(self.stacker.bag.previews, self.stacker.held)
        if Update.PIECE in instructions:
            self.view.set_piece(self.stacker.current, self.stacker.ghost)
        if Update.BOARD in instructions:
            self.view.set_board(self.stacker.board)
