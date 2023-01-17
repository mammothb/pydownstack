from enum import Enum, IntEnum


class Action(Enum):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    SOFT_DROP = 2
    HARD_DROP = 3
    ROTATE_CCW = 4
    ROTATE_CW = 5
    HOLD = 6
    RESET = 7

    @property
    def can_das(self) -> bool:
        """Flag to indicate if action can be DAS'd (only horizontal moves)."""
        return self in {Action.MOVE_LEFT, Action.MOVE_RIGHT}


class CellStyle(IntEnum):
    """Cell render style: either filled (SOLID) or outline only (OUTLINE)."""

    SOLID = 0
    OUTLINE = 1


class Mino(Enum):
    J = 0
    L = 1
    S = 2
    Z = 3
    T = 4
    I = 5
    O = 6
    EMPTY = 7
    GARBAGE = 8


class Rotation(Enum):
    CCW = 0
    CW = 1


class Update(Enum):
    """Controller update instruction types."""

    QUEUE = 0
    PIECE = 1
    BOARD = 2
    STACKER = 3

    @classmethod
    def all(cls) -> "list[Update]":
        """Returns all enum values."""
        return list(cls.__members__.values())
