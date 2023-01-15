from dataclasses import dataclass
from enum import Enum


@dataclass
class Polymino:
    width: int
    coords: list[list[int]]
    origin: list[int]
    kicks: dict[int, list[list[int]]]


class Mino(Enum):
    J = 0
    L = 1
    S = 2
    Z = 3
    T = 4
    I = 5
    O = 6
    EMPTY = 7
