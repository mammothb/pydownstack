from dataclasses import dataclass
from typing import ClassVar

from common.vector import Vector2D


@dataclass
class Direction:
    """Direction vectors."""

    DOWN: ClassVar[Vector2D] = Vector2D(0, -1)
    LEFT: ClassVar[Vector2D] = Vector2D(-1, 0)
    RIGHT: ClassVar[Vector2D] = Vector2D(1, 0)
