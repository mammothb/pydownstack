"""2D vector."""

from dataclasses import dataclass


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
        """Constructs from a 2 element list."""
        return cls(coord[0], coord[1])
