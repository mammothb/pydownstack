"""Origin and kicks data of a polymino."""

from collections import defaultdict
from dataclasses import dataclass

from common.enum import Rotation
from common.vector import Vector2D


@dataclass
class Polymino:
    """Origin and kicks data of one polymino type."""

    width: int
    coords: list[Vector2D]
    origin: Vector2D
    kicks: defaultdict[Rotation, dict[int, list[Vector2D]]]

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
        kicks_vec: defaultdict[Rotation, dict[int, list[Vector2D]]] = defaultdict(dict)
        for key, value in kicks.items():
            rotation = Rotation.CCW if key[0] == "<" else Rotation.CW
            kicks_vec[rotation][int(key[1])] = list(map(Vector2D.from_list, value))
        return cls(width, coords_vec, origin_vec, kicks_vec)
