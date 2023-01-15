from dataclasses import dataclass

from common.vector import Vector2D


@dataclass
class Polymino:
    width: int
    coords: list[Vector2D]
    origin: Vector2D
    kicks: dict[str, list[Vector2D]]

    @classmethod
    def from_config(
        cls,
        width: int,
        coords: list[list[int]],
        origin: list[int],
        kicks: dict[str, list[list[int]]],
    ) -> "Polymino":
        """Convert coordinates from list to Vector2D before constructing the
        class.
        """
        coords_vec = list(map(Vector2D.from_list, coords))
        origin_vec = Vector2D.from_list(origin)
        kicks_vec = {
            key: list(map(Vector2D.from_list, value)) for key, value in kicks.items()
        }
        return cls(width, coords_vec, origin_vec, kicks_vec)
