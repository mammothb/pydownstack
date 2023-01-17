from dataclasses import dataclass
from pathlib import Path

import yaml

from common.enum import Mino, Rotation
from common.vector import Vector2D
from model.polymino import Polymino


@dataclass
class Ruleset:
    num_cols: int
    num_rows: int
    num_rots: int
    num_visible_rows: int
    num_previews: int
    polyminos: dict[Mino, Polymino]

    @property
    def mino_types(self) -> list[Mino]:
        return list(self.polyminos.keys())

    def get_coords(self, mino: Mino, rot: int = 0) -> list[Vector2D]:
        poly = self.polyminos[mino]
        return [rotate(coord, poly.width, rot) for coord in poly.coords]

    def get_kicks(self, mino: Mino, rotation: Rotation, rot_dst: int) -> list[Vector2D]:
        if rotation not in self.polyminos[mino].kicks:
            return []
        return self.polyminos[mino].kicks[rotation][rot_dst]

    def get_origin(self, mino: Mino) -> Vector2D:
        return self.polyminos[mino].origin

    def debug_pieces(self) -> None:
        for mino, poly in self.polyminos.items():
            width = poly.width
            print(mino)
            for rot in range(4):
                print(rot)
                cells = [[0] * width for _ in range(width)]
                for coord in poly.coords:
                    coord = rotate(coord, width, rot)
                    cells[coord.y][coord.x] = 1

                for row in reversed(cells):
                    print(f"{' '.join(map(str, row))}")

    @classmethod
    def from_config(cls, config_path: Path) -> "Ruleset":
        """Constructs Ruleset object from a config file."""
        with open(config_path, encoding="utf8") as infile:
            cfg = yaml.safe_load(infile.read())
        polyminos = {
            getattr(Mino, mino_type): Polymino.from_config(**mino_cfg)
            for mino_type, mino_cfg in cfg["polyminos"].items()
        }

        return cls(
            cfg["num_cols"],
            cfg["num_rows"],
            cfg["num_rots"],
            cfg["num_visible_rows"],
            cfg["num_previews"],
            polyminos,
        )


def rotate(coord: Vector2D, width: int, rot: int) -> Vector2D:
    """Rotates a 2D coordinate clockwise `rot` times."""
    rot %= 4
    while rot > 0:
        coord = Vector2D(coord.y, width - coord.x - 1)
        rot -= 1
    return coord
