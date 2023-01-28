"""The current piece controlled by the player."""

import copy
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Iterable

from common.enum import Direction, Mino, Rotation

if TYPE_CHECKING:
    from common.vector import Vector2D
    from model.board import Board
    from model.ruleset import Ruleset


@dataclass
class BasePiece:
    """A barebones piece which contains only its mino type and default
    coordinates."""

    mino: Mino
    _all_coords: list[list["Vector2D"]]

    @property
    def base_coords(self) -> list["Vector2D"]:
        """The base coordinates without considering the origin."""
        return self._all_coords[0]


@dataclass
class GhostPiece(BasePiece):
    """A ghost piece which has movements but no rotation."""

    rot: int
    origin: "Vector2D"

    @property
    def coords(self) -> Iterable["Vector2D"]:
        """The coordinates occupied by the piece."""
        return (coord + self.origin for coord in self._all_coords[self.rot])

    def soft_drop(self, board: "Board") -> int:
        """Drops piece down until there is a collision.

        Returns:
            The number of rows moved.
        """
        steps = 0
        while self.try_move(Direction.DOWN, board):
            steps += 1
        return steps

    def try_move(self, displacement: "Vector2D", board: "Board") -> bool:
        """Returns a list of coordinates if moved by the provided
        `displacement`.
        """
        tmp = copy.deepcopy(self)
        tmp._move(displacement)  # pylint: disable=protected-access
        if not board.has_collision(tmp.coords):
            self._move(displacement)
            return True
        return False

    def _move(self, displacement: "Vector2D") -> None:
        self.origin += displacement


@dataclass
class Piece(GhostPiece):
    """The current piece controlled by the player."""

    ruleset: InitVar["Ruleset"]

    _num_rots: int = field(init=False)
    _kicks: dict[Rotation, dict[int, list["Vector2D"]]] = field(init=False)

    def __init__(self, ruleset: "Ruleset", mino: Mino) -> None:
        all_coords = [ruleset.get_coords(mino, rot) for rot in range(ruleset.num_rots)]
        super().__init__(mino, all_coords, 0, ruleset.get_origin(mino))
        self.__post_init__(ruleset)

    def __post_init__(self, ruleset: "Ruleset") -> None:
        self._num_rots = ruleset.num_rots
        self._kicks = ruleset.polyminos[self.mino].kicks

    @property
    def base(self) -> "BasePiece":
        """A ghost version of the current, which contains less data."""
        return BasePiece(self.mino, self._all_coords)

    @property
    def ghost(self) -> "GhostPiece":
        """A ghost version of the current, which contains less data."""
        return GhostPiece(self.mino, self._all_coords, self.rot, self.origin)

    def try_rotate(self, dr: int, board: "Board") -> bool:
        """Returns possible a list of possible coordinates after rotating by
        `dr`.
        """
        rotation = Rotation.CW if dr > 0 else Rotation.CCW
        rot_dst = (self.rot + dr) % 4
        for displacement in self._get_kicks(rotation, rot_dst):
            tmp = copy.deepcopy(self)
            tmp._rotate(displacement, dr)  # pylint: disable=protected-access
            if not board.has_collision(tmp.coords):
                self._rotate(displacement, dr)
                return True
        return False

    def _get_kicks(self, rotation: Rotation, rot_dst: int) -> list["Vector2D"]:
        """Returns the kick data for the mino at the specified rotation
        configuration.
        """
        if rotation not in self._kicks:
            return []
        return self._kicks[rotation][rot_dst]

    def _rotate(self, displacement: "Vector2D", dr: int) -> None:
        self._move(displacement)
        self.rot = (self.rot + dr) % self._num_rots
