from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame.font import Font
    from pygame.surface import Surface


@dataclass
class Label:
    text: str
    updated: bool = field(default=True, init=False)
    size: tuple[int, int] | None = field(default=None, init=False)
    surface: "Surface | None" = field(default=None, init=False)

    def paint(self, canvas: "Surface", top_left: tuple[int, int]) -> None:
        """Paints text surface onto canvas."""
        if self.surface is None:
            return
        canvas.blit(self.surface, top_left)

    def render(self, font: "Font") -> None:
        """Renders the text into a surface."""
        if not self.updated:
            return
        self.surface = font.render(self.text, True, (255, 255, 255))
        self.size = self.surface.get_size()
        self.updated = False

    def set_text(self, text: str) -> None:
        """Updates text and set flag to re-render."""
        self.text = text
        self.updated = True
