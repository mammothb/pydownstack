"""Ruleset."""

from dataclasses import dataclass
from pathlib import Path

import yaml

from common.enum import Mino
from common.vector import Vector2D
from model.polymino import Polymino


@dataclass
class Ruleset:
    """Ruleset, determines the positions and kicks of the pieces."""

    difficulty: int
    num_cols: int
    num_rows: int
    num_rots: int
    num_visible_rows: int
    num_previews: int
    polyminos: dict[Mino, Polymino]

    @property
    def mino_types(self) -> list[Mino]:
        """All types of minos."""
        return list(self.polyminos.keys())

    def get_coords(self, mino: Mino, rot: int = 0) -> list[Vector2D]:
        """Returns the coordinates of the specified mino at the specified
        rotation.
        """
        poly = self.polyminos[mino]
        return [_rotate(coord, poly.width, rot) for coord in poly.coords]

    def get_origin(self, mino: Mino) -> Vector2D:
        """Returns the coordinates of the specified mino."""
        return self.polyminos[mino].origin

    @classmethod
    def from_config(cls, settings_path: Path, config_path: Path) -> "Ruleset":
        """Constructs Ruleset object from a config file."""
        with open(settings_path, encoding="utf8") as infile:
            setting = yaml.safe_load(infile.read())
        difficulty = min(max(int(setting["difficulty"]), 1), 4)

        with open(config_path, encoding="utf8") as infile:
            cfg = yaml.safe_load(infile.read())
        polyminos = {
            getattr(Mino, mino_type): Polymino.from_config(**mino_cfg)
            for mino_type, mino_cfg in cfg["polyminos"].items()
        }

        return cls(
            difficulty,
            cfg["num_cols"],
            cfg["num_rows"],
            cfg["num_rots"],
            cfg["num_visible_rows"],
            cfg["num_previews"],
            polyminos,
        )


def _rotate(coord: Vector2D, width: int, rot: int) -> Vector2D:
    """Rotates a 2D coordinate clockwise `rot` times."""
    rot %= 4
    while rot > 0:
        coord = Vector2D(coord.y, width - coord.x - 1)
        rot -= 1
    return coord
