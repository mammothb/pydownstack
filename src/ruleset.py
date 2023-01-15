from dataclasses import dataclass
from pathlib import Path

import yaml

from polymino import Mino, Polymino


@dataclass
class Ruleset:
    num_cols: int
    num_rows: int
    num_visible_rows: int
    num_previews: int
    polyminos: dict[Mino, Polymino]

    @property
    def mino_types(self) -> list[Mino]:
        return list(self.polyminos.keys())

    def get_coords(self, mino: Mino, rot: int) -> list[list[int]]:
        poly = self.polyminos[mino]
        return [rotate(coord, poly.width, rot) for coord in poly.coords]

    def get_origin(self, mino: Mino) -> list[int]:
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
                    cells[coord[1]][coord[0]] = 1

                for row in reversed(cells):
                    print(f"{' '.join(map(str, row))}")

    @classmethod
    def from_config(cls, config_path: Path) -> "Ruleset":
        with open(config_path, encoding="utf8") as infile:
            cfg = yaml.safe_load(infile.read())
        polyminos = {
            getattr(Mino, mino_type): Polymino(**mino_cfg)
            for mino_type, mino_cfg in cfg["polyminos"].items()
        }

        return cls(
            cfg["num_cols"],
            cfg["num_rows"],
            cfg["num_visible_rows"],
            cfg["num_previews"],
            polyminos,
        )


def rotate(coord: list[int], width: int, rot: int) -> list[int]:
    rot %= 4
    while rot > 0:
        coord = [width - coord[1] - 1, coord[0]]
        rot -= 1
    return coord
