import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Iterable

import pygame
from pygame import Color, Rect, Surface

from common.mino import Mino
from common.vector import Vector2D


@dataclass
class Cells:
    max_row: int = field(default=sys.maxsize)
    rects: dict[Mino, list[Rect]] = field(
        default_factory=lambda: defaultdict(list), init=False
    )

    def append(
        self,
        cells: Iterable[tuple[Vector2D, Mino]],
        transform: Callable[[Vector2D], Rect],
    ) -> None:
        for coord, mino in cells:
            if coord.y >= self.max_row:
                continue
            self.rects[mino].append(transform(coord))

    def clear(self) -> None:
        for key in self.rects:
            self.rects[key].clear()

    def paint(self, canvas: Surface, colors: dict[Mino, Color]) -> None:
        for c, rects in self.rects.items():
            color = colors[c]
            for rect in rects:
                pygame.draw.rect(canvas, color, rect)
