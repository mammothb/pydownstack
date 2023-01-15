from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Vector2D:
    """A 2 element vector represented by x,y-coordinates in int."""

    # pylint: disable=invalid-name
    x: int
    y: int

    def __add__(self, other: "Vector2D") -> "Vector2D":
        if not isinstance(other, Vector2D):
            raise ValueError("Vector2D is required.")
        vector = Vector2D(self.x + other.x, self.y + other.y)
        return vector

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def from_list(cls, coord: list[int]) -> "Vector2D":
        return cls(coord[0], coord[1])


@dataclass
class Direction:
    """Direction vectors."""

    DOWN: ClassVar[Vector2D] = Vector2D(0, -1)
    LEFT: ClassVar[Vector2D] = Vector2D(-1, 0)
    RIGHT: ClassVar[Vector2D] = Vector2D(1, 0)
