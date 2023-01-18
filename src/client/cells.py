"""Stores and renders cells in the board."""

import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Iterable

import pygame

if TYPE_CHECKING:
    from pygame import Color, Rect
    from pygame.surface import Surface

    from common.enum import CellStyle, Mino
    from common.vector import Vector2D


@dataclass
class Cells:
    """Stores and renders cells in the board."""

    max_row: int = field(default=sys.maxsize)
    rects: "dict[Mino, list[Rect]]" = field(
        default_factory=lambda: defaultdict(list), init=False
    )

    def append(
        self,
        cells: "Iterable[tuple[Vector2D, Mino]]",
        transform: "Callable[[Vector2D], Rect]",
    ) -> None:
        """Adds a rect if it's in a visible row."""
        for coord, mino in cells:
            if coord.y >= self.max_row:
                continue
            self.rects[mino].append(transform(coord))

    def clear(self) -> None:
        """Clears stored rects."""
        for key in self.rects:
            self.rects[key].clear()

    def paint(
        self,
        canvas: "Surface",
        colors: "dict[Mino, Color]",
        styles: "CellStyle | dict[Mino, CellStyle]",
    ) -> None:
        """Paints the canvas with at the specified rects with the specified
        colors and styles.
        """
        for mino, rects in self.rects.items():
            color = colors[mino]
            style = styles[mino] if isinstance(styles, dict) else styles
            for rect in rects:
                pygame.draw.rect(canvas, color, rect, style)
