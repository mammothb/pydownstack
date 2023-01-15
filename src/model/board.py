from dataclasses import dataclass, field
from typing import Union

from model.line import Line
from model.piece import Piece
from model.polymino import Mino
from model.vector import Direction, Vector2D


@dataclass
class Board:
    num_cols: int
    num_rows: int
    lines: list[Line] = field(init=False)

    def __post_init__(self) -> None:
        self.lines = [Line(self.num_cols) for _ in range(self.num_rows)]

    def __getitem__(self, coord: Vector2D) -> Mino:
        if not 0 <= coord.y < self.num_rows or not 0 <= coord.x < self.num_cols:
            raise IndexError
        return self.lines[coord.y][coord.x]

    def __setitem__(self, coord: Vector2D, mino: Mino) -> None:
        self.lines[coord.y][coord.x] = mino

    def finalize(self, piece: Piece) -> None:
        for coord in piece.coords:
            self[coord] = piece.mino

    def has_collision(self, target: Union[Piece, list[Vector2D]]) -> bool:
        """Checks if the provided `target` has collision with any cells in the
        board or the walls.
        """
        coords = target.coords if isinstance(target, Piece) else target
        try:
            return any(self[coord] != Mino.EMPTY for coord in coords)
        except IndexError:
            return True

    def move_horizontal(self, piece: Piece, direction: Vector2D) -> bool:
        if self.has_collision(piece.try_move(direction)):
            return False
        piece.move(direction)
        return True

    def soft_drop(self, piece: Piece) -> int:
        steps = 0
        while not self.has_collision(piece.try_move(Direction.DOWN)):
            piece.move(Direction.DOWN)
            steps += 1

        return steps
